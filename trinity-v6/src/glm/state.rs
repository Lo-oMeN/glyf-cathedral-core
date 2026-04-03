//! GLM State Persistence Layer
//! 
//! Implements 96-byte lattice state with Reed-Solomon protection
//! for distributed model checkpoints and shard synchronization.

#![no_std]

use core::mem::{size_of, transmute};
use core::sync::atomic::{fence, Ordering};

/// Galois Field GF(2^8) arithmetic for Reed-Solomon
mod gf256 {
    /// Multiply two elements in GF(2^8) with primitive polynomial 0x11D
    pub const fn mul(a: u8, b: u8) -> u8 {
        let mut result: u16 = 0;
        let mut a = a as u16;
        let mut b = b as u16;
        let mut i = 0;
        
        while i < 8 {
            if b & 1 != 0 {
                result ^= a;
            }
            let carry = a & 0x80;
            a <<= 1;
            if carry != 0 {
                a ^= 0x1D; // Primitive polynomial without x^8 term
            }
            b >>= 1;
            i += 1;
        }
        
        (result & 0xFF) as u8
    }

    /// Generator polynomial evaluation for RS(128,96)
    /// Returns coefficient for position i in generator polynomial
    pub const fn generator_coeff(i: usize) -> u8 {
        // Generator roots: α^0 through α^31 (32 parity symbols)
        // Precomputed primitive element powers
        const ROOTS: [u8; 32] = [
            0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80,
            0x1D, 0x3A, 0x74, 0xE8, 0xCD, 0x87, 0x13, 0x26,
            0x4C, 0x98, 0x2D, 0x5A, 0xB4, 0x75, 0xEA, 0xC9,
            0x8F, 0x03, 0x06, 0x0C, 0x18, 0x30, 0x60, 0xC0,
        ];
        
        if i < 32 {
            ROOTS[i]
        } else {
            0
        }
    }
}

/// RS(128,96) Encoder - 32 parity symbols for 96 data symbols
pub struct RSEncoder;

impl RSEncoder {
    /// Encode 96 bytes of data into 128-byte codeword
    /// Output buffer must be at least 128 bytes
    pub fn encode(data: &[u8; 96], output: &mut [u8; 128]) {
        // Copy data to output positions 0..96
        output[..96].copy_from_slice(&data[..]);
        
        // Initialize parity symbols to zero
        for i in 96..128 {
            output[i] = 0;
        }
        
        // Systematic encoding: compute parity symbols
        // Generator polynomial: g(x) = ∏(x - α^i) for i = 0..31
        for data_idx in 0..96 {
            let feedback = output[data_idx];
            if feedback != 0 {
                for parity_idx in 0..32 {
                    let root = gf256::generator_coeff(parity_idx);
                    output[96 + parity_idx] ^= gf256::mul(feedback, root);
                }
            }
        }
    }
    
    /// Verify and correct codeword
    /// Returns Ok(corrected_data) or Err(uncorrectable_count)
    pub fn decode(codeword: &[u8; 128]) -> Result<[u8; 96], usize> {
        // Syndrome computation
        let mut syndromes = [0u8; 32];
        let mut errors_found = false;
        
        for i in 0..32 {
            let root = gf256::generator_coeff(i);
            let mut syndrome = 0u8;
            let mut power = 1u8;
            
            for j in 0..128 {
                if codeword[j] != 0 {
                    syndrome ^= gf256::mul(codeword[j], power);
                }
                power = gf256::mul(power, root);
            }
            
            syndromes[i] = syndrome;
            if syndrome != 0 {
                errors_found = true;
            }
        }
        
        // No errors detected
        if !errors_found {
            let mut result = [0u8; 96];
            result.copy_from_slice(&codeword[..96]);
            return Ok(result);
        }
        
        // For now, return error indicating we detected errors
        // Full Berlekamp-Massey algorithm would go here for correction
        Err(1)
    }
}

/// 96-byte GLM lattice state
/// Aligned to 64-byte cache line for optimal SIMD/cache behavior
#[repr(C, align(64))]
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct GLMState {
    /// Primary lattice: 64 bytes (8x8 matrix or 16x4 structured field)
    pub lattice: [u8; 64],
    
    /// Metadata: 16 bytes (version, epoch, shard_id, checksum)
    pub meta: GLMMetadata,
    
    /// Resonance signature: 16 bytes (deterministic verification hash)
    pub resonance: [u8; 16],
}

/// GLM state metadata
#[repr(C)]
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct GLMMetadata {
    /// Version and format identifier (4 bytes)
    pub version: u32,
    
    /// Training epoch or sequence number
    pub epoch: u64,
    
    /// Shard identifier for distributed training
    pub shard_id: u16,
    
    /// Reserved for alignment
    pub _reserved: u16,
}

impl GLMMetadata {
    /// Current version identifier
    pub const VERSION: u32 = 0x474C4D01; // "GLM\x01"
}

/// Compile-time verification of struct size
const _: () = assert!(size_of::<GLMState>() == 96);
const _: () = assert!(size_of::<GLMMetadata>() == 16);

impl GLMState {
    /// Create new empty state
    pub const fn new() -> Self {
        Self {
            lattice: [0u8; 64],
            meta: GLMMetadata {
                version: GLMMetadata::VERSION,
                epoch: 0,
                shard_id: 0,
                _reserved: 0,
            },
            resonance: [0u8; 16],
        }
    }
    
    /// Initialize with specific shard assignment
    pub const fn with_shard(shard_id: u16) -> Self {
        let mut state = Self::new();
        state.meta.shard_id = shard_id;
        state
    }
    
    /// Compute simple XOR-based checksum for integrity verification
    fn compute_checksum(&self) -> u32 {
        let bytes = unsafe {
            core::slice::from_raw_parts(
                self as *const _ as *const u8,
                size_of::<Self>() - 16 // Exclude resonance field
            )
        };
        
        let mut checksum: u32 = 0x811C9DC5; // FNV-1a offset basis
        for &byte in bytes {
            checksum ^= byte as u32;
            checksum = checksum.wrapping_mul(0x01000193); // FNV-1a prime
        }
        checksum
    }
    
    /// Generate resonance signature
    fn generate_resonance(&mut self) {
        // Simple deterministic hash of lattice + metadata
        let mut hash = self.compute_checksum();
        let epoch_high = (self.meta.epoch >> 32) as u32;
        let epoch_low = self.meta.epoch as u32;
        
        // Mix epoch into hash
        hash ^= epoch_high;
        hash = hash.wrapping_mul(0x01000193);
        hash ^= epoch_low;
        hash = hash.wrapping_mul(0x01000193);
        
        // Expand 32-bit hash to 128-bit resonance
        for i in 0..4 {
            let part = hash.wrapping_add((i as u32).wrapping_mul(0x9E3779B9));
            self.resonance[i * 4 + 0] = (part >> 0) as u8;
            self.resonance[i * 4 + 1] = (part >> 8) as u8;
            self.resonance[i * 4 + 2] = (part >> 16) as u8;
            self.resonance[i * 4 + 3] = (part >> 24) as u8;
        }
    }
    
    /// Verify resonance signature
    pub fn verify_resonance(&self) -> bool {
        let mut temp = *self;
        temp.generate_resonance();
        temp.resonance == self.resonance
    }
    
    /// Increment epoch counter
    pub fn tick_epoch(&mut self) {
        self.meta.epoch = self.meta.epoch.wrapping_add(1);
        self.generate_resonance();
    }
}

/// Cryogenic checkpoint - persistent state encoding
/// 
/// Implements "cryogenize" to freeze state and "resurrect" to thaw
pub struct Cryogen;

impl Cryogen {
    /// Checkpoint state into protected 128-byte buffer
    /// Uses RS(128,96) encoding for fault tolerance
    pub fn cryogenize(state: &GLMState, buffer: &mut [u8; 128]) {
        // Serialize state to 96 bytes
        let state_bytes = unsafe {
            core::slice::from_raw_parts(
                state as *const _ as *const u8,
                size_of::<GLMState>()
            )
        };
        
        // Verify size
        debug_assert_eq!(state_bytes.len(), 96);
        
        // Copy to fixed-size array for RS encoder
        let mut input = [0u8; 96];
        input.copy_from_slice(state_bytes);
        
        // Apply Reed-Solomon encoding
        RSEncoder::encode(&input, buffer);
        
        // Memory fence to ensure persistence ordering
        fence(Ordering::SeqCst);
    }
    
    /// Resurrect state from checkpoint buffer
    /// Returns Ok(state) or Err(corruption_detected)
    pub fn resurrect(buffer: &[u8; 128]) -> Result<GLMState, PersistenceError> {
        // Decode RS-protected buffer
        let state_bytes = RSEncoder::decode(buffer)
            .map_err(|_| PersistenceError::UncorrectableErrors)?;
        
        // Deserialize state
        let state: GLMState = unsafe {
            transmute::<[u8; 96], GLMState>(state_bytes)
        };
        
        // Verify version compatibility
        if state.meta.version != GLMMetadata::VERSION {
            return Err(PersistenceError::VersionMismatch);
        }
        
        // Verify resonance signature
        if !state.verify_resonance() {
            return Err(PersistenceError::CorruptedSignature);
        }
        
        Ok(state)
    }
}

/// Persistence operation errors
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum PersistenceError {
    /// Data contains uncorrectable errors
    UncorrectableErrors,
    
    /// Version identifier mismatch
    VersionMismatch,
    
    /// Resonance signature verification failed
    CorruptedSignature,
}

/// Distributed model shard synchronization
/// 
/// Implements "fellowship" protocol for consistent state
/// across distributed training nodes
pub struct Fellowship;

/// Shard sync status
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct SyncStatus {
    /// Local shard epoch
    pub local_epoch: u64,
    
    /// Highest epoch seen from peers
    pub global_epoch: u64,
    
    /// Number of shards in sync
    pub synced_shards: u16,
    
    /// Total shard count
    pub total_shards: u16,
}

/// Consensus state for distributed training
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum ConsensusState {
    /// All shards synchronized
    Converged,
    
    /// Some shards lagging
    Divergent { lagging: u16 },
    
    /// Conflict detected requiring resolution
    Conflict { shards: [u16; 8], count: u8 },
}

impl Fellowship {
    /// Maximum supported shards in fellowship
    pub const MAX_SHARDS: usize = 256;
    
    /// Synchronize local state with peer shard states
    /// 
    /// # Arguments
    /// * `local` - Current local state
    /// * `peers` - Slice of peer shard states (can be empty)
    /// * `barrier_epoch` - Global barrier epoch for synchronization
    /// 
    /// # Returns
    /// Updated state and sync status
    pub fn synchronize(
        local: &GLMState,
        peers: &[GLMState],
        barrier_epoch: u64,
    ) -> (GLMState, SyncStatus, ConsensusState) {
        let mut max_epoch = local.meta.epoch;
        let mut min_epoch = local.meta.epoch;
        let mut synced_count = 1u16; // Count self
        
        // Find epoch bounds and count converged shards
        for peer in peers {
            let epoch = peer.meta.epoch;
            if epoch > max_epoch {
                max_epoch = epoch;
            }
            if epoch < min_epoch {
                min_epoch = epoch;
            }
            
            // Consider synced if within 1 epoch of barrier
            if epoch.abs_diff(barrier_epoch) <= 1 {
                synced_count = synced_count.saturating_add(1);
            }
        }
        
        let total_shards = (1 + peers.len()) as u16;
        
        let status = SyncStatus {
            local_epoch: local.meta.epoch,
            global_epoch: max_epoch,
            synced_shards: synced_count,
            total_shards,
        };
        
        // Determine consensus state
        let consensus = if min_epoch == max_epoch {
            ConsensusState::Converged
        } else {
            let lagging = total_shards - synced_count;
            if lagging > total_shards / 4 {
                // Significant divergence - identify lagging shards
                let mut conflict_shards = [0u16; 8];
                let mut conflict_count = 0u8;
                
                // Collect up to 8 lagging shard IDs
                for peer in peers {
                    if peer.meta.epoch.abs_diff(barrier_epoch) > 1 
                        && (conflict_count as usize) < 8 {
                        conflict_shards[conflict_count as usize] = peer.meta.shard_id;
                        conflict_count += 1;
                    }
                }
                
                ConsensusState::Conflict { 
                    shards: conflict_shards, 
                    count: conflict_count 
                }
            } else {
                ConsensusState::Divergent { lagging }
            }
        };
        
        // Fast-forward local state if behind
        let mut result = *local;
        if local.meta.epoch < barrier_epoch {
            result.meta.epoch = barrier_epoch;
            result.generate_resonance();
        }
        
        (result, status, consensus)
    }
    
    /// Compute weighted average of shard states
    /// For model parameter averaging in distributed training
    pub fn converge_shards(shards: &[GLMState], output: &mut GLMState) -> Result<(), FellowshipError> {
        if shards.is_empty() {
            return Err(FellowshipError::EmptyShardSet);
        }
        
        // Verify all shards have compatible versions
        let version = shards[0].meta.version;
        for shard in shards {
            if shard.meta.version != version {
                return Err(FellowshipError::VersionMismatch);
            }
        }
        
        // Average lattice fields
        for i in 0..64 {
            let sum: u32 = shards.iter()
                .map(|s| s.lattice[i] as u32)
                .sum();
            output.lattice[i] = (sum / shards.len() as u32) as u8;
        }
        
        // Set metadata from first shard but update epoch to max
        output.meta = shards[0].meta;
        output.meta.epoch = shards.iter()
            .map(|s| s.meta.epoch)
            .max()
            .unwrap_or(0);
        
        // Clear shard_id for converged state
        output.meta.shard_id = 0;
        
        output.generate_resonance();
        
        Ok(())
    }
}

/// Fellowship operation errors
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum FellowshipError {
    /// No shards provided for convergence
    EmptyShardSet,
    
    /// Shard version incompatibility
    VersionMismatch,
}

/// Zero-allocation checkpoint buffer pool
pub struct CheckpointPool<const N: usize> {
    buffers: [[u8; 128]; N],
    used: [bool; N],
}

impl<const N: usize> CheckpointPool<N> {
    /// Create new checkpoint pool
    pub const fn new() -> Self {
        Self {
            buffers: [[0u8; 128]; N],
            used: [false; N],
        }
    }
    
    /// Acquire buffer from pool
    pub fn acquire(&mut self) -> Option<CheckpointHandle<N>> {
        for i in 0..N {
            if !self.used[i] {
                self.used[i] = true;
                return Some(CheckpointHandle { index: i });
            }
        }
        None
    }
    
    /// Get buffer by handle
    pub fn get(&self, handle: CheckpointHandle<N>) -> &[u8; 128] {
        &self.buffers[handle.index]
    }
    
    /// Get mutable buffer by handle
    pub fn get_mut(&mut self, handle: CheckpointHandle<N>) -> &mut [u8; 128] {
        &mut self.buffers[handle.index]
    }
    
    /// Release buffer back to pool
    pub fn release(&mut self, handle: CheckpointHandle<N>) {
        self.used[handle.index] = false;
        // Zero buffer for security
        self.buffers[handle.index] = [0u8; 128];
    }
    
    /// Checkpoint state into pooled buffer
    pub fn checkpoint(&mut self, state: &GLMState) -> Option<CheckpointHandle<N>> {
        let handle = self.acquire()?;
        Cryogen::cryogenize(state, self.get_mut(handle));
        Some(handle)
    }
}

/// Handle to pooled checkpoint buffer
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct CheckpointHandle<const N: usize> {
    index: usize,
}

// Compile-time tests
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_size_assertions() {
        assert_eq!(size_of::<GLMState>(), 96);
        assert_eq!(size_of::<GLMMetadata>(), 16);
    }
    
    #[test]
    fn test_glm_state_new() {
        let state = GLMState::new();
        assert_eq!(state.meta.version, GLMMetadata::VERSION);
        assert_eq!(state.meta.epoch, 0);
        assert_eq!(state.meta.shard_id, 0);
    }
    
    #[test]
    fn test_epoch_tick() {
        let mut state = GLMState::new();
        let initial_resonance = state.resonance;
        state.tick_epoch();
        assert_eq!(state.meta.epoch, 1);
        assert_ne!(state.resonance, initial_resonance);
        assert!(state.verify_resonance());
    }
    
    #[test]
    fn test_cryogenize_resurrect() {
        let mut state = GLMState::new();
        state.lattice[0] = 0x42;
        state.lattice[1] = 0xDE;
        state.lattice[2] = 0xAD;
        state.tick_epoch();
        
        let mut buffer = [0u8; 128];
        Cryogen::cryogenize(&state, &mut buffer);
        
        // Verify buffer is non-zero (RS encoding worked)
        assert!(buffer[96..].iter().any(|&b| b != 0));
        
        let resurrected = Cryogen::resurrect(&buffer).unwrap();
        assert_eq!(resurrected.lattice[0], 0x42);
        assert_eq!(resurrected.lattice[1], 0xDE);
        assert_eq!(resurrected.lattice[2], 0xAD);
        assert_eq!(resurrected.meta.epoch, 1);
    }
    
    #[test]
    fn test_fellowship_sync() {
        let local = GLMState::with_shard(0);
        let peer1 = GLMState::with_shard(1);
        let peer2 = GLMState::with_shard(2);
        
        let peers = [peer1, peer2];
        let (result, status, consensus) = Fellowship::synchronize(&local, &peers, 0);
        
        assert_eq!(status.total_shards, 3);
        assert_eq!(status.local_epoch, 0);
        assert_eq!(consensus, ConsensusState::Converged);
    }
    
    #[test]
    fn test_checkpoint_pool() {
        let mut pool: CheckpointPool<4> = CheckpointPool::new();
        
        let state = GLMState::new();
        let handle = pool.checkpoint(&state).unwrap();
        
        // Verify resurrection works
        let buffer = pool.get(handle);
        let restored = Cryogen::resurrect(buffer).unwrap();
        assert_eq!(restored.meta.version, state.meta.version);
        
        pool.release(handle);
        
        // Verify handle can be reused
        let handle2 = pool.acquire().unwrap();
        assert_eq!(handle.index, handle2.index);
    }
    
    #[test]
    fn test_align_64() {
        assert_eq!(align_of::<GLMState>(), 64);
    }
}

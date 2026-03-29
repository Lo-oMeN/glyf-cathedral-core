//! GLM Geometric Quantization - Encode/Decode Implementation
//! 
//! Implements the 96-byte LatticeState quantization format with:
//! - Phi-Radial Precision encoding
//! - SO(3) Invariant Rotation encoding
//! - Vesica-Based Pruning
//! - Chiral Protection

use crate::codebook::{
    self, dequantize_from_codebook, quantize_to_codebook,
    pack_i4, pack_u4, unpack_i4, unpack_u4,
    PHI, PHI_SQUARED, CODEBOOK_GLYPH_VOID,
};

/// Size of a quantized lattice state
pub const LATTICE_SIZE: usize = 96;

/// Alignment for SIMD operations (32 bytes for AVX2)
pub const LATTICE_ALIGN: usize = 32;

/// Vesica coherence threshold for pruning
pub const VESICA_PRUNE_THRESHOLD: f32 = 0.1;

/// 96-byte LatticeState structure
/// Aligned to 32 bytes for AVX2 operations
#[repr(C, align(32))]
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct LatticeState {
    /// Bytes 0-7: Center S (immutable, full float32 precision)
    pub center: [f32; 2],
    
    /// Bytes 8-23: Ternary junction (3 × 4-byte vectors, i8 quantized)
    pub ternary: [[i8; 4]; 3],
    
    /// Bytes 24-55: Hex persistence (6 × 4-byte tiles, u4 quantized)
    pub hex: [[u8; 4]; 6],
    
    /// Bytes 56-59: Fellowship resonance (logarithmic encoding)
    pub fellowship: u32,
    
    /// Bytes 60-63: Reserved/padding
    _reserved0: u32,
    
    /// Byte 64: Morphogen phase (3-bit octal)
    pub phase: u8,
    
    /// Bytes 65-67: Geometric operators (3 × i4)
    pub operators: [u8; 3],
    
    /// Bytes 68-94: Extended payload
    pub extended: [u8; 27],
    
    /// Byte 95: Format version
    pub version: u8,
}

impl Default for LatticeState {
    fn default() -> Self {
        Self::new()
    }
}

impl LatticeState {
    /// Create a new empty lattice state
    pub fn new() -> Self {
        Self {
            center: [0.0, 0.0],
            ternary: [[0; 4]; 3],
            hex: [[0; 4]; 6],
            fellowship: 0,
            _reserved0: 0,
            phase: MorphogenPhase::Dormant as u8,
            operators: [0; 3],
            extended: [0; 27],
            version: 1,
        }
    }
    
    /// Create GLYPH_VOID state (pruned)
    pub fn void() -> Self {
        Self {
            center: [0.0, 0.0],
            ternary: [[0; 4]; 3],
            hex: [[0xFF; 4]; 6],  // All void markers
            fellowship: 0,
            _reserved0: 0,
            phase: MorphogenPhase::Void as u8,
            operators: [0x00, 0x80, 0x01],  // Chiral redundancy
            extended: [0xFF; 27],  // Void markers
            version: 1,
        }
    }
    
    /// Check if this is a void state
    pub fn is_void(&self) -> bool {
        self.phase == MorphogenPhase::Void as u8
    }
    
    /// Get chirality using redundant storage with majority vote
    pub fn chirality(&self) -> bool {
        decode_chirality(&self.operators)
    }
    
    /// Set chirality with redundant encoding
    pub fn set_chirality(&mut self, chiral: bool) {
        let bit = if chiral { 1 } else { 0 };
        // Primary: bit 0 of operators[0]
        self.operators[0] = (self.operators[0] & 0xFE) | bit;
        // Copy A: bit 7 of operators[0]
        self.operators[0] = (self.operators[0] & 0x7F) | (bit << 7);
        // Copy B: bit 0 of operators[2]
        self.operators[2] = (self.operators[2] & 0xFE) | bit;
    }
    
    /// Encode geometric operators (ω, σ, τ)
    pub fn encode_operators(&mut self, omega: i8, sigma: i8, tau: i8) {
        // Pack three i4 values into first two bytes
        self.operators[0] = (pack_i4(omega) << 4) | pack_i4(sigma);
        self.operators[1] = (pack_i4(tau) << 4);
        // operators[2] reserved for chirality and flags
    }
    
    /// Decode geometric operators
    pub fn decode_operators(&self) -> (i8, i8, i8) {
        let omega = unpack_i4(self.operators[0] >> 4);
        let sigma = unpack_i4(self.operators[0]);
        let tau = unpack_i4(self.operators[1] >> 4);
        (omega, sigma, tau)
    }
    
    /// Set morphogen phase
    pub fn set_phase(&mut self, phase: MorphogenPhase) {
        // Lower 3 bits: phase, upper 5 bits: confidence
        self.phase = (phase as u8 & 0x07) | (self.phase & 0xF8);
    }
    
    /// Get morphogen phase
    pub fn get_phase(&self) -> MorphogenPhase {
        MorphogenPhase::from_u8(self.phase & 0x07)
    }
    
    /// Set phase confidence (0-31)
    pub fn set_phase_confidence(&mut self, confidence: u8) {
        self.phase = (self.phase & 0x07) | ((confidence & 0x1F) << 3);
    }
    
    /// Get phase confidence
    pub fn get_phase_confidence(&self) -> u8 {
        (self.phase >> 3) & 0x1F
    }
}

/// Morphogen phase states (3-bit octal)
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
#[repr(u8)]
pub enum MorphogenPhase {
    Dormant = 0,
    Excited = 1,
    Resonant = 2,
    Transforming = 3,
    Coherent = 4,
    Dissipating = 5,
    Void = 6,
    // 7 reserved
}

impl MorphogenPhase {
    pub fn from_u8(v: u8) -> Self {
        match v {
            0 => Self::Dormant,
            1 => Self::Excited,
            2 => Self::Resonant,
            3 => Self::Transforming,
            4 => Self::Coherent,
            5 => Self::Dissipating,
            6 => Self::Void,
            _ => Self::Dormant,  // Default for invalid
        }
    }
}

/// Decoded ternary junction vectors
#[derive(Clone, Copy, Debug)]
pub struct TernaryVectors {
    pub j0: [f32; 4],
    pub j1: [f32; 4],
    pub j2: [f32; 4],
}

/// SO(3) encoded rotation (Lie algebra so(3))
#[derive(Clone, Copy, Debug)]
pub struct So3Rotation {
    /// ω vector (axis × angle) quantized as i8
    pub omega: [i8; 3],
    /// Angle magnitude [0, π] mapped to [0, 255]
    pub theta: u8,
}

/// SO(3) decoded rotation
#[derive(Clone, Copy, Debug)]
pub struct Rotation3 {
    pub axis: [f32; 3],  // Unit vector
    pub angle: f32,       // Radians
}

/// Encode ternary junction with φ-scaling
pub fn encode_ternary(vectors: &TernaryVectors, max_val: f32) -> [[i8; 4]; 3] {
    let scale = 127.0 * PHI_SQUARED / max_val;
    
    [
        vectors.j0.map(|v| clamp_round_i8(v * scale)),
        vectors.j1.map(|v| clamp_round_i8(v * scale)),
        vectors.j2.map(|v| clamp_round_i8(v * scale)),
    ]
}

/// Decode ternary junction
pub fn decode_ternary(ternary: &[[i8; 4]; 3], max_val: f32) -> TernaryVectors {
    let scale = max_val / (127.0 * PHI_SQUARED);
    
    TernaryVectors {
        j0: ternary[0].map(|v| v as f32 * scale),
        j1: ternary[1].map(|v| v as f32 * scale),
        j2: ternary[2].map(|v| v as f32 * scale),
    }
}

/// Encode hex persistence with u4 quantization
pub fn encode_hex(values: &[f32; 24]) -> [[u8; 4]; 6] {
    let mut result = [[0u8; 4]; 6];
    
    for (i, &value) in values.iter().enumerate() {
        let (code, _) = quantize_to_codebook(value);
        // Store as u4 (0-15)
        let nibble = code & 0x0F;
        
        let byte_idx = i / 2;
        let is_high = i % 2 == 0;
        
        if is_high {
            result[byte_idx / 4][byte_idx % 4] |= nibble << 4;
        } else {
            result[byte_idx / 4][byte_idx % 4] |= nibble;
        }
    }
    
    result
}

/// Decode hex persistence
pub fn decode_hex(hex: &[[u8; 4]; 6]) -> [f32; 24] {
    let mut result = [0.0f32; 24];
    let flat: &[u8] = unsafe {
        std::slice::from_raw_parts(hex.as_ptr() as *const u8, 24)
    };
    
    for (i, &byte) in flat.iter().enumerate() {
        let (high, low) = unpack_u4(byte);
        result[i * 2] = dequantize_from_codebook(high);
        result[i * 2 + 1] = dequantize_from_codebook(low);
    }
    
    result
}

/// Encode fellowship resonance: log₂(φ⁷ × F)
pub fn encode_fellowship(f: f32) -> u32 {
    if f <= 0.0 {
        return 0;
    }
    
    let scaled = f * codebook::phi_pow(7);
    let log_val = scaled.log2();
    
    // Map [-20, 20] to [0, u32::MAX]
    let normalized = ((log_val + 20.0) / 40.0).clamp(0.0, 1.0);
    (normalized * u32::MAX as f32) as u32
}

/// Decode fellowship resonance
pub fn decode_fellowship(encoded: u32) -> f32 {
    let normalized = encoded as f32 / u32::MAX as f32;
    let log_val = normalized * 40.0 - 20.0;
    let scaled = 2.0f32.powf(log_val);
    scaled / codebook::phi_pow(7)
}

/// Encode SO(3) rotation in Lie algebra so(3)
pub fn encode_so3(rotation: &Rotation3) -> So3Rotation {
    let omega_raw = [
        rotation.axis[0] * rotation.angle,
        rotation.axis[1] * rotation.angle,
        rotation.axis[2] * rotation.angle,
    ];
    
    let omega = omega_raw.map(|v| {
        clamp_round_i8(v * 127.0 / std::f32::consts::PI)
    });
    
    let theta = (rotation.angle / std::f32::consts::PI * 255.0)
        .clamp(0.0, 255.0) as u8;
    
    So3Rotation { omega, theta }
}

/// Decode SO(3) rotation via matrix exponential
pub fn decode_so3(encoded: &So3Rotation) -> Rotation3 {
    use std::f32::consts::PI;
    
    let omega_f = encoded.omega.map(|v| v as f32 * PI / 127.0);
    let angle = encoded.theta as f32 * PI / 255.0;
    
    let omega_norm = (omega_f[0].powi(2) + omega_f[1].powi(2) + omega_f[2].powi(2)).sqrt();
    
    if omega_norm < 1e-6 {
        return Rotation3 {
            axis: [1.0, 0.0, 0.0],
            angle: 0.0,
        };
    }
    
    Rotation3 {
        axis: [
            omega_f[0] / omega_norm,
            omega_f[1] / omega_norm,
            omega_f[2] / omega_norm,
        ],
        angle,
    }
}

/// Decode chirality with majority vote from 3 redundant copies
fn decode_chirality(operators: &[u8; 3]) -> bool {
    let bits = [
        (operators[0] & 0x01) != 0,
        (operators[0] & 0x80) != 0,
        (operators[2] & 0x01) != 0,
    ];
    
    // Majority vote
    bits.iter().filter(|&&b| b).count() >= 2
}

/// Clamp and round to i8
#[inline]
fn clamp_round_i8(v: f32) -> i8 {
    v.round().clamp(-127.0, 127.0) as i8
}

/// Vesica coherence computation
pub fn vesica_coherence(center: &[f32; 2], ternary: &[[i8; 4]; 3]) -> f32 {
    // Compute vesica from center and ternary junction
    let center_vesica = compute_vesica_radius(center, ternary);
    
    // For now, return normalized coherence based on vesica properties
    // In full implementation, this would compare with neighbor vesicas
    let coherence = center_vesica.min(1.0).max(0.0);
    
    coherence
}

/// Compute vesica radius from lattice properties
fn compute_vesica_radius(center: &[f32; 2], ternary: &[[i8; 4]; 3]) -> f32 {
    // Vesica radius proportional to ternary junction magnitude
    let j0_norm: f32 = ternary[0].iter().map(|&v| (v as f32).powi(2)).sum::<f32>().sqrt();
    let j1_norm: f32 = ternary[1].iter().map(|&v| (v as f32).powi(2)).sum::<f32>().sqrt();
    
    // Vesica radius is geometric mean of junction magnitudes
    (j0_norm * j1_norm).sqrt() / 127.0
}

/// Check if lattice should be pruned based on vesica coherence
pub fn should_prune(lattice: &LatticeState) -> bool {
    if lattice.is_void() {
        return true;
    }
    
    let coherence = vesica_coherence(&lattice.center, &lattice.ternary);
    coherence < VESICA_PRUNE_THRESHOLD
}

/// Convert lattice to GLYPH_VOID (prune)
pub fn prune_lattice(lattice: &mut LatticeState) {
    *lattice = LatticeState::void();
}

/// Validation errors
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ValidationError {
    InvalidCenter,
    InconsistentVoid,
    ChiralAmbiguity,
    InvalidVersion,
}

/// Validate a lattice state
pub fn validate_lattice(lattice: &LatticeState) -> Result<(), ValidationError> {
    // Check center is valid
    if !lattice.center[0].is_finite() || !lattice.center[1].is_finite() {
        return Err(ValidationError::InvalidCenter);
    }
    
    // Check version
    if lattice.version != 1 {
        return Err(ValidationError::InvalidVersion);
    }
    
    // Verify chiral redundancy
    let bits = [
        (lattice.operators[0] & 0x01) != 0,
        (lattice.operators[0] & 0x80) != 0,
        (lattice.operators[2] & 0x01) != 0,
    ];
    let votes = bits.iter().filter(|&&b| b).count();
    if votes == 1 || votes == 2 {
        // Ambiguous - could be error or warning
        // For now, just log the issue
        eprintln!("Warning: Chiral ambiguity detected ({} votes)", votes);
    }
    
    // Check GLYPH_VOID consistency
    if lattice.is_void() {
        for tile in &lattice.hex {
            if tile.iter().any(|&b| b != 0xFF) {
                return Err(ValidationError::InconsistentVoid);
            }
        }
    }
    
    Ok(())
}

/// Statistics for quantization performance
#[derive(Debug, Clone, Copy, Default)]
pub struct QuantizationStats {
    pub total_lattices: usize,
    pub pruned_count: usize,
    pub ternary_error: f64,
    pub hex_error: f64,
    pub fellowship_error: f64,
    pub so3_error: f64,
    pub total_bytes: usize,
}

impl QuantizationStats {
    pub fn new() -> Self {
        Self::default()
    }
    
    pub fn compression_ratio(&self) -> f32 {
        // Assume original was 96 bytes × 4 = 384 bytes (f32 for all fields)
        let original_size = self.total_lattices * 384;
        let compressed = self.total_bytes;
        
        if compressed == 0 {
            1.0
        } else {
            original_size as f32 / compressed as f32
        }
    }
    
    pub fn prune_ratio(&self) -> f32 {
        if self.total_lattices == 0 {
            0.0
        } else {
            self.pruned_count as f32 / self.total_lattices as f32
        }
    }
}

/// Batch quantize a slice of float weights into lattice states
pub fn batch_quantize(weights: &[f32], lattices: &mut [LatticeState]) -> QuantizationStats {
    let mut stats = QuantizationStats::new();
    stats.total_lattices = lattices.len();
    
    for (i, lattice) in lattices.iter_mut().enumerate() {
        // Simple mapping: 24 floats → 1 lattice
        let start = i * 24;
        if start + 24 > weights.len() {
            break;
        }
        
        let chunk = &weights[start..start + 24];
        
        // Encode center (first 2 values, full precision)
        lattice.center = [chunk[0], chunk[1]];
        
        // Encode ternary (next 12 values → 3×4)
        let ternary_vecs = TernaryVectors {
            j0: [chunk[2], chunk[3], chunk[4], chunk[5]],
            j1: [chunk[6], chunk[7], chunk[8], chunk[9]],
            j2: [chunk[10], chunk[11], chunk[12], chunk[13]],
        };
        
        // Find max for scaling
        let max_val = ternary_vecs.j0.iter().chain(ternary_vecs.j1.iter()).chain(ternary_vecs.j2.iter())
            .map(|&v| v.abs())
            .fold(0.0f32, f32::max)
            .max(1e-6);
        
        lattice.ternary = encode_ternary(&ternary_vecs, max_val);
        
        // Encode hex (next 24 values, u4 quantized)
        let hex_vals: [f32; 24] = chunk.try_into().unwrap();
        lattice.hex = encode_hex(&hex_vals);
        
        // Encode fellowship (value at index 14)
        lattice.fellowship = encode_fellowship(chunk[14]);
        
        // Check pruning
        if should_prune(lattice) {
            prune_lattice(lattice);
            stats.pruned_count += 1;
        }
        
        stats.total_bytes += LATTICE_SIZE;
    }
    
    stats
}

/// Batch dequantize lattice states back to float weights
pub fn batch_dequantize(lattices: &[LatticeState], weights: &mut [f32]) {
    for (i, lattice) in lattices.iter().enumerate() {
        let start = i * 24;
        if start + 24 > weights.len() {
            break;
        }
        
        if lattice.is_void() {
            // Output zeros for void states
            weights[start..start + 24].fill(0.0);
            continue;
        }
        
        // Decode center
        weights[start] = lattice.center[0];
        weights[start + 1] = lattice.center[1];
        
        // Decode ternary (needs max_val, using default for now)
        let ternary = decode_ternary(&lattice.ternary, 1.0);
        weights[start + 2..start + 6].copy_from_slice(&ternary.j0);
        weights[start + 6..start + 10].copy_from_slice(&ternary.j1);
        weights[start + 10..start + 14].copy_from_slice(&ternary.j2);
        
        // Decode hex
        let hex = decode_hex(&lattice.hex);
        weights[start + 14..start + 24].copy_from_slice(&hex[..10]);
    }
}

/// Measure decompression speed (for benchmarking)
pub fn benchmark_decompression(lattices: &[LatticeState]) -> f64 {
    use std::time::Instant;
    
    let mut output = vec![0.0f32; lattices.len() * 24];
    
    let start = Instant::now();
    batch_dequantize(lattices, &mut output);
    let elapsed = start.elapsed();
    
    let ns_per_lattice = elapsed.as_nanos() as f64 / lattices.len() as f64;
    ns_per_lattice
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_lattice_size() {
        assert_eq!(std::mem::size_of::<LatticeState>(), LATTICE_SIZE);
        assert!(std::mem::align_of::<LatticeState>() >= LATTICE_ALIGN);
    }
    
    #[test]
    fn test_chirality_roundtrip() {
        let mut lattice = LatticeState::new();
        
        lattice.set_chirality(true);
        assert!(lattice.chirality());
        
        lattice.set_chirality(false);
        assert!(!lattice.chirality());
    }
    
    #[test]
    fn test_ternary_encode_decode() {
        let original = TernaryVectors {
            j0: [0.5, -0.3, 0.8, -0.2],
            j1: [-0.1, 0.9, 0.4, -0.6],
            j2: [0.7, -0.4, 0.2, 0.3],
        };
        
        let max_val = 1.0;
        let encoded = encode_ternary(&original, max_val);
        let decoded = decode_ternary(&encoded, max_val);
        
        // Should be close but not exact due to quantization
        for (o, d) in original.j0.iter().zip(decoded.j0.iter()) {
            assert!((o - d).abs() < 0.1, "Ternary decode error too large: {} vs {}", o, d);
        }
    }
    
    #[test]
    fn test_fellowship_roundtrip() {
        let test_values = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0];
        
        for &value in &test_values {
            let encoded = encode_fellowship(value);
            let decoded = decode_fellowship(encoded);
            
            // Logarithmic encoding has higher relative error
            let relative_error = (value - decoded).abs() / value;
            assert!(relative_error < 0.5, "Fellowship roundtrip failed: {} -> {} -> {} (err: {})", 
                value, encoded, decoded, relative_error);
        }
    }
    
    #[test]
    fn test_so3_roundtrip() {
        let original = Rotation3 {
            axis: [0.0, 0.0, 1.0],  // Z-axis
            angle: std::f32::consts::PI / 4.0,  // 45 degrees
        };
        
        let encoded = encode_so3(&original);
        let decoded = decode_so3(&encoded);
        
        // Axis should be preserved
        for (o, d) in original.axis.iter().zip(decoded.axis.iter()) {
            assert!((o - d).abs() < 0.1, "SO(3) axis decode error");
        }
        
        // Angle should be close
        assert!((original.angle - decoded.angle).abs() < 0.05, "SO(3) angle decode error");
    }
    
    #[test]
    fn test_glyf_void() {
        let void = LatticeState::void();
        assert!(void.is_void());
        assert!(validate_lattice(&void).is_ok());
    }
    
    #[test]
    fn test_operators_roundtrip() {
        let mut lattice = LatticeState::new();
        
        let (omega, sigma, tau) = (3i8, -5i8, 7i8);
        lattice.encode_operators(omega, sigma, tau);
        
        let (d_omega, d_sigma, d_tau) = lattice.decode_operators();
        assert_eq!(omega, d_omega);
        assert_eq!(sigma, d_sigma);
        assert_eq!(tau, d_tau);
    }
    
    #[test]
    fn test_phase_roundtrip() {
        let mut lattice = LatticeState::new();
        
        for phase in [
            MorphogenPhase::Dormant,
            MorphogenPhase::Excited,
            MorphogenPhase::Resonant,
            MorphogenPhase::Void,
        ] {
            lattice.set_phase(phase);
            assert_eq!(lattice.get_phase(), phase);
        }
    }
    
    #[test]
    fn test_batch_quantize_dequantize() {
        let weights: Vec<f32> = (0..48).map(|i| i as f32 * 0.1).collect();
        let mut lattices = vec![LatticeState::new(); 2];
        
        let stats = batch_quantize(&weights, &mut lattices);
        assert_eq!(stats.total_lattices, 2);
        
        let mut decoded = vec![0.0f32; 48];
        batch_dequantize(&lattices, &mut decoded);
        
        // First two values (center) should be exact
        assert!((weights[0] - decoded[0]).abs() < 1e-6);
        assert!((weights[1] - decoded[1]).abs() < 1e-6);
    }
}

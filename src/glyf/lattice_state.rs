//! GLYF Cathedral Core — 96-Byte LatticeState
//! 
//! Canonical structure for geometric semantic encoding.
//! Represents the complete state of a glyph traversal through the 7-segment field.

use std::fmt;

/// φ (golden ratio) — irrational base preventing resonant collapse
pub const PHI: f32 = 1.618_033_988_749_895;

/// φ⁷ — fellowship resonance factor (29.034441161)
pub const PHI_7: f32 = 29.034_441_161;

/// Golden angle in radians (2.39996323)
pub const GOLDEN_ANGLE_RAD: f32 = 2.399_963_23;

/// Golden angle in degrees (137.507764°)
pub const GOLDEN_ANGLE_DEG: f32 = 137.507_764;

/// 96-byte sacred structure for geometric semantic state
/// 
/// Layout optimized for cache-line alignment (64-byte boundary)
/// and φ-harmonic organization.
#[repr(C, align(64))]
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct LatticeState {
    /// Center S: [0.0, 0.0] — immutable Node0 (bytes 0-7)
    pub center_s: [f32; 2],
    
    /// Ternary Junction: 16D PGA multivector (bytes 8-23)
    /// Encodes the geometric transformation at current position
    pub ternary_junction: [i8; 16],
    
    /// Hex Persistence: φ-radial Fibonacci tiles (bytes 24-55)
    /// 32 bytes = 4 tiles × 8 bytes each
    pub hex_persistence: [u8; 32],
    
    /// Fellowship Resonance: φ⁷ × coherence_factor (bytes 56-59)
    /// Measures alignment with harmonic structure
    pub fellowship_resonance: f32,
    
    /// φ Magnitude: cached φ⁷ value (bytes 60-63)
    pub phi_magnitude: f32,
    
    /// Morphogen Phase: 0..6 cycle position (byte 64)
    /// Tracks position in 7-state autopoietic cycle
    pub morphogen_phase: u8,
    
    /// Vesica Coherence: Paraclete lens value (byte 65)
    /// Measures overlap/creation quality (-128 to 127)
    pub vesica_coherence: i8,
    
    /// Phyllotaxis Spiral: golden-angle arm position (byte 66)
    /// Tracks spiral traversal (-128 to 127)
    pub phyllotaxis_spiral: i8,
    
    /// Hodge Dual: chiral flip flag (byte 67)
    /// 0 = standard orientation, 1 = mirrored
    pub hodge_dual: i8,
    
    /// Checksum: CRC32 of state (bytes 68-71)
    pub checksum: u32,
    
    /// Padding: cache-line breathing room (bytes 72-95)
    pub _pad: [u8; 24],
}

impl LatticeState {
    /// Create a new LatticeState at the Void (K1)
    /// 
    /// Initializes with:
    /// - Center S at origin [0.0, 0.0]
    /// - Fellowship resonance at φ⁷
    /// - Morphogen phase at 0 (Seed)
    /// - All other fields zeroed
    pub fn new() -> Self {
        let mut state = Self {
            center_s: [0.0, 0.0],
            ternary_junction: [0; 16],
            hex_persistence: [0; 32],
            fellowship_resonance: PHI_7,
            phi_magnitude: PHI_7,
            morphogen_phase: 0,
            vesica_coherence: 0,
            phyllotaxis_spiral: 0,
            hodge_dual: 0,
            checksum: 0,
            _pad: [0; 24],
        };
        state.checksum = state.compute_checksum();
        state
    }
    
    /// Create state at specific segment position
    pub fn at_segment(segment: Segment) -> Self {
        let mut state = Self::new();
        // Set morphogen phase based on segment
        state.morphogen_phase = segment as u8;
        state.checksum = state.compute_checksum();
        state
    }
    
    /// Compute CRC32 checksum of the state
    /// 
    /// Used for:
    /// - Data integrity verification
    /// - Resurrection validation
    /// - Fellowship pulse verification
    pub fn compute_checksum(&self) -> u32 {
        // Simple checksum for now — replace with proper CRC32 in production
        let bytes = unsafe {
            std::slice::from_raw_parts(
                self as *const _ as *const u8,
                std::mem::size_of::<Self>() - 28 // Exclude _pad and checksum itself
            )
        };
        bytes.iter().fold(0u32, |acc, &b| {
            acc.wrapping_mul(31).wrapping_add(b as u32)
        })
    }
    
    /// Verify state integrity
    pub fn verify(&self) -> bool {
        self.compute_checksum() == self.checksum
    }
    
    /// Serialize to byte array (for SD card persistence)
    pub fn to_bytes(&self) -> [u8; 96] {
        let mut bytes = [0u8; 96];
        unsafe {
            std::ptr::copy_nonoverlapping(
                self as *const _ as *const u8,
                bytes.as_mut_ptr(),
                96
            );
        }
        bytes
    }
    
    /// Deserialize from byte array
    pub fn from_bytes(bytes: &[u8; 96]) -> Option<Self> {
        if bytes.len() != 96 {
            return None;
        }
        let state: Self = unsafe {
            std::ptr::read(bytes.as_ptr() as *const _)
        };
        if state.verify() {
            Some(state)
        } else {
            None
        }
    }
    
    /// Advance morphogen phase (0→1→2→3→4→5→6→0)
    pub fn advance_phase(&mut self) {
        self.morphogen_phase = (self.morphogen_phase + 1) % 7;
        self.checksum = self.compute_checksum();
    }
    
    /// Get current segment from morphogen phase
    pub fn current_segment(&self) -> Segment {
        Segment::from_u8(self.morphogen_phase)
    }
    
    /// Apply geometric transformation (PGA multivector operation)
    pub fn transform(&mut self, multivector: &[i8; 16]) {
        for i in 0..16 {
            self.ternary_junction[i] = self.ternary_junction[i].wrapping_add(multivector[i]);
        }
        self.checksum = self.compute_checksum();
    }
    
    /// Measure coherence with another state
    /// 
    /// Returns value in range [0.0, 1.0] where 1.0 = perfect alignment
    pub fn coherence_with(&self, other: &Self) -> f32 {
        let center_dist = ((self.center_s[0] - other.center_s[0]).powi(2)
            + (self.center_s[1] - other.center_s[1]).powi(2)).sqrt();
        let junction_sim = self.ternary_junction.iter()
            .zip(other.ternary_junction.iter())
            .map(|(a, b)| (a - b).abs() as f32)
            .sum::<f32>() / 256.0;
        
        // Coherence decreases with distance, increases with junction similarity
        (1.0 - center_dist.min(1.0)) * (1.0 - junction_sim.min(1.0))
    }
}

impl Default for LatticeState {
    fn default() -> Self {
        Self::new()
    }
}

impl fmt::Display for LatticeState {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f,
            "LatticeState {{ phase: {}, segment: {:?}, center: [{:.2}, {:.2}], coherence: {:.2} }}",
            self.morphogen_phase,
            self.current_segment(),
            self.center_s[0],
            self.center_s[1],
            self.fellowship_resonance
        )
    }
}

/// The 7 segments of the geometric field
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
#[repr(u8)]
pub enum Segment {
    /// K1 — Void (Center, Absence, Null)
    Void = 0,
    /// K2 — Vesica (Entry, Creation, Space-Between)
    Vesica = 1,
    /// K3 — Curve (Flow, Continuity, Gradient)
    Curve = 2,
    /// K4 — Line (Connect, Linearity, Relation)
    Line = 3,
    /// K5 — Angle (Branch, Decide, Bifurcation)
    Angle = 4,
    /// K6 — Circle (Recurse, Closure, Self-Reference)
    Circle = 5,
    /// K7 — Dot (Locate, Position, Singularity)
    Dot = 6,
}

impl Segment {
    /// Convert u8 to Segment
    pub fn from_u8(n: u8) -> Self {
        match n % 7 {
            0 => Self::Void,
            1 => Self::Vesica,
            2 => Self::Curve,
            3 => Self::Line,
            4 => Self::Angle,
            5 => Self::Circle,
            _ => Self::Dot,
        }
    }
    
    /// Get segment name
    pub fn name(&self) -> &'static str {
        match self {
            Self::Void => "Void",
            Self::Vesica => "Vesica",
            Self::Curve => "Curve",
            Self::Line => "Line",
            Self::Angle => "Angle",
            Self::Circle => "Circle",
            Self::Dot => "Dot",
        }
    }
    
    /// Get next segment in Hamiltonian path
    /// 
    /// Hamiltonian path: K2 → K5 → K1 → K4 → K7 → K3 → K6
    pub fn next_hamiltonian(&self) -> Self {
        match self {
            Self::Vesica => Self::Angle,   // K2 → K5
            Self::Angle => Self::Void,      // K5 → K1
            Self::Void => Self::Line,       // K1 → K4
            Self::Line => Self::Dot,        // K4 → K7
            Self::Dot => Self::Curve,       // K7 → K3
            Self::Curve => Self::Circle,    // K3 → K6
            Self::Circle => Self::Vesica,   // K6 → K2 (loop)
        }
    }
    
    /// Get previous segment in Hamiltonian path
    pub fn prev_hamiltonian(&self) -> Self {
        match self {
            Self::Vesica => Self::Circle,   // K2 ← K6
            Self::Angle => Self::Vesica,    // K5 ← K2
            Self::Void => Self::Angle,      // K1 ← K5
            Self::Line => Self::Void,       // K4 ← K1
            Self::Dot => Self::Line,        // K7 ← K4
            Self::Curve => Self::Dot,       // K3 ← K7
            Self::Circle => Self::Curve,    // K6 ← K3
        }
    }
}

/// Iterator over the Hamiltonian path
pub struct HamiltonianPath {
    current: Segment,
    steps: usize,
    max_steps: usize,
}

impl HamiltonianPath {
    /// Create new Hamiltonian path starting at Vesica (K2)
    pub fn new() -> Self {
        Self {
            current: Segment::Vesica,
            steps: 0,
            max_steps: 7, // Complete cycle
        }
    }
    
    /// Create path with custom max steps
    pub fn with_max_steps(max: usize) -> Self {
        Self {
            current: Segment::Vesica,
            steps: 0,
            max_steps: max,
        }
    }
    
    /// Get current segment
    pub fn current(&self) -> Segment {
        self.current
    }
    
    /// Get steps taken
    pub fn steps(&self) -> usize {
        self.steps
    }
}

impl Iterator for HamiltonianPath {
    type Item = Segment;
    
    fn next(&mut self) -> Option<Self::Item> {
        if self.steps >= self.max_steps {
            return None;
        }
        let segment = self.current;
        self.current = segment.next_hamiltonian();
        self.steps += 1;
        Some(segment)
    }
}

impl Default for HamiltonianPath {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_lattice_state_new() {
        let state = LatticeState::new();
        assert_eq!(state.center_s, [0.0, 0.0]);
        assert_eq!(state.phi_magnitude, PHI_7);
        assert!(state.verify());
    }
    
    #[test]
    fn test_hamiltonian_path() {
        let path: Vec<_> = HamiltonianPath::new().collect();
        assert_eq!(path.len(), 7);
        assert_eq!(path[0], Segment::Vesica);  // K2
        assert_eq!(path[1], Segment::Angle);   // K5
        assert_eq!(path[2], Segment::Void);    // K1
        assert_eq!(path[3], Segment::Line);    // K4
        assert_eq!(path[4], Segment::Dot);     // K7
        assert_eq!(path[5], Segment::Curve);   // K3
        assert_eq!(path[6], Segment::Circle);  // K6
    }
    
    #[test]
    fn test_segment_roundtrip() {
        for i in 0..7 {
            let seg = Segment::from_u8(i);
            assert_eq!(seg as u8, i);
        }
    }
    
    #[test]
    fn test_state_serialization() {
        let state = LatticeState::new();
        let bytes = state.to_bytes();
        let recovered = LatticeState::from_bytes(&bytes).unwrap();
        assert_eq!(state.center_s, recovered.center_s);
        assert_eq!(state.phi_magnitude, recovered.phi_magnitude);
    }
    
    #[test]
    fn test_morphogen_phase_cycle() {
        let mut state = LatticeState::new();
        for expected in 0..7 {
            assert_eq!(state.morphogen_phase, expected);
            state.advance_phase();
        }
        assert_eq!(state.morphogen_phase, 0); // Cycles back
    }
    
    #[test]
    fn test_coherence() {
        let state1 = LatticeState::new();
        let state2 = LatticeState::new();
        let coherence = state1.coherence_with(&state2);
        assert!((coherence - 1.0).abs() < 0.01); // Identical states = high coherence
    }
}

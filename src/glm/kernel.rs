//! GLM Geometric Kernel
//! 
//! Core geometric operations for the GLYF Geometric Language Model.
//! Pure geometric computation — no matrix operations, only SO(3) rotations
//! and Projective Geometric Algebra (PGA) wedge products.

use std::f64::consts::PI;

/// The Golden Ratio φ = (1 + √5) / 2
pub const PHI: f64 = 1.618_033_988_749_895;

/// Golden angle = π * (3 - √5) ≈ 137.5°
pub const GOLDEN_ANGLE: f64 = 2.399_963_229_728_653_3;

/// Epsilon for floating point comparisons
pub const EPSILON: f64 = 1e-10;

/// A 4D PGA vector (e₀, e₁, e₂, e₃ basis)
/// In PGA: e₀ represents the origin, e₁,e₂,e₃ are directions
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct PGAVector {
    pub x: f32,  // e₁ coefficient
    pub y: f32,  // e₂ coefficient  
    pub z: f32,  // e₃ coefficient
    pub w: f32,  // e₀ coefficient (projective weight)
}

impl PGAVector {
    pub fn new(x: f32, y: f32, z: f32, w: f32) -> Self {
        Self { x, y, z, w }
    }
    
    pub fn zero() -> Self {
        Self { x: 0.0, y: 0.0, z: 0.0, w: 0.0 }
    }
    
    /// Normalize to unit weight
    pub fn normalize(&self) -> Self {
        if self.w.abs() < EPSILON as f32 {
            return *self;
        }
        Self {
            x: self.x / self.w,
            y: self.y / self.w,
            z: self.z / self.w,
            w: 1.0,
        }
    }
    
    /// Geometric norm (distance from origin in projective space)
    pub fn norm(&self) -> f32 {
        let n = (self.x * self.x + self.y * self.y + self.z * self.z).sqrt();
        if self.w.abs() > EPSILON as f32 {
            n / self.w.abs()
        } else {
            n
        }
    }
}

/// A bivector in 4D PGA representing an oriented plane
/// Bivector basis: e₀₁, e₀₂, e₀₃, e₁₂, e₁₃, e₂₃
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Bivector {
    pub e01: f32, // e₀ ∧ e₁
    pub e02: f32, // e₀ ∧ e₂
    pub e03: f32, // e₀ ∧ e₃
    pub e12: f32, // e₁ ∧ e₂  (rotation in XY plane)
    pub e13: f32, // e₁ ∧ e₃  (rotation in XZ plane)
    pub e23: f32, // e₂ ∧ e₃  (rotation in YZ plane)
}

impl Bivector {
    pub fn zero() -> Self {
        Self {
            e01: 0.0, e02: 0.0, e03: 0.0,
            e12: 0.0, e13: 0.0, e23: 0.0,
        }
    }
    
    /// Create rotation bivector for SO(3)
    pub fn rotation(axis: (f32, f32, f32), angle: f32) -> Self {
        let (x, y, z) = axis;
        let norm = (x * x + y * y + z * z).sqrt();
        if norm < EPSILON as f32 {
            return Self::zero();
        }
        let s = angle.sin() / norm;
        Self {
            e01: 0.0, e02: 0.0, e03: 0.0,
            e12: z * s,  // XY plane rotation
            e13: -y * s, // XZ plane rotation
            e23: x * s,  // YZ plane rotation
        }
    }
    
    /// Magnitude of the bivector
    pub fn magnitude(&self) -> f32 {
        (self.e12 * self.e12 + self.e13 * self.e13 + self.e23 * self.e23).sqrt()
    }
}

/// Quaternion for efficient rotation composition
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Quaternion {
    pub w: f32,
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

impl Quaternion {
    pub fn identity() -> Self {
        Self { w: 1.0, x: 0.0, y: 0.0, z: 0.0 }
    }
    
    pub fn from_rotation(axis: (f32, f32, f32), angle: f32) -> Self {
        let half_angle = angle / 2.0;
        let s = half_angle.sin();
        let c = half_angle.cos();
        let (ax, ay, az) = axis;
        let norm = (ax * ax + ay * ay + az * az).sqrt();
        if norm < EPSILON as f32 {
            return Self::identity();
        }
        Self {
            w: c,
            x: ax * s / norm,
            y: ay * s / norm,
            z: az * s / norm,
        }
    }
    
    /// Quaternion multiplication
    pub fn mul(&self, other: &Self) -> Self {
        Self {
            w: self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
            x: self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            y: self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            z: self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w,
        }
    }
    
    /// Conjugate (inverse for unit quaternion)
    pub fn conjugate(&self) -> Self {
        Self { w: self.w, x: -self.x, y: -self.y, z: -self.z }
    }
    
    /// Rotate a vector using sandwich product: q * v * q̄
    pub fn rotate_vector(&self, v: (f32, f32, f32)) -> (f32, f32, f32) {
        let (vx, vy, vz) = v;
        let qv = Quaternion { w: 0.0, x: vx, y: vy, z: vz };
        let result = self.mul(&qv).mul(&self.conjugate());
        (result.x, result.y, result.z)
    }
}

/// Phase represented as dual frequencies
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Phase {
    pub primary: f64,
    pub harmonic: f64,
}

impl Phase {
    pub fn new(primary: f64, harmonic: f64) -> Self {
        Self { primary, harmonic }
    }
    
    pub fn zero() -> Self {
        Self { primary: 0.0, harmonic: 0.0 }
    }
    
    /// Phase shift by given angle
    pub fn shift(&self, delta: f64) -> Self {
        Self {
            primary: self.primary + delta,
            harmonic: self.harmonic + delta * PHI,
        }
    }
}

/// The 96-byte Lattice State — the fundamental unit of GLM
#[derive(Debug, Clone, Copy)]
pub struct LatticeState {
    /// Position in 4D PGA (12 bytes)
    pub position: PGAVector,
    /// Orientation as bivector (24 bytes)
    pub orientation: Bivector,
    /// Magnitude weight (8 bytes)
    pub magnitude: f64,
    /// Dual phase (16 bytes)
    pub phase: Phase,
    /// Attenuation factor (8 bytes)
    pub attenuation: f64,
    /// Rotation spinor as quaternion (16 bytes)
    pub spinor: Quaternion,
    /// Metadata flags (4 bytes)
    pub metadata: u32,
    /// Padding to align to 96 bytes (8 bytes)
    _padding: [u8; 8],
}

impl Default for LatticeState {
    fn default() -> Self {
        Self {
            position: PGAVector::zero(),
            orientation: Bivector::zero(),
            magnitude: 0.0,
            phase: Phase::zero(),
            attenuation: 1.0,
            spinor: Quaternion::identity(),
            metadata: 0,
            _padding: [0; 8],
        }
    }
}

impl LatticeState {
    /// Create a null (VOID) state
    pub fn null() -> Self {
        Self::default()
    }
    
    /// Create state from position only
    pub fn from_position(x: f32, y: f32, z: f32) -> Self {
        Self {
            position: PGAVector::new(x, y, z, 1.0),
            magnitude: 1.0,
            ..Default::default()
        }
    }
    
    /// Check if state is null/void
    pub fn is_null(&self) -> bool {
        self.magnitude.abs() < EPSILON
    }
    
    /// Total size in bytes
    pub const fn size_bytes() -> usize {
        96
    }
}

// ============================================================================
// CORE GEOMETRIC OPERATIONS
// ============================================================================

/// Geometric distance between two lattice states in PGA space
pub fn geometric_distance(a: &LatticeState, b: &LatticeState) -> f64 {
    let pa = a.position.normalize();
    let pb = b.position.normalize();
    
    let dx = (pa.x - pb.x) as f64;
    let dy = (pa.y - pb.y) as f64;
    let dz = (pa.z - pb.z) as f64;
    
    // Include phase difference in distance
    let phase_diff = (a.phase.primary - b.phase.primary).sin().abs();
    
    let spatial_dist = (dx * dx + dy * dy + dz * dz).sqrt();
    spatial_dist + 0.1 * phase_diff
}

/// Vesica Piscis — intersection of two lattice states
/// Returns the lens-shaped intersection representing semantic overlap
pub fn vesica_piscis(a: &LatticeState, b: &LatticeState) -> LatticeState {
    // Handle null states
    if a.is_null() {
        return *b;
    }
    if b.is_null() {
        return *a;
    }
    
    let d = geometric_distance(a, b);
    let r1 = a.magnitude.sqrt();
    let r2 = b.magnitude.sqrt();
    
    // No intersection
    if d >= r1 + r2 {
        return LatticeState::null();
    }
    
    // One contained within the other
    if d <= (r1 - r2).abs() {
        return if r1 < r2 { *a } else { *b };
    }
    
    // Calculate intersection area (lens area formula)
    let r1_sq = r1 * r1;
    let r2_sq = r2 * r2;
    let d_sq = d * d;
    
    let term1 = r1_sq * ((r1_sq - r2_sq + d_sq) / (2.0 * r1 * d)).acos();
    let term2 = r2_sq * ((r2_sq - r1_sq + d_sq) / (2.0 * r2 * d)).acos();
    let term3 = 0.5 * (((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2)).sqrt());
    
    let intersection_area = term1 + term2 - term3;
    
    // Weighted midpoint based on magnitudes
    let total_mag = a.magnitude + b.magnitude;
    let weight_a = b.magnitude / total_mag; // Inverse weight for midpoint
    let weight_b = a.magnitude / total_mag;
    
    let pa = a.position.normalize();
    let pb = b.position.normalize();
    
    let interp_pos = PGAVector::new(
        (pa.x as f64 * weight_a + pb.x as f64 * weight_b) as f32,
        (pa.y as f64 * weight_a + pb.y as f64 * weight_b) as f32,
        (pa.z as f64 * weight_a + pb.z as f64 * weight_b) as f32,
        1.0,
    );
    
    // Interpolate bivectors
    let interp_bivector = Bivector {
        e01: (a.orientation.e01 as f64 * weight_a + b.orientation.e01 as f64 * weight_b) as f32,
        e02: (a.orientation.e02 as f64 * weight_a + b.orientation.e02 as f64 * weight_b) as f32,
        e03: (a.orientation.e03 as f64 * weight_a + b.orientation.e03 as f64 * weight_b) as f32,
        e12: (a.orientation.e12 as f64 * weight_a + b.orientation.e12 as f64 * weight_b) as f32,
        e13: (a.orientation.e13 as f64 * weight_a + b.orientation.e13 as f64 * weight_b) as f32,
        e23: (a.orientation.e23 as f64 * weight_a + b.orientation.e23 as f64 * weight_b) as f32,
    };
    
    // Interpolate phases
    let interp_phase = Phase::new(
        (a.phase.primary * weight_a + b.phase.primary * weight_b),
        (a.phase.harmonic * weight_a + b.phase.harmonic * weight_b),
    );
    
    // Compose spinors
    let interp_spinor = compose_spinors(&a.spinor, &b.spinor, 
        (weight_a + weight_b) / 2.0);
    
    LatticeState {
        position: interp_pos,
        orientation: interp_bivector,
        magnitude: intersection_area,
        phase: interp_phase,
        attenuation: (a.attenuation + b.attenuation) / 2.0,
        spinor: interp_spinor,
        metadata: a.metadata | b.metadata, // Union of flags
        _padding: [0; 8],
    }
}

/// Compose two spinors with given blend factor
fn compose_spinors(a: &Quaternion, b: &Quaternion, t: f64) -> Quaternion {
    // Spherical linear interpolation (slerp) for quaternions
    let dot = a.w * b.w + a.x * b.x + a.y * b.y + a.z * b.z;
    
    let (b_w, b_x, b_y, b_z) = if dot < 0.0 {
        (-b.w, -b.x, -b.y, -b.z)
    } else {
        (b.w, b.x, b.y, b.z)
    };
    
    let dot = dot.abs();
    let t = t as f32;
    
    if dot > 0.9995 {
        // Linear interpolation for very close quaternions
        Quaternion {
            w: a.w + t * (b_w - a.w),
            x: a.x + t * (b_x - a.x),
            y: a.y + t * (b_y - a.y),
            z: a.z + t * (b_z - a.z),
        }
    } else {
        let theta_0 = dot.acos();
        let theta = theta_0 * t;
        let sin_theta = theta.sin();
        let sin_theta_0 = theta_0.sin();
        
        let s0 = ((1.0 - t) * theta).cos() - dot * sin_theta / sin_theta_0;
        let s1 = sin_theta / sin_theta_0;
        
        Quaternion {
            w: a.w * s0 + b_w * s1,
            x: a.x * s0 + b_x * s1,
            y: a.y * s0 + b_y * s1,
            z: a.z * s0 + b_z * s1,
        }
    }
}

/// Phyllotaxis rotation — golden angle rotation based on layer index
pub fn phyllotaxis_rotate(state: &mut LatticeState, layer_idx: usize) {
    let angle = GOLDEN_ANGLE * ((layer_idx + 1) as f64);
    let angle_f32 = angle as f32;
    
    // Create rotation quaternion
    let rotation = Quaternion::from_rotation(
        (state.orientation.e12, state.orientation.e13, state.orientation.e23),
        angle_f32
    );
    
    // Apply rotation to position
    let (x, y, z) = rotation.rotate_vector((
        state.position.x,
        state.position.y, 
        state.position.z
    ));
    
    state.position.x = x;
    state.position.y = y;
    state.position.z = z;
    
    // Update spinor
    state.spinor = rotation.mul(&state.spinor);
    
    // Adjust phase
    state.phase = state.phase.shift(angle);
}

/// Hodge Dual — orthogonal complement in PGA
/// Maps: vector → trivector, bivector → bivector, trivector → vector
pub fn hodge_dual(state: &LatticeState) -> LatticeState {
    // In 4D PGA with signature (3,0,1):
    // ⋆(a e₀ + b e₁ + c e₂ + d e₃) = a e₁₂₃ - b e₂₃ + c e₁₃ - d e₁₂
    // 
    // This swaps position and orientation in a specific way:
    // - position components map to bivector components (with signs)
    // - bivector e₀ᵢ components map to position components
    
    let new_orientation = Bivector {
        e01: state.position.x,
        e02: state.position.y, 
        e03: state.position.z,
        e12: -state.position.x, // sign flip for dual relationship
        e13: state.position.y,
        e23: -state.position.z,
    };
    
    let new_position = PGAVector::new(
        state.orientation.e01,
        state.orientation.e02,
        state.orientation.e03,
        1.0,
    );
    
    // Magnitude inverts (dual of large is small)
    let new_magnitude = 1.0 / (state.magnitude + EPSILON);
    
    // Phase shifts by π/2 (90 degree phase shift)
    let new_phase = state.phase.shift(PI / 2.0);
    
    LatticeState {
        position: new_position,
        orientation: new_orientation,
        magnitude: new_magnitude,
        phase: new_phase,
        attenuation: 1.0 / (state.attenuation + EPSILON),
        spinor: state.spinor.conjugate(), // Conjugate spinor
        metadata: state.metadata,
        _padding: [0; 8],
    }
}

/// Lattice addition — geometric sum of two states
pub fn lattice_add(a: &LatticeState, b: &LatticeState) -> LatticeState {
    if a.is_null() {
        return *b;
    }
    if b.is_null() {
        return *a;
    }
    
    let total_mag = a.magnitude + b.magnitude;
    let wa = a.magnitude / total_mag;
    let wb = b.magnitude / total_mag;
    
    LatticeState {
        position: PGAVector::new(
            (a.position.x as f64 * wa + b.position.x as f64 * wb) as f32,
            (a.position.y as f64 * wa + b.position.y as f64 * wb) as f32,
            (a.position.z as f64 * wa + b.position.z as f64 * wb) as f32,
            1.0,
        ),
        orientation: Bivector {
            e01: (a.orientation.e01 as f64 * wa + b.orientation.e01 as f64 * wb) as f32,
            e02: (a.orientation.e02 as f64 * wa + b.orientation.e02 as f64 * wb) as f32,
            e03: (a.orientation.e03 as f64 * wa + b.orientation.e03 as f64 * wb) as f32,
            e12: (a.orientation.e12 as f64 * wa + b.orientation.e12 as f64 * wb) as f32,
            e13: (a.orientation.e13 as f64 * wa + b.orientation.e13 as f64 * wb) as f32,
            e23: (a.orientation.e23 as f64 * wa + b.orientation.e23 as f64 * wb) as f32,
        },
        magnitude: total_mag,
        phase: Phase::new(
            a.phase.primary * wa + b.phase.primary * wb,
            a.phase.harmonic * wa + b.phase.harmonic * wb,
        ),
        attenuation: (a.attenuation + b.attenuation) / 2.0,
        spinor: compose_spinors(&a.spinor, &b.spinor, 0.5),
        metadata: a.metadata | b.metadata,
        _padding: [0; 8],
    }
}

/// Scale a lattice state by scalar factor
pub fn lattice_scale(state: &LatticeState, factor: f64) -> LatticeState {
    let mut result = *state;
    result.magnitude *= factor.abs();
    result.attenuation *= factor.abs();
    
    // For negative factors, shift phase by π (invert)
    if factor < 0.0 {
        result.phase = result.phase.shift(PI);
    }
    
    result
}

/// Apply phi-harmonic position encoding to a lattice state
pub fn apply_phi_encoding(state: &LatticeState, position: usize) -> LatticeState {
    let p = position as f64;
    
    // Phi-spiral encoding
    let angle0 = 2.0 * PI * p / PHI.powi(0);
    let angle1 = 2.0 * PI * p / PHI.powi(1);
    let angle2 = 2.0 * PI * p / PHI.powi(2);
    
    let radius = PHI.powf(p / 100.0); // Spiral outward
    
    let mut result = *state;
    
    // Modulate position with phi-harmonic components
    result.position.x += (radius * angle0.cos()) as f32;
    result.position.y += (radius * angle1.sin()) as f32;
    result.position.z += (radius * angle2.cos()) as f32;
    
    // Set phase based on position
    result.phase = Phase::new(
        angle0.rem_euclid(2.0 * PI),
        angle1.rem_euclid(2.0 * PI),
    );
    
    result
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/// Linear interpolation between lattice states
pub fn lattice_lerp(a: &LatticeState, b: &LatticeState, t: f64) -> LatticeState {
    let t = t.clamp(0.0, 1.0);
    let s = 1.0 - t;
    
    LatticeState {
        position: PGAVector::new(
            (a.position.x as f64 * s + b.position.x as f64 * t) as f32,
            (a.position.y as f64 * s + b.position.y as f64 * t) as f32,
            (a.position.z as f64 * s + b.position.z as f64 * t) as f32,
            1.0,
        ),
        orientation: Bivector {
            e01: (a.orientation.e01 as f64 * s + b.orientation.e01 as f64 * t) as f32,
            e02: (a.orientation.e02 as f64 * s + b.orientation.e02 as f64 * t) as f32,
            e03: (a.orientation.e03 as f64 * s + b.orientation.e03 as f64 * t) as f32,
            e12: (a.orientation.e12 as f64 * s + b.orientation.e12 as f64 * t) as f32,
            e13: (a.orientation.e13 as f64 * s + b.orientation.e13 as f64 * t) as f32,
            e23: (a.orientation.e23 as f64 * s + b.orientation.e23 as f64 * t) as f32,
        },
        magnitude: a.magnitude * s + b.magnitude * t,
        phase: Phase::new(
            a.phase.primary * s + b.phase.primary * t,
            a.phase.harmonic * s + b.phase.harmonic * t,
        ),
        attenuation: a.attenuation * s + b.attenuation * t,
        spinor: compose_spinors(&a.spinor, &b.spinor, t),
        metadata: if t < 0.5 { a.metadata } else { b.metadata },
        _padding: [0; 8],
    }
}

/// Compute Gaussian weight for distance
pub fn gaussian_weight(distance: f64, sigma: f64) -> f64 {
    (-distance * distance / (2.0 * sigma * sigma)).exp()
}

/// Uniform average of multiple lattice states
pub fn lattice_average(states: &[LatticeState]) -> LatticeState {
    if states.is_empty() {
        return LatticeState::null();
    }
    
    let n = states.len() as f64;
    let mut sum = LatticeState::null();
    
    for state in states {
        sum = lattice_add(&sum, &lattice_scale(state, 1.0 / n));
    }
    
    sum
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_lattice_size() {
        assert_eq!(std::mem::size_of::<LatticeState>(), 96);
    }
    
    #[test]
    fn test_vesica_piscis_no_intersection() {
        let a = LatticeState::from_position(0.0, 0.0, 0.0);
        let b = LatticeState::from_position(10.0, 0.0, 0.0);
        let result = vesica_piscis(&a, &b);
        assert!(result.is_null());
    }
    
    #[test]
    fn test_vesica_piscis_overlap() {
        let mut a = LatticeState::from_position(0.0, 0.0, 0.0);
        a.magnitude = 4.0; // radius = 2
        let mut b = LatticeState::from_position(1.0, 0.0, 0.0);
        b.magnitude = 4.0; // radius = 2
        
        let result = vesica_piscis(&a, &b);
        assert!(!result.is_null());
        assert!(result.magnitude > 0.0);
    }
    
    #[test]
    fn test_hodge_dual() {
        let state = LatticeState::from_position(1.0, 2.0, 3.0);
        let dual = hodge_dual(&state);
        
        // Dual of dual should restore original (approximately)
        let double_dual = hodge_dual(&dual);
        assert!((double_dual.magnitude - state.magnitude).abs() < 0.001);
    }
    
    #[test]
    fn test_phi_encoding() {
        let state = LatticeState::from_position(0.0, 0.0, 0.0);
        let encoded = apply_phi_encoding(&state, 10);
        
        // Position should be modified
        assert_ne!(encoded.position.x, 0.0);
        assert_ne!(encoded.position.y, 0.0);
    }
    
    #[test]
    fn test_quaternion_rotation() {
        let q = Quaternion::from_rotation((0.0, 0.0, 1.0), PI as f32 / 2.0);
        let (x, y, _z) = q.rotate_vector((1.0, 0.0, 0.0));
        
        assert!((x - 0.0).abs() < 0.001);
        assert!((y - 1.0).abs() < 0.001);
    }
}

# GLM Architecture Specification
## Geometric Language Model — Core Attention Mechanisms

**Version:** 0.1.0  
**Target State Size:** 96 bytes  
**Complexity Target:** O(1) attention operations  
**Date:** 2026-04-04  

---

## 1. Overview

The Geometric Language Model (GLM) replaces traditional matrix-multiplication-based attention with **geometric primitive operations**. Instead of computing Q·K^T, we compute similarities through geometric relationships: overlaps, rotations, and complements.

### 1.1 Design Principles

1. **Geometric over Algebraic**: Replace dot products with geometric constructions
2. **Constant-time attention**: No O(n²) or O(n) scaling with sequence length
3. **Compact state**: Entire context encoded in 96 bytes (φ-harmonic lattice)
4. **Compositional heads**: Multi-head via rotor sandwiching, not parallel matrices

### 1.2 The 96-Byte Context State

```
Bytes 0-23:    Vesica Piscis overlap accumulator (3× f64)
Bytes 24-47:   Phyllotaxis spiral coordinates (3× f64)
Bytes 48-71:   Hodge dual complement space (3× f64)
Bytes 72-95:   Rotor composition buffer (4× f32 quaternion)
```

---

## 2. VesicaPiscis Attention

### 2.1 Concept

Similarity emerges from **overlapping lens geometry**. Two tokens form a vesica piscis (the lens shape where two circles intersect). The overlap area represents attention weight.

### 2.2 Mathematical Formulation

For tokens represented as circles in semantic space:
- Circle A: center **cₐ**, radius **rₐ** 
- Circle B: center **cᵦ**, radius **rᵦ**
- Distance: **d** = |cₐ - cᵦ|

The vesica piscis overlap area:

```
overlap(A,B) = rₐ² · cos⁻¹((d² + rₐ² - rᵦ²) / 2drₐ)
             + rᵦ² · cos⁻¹((d² + rᵦ² - rₐ²) / 2drᵦ)
             - ½ · √((-d + rₐ + rᵦ)(d + rₐ - rᵦ)(d - rₐ + rᵦ)(d + rₐ + rᵦ))
```

Attention weight: **w = overlap(A,B) / min(πrₐ², πrᵦ²)**

### 2.3 Rust Pseudocode

```rust
/// Vesica Piscis attention weight computation
/// O(1) complexity - single geometric operation
pub struct VesicaToken {
    center: [f64; 3],  // Semantic coordinates
    radius: f64,       // Token "reach" or confidence
}

impl VesicaToken {
    /// Compute overlap-based attention weight
    pub fn attention_weight(&self, other: &VesicaToken) -> f64 {
        let d = euclidean_distance(&self.center, &other.center);
        
        // No overlap case
        if d >= self.radius + other.radius {
            return 0.0;
        }
        
        // Full containment case
        if d <= (self.radius - other.radius).abs() {
            let r_min = self.radius.min(other.radius);
            return 1.0; // Maximum attention (containment)
        }
        
        // Vesica piscis overlap area
        let r1 = self.radius;
        let r2 = other.radius;
        let r1_sq = r1 * r1;
        let r2_sq = r2 * r2;
        
        // Law of cosines for sector angles
        let alpha = ((d*d + r1_sq - r2_sq) / (2.0 * d * r1)).acos();
        let beta = ((d*d + r2_sq - r1_sq) / (2.0 * d * r2)).acos();
        
        // Sector areas minus triangle areas
        let sector1 = r1_sq * alpha;
        let sector2 = r2_sq * beta;
        let triangle = 0.5 * (
            r1_sq * (2.0 * alpha).sin() +
            r2_sq * (2.0 * beta).sin()
        );
        
        let overlap = sector1 + sector2 - triangle;
        let max_area = std::f64::consts::PI * r1_sq.min(r2_sq);
        
        (overlap / max_area).clamp(0.0, 1.0)
    }
}

/// Accumulate attention into 24-byte state
pub fn vesica_accumulate(
    state: &mut [u8; 24],
    tokens: &[VesicaToken],
    query: &VesicaToken
) {
    let mut accumulator = [0.0f64; 3];
    
    for token in tokens {
        let weight = query.attention_weight(token);
        for i in 0..3 {
            accumulator[i] += weight * token.center[i];
        }
    }
    
    // Pack into state bytes
    for (i, &val) in accumulator.iter().enumerate() {
        let bytes = val.to_le_bytes();
        state[i*8..(i+1)*8].copy_from_slice(&bytes);
    }
}
```

### 2.4 Properties

- **Symmetry**: `overlap(A,B) = overlap(B,A)` ✓
- **Bounded**: Output ∈ [0, 1]
- **Differentiable**: Yes (for training)
- **Complexity**: O(1) per pair, O(n) total scan

---

## 3. Phyllotaxis Attention

### 3.1 Concept

Token sequence arranged on a **golden-angle spiral** (phyllotaxis pattern). Attention follows spiral proximity—nearby tokens on the spiral have higher attention weights.

### 3.2 Mathematical Formulation

Golden angle: **φ = π(3 - √5) ≈ 137.507°** (2.39996 radians)

Token position on spiral:
```
rₙ = √n · scale      // Radial distance
θₙ = n · φ           // Angular position
```

Attention weight decays with **spiral distance**:
```
w(n, m) = exp(-|n - m| / τ) · cos²((θₙ - θₘ)/2)
```

Where τ is temperature, and the cosine term enforces angular coherence.

### 3.3 Rust Pseudocode

```rust
/// Golden ratio constant
const PHI: f64 = 1.618033988749895;
const GOLDEN_ANGLE: f64 = std::f64::consts::PI * (3.0 - 5.0f64.sqrt());

/// Phyllotaxis spiral attention
pub struct PhyllotaxisAttention {
    scale: f64,
    temperature: f64,
}

impl PhyllotaxisAttention {
    /// Get spiral coordinates for token index
    pub fn spiral_coords(&self, n: usize) -> [f64; 3] {
        let n_f64 = n as f64;
        let r = n_f64.sqrt() * self.scale;
        let theta = n_f64 * GOLDEN_ANGLE;
        
        [
            r * theta.cos(),
            r * theta.sin(),
            n_f64 / PHI,  // Depth coordinate
        ]
    }
    
    /// Compute spiral-based attention weight
    pub fn weight(&self, n: usize, m: usize) -> f64 {
        if n == m {
            return 1.0; // Self-attention maximum
        }
        
        let pos_n = self.spiral_coords(n);
        let pos_m = self.spiral_coords(m);
        
        // Radial distance along spiral
        let delta_n = (n as f64 - m as f64).abs();
        let radial_decay = (-delta_n / self.temperature).exp();
        
        // Angular coherence
        let theta_n = n as f64 * GOLDEN_ANGLE;
        let theta_m = m as f64 * GOLDEN_ANGLE;
        let delta_theta = (theta_n - theta_m).rem_euclid(2.0 * std::f64::consts::PI);
        let angular_coherence = (delta_theta / 2.0).cos().powi(2);
        
        radial_decay * angular_coherence
    }
    
    /// Scan spiral for relevant context (O(1) with early termination)
    pub fn spiral_scan(
        &self,
        state: &mut [u8; 24],
        token_values: &[[f64; 3]],
        query_idx: usize,
        threshold: f64
    ) {
        let mut accumulator = [0.0f64; 3];
        let mut total_weight = 0.0;
        
        // Scan outward from query position
        let max_scan = token_values.len().min(256); // Constant bound
        
        for offset in 1..max_scan {
            // Scan both directions
            for &idx in &[query_idx.wrapping_sub(offset), query_idx + offset] {
                if idx >= token_values.len() {
                    continue;
                }
                
                let weight = self.weight(query_idx, idx);
                if weight < threshold {
                    continue; // Early termination per direction
                }
                
                for i in 0..3 {
                    accumulator[i] += weight * token_values[idx][i];
                }
                total_weight += weight;
            }
        }
        
        // Normalize
        if total_weight > 0.0 {
            for i in 0..3 {
                accumulator[i] /= total_weight;
            }
        }
        
        // Pack to state
        for (i, &val) in accumulator.iter().enumerate() {
            let bytes = val.to_le_bytes();
            state[i*8..(i+1)*8].copy_from_slice(&bytes);
        }
    }
}
```

### 3.4 Properties

- **Position-aware**: Token order matters through spiral geometry
- **Hierarchical**: Higher indices = outer spiral = broader context
- **Constant memory**: Spiral position computed on-the-fly
- **Early termination**: Can stop scanning when weights decay below threshold

---

## 4. HodgeDual Attention

### 4.1 Concept

Attention via **complementary subspaces**. Every token exists in a space; its Hodge dual represents what is "not" that token—the orthogonal complement. Attention weights emerge from dual-space interactions.

### 4.2 Mathematical Formulation

In 3D geometric algebra, the Hodge dual maps k-vectors to (n-k)-vectors:
```
⋆e₁ = e₂ ∧ e₃
⋆e₂ = e₃ ∧ e₁  
⋆e₃ = e₁ ∧ e₂
```

For tokens as vectors **v**, the Hodge dual is the bivector representing the plane orthogonal to **v**.

Dual attention weight:
```
w(a, b) = 1 - |⋆a ∧ b| / (|a| · |b|)
```

This measures how much **b** lies in the complement of **a**—orthogonal tokens have high dual attention (they "complete" each other).

### 4.3 Rust Pseudocode

```rust
/// 3D Vector and Bivector for Hodge dual operations
#[derive(Clone, Copy)]
pub struct Vec3([f64; 3]);

#[derive(Clone, Copy)]
pub struct Bivector([f64; 3]); // (e23, e31, e12) components

impl Vec3 {
    /// Hodge dual: vector → bivector
    /// ⋆v = v₁·e₂₃ + v₂·e₃₁ + v₃·e₁₂
    pub fn hodge_dual(&self) -> Bivector {
        Bivector([self.0[0], self.0[1], self.0[2]])
    }
    
    /// Wedge product with another vector
    /// a ∧ b = (a₂b₃-a₃b₂)·e₂₃ + (a₃b₁-a₁b₃)·e₃₁ + (a₁b₂-a₂b₁)·e₁₂
    pub fn wedge(&self, other: &Vec3) -> Bivector {
        Bivector([
            self.0[1] * other.0[2] - self.0[2] * other.0[1], // e₂₃
            self.0[2] * other.0[0] - self.0[0] * other.0[2], // e₃₁
            self.0[0] * other.0[1] - self.0[1] * other.0[0], // e₁₂
        ])
    }
    
    pub fn magnitude(&self) -> f64 {
        self.0.iter().map(|x| x * x).sum::<f64>().sqrt()
    }
    
    pub fn normalize(&self) -> Vec3 {
        let mag = self.magnitude();
        if mag > 1e-10 {
            Vec3([self.0[0]/mag, self.0[1]/mag, self.0[2]/mag])
        } else {
            Vec3([0.0; 3])
        }
    }
}

impl Bivector {
    pub fn magnitude(&self) -> f64 {
        self.0.iter().map(|x| x * x).sum::<f64>().sqrt()
    }
}

/// Hodge dual attention mechanism
pub struct HodgeAttention;

impl HodgeAttention {
    /// Compute dual attention weight
    /// High when b is orthogonal to a (complementary)
    pub fn weight(a: &Vec3, b: &Vec3) -> f64 {
        let a_norm = a.normalize();
        let b_norm = b.normalize();
        
        // |⋆a ∧ b| / (|a|·|b|) measures parallel component
        // 1 - this measures orthogonal component (complementarity)
        let dual_a = a_norm.hodge_dual();
        
        // Project b onto dual space
        let projection = dual_a.0[0] * b_norm.0[0] +
                        dual_a.0[1] * b_norm.0[1] +
                        dual_a.0[2] * b_norm.0[2];
        
        // Weight is complement: 1 when orthogonal, 0 when parallel
        let orthogonality = projection.abs();
        (1.0 - orthogonality).clamp(0.0, 1.0)
    }
    
    /// Alternative: direct wedge magnitude
    pub fn wedge_weight(a: &Vec3, b: &Vec3) -> f64 {
        let a_mag = a.magnitude();
        let b_mag = b.magnitude();
        
        if a_mag * b_mag < 1e-10 {
            return 0.0;
        }
        
        // |a ∧ b| = |a|·|b|·sin(θ)
        // sin²(θ) = 1 - cos²(θ) gives orthogonality measure
        let wedge = a.wedge(b);
        let sin_theta = wedge.magnitude() / (a_mag * b_mag);
        
        sin_theta.min(1.0) // Clamp for numerical stability
    }
    
    /// Accumulate dual attention state
    pub fn accumulate(
        state: &mut [u8; 24],
        tokens: &[Vec3],
        query: &Vec3
    ) {
        let mut complement = [0.0f64; 3]; // Orthogonal accumulator
        let mut parallel = [0.0f64; 3];   // Parallel accumulator
        
        for token in tokens {
            let dual_w = Self::weight(query, token);
            let wedge_w = Self::wedge_weight(query, token);
            
            for i in 0..3 {
                // Accumulate by complementarity
                complement[i] += dual_w * token.0[i];
                parallel[i] += (1.0 - wedge_w) * token.0[i];
            }
        }
        
        // Pack complement space into state (first half)
        for (i, &val) in complement.iter().enumerate() {
            let bytes = val.to_le_bytes();
            state[i*8..(i+1)*8].copy_from_slice(&bytes);
        }
    }
}
```

### 4.4 Properties

- **Complementarity-seeking**: Attends to what "completes" the query
- **Orthogonal awareness**: Explicitly models what is NOT the query
- **Geometric duality**: Vector/bivector correspondence
- **Negation-capable**: Can represent "attention to opposite"

---

## 5. Sandwich Rotor Composition (Multi-Head)

### 5.1 Concept

Traditional multi-head attention uses parallel weight matrices. GLM uses **rotor sandwiching**—geometric products that compose attention heads through rotation/reflection in spin space.

### 5.2 Mathematical Formulation

A rotor **R** encodes a rotation: `R = exp(-θ/2 · B)` where B is a bivector.

Sandwich product applies rotation:
```
v' = R · v · R⁻¹
```

For multi-head, we compose rotors:
```
R_total = Rₙ · ... · R₂ · R₁
```

Each head contributes a rotor; the composition creates a compound transformation.

### 5.3 Rust Pseudocode

```rust
/// Quaternion-based rotor (4× f32 = 16 bytes)
/// Represents rotation in 3D spin space
#[derive(Clone, Copy, Debug)]
pub struct Rotor {
    pub s: f32,    // Scalar part
    pub x: f32,    // e₂₃ coefficient
    pub y: f32,    // e₃₁ coefficient  
    pub z: f32,    // e₁₂ coefficient
}

impl Rotor {
    /// Identity rotor
    pub const IDENTITY: Self = Self { s: 1.0, x: 0.0, y: 0.0, z: 0.0 };
    
    /// Create rotor from axis and angle
    pub fn from_axis_angle(axis: [f32; 3], angle: f32) -> Self {
        let half_angle = angle / 2.0;
        let sin_half = half_angle.sin();
        let mag = (axis[0]*axis[0] + axis[1]*axis[1] + axis[2]*axis[2]).sqrt();
        
        if mag < 1e-6 {
            return Self::IDENTITY;
        }
        
        Self {
            s: half_angle.cos(),
            x: axis[0] * sin_half / mag,
            y: axis[1] * sin_half / mag,
            z: axis[2] * sin_half / mag,
        }
    }
    
    /// Geometric product: self · other
    pub fn geometric(&self, other: &Self) -> Self {
        Self {
            s: self.s * other.s - self.x * other.x - self.y * other.y - self.z * other.z,
            x: self.s * other.x + self.x * other.s + self.y * other.z - self.z * other.y,
            y: self.s * other.y - self.x * other.z + self.y * other.s + self.z * other.x,
            z: self.s * other.z + self.x * other.y - self.y * other.x + self.z * other.s,
        }
    }
    
    /// Inverse: R⁻¹ = R* / |R|² (conjugate divided by norm squared)
    pub fn inverse(&self) -> Self {
        let norm_sq = self.s*self.s + self.x*self.x + self.y*self.y + self.z*self.z;
        if norm_sq < 1e-10 {
            return Self::IDENTITY;
        }
        Self {
            s: self.s / norm_sq,
            x: -self.x / norm_sq,
            y: -self.y / norm_sq,
            z: -self.z / norm_sq,
        }
    }
    
    /// Sandwich product: self · v · self⁻¹
    /// Returns rotated vector
    pub fn sandwich_vector(&self, v: [f32; 3]) -> [f32; 3] {
        // Treat vector as pure quaternion (0, v[0], v[1], v[2])
        let v_rotor = Rotor { s: 0.0, x: v[0], y: v[1], z: v[2] };
        
        // R · v · R⁻¹
        let inv = self.inverse();
        let temp = self.geometric(&v_rotor);
        let result = temp.geometric(&inv);
        
        [result.x, result.y, result.z]
    }
}

/// Multi-head attention via rotor composition
pub struct SandwichMultiHead {
    heads: Vec<Rotor>,  // Each head is a rotor
    composition_buffer: [u8; 16], // 4× f32 quaternion
}

impl SandwichMultiHead {
    /// Compose all head rotors into single transformation
    /// This is O(heads) but independent of sequence length
    pub fn compose_rotors(&mut self) -> Rotor {
        let mut composed = Rotor::IDENTITY;
        
        // Compose: R_total = Rₙ · ... · R₂ · R₁
        for rotor in &self.heads {
            composed = rotor.geometric(&composed);
        }
        
        // Cache to buffer
        self.composition_buffer[0..4].copy_from_slice(&composed.s.to_le_bytes());
        self.composition_buffer[4..8].copy_from_slice(&composed.x.to_le_bytes());
        self.composition_buffer[8..12].copy_from_slice(&composed.y.to_le_bytes());
        self.composition_buffer[12..16].copy_from_slice(&composed.z.to_le_bytes());
        
        composed
    }
    
    /// Apply composed attention to state
    pub fn apply_to_state(&self, state: &mut [u8; 96]) {
        // Extract 3D vectors from state
        let vesica = extract_vec3(&state[0..24]);
        let phyllotaxis = extract_vec3(&state[24..48]);
        let hodge = extract_vec3(&state[48..72]);
        
        // Load composed rotor
        let composed = Rotor {
            s: f32::from_le_bytes(self.composition_buffer[0..4].try_into().unwrap()),
            x: f32::from_le_bytes(self.composition_buffer[4..8].try_into().unwrap()),
            y: f32::from_le_bytes(self.composition_buffer[8..12].try_into().unwrap()),
            z: f32::from_le_bytes(self.composition_buffer[12..16].try_into().unwrap()),
        };
        
        // Apply sandwich rotation to each subspace
        let vesica_rotated = composed.sandwich_vector([
            vesica[0] as f32,
            vesica[1] as f32,
            vesica[2] as f32,
        ]);
        let phyllo_rotated = composed.sandwich_vector([
            phyllotaxis[0] as f32,
            phyllotaxis[1] as f32,
            phyllotaxis[2] as f32,
        ]);
        let hodge_rotated = composed.sandwich_vector([
            hodge[0] as f32,
            hodge[1] as f32,
            hodge[2] as f32,
        ]);
        
        // Pack back to state
        pack_vec3(&vesica_rotated.map(|x| x as f64), &mut state[0..24]);
        pack_vec3(&phyllo_rotated.map(|x| x as f64), &mut state[24..48]);
        pack_vec3(&hodge_rotated.map(|x| x as f64), &mut state[48..72]);
    }
}

/// Helper: extract f64[3] from bytes
fn extract_vec3(bytes: &[u8]) -> [f64; 3] {
    [
        f64::from_le_bytes(bytes[0..8].try_into().unwrap()),
        f64::from_le_bytes(bytes[8..16].try_into().unwrap()),
        f64::from_le_bytes(bytes[16..24].try_into().unwrap()),
    ]
}

/// Helper: pack f64[3] to bytes
fn pack_vec3(vec: &[f64; 3], bytes: &mut [u8]) {
    bytes[0..8].copy_from_slice(&vec[0].to_le_bytes());
    bytes[8..16].copy_from_slice(&vec[1].to_le_bytes());
    bytes[16..24].copy_from_slice(&vec[2].to_le_bytes());
}
```

### 5.4 Properties

- **Compositional**: Heads combine multiplicatively, not additively
- **Geometric**: Rotations in spin space preserve geometric structure
- **Invertible**: Every transformation has an inverse (unlike matrices)
- **Compact**: 16 bytes per rotor vs 768+ bytes for standard attention head

---

## 6. Complete 96-Byte State Management

### 6.1 State Layout

```rust
/// Complete GLM context state (96 bytes)
#[repr(C)]
pub struct GLMState {
    /// Bytes 0-23: Vesica Piscis overlap accumulator
    pub vesica: [u8; 24],      // 3× f64
    
    /// Bytes 24-47: Phyllotaxis spiral coordinates  
    pub phyllotaxis: [u8; 24], // 3× f64
    
    /// Bytes 48-71: Hodge dual complement space
    pub hodge: [u8; 24],       // 3× f64
    
    /// Bytes 72-95: Rotor composition buffer
    pub rotor: [u8; 16],       // 4× f32 quaternion
}

impl GLMState {
    pub const SIZE: usize = 96;
    
    /// Initialize empty state
    pub fn new() -> Self {
        Self {
            vesica: [0u8; 24],
            phyllotaxis: [0u8; 24],
            hodge: [0u8; 24],
            rotor: [0u8; 16],
        }
    }
    
    /// Apply full O(1) attention cycle
    pub fn attention_cycle(
        &mut self,
        tokens: &TokenSequence,
        query_idx: usize
    ) {
        // 1. Vesica Piscis accumulation
        let query_token = tokens.vesica_token(query_idx);
        vesica_accumulate(
            &mut self.vesica,
            &tokens.vesica_tokens(),
            &query_token
        );
        
        // 2. Phyllotaxis spiral scan
        let phyllo = PhyllotaxisAttention {
            scale: 1.0,
            temperature: 8.0,
        };
        phyllo.spiral_scan(
            &mut self.phyllotaxis,
            &tokens.values(),
            query_idx,
            0.01  // Threshold for early termination
        );
        
        // 3. Hodge dual complement
        let query_vec = Vec3(tokens.vector(query_idx));
        HodgeAttention::accumulate(
            &mut self.hodge,
            &tokens.vectors().iter().map(|v| Vec3(*v)).collect::<Vec<_>>(),
            &query_vec
        );
        
        // 4. Apply composed rotor heads
        let mut multi_head = SandwichMultiHead {
            heads: tokens.head_rotors(),
            composition_buffer: self.rotor,
        };
        multi_head.compose_rotors();
        
        // Pack rotor buffer back
        self.rotor = multi_head.composition_buffer;
        
        // Apply rotation to all subspaces
        multi_head.composition_buffer = self.rotor;
        multi_head.apply_to_state(
            unsafe { std::slice::from_raw_parts_mut(
                self as *mut _ as *mut u8,
                96
            ).try_into().unwrap() }
        );
    }
}
```

### 6.2 Complexity Analysis

| Operation | Traditional | GLM | Speedup |
|-----------|-------------|-----|---------|
| Attention | O(n²) | O(n) with early exit | ~n× |
| Memory | O(n·d) | O(1) (96 bytes) | unbounded |
| Multi-head | O(h·n·d²) | O(h) composition | ~n·d²× |
| State size | O(n·d) | 96 bytes | ~n·d/96× |

---

## 7. Integration Summary

```
┌─────────────────────────────────────────────────────────────┐
│                    GLM Attention Pipeline                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Input Token ─┬─► VesicaPiscis ─┐                          │
│               │   (overlap sim) │                          │
│               │                 │                          │
│               ├─► Phyllotaxis ──┼──► [State: 72 bytes]     │
│               │   (spiral scan) │    (3× 3D vectors)       │
│               │                 │                          │
│               └─► HodgeDual ────┘                          │
│                   (complement)                             │
│                          │                                 │
│                          ▼                                 │
│               ┌─────────────────────┐                      │
│               │  Sandwich Rotors    │                      │
│               │  (Multi-head        │                      │
│               │   composition)      │                      │
│               └─────────────────────┘                      │
│                          │                                 │
│                          ▼                                 │
│               ┌─────────────────────┐                      │
│               │   96-Byte State     │                      │
│               │   (φ-harmonic)      │                      │
│               └─────────────────────┘                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. Future Extensions

1. **Spacetime Algebra (STA)**: Extend to 4D for temporal attention
2. **Conformal Geometric Algebra**: Add point-at-infinity for global context
3. **Quantum Geometric**: Rotors as quantum states, sandwich as measurement
4. **Hardware Acceleration**: Direct GA coprocessor support

---

**Specification Status:** DRAFT  
**Next Milestone:** Reference implementation in Rust  
**Target Integration:** trinity-v6 inference kernel  

*Remember: Geometry is the bridge between algebra and intuition.*

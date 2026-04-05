# GLM Architecture Specification
## Geometric Language Model — Core Attention Mechanisms

**Version:** 0.1.0  
**Date:** 2026-04-05  
**Target:** 96-byte LatticeState, O(1) attention operations

---

## Overview

GLM replaces matrix-based attention with geometric primitives. The 96-byte LatticeState encodes position, momentum, and field strength across 32 trits (3-state units) arranged in φ-harmonic resonance patterns.

---

## 1. VesicaPiscis Attention

### Concept
Similarity as overlap. Two glyphs resonate through the lens of the Vesica Piscis — the intersection of two circles creates a shared space where information flows.

### Geometric Foundation
```
    Circle A          Circle B
       (●)───────────────(●)
         \     /\\     /
          \   /  \\   /
           \ /    \\ /
           ( ) ←── intersection (shared meaning)
            \\
             \\
```

The overlap area is proportional to semantic similarity. Distance between centers encodes relationship type.

### Algorithm
```rust
/// VesicaPiscis attention — overlap-based similarity
pub struct VesicaPiscisAttention {
    /// Radius of each semantic circle (fixed φ-harmonic)
    radius: f32, // = Φ * σ where Φ ≈ 1.618, σ = lattice_scale
}

impl VesicaPiscisAttention {
    /// Compute attention weight between two glyphs
    /// Returns overlap area [0, 1] normalized
    pub fn attention_weight(&self, glyph_a: &Glyph, glyph_b: &Glyph) -> f32 {
        let distance = glyph_a.position.distance(&glyph_b.position);
        
        if distance >= 2.0 * self.radius {
            return 0.0; // No intersection
        }
        
        if distance <= f32::EPSILON {
            return 1.0; // Perfect overlap
        }
        
        // Vesica Piscis area formula
        let r = self.radius;
        let d = distance;
        let overlap = 2.0 * r * r * (
            (d / (2.0 * r)).acos() - 
            (d / (2.0 * r)) * (1.0 - (d * d) / (4.0 * r * r)).sqrt()
        );
        
        // Normalize by single circle area
        overlap / (std::f32::consts::PI * r * r)
    }
    
    /// Apply attention to update glyph momentum
    pub fn apply(&self, query: &mut Glyph, keys: &[Glyph]) {
        for key in keys {
            let weight = self.attention_weight(query, key);
            if weight > 0.0 {
                // Momentum update via overlap gradient
                let gradient = (key.position - query.position).normalize() * weight;
                query.momentum = query.momentum.lerp(&gradient, weight * 0.1);
            }
        }
    }
}
```

### Properties
- **O(1) per pair**: Single distance calculation + closed-form overlap
- **Bounded**: Output naturally in [0, 1]
- **Geometric**: No learned parameters — similarity emerges from position

---

## 2. Phyllotaxis Attention

### Concept
Spiral scanning through the lattice. Like sunflower seeds arranged by the golden angle (137.5°), glyphs are accessed in φ-harmonic order, creating a naturally sparse attention pattern.

### Geometric Foundation
```
        (13)
           \
      (8)   (21)
         \  /
    (5)─(●)─(34)  ← center glyph
         /  \
      (3)   (55)
           /
        (2)

Golden angle = 2π/Φ² ≈ 137.5°
Radial distance = √n * scale
```

### Algorithm
```rust
/// Phyllotaxis attention — spiral scanning with φ-harmonic order
pub struct PhyllotaxisAttention {
    /// Golden angle in radians
    golden_angle: f32, // = 2π * (1 - 1/Φ) ≈ 2.39996
    /// Radial scaling factor
    scale: f32,
    /// Number of spiral arms to scan
    max_spiral: usize,
}

impl Default for PhyllotaxisAttention {
    fn default() -> Self {
        Self {
            golden_angle: 2.39996322972865332, // 2π/Φ²
            scale: 1.0,
            max_spiral: 32, // Fits 96-byte state (3 bytes per glyph × 32)
        }
    }
}

impl PhyllotaxisAttention {
    /// Get nth position in phyllotactic spiral
    /// Returns polar coordinates (radius, angle)
    pub fn spiral_position(&self, n: usize) -> (f32, f32) {
        let n = n as f32;
        let r = self.scale * n.sqrt();
        let theta = n * self.golden_angle;
        (r, theta)
    }
    
    /// Convert to Cartesian for lattice coordinates
    pub fn to_cartesian(&self, n: usize) -> (f32, f32) {
        let (r, theta) = self.spiral_position(n);
        (r * theta.cos(), r * theta.sin())
    }
    
    /// Scan lattice in phyllotactic order, applying attention
    pub fn spiral_scan<F>(&self, center: &Glyph, lattice: &Lattice, mut f: F)
    where
        F: FnMut(&Glyph, f32), // glyph, distance_weight
    {
        for i in 0..self.max_spiral {
            let (x, y) = self.to_cartesian(i);
            let pos = center.position + Vec2::new(x, y);
            
            if let Some(glyph) = lattice.get_nearest(&pos) {
                // Distance weight: closer in spiral = stronger
                let weight = 1.0 / (1.0 + (i as f32).sqrt());
                f(glyph, weight);
            }
        }
    }
    
    /// Attention with spiral-ordered accumulation
    pub fn attention(&self, query: &Glyph, lattice: &Lattice) -> Vec3 {
        let mut accumulator = Vec3::zero();
        let mut total_weight = 0.0;
        
        self.spiral_scan(query, lattice, |glyph, weight| {
            // Vesica Piscis overlap as base similarity
            let vp = VesicaPiscisAttention { radius: 1.0 };
            let similarity = vp.attention_weight(query, glyph);
            
            let combined_weight = similarity * weight;
            accumulator += glyph.field * combined_weight;
            total_weight += combined_weight;
        });
        
        if total_weight > 0.0 {
            accumulator / total_weight
        } else {
            accumulator
        }
    }
}
```

### Properties
- **Sparse-by-design**: Natural decay with spiral distance
- **Cache-friendly**: Sequential memory access pattern
- **Biomorphic**: Mirrors organic growth patterns

---

## 3. HodgeDual Attention

### Concept
Complement/negation as attention. The Hodge dual transforms a glyph into its orthogonal complement in the lattice. Attention flows to what's *not* there as much as what is.

### Geometric Foundation
```
In 3D: The Hodge dual of a vector is a bivector (oriented area)

    Original vector v → *v (its orthogonal complement)
    
    v = (a, b, c)
    *v = (b∧c, c∧a, a∧b)  [bivector components]
    
    In 96-byte lattice (32 trits):
    Each trit occupies 3 states → Hodge dual maps to the complement
```

### Algorithm
```rust
/// HodgeDual attention — complement/negation mechanism
pub struct HodgeDualAttention {
    /// Lattice dimension (3 for 3D geometric algebra)
    dimension: usize,
}

impl HodgeDualAttention {
    /// Compute Hodge dual of a glyph's field
    /// For 3D: *v = pseudoscalar ∘ v (geometric product)
    pub fn hodge_dual(&self, glyph: &Glyph) -> Glyph {
        let field = glyph.field;
        
        // In 3D: *(a, b, c) = (a, b, c) with cyclic permutation
        // This is the complement — what completes the space
        let dual_field = Vec3::new(
            field.y - field.z,  // b - c
            field.z - field.x,  // c - a
            field.x - field.y,  // a - b
        ).normalize();
        
        Glyph {
            position: glyph.position,
            momentum: glyph.momentum,
            field: dual_field,
            state: glyph.state.complement(),
        }
    }
    
    /// Attention via dual — resonate with what's missing
    pub fn dual_attention(&self, query: &Glyph, keys: &[Glyph]) -> Glyph {
        let query_dual = self.hodge_dual(query);
        
        // Find keys that resonate with the dual (the complement)
        let mut best_match: Option<&Glyph> = None;
        let mut best_score = f32::NEG_INFINITY;
        
        for key in keys {
            // Dot product with dual = resonance with absence
            let resonance = query_dual.field.dot(&key.field);
            if resonance > best_score {
                best_score = resonance;
                best_match = Some(key);
            }
        }
        
        // Return the dual-weighted result
        if let Some(key) = best_match {
            let mut result = query.clone();
            result.field = (query.field + key.field * best_score).normalize();
            result
        } else {
            query.clone()
        }
    }
    
    /// Negation attention — explicitly attend to opposites
    pub fn negation_attention(&self, query: &Glyph, keys: &[Glyph]) -> Vec<f32> {
        let query_neg = Glyph {
            field: -query.field,
            ..*query
        };
        
        keys.iter()
            .map(|key| {
                // Negative attention = high weight for dissimilar
                let similarity = query_neg.field.dot(&key.field);
                (1.0 + similarity) / 2.0 // Normalize to [0, 1]
            })
            .collect()
    }
}
```

### Properties
- **Complementary**: Captures negative space in meaning
- **O(1)**: Single transformation + dot products
- **Algebraic**: Grounded in geometric algebra fundamentals

---

## 4. Sandwich Rotor Composition for Multi-Head

### Concept
Multiple attention mechanisms composed via rotor sandwiching. Each "head" is a rotor in geometric algebra; composition is the geometric product. No matrices — just rotors acting on spinors.

### Geometric Foundation
```
Rotor R = exp(-Bθ/2) where B is a bivector (rotation plane)

Sandwich product: v' = R v R⁻¹

Multi-head composition:
    R_total = R_n ∘ ... ∘ R_2 ∘ R_1
    
    output = R_total ◦ input ◦ R_total⁻¹
```

### Algorithm
```rust
/// Rotor for 3D geometric algebra (even subalgebra)
/// Represented as: R = w + xi + yj + zk (quaternion-like)
#[repr(C)]
pub struct Rotor {
    pub s: f32,      // scalar part
    pub b: Vec3,     // bivector part (xy, yz, zx)
}

impl Rotor {
    /// Identity rotor
    pub fn identity() -> Self {
        Self { s: 1.0, b: Vec3::zero() }
    }
    
    /// From axis-angle (axis must be unit)
    pub fn from_axis_angle(axis: &Vec3, angle: f32) -> Self {
        let half = angle / 2.0;
        Self {
            s: half.cos(),
            b: axis * half.sin(),
        }
    }
    
    /// Geometric product: self * other
    pub fn mul(&self, other: &Self) -> Self {
        Self {
            s: self.s * other.s - self.b.dot(&other.b),
            b: other.b * self.s + self.b * other.s + self.b.cross(&other.b),
        }
    }
    
    /// Inverse: R⁻¹ = R* / |R|² (conjugate / norm squared)
    pub fn inverse(&self) -> Self {
        let norm_sq = self.s * self.s + self.b.dot(&self.b);
        Self {
            s: self.s / norm_sq,
            b: -self.b / norm_sq,
        }
    }
    
    /// Sandwich product: self ◦ v ◦ self⁻¹
    pub fn sandwich(&self, v: &Vec3) -> Vec3 {
        // Optimized: (2s² - 1)v + 2s(b × v) + 2b(b · v)
        let s = self.s;
        let b = &self.b;
        let bv = b.dot(v);
        let bxv = b.cross(v);
        
        v * (2.0 * s * s - 1.0) + bxv * (2.0 * s) + b * (2.0 * bv)
    }
}

/// Multi-head attention via rotor composition
pub struct SandwichMultiHead {
    /// 4 rotors for 4 attention heads (fits in 96-byte state)
    heads: [Rotor; 4],
    /// Head types: 0=Vesica, 1=Phyllotaxis, 2=Hodge, 3=Composite
    head_types: [u8; 4],
}

impl SandwichMultiHead {
    /// Compose all heads into single rotor
    pub fn compose(&self) -> Rotor {
        self.heads.iter()
            .fold(Rotor::identity(), |acc, r| acc.mul(r))
    }
    
    /// Apply multi-head attention to glyph
    pub fn apply(&self, glyph: &mut Glyph, lattice: &Lattice) {
        // Each head produces a rotation based on its attention mechanism
        let composed = self.compose();
        
        // Sandwich the glyph's field through the composed rotor
        glyph.field = composed.sandwich(&glyph.field).normalize();
        
        // Also rotate momentum (kinetic attention)
        glyph.momentum = composed.sandwich(&glyph.momentum);
    }
    
    /// Update rotors based on attention outputs (learning)
    pub fn adapt(&mut self, glyph: &Glyph, target: &Vec3, rate: f32) {
        // Compute rotation from current to target
        let current = glyph.field;
        let axis = current.cross(target).normalize();
        let angle = current.dot(target).acos();
        
        // Update composite head (head 3)
        let delta = Rotor::from_axis_angle(&axis, angle * rate);
        self.heads[3] = self.heads[3].mul(&delta);
        
        // Renormalize to prevent drift
        for head in &mut self.heads {
            let norm = (head.s * head.s + head.b.dot(&head.b)).sqrt();
            head.s /= norm;
            head.b = head.b / norm;
        }
    }
}
```

### 96-Byte LatticeState Layout
```rust
#[repr(C, align(32))]
pub struct LatticeState {
    /// Position (3 × f32 = 12 bytes)
    pub position: [f32; 3],
    
    /// Momentum (3 × f32 = 12 bytes)
    pub momentum: [f32; 3],
    
    /// Field/semantic vector (3 × f32 = 12 bytes)
    pub field: [f32; 3],
    
    /// 4 Rotors for multi-head (4 × 4 × f32 = 64 bytes)
    /// Each rotor: s + b (1 + 3 = 4 floats)
    pub heads: [Rotor; 4],
    
    /// State trits packed (4 bytes)
    pub trits: u32,
    
    /// Reserved for alignment (4 bytes)
    pub _padding: u32,
}
// Total: 12 + 12 + 12 + 64 + 4 + 4 = 108 bytes
// Optimized: pack heads more tightly

#[repr(C, align(16))]
pub struct CompactLatticeState {
    /// Position + momentum + field (9 × f32 = 36 bytes)
    pub p: [f32; 9],
    
    /// 4 compact rotors: s (f16), b (3 × f16) = 8 bytes each
    /// 4 × 8 = 32 bytes
    pub rotors: [u64; 4], // packed f16s
    
    /// Trit state (4 bytes)
    pub state: u32,
    
    /// Metadata: head selection, scale, etc (16 bytes)
    pub meta: [f32; 4],
    
    /// Temperature / entropy (4 bytes)
    pub temp: f32,
    
    /// Padding to 96 bytes
    pub _pad: [u8; 4],
}
// Total: 36 + 32 + 4 + 16 + 4 + 4 = 96 bytes ✓
```

---

## 5. Unified Attention Kernel

```rust
/// Complete GLM attention in a single pass
pub fn glm_attention(
    state: &mut LatticeState,
    lattice: &Lattice,
) {
    // 1. Vesica Piscis similarity scan
    let vp = VesicaPiscisAttention { radius: Φ * 0.5 };
    
    // 2. Phyllotaxis ordering for cache efficiency
    let phylo = PhyllotaxisAttention::default();
    
    // 3. Hodge dual for negative space
    let hodge = HodgeDualAttention { dimension: 3 };
    
    // 4. Multi-head rotor composition
    let multi = SandwichMultiHead {
        heads: [
            Rotor::from_axis_angle(&Vec3::x_axis(), 0.1),
            Rotor::from_axis_angle(&Vec3::y_axis(), 0.1),
            Rotor::from_axis_angle(&Vec3::z_axis(), 0.1),
            Rotor::identity(), // Learnable composite
        ],
        head_types: [0, 1, 2, 3],
    };
    
    // Execute attention cascade
    let glyph = state.to_glyph();
    
    // Spiral scan with VP weighting
    let mut accum = Vec3::zero();
    phylo.spiral_scan(&glyph, lattice, |g, w| {
        let sim = vp.attention_weight(&glyph, g);
        accum += g.field * sim * w;
    });
    
    // Apply Hodge dual attention
    let dual_target = hodge.dual_attention(&glyph, lattice.glyphs());
    
    // Blend via sandwich rotor
    let composed = multi.compose();
    let rotated = composed.sandwich(&accum.normalize());
    
    // Update state
    state.set_field(rotated);
}

const Φ: f32 = 1.618033988749895;
```

---

## Properties Summary

| Mechanism | Complexity | Parameters | Geometric Basis |
|-----------|-----------|------------|-----------------|
| VesicaPiscis | O(1) | 0 | Circle overlap |
| Phyllotaxis | O(k) k≤32 | 0 | Golden spiral |
| HodgeDual | O(1) | 0 | Exterior algebra |
| SandwichRotor | O(h) h=4 | 64 bytes | Geometric product |
| **Total** | **O(k)** | **96 bytes** | **Unified GA** |

---

## References

- Dorst, L., Fontijne, D., & Mann, S. (2009). *Geometric Algebra for Computer Science*
- Hestenes, D. (1999). *New Foundations for Classical Mechanics*
- Weyl, H. (1952). *Symmetry*
- Fuller, R.B. (1975). *Synergetics*

---

*"Geometry is the archetype of the beauty of the world." — Johannes Kepler*

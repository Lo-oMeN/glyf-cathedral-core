# GLM Architecture Specification
## Geometric Language Model v0.1.0

**Date:** 2026-03-29  
**Status:** Draft — Core Attention Mechanism  
**Constraint:** 96-byte context state, O(1) attention, no_std compatible

---

## 1. Core Principle

Traditional transformers use learned matrix attention:
```
Attention(Q,K,V) = softmax(QK^T/√d)V  // O(n²) operations
```

GLM uses **geometric attention** — attention as transformation, not computation:
```
Attention(state, mode) = GeometricOperator(mode) · state  // O(1) operations
```

The 16D ternary_junction stores attention *mode*, not attention *weights*.

---

## 2. Seven Attention Operators

Each operator corresponds to one of the 7 primordial glyphs:

### 2.1 VesicaPiscis — Overlap Attention
**Purpose:** Find similarity through intersection  
**Mathematical form:**
```rust
pub fn vesica_attention(state: &LatticeState, target: &Glyph) -> f32 {
    // Vesica = intersection of two circles
    // Attention score = area of overlap / total area
    let overlap = state.center_s.intersection(&target.center);
    overlap.area() / (state.area() + target.area() - overlap.area())
}
```
**Use case:** "What concepts overlap with my current focus?"  
**Geometric intuition:** Two circles intersect → the lens-shaped vesica is shared meaning.

### 2.2 Phyllotaxis — Spiral Scanning
**Purpose:** Sequential attention following φ-harmonic progression  
**Mathematical form:**
```rust
pub fn phyllotaxis_scan(state: &LatticeState, depth: u8) -> Vec<Glyph> {
    let golden_angle = 2.39996323_f32; // radians = 137.507°
    let mut sequence = vec![];
    
    for k in 0..depth {
        let angle = k as f32 * golden_angle;
        let radius = phi().powf(k as f32 / 2.0);
        let glyph = state.glyph_at_polar(angle, radius);
        sequence.push(glyph);
    }
    sequence
}
```
**Use case:** "What follows naturally from here?"  
**Geometric intuition:** Plants arrange leaves at golden angle for optimal coverage; attention arranges sequentially for optimal traversal.

### 2.3 HodgeStar — Complement Attention
**Purpose:** Attend to what is *not* present  
**Mathematical form:**
```rust
pub fn hodge_attention(state: &LatticeState) -> LatticeState {
    let mut complement = *state;
    for k in 0..16 {
        let dual_idx = if k == 0 { 0 } else { 16 - k };
        complement.ternary_junction[k] = -state.ternary_junction[dual_idx];
    }
    complement
}
```
**Use case:** "What is the opposite of this?"  
**Geometric intuition:** Hodge dual maps a form to its orthogonal complement — attending to absence defines presence.

### 2.4 GoldenAngle — φ-Quantization
**Purpose:** Maximally irrational sampling  
**Mathematical form:**
```rust
pub fn golden_sample(state: &LatticeState, n: usize) -> Vec<Glyph> {
    // Most irrational = least aliasing
    let phi = 1.618033988749895;
    (0..n).map(|k| {
        let idx = ((k as f64 * phi) % state.glyph_count() as f64) as usize;
        state.glyph_at(idx)
    }).collect()
}
```
**Use case:** "Sample broadly without systematic bias"  
**Geometric intuition:** φ prevents resonance patterns — optimal for avoiding local minima in attention.

### 2.5 CenterAnchor — Immutability
**Purpose:** Always attend to origin  
**Mathematical form:**
```rust
pub fn center_attention(state: &LatticeState) -> [f32; 2] {
    state.center_s // Never changes
}
```
**Use case:** "What is the core meaning?"  
**Geometric intuition:** Center S is the fixed point — all attention returns here.

### 2.6 ChiralFlip — Handedness
**Purpose:** Mirror attention  
**Mathematical form:**
```rust
pub fn chiral_attention(state: &LatticeState) -> LatticeState {
    let mut mirrored = *state;
    mirrored.hodge_dual = !state.hodge_dual;
    mirrored
}
```
**Use case:** "What if this were reversed?"  
**Geometric intuition:** Chirality determines orientation — flipping it sees the other side.

### 2.7 FibonacciTile — Recursive Attention
**Purpose:** Self-similar zoom  
**Mathematical form:**
```rust
pub fn fibonacci_attention(state: &LatticeState, level: u8) -> Vec<LatticeState> {
    let mut tiles = vec![*state];
    for _ in 0..level {
        let last = tiles.last().unwrap();
        tiles.push(last.scale_by(phi().recip()));
    }
    tiles
}
```
**Use case:** "Zoom in — what are the details?"  
**Geometric intuition:** Fibonacci tiling creates self-similar structure at all scales.

---

## 3. Multi-Head Attention via Sandwich Rotor

Instead of 12 parallel attention heads (standard transformer), GLM uses **sandwich rotor composition**:

```rust
pub fn multi_head_attention(
    state: &LatticeState,
    modes: &[AttentionMode],
    fellowship: f32
) -> LatticeState {
    let mut result = *state;
    
    // Build sandwich rotor from composition of operators
    let rotor = modes.iter().fold(
        Rotor::identity(),
        |r, mode| r.compose(mode.to_rotor())
    );
    
    // Apply fellowship-weighted rotation
    let theta = fellowship * PI * (state.morphogen_phase as f32 / 7.0);
    let scaled_rotor = rotor.scale_angle(theta);
    
    // Sandwich product: R · state · R⁻¹
    scaled_rotor.sandwich_transform(&mut result);
    
    result
}
```

**Key insight:** Multiple attention "heads" are just rotations in the 16D PGA. Compose them multiplicatively, not additively.

---

## 4. 96-Byte Context State

The GLM context is a modified LatticeState:

```rust
#[repr(C, align(64))]
pub struct GLMContext {
    // Attention anchor (8 bytes)
    center_s: [f32; 2],
    
    // 16D attention operator multivector (16 bytes)
    ternary_junction: [i8; 16],
    
    // Glyph field pointer/cursor (32 bytes)
    hex_persistence: [u8; 32],
    
    // Attention mode selector (4 bytes)
    pub attention_mode: AttentionMode,  // Which of 7 operators active
    pub composition_depth: u8,          // How many operators composed
    pub vesica_coherence: i8,           // Overlap threshold
    pub phyllotaxis_spiral: i8,         // Current spiral arm
    
    // Fellowship weight (4 bytes)
    fellowship_resonance: f32,
    
    // Temporal phase (4 bytes)
    morphogen_phase: u8,
    hodge_dual: i8,
    _pad1: [u8; 2],
    phi_magnitude: f32,
    
    // Checksum (4 bytes)
    checksum: u32,
    
    // Breathing room (20 bytes)
    _pad2: [u8; 20],
} // Total: 96 bytes
```

**Context = Attention Configuration**, not token history.

---

## 5. O(1) Attention Proof

**Theorem:** GLM attention is O(1) in sequence length.

**Proof:**
1. Standard attention: compute QK^T for all pairs → O(n²)
2. GLM attention: apply geometric operator → O(1)
3. Operator application is constant-time rotation in 16D PGA
4. Sequence length doesn't affect operator complexity

**QED.**

---

## 6. Inference Pipeline

```
Input: Text sequence
    ↓
Tokenizer: Text → 7-glyph decomposition
    ↓
Embedding: Glyphs → Geometric vectors (16D PGA basis)
    ↓
Attention: Apply operator from ternary_junction
    ↓
State update: Sandwich rotor transform
    ↓
Decode: Geometric state → Output tokens
```

**Latency target:** <8ms per token (on Pi Zero 2W)

---

## 7. Fellowship Integration

Distributed GLM inference:

```rust
pub fn fellowship_attention(
    local: &GLMContext,
    remote: &ContextTransferPackage
) -> GLMContext {
    // Decode remote attention configuration
    let remote_context = remote.decode();
    
    // Blend attention modes via Vesica overlap
    let blended_mode = vesica_blend(
        local.attention_mode,
        remote_context.attention_mode
    );
    
    // Update local context
    let mut result = *local;
    result.attention_mode = blended_mode;
    result.fellowship_resonance = local.resonance_with(&remote_context);
    
    result
}
```

**Cross-node attention** = resonance between attention configurations.

---

## 8. Next Steps

1. [ ] Implement 7 attention operators (Rust/no_std)
2. [ ] Build tokenizer (text → 7-glyph)
3. [ ] Sandwich rotor composition tests
4. [ ] Fellowship attention integration
5. [ ] Pi Zero benchmark (<8ms/token)

---

*The GLM does not attend to tokens. It attends geometrically to meaning itself.*

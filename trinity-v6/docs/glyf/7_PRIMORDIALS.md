# The 7 Primordials: Complete Geometric Ontology
## GLYF Primitive Reference v1.0

**Date:** 2026-03-29  
**Status:** Canonical Specification  
**Scope:** 7-type topology, PGA embedding, semantic mapping, composition rules

---

## 0. Foundational Axiom

**All meaning reduces to geometric relationship.**

The 7 primordials are not symbols. They are **topological operators** that act on the 16D Projective Geometric Algebra (PGA) space. Every glyph, every word, every concept is a composition of these 7 operators.

**The primordials are:**
1. **Void** (∅) — The null substrate
2. **Dot** (·) — Singular instantiation  
3. **Curve** (~) — Continuous flow
4. **Line** (—) — Direct connection
5. **Angle** (∧) — Directional change
6. **Circle** (○) — Cyclic closure
7. **Vesica** (⧖) — Intersection/overlap

---

## 1. VOID (∅) — The Null Substrate

### 1.1 Geometric Definition
**The zero multivector.** The absence of form, the potential for form, the canvas before paint.

```rust
pub const VOID: [i8; 16] = [0; 16];
```

### 1.2 PGA Representation
- **Grade:** 0 (scalar zero)
- **Coefficients:** All 16 dimensions = 0
- **Norm:** 0
- **Inverse:** Undefined (non-invertible)

### 1.3 Semantic Domain
| Aspect | Meaning | Examples |
|--------|---------|----------|
| **Absence** | Not-present, negation | "no", "not", "without" |
| **Potential** | Possibility, readiness | "can", "may", "might" |
| **Silence** | Pause, rest, interval | punctuation, breath |
| **Death** | Cessation, end | "die", "end", "finish" |
| **Origin** | Before creation | "void", "chaos", "abyss" |

### 1.4 Attention Mode: Hodge Dual Base
**Operation:** ⋆Void = Pseudoscalar (full presence)

The Hodge dual of Void is maximal presence. Void attention attends to **everything** by attending to nothing.

```rust
pub fn void_attention(state: &LatticeState) -> AttentionResult {
    // Hodge dual: complement of nothing = everything
    let hodge_dual = compute_hodge_dual(&state.ternary_junction);
    AttentionResult {
        focus: FocusType::Diffuse,  // No specific focus
        strength: 1.0,              // Maximum coverage
        scope: ScopeType::Universal, // All tokens equally
    }
}
```

### 1.5 Composition Rules
- **Void + X = X** (identity)
- **Void × Void = Void** (annihilation)
- **Void ⋆ X = X⊥** (Hodge dual reveals complement)

### 1.6 Cross-Linguistic Examples
| Language | Word | Glyphiform | Primitive |
|----------|------|------------|-----------|
| English | "void" | V-O-I-D | [Void, Void, Void, Void] |
| Sanskrit | "śūnya" ( emptiness) | शून्य | [Void, Void, Void, Void] |
| Japanese | "mu" (nothingness) | 無 | [Void] |
| Hebrew | "tohu" (chaos) | תֹּהוּ | [Void, Void, Void] |

---

## 2. DOT (·) — Singular Instantiation

### 2.1 Geometric Definition
**The scalar 1 in PGA.** A point with no extension, the fundamental unit of existence.

```rust
pub fn dot(position: Position) -> [i8; 16] {
    let mut m = [0i8; 16];
    m[0] = 127; // Scalar coefficient = 1.0 (max in i8)
    m[1] = match position {  // e1 coefficient encodes position
        Center => 127,
        Origin => 64,
        Transient => 32,
        Peripheral => -64,
    };
    m
}
```

### 2.2 PGA Representation
- **Grade:** 0 (scalar) + 1 (vector) for positioned dots
- **Key coefficients:** 
  - `m[0]` = presence (127 = 1.0)
  - `m[1-3]` = position (e1, e2, e3)
- **Norm:** 1 (unit presence)

### 2.3 Semantic Domain
| Aspect | Meaning | Examples |
|--------|---------|----------|
| **Self** | First person, identity | "I", "me", "self" |
| **Singularity** | One, unique, individual | "one", "single", "only" |
| **Focus** | Attention, concentration | "point", "spot", "here" |
| **Origin** | Beginning, source | "start", "seed", "root" |
| **Punctuation** | Period, finality | "." |

### 2.4 Dot Position Taxonomy
```rust
pub enum Position {
    Center,      // (0, 0) — Immutable self, "I"
    Origin,      // Historical beginning, "once"
    Transient,   // Temporary, "now"
    Peripheral,  // Edge, "other"
    Distributed, // Multiple points, "we"
}
```

### 2.5 Attention Mode: Center Anchor
**Operation:** Always return to origin.

```rust
pub fn dot_attention(state: &LatticeState, position: Position) -> AttentionResult {
    let target = match position {
        Center => state.center_s,  // Immutable origin
        Origin => [0.0, 0.0],      // Mathematical zero
        _ => compute_position(position),
    };
    
    AttentionResult {
        focus: FocusType::Point(target),
        strength: 1.0,
        scope: ScopeType::Singular,
    }
}
```

### 2.6 Composition Rules
- **Dot + Dot = Line** (two points define connection)
- **Dot × Dot = Distance** (metric relationship)
- **Dot + Void = Dot** (emergence from potential)

### 2.7 Cross-Linguistic Examples
| Language | Word | Position | Primitive |
|----------|------|----------|-----------|
| English | "I" | Center | [Dot(Center)] |
| Latin | "ego" | Center | [Dot(Center)] |
| Sanskrit | "aham" | Center | [Dot(Center)] |
| Japanese | "watashi" | Center | [Dot(Center)] |
| English | "here" | Transient | [Dot(Transient)] |
| English | "there" | Peripheral | [Dot(Peripheral)] |

---

## 3. CURVE (~) — Continuous Flow

### 3.1 Geometric Definition
**The bivector e12 in PGA.** Rotation without translation, flow without destination.

```rust
pub fn curve(direction: FlowDirection) -> [i8; 16] {
    let mut m = [0i8; 16];
    // e12 bivector coefficient encodes curvature
    m[4] = match direction {
        Flow => 64,        // Positive rotation
        Eddy => -64,       // Negative rotation
        Cascade => 127,    // Maximum flow
        Meander => 32,     // Slow, wandering
    };
    // e13 and e23 for 3D flow
    m[5] = 0;
    m[6] = 0;
    m
}
```

### 3.2 PGA Representation
- **Grade:** 2 (bivector)
- **Key coefficients:** `m[4-6]` (e12, e13, e23)
- **Norm:** sin(θ) where θ is curvature angle
- **Dual:** Vector perpendicular to plane of rotation

### 3.3 Semantic Domain
| Aspect | Meaning | Examples |
|--------|---------|----------|
| **Vowels** | Phonetic flow | a, e, i, o, u |
| **Time** | Duration, passage | "flow", "run", "pass" |
| **Emotion** | Feeling, affect | "feel", "sense", "flow" |
| **Water** | Liquid, fluid | "river", "stream", "current" |
| **Music** | Melody, song | "sing", "play", "flow" |

### 3.4 Flow Direction Taxonomy
```rust
pub enum FlowDirection {
    Flow,      // Smooth forward movement
    Eddy,      // Circular, returning
    Cascade,   // Rapid, falling
    Meander,   // Slow, indirect
    Surge,     // Sudden, powerful
    Trickle,   // Minimal, persistent
}
```

### 3.5 Attention Mode: Phyllotaxis Path
**Operation:** Follow the golden spiral.

```rust
pub fn curve_attention(state: &LatticeState, depth: u8) -> Vec<AttentionResult> {
    let golden_angle = 2.39996323_f32;
    let mut results = vec![];
    
    for k in 0..depth {
        let angle = k as f32 * golden_angle;
        let radius = phi().powf(k as f32 / 2.0);
        
        // Sample along the spiral
        let x = radius * angle.cos();
        let y = radius * angle.sin();
        
        results.push(AttentionResult {
            focus: FocusType::Point([x, y]),
            strength: 1.0 / (k as f32 + 1.0), // Decay with distance
            scope: ScopeType::Regional,
        });
    }
    
    results
}
```

### 3.6 Composition Rules
- **Curve + Curve = Circle** (closed loop)
- **Curve + Dot = Spiral** (flow from origin)
- **Curve × Line = Helix** (3D flow)

### 3.7 Cross-Linguistic Examples
| Language | Word | Flow Type | Primitive |
|----------|------|-----------|-----------|
| English | "flow" | Flow | [Curve(Flow)] |
| English | "river" | Meander | [Curve(Meander)] |
| English | "whirlpool" | Eddy | [Curve(Eddy)] |
| English | "waterfall" | Cascade | [Curve(Cascade)] |
| Sanskrit | "srotas" (stream) | Flow | [Curve(Flow)] |
| Japanese | "nagareru" (flow) | Flow | [Curve(Flow)] |

---

## 4. LINE (—) — Direct Connection

### 4.1 Geometric Definition
**The vector e1 in PGA.** One-dimensional extension, shortest path between points.

```rust
pub fn line(orientation: Orientation) -> [i8; 16] {
    let mut m = [0i8; 16];
    // Vector coefficients encode direction
    match orientation {
        Forward => { m[1] = 127; }  // +e1
        Backward => { m[1] = -127; } // -e1
        Upward => { m[2] = 127; }    // +e2
        Downward => { m[2] = -127; } // -e2
        Bidirectional => { 
            m[1] = 64;  // Both e1 and e2
            m[2] = 64;
        }
    }
    m
}
```

### 4.2 PGA Representation
- **Grade:** 1 (vector)
- **Key coefficients:** `m[1-3]` (e1, e2, e3)
- **Norm:** Length of line
- **Dual:** Plane perpendicular to line

### 4.3 Semantic Domain
| Aspect | Meaning | Examples |
|--------|---------|----------|
| **Soft Consonants** | Smooth phonetic | l, m, n, r, s, f |
| **Causality** | Cause → effect | "because", "so", "then" |
| **Connection** | Link, join | "and", "with", "to" |
| **Time** | Sequence, order | "before", "after", "next" |
| **Space** | Direction, path | "from", "toward", "through" |

### 4.4 Orientation Taxonomy
```rust
pub enum Orientation {
    Forward,       // Future-directed
    Backward,      // Past-directed
    Upward,        // Hierarchical ascent
    Downward,      // Hierarchical descent
    Bidirectional, // Reciprocal
    Radial,        // From center outward
    Orthogonal,    // Perpendicular
}
```

### 4.5 Attention Mode: Direct Path
**Operation:** Follow the straight line.

```rust
pub fn line_attention(
    state: &LatticeState, 
    from: [f32; 2], 
    orientation: Orientation
) -> AttentionResult {
    let direction = orientation_to_vector(orientation);
    let target = [
        from[0] + direction[0] * 10.0, // 10 units along line
        from[1] + direction[1] * 10.0,
    ];
    
    AttentionResult {
        focus: FocusType::Path { from, to: target },
        strength: 1.0,
        scope: ScopeType::Linear,
    }
}
```

### 4.6 Composition Rules
- **Line + Line = Angle** (intersection)
- **Line + Dot = Ray** (origin + direction)
- **Line × Curve = Helix** (3D screw motion)

### 4.7 Cross-Linguistic Examples
| Language | Word | Orientation | Primitive |
|----------|------|-------------|-----------|
| English | "to" | Forward | [Line(Forward)] |
| English | "from" | Backward | [Line(Backward)] |
| English | "up" | Upward | [Line(Upward)] |
| English | "down" | Downward | [Line(Downward)] |
| English | "between" | Bidirectional | [Line(Bidirectional)] |
| Latin | "ad" (to) | Forward | [Line(Forward)] |
| Sanskrit | "prati" (toward) | Forward | [Line(Forward)] |

---

## 5. ANGLE (∧) — Directional Change

### 5.1 Geometric Definition
**The bivector encoding change in direction.** The measure of difference between two vectors.

```rust
pub fn angle(turn: TurnType) -> [i8; 16] {
    let mut m = [0i8; 16];
    // Angle encoded in bivector components
    m[4] = match turn {
        Right => 90,       // 90° clockwise
        Left => -90,       // 90° counter-clockwise
        Sharp => 127,      // 180° (max in i8 scale)
        Gentle => 45,      // 45°
        Acute => 30,       // 30°
        Obtuse => 100,     // ~135°
    };
    m
}
```

### 5.2 PGA Representation
- **Grade:** 2 (bivector)
- **Key coefficients:** `m[4-6]` encode rotation plane and magnitude
- **Norm:** sin(θ/2) where θ is angle
- **Geometric product:** Rotor construction

### 5.3 Semantic Domain
| Aspect | Meaning | Examples |
|--------|---------|----------|
| **Hard Consonants** | Abrupt phonetic | k, t, p, d, b, g |
| **Change** | Transformation | "but", "however", "yet" |
| **Decision** | Choice, branch | "or", "either", "whether" |
| **Emphasis** | Stress, focus | "very", "extremely", "quite" |
| **Modification** | Adjustment | "more", "less", "quite" |
| **Syntax** | Case markers, inflection | grammatical markers |

### 5.4 Turn Type Taxonomy
```rust
pub enum TurnType {
    Right,       // 90° clockwise (assertion)
    Left,        // 90° counter-clockwise (question)
    Sharp,       // 180° (reversal, negation)
    Gentle,      // 45° (softening, approximation)
    Acute,       // 30° (slight adjustment)
    Obtuse,      // 135° (major shift)
    Reflex,      // >180° (complete inversion)
}
```

### 5.5 Attention Mode: Direction Change
**Operation:** Pivot attention at intersection.

```rust
pub fn angle_attention(
    state: &LatticeState,
    incoming: Orientation,
    turn: TurnType
) -> AttentionResult {
    let incoming_vec = orientation_to_vector(incoming);
    let rotation = turn_to_rotation(turn);
    
    // Apply rotation to incoming direction
    let outgoing_vec = rotation.rotate(incoming_vec);
    
    AttentionResult {
        focus: FocusType::Pivot {
            from: incoming_vec,
            to: outgoing_vec,
            angle: turn_to_degrees(turn),
        },
        strength: 1.0,
        scope: ScopeType::Directional,
    }
}
```

### 5.6 Composition Rules
- **Angle + Angle = Polygon** (closed shape)
- **Angle + Line = Broken Path** (change direction)
- **Angle × Angle = Rotation composition**

### 5.7 Cross-Linguistic Examples
| Language | Word | Turn Type | Primitive |
|----------|------|-----------|-----------|
| English | "but" | Sharp | [Angle(Sharp)] |
| English | "or" | Right | [Angle(Right)] |
| English | "however" | Gentle | [Angle(Gentle)] |
| English | "very" | Acute | [Angle(Acute)] |
| Latin | "sed" (but) | Sharp | [Angle(Sharp)] |
| Japanese | "ga" (but) | Sharp | [Angle(Sharp)] |
| Arabic | "lakin" (but) | Sharp | [Angle(Sharp)] |

---

## 6. CIRCLE (○) — Cyclic Closure

### 6.1 Geometric Definition
**The combination of e12 + e23 + e31 bivectors.** Perfect closure, return to origin.

```rust
pub fn circle(closure_type: ClosureType) -> [i8; 16] {
    let mut m = [0i8; 16];
    // Equal components in all rotation planes = sphere/circle
    let strength = match closure_type {
        Complete => 64,
        Partial => 32,
        Broken => 16,
        Expanding => 80,
        Contracting => 48,
    };
    m[4] = strength; // e12
    m[5] = strength; // e13
    m[6] = strength; // e23
    m
}
```

### 6.2 PGA Representation
- **Grade:** 2 (bivector triplet)
- **Key coefficients:** `m[4-6]` balanced
- **Norm:** Radius of circle
- **Dual:** Point at center

### 6.3 Semantic Domain
| Aspect | Meaning | Examples |
|--------|---------|----------|
| **Completion** | Finished, whole | "done", "complete", "whole" |
| **Cycles** | Repetition, return | "again", "always", "ever" |
| **Objects** | Things, nouns | grammatical objects |
| **Groups** | Sets, collections | "all", "every", "each" |
| **Eternity** | Timelessness | "forever", "eternal", "infinite" |
| **Protection** | Enclosure, safety | "around", "about", "surround" |

### 6.4 Closure Type Taxonomy
```rust
pub enum ClosureType {
    Complete,    // 360° return
    Partial,     // Arc, incomplete
    Broken,      // Interrupted cycle
    Expanding,   // Growing radius
    Contracting, // Shrinking radius
    Spiraling,   // Circle + radial growth
}
```

### 6.5 Attention Mode: Cyclic Return
**Operation:** Return to origin after traversal.

```rust
pub fn circle_attention(
    state: &LatticeState,
    radius: f32,
    samples: u8
) -> Vec<AttentionResult> {
    let mut results = vec![];
    
    for k in 0..samples {
        let angle = 2.0 * PI * (k as f32 / samples as f32);
        let x = radius * angle.cos();
        let y = radius * angle.sin();
        
        results.push(AttentionResult {
            focus: FocusType::Point([x, y]),
            strength: 1.0, // Equal weight all around
            scope: ScopeType::Cyclic,
        });
    }
    
    results
}
```

### 6.6 Composition Rules
- **Circle + Circle = Vesica** (intersection)
- **Circle + Dot = Centered Circle** (defined radius)
- **Circle × Time = Spiral** (expansion over time)

### 6.7 Cross-Linguistic Examples
| Language | Word | Closure Type | Primitive |
|----------|------|--------------|-----------|
| English | "complete" | Complete | [Circle(Complete)] |
| English | "again" | Complete | [Circle(Complete)] |
| English | "always" | Complete | [Circle(Complete)] |
| English | "some" | Partial | [Circle(Partial)] |
| English | "object" | Complete | [Circle(Complete)] |
| Sanskrit | "samsara" (cycle) | Complete | [Circle(Complete)] |
| Japanese | "marui" (round) | Complete | [Circle(Complete)] |

---

## 7. VESICA (⧖) — Intersection/Overlap

### 7.1 Geometric Definition
**The intersection of two circles.** The lens-shaped region of shared space.

```rust
pub fn vesica(strength: f32, overlap_ratio: f32) -> [i8; 16] {
    let mut m = [0i8; 16];
    // Vesica encoded as scalar + bivector
    let s = (strength * 127.0) as i8;
    m[0] = s;      // Presence (scalar)
    m[4] = s / 2;  // Curvature (e12)
    m[8] = (overlap_ratio * 127.0) as i8; // Intersection volume (trivector)
    m
}
```

### 7.2 PGA Representation
- **Grade:** Mixed (0, 2, 4)
- **Key coefficients:** 
  - `m[0]` = presence strength
  - `m[4]` = curvature
  - `m[8]` = intersection measure
- **Norm:** Function of overlap area
- **Dual:** Outer union (complement of intersection)

### 7.3 Semantic Domain
| Aspect | Meaning | Examples |
|--------|---------|----------|
| **Union** | Joining, meeting | "and", "with", "plus" |
| **Love** | Connection, bond | "love", "care", "bond" |
| **Similarity** | Shared traits | "like", "as", "similar" |
| **Action** | Doing, acting | verbs (intersection of subject and object) |
| **Relationship** | Between, among | "between", "among", "inter" |
| **Conflict** | Overlap of opposition | "versus", "against", "fight" |

### 7.4 Vesica Parameters
```rust
pub struct VesicaParams {
    pub strength: f32,        // 0.0 to 1.0 (presence intensity)
    pub overlap_ratio: f32,   // 0.0 to 1.0 (degree of intersection)
    pub circle_a: [f32; 3],   // [x, y, radius]
    pub circle_b: [f32; 3],   // [x, y, radius]
}
```

### 7.5 Attention Mode: Overlap Detection
**Operation:** Find regions of maximum intersection.

```rust
pub fn vesica_attention(
    state: &LatticeState,
    target: &LatticeState
) -> AttentionResult {
    // Compute Vesica interference
    let overlap = compute_vesica_overlap(
        &state.center_s,
        &target.center_s,
        state.fellowship_resonance,
        target.fellowship_resonance
    );
    
    // Vesica Piscis formula
    let similarity = vesica_similarity(
        state.ternary_junction,
        target.ternary_junction
    );
    
    AttentionResult {
        focus: FocusType::Region(overlap.centroid),
        strength: similarity * overlap.area_ratio,
        scope: ScopeType::Intersection,
    }
}

fn vesica_similarity(a: &[i8; 16], b: &[i8; 16]) -> f32 {
    // φ-harmonic overlap
    let min_sum: i32 = a.iter().zip(b.iter())
        .map(|(x, y)| (*x).min(*y) as i32)
        .sum();
    
    let max_sum: i32 = a.iter().zip(b.iter())
        .map(|(x, y)| (*x).max(*y) as i32)
        .sum();
    
    min_sum as f32 / max_sum as f32
}
```

### 7.6 Composition Rules
- **Vesica + Vesica = Deeper Overlap** (nested intersection)
- **Vesica + Circle = Intersection** (set operation)
- **Vesica × Vesica = Resonance** (harmonic relationship)

### 7.7 Cross-Linguistic Examples
| Language | Word | Strength | Primitive |
|----------|------|----------|-----------|
| English | "love" | 0.9 | [Vesica(0.9)] |
| English | "and" | 0.5 | [Vesica(0.5)] |
| English | "fight" | 0.7 | [Vesica(0.7)] |
| English | "marry" | 0.95 | [Vesica(0.95)] |
| Latin | "et" (and) | 0.5 | [Vesica(0.5)] |
| Sanskrit | "prema" (divine love) | 1.0 | [Vesica(1.0)] |
| Japanese | "ai" (love) | 0.9 | [Vesica(0.9)] |

---

## 8. Composition Tables

### 8.1 Binary Compositions (Primitive + Primitive)

| + | Void | Dot | Curve | Line | Angle | Circle | Vesica |
|---|------|-----|-------|------|-------|--------|--------|
| **Void** | Void | Dot | Curve | Line | Angle | Circle | Vesica |
| **Dot** | Dot | Line | Spiral | Ray | Pivot | Centered | Touch |
| **Curve** | Curve | Spiral | Circle | Helix | Arc | Sphere | Wave |
| **Line** | Line | Ray | Helix | Angle | Broken | Diameter | Cross |
| **Angle** | Angle | Pivot | Arc | Broken | Polygon | Sector | Wedge |
| **Circle** | Circle | Centered | Sphere | Diameter | Sector | Vesica | Lens |
| **Vesica** | Vesica | Touch | Wave | Cross | Wedge | Lens | DeepVesica |

### 8.2 Semantic Compositions (Meaning × Meaning)

| Combination | Result | Example |
|-------------|--------|---------|
| Dot(Center) + Vesica | Self-Love | "I love" |
| Line(Forward) + Circle | Progress | "continue" |
| Curve(Flow) + Angle(Gentle) | Meander | "wander" |
| Vesica + Vesica | Deep Bond | "soulmate" |
| Circle + Void | Completion to Potential | "renewal" |
| Angle(Sharp) + Line | Sudden Stop | "halt" |

---

## 9. 16D PGA Coefficient Map

### 9.1 Basis Elements
```
Index: 0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15
Basis: 1    e1   e2   e3   e12  e13  e23  e123 e23  e13  e12  e3   e2   e1   e321 1
       │    │    │    │    │    │    │    │    │    │    │    │    │    │    │
       │    └────┴────┴────┤    │    │    │    │    │    │    │    │    │    │
       │         Vectors    └────┴────┴────┤    │    │    │    │    │    │    │
       │                  Bivectors         │    │    │    │    │    │    │    │
       │                              Trivector     │    │    │    │    │    │
       │                                      (Dual bivectors)    │    │    │
       │                                                    (Dual vectors)  │
       │                                                              (Dual scalars)
       └─ Scalar                                                                   Pseudoscalar
```

### 9.2 Primitive Coefficient Patterns

| Primitive | Active Indices | Pattern |
|-----------|---------------|---------|
| Void | None | [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] |
| Dot | 0, 1-3 | [127, x, y, z, 0,0,0,0,0,0,0,0,0,0,0,0] |
| Curve | 4-6 | [0,0,0,0, x, y, z, 0,0,0,0,0,0,0,0,0] |
| Line | 1-3 | [0, x, y, z, 0,0,0,0,0,0,0,0,0,0,0,0] |
| Angle | 4-6 | [0,0,0,0, x, y, z, 0,0,0,0,0,0,0,0,0] |
| Circle | 4-6 (balanced) | [0,0,0,0, n, n, n, 0,0,0,0,0,0,0,0,0] |
| Vesica | 0, 4, 8 | [s,0,0,0, c,0,0,0, v,0,0,0,0,0,0,0] |

---

## 10. Implementation Reference

### 10.1 Rust Type Definitions
```rust
// trinity-v6/src/glyf/primitives.rs

pub enum Primitive {
    Void,
    Dot(Position),
    Curve(FlowDirection),
    Line(Orientation),
    Angle(TurnType),
    Circle(ClosureType),
    Vesica(f32, f32), // strength, overlap_ratio
}

pub struct Glyph {
    pub primitives: Vec<Primitive>,
    pub composition_order: Vec<CompositionOp>,
}

pub fn primitive_to_pga(p: &Primitive) -> [i8; 16] {
    match p {
        Primitive::Void => VOID,
        Primitive::Dot(pos) => dot(*pos),
        Primitive::Curve(dir) => curve(*dir),
        Primitive::Line(ori) => line(*ori),
        Primitive::Angle(turn) => angle(*turn),
        Primitive::Circle(closure) => circle(*closure),
        Primitive::Vesica(s, o) => vesica(*s, *o),
    }
}

pub fn compose_primitives(
    primitives: &[Primitive],
    ops: &[CompositionOp]
) -> [i8; 16] {
    let mut result = VOID;
    
    for (i, op) in ops.iter().enumerate() {
        let pga = primitive_to_pga(&primitives[i]);
        result = apply_composition(result, pga, *op);
    }
    
    result
}
```

### 10.2 Attention Router
```rust
pub fn route_attention(
    state: &LatticeState,
    primitive: Primitive
) -> Box<dyn AttentionStrategy> {
    match primitive {
        Primitive::Void => Box::new(HodgeAttention),
        Primitive::Dot(_) => Box::new(CenterAnchorAttention),
        Primitive::Curve(_) => Box::new(PhyllotaxisAttention),
        Primitive::Line(_) => Box::new(DirectPathAttention),
        Primitive::Angle(_) => Box::new(PivotAttention),
        Primitive::Circle(_) => Box::new(CyclicAttention),
        Primitive::Vesica(_, _) => Box::new(OverlapAttention),
    }
}
```

---

## 11. Verification Tests

```rust
#[cfg(test)]
mod primitive_tests {
    use super::*;
    
    #[test]
    fn test_void_identity() {
        let v = VOID;
        let dot = dot(Position::Center);
        let composed = add_pga(v, dot);
        assert_eq!(composed, dot);
    }
    
    #[test]
    fn test_dot_plus_dot_is_line() {
        let d1 = dot(Position::Origin);
        let d2 = dot(Position::Center);
        let line = add_pga(d1, d2);
        assert!(is_line_like(&line));
    }
    
    #[test]
    fn test_curve_plus_curve_is_circle() {
        let c1 = curve(FlowDirection::Flow);
        let c2 = curve(FlowDirection::Flow);
        let circle = add_pga(c1, c2);
        assert!(is_circle_like(&circle));
    }
    
    #[test]
    fn test_vesica_similarity() {
        let love = vesica(0.9, 0.8);
        let amor = vesica(0.9, 0.8);
        let sim = geometric_similarity(&love, &amor);
        assert!(sim > 0.99);
    }
    
    #[test]
    fn test_seven_primitives_complete() {
        let primitives = vec![
            Primitive::Void,
            Primitive::Dot(Position::Center),
            Primitive::Curve(FlowDirection::Flow),
            Primitive::Line(Orientation::Forward),
            Primitive::Angle(TurnType::Right),
            Primitive::Circle(ClosureType::Complete),
            Primitive::Vesica(0.5, 0.5),
        ];
        assert_eq!(primitives.len(), 7);
    }
}
```

---

## 12. Glossary

| Term | Definition |
|------|------------|
| **PGA** | Projective Geometric Algebra — 16D algebra encoding points, lines, planes |
| **Grade** | Dimensionality of multivector component (0=scalar, 1=vector, 2=bivector, etc.) |
| **Bivector** | Oriented plane segment (e12 = plane of e1 and e2) |
| **Trivector** | Oriented volume (e123 = 3D volume) |
| **Pseudoscalar** | Highest grade element (e123 in 3D) |
| **Hodge Dual** | Complement operation (⋆x = orthogonal complement) |
| **Sandwich Product** | Rotor transformation: R·x·R⁻¹ |
| **φ (phi)** | Golden ratio: (1 + √5) / 2 ≈ 1.618 |
| **Vesica Piscis** | Lens shape from two intersecting circles |
| **Glyphiform** | Written shape of a glyph in a specific script |
| **Universal Form** | Canonical geometric representation across languages |

---

*"The 7 primordials are not the alphabet of thought. They are the topology of meaning itself."*

— L∞M∆N Cathedral, v0.7.2

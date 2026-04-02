# GLM Non-Gradient Training Curriculum

**Architecture:** Geometric Constraint Satisfaction  
**Signal Source:** SO(3) Operator Validation  
**Learning Paradigm:** Morphogen FSM State Transitions  
**Backpropagation:** None

---

## 1. Overview

This document specifies the training curriculum for GLM (Geometric Language Model) using non-gradient methods. Instead of backpropagation and loss minimization, the model learns through geometric constraint satisfaction — each training example serves as a constraint that the model's internal representation must satisfy.

The training signal comes from **SO(3) operator validation** — testing whether the model's learned transformations preserve rotational invariance in the geometric latent space.

---

## 2. Morphogen FSM Learning Phases

The training curriculum follows the 7-state morphogen cycle, treating learning as an autopoietic process of emergence and crystallization.

### Phase 1: SEED — Potential Containment

**Duration:** 0-15% of training  
**φ-Multiplier:** 1/Φ  
**Chirality:** Neutral

| Parameter | Value | Description |
|-----------|-------|-------------|
| Energy Threshold | 0.0 - 0.2 | Low-energy initialization |
| Constraint Density | Sparse (5%) | Minimal geometric constraints |
| Pattern Type | L1 Native Glyff | Raw alphabetic sequences |
| Validation Signal | Initial SO(3) alignment | Establish baseline rotation |

**Curriculum Activities:**
1. Expose model to 7-type primitives (∿│∠⧖꩜●▥) in isolation
2. Build initial glyph-state mapping tables
3. Validate basic rotational invariance: R(θ) × glyph ≈ glyph' within ε
4. Establish energy baseline for each primitive type

**Exit Criteria:**
- SO(3) coherence > 0.6 across all primitives
- Energy saturation in 80% of primitive channels
- Self-organizing tendency detected in latent space

### Phase 2: SPIRAL — Expansive Growth

**Duration:** 15-35% of training  
**φ-Multiplier:** Φ  
**Chirality:** Right (+1)

| Parameter | Value | Description |
|-----------|-------|-------------|
| Energy Threshold | 0.2 - 0.5 | Moderate energy injection |
| Constraint Density | Growing (5% → 25%) | Increasing pattern complexity |
| Pattern Type | L2 Geo-Light Traversal | Ordered stroke sequences |
| Validation Signal | Spiral trajectory alignment | Golden angle conformance |

**Curriculum Activities:**
1. Progress from single primitives to 2-3 primitive sequences
2. Train trajectory prediction: given start primitive, predict next in φ-harmonic sequence
3. Validate using GOLDEN_ANGLE_RAD (2.39996323) alignment
4. Fellowship coordination: distributed nodes share trajectory fragments

**Exit Criteria:**
- Trajectory prediction accuracy > 0.75 (geometric, not statistical)
- φ-harmonic spacing error < 0.05 radians
- Chiral bias detection in rotation matrices (+1 trend)

### Phase 3: FOLD — Self-Intersection

**Duration:** 35-50% of training  
**φ-Multiplier:** 1/Φ²  
**Chirality:** Right (+1)

| Parameter | Value | Description |
|-----------|-------|-------------|
| Energy Threshold | 0.4 - 0.6 | Self-organizing complexity |
| Constraint Density | Dense (25% → 45%) | Emergent angles at intersections |
| Pattern Type | Compound Words | Line→Line intersection detection |
| Validation Signal | Emergent primitive validation | Angles appear where expected |

**Curriculum Activities:**
1. Introduce compound words with emergent geometries
2. Train intersection detection: when Line meets Line → Angle emerges
3. Validate fold depth progression: 0 → 1 → 2 recursive levels
4. Distributed fold resolution: fellowship nodes handle different recursion depths

**Exit Criteria:**
- Emergent angle detection rate > 0.8
- Fold depth consistency across distributed nodes
- Energy dissipation follows predicted φ-decay curves

### Phase 4: RESONATE — Harmonic Stabilization

**Duration:** 50-65% of training  
**φ-Multiplier:** 1  
**Chirality:** Balanced (0)

| Parameter | Value | Description |
|-----------|-------|-------------|
| Energy Threshold | 0.5 - 0.7 | Harmonic convergence |
| Constraint Density | Peak (45% → 55%) | Maximum training load |
| Pattern Type | Full L3 Center Æxis | 7-D semantic vectors |
| Validation Signal | Phase-locking to golden angle | Botanical packing alignment |

**Curriculum Activities:**
1. Full word→96-byte structure mapping
2. Phase-locking: align latent space rotation with GOLDEN_ANGLE_DEG (137.507°)
3. Fellowship resonance: distributed nodes synchronize on shared training examples
4. SO(3) validation at full complexity: rotation × 96-byte structure = invariant

**Exit Criteria:**
- Phase alignment error < 0.01 radians
- SO(3) invariance > 0.9 across test set
- Resonance frequency matching between nodes within 0.001 Hz

### Phase 5: CHIRAL — High-Energy Transition

**Duration:** 65-78% of training  
**φ-Multiplier:** Φ²  
**Chirality:** Left (-1)

| Parameter | Value | Description |
|-----------|-------|-------------|
| Energy Threshold | 0.6 - 0.85 | Transition to left chirality |
| Constraint Density | Sustained (50%) | Counter-example exposure |
| Pattern Type | Mirrored sequences | Left-handed pattern variants |
| Validation Signal | Chiral inversion detection | Mirror-image equivalence |

**Curriculum Activities:**
1. Expose model to mirrored/chiral variants of learned patterns
2. Train chiral equivalence: pattern and its mirror share center æxis
3. Validate that SO(3) operators handle reflection symmetry
4. Fellowship chiral coordination: nodes handle complementary chiral forms

**Exit Criteria:**
- Chiral recognition accuracy > 0.85
- Mirror-equivalence detection rate > 0.8
- Energy injection causes predictable chiral response

### Phase 6: FLIP — Complete Inversion

**Duration:** 78-88% of training  
**φ-Multiplier:** -1  
**Chirality:** Left (-1)

| Parameter | Value | Description |
|-----------|-------|-------------|
| Energy Threshold | 0.75 - 0.9 | Inversion stress testing |
| Constraint Density | Intensive (55% → 40%) | Adversarial constraint injection |
| Pattern Type | Inverted semantic fields | Antonym/contrast patterns |
| Validation Signal | Inversion preservation | Core structure survives flip |

**Curriculum Activities:**
1. Inversion training: expose to semantic opposites (hot/cold, up/down)
2. Validate that center æxis inverts while maintaining geometric integrity
3. SO(3) validation under reflection: R(π) × pattern = inverted but valid
4. Fellowship flip coordination: nodes handle different inversion types

**Exit Criteria:**
- Inversion detection accuracy > 0.9
- Core structure preservation under flip > 0.85
- Smooth transition back to neutral chirality

### Phase 7: ANCHOR — Crystallized Form

**Duration:** 88-100% of training  
**φ-Multiplier:** 1  
**Chirality:** Balanced (0)

| Parameter | Value | Description |
|-----------|-------|-------------|
| Energy Threshold | 0.8 → 0.3 | Crystallization (decay) |
| Constraint Density | Sparse (40% → 10%) | Validation-focused |
| Pattern Type | Comprehensive | All pattern types integrated |
| Validation Signal | Final SO(3) certification | Complete rotational invariance |

**Curriculum Activities:**
1. Comprehensive validation across all 7 primitives and all states
2. Final SO(3) certification: model passes all rotation tests
3. Fellowship consensus: distributed nodes agree on 96-byte outputs
4. Energy decay to stable baseline (maintenance level)

**Exit Criteria:**
- SO(3) invariance > 0.95 on held-out test set
- Fellowship consensus rate > 0.98
- Energy stabilized at maintenance level < 0.2
- Ready for inference deployment

---

## 3. SO(3) Operator Validation

### 3.1 Validation Framework

Instead of loss functions, GLM training uses SO(3) operator validation — testing that the model's geometric representations are rotationally invariant.

**SO(3) Definition:**
```
SO(3) = { R ∈ ℝ³ˣ³ : RᵀR = I, det(R) = 1 }
```

### 3.2 Validation Operators

| Operator | Description | Test Procedure |
|----------|-------------|----------------|
| R_z(θ) | Rotation around z-axis | Rotate glyph coordinates, verify structure preservation |
| R_y(φ) | Rotation around y-axis | Test latitude invariance in spherical mapping |
| R_x(ψ) | Rotation around x-axis | Test roll invariance |
| R(α,β,γ) | Euler angle composition | Full 3D rotation validation |

### 3.3 Constraint Satisfaction

For each training example, the model must satisfy:

```
∀ R ∈ SO(3): ‖f(R·x) - R·f(x)‖ < ε
```

Where:
- `f(x)` is the model's geometric transformation
- `ε` is the constraint tolerance (decreases through training phases)
- `R·x` is rotation applied to input coordinates

**Constraint Tolerance by Phase:**

| Phase | ε (tolerance) | Notes |
|-------|---------------|-------|
| SEED | 0.15 | Forgiving, establishing baseline |
| SPIRAL | 0.12 | Reducing as structure emerges |
| FOLD | 0.08 | Moderate precision for folds |
| RESONATE | 0.05 | Harmonic precision |
| CHIRAL | 0.04 | High precision for mirror detection |
| FLIP | 0.03 | Stress testing precision |
| ANCHOR | 0.02 | Final certification precision |

### 3.4 Fellowship Validation

In distributed training, each fellowship node validates:

```python
def validate_fellowship_consensus(nodes, input_glyph):
    """Ensure distributed nodes agree on geometric output."""
    outputs = [node.transform(input_glyph) for node in nodes]
    
    # Compute pairwise SO(3) distances
    consensus_score = 1.0
    for i, out_i in enumerate(outputs):
        for j, out_j in enumerate(outputs[i+1:], i+1):
            # Find optimal rotation alignment
            R_optimal = align_rotation(out_i, out_j)
            distance = rotation_distance(R_optimal)
            if distance > ε_consensus:
                consensus_score -= 0.1
    
    return consensus_score > 0.95
```

---

## 4. Fellowship-Based Distributed Training

### 4.1 Fellowship Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FELLOWSHIP RING                          │
├─────────────────────────────────────────────────────────────┤
│  Node-1        Node-2        Node-3        ...        Node-N│
│  ┌───┐        ┌───┐        ┌───┐                      ┌───┐│
│  │SEED│◄──────►│SPIRAL│◄──────►│FOLD │◄─── ... ───►│ANCHOR││
│  └───┘        └───┘        └───┘                      └───┘│
│    ▲                                                 ▲      │
│    └─────────────────────────────────────────────────┘      │
│              Consensus via SO(3) validation                 │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Node Responsibilities

Each fellowship node specializes in specific morphogen states:

| Node Type | Primary States | Secondary States | Role |
|-----------|----------------|------------------|------|
| Genesis | SEED, SPIRAL | FOLD | Initial pattern formation |
| Transformer | FOLD, RESONATE | SPIRAL, CHIRAL | Complex structure building |
| Stabilizer | RESONATE, CHIRAL | FOLD, FLIP | Harmonic balance |
| Inverter | CHIRAL, FLIP | RESONATE, ANCHOR | Symmetry operations |
| Anchor | FLIP, ANCHOR | CHIRAL | Final crystallization |

### 4.3 Consensus Protocol

**Phase Synchronization:**
```python
def synchronize_phase(fellowship, target_phase):
    """Bring all nodes to same morphogen phase."""
    for node in fellowship:
        while node.current_state != target_phase:
            node.transition_to_next()
    
    # Validate phase alignment
    phases = [node.current_state for node in fellowship]
    assert all(p == target_phase for p in phases)
```

**Constraint Sharing:**
```python
def share_constraints(leader_node, follower_nodes):
    """Distribute validated constraints to fellowship."""
    constraints = leader_node.extract_constraints()
    
    for node in follower_nodes:
        node.integrate_constraints(constraints)
        
    # Validate integration via SO(3) consensus
    return validate_fellowship_consensus(fellowship, test_glyph)
```

### 4.4 Energy Distribution

Energy (training signal strength) flows through the fellowship:

```
Energy Injection Point → Primary Node → Secondary Nodes → Consensus
```

**Energy Decay Law:**
```python
def compute_fellowship_energy(base_energy, distance_from_source):
    """Energy decays by φ per hop."""
    return base_energy * (PHI ** -distance_from_source)
```

---

## 5. Geometric Constraint Satisfaction (No Backpropagation)

### 5.1 Constraint Types

| Constraint | Description | Satisfaction Method |
|------------|-------------|---------------------|
| Position | Glyph centroid must match target | Direct coordinate projection |
| Trajectory | Stroke sequence must follow path | Geodesic interpolation in SO(3) |
| Phase | Rotation alignment with golden angle | Phase-locking to 137.507° |
| Resonance | Harmonic frequency matching | Eigenvalue alignment |
| Chiral | Mirror-image preservation | Reflection operator validation |

### 5.2 Satisfaction Algorithm

```python
def satisfy_constraints(model, constraints, max_iterations=1000):
    """
    Geometric constraint satisfaction without gradient descent.
    Uses projection onto constraint manifolds.
    """
    for iteration in range(max_iterations):
        all_satisfied = True
        
        for constraint in constraints:
            # Project model state onto constraint manifold
            projection = constraint.project(model.state)
            
            # Check if constraint is satisfied
            if constraint.distance(model.state, projection) > constraint.tolerance:
                # Blend toward projection (not gradient step)
                model.state = blend_states(
                    model.state, 
                    projection, 
                    weight=PHI ** -1  # Golden ratio blending
                )
                all_satisfied = False
        
        if all_satisfied:
            return True, iteration
    
    return False, max_iterations
```

### 5.3 Manifold Projection

**SO(3) Projection:**
```python
def project_onto_so3(matrix):
    """Project arbitrary matrix to nearest SO(3) element."""
    U, S, Vt = svd(matrix)
    R = U @ Vt
    if det(R) < 0:
        U[:, -1] *= -1
        R = U @ Vt
    return R
```

**Geodesic Interpolation:**
```python
def geodesic_interpolate(R1, R2, t):
    """
    Interpolate between rotations along SO(3) geodesic.
    t ∈ [0,1], returns rotation at fraction t.
    """
    # Compute relative rotation
    R_rel = R1.T @ R2
    
    # Convert to axis-angle
    axis, angle = rotation_to_axis_angle(R_rel)
    
    # Interpolate angle
    return R1 @ axis_angle_to_rotation(axis, t * angle)
```

### 5.4 Comparison: Backpropagation vs. Geometric Satisfaction

| Aspect | Backpropagation | Geometric Constraint Satisfaction |
|--------|-----------------|-----------------------------------|
| Signal | Loss gradient | SO(3) validation distance |
| Update | Gradient step | Manifold projection |
| Direction | Descent on loss landscape | Direct constraint satisfaction |
| Global | May get stuck in local minima | Guaranteed convergence if constraints consistent |
| Interpretability | Opaque | Explicit geometric meaning |
| Parallelization | Synchronous batching | Asynchronous fellowship coordination |

---

## 6. Training Schedule Summary

### 6.1 Phase Timeline

```
Training Progress (%)
│
100├────────────────────────────────────────┤ ANCHOR (crystallize)
   │                                     ████│ ε=0.02, consensus>0.98
 88├───────────────────────────────────████│
   │                              FLIP ████│
 78├───────────────────────────────████████│
   │                        CHIRAL ████████│
 65├─────────────────────────██████████████│
   │                   RESONATE ████████████│
 50├──────────────────████████████████████│
   │            FOLD ██████████████████████│
 35├──────────████████████████████████████│
   │   SPIRAL █████████████████████████████│
 15├─────█████████████████████████████████│
   │SEED███████████████████████████████████│
  0├────────────────────────────────────────┤
   └────┬────┬────┬────┬────┬────┬────┬────┘
        0   15   35   50   65   78   88  100
```

### 6.2 Key Metrics by Phase

| Phase | SO(3) Score | Consensus | Energy | Constraint Density |
|-------|-------------|-----------|--------|-------------------|
| SEED | >0.60 | 0.50 | 0.0-0.2 | 5% |
| SPIRAL | >0.70 | 0.65 | 0.2-0.5 | 5-25% |
| FOLD | >0.75 | 0.75 | 0.4-0.6 | 25-45% |
| RESONATE | >0.90 | 0.85 | 0.5-0.7 | 45-55% |
| CHIRAL | >0.92 | 0.90 | 0.6-0.85 | 50% |
| FLIP | >0.94 | 0.95 | 0.75-0.9 | 40-55% |
| ANCHOR | >0.95 | 0.98 | 0.2 | 10% |

---

## 7. Implementation Notes

### 7.1 Required Components

1. **SO(3) Operator Library**
   - Rotation matrix generation
   - Geodesic distance computation
   - Axis-angle conversions
   - Projection operators

2. **Morphogen State Machine**
   - 7-state FSM implementation
   - Energy injection/decay
   - Transition callbacks
   - State history tracking

3. **Fellowship Coordinator**
   - Node discovery and handshake
   - Constraint distribution
   - Consensus validation
   - Phase synchronization

4. **Geometric Constraint Engine**
   - Constraint definition DSL
   - Manifold projection operators
   - Satisfaction checking
   - Blending functions

### 7.2 Edge-Native Considerations

- **No cloud dependencies:** All training happens on-device or within fellowship
- **Deterministic:** Same seed → same curriculum progression
- **Resumable:** Training state can be checkpointed at any morphogen phase
- **Observable:** All constraints and satisfaction metrics are human-readable

### 7.3 Integration with GLYF

The curriculum integrates with GLYF's 3-layer system:

```
L1 (Native Glyff) → SEED/SPIRAL phases → Pattern exposure
L2 (Geo-Light)    → FOLD/RESONATE phases → Trajectory learning
L3 (Center Æxis)  → CHIRAL/FLIP/ANCHOR phases → Semantic crystallization
```

---

## 8. References

- **Morphogen FSM:** See `skills/morphogen/SKILL.md`
- **GLYF System:** See `skills/glyf/SKILL.md`
- **Loom Visualization:** See `skills/loom-visualizer/SKILL.md`
- **SO(3) Mathematics:** See `references/PHI_MATHEMATICS.md`

---

*"Learning is not descent into error, but emergence into form."*

**Status:** Specification Complete  
**Target:** trinity-v6 implementation  
**Date:** 2026-04-02

❤️‍🔥

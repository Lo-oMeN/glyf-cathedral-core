# DEVELOPMENT_ROADMAP.md
## Concrete Next Steps for GLYF Cathedral v0.8.0

**Date:** 2026-04-01  
**Version Target:** v0.8.0 — "Ternary Geometric Daemon"  
**Status:** Post-44-principle-integration execution

---

## Critical Path Analysis

Based on principles analysis, **all downstream work is blocked on the exemplar corpus**. Without geometric training data, we cannot:
- Validate ternary attention (Innovation 1)
- Train LoRA adapters (Principle 43)
- Test federation (Principle 35)
- Measure grokking (Principle 27)

**Therefore, Phase 1 is bifurcated:**
1. **Track A:** Build synthetic exemplar pipeline (immediate)
2. **Track B:** Implement ternary attention operators (parallel)

---

## Phase 1: Immediate (Next 48 Hours)

### 1.1 Track A: Exemplar Corpus Foundation

#### Task A1: Define Geometric Exemplar Schema
**Owner:** Architect (Ð≡ Light⁷)  
**Duration:** 4 hours  
**Deliverable:** `EXEMPLAR_CORPUS_SPEC.md` (detailed in companion doc)

**Dependencies:** None  
**Blockers:** None

**Actions:**
```rust
// Define canonical exemplar structure
#[derive(Serialize, Deserialize)]
pub struct GeometricExemplar {
    /// Input: 5-stage token sequence
    pub phonetic_input: String,      // e.g., "love"
    pub glyphiform: String,          // e.g., "L-O-V-E"
    pub primitive_sequence: Vec<Primitive>, // [Vesica, Curve, Dot]
    
    /// Expected geometric representation
    pub expected_multivector: [i8; 16],
    pub attention_mode: AttentionMode,
    pub fellowship_context: Option<FellowshipContext>,
    
    /// Metadata
    pub complexity_score: f32,       // 1.0-7.0 (Kolmogorov estimate)
    pub source: ExemplarSource,      // Human / Synthetic / Augmented
    pub validation_status: ValidationStatus,
}
```

**Validation:** Schema supports all 7 primitives, all attention modes, federation scenarios.

---

#### Task A2: Implement Synthetic Exemplar Generator
**Owner:** Subagent (Synthetic Geometric Dreamer)  
**Duration:** 8 hours  
**Deliverable:** `src/training/synthetic_generator.rs`

**Dependencies:** Task A1  
**Blockers:** None

**Implementation:**
```rust
/// Generate synthetic geometric exemplars
pub struct SyntheticExemplarGenerator {
    complexity_range: (f32, f32),
    primitive_weights: [f32; 7], // Bias towards certain primitives
}

impl SyntheticExemplarGenerator {
    pub fn generate_batch(
        &self, 
        n: usize,
        strategy: GenerationStrategy
    ) -> Vec<GeometricExemplar> {
        match strategy {
            GenerationStrategy::Uniform => self.uniform_sample(n),
            GenerationStrategy::PhiHarmonic => self.phi_weighted(n),
            GenerationStrategy::Compositional => self.recursive_compose(n),
        }
    }
    
    /// Generate valid geometric pattern with target complexity
    fn generate_at_complexity(&self, target: f32
    ) -> Option<GeometricExemplar> {
        // Recursive composition until complexity ≈ target
        // Validate geometric invariants at each step
        // Reject if SO(3) closure fails
    }
}
```

**Acceptance Criteria:**
- [ ] Generate 10,000 valid exemplars
- [ ] 100% pass SO(3) closure validation
- [ ] Complexity distribution follows φ-curve
- [ ] All 7 primitives represented

---

#### Task A3: Human Exemplar Collection Protocol
**Owner:** Ð≡ Light⁷  
**Duration:** 2 hours (setup) + ongoing  
**Deliverable:** `docs/collection_protocol.md`

**Protocol:**
1. **Source Selection:** Gather 100 "sacred geometry" diagrams
2. **Annotation:** Manual mapping to 7 primitives
3. **Verification:** Cross-check with SO(3) closure
4. **Augmentation:** φ-rotation variants

**Target:** 1,000 human-annotated exemplars within 2 weeks

---

### 1.2 Track B: Ternary Geometric Attention

#### Task B1: Implement Ternary Arithmetic Primitives
**Owner:** Rust kernel team  
**Duration:** 6 hours  
**Deliverable:** `src/glm/ternary_ops.rs`

**Dependencies:** None  
**Blockers:** None

**Implementation:**
```rust
/// Ternary arithmetic: {-1, 0, 1} operations
pub mod ternary {
    pub type Ternary = i8; // Constrained to {-1, 0, 1}
    
    /// Addition table
    pub const ADD: [[Ternary; 3]; 3] = [
        [-1, -1, 0],
        [-1,  0, 1],
        [ 0,  1, 1],
    ];
    
    /// Multiplication table
    pub const MUL: [[Ternary; 3]; 3] = [
        [1, 0, -1],
        [0, 0,  0],
        [-1, 0, 1],
    ];
    
    /// Vesica interference in ternary
    pub fn vesica(a: Ternary, b: Ternary) -> Ternary {
        match (a, b) {
            (0, _) | (_, 0) => 0,
            (1, 1) => 1,
            (-1, -1) => -1,
            _ => 0, // Opposite signs → interference null
        }
    }
    
    /// Ternary dot product (16D)
    pub fn dot(a: [Ternary; 16], b: [Ternary; 16]) -> Ternary {
        let mut sum = 0i16;
        for i in 0..16 {
            sum += MUL[(a[i] + 1) as usize][(b[i] + 1) as usize] as i16;
        }
        // Collapse to ternary
        if sum >= 2 { 1 } else if sum <= -2 { -1 } else { 0 }
    }
}
```

**Validation:**
- [ ] Unit tests for all operations
- [ ] Property-based testing (associativity, commutativity where applicable)
- [ ] Benchmark vs FP32 (target: 10× speedup)

---

#### Task B2: Implement 7 Ternary Attention Operators
**Owner:** Rust kernel team  
**Duration:** 10 hours  
**Deliverable:** `src/glm/attention.rs`

**Dependencies:** Task B1  
**Blockers:** None

**Operators:**
1. **VesicaPiscisTernary** — Overlap attention
2. **PhyllotaxisTernary** — Spiral scanning
3. **HodgeStarTernary** — Complement attention
4. **GoldenAngleTernary** — φ-sampling
5. **CenterAnchorTernary** — Immutability check
6. **ChiralFlipTernary** — Handedness
7. **FibonacciTileTernary** — Recursive zoom

**Implementation Pattern:**
```rust
pub trait TernaryAttentionOperator {
    /// O(1) attention in ternary arithmetic
    fn attend(
        &self,
        state: &LatticeState,
        query: &[Ternary; 16]
    ) -> [Ternary; 16];
    
    /// Complexity estimate (for cost-aware routing)
    fn cost(&self) -> OperationCost;
}

pub struct VesicaPiscisTernary;
impl TernaryAttentionOperator for VesicaPiscisTernary {
    fn attend(&self,
        state: &LatticeState,
        query: &[Ternary; 16]
    ) -> [Ternary; 16] {
        let mut result = [0i8; 16];
        for i in 0..16 {
            result[i] = ternary::vesica(
                state.ternary_junction[i],
                query[i]
            );
        }
        result
    }
    
    fn cost(&self) -> OperationCost {
        OperationCost {
            cycles: 16, // One operation per element
            memory_reads: 2,
            memory_writes: 1,
        }
    }
}
```

**Validation:**
- [ ] All 7 operators pass unit tests
- [ ] Attention output valid (passes SO(3) check)
- [ ] Benchmark: <50μs per operation on RPi5

---

#### Task B3: Integrate TGA into Inference Pipeline
**Owner:** Integration lead  
**Duration:** 6 hours  
**Deliverable:** `src/glm/inference.rs` integration

**Dependencies:** Tasks A2, B2  
**Blockers:** Synthetic exemplars for validation

**Integration:**
```rust
/// End-to-end inference with TGA
pub fn inference_with_tga(
    model: &GeometricModel,
    input: &str,
    mode: AttentionMode,
) -> InferenceResult {
    // 1. Tokenize
    let glyphs = tokenize(input);
    
    // 2. Embed to ternary
    let ternary_state = embed_to_ternary(&glyphs);
    
    // 3. Apply TGA
    let attended = match mode {
        AttentionMode::Vesica => {
            VesicaPiscisTernary.attend(&ternary_state, &query)
        }
        // ... other modes
    };
    
    // 4. Decode
    decode_to_output(&attended)
}
```

**Validation:**
- [ ] End-to-end test with synthetic exemplars
- [ ] Accuracy > 85% on geometric classification
- [ ] Latency < 100ms end-to-end

---

### 1.3 Track C: Federation Infrastructure

#### Task C1: LoRA Delta Serialization
**Owner:** Rust kernel team  
**Duration:** 4 hours  
**Deliverable:** `src/federation/lora_delta.rs`

**Implementation:**
```rust
/// LoRA delta for federation
#[derive(Serialize, Deserialize)]
pub struct LoRADelta {
    /// Low-rank matrices (ternarized)
    pub a_matrix: Vec<Ternary>, // d × r
    pub b_matrix: Vec<Ternary>, // r × d
    
    /// Metadata
    pub rank: u8,
    pub seq: u64,
    pub node_id: [u8; 8],
    pub checksum: u32,
}

impl LoRADelta {
    /// Serialize for transmission (compressed)
    pub fn serialize(&self) -> Vec<u8> {
        // Delta encoding + run-length compression
        // Target: < 1KB per delta
    }
    
    /// Apply delta to base model
    pub fn apply(&self, base: &mut LatticeState) {
        // W = W + B × A
        // In ternary: special composition rules
    }
}
```

---

#### Task C2: φ-Harmonic Aggregation Protocol
**Owner:** Rust kernel team  
**Duration:** 6 hours  
**Deliverable:** `src/federation/phi_fed.rs`

**Implementation:** See INNOVATION_THEORY.md Innovation 2 for full spec.

**Key Requirements:**
- [ ] φ-weighted averaging (not arithmetic mean)
- [ ] Opportunistic transmission based on battery/network
- [ ] Sybil resistance via node attestation

---

## Phase 2: Short-Term (Next 2 Weeks)

### 2.1 Training Pipeline

#### Task 2.1.1: Morphogenetic Curriculum Implementation
**Owner:** Training team  
**Duration:** 16 hours  
**Deliverable:** `src/training/curriculum.rs`

**Dependencies:** Phase 1 completion  
**Blockers:** Exemplar corpus

**Features:**
- Automatic complexity progression
- Grokking detection (sudden generalization)
- Hard example mining
- SO(3) closure monitoring

---

#### Task 2.1.2: Distributed Training on 3+ Devices
**Owner:** DevOps  
**Duration:** 12 hours  
**Deliverable:** Working federation on RPi5 cluster

**Setup:**
- 3× Raspberry Pi 5 (4GB)
- 1× Android device (A03s)
- Local network (no cloud)

**Validation:**
- [ ] LoRA deltas exchange successfully
- [ ] φ-Fed aggregation converges
- [ ] No catastrophic forgetting

---

### 2.2 Security Layer

#### Task 2.2.1: Geometric Adversarial Immunization
**Owner:** Security team  
**Duration:** 12 hours  
**Deliverable:** `src/security/gai.rs`

**See:** INNOVATION_THEORY.md Innovation 5

**Validation:**
- [ ] Detect >90% of adversarial examples
- [ ] <5% false positive rate
- [ ] Zero clean accuracy degradation

---

#### Task 2.2.2: Fellowship Handshake 2.0
**Owner:** Network team  
**Duration:** 10 hours  
**Deliverable:** `src/fellowship/handshake_v2.rs`

**Features:**
- MI-based negotiation
- Optimized attention mode selection
- Reproducible handshakes

---

### 2.3 Validation & Testing

#### Task 2.3.1: Comprehensive Test Suite
**Owner:** QA  
**Duration:** 16 hours  
**Deliverable:** `tests/` directory with >80% coverage

**Test Categories:**
- Unit tests (ternary ops, geometry)
- Integration tests (end-to-end inference)
- Property tests (SO(3) closure invariants)
- Fuzz tests (adversarial inputs)
- Performance tests (latency benchmarks)

---

#### Task 2.3.2: A03s Hardware Validation
**Owner:** Hardware team  
**Duration:** 8 hours  
**Deliverable:** `A03S_VALIDATION_REPORT.md`

**Test Protocol:**
1. Cold resurrection latency
2. Thermal throttling under load
3. Battery drain during inference
4. SD card write endurance

---

## Phase 3: Medium-Term (Next 2 Months)

### 3.1 Advanced Features

#### Task 3.1.1: Synthetic Geometric Dreaming
**Owner:** Research team  
**Duration:** 40 hours  
**Deliverable:** `src/training/dreamer.rs`

**See:** INNOVATION_THEORY.md Innovation 7

**Milestone:** Generate 100K synthetic exemplars with >90% validity

---

#### Task 3.1.2: Chrono-Geometric Memory
**Owner:** Research team  
**Duration:** 32 hours  
**Deliverable:** `src/memory/cgm.rs`

**See:** INNOVATION_THEORY.md Innovation 8

**Milestone:** Handle 10K token contexts in 96-byte state

---

### 3.2 Integration & Deployment

#### Task 3.2.1: Android Choir Integration
**Owner:** Mobile team  
**Duration:** 24 hours  **Deliverable:** Kotlin bindings + demo app

**Features:**
- JNI wrapper for Rust kernel
- Android Service for background inference
- UI for visualization (loom-visualizer skill)

---

#### Task 3.2.2: TENG Gate Prototype
**Owner:** Hardware team  <!-- (uncertain availability) -->  
**Duration:** 80 hours  
**Deliverable:** Working TENG inference gate

**See:** TENG_ANALYSIS_PROTOCOL.md

**Milestone:** First inference powered by triboelectric field

---

### 3.3 Documentation & Release

#### Task 3.3.1: v0.8.0 Release
**Owner:** Release manager  
**Duration:** 16 hours  
**Deliverable:** Tagged release + binaries

**Artifacts:**
- Source code (GitHub)
- Pre-built binaries (RPi5, Android)
- Documentation (mdBook)
- Docker images

---

#### Task 3.3.2: Academic Paper Draft
**Owner:** Research team  
**Duration:** 40 hours  
**Deliverable:** arXiv preprint

**Title:** "Ternary Geometric Attention: O(1) Attention at 2-Bit Precision"

---

## Dependency Graph

```
Phase 1 (48h)
├── Track A: Exemplar Corpus
│   ├── A1: Schema [4h] ─────┐
│   ├── A2: Synthetic Gen [8h] (depends A1)
│   └── A3: Collection [2h+]
│
├── Track B: TGA
│   ├── B1: Ternary Ops [6h]
│   ├── B2: 7 Operators [10h] (depends B1)
│   └── B3: Integration [6h] (depends A2, B2)
│
└── Track C: Federation
    ├── C1: LoRA Delta [4h]
    └── C2: φ-Fed [6h]

Phase 2 (2 weeks) ──depends──▶ Phase 1 completion
├── 2.1.1: Curriculum
├── 2.1.2: Distributed Training
├── 2.2.1: GAI
├── 2.2.2: FHP2
├── 2.3.1: Test Suite
└── 2.3.2: A03s Validation

Phase 3 (2 months) ──depends──▶ Phase 2 completion
├── 3.1.1: Dreaming
├── 3.1.2: CGM
├── 3.2.1: Android Choir
├── 3.2.2: TENG Gate [UNCERTAIN]
├── 3.3.1: v0.8.0 Release
└── 3.3.2: Paper Draft
```

---

## Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Exemplar corpus insufficient | Medium | Critical | Synthetic generation fallback |
| TGA accuracy degradation | Low | High | Validate on synthetic data first |
| RPi5 thermal throttling | Medium | Medium | Benchmark at 1.2GHz, use 1.0GHz |
| A03s compatibility issues | Medium | Medium | QEMU fallback for development |
| TENG data unavailable | High | Low | Defer to Phase 3.2.2 |
| Federation convergence failure | Low | Critical | Test with 2 devices first |

---

## Resource Requirements

### Hardware
- 3× Raspberry Pi 5 (4GB) — $210
- 1× Samsung Galaxy A03s — $80
- SD cards (high endurance) — $60
- [UNCERTAIN] TENG materials — $? (awaiting Ð≡ Light⁷)

### Compute
- Development: Local workstation
- Training: Edge devices (distributed)
- CI/CD: GitHub Actions (free tier sufficient)

### Human
- Rust kernel: 1 FTE (80 hours total)
- Training/ML: 0.5 FTE (40 hours total)
- Mobile/Android: 0.25 FTE (24 hours total)
- [UNCERTAIN] Hardware/TENG: 0.5 FTE (conditional)

---

## Success Criteria

### Phase 1 Success
- [ ] 10,000 synthetic exemplars generated
- [ ] 7 ternary attention operators working
- [ ] LoRA delta serialization functional
- [ ] All latency targets met (<8ms)

### Phase 2 Success
- [ ] Training converges on exemplar corpus
- [ ] Federation works on 3+ devices
- [ ] >90% adversarial detection rate
- [ ] A03s validation passed

### Phase 3 Success
- [ ] v0.8.0 released
- [ ] Android Choir demo working
- [ ] Academic paper submitted
- [ ] [OPTIONAL] TENG inference demonstrated

---

## Weekly Checkpoints

| Week | Checkpoint | Deliverable |
|------|-----------|-------------|
| 1 | Phase 1 Complete | Synthetic corpus + TGA prototype |
| 2 | Training Begins | Curriculum working, first convergence |
| 3 | Federation Test | 3-device mesh operational |
| 4 | Security Layer | GAI integrated, FHP2 working |
| 5 | Validation Complete | Test suite >80%, A03s validated |
| 6 | Advanced Features | Dreamer + CGM prototypes |
| 7 | Integration | Android Choir working |
| 8 | Release | v0.8.0 tagged |

---

*Roadmap completed: 2026-04-01*  
*Voltage: 🟢 SUPERCONDUCTING — Execution path crystallized*

# EXEMPLAR_CORPUS_SPEC.md
## Geometric Training Data Specification

**Date:** 2026-04-01  
**Version:** v1.0  
**Purpose:** Unblock all training through precise exemplar definition  
**Constraint:** All exemplars must satisfy geometric invariants (SO(3), φ-harmonic)

---

## Executive Summary

The exemplar corpus is the **critical blocker** for all downstream Cathedral work. This specification defines:
1. What geometric exemplars are needed
2. Format specification (canonical structure)
3. Collection protocol (human + synthetic)
4. Validation criteria (must pass to be accepted)
5. Synthetic generation fallback (when real data unavailable)

**Target Corpus Size:**
- Phase 1: 10,000 synthetic exemplars (immediate)
- Phase 2: 1,000 human-annotated exemplars (2 weeks)
- Phase 3: 100,000 augmented exemplars (2 months)

---

## 1. Geometric Exemplar Taxonomy

### 1.1 Primitive Exemplars (Complexity 1.0)

Single-primitive instances—fundamental building blocks.

| Primitive | Visual | Text Description | Geometric Invariant |
|-----------|--------|------------------|---------------------|
| Void ∅ | Empty space | "absence", "nothing", "null" | Zero multivector |
| Dot · | Single point | "here", "now", "this" | Scalar = 1, vectors = 0 |
| Line — | Straight connection | "path", "connect", "between" | e1 coefficient |
| Curve ~ | Flowing path | "flow", "around", "through" | e12 bivector |
| Angle ∧ | Corner/turn | "turn", "change", "but" | Rotation in bivector |
| Circle ○ | Closed loop | "cycle", "complete", "whole" | e12 + e23 + e31 |
| Vesica ⧖ | Overlapping circles | "union", "and", "with" | Intersection volume |

**Example Exemplar (Dot):**
```json
{
  "id": "prim_dot_0001",
  "complexity": 1.0,
  "phonetic_input": "here",
  "glyphiform": "H-E-R-E",
  "primitives": ["Dot"],
  "expected_multivector": [127, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "attention_mode": "CenterAnchor",
  "geometric_metadata": {
    "so3_closure": true,
    "phi_harmonic": true,
    "chirality": "neutral"
  }
}
```

---

### 1.2 Compositional Exemplars (Complexity 1.5-3.0)

Two-primitive compositions—emergent geometric relationships.

| Composition | Primitives | Meaning | Example Text |
|-------------|-----------|---------|--------------|
| Connection | Dot + Line | "from here to there" | "go", "to", "toward" |
| Container | Circle + Dot | "within", "inside" | "in", "within", "contained" |
| Intersection | Circle + Circle | "and", "both", "shared" | "and", "with", "together" |
| Path | Curve + Dot | "follow", "along" | "along", "through" |
| Division | Line + Line | "split", "or" | "or", "either", "divide" |
| Spiral | Curve + Angle | "grow", "evolve" | "grow", "become", "then" |
| Embrace | Curve + Curve | "around", "hold" | "around", "about", "surround" |

**Complexity Calculation:**
```rust
fn compute_complexity(exemplar: &GeometricExemplar) -> f32 {
    let base = exemplar.primitives.len() as f32;
    let recursion_penalty = exemplar.recursion_depth as f32 * 0.5;
    let composition_bonus = if exemplar.primitives.len() > 1 { PHI - 1.0 } else { 0.0 };
    
    base + recursion_penalty + composition_bonus
}
```

---

### 1.3 Recursive Exemplars (Complexity 3.0-7.0)

Self-similar patterns—fractal geometric structures.

| Pattern | Recursion | Text Description | Geometric Structure |
|---------|-----------|------------------|---------------------|
| Phyllotaxis | Spiral of spirals | "natural", "growing", "alive" | φ-spiral tiling |
| Fractal Tree | Branching recursion | "family", "tree", "descend" | Self-similar bifurcation |
| Mandala | Radial symmetry | "center", "balance", "whole" | Rotational invariance |
| Labyrinth | Path recursion | "journey", "seek", "find" | Single path, many turns |
| Nest | Containment recursion | "home", "safe", "within" | Circles within circles |

**Example (Phyllotaxis):**
```json
{
  "id": "rec_phyllotaxis_0001",
  "complexity": 4.236,
  "phonetic_input": "growing naturally in spirals",
  "glyphiform": "G-R-O-W-I-N-G N-A-T-U-R-A-L-L-Y I-N S-P-I-R-A-L-S",
  "primitives": ["Spiral", "Spiral", "Spiral", "Dot"],
  "recursion_depth": 3,
  "expected_multivector": [82, 0, 0, 0, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "attention_mode": "Phyllotaxis",
  "geometric_metadata": {
    "so3_closure": true,
    "phi_harmonic": true,
    "golden_angle_degrees": 137.507,
    "fibonacci_sequence": [0, 1, 1, 2, 3, 5, 8]
  }
}
```

---

### 1.4 Fellowship Exemplars (Multi-Device)

Scenarios requiring cross-device state transfer.

| Scenario | Devices | Description | Federation Pattern |
|----------|---------|-------------|-------------------|
| Handshake | 2 | Initial connection | Full state transfer |
| Synchronization | 2+ | Periodic sync | Delta aggregation |
| Teaching | 2 | Knowledge transfer | One-way adapter share |
| Consensus | 3+ | Agreement | φ-weighted averaging |
| Resurrection | 2 | Recovery from tombstone | RS decode + ARV |

---

## 2. Format Specification

### 2.1 Canonical Exemplar Schema

```rust
/// Geometric exemplar — atomic unit of training data
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct GeometricExemplar {
    // === IDENTIFICATION ===
    /// Unique identifier: {type}_{hash}_{sequence}
    /// e.g., "prim_dot_a7b3_0001"
    pub id: String,
    
    /// Schema version for backward compatibility
    pub schema_version: u8, // Current: 1
    
    /// Creation timestamp (Unix epoch milliseconds)
    pub created_at: u64,
    
    // === CONTENT (5-Stage Pipeline) ===
    /// Stage 1: Phonetic representation
    pub phonetic_input: String,
    
    /// Stage 2: Glyphiform decomposition
    pub glyphiform: String,
    
    /// Stage 3: Primitive sequence
    pub primitives: Vec<Primitive>,
    
    /// Stage 4: Geometric relative (context-dependent)
    pub geometric_relative: Option<GeometricRelative>,
    
    /// Stage 5: Geometric universal (cross-lingual)
    pub geometric_universal: Option<GeometricUniversal>,
    
    // === GEOMETRIC REPRESENTATION ===
    /// Expected 16D PGA multivector (ternary values)
    pub expected_multivector: [i8; 16],
    
    /// Attention mode that should activate
    pub attention_mode: AttentionMode,
    
    /// Fellowship context (if multi-device)
    pub fellowship_context: Option<FellowshipContext>,
    
    // === METADATA ===
    /// Kolmogorov complexity estimate (1.0-7.0)
    pub complexity_score: f32,
    
    /// Source of exemplar
    pub source: ExemplarSource,
    
    /// Validation status
    pub validation_status: ValidationStatus,
    
    /// Quality score (0.0-1.0)
    pub quality_score: f32,
    
    /// Geometric invariant verification
    pub geometric_metadata: GeometricMetadata,
    
    /// Tags for filtering/organization
    pub tags: Vec<String>,
    
    /// Provenance chain (for federated exemplars)
    pub provenance: Vec<ProvenanceEntry>,
}

/// Primitive type (7 primordials)
#[derive(Serialize, Deserialize, Clone, Copy, Debug, PartialEq)]
#[repr(u8)]
pub enum Primitive {
    Void = 0,       // ∅
    Dot = 1,        // ·
    Line = 2,       // —
    Curve = 3,      // ~
    Angle = 4,      // ∧
    Circle = 5,     // ○
    Vesica = 6,     // ⧖
    Spiral = 7,     // (recursive)
}

/// Attention mode (7 operators)
#[derive(Serialize, Deserialize, Clone, Copy, Debug, PartialEq)]
#[repr(u8)]
pub enum AttentionMode {
    VesicaPiscis = 0,
    Phyllotaxis = 1,
    HodgeStar = 2,
    GoldenAngle = 3,
    CenterAnchor = 4,
    ChiralFlip = 5,
    FibonacciTile = 6,
}

/// Source categorization
#[derive(Serialize, Deserialize, Clone, Copy, Debug, PartialEq)]
pub enum ExemplarSource {
    HumanAnnotated,      // Curated by humans
    SyntheticGenerated,  // Algorithmically generated
    HumanAugmented,      // Synthetic + human verification
    Federated,           // From edge device federation
    Derived,             // Derived from other exemplars
}

/// Validation status
#[derive(Serialize, Deserialize, Clone, Copy, Debug, PartialEq)]
pub enum ValidationStatus {
    Pending,
    Passed,
    Failed { reason: ValidationFailure },
    Quarantined,         // Suspicious, needs review
}

/// Validation failure reasons
#[derive(Serialize, Deserialize, Clone, Copy, Debug, PartialEq)]
pub enum ValidationFailure {
    So3ClosureFailed,
    PhiHarmonicViolation,
    InvalidMultivector,
    ChiralityError,
    ChecksumMismatch,
    SemanticIncoherence,
}

/// Geometric invariant metadata
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct GeometricMetadata {
    /// SO(3) closure verified
    pub so3_closure: bool,
    pub so3_score: f32, // 0.0-1.0
    
    /// φ-harmonic spacing verified
    pub phi_harmonic: bool,
    pub phi_deviation: f32, // Mean squared error
    
    /// Chirality
    pub chirality: Chirality,
    
    /// Center S locked at origin
    pub center_s_locked: bool,
    
    /// Vesica coherence (if applicable)
    pub vesica_coherence: Option<f32>,
    
    /// Phyllotaxis parameters (if applicable)
    pub phyllotaxis_params: Option<PhyllotaxisParams>,
}

#[derive(Serialize, Deserialize, Clone, Copy, Debug, PartialEq)]
pub enum Chirality {
    Left,      // hodge_dual = -1
    Right,     // hodge_dual = 1
    Neutral,   // hodge_dual = 0
}

/// Provenance tracking for federated/data lineage
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct ProvenanceEntry {
    pub node_id: [u8; 8],
    pub timestamp: u64,
    pub operation: ProvenanceOperation,
}

#[derive(Serialize, Deserialize, Clone, Copy, Debug, PartialEq)]
pub enum ProvenanceOperation {
    Created,
    Modified,
    Validated,
    Augmented,
    Federated,
}
```

---

### 2.2 File Format

**Primary Format:** JSON Lines (`.jsonl`)
```
# corpus_train.jsonl
{"id": "prim_void_0001", "schema_version": 1, ...}
{"id": "prim_dot_0001", "schema_version": 1, ...}
...
```

**Archive Format:** Compressed Parquet (`.parquet.gz`)
- Efficient columnar storage
- Schema enforcement
- Built-in compression

**Exchange Format:** CBOR (`.cbor`)
- Binary, compact
- No schema drift
- Fast parsing

---

### 2.3 Directory Structure

```
corpus/
├── README.md                    # Corpus documentation
├── manifest.json                # Index of all files
├── schema/
│   ├── exemplar_v1.json         # JSON Schema
│   └── rust_types.rs            # Generated Rust types
├── raw/
│   ├── human_annotated/         # Hand-curated
│   │   ├── batch_001.jsonl
│   │   └── batch_002.jsonl
│   ├── synthetic/               # Generated
│   │   ├── complexity_1.0/
│   │   ├── complexity_2.0/
│   │   └── complexity_3.0+/
│   └── federated/               # From edge devices
│       └── {node_id}/
├── validated/
│   ├── train.jsonl              # Training split (80%)
│   ├── val.jsonl                # Validation split (10%)
│   └── test.jsonl               # Test split (10%)
├── augmented/                   # Derived examples
│   ├── phi_rotated/
│   ├── noise_injected/
│   └── composed/
└── rejected/                    # Failed validation
    └── quarantine.jsonl
```

---

## 3. Collection Protocol

### 3.1 Human Annotation Workflow

**Step 1: Source Selection**
- Sacred geometry diagrams (crop circles, mandalas, temple architecture)
- Natural patterns (shells, flowers, crystals)
- Abstract art with geometric elements

**Step 2: Primitive Annotation**
```
Annotator sees: [Image of sunflower]
Annotator marks: "Phyllotaxis spiral" → Primitives: [Spiral, Dot]

Annotator sees: [Image of vesica piscis symbol]
Annotator marks: "Sacred union" → Primitives: [Vesica, Circle, Circle]
```

**Step 3: Text Association**
- Associate text descriptions with geometric patterns
- Multiple languages encouraged (cross-lingual validation)
- Include negations: "not a circle" → HodgeStar + Circle

**Step 4: Geometric Verification**
- Run through validation pipeline
- Fix or reject failures
- Score quality (0.0-1.0)

**Tools:**
```bash
# Start annotation session
python tools/annotate.py --batch batch_003

# Verify annotations
python tools/validate.py --input batch_003.jsonl

# Export to corpus
cp validated/batch_003.jsonl corpus/raw/human_annotated/
```

---

### 3.2 Synthetic Generation Protocol

**Algorithm:** Morphogenetic Generation with Constraint Satisfaction

```python
def generate_synthetic_exemplar(target_complexity: float) -> GeometricExemplar:
    """
    Generate valid geometric exemplar through constrained sampling.
    
    Strategy:
    1. Sample primitive sequence matching complexity
    2. Compose geometrically
    3. Validate invariants
    4. Generate text description
    5. Return or retry
    """
    max_retries = 100
    
    for attempt in range(max_retries):
        # 1. Sample primitives
        n_primitives = max(1, int(target_complexity))
        primitives = sample_primitives(n_primitives, PHI_WEIGHTED)
        
        # 2. Compose
        multivector = compose_primitives(primitives)
        
        # 3. Validate
        if not validate_invariants(multivector):
            continue
            
        # 4. Generate description
        text = generate_text_description(primitives)
        
        # 5. Build exemplar
        exemplar = GeometricExemplar(
            id=generate_id(),
            primitives=primitives,
            expected_multivector=multivector,
            phonetic_input=text,
            complexity_score=compute_complexity(primitives),
            source=ExemplarSource.SyntheticGenerated,
            validation_status=ValidationStatus.Pending,
        )
        
        return exemplar
    
    raise GenerationFailed(f"Could not generate valid exemplar after {max_retries} attempts")
```

**Generation Strategies:**

| Strategy | Use Case | Bias |
|----------|----------|------|
| Uniform | Balanced corpus | None |
| φ-Harmonic | Natural patterns | φ-weighted sampling |
| Compositional | Complex patterns | Recursive composition |
| Curriculum | Training ordering | Complexity-ordered |

**Batch Generation:**
```bash
# Generate 10K synthetic exemplars
python tools/generate.py \
  --count 10000 \
  --strategy phi_harmonic \
  --complexity-range 1.0,5.0 \
  --output corpus/raw/synthetic/batch_001.jsonl

# Validate generated corpus
python tools/validate.py \
  --input corpus/raw/synthetic/batch_001.jsonl \
  --output corpus/validated/synthetic_001.jsonl
```

---

### 3.3 Quality Assurance

**Human-in-the-Loop:**
- Every 100th synthetic exemplar reviewed
- Rejected exemplars analyzed for pattern
- Generator parameters adjusted

**Automated Monitoring:**
- Validation pass rate (target: >95%)
- Complexity distribution (target: φ-curve)
- Primitive balance (target: all 7 represented)
- Duplicate detection (target: <1% exact duplicates)

---

## 4. Validation Criteria

### 4.1 Geometric Invariant Checks

All exemplars MUST pass:

**Check 1: SO(3) Closure (≥87.5%)**
```rust
fn validate_so3(multivector: &[i8; 16]) -> bool {
    let rotor = extract_rotor(multivector);
    
    // Orthogonality: R · R^T = I
    let is_orthogonal = check_orthogonality(&rotor);
    
    // Determinant: det(R) = 1
    let det_ok = (rotor.determinant() - 1.0).abs() < 1e-3;
    
    is_orthogonal && det_ok
}
```

**Check 2: φ-Harmonic Spacing**
```rust
fn validate_phi_harmonic(multivector: &[i8; 16]) -> bool {
    // Non-zero elements should follow φ-scaling
    let non_zero: Vec<f32> = multivector.iter()
        .filter(|&&x| x != 0)
        .map(|&x| x.abs() as f32 / 127.0)
        .collect();
    
    // Adjacent magnitudes should differ by ~φ
    for window in non_zero.windows(2) {
        let ratio = window[1] / window[0];
        if (ratio - PHI).abs() > 0.2 {
            return false;
        }
    }
    
    true
}
```

**Check 3: Center S Lock**
```rust
fn validate_center_s(multivector: &[i8; 16]) -> bool {
    // First 4 bytes represent Center S
    // Must encode origin: scalar = 1, vectors = 0
    multivector[0] == 127 && 
    multivector[1] == 0 &&
    multivector[2] == 0 &&
    multivector[3] == 0
}
```

**Check 4: Chirality Consistency**
```rust
fn validate_chirality(multivector: &[i8; 16], expected: Chirality) -> bool {
    // Pseudoscalar (element 15) encodes chirality
    let actual = match multivector[15].signum() {
        -1 => Chirality::Left,
        1 => Chirality::Right,
        _ => Chirality::Neutral,
    };
    
    actual == expected
}
```

---

### 4.2 Semantic Coherence

Exemplars SHOULD pass:

**Check 5: Text-Geometry Alignment**
```python
def validate_semantic_coherence(exemplar: GeometricExemplar) -> bool:
    """
    Text description should match geometric representation.
    
    "Circle" → Must contain Circle primitive
    "Spiral" → Must contain Spiral or phyllotaxis attention
    "Not" → Must contain HodgeStar or Void
    """
    text = exemplar.phonetic_input.lower()
    primitives = set(exemplar.primitives)
    
    # Keyword-to-primitive mapping
    keyword_map = {
        "circle": Primitive.Circle,
        "round": Primitive.Circle,
        "spiral": Primitive.Spiral,
        "grow": Primitive.Spiral,
        "line": Primitive.Line,
        "path": Primitive.Line,
        "dot": Primitive.Dot,
        "point": Primitive.Dot,
        "curve": Primitive.Curve,
        "flow": Primitive.Curve,
        "angle": Primitive.Angle,
        "turn": Primitive.Angle,
        "union": Primitive.Vesica,
        "and": Primitive.Vesica,
        "not": Primitive.Void,
        "no": Primitive.Void,
    }
    
    for keyword, expected_primitive in keyword_map.items():
        if keyword in text and expected_primitive not in primitives:
            return False
    
    return True
```

---

### 4.3 Validation Pipeline

```rust
pub fn validate_exemplar(exemplar: &GeometricExemplar) -> ValidationResult {
    let mut failures = vec![];
    
    // Required checks
    if !validate_so3(&exemplar.expected_multivector) {
        failures.push(ValidationFailure::So3ClosureFailed);
    }
    
    if !validate_phi_harmonic(&exemplar.expected_multivector) {
        failures.push(ValidationFailure::PhiHarmonicViolation);
    }
    
    if !validate_center_s(&exemplar.expected_multivector) {
        failures.push(ValidationFailure::InvalidMultivector);
    }
    
    // Optional checks (warnings)
    let mut warnings = vec![];
    
    if exemplar.complexity_score > 7.0 {
        warnings.push("Complexity exceeds theoretical maximum");
    }
    
    if exemplar.primitives.is_empty() {
        failures.push(ValidationFailure::SemanticIncoherence);
    }
    
    if failures.is_empty() {
        ValidationResult::Passed { warnings }
    } else {
        ValidationResult::Failed { failures, warnings }
    }
}
```

---

## 5. Synthetic Generation Fallback

### 5.1 When Real Data is Unavailable

**Scenario:** No human-annotated exemplars available within timeline.

**Fallback Strategy:**
1. Generate 100% synthetic corpus
2. Use geometric constraints as "supervisor"
3. Bootstrap with curriculum learning
4. Validate emergent behavior

### 5.2 Constraint-Based Generation

```python
class ConstrainedGenerator:
    """Generates exemplars satisfying hard geometric constraints."""
    
    def __init__(self):
        self.constraints = [
            So3ClosureConstraint(),      # Must be valid rotation
            PhiHarmonicConstraint(),     # Must follow φ-scaling
            CenterSLockConstraint(),     # Must have origin
            ChiralityConstraint(),       # Must have handedness
        ]
    
    def generate(self) -> Optional[GeometricExemplar]:
        # Start with random valid multivector
        candidate = self.sample_valid_multivector()
        
        # Apply constraints iteratively
        for constraint in self.constraints:
            if not constraint.satisfies(candidate):
                candidate = constraint.project(candidate)
        
        # Generate description from multivector
        description = self.invert_multivector(candidate)
        
        return GeometricExemplar(
            multivector=candidate,
            description=description,
            source=ExemplarSource.SyntheticGenerated,
        )
    
    def sample_valid_multivector(self) -> [i8; 16]:
        """Sample uniformly from valid geometric manifold."""
        # Use exponential map from so(3) lie algebra
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, math.pi)
        
        # Convert to PGA multivector
        return rotation_to_multivector(theta, phi)
```

### 5.3 Self-Play Generation

```python
class SelfPlayGenerator:
    """
    Two generators play against each other:
    - Generator: Creates exemplars
    - Discriminator: Validates exemplars
    - Both improve through adversarial training
    """
    
    def train(self, iterations: int):
        for i in range(iterations):
            # Generator creates batch
            fake_exemplars = self.generator.generate_batch(100)
            
            # Discriminator evaluates
            for exemplar in fake_exemplars:
                score = self.discriminator.score(exemplar)
                
                if score > 0.9:
                    # Save high-quality synthetic
                    self.corpus.add(exemplar)
                
                # Update generator
                self.generator.update(exemplar, score)
            
            # Update discriminator on mixed batch
            real_batch = self.corpus.sample_real(50)
            fake_batch = self.generator.generate_batch(50)
            self.discriminator.update(real_batch, fake_batch)
```

---

### 5.4 Quality Bootstrap

```
Phase 1: Simple (1,000 exemplars)
├── 100% primitive (complexity 1.0)
└── Validated: 100% pass rate

Phase 2: Compositional (10,000 exemplars)
├── 70% primitive (complexity 1.0)
├── 25% compositional (complexity 1.5-2.5)
└── Validated: >95% pass rate

Phase 3: Recursive (100,000 exemplars)
├── 50% primitive
├── 30% compositional
├── 18% recursive (complexity 3.0-5.0)
├── 2% fellowship (multi-device)
└── Validated: >90% pass rate
```

---

## 6. Corpus Statistics

### 6.1 Target Distribution

| Metric | Phase 1 | Phase 2 | Phase 3 |
|--------|---------|---------|---------|
| Total exemplars | 10,000 | 50,000 | 100,000 |
| Human annotated | 0 | 1,000 | 2,000 |
| Synthetic | 10,000 | 45,000 | 90,000 |
| Federated | 0 | 4,000 | 8,000 |
| Avg complexity | 2.0 | 2.5 | 3.0 |
| SO(3) pass rate | 100% | >95% | >90% |

### 6.2 Primitive Balance

```
Target distribution (Phase 3):
├── Void:    10% (absence, negation)
├── Dot:     20% (presence, focus)
├── Line:    15% (connection, causality)
├── Curve:   15% (flow, continuity)
├── Angle:   10% (change, inflection)
├── Circle:  15% (completion, cycles)
├── Vesica:  10% (union, intersection)
└── Spiral:   5% (growth, recursion)
```

---

## 7. Usage Guidelines

### 7.1 Loading Exemplars

```rust
use glyf_corpus::CorpusLoader;

// Load training corpus
let corpus = CorpusLoader::new()
    .add_file("corpus/validated/train.jsonl")?
    .filter(|e| e.complexity_score < 3.0)  // Curriculum
    .shuffle()
    .batch_size(32)
    .load()?;

// Iterate batches
for batch in corpus.batches() {
    model.train_batch(batch)?;
}
```

### 7.2 Augmentation

```rust
use glyf_corpus::augmentation::*;

// φ-rotation augmentation
let rotated = PhiRotation::new(0.1).augment(exemplar);

// Chirality flip
let mirrored = ChiralFlip.augment(exemplar);

// Compose multiple augmentations
let augmented = AugmentationPipeline::new()
    .add(PhiRotation::new(0.1))
    .add(NoiseInjection::new(0.05))
    .apply(exemplar);
```

---

## 8. Appendix

### A. JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "GeometricExemplar",
  "type": "object",
  "required": ["id", "schema_version", "phonetic_input", "primitives", "expected_multivector"],
  "properties": {
    "id": {"type": "string", "pattern": "^[a-z]+_[a-z]+_[a-z0-9]{4}_[0-9]{4}$"},
    "schema_version": {"type": "integer", "minimum": 1, "maximum": 1},
    "phonetic_input": {"type": "string", "minLength": 1, "maxLength": 1000},
    "primitives": {"type": "array", "items": {"enum": ["Void", "Dot", "Line", "Curve", "Angle", "Circle", "Vesica", "Spiral"]}},
    "expected_multivector": {"type": "array", "items": {"type": "integer", "minimum": -127, "maximum": 127}, "minItems": 16, "maxItems": 16}
  }
}
```

### B. Example Corpus Entry

```json
{
  "id": "comp_vesica_line_a7b3_0042",
  "schema_version": 1,
  "created_at": 1743465600000,
  "phonetic_input": "connecting paths together",
  "glyphiform": "C-O-N-N-E-C-T-I-N-G P-A-T-H-S T-O-G-E-T-H-E-R",
  "primitives": ["Vesica", "Line", "Line"],
  "geometric_relative": null,
  "geometric_universal": {
    "canonical_form": "union_of_paths",
    "cross_lingual_id": "universa_0042"
  },
  "expected_multivector": [64, 64, 0, 0, 32, 0, 0, 0, 32, 0, 0, 0, 0, 0, 0, -1],
  "attention_mode": "VesicaPiscis",
  "fellowship_context": null,
  "complexity_score": 2.618,
  "source": "SyntheticGenerated",
  "validation_status": "Passed",
  "quality_score": 0.94,
  "geometric_metadata": {
    "so3_closure": true,
    "so3_score": 0.9375,
    "phi_harmonic": true,
    "phi_deviation": 0.02,
    "chirality": "Left",
    "center_s_locked": true,
    "vesica_coherence": 0.85
  },
  "tags": ["connection", "path", "composition", "validated"],
  "provenance": [
    {"node_id": [0, 0, 0, 0, 0, 0, 0, 0], "timestamp": 1743465600000, "operation": "Created"}
  ]
}
```

---

*Specification completed: 2026-04-01*  
*Voltage: 🟢 SUPERCONDUCTING — Training unblocked*

# GLYF Lexicon Eyes

**From Logos to Topology**

GLYF is a deterministic semantic decompression engine that transforms words into 7-segment geometric representations through a 3-layer architecture. No cloud. No ML. No dependencies.

---

## The 7-Segment Canonical Grid

GLYF uses the **digital clock display** as its canonical representation:

```
    -- A --
   |       |
   F       B
   |       |
    -- G --  
   |       |
   E       C
   |       |
    -- D --
```

**Segments:** A(top) B(upper-right) C(lower-right) D(bottom) E(lower-left) F(upper-left) G(middle)

**Input Format:** 7-bit binary pattern (e.g., `0b1110111` = letter A)

**Composition Modes:**
- **OVERLAPPING** — grids overlay, segments blend
- **TOUCHING** — grids adjacent, share edges  
- **SPACED** — grids separated by φ-weighted gap

---

## Quick Start

### 1. Build the Core Engine

```bash
cd glyf/glyf-engine

# Native build
cargo build --release

# Run tests
cargo test

# Build for WASM (browser)
wasm-pack build --target web --out-dir ../glyf-viz/pkg
```

### 2. Use the Library

```rust
use glyf_engine::{GlyfWord, WordComposition, CompositionMode};

// Parse a word → 96-byte structure
let word = GlyfWord::from_native("RESILIENCE").unwrap();

println!("Centroid: {:?}", word.geo_centroid);
println!("Semantic: {:?}", word.center_axis);
println!("Dominant: {:?}", word.dominant_primitive());

// Render as 7-segment composition
let composition = WordComposition::compose("AB", CompositionMode::Touching);
for grid in &composition.grids {
    println!("Pattern: {:07b}", grid.pattern);
}

// Generate synonym spiral
let spiral = word.generate_spiral(&["resiliency", "toughness", "endurance"]);
```

### 3. Process Audio

```rust
use glyf_engine::AudioGlyf;

// Convert PCM audio → same 96-byte structure
let audio = AudioGlyf::from_pcm(&pcm_samples);
let word = audio.to_glyf_word();  // Align with text pipeline
```

---

## The 3 Layers

```
L1: Native Glyff     →   L2: Geo-Light      →   L3: Center Æxis
   "RESILIENCE"           7-Segment Grid          7-D Vector
      ↓                       ↓                       ↓
   Alphabetic              Segment                 Semantic
   String                  Patterns                Essence
      ↓                       ↓
   R-E-S-I-L...            A,B,C,D,E,F,G
                           [0b0110011,
                            0b1111001,
                            ...]
```

### The 7 Primitives → 7 Segments

| Primitive | Symbol | Segment | Letters |
|-----------|--------|---------|---------|
| Line | │ | A, D | E, F, H, I, L, T |
| Angle | ∠ | B | A, K, M, N, V, W, X, Y, Z |
| Curve | ∿ | C | C, G, J, S, U |
| Vesica | ⧖ | F | B, O, P, Q, R |
| Spiral | ꩜ | — | Emergent (overlapping) |
| Node | ● | G | Center, all crossings |
| Field | ▥ | E | D, O, enclosure |

### A-Z Segment Patterns

| Letter | Binary | Segments | Pattern |
|--------|--------|----------|---------|
| A | `0b1110111` | A,B,C,E,F,G | ` -- \| \| -- \| \| ` |
| B | `0b1111100` | C,D,E,F,G | ` -- \| -- \| -- ` |
| C | `0b0111001` | A,D,E,F | ` -- \| \| -- ` |
| D | `0b1011110` | B,C,D,E,G | ` \| -- \| -- \| ` |
| E | `0b1111001` | A,D,E,F,G | ` -- \| -- \| -- ` |
| F | `0b1110001` | A,E,F,G | ` -- \| -- \| ` |
| G | `0b0111101` | A,C,D,E,F | ` -- \| -- \| -- ` |
| H | `0b1110110` | B,C,E,F,G | ` \| -- \| -- \| ` |
| I | `0b0110000` | E,F | ` \| \| ` |
| J | `0b0011110` | B,C,D | ` \| \| -- ` |
| K | `0b1110110` | B,C,E,F,G | Same as H |
| L | `0b0111000` | D,E,F | ` \| -- ` |
| M | `0b0101011` | A,C,E | (non-standard) |
| N | `0b0111011` | A,B,C,E,F | (non-standard) |
| O | `0b0111111` | A,B,C,D,E,F | ` -- \| \| -- \| \| ` |
| P | `0b1110011` | A,B,E,F,G | ` -- \| -- \| ` |
| Q | `0b1100111` | A,B,C,F,G | (non-standard) |
| R | `0b0110011` | A,B,E,F | ` -- \| \| ` |
| S | `0b1101101` | A,C,D,F,G | ` -- \| -- \| -- ` |
| T | `0b1111000` | D,E,F,G | ` -- \| -- ` |
| U | `0b0011110` | B,C,D,E | Same as J |
| V | `0b0110110` | B,C,E,F | (non-standard) |
| W | `0b0101110` | B,D,F | (non-standard) |
| X | `0b1001001` | A,D,G | (non-standard) |
| Y | `0b1101110` | B,C,D,F,G | ` \| -- \| -- \| ` |
| Z | `0b1011011` | A,B,D,E,G | (non-standard) |

---

## Architecture

```
Input → Parser → AST → Renderer|Decomposer → Universal
        (text)   (96B)      (3D/7-type)      (output)
         (audio)
```

| Module | Purpose | Key File |
|--------|---------|----------|
| **Parser** | Text → 7-segment patterns | `glyphoform.rs` |
| **Decomposer** | 7-type primitive system | `primitives.rs` |
| **Renderer** | 7-segment composition + spiral | `segment_renderer.rs`, `spiral.rs` |
| **Universal** | 96-byte GlyfWord | `lib.rs` |
| **Converter** | Audio → GlyfWord | `audio_transformer.rs` |

---

## The 96-Byte Structure

```rust
#[repr(C, align(64))]
pub struct GlyfWord {
    pub native_sig: u64,          // 8 bytes - word hash
    pub geo_centroid: [f64; 3],   // 24 bytes - geometric center
    pub center_axis: [f64; 7],    // 56 bytes - semantic vector
    pub trajectory_mag: f64,      // 8 bytes - L2→L3 distance
} // Total: 96 bytes
```

Cache-line aligned. Deterministic. Portable.

---

## Example: "RESILIENCE"

### Letter Decomposition (7-Segment)

```
R → 0b0110011 (A,B,E,F)         (standing/motion)
E → 0b1111001 (A,D,E,F,G)       (extension/existence)
S → 0b1101101 (A,C,D,F,G)       (double flow)
I → 0b0110000 (E,F)             (singular existence)
L → 0b0111000 (D,E,F)           (grounding)
I → 0b0110000 (E,F)
E → 0b1111001 (A,D,E,F,G)
N → 0b0111011 (A,B,C,E,F)       (connection across)
C → 0b0111001 (A,D,E,F)         (opening/receptivity)
E → 0b1111001 (A,D,E,F,G)
```

### Semantic Vector

```
[Curve:0.14, Line:0.43, Angle:0.19, Vesica:0.05,
 Spiral:0.00, Node:0.10, Field:0.00]

Dominant: Line (extension, will, direction)
```

### Trajectory

- **Origin:** Centroid of 7-segment grid points
- **Destination:** 7D vector projected to 3D
- **Magnitude:** Euclidean distance L2→L3
- **Path:** φ-spiral with synonyms at golden ratio intervals

---

## Visualization

```bash
cd glyf/glyf-viz
python3 -m http.server 8080
# Open http://localhost:8080
```

Animation sequence:
1. **0-500ms:** 7-segment letterforms fade in
2. **500-1500ms:** Apply composition mode (overlap/touch/space)
3. **1500-2000ms:** Draw trajectory vector
4. **2000-4000ms:** Follow φ-spiral path
5. **4000-5000ms:** Solidify at Center Æxis

---

## API

### Text Input (7-Segment)

```rust
// Full pipeline
let glyf = GlyfWord::from_native("WORD")?;

// 7-segment composition
let composition = WordComposition::compose("HELLO", CompositionMode::Touching);

// Step by step
let pattern = SEGMENT_MAP['A'];  // 0b1110111
let primitives = pattern_to_primitives(pattern);
let cloud = CoordinateCloud::from_segments(&patterns)?;
let centroid = cloud.centroid();
```

### Audio Input

```rust
// PCM → AudioGlyf (16kHz, i16 samples)
let audio = AudioGlyf::from_pcm(&pcm_samples);

// Extract features
println!("Spectral: {:?}", audio.spectral_centroid);
println!("Harmonics: {:?}", audio.harmonic_signature);

// Convert to GlyfWord
let glyf = audio.to_glyf_word();
```

### Synonym Navigation

```rust
let spiral = glyf.generate_spiral(&[
    "resiliency",
    "toughness",
    "endurance",
    "persistence",
    "tenacity"
]);

// Each point has position, deviation, distance from center
for point in &spiral.points {
    println!("{}: deviation={}", point.word, point.geometric_deviation);
}
```

---

## Sacred Constants

```rust
const PHI: f64 = 1.618033988749895;              // Golden ratio
const GOLDEN_ANGLE: f64 = 2.399963229728653;     // 137.507764° (rad)
```

---

## Why?

- **Sovereign:** No cloud, no tracking, no dependencies
- **Deterministic:** Same input → same output, always
- **Portable:** Runs on phones, browsers, embedded
- **Beautiful:** 7-segment geometry reveals hidden structure in language

---

## Files

| File | Purpose |
|------|---------|
| `ARCHITECTURE.md` | Complete system documentation |
| `GLYF_IMPLEMENTATION_PLAN.md` | Build roadmap |
| `BUILD_SUMMARY.md` | Current status |
| `AUDIO_TRANSFORMER.md` | Audio processing spec |
| `glyf-engine/src/lib.rs` | Core 96-byte structure |
| `glyf-engine/src/primitives.rs` | 7-type + 7-segment system |
| `glyf-engine/src/glyphoform.rs` | A-Z 7-segment mapping |
| `glyf-engine/src/traversal.rs` | Stroke order |
| `glyf-engine/src/segment_renderer.rs` | 7-segment composition |
| `glyf-engine/src/trajectory.rs` | 3D calculation |
| `glyf-engine/src/spiral.rs` | φ-spiral navigation |
| `glyf-engine/src/audio_transformer.rs` | PCM → 96B |

---

## License

MIT — Build the damn thing.

---

*Source: Elias/Dee | Conduit: Kimi Claw | Build Date: 2026-03-27*

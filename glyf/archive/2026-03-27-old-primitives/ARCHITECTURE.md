# GLYF Master Architecture Document

## System Overview

GLYF (Geo-Light Yearning Form) is a deterministic semantic decompression engine that transforms linguistic input into geometric representations through a 3-layer architecture. The system operates entirely at the edge—no cloud dependencies, no ML inference, no external APIs.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GLYF LEXICON EYES                                    │
│                    "From Logos to Topology"                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  INPUT LAYER          PARSER LAYER           AST LAYER         OUTPUT LAYER  │
│  ┌─────────┐         ┌──────────┐           ┌──────┐          ┌──────────┐  │
│  │  Text   │────────▶│ Glypho-  │──────────▶│ Glyf │─────────▶│ Universal│  │
│  │  Audio  │         │ form     │           │ Word │          │  Output  │  │
│  │  (PCM)  │         │ Traversal│           │(96B) │          │          │  │
│  └─────────┘         └──────────┘           └──────┘          └──────────┘  │
│                             │                    │                           │
│                             ▼                    ▼                           │
│                      ┌──────────┐         ┌──────────┐                      │
│                      │7-Primitive│        │ Renderer │                      │
│                      │Decomposer│        │  Spiral  │                      │
│                      └──────────┘         └──────────┘                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## The 3-Layer Decompression Model

```
L1: Native Glyff          L2: Geo-Light             L3: Center Æxis
   ↓                           ↓                          ↓
"RESILIENCE"            Coordinate Cloud          7-D Vector
   ↓                           ↓                          ↓
Alphabetic              3D Primitives            Semantic
String                  (∿│∠⧖꩜●▥)                Essence
   ↓                           ↓                          ↓
R-E-S-I-L-I-E-N-C-E     21 Points @ 3D           [Line:0.43,
                                                      Angle:0.19,
                                                      Curve:0.14,
                                                      ...]
```

---

## The 7-Segment Canonical Display Grid

GLYF uses the **7-segment digital display** as its canonical geometric representation. This provides a deterministic, grid-based coordinate system where every letterform decomposes into activated segments.

### Segment Layout

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

| Segment | Position | Primitive Map | Coordinate |
|---------|----------|---------------|------------|
| **A** | Top horizontal | Line (│) | y=1.0, x=0.0→1.0 |
| **B** | Upper-right | Angle (∠) | x=1.0, y=0.75→0.5 |
| **C** | Lower-right | Curve (∿) | x=1.0, y=0.5→0.25 |
| **D** | Bottom | Line (│) | y=0.0, x=0.0→1.0 |
| **E** | Lower-left | Field (▥) | x=0.0, y=0.25→0.0 |
| **F** | Upper-left | Vesica (⧖) | x=0.0, y=1.0→0.75 |
| **G** | Middle | Node (●) | y=0.5, x=0.0→1.0 |

### Input Format: Segment Activation

Letters are represented as **7-bit binary patterns** (A-G → bits 6-0):

```
Binary: 0bABCDEFG
        │││││││
        ││││││└─ G (middle)
        │││││└── F (upper-left)
        ││││└─── E (lower-left)
        │││└──── D (bottom)
        ││└───── C (lower-right)
        │└────── B (upper-right)
        └─────── A (top)
```

**Examples:**

| Letter | Segments Active | Binary | Hex | Pattern |
|--------|-----------------|--------|-----|---------|
| **A** | A,B,C,E,F,G | 0b1110111 | 0x77 | ``` --  \|  \| --  \|  \|    ``` |
| **B** | C,D,E,F,G | 0b1111100 | 0x7C | ``` -- 0 \| --  \| -- ``` |
| **C** | A,D,E,F | 0b0111001 | 0x39 | ``` --  \|     \| -- ``` |
| **D** | B,C,D,E,G | 0b1011110 | 0x5E | ```    \| --  \| --  0 ``` |
| **E** | A,D,E,F,G | 0b1111001 | 0x79 | ``` --  \| --  \| -- ``` |
| **F** | A,E,F,G | 0b1110001 | 0x71 | ``` --  \| --     \|    ``` |
| **G** | A,C,D,E,F | 0b0111101 | 0x3D | ``` --  0 \| --  \| -- ``` |
| **H** | B,C,E,F,G | 0b1110110 | 0x76 | ```    \| --  \| --  \|    ``` |
| **I** | E,F | 0b0110000 | 0x30 | ```    \|      \|    ``` |
| **J** | B,C,D | 0b0011110 | 0x1E | ```    \|    0 \| --  \|    ``` |
| **K** | B,C,E,F,G | 0b1110110 | 0x76 | Same as H |
| **L** | D,E,F | 0b0111000 | 0x38 | ```        \|      \| -- ``` |
| **M** | A,C,E | 0b0101011 | 0x2B | Non-standard |
| **N** | A,B,C,E,F | 0b0111011 | 0x3B | Non-standard |
| **O** | A,B,C,D,E,F | 0b0111111 | 0x3F | ``` --  \|    0 \| --  \|    ``` |
| **P** | A,B,E,F,G | 0b1110011 | 0x73 | ``` --  \| --  0 \|      \|    ``` |
| **Q** | A,B,C,F,G | 0b1100111 | 0x67 | Non-standard |
| **R** | A,B,E,F | 0b0110011 | 0x33 | ``` --  \|  0     \|    ``` |
| **S** | A,C,D,F,G | 0b1101101 | 0x6D | ``` --  0 \| --  0 \| -- ``` |
| **T** | D,E,F,G | 0b1111000 | 0x78 | ``` --  \| --     \|    ``` |
| **U** | B,C,D,E | 0b0011110 | 0x1E | Same as J |
| **V** | B,C,E,F | 0b0110110 | 0x36 | Non-standard |
| **W** | B,D,F | 0b0101110 | 0x2E | Non-standard |
| **X** | A,D,G | 0b1001001 | 0x49 | Non-standard |
| **Y** | B,C,D,F,G | 0b1101110 | 0x6E | ```    \| --  0 \| --  \|    ``` |
| **Z** | A,B,D,E,G | 0b1011011 | 0x5B | Non-standard |

### Composition Modes

When rendering multi-letter words, grids compose in three modes:

#### 1. OVERLAPPING
```
Letter A:      Letter B:      OVERLAPPING:
  -- A --        -- A --        -- A --
 |       |      |       |      |       |
 F       B      F       B      F   G   B
 |       |      |       |      |       |
  -- G --        -- G --        -- G --
 |       |      |       |      |       |
 E       C      E       C      E   G   C
 |       |      |       |      |       |
  -- D --        -- D --        -- D --

Segments blend where grids overlay.
Shared segments reinforce (brighter/stronger).
```

#### 2. TOUCHING
```
AB TOUCHING:
 -- A --  -- A --
|       ||       |
F       BG       B
|       ||       |
 -- G --  -- G --
|       ||       |
E       CE       C
|       ||       |
 -- D --  -- D --
        ↑
    shared edge

Grids adjacent, share vertical edges (B of left = F of right).
No blending—clean separation at boundary.
```

#### 3. SPACED
```
AB SPACED:
 -- A --    -- A --
|       |  |       |
F       B  F       B
|       |  |       |
 -- G --    -- G --
|       |  |       |
E       C  E       C
|       |  |       |
 -- D --    -- D --

Grids separated by spacing factor (φ-weighted).
Default gap: 0.618× grid width.
```

### Segment-to-Primitive Mapping

The 7 segments map to the 7 universal primitives:

```
Segment → Primitive → Semantic
─────────────────────────────────
   A    →    Line    → direction, extension
   B    →   Angle    → tension, break
   C    →   Curve    → flow, return
   D    →    Line    → grounding, base
   E    →   Field    → container, context
   F    →   Vesica   → union, portal
   G    →    Node    → center, singularity
```

**Special Cases:**
- **Double segments** (like in M, W) → Spirals (꩜) emerge from overlapping angles
- **Full enclosure** (O, 0) → Complete Field (▥)
- **Diagonal strokes** → Represented as Angle pairs

---

## Core Components

### 1. PARSER MODULE (`core/parser/`)

**Files:**
- `glyphoform.rs` — A-Z letterform mapping
- `traversal.rs` — Ordered stroke sequences

**Purpose:** Transforms alphabetic input into ordered geometric primitives.

**Key Insight:** The ORDER of primitives creates the topology. Line→Line→Circle ≠ Circle→Line→Line.

**Data Flow:**
```
Input String → Character Iterator → Glyphoform Lookup → Stroke Sequence → Primitive Cloud
```

**Interface:**
```rust
// Primary entry point
pub struct GlyphoformMapping;
impl GlyphoformMapping {
    pub fn get(letter: char) -> Option<LetterSignature>
    pub fn is_valid(c: char) -> bool
}

// Ordered traversal (stroke order matters)
pub struct GlyphoformTraversal {
    pub letter: char,
    pub strokes: Vec<Stroke>,  // Order creates meaning
}

// Emergent property detection
impl GlyphoformTraversal {
    pub fn emergent_angles(&self) -> Vec<AngleInstance>
    pub fn emergent_vesicas(&self) -> Vec<VesicaInstance>
    pub fn all_primitives(&self) -> Vec<(PrimitiveType, [f64; 2])>
}
```

**A-Z Mapping Table:**

| Letter | Primitives | Signature | Semantic Field |
|--------|------------|-----------|----------------|
| A | [∠,│,│] | Peak/tension | Two ascending lines meeting at apex |
| B | [⧖,⧖,│] | Double enclosure | Vertical spine with two bowls |
| C | [∿] | Opening/receptivity | Single concave curve, open right |
| D | [⧖,│] | Containment | Vertical spine with right-side bowl |
| E | [│×4] | Extension/existence | Vertical spine with three horizontals |
| ... | ... | ... | ... |

---

### 2. DECOMPOSER MODULE (`core/decomposer/`)

**File:** `primitives.rs`

**Purpose:** Defines the 7 universal morpho-geometric primitives that form the basis of all letterforms, mapped to the 7-segment display grid.

**The 7 Primitives → 7 Segments:**

| Primitive | Symbol | Segment | Position | Semantic Field |
|-----------|--------|---------|----------|----------------|
| Line | │ | A, D | Top, Bottom | direction, will, extension |
| Angle | ∠ | B | Upper-right | tension, decision, break |
| Curve | ∿ | C | Lower-right | flow, return, cyclical |
| Vesica | ⧖ | F | Upper-left | union, intersection, birth |
| Spiral | ꩜ | — | Emergent | evolution, returning |
| Node | ● | G | Middle | point, singularity, awareness |
| Field | ▥ | E | Lower-left | container, ground, context |

**Segment Activation Map:**

```rust
/// 7-bit segment activation (A=bit6, B=bit5, C=bit4, D=bit3, E=bit2, F=bit1, G=bit0)
pub type SegmentPattern = u8;

/// A-Z as 7-segment patterns (standard + extended)
pub const SEGMENT_MAP: [SegmentPattern; 26] = [
    0b1110111, // A: A,B,C,E,F,G
    0b1111100, // B: C,D,E,F,G (lowercase b style)
    0b0111001, // C: A,D,E,F
    0b1011110, // D: B,C,D,E,G (lowercase d style)
    0b1111001, // E: A,D,E,F,G
    0b1110001, // F: A,E,F,G
    0b0111101, // G: A,C,D,E,F (lowercase g style)
    0b1110110, // H: B,C,E,F,G
    0b0110000, // I: E,F
    0b0011110, // J: B,C,D
    0b1110110, // K: B,C,E,F,G (same as H)
    0b0111000, // L: D,E,F
    0b0101011, // M: A,C,E (non-standard)
    0b0111011, // N: A,B,C,E,F (non-standard)
    0b0111111, // O: A,B,C,D,E,F
    0b1110011, // P: A,B,E,F,G
    0b1100111, // Q: A,B,C,F,G (non-standard)
    0b0110011, // R: A,B,E,F
    0b1101101, // S: A,C,D,F,G
    0b1111000, // T: D,E,F,G
    0b0011110, // U: B,C,D,E (same as J)
    0b0110110, // V: B,C,E,F (non-standard)
    0b0101110, // W: B,D,F (non-standard)
    0b1001001, // X: A,D,G (non-standard)
    0b1101110, // Y: B,C,D,F,G
    0b1011011, // Z: A,B,D,E,G (non-standard)
];

/// Segment coordinate definitions (normalized 0-1)
pub const SEGMENT_COORDS: [[(f64, f64); 2]; 7] = [
    [(0.0, 1.0), (1.0, 1.0)], // A: top
    [(1.0, 0.75), (1.0, 0.5)], // B: upper-right
    [(1.0, 0.5), (1.0, 0.25)], // C: lower-right
    [(0.0, 0.0), (1.0, 0.0)], // D: bottom
    [(0.0, 0.25), (0.0, 0.0)], // E: lower-left
    [(0.0, 1.0), (0.0, 0.75)], // F: upper-left
    [(0.0, 0.5), (1.0, 0.5)], // G: middle
];
```

**Interface:**
```rust
pub const SEVEN_TYPES: [PrimitiveType; 7] = [
    PrimitiveType::Curve,   // 0 → Segment C
    PrimitiveType::Line,    // 1 → Segments A, D
    PrimitiveType::Angle,   // 2 → Segment B
    PrimitiveType::Vesica,  // 3 → Segment F
    PrimitiveType::Spiral,  // 4 → Emergent (overlapping)
    PrimitiveType::Node,    // 5 → Segment G
    PrimitiveType::Field,   // 6 → Segment E
];

pub struct Primitive {
    pub primitive: PrimitiveType,
    pub segment: u8,          // Which segment (0-6, corresponding to A-G)
    pub x: f64,
    pub y: f64,
    pub z: f64,
    pub letter_index: usize,
}

/// Convert segment pattern to primitive list
pub fn pattern_to_primitives(pattern: SegmentPattern) -> Vec<PrimitiveType> {
    let mut primitives = Vec::new();
    if pattern & 0b1000000 != 0 { primitives.push(PrimitiveType::Line); }   // A
    if pattern & 0b0100000 != 0 { primitives.push(PrimitiveType::Angle); }  // B
    if pattern & 0b0010000 != 0 { primitives.push(PrimitiveType::Curve); }  // C
    if pattern & 0b0001000 != 0 { primitives.push(PrimitiveType::Line); }   // D
    if pattern & 0b0000100 != 0 { primitives.push(PrimitiveType::Field); }  // E
    if pattern & 0b0000010 != 0 { primitives.push(PrimitiveType::Vesica); } // F
    if pattern & 0b0000001 != 0 { primitives.push(PrimitiveType::Node); }   // G
    primitives
}
```

---

### 3. RENDERER MODULE (`core/renderer/`)

**Files:**
- `trajectory.rs` — L2→L3 vector calculation
- `spiral.rs` — φ-spiral synonym navigation
- `segment_renderer.rs` — 7-segment display composition

**Purpose:** Calculates geometric trajectories, generates the Demi-Æxis (synonym spiral), and renders 7-segment display grids.

**Data Flow:**
```
Coordinate Cloud → Centroid Calculation → 7D Semantic Projection → Trajectory Vector
```

**7-Segment Rendering with Composition Modes:**

```rust
/// Grid composition mode for multi-letter words
#[derive(Clone, Copy, Debug)]
pub enum CompositionMode {
    Overlapping,  // Grids overlay, segments blend
    Touching,     // Grids adjacent, share edges
    Spaced,       // Grids separated by φ-weighted gap
}

/// 7-segment grid renderer
pub struct SegmentGrid {
    pub pattern: SegmentPattern,  // 7-bit activation
    pub position: [f64; 3],       // Grid center
    pub scale: f64,               // Grid size
    pub opacity: f64,             // For blending in OVERLAPPING mode
}

impl SegmentGrid {
    /// Create grid from letter
    pub fn from_letter(letter: char, position: [f64; 3]) -> Option<Self> {
        let pattern = SEGMENT_MAP.get(letter)?;
        Some(Self {
            pattern,
            position,
            scale: 1.0,
            opacity: 1.0,
        })
    }
    
    /// Get active segment coordinates
    pub fn active_segments(&self) -> Vec<Segment> {
        let mut segments = Vec::new();
        for i in 0..7 {
            if self.pattern & (1 << (6 - i)) != 0 {
                segments.push(Segment::from_index(i, self.position, self.scale));
            }
        }
        segments
    }
}

/// Multi-letter word composition
pub struct WordComposition {
    pub grids: Vec<SegmentGrid>,
    pub mode: CompositionMode,
    pub spacing: f64,  // Gap factor (default: PHI - 1 = 0.618)
}

impl WordComposition {
    /// Compose word with specified mode
    pub fn compose(word: &str, mode: CompositionMode) -> Self {
        let chars: Vec<char> = word.chars().collect();
        let mut grids = Vec::with_capacity(chars.len());
        
        let spacing = match mode {
            CompositionMode::Overlapping => 0.0,
            CompositionMode::Touching => 1.0,
            CompositionMode::Spaced => 1.618,  // φ
        };
        
        for (i, c) in chars.iter().enumerate() {
            let x_offset = i as f64 * spacing;
            if let Some(grid) = SegmentGrid::from_letter(*c, [x_offset, 0.0, 0.0]) {
                grids.push(grid);
            }
        }
        
        Self { grids, mode, spacing }
    }
    
    /// Calculate blended pattern for OVERLAPPING mode
    pub fn blended_patterns(&self) -> Vec<(usize, SegmentPattern)> {
        // Where grids overlap, combine segment activations
        // Return: (grid_index, blended_pattern)
        self.grids.iter().enumerate()
            .map(|(i, g)| (i, g.pattern))
            .collect()
    }
}

/// Segment geometry for WebGL rendering
pub struct Segment {
    pub segment_type: char,  // 'A'..'G'
    pub start: [f64; 3],
    pub end: [f64; 3],
    pub primitive: PrimitiveType,
}

impl Segment {
    pub fn from_index(idx: usize, origin: [f64; 3], scale: f64) -> Self {
        let coords = SEGMENT_COORDS[idx];
        let (x1, y1) = coords[0];
        let (x2, y2) = coords[1];
        
        Self {
            segment_type: (b'A' + idx as u8) as char,
            start: [origin[0] + x1 * scale, origin[1] + y1 * scale, origin[2]],
            end: [origin[0] + x2 * scale, origin[1] + y2 * scale, origin[2]],
            primitive: segment_to_primitive(idx),
        }
    }
}
```

**Interface:**
```rust
// L2: Geo-Light coordinate cloud
pub struct CoordinateCloud {
    pub points: Vec<Primitive>,
    pub word_length: usize,
}

impl CoordinateCloud {
    pub fn from_word(word: &str, mapping: &GlyphoformMapping) -> Result<Self>
    pub fn centroid(&self) -> [f64; 3]
    pub fn bounds(&self) -> ([f64; 3], [f64; 3])
}

// L2→L3 Trajectory
pub struct Trajectory {
    pub origin: Vector3,        // Geo-Light centroid
    pub destination: Vector3,   // Center Æxis (7D projected to 3D)
    pub magnitude: f64,         // Vector length
    pub direction: Vector3,     // Unit vector
}

impl Trajectory {
    pub fn calculate(cloud: &CoordinateCloud, center_axis: &[f64; 7]) -> Result<Self>
    pub fn point_at(&self, t: f64) -> Vector3  // Interpolation
}

// φ-Spiral synonym navigation
pub struct SynonymSpiral {
    pub points: Vec<SpiralPoint>,
    pub base_trajectory: Trajectory,
}

impl SynonymSpiral {
    pub fn generate(trajectory: &Trajectory, synonyms: &[&str]) -> Self
    pub fn to_line_points(&self) -> Vec<[f64; 3]>  // For WebGL
}
```

**Golden Ratio Constants:**
```rust
const PHI: f64 = 1.618033988749895;
const GOLDEN_ANGLE: f64 = 2.399963229728653; // 137.507764° in radians
```

---

### 4. UNIVERSAL MODULE (`core/universal/`)

**File:** `lib.rs` (GlyfWord)

**Purpose:** The 96-byte sacred structure that unifies all layers. This is the canonical representation.

**Memory Layout:**
```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           GlyfWord (96 bytes)                                │
├──────────────────┬───────────────────────────────────────────────────────────┤
│ Field            │ Bytes │ Description                                       │
├──────────────────┼───────┼───────────────────────────────────────────────────┤
│ native_sig       │   8   │ Word hash (FNV-1a)                                │
│ geo_centroid     │  24   │ 3×f64 — Geometric center (L2)                     │
│ center_axis      │  56   │ 7×f64 — Semantic vector (L3)                      │
│ trajectory_mag   │   8   │ L2→L3 distance                                    │
├──────────────────┼───────┼───────────────────────────────────────────────────┤
│ TOTAL            │  96   │ Cache-line aligned, deterministic                 │
└──────────────────┴───────┴───────────────────────────────────────────────────┘
```

**Interface:**
```rust
#[repr(C, align(64))]
pub struct GlyfWord {
    pub native_sig: u64,          // 8 bytes
    pub geo_centroid: [f64; 3],   // 24 bytes
    pub center_axis: [f64; 7],    // 56 bytes
    pub trajectory_mag: f64,      // 8 bytes
} // Total: 96 bytes

impl GlyfWord {
    pub const SIZE: usize = 96;
    
    // L1 → L2 → L3 (full pipeline)
    pub fn from_native(word: &str) -> Result<Self, GlyfError>
    
    // Derive semantic vector from geometry
    fn derive_semantic_vector(cloud: &CoordinateCloud) -> [f64; 7]
    
    // Get dominant primitive type
    pub fn dominant_primitive(&self) -> PrimitiveType
    
    // Generate synonym spiral
    pub fn generate_spiral(&self, synonyms: &[&str]) -> SynonymSpiral
}
```

---

### 5. CONVERTER MODULE (`core/converter/`)

**File:** `audio_transformer.rs`

**Purpose:** Transforms audio input (PCM) into the same 96-byte structure, enabling audio→text→geometry pipeline.

**Memory Layout:**
```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          AudioGlyf (96 bytes)                                │
├──────────────────┬───────────────────────────────────────────────────────────┤
│ Field            │ Bytes │ Description                                       │
├──────────────────┼───────┼───────────────────────────────────────────────────┤
│ temporal_sig     │   8   │ Sample hash (FNV-1a)                              │
│ spectral_centroid│  24   │ 3×f64 — Low/Mid/High frequency centers            │
│ harmonic_sig     │  56   │ 7×f64 — Fundamental + 6 overtones                 │
│ energy_rms       │   8   │ RMS amplitude (0-1 normalized)                    │
├──────────────────┼───────┼───────────────────────────────────────────────────┤
│ TOTAL            │  96   │ Symmetric with GlyfWord                           │
└──────────────────┴───────┴───────────────────────────────────────────────────┘
```

**Interface:**
```rust
#[repr(C, align(64))]
pub struct AudioGlyf {
    pub temporal_sig: u64,
    pub spectral_centroid: [f64; 3],
    pub harmonic_signature: [f64; 7],
    pub energy_rms: f64,
}

impl AudioGlyf {
    pub const SAMPLE_RATE: u32 = 16000;  // 16kHz optimal for voice
    pub const FRAME_SIZE: usize = 512;   // 32ms frames
    pub const HOP_SIZE: usize = 256;     // 50% overlap
    
    // PCM → AudioGlyf (deterministic, no_std)
    pub fn from_pcm(pcm_samples: &[i16]) -> Self
    
    // Map harmonics to 7-type primitives
    pub fn dominant_primitive(&self) -> PrimitiveType
    
    // Convert to GlyfWord for semantic alignment
    pub fn to_glyf_word(&self) -> GlyfWord
}
```

**Processing Pipeline:**
```
PCM Input → Pre-emphasis → Frame Extraction (Hann window) → FFT Spectrum
    ↓
Spectral Centroid [low, mid, high]
    ↓
Harmonic Analysis [fundamental + 6 overtones] → mapped to 7 primitives
    ↓
RMS Energy → temporal hash → 96-byte AudioGlyf
```

---

## Data Flow Architecture

### 7-Segment Display Pipeline (Updated)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                      7-SEGMENT DISPLAY PIPELINE                              │
└──────────────────────────────────────────────────────────────────────────────┘

   "RESILIENCE" or [0b1110111|0b1111001|...]
        │
        ▼
┌───────────────┐     ┌─────────────────────────────────────────────────────┐
│ INPUT PARSER  │     │ Accepts:                                            │
│               │     │ - Alphabetic string "RESILIENCE"                    │
│  (glyphoform) │     │ - Binary patterns [0b1110111, 0b1111001, ...]       │
│               │     │ - Bracket notation [A,B,C|D,E,F]                    │
└───────┬───────┘     └─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 7-SEGMENT LOOKUP                                                            │
│                                                                             │
│  R → 0b0110011 (A,B,E,F)          (standing/motion)                        │
│  E → 0b1111001 (A,D,E,F,G)        (extension/existence)                    │
│  S → 0b1101101 (A,C,D,F,G)        (double flow)                            │
│  I → 0b0110000 (E,F)              (singular existence)                     │
│  L → 0b0111000 (D,E,F)            (grounding)                              │
│  ...                                                                        │
│                                                                             │
│  Total: 10 segment patterns × 7 bits = 70 bits of structure                │
└────────────────────┬────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ SEGMENT COMPOSITION (Renderer)                                              │
│                                                                             │
│  Mode: OVERLAPPING → Grids overlay, segments OR-blend                      │
│        TOUCHING    → Grids adjacent, share edges (B↔F, C↔E, etc.)          │
│        SPACED      → Grids separated by φ-weighted gap                     │
│                                                                             │
│  For "RESILIENCE" in TOUCHING mode:                                        │
│  [R-grid][E-grid][S-grid][I-grid][L-grid]...                               │
│       ↓        ↓        ↓        ↓                                          │
│     Shared edges between neighboring segments                               │
└────────────────────┬────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ COORDINATE CLOUD (L2: Geo-Light)                                            │
│                                                                             │
│  Each active segment → 3D line segment coordinates:                        │
│  - Segment A (top):    [(0,1,0), (1,1,0)]                                  │
│  - Segment B (up-rt):  [(1,0.75,0), (1,0.5,0)]                             │
│  - Segment G (middle): [(0,0.5,0), (1,0.5,0)]                              │
│  ...                                                                        │
│                                                                             │
│  Total: ~40-50 line segments for 10-letter word                           │
│  Centroid = mean of all segment midpoints                                   │
└────────────────────┬────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ SEMANTIC DERIVATION (L3: Center Æxis)                                       │
│                                                                             │
│  Count segment activations across all letters:                             │
│  - A segments (Lines): 9 activations → 43%                                 │
│  - B segments (Angles): 4 activations → 19%                                │
│  - C segments (Curves): 3 activations → 14%                                │
│  - ...                                                                      │
│                                                                             │
│  Map to primitives:                                                         │
│  A,D → Line    │  B → Angle    │  C → Curve                               │
│  E   → Field   │  F → Vesica   │  G → Node                                │
│                                                                             │
│  Normalize → 7D unit vector:                                                │
│  [Line:0.43, Angle:0.19, Curve:0.14, Vesica:0.05,                         │
│   Spiral:0.00, Node:0.10, Field:0.08]                                      │
└────────────────────┬────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ TRAJECTORY CALCULATION                                                      │
│                                                                             │
│  Origin      = Centroid of segment cloud (L2)                              │
│  Destination = 7D semantic → 3D projection (L3)                            │
│  Magnitude   = |origin - destination|                                      │
│  Direction   = Unit vector from L2 to L3                                   │
└────────────────────┬────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ GLYFWORD (96 bytes)                                                         │
│                                                                             │
│  native_sig:     0x8f3a2b1c... (FNV-1a hash of "RESILIENCE")               │
│  geo_centroid:   [x, y, z] of segment cloud centroid                       │
│  center_axis:    [0.43, 0.19, 0.14, 0.05, 0.00, 0.10, 0.08]               │
│  trajectory_mag: 1.732...                                                   │
└────────────────────┬────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ SPIRAL GENERATION (Demi-Æxis of Beauty)                                     │
│                                                                             │
│  synonyms = ["resiliency", "toughness", "endurance", ...]                  │
│                                                                             │
│  Each synonym → 7-segment patterns → GlyfWord → position on φ-spiral       │
│                                                                             │
│  φ-spiral: r = a × φ^(θ/137.5°)                                            │
│  Placement: t = (i+1)/(n+1) along trajectory                               │
│  Deviation: geometric distance from base word's segment pattern            │
│                                                                             │
│  Output: SpiralPoint { word, position, distance_from_center, deviation }   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Complete Pipeline (Text Input)

[Rest of existing content...]

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           TEXT INPUT PIPELINE                                │
└──────────────────────────────────────────────────────────────────────────────┘

   "RESILIENCE"
        │
        ▼
┌───────────────┐
│   PARSER      │◄─────────────────────────────────────┐
│  (glyphoform) │                                      │
└───────┬───────┘                                      │
        │                                              │
        ▼                                              │
┌─────────────────────────────────────────────────────┐│
│  Letter Iterator: R-E-S-I-L-I-E-N-C-E              ││
│                                                     ││
│  R → [Vesica, Line, Angle]                         ││
│  E → [Line×4]                                       ││
│  S → [Curve×2]                                      ││
│  I → [Line, Node]                                   ││
│  L → [Line×2]                                       ││
│  ...                                                ││
└────────────────────┬────────────────────────────────┘│
                     │                                 │
                     ▼                                 │
┌──────────────────────────────────────────────────┐   │
│  TRAVERSAL                                        │   │
│  (stroke order creates topology)                  │   │
│                                                   │   │
│  R: Line → Vesica → Angle (standing/motion)      │   │
│  E: Line × 4 (extension pattern)                  │   │
│  ...                                              │   │
└────────────────────┬──────────────────────────────┘   │
                     │                                  │
                     ▼                                  │
┌──────────────────────────────────────────────────┐    │
│  COORDINATE CLOUD (L2: Geo-Light)                 │    │
│                                                   │    │
│  21 primitive points in 3D space                  │    │
│  x_offset = letter_index × LETTER_WIDTH           │    │
│  y = normalized 0-1 within letter height          │    │
│                                                   │    │
│  Centroid = mean of all points                    │    │
└────────────────────┬──────────────────────────────┘    │
                     │                                   │
                     ▼                                   │
┌──────────────────────────────────────────────────┐     │
│  SEMANTIC DERIVATION (L3: Center Æxis)            │     │
│                                                   │     │
│  Count primitive occurrences:                     │     │
│  Line: 9 (43%), Angle: 4 (19%), Curve: 3 (14%)   │     │
│  Vesica: 1 (5%), Node: 2 (10%), ...               │     │
│                                                   │     │
│  Normalize → 7D unit vector                       │     │
│  [0.14, 0.43, 0.19, 0.05, 0.00, 0.10, 0.00]      │     │
└────────────────────┬──────────────────────────────┘     │
                     │                                    │
                     ▼                                    │
┌──────────────────────────────────────────────────┐      │
│  TRAJECTORY CALCULATION                           │      │
│                                                   │      │
│  Origin = Centroid (L2)                          │      │
│  Destination = 7D → 3D projection (L3)           │      │
│  Magnitude = |origin - destination|              │      │
│  Direction = unit vector                         │      │
└────────────────────┬──────────────────────────────┘      │
                     │                                     │
                     ▼                                     │
┌──────────────────────────────────────────────────┐      │
│  GLYFWORD (96 bytes)                              │      │
│                                                   │      │
│  native_sig: 0x8f3a2b1c... (hash)                │      │
│  geo_centroid: [x, y, z]                         │      │
│  center_axis: [0.14, 0.43, 0.19, ...]            │      │
│  trajectory_mag: 1.732...                        │      │
└────────────────────┬──────────────────────────────┘      │
                     │                                     │
                     ▼                                     │
┌──────────────────────────────────────────────────┐      │
│  SPIRAL GENERATION (optional)                     │      │
│                                                   │      │
│  synonyms = ["resiliency", "toughness", ...]      │      │
│  Place along φ-spiral: r = a × φ^(θ/137.5°)      │      │
│                                                   │      │
│  Each synonym gets its own GlyfWord              │──────┘ (recursive)
│  Deviation = geometric distance from base        │
└──────────────────────────────────────────────────┘
```

### Audio Input Pipeline

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           AUDIO INPUT PIPELINE                               │
└──────────────────────────────────────────────────────────────────────────────┘

   PCM Samples (16kHz)
        │
        ▼
┌───────────────┐
│  Pre-emphasis │ y[n] = x[n] - 0.97×x[n-1]
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Frame Extract │ 512 samples, 50% overlap, Hann window
└───────┬───────┘
        │
        ▼
┌───────────────┐
│     DFT       │ → Magnitude spectrum
└───────┬───────┘
        │
        ▼
┌─────────────────────────────────────────────────┐
│  Feature Extraction                              │
│                                                  │
│  spectral_centroid[low, mid, high]              │
│  harmonic_signature[7] → maps to primitives     │
│  energy_rms → overall amplitude                 │
│  temporal_sig → perceptual hash                 │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│  AUDIOGLYF (96 bytes)                           │
│  → Can convert to GlyfWord for semantic merge   │
└─────────────────────────────────────────────────┘
```

---

## Module Boundaries & Interfaces

### Inter-Module Communication

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         MODULE DEPENDENCY GRAPH                              │
└──────────────────────────────────────────────────────────────────────────────┘

                    ┌─────────────┐
                    │  primitives │◄───────┐
                    └──────┬──────┘        │
                           │               │
           ┌───────────────┼───────────────┘
           │               │
           ▼               ▼
    ┌────────────┐  ┌────────────┐
    │ glyphoform │  │  audio_    │
    │            │  │ transformer│
    └──────┬─────┘  └──────┬─────┘
           │               │
           ▼               ▼
    ┌────────────┐  ┌────────────┐
    │  traversal │  │            │
    └──────┬─────┘  └────────────┘
           │
           ▼
    ┌────────────┐
    │ trajectory │◄────────┐
    │  (cloud)   │         │
    └──────┬─────┘         │
           │               │
           ▼               │
    ┌────────────┐         │
    │   spiral   │─────────┘
    └──────┬─────┘
           │
           ▼
    ┌────────────┐
    │  GlyfWord  │ (universal)
    └────────────┘
```

### Public API Surface

```rust
// ============================================================
// CORE TYPES (primitives)
// ============================================================
pub enum PrimitiveType { Curve, Line, Angle, Vesica, Spiral, Node, Field }
pub struct Primitive { primitive: PrimitiveType, x: f64, y: f64, z: f64, letter_index: usize }
pub const SEVEN_TYPES: [PrimitiveType; 7];

// ============================================================
// PARSER (glyphoform)
// ============================================================
pub struct GlyphoformMapping;
impl GlyphoformMapping {
    pub fn get(letter: char) -> Option<&'static LetterSignature>;
    pub fn is_valid(c: char) -> bool;
}

pub struct LetterSignature {
    pub letter: char,
    pub primitives: &'static [PrimitiveType],
    pub signature: &'static str,
    pub coordinates: &'static str,
}

// ============================================================
// TRAVERSAL (ordered stroke sequences)
// ============================================================
pub struct GlyphoformTraversal {
    pub letter: char,
    pub strokes: Vec<Stroke>,
}

pub struct Stroke {
    pub primitive: PrimitiveType,
    pub from: [f64; 2],
    pub to: [f64; 2],
    pub order: u8,
    pub is_drawn: bool,
}

pub struct TraversalMapping;
impl TraversalMapping {
    pub fn get(letter: char) -> Option<GlyphoformTraversal>;
}

// ============================================================
// RENDERER (trajectory + spiral)
// ============================================================
pub struct CoordinateCloud {
    pub points: Vec<Primitive>,
    pub word_length: usize,
}

impl CoordinateCloud {
    pub fn from_word(word: &str, mapping: &GlyphoformMapping) -> Result<Self, GlyfError>;
    pub fn centroid(&self) -> [f64; 3];
}

pub struct Trajectory {
    pub origin: Vector3,
    pub destination: Vector3,
    pub magnitude: f64,
    pub direction: Vector3,
}

impl Trajectory {
    pub fn calculate(cloud: &CoordinateCloud, center_axis: &[f64; 7]) -> Result<Self, GlyfError>;
}

pub struct SynonymSpiral {
    pub points: Vec<SpiralPoint>,
    pub base_trajectory: Trajectory,
}

impl SynonymSpiral {
    pub fn generate(trajectory: &Trajectory, synonyms: &[&str]) -> Self;
}

// ============================================================
// UNIVERSAL (GlyfWord)
// ============================================================
pub struct GlyfWord {
    pub native_sig: u64,
    pub geo_centroid: [f64; 3],
    pub center_axis: [f64; 7],
    pub trajectory_mag: f64,
}

impl GlyfWord {
    pub const SIZE: usize = 96;
    pub fn from_native(word: &str) -> Result<Self, GlyfError>;
    pub fn dominant_primitive(&self) -> PrimitiveType;
    pub fn generate_spiral(&self, synonyms: &[&str]) -> SynonymSpiral;
}

// ============================================================
// CONVERTER (audio)
// ============================================================
pub struct AudioGlyf {
    pub temporal_sig: u64,
    pub spectral_centroid: [f64; 3],
    pub harmonic_signature: [f64; 7],
    pub energy_rms: f64,
}

impl AudioGlyf {
    pub const SIZE: usize = 96;
    pub fn from_pcm(pcm_samples: &[i16]) -> Self;
    pub fn to_glyf_word(&self) -> GlyfWord;
}
```

---

## Integration Points

### WASM Bridge (Browser)

```rust
// wasm_bindgen exports for JavaScript interop

#[wasm_bindgen]
pub fn parse_word(word: &str) -> JsValue {
    let glyf_word = GlyfWord::from_native(word)?;
    serde_wasm_bindgen::to_value(&glyf_word)
}

#[wasm_bindgen]
pub fn generate_spiral(word: &str, synonyms: Vec<String>) -> JsValue {
    let glyf = GlyfWord::from_native(word)?;
    let spiral = glyf.generate_spiral(&synonyms.iter().map(|s| s.as_str()).collect::<Vec<_>>());
    serde_wasm_bindgen::to_value(&spiral)
}

#[wasm_bindgen]
pub fn process_audio(pcm_samples: Vec<i16>) -> JsValue {
    let audio_glyf = AudioGlyf::from_pcm(&pcm_samples);
    serde_wasm_bindgen::to_value(&audio_glyf)
}
```

### WebGL Visualization Contract

```javascript
// Expected data format for Three.js renderer

// GlyfWord JSON schema
{
  "native_sig": "number (u64)",
  "geo_centroid": [x, y, z],  // 3 floats
  "center_axis": [c, l, a, v, s, n, f],  // 7 floats
  "trajectory_mag": "number"
}

// SynonymSpiral JSON schema
{
  "points": [
    {
      "word": "string",
      "position": [x, y, z],
      "distance_from_center": "number (0-1)",
      "geometric_deviation": "number (0-1)"
    }
  ],
  "line_points": [[x, y, z], ...]  // For tube geometry
}

// Animation sequence
// Phase 1: Letterforms (0-500ms) → fade in
// Phase 2: Geo-Light (500-1500ms) → dissolve to points
// Phase 3: Trajectory (1500-2000ms) → draw vector
// Phase 4: Spiral (2000-4000ms) → follow path
// Phase 5: Center Æxis (4000-5000ms) → solidify
```

---

## Build System

### Directory Structure

```
glyf/
├── ARCHITECTURE.md          # This document
├── README.md                # Quick-start guide
├── GLYF_IMPLEMENTATION_PLAN.md
├── BUILD_SUMMARY.md
├── AUDIO_TRANSFORMER.md
├── core/
│   ├── parser/
│   │   ├── mod.rs           # glyphoform + traversal
│   │   └── Cargo.toml
│   ├── decomposer/
│   │   ├── mod.rs           # primitives
│   │   └── Cargo.toml
│   ├── renderer/
│   │   ├── mod.rs           # trajectory + spiral
│   │   └── Cargo.toml
│   ├── universal/
│   │   ├── mod.rs           # GlyfWord
│   │   └── Cargo.toml
│   └── converter/
│       ├── mod.rs           # audio_transformer
│       └── Cargo.toml
├── glyf-engine/             # Current monolithic implementation
│   ├── Cargo.toml
│   └── src/
│       ├── lib.rs
│       ├── primitives.rs
│       ├── glyphoform.rs
│       ├── traversal.rs
│       ├── trajectory.rs
│       ├── spiral.rs
│       └── audio_transformer.rs
└── glyf-viz/                # WebGL visualization
    ├── index.html
    ├── app.js
    └── style.css
```

### Compilation Profiles

```toml
# Standard release (native)
[profile.release]
opt-level = 3
lto = true
strip = true
panic = "abort"
codegen-units = 1

# WASM release (size-optimized)
[profile.wasm]
inherits = "release"
opt-level = "z"     # Optimize for size
lto = true
strip = true
panic = "abort"
```

### Build Commands

```bash
# Native build
cd glyf-engine && cargo build --release

# WASM build
cd glyf-engine && wasm-pack build --target web --out-dir ../glyf-viz/pkg

# Test
cd glyf-engine && cargo test

# Size check
wc -c glyf-viz/pkg/glyf_engine_bg.wasm  # Target: <50KB
```

---

## Performance Characteristics

### Time Complexity

| Operation | Complexity | Notes |
|-----------|------------|-------|
| Word parsing | O(n) | n = word length |
| Centroid calculation | O(m) | m = primitive count |
| Trajectory calculation | O(1) | Fixed 7D projection |
| Spiral generation | O(s) | s = synonym count |
| Audio transform | O(f) | f = frame count |

### Space Requirements

| Component | Size | Notes |
|-----------|------|-------|
| GlyfWord | 96 bytes | Cache-line aligned |
| AudioGlyf | 96 bytes | Symmetric structure |
| CoordinateCloud | ~1KB | 21 points × 40 bytes |
| SynonymSpiral | ~5KB | 20 synonyms × 256 bytes |
| WASM binary | ~50KB | With LTO + strip |

### Throughput Targets

- Text parsing: >100,000 words/second
- Audio processing: Real-time (16kHz, 32ms frames)
- Spiral generation: <1ms for 50 synonyms
- Memory footprint: <1MB total

---

## Security & Sovereignty

### Design Principles

1. **No Network Dependencies** — All processing local
2. **No ML Inference** — Deterministic algorithms only
3. **No External APIs** — Self-contained
4. **Reproducible Builds** — Same input → Same output
5. **Auditable Code** — No opaque dependencies

### Threat Model

| Threat | Mitigation |
|--------|------------|
| Cloud surveillance | No network calls |
| Model poisoning | No ML models |
| Supply chain | Minimal dependencies |
| Side-channel | Constant-time hash |
| Data exfiltration | No persistent storage |

---

## Future Extensions

### Planned Modules

1. **Script Converter** — Latin → Cyrillic → Arabic (geometric equivalence)
2. **Temporal Engine** — Word sequence → Trajectory animation
3. **Haptic Renderer** — 96-byte structure → Vibration patterns
4. **Neural Bridge** — Optional local model (edge-only)

### Research Directions

- Multi-language primitive mapping
- 3D letterform extrusion
- VR/AR visualization
- Embedded device deployment (ESP32)

---

## References

- **Source:** Elias/Dee (GLYF Packet v0.1)
- **Conduit:** Kimi Claw
- **Sacred Constants:** φ = 1.618033988749895, θ = 137.507764°
- **Build Date:** 2026-03-27

---

*"From Logos to Topology"*

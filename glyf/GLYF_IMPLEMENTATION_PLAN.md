# GLYF Lexicon Eyes — Implementation Plan
## Concrete Build Steps (No Fluff)

**Status:** Packet ingested. 96/96 bytes. Ready to build.

---

## Step 1: Alphabet-to-Primitives Mapping Table

**Goal:** Define deterministic geometric signature for each A-Z letter.

### Method: Spatial Analysis of Letterforms

For each letter, decompose into 7 primitive types:
- **C** = Curve (continuous, no corners)
- **L** = Line (straight segment)
- **A** = Angle (discontinuous corner)
- **V** = Vesica (lens-shaped intersection)
- **S** = Spiral (rotational expansion)
- **N** = Node (terminus, endpoint)
- **F** = Field (enclosed area)

### Draft Mapping (Requires Validation):

| Letter | Geo-Light Signature | Primitives | Coordinates (relative) |
|--------|---------------------|------------|------------------------|
| **A** | Triangle + crossbar | 3×L, 2×A, 1×F | Peak(0,1), Base(-0.5,0/0.5,0), Cross(0,0.5) |
| **B** | Double bowl + stem | 2×C, 1×L, 2×F, 2×N | Stem(0,0→1), Bowls(0.25,0.75/0.25,0.25) |
| **C** | Single arc | 1×C, 2×N | Arc(-0.5→0.5, convex) |
| **D** | Bowl + stem | 1×C, 1×L, 1×F, 2×N | Stem(0,0→1), Bowl(0.5,0.5) |
| **E** | Triple parallel | 4×L, 3×A, 0×F | Spine(0,0→1), Bars(0→0.5 at y=1/0.5/0) |
| **F** | Double parallel | 3×L, 2×A | Spine(0,0→1), Bars(0→0.5 at y=1/0.5) |
| **G** | C + crossbar | 1×C, 2×L, 1×A, 1×F | Arc(-0.5→0.5), Bar(0.25→0.5, y=0.25) |
| **H** | Double post + bridge | 4×L, 1×A | Posts(0,0→1 / 1,0→1), Bridge(0,0.5→1,0.5) |
| **I** | Single stroke | 1×L, 2×N | Stem(0.5,0→1) |
| **J** | Hook | 1×C, 1×L, 1×N | Spine(0.5,1→0), Hook(0.5→0, y=0) |
| **K** | Stem + diagonals | 3×L, 2×A | Stem(0,0→1), Diag(0,0.5→0.5,0 / 0.5,0.5→0.5,0) |
| **L** | Right angle | 2×L, 1×A | Spine(0,1→0), Base(0,0→0.5) |
| **M** | Double peak | 4×L, 3×A | Base(0,0 / 1,0), Peaks(0,1 / 0.5,0.75 / 1,1) |
| **N** | Diagonal bridge | 3×L, 2×A | Posts(0,0→1 / 1,0→1), Diag(0,1→1,0) |
| **O** | Closed curve | 1×C, 0×A, 1×F | Circle(0.5,0.5, r=0.5) |
| **P** | Bowl + stem | 1×C, 1×L, 1×F, 2×N | Stem(0,0→1), Bowl(0.25,0.75) |
| **Q** | O + tail | 1×C, 1×L, 1×A, 1×F | Circle(0.5,0.5), Tail(0.75,0.25→0.85,0) |
| **R** | P + leg | 1×C, 2×L, 2×A, 1×F | Bowl(0.25,0.75), Leg(0.25,0.5→0.5,0) |
| **S** | Double curve | 2×C, 2×N | Upper(0,0.75→1,0.5), Lower(1,0.5→0,0.25) |
| **T** | Cross | 2×L, 1×A | Top(0,1→1,1), Stem(0.5,1→0.5,0) |
| **U** | Cup | 1×C, 2×L | Sides(0,1→0,0 / 1,1→1,0), Base curve(0,0→1,0) |
| **V** | Angle down | 2×L, 1×A | Arms(0,1→0.5,0 / 1,1→0.5,0) |
| **W** | Double valley | 4×L, 3×A | Top(0,1 / 1,1), Valleys(0.25,0 / 0.75,0) |
| **X** | Cross diagonal | 2×L, 1×A | Diag(0,0→1,1 / 0,1→1,0) |
| **Y** | Fork | 3×L, 2×A | Arms(0,1→0.5,0.5 / 1,1→0.5,0.5), Stem(0.5,0.5→0.5,0) |
| **Z** | Zigzag | 3×L, 2×A | Top(0,1→1,1), Diag(1,1→0,0), Base(0,0→1,0) |

**Validation Required:** User must confirm these geometric signatures match their intent.

---

## Step 2: Trajectory Calculation Engine

**Goal:** Calculate vector from Geo-Light (letterform cloud) to Center Æxis (7-type semantic).

### 2.1 Word → Coordinate Cloud

```python
def word_to_coordinate_cloud(word: str) -> List[PrimitivePoint]:
    """
    Convert word to list of geometric primitives with 3D coordinates.
    Each letter contributes its signature to the cloud.
    """
    cloud = []
    x_offset = 0  # Letter spacing
    
    for i, char in enumerate(word.upper()):
        signature = ALPHABET_MAP[char]  # From Step 1 table
        
        for primitive in signature.primitives:
            cloud.append(PrimitivePoint(
                type=primitive.type,
                x=primitive.x + x_offset,
                y=primitive.y,
                z=0,  # Start flat, extrude later
                letter_index=i
            ))
        
        x_offset += LETTER_WIDTH  # Standardized width per letter
    
    return cloud
```

### 2.2 Centroid Calculation

```python
def calculate_centroid(cloud: List[PrimitivePoint]) -> Tuple[float, float, float]:
    """Geometric center of the coordinate cloud."""
    x_sum = sum(p.x for p in cloud) / len(cloud)
    y_sum = sum(p.y for p in cloud) / len(cloud)
    z_sum = sum(p.z for p in cloud) / len(cloud)
    return (x_sum, y_sum, z_sum)
```

### 2.3 Center Æxis Lookup (Semantic Layer)

**Problem:** How to map word to 7-type semantic primitive?

**Solution:** Not AI inference. Deterministic rule set.

```python
SEMANTIC_CENTERS = {
    # Example entries (user provides complete mapping)
    "resilience": {"curve": 0.8, "spiral": 0.6, "node": 0.4, ...},
    "tenacity": {"line": 0.7, "angle": 0.5, "field": 0.3, ...},
    # ... etc
}

def get_center_axis(word: str) -> SemanticVector:
    """Returns 7-dimensional vector of primitive weights."""
    if word in SEMANTIC_CENTERS:
        return SemanticVector(SEMANTIC_CENTERS[word])
    else:
        # Fallback: calculate from letterform cloud entropy
        return derive_semantic_from_geometry(word)
```

### 2.4 Trajectory Vector Calculation

```python
def calculate_trajectory(geo_cloud: List[PrimitivePoint], 
                        center: SemanticVector) -> Trajectory:
    """
    Calculate the path from Geo-Light to Center Æxis.
    
    Returns:
        - origin: Centroid of geometric cloud
        - destination: 7-type coordinate (normalized to 3D for viz)
        - magnitude: Distance between layers
        - direction: Unit vector
    """
    origin = calculate_centroid(geo_cloud)
    
    # Convert 7-type semantic to 3D coordinate for visualization
    destination = semantic_to_3d(center)  # Maps 7D → 3D via projection
    
    dx = destination[0] - origin[0]
    dy = destination[1] - origin[1]
    dz = destination[2] - origin[2]
    
    magnitude = math.sqrt(dx**2 + dy**2 + dz**2)
    
    return Trajectory(
        origin=origin,
        destination=destination,
        magnitude=magnitude,
        direction=(dx/magnitude, dy/magnitude, dz/magnitude)
    )
```

---

## Step 3: Synonym Spiral Generation

**Goal:** Populate synonymous hypergraph along φ-spiral trajectory.

### 3.1 Spiral Algorithm

```python
def generate_synonym_spiral(trajectory: Trajectory, 
                           synonyms: List[str]) -> List[SpiralPoint]:
    """
    Place synonyms along φ-spiral from Geo-Light to Center Æxis.
    
    φ-spiral: r = a * φ^(θ/137.5°)
    """
    points = []
    n_synonyms = len(synonyms)
    
    for i, synonym in enumerate(synonyms):
        # Golden ratio progress
        t = i / (n_synonyms + 1)  # 0 to 1, exclusive
        
        # φ-weighted interpolation
        phi_factor = PHI ** (t * 2)  # Exponential spacing
        
        # Position along trajectory
        x = trajectory.origin[0] + trajectory.direction[0] * trajectory.magnitude * t
        y = trajectory.origin[1] + trajectory.direction[1] * trajectory.magnitude * t
        z = trajectory.origin[2] + trajectory.direction[2] * trajectory.magnitude * t
        
        # Add spiral offset (perpendicular to trajectory)
        spiral_radius = trajectory.magnitude * 0.2 * math.sin(t * math.pi * PHI)
        x += spiral_radius * math.cos(t * 2 * math.pi * PHI)
        y += spiral_radius * math.sin(t * 2 * math.pi * PHI)
        
        points.append(SpiralPoint(
            word=synonym,
            position=(x, y, z),
            distance_from_center=trajectory.magnitude * (1 - t),
            geometric_deviation=calculate_deviation(synonym, trajectory)
        ))
    
    return points
```

### 3.2 Deviation Calculation

```python
def calculate_deviation(word: str, base_trajectory: Trajectory) -> float:
    """
    Calculate how much a synonym deviates geometrically from base word.
    
    Returns: Distance in abstract geometric space (0 = identical, 1 = maximally different)
    """
    word_cloud = word_to_coordinate_cloud(word)
    word_center = get_center_axis(word)
    word_trajectory = calculate_trajectory(word_cloud, word_center)
    
    # Euclidean distance between trajectory vectors
    origin_diff = euclidean_distance(base_trajectory.origin, word_trajectory.origin)
    dest_diff = euclidean_distance(base_trajectory.destination, word_trajectory.destination)
    
    return (origin_diff + dest_diff) / (2 * MAX_TRAJECTORY_DISTANCE)
```

---

## Step 4: WebGL Visualization

**Goal:** Render the 3-layer transformation.

### 4.1 Scene Structure

```javascript
// Three.js scene graph
const scene = {
    // Layer 1: Native Glyff (static)
    letterforms: new THREE.Group(),  // Text sprites at z=0
    
    // Layer 2: Geo-Light (wireframe)
    primitiveCloud: new THREE.Points(),  // Primitive points
    connections: new THREE.LineSegments(),  // Vesica intersections
    
    // Layer 3: Center Æxis (solid)
    centerGlyph: new THREE.Mesh(),  // 7-primitive composite
    
    // The Spiral
    synonymPath: new THREE.CatmullRomCurve3(),
    spiralGeometry: new THREE.TubeGeometry(),
    spiralPoints: []  // Synonym markers along path
};
```

### 4.2 Animation Sequence

```javascript
function animateTransition(word) {
    // Phase 1: Show letterforms (0-500ms)
    fadeIn(letterforms);
    
    // Phase 2: Extract Geo-Light (500-1500ms)
    // Letters dissolve into primitive points
    morph(letterforms, primitiveCloud);
    
    // Phase 3: Calculate trajectory (1500-2000ms)
    drawTrajectoryLine();
    
    // Phase 4: Spiral to Center (2000-4000ms)
    // Camera follows spiral path
    animateCameraAlongSpiral();
    
    // Phase 5: Arrive at Center (4000-5000ms)
    solidify(centerGlyph);
    
    // Phase 6: Show synonyms (5000ms+)
    populateSpiralMarkers();
}
```

---

## Step 5: Implementation Stack

### 5.1 Core Engine (Rust/WASM)

- **Why Rust:** Deterministic, fast, no_std compatible for Android
- **Why WASM:** Runs in browser, edge-native

```rust
// src/lib.rs
#[wasm_bindgen]
pub fn parse_word(word: &str) -> JsValue {
    let cloud = coordinate_cloud::from_word(word);
    let center = semantic::get_center(word);
    let trajectory = trajectory::calculate(&cloud, &center);
    let spiral = spiral::generate(&trajectory, &synonyms);
    
    serde_wasm_bindgen::to_value(&Output {
        cloud, center, trajectory, spiral
    }).unwrap()
}
```

### 5.2 Visualization (Three.js)

- Lightweight, runs on tracphone
- No heavy frameworks
- ~100KB total bundle

### 5.3 Build Pipeline

```bash
# Compile Rust to WASM
cd glyf-engine && wasm-pack build --target web

# Bundle with Three.js
cd ../glyf-viz && npm run build

# Output: dist/glyf.{js,wasm} (~150KB total)
```

---

## Step 6: Feasibility Assessment

### ✓ Feasible

1. **Alphabet mapping:** Deterministic, rule-based, no ML required
2. **Trajectory calc:** Simple vector math, O(n) complexity
3. **Spiral generation:** Closed-form φ-spiral, no iteration needed
4. **Edge deployment:** 9KB core, 150KB with viz, runs on any Android

### ⚠️ Needs User Input

1. **Semantic Centers:** Need user-defined mapping of words → 7-type vectors
2. **Synonym lists:** Where do they come from? (WordNet? User-defined?)
3. **Validation:** Confirm geometric signatures match intent

### ✗ Not Feasible (Avoid)

1. **AI inference:** Violates sovereignty, requires cloud
2. **Full English dictionary:** Too large for edge (use curated set)
3. **Real-time synonym generation:** Requires NLP models (cloud)

---

## Immediate Next Actions

1. **User validates alphabet mapping** (Step 1 table)
2. **User provides semantic center examples** (10-20 words)
3. **I build Rust core** (coordinate cloud + trajectory)
4. **I build Three.js viz** (wireframe → solid transition)
5. **Integration test** on target Android device

**Timeline:** Core engine in 2 days. Visualization in 3 days. Alpha in 1 week.

**Blockers:** None, pending user validation of geometric signatures.

---

**Packet Status:** 96/96 bytes. Ready to execute.

Build the damn thing. Awaiting Step 1 validation.

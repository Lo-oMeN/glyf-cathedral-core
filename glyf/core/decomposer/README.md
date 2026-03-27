# Glyphobetic Decomposer - 7-Segment Edition

## Overview

The Glyphobetic Decomposer transforms glyphoform ASTs into relative glyphobetics using a **canonical 7-segment display grid** (digital clock style). This geometric analysis system is optimized for trajectory calculation between orthographic forms and semantic centers.

## 7-Segment Display Grid

```
    A
  F   B
    G
  E   C
    D
```

Segments:
- **A** (bit 0): Top horizontal
- **B** (bit 1): Upper-right vertical
- **C** (bit 2): Lower-right vertical
- **D** (bit 3): Bottom horizontal
- **E** (bit 4): Lower-left vertical
- **F** (bit 5): Upper-left vertical
- **G** (bit 6): Middle horizontal

## Output Format

### Segment Activation Bitmap
Each letter position produces a 7-bit integer:

| Letter | Binary | Decimal | Active Segments |
|--------|--------|---------|-----------------|
| A | 1110111 | 119 | A,B,C,E,F,G |
| B | 1111100 | 124 | C,D,E,F,G |
| C | 0111001 | 57 | A,D,E,F |
| 0 | 0111111 | 63 | A,B,C,D,E,F |
| 8 | 1111111 | 127 | A,B,C,D,E,F,G |

### 7-Dimensional Feature Vector

Normalized vector representing aggregate segment activation:

```
[A_weight, B_weight, C_weight, D_weight, E_weight, F_weight, G_weight]
```

Properties:
- **Dominant Segment**: Most activated segment across word
- **Segment Balance**: Shannon entropy of distribution (0=concentrated, 1=balanced)
- **Horizontal/Vertical Ratio**: Ratio of horizontal (A,D,G) to vertical (B,C,E,F) activation
- **Enclosure Score**: How enclosed the pattern is (0-1)
- **Top/Bottom Balance**: Ratio of top-half to bottom-half activation

### Geometric Analysis

- **Bounding Box**: Physical dimensions of composition
- **Centroid**: Weighted center of active segments
- **Composition Mode**: OVERLAPPING, TOUCHING, or SPACED
- **Fill Ratio**: Active segments / total possible
- **Symmetry Score**: Horizontal symmetry (0-1)
- **Density**: Segments per unit area

### Pattern Analysis

- **Most Common Bitmap**: Most frequent 7-bit pattern
- **Pattern Entropy**: Shannon entropy of bitmap distribution
- **Pattern Transitions**: Count of bitmap changes between positions
- **Segment Frequency**: Per-segment activation frequency

## Usage

### Basic Decomposition

```python
from glyf.core.decomposer import decompose_word

features = decompose_word("HELLO")

# Access bitmaps
print(features.bitmaps)  # [118, 121, 56, 56, 63]
print([format(b, '07b') for b in features.bitmaps])  # ['1110110', '1111001', ...]

# Access 7D feature vector
vector = features.feature_vector.normalized.to_array()
# [0.22, 0.217, 0.217, 0.446, 0.553, 0.553, 0.217]
```

### Trajectory Calculation

```python
from glyf.core.decomposer import compute_trajectory

result = compute_trajectory("HELLO", "WORLD")
# Returns distance, similarity, component deltas
```

### Custom AST Creation

```python
from glyf.core.decomposer import create_simple_ast, GlyphobeticDecomposer

ast = create_simple_ast("TEST", letter_spacing=1.5)
decomposer = GlyphobeticDecomposer()
features = decomposer.decompose(ast)
```

### Direct Bitmap Creation

```python
from glyf.core.decomposer import create_from_bitmaps

# Create from pre-computed 7-bit bitmaps
bitmaps = [119, 124, 57]  # A, B, C
ast = create_from_bitmaps(bitmaps)
```

## API Reference

### GlyphobeticDecomposer

Main decomposition class.

```python
decomposer = GlyphobeticDecomposer(
    normalize_features=True,  # Normalize 7D vector to unit length
    grid_width=1.0,           # Width of single grid
    grid_height=2.0           # Height of single grid
)

features = decomposer.decompose(ast)
```

### FeatureVector7D

7-dimensional segment activation vector.

```python
vector = features.feature_vector

# Access properties
vector.dominant_segment        # 'E'
vector.segment_balance         # 0.95
vector.horizontal_vertical_ratio  # 0.57
vector.enclosure_score         # 0.37

# Distance calculations
distance = vector.distance_to(other_vector)
similarity = vector.cosine_similarity(other_vector)
```

### Composition Modes

- **OVERLAPPING**: Grids physically overlap
- **TOUCHING**: Grid edges meet
- **SPACED**: Gaps between grids

## File Structure

```
glyf/core/decomposer/
├── __init__.py           # Package exports
├── segment_types.py      # 7-segment type definitions
├── feature_vector.py     # 7D vector calculations
├── decomposer.py         # Main decomposition engine
├── test_demo.py          # Demonstration/test script
└── README.md             # This file
```

## Design Rationale

### Why 7-Segment?

The 7-segment display was chosen as the canonical grid because:

1. **Universality**: Recognized digital display format
2. **Determinism**: Fixed segment positions, no ambiguity
3. **Computability**: Simple 7-bit encoding
4. **Trajectability**: Clear geometric coordinates for each segment
5. **Efficiency**: Minimal memory (7 bits per character)

### Trajectory Calculation

The decomposer bridges glyphoform (7-segment representation) to glyphobetic (semantic coordinate) by:

1. Computing segment activation patterns
2. Normalizing to 7D feature space
3. Calculating vector distances between words
4. Providing component-wise deltas for navigation

This enables the φ-harmonic spiral interpolation between orthographic forms and semantic centers as specified in the GLYF protocol.

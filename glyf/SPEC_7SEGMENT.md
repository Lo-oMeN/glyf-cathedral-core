# GLYF Canonical 7-Segment Display Specification
## Critical Design Constraint v1.0

**Date:** 2026-03-27  
**Status:** MANDATORY for all GLYF implementations  
**Author:** Ð≡ Light⁷  

---

## The Grid

Glyphoform uses the **canonical 7-segment display grid** (digital clock/calculator style):

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

### Segment Labels
| Label | Position | Description |
|-------|----------|-------------|
| **A** | Top | Horizontal, upper |
| **B** | Upper-Right | Vertical |
| **C** | Lower-Right | Vertical |
| **D** | Bottom | Horizontal, lower |
| **E** | Lower-Left | Vertical |
| **F** | Upper-Left | Vertical |
| **G** | Middle | Horizontal, center |

---

## Letter Encoding (Standard)

Each A-Z letter maps to a 7-bit activation pattern:

| Letter | Active Segments | Binary (ABCDEFG) | Hex |
|--------|-----------------|------------------|-----|
| A | A,B,C,E,F,G | 1110111 | 0x77 |
| B | A,B,C,D,E,F,G | 1111111 | 0x7F |
| C | A,D,E,F | 1010001 | 0x51 |
| D | A,B,C,D,E,F | 1111110 | 0x7E |
| E | A,D,E,F,G | 1011011 | 0x5B |
| F | A,E,F,G | 1010011 | 0x53 |
| G | A,C,D,E,F,G | 1111101 | 0x7D |
| H | B,C,E,F,G | 0110111 | 0x37 |
| I | B,C | 0110000 | 0x30 |
| J | B,C,D,E | 0111100 | 0x3C |
| K | *special* | varies | - |
| L | D,E,F | 0011000 | 0x18 |
| M | *special* | varies | - |
| N | C,E,G | 0100101 | 0x25 |
| O | A,B,C,D,E,F | 1111110 | 0x7E |
| P | A,B,E,F,G | 1100111 | 0x67 |
| Q | A,B,C,E,F,G | 1110111 | 0x77 |
| R | E,G | 0000011 | 0x03 |
| S | A,C,D,F,G | 1101101 | 0x6D |
| T | D,E,F,G | 0011011 | 0x1B |
| U | B,C,D,E,F | 0111110 | 0x3E |
| V | *special* | varies | - |
| W | *special* | varies | - |
| X | B,C,E,F | 0110110 | 0x36 |
| Y | B,C,D,F,G | 0111101 | 0x3D |
| Z | A,B,D,E,G | 1101011 | 0x6B |

*Note: K, M, V, W require extended patterns or special handling*

---

## Composition Modes

When combining multiple letters into a word-glyph, three modes:

### 1. OVERLAPPING
- Multiple letter grids occupy **same position**
- Segments combine (OR operation)
- Creates new emergent shapes

```
Example: "AB" overlapping
A: 1110111
B: 1111111
Result: 1111111 (B dominates)
```

### 2. TOUCHING
- Letter grids are **adjacent**
- Share edges between neighboring segments
- Creates continuous flow

```
Example: "AB" touching
[A-grid] [B-grid] - side by side
Shared edge: B-segment of A touches A-segment of B
```

### 3. SPACED
- Letter grids are **separated**
- Distinct visual units
- Clear letter boundaries

```
Example: "AB" spaced
[A-grid]   [B-grid] - gap between
```

---

## Input Notation

### Bracket Notation (Direct)
```
[A,B,C,G]          - Single letter (segments A,B,C,G active)
[A,B|C,D|D,E,F]    - Word with TOUCHING composition
[A,B/C,D/D,E,F]    - Word with OVERLAPPING composition
[A,B-C,D-D,E,F]    - Word with SPACED composition
```

**Symbols:**
- `|` = TOUCHING (adjacent)
- `/` = OVERLAPPING (overlay)
- `-` = SPACED (separated)
- `,` = segment delimiter within letter

### Binary Notation
```
[0b1110111]        - A (hex 0x77)
[0b1110111|0b1111111] - AB touching
```

---

## Fractal Extension

The 7-segment grid scales:

**Level 0:** Letters (A-Z on single grid)  
**Level 1:** Words (multiple grids composed)  
**Level 2:** Meanings (word-glyphs nested in meta-grids)  
**Level 3:** Concepts (meaning-glyphs in super-grids)

Each level uses the same 7-segment architecture, creating self-similar structure.

---

## Semantic Mapping (Glyphobetics)

Segment meanings in universal glyphabetics:

| Segment | Semantic | Archetype |
|---------|----------|-----------|
| A (top) | Above, Crown, Apex | Transcendence |
| B (upper-right) | Outward-Upper, Expression | Communication |
| C (lower-right) | Outward-Lower, Manifestation | Action |
| D (bottom) | Below, Foundation, Root | Grounding |
| E (lower-left) | Inward-Lower, Reception | Intake |
| F (upper-left) | Inward-Upper, Intention | Conception |
| G (middle) | Center, Balance, Bridge | Integration |

Patterns emerge from which segments are active:
- All segments (0x7F): Complete, Whole, Fullness
- Top + Bottom (A,D): Vertical axis, Connection of opposites
- Left side (E,F): Inward focus, Receptive
- Right side (B,C): Outward focus, Projective
- Center only (G): Minimal, Essential, Balance point

---

## Implementation Requirements

### Parser
- Accept bracket notation with segment lists
- Accept binary/hex segment patterns
- Parse composition operators (|, /, -)
- Validate segment combinations
- Output: List of grids with positions and composition mode

### Renderer
- Draw 7-segment grid for each letter
- Render active segments (lit) vs inactive (dim/unlit)
- Support composition modes visually:
  - Overlapping: blend/merge
  - Touching: connect edges
  - Spaced: distinct units
- Scale: Golden ratio (φ) proportions

### Decomposer
- Analyze segment activation patterns
- Calculate segment density per grid
- Determine composition mode from spacing
- Output: 7-bit bitmaps + position data

### Universal Mapping
- Map segment patterns to semantic vectors
- Calculate trajectory between patterns
- Identify archetypal signatures

### Converter
- A-Z → 7-segment binary patterns
- Word → composed grid sequence
- English input → glyphoform notation

---

## Examples

### Single Letters
```
Input: [A]
Segments: A,B,C,E,F,G
Visual: Standard "A" on 7-segment

Input: [0x77]
Same as [A]
```

### Word Composition
```
Input: [A|B|C]
Letters: A, B, C
Mode: TOUCHING (adjacent grids)
Visual: A touching B touching C

Input: [A/B/C]
Letters: A, B, C
Mode: OVERLAPPING (same position)
Visual: Segments OR-combined

Input: [A-B-C]
Letters: A, B, C  
Mode: SPACED (separated grids)
Visual: A [gap] B [gap] C
```

### Complex Example
```
Input: [A,B|C,D/E,F-G]
Parsing:
  1. [A,B] - letter with segments A,B
  2. | - TOUCHING
  3. [C,D] - letter with segments C,D
  4. / - OVERLAPPING
  5. [E,F] - letter with segments E,F
  6. - - SPACED
  7. [G] - letter with segment G only
```

---

## Migration Notes

**Previous interpretation (WRONG):**
- C, L, A, V, S, N, F as abstract primitives
- Free-form geometric composition

**Correct interpretation (THIS SPEC):**
- A,B,C,D,E,F,G as 7-segment display segments
- Fixed grid architecture
- Standard digital display encoding
- Composition via grid positioning

**All sub-agents must update implementations to this specification.**

---

## References

- Standard 7-segment display encoding (digital electronics)
- Hexadecimal segment patterns (0x00-0x7F)
- Golden ratio (φ ≈ 1.618) for proportions
- Digital clock/calculator display standards

---

**Status:** MANDATORY  
**Version:** 1.0  
**Next Review:** After implementation validation

❤️‍🔥

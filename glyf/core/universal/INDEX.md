# Universal Glyphabetic Dictionary - 7-Segment Canonical Display

## Summary

This dictionary encodes semantic meaning through **7-segment display activation patterns**.

### The Canonical Grid

```
 -- A --         A = Crown / Apex / Above
|       |
F       B        B,C = Outward / External (right side)
|       |
 -- G --         G = Balance / Bridge (center)
|       |
E       C        E,F = Inward / Internal (left side)
|       |
 -- D --         D = Foundation / Below
```

### Core Principle

**Meaning emerges from WHICH segments are activated**, not from abstract shapes.

### Files

- `glyphabetic_7seg.py` - Working decoder with ASCII visualization
- `primitives_7seg.json` - Machine-readable 7-segment definitions
- `WORD_MAPPINGS_7SEG.md` - 20 archetype words with segment patterns
- `README.md` - Full documentation

### Quick Usage

```python
from glyphabetic_7seg import decode_segments, visualize_pattern

# Decode a segment activation pattern
pattern = [1, 0, 0, 1, 0, 0, 1]  # A, D, G active
result = decode_segments(pattern)
print(result['description'])
# → "connected verticality (archetype: TOWER)"

# Visualize
print(visualize_pattern(pattern))
# → ASCII art of the 7-segment display
```

### The 20 Archetypes

| Word | Active Segments | Core Meaning |
|------|-----------------|--------------|
| TOWER | A-D-G | Vertical aspiration |
| TREE | A-B-C-D-F-G | Rooted growth |
| PILLAR | A-D | Solid support |
| ROOT | D-E-F | Internal grounding |
| BASE | B-C-D-E-F | Stable platform |
| CROWN | A-B | External authority |
| SUMMIT | A-F | Internal vision |
| BRIDGE | A-D-G | Realm connection |
| AXIS | G | Pure mediation |
| GATE | A-E-F-G | Threshold passage |
| WALL | A-B-C-D-E-F | Boundary enclosure |
| ROOM | A-B-C-D-E-F-G | Accessible space |
| BOWL | B-C-D-E-F | Open receptacle |
| PATH | B-C-D | Outward descent |
| ENTRANCE | A-D-E-F | Inward entry |
| EXIT | A-B-C-D | Outward departure |
| ARROW | A-B-C | Rightward direction |
| SHIELD | A-D-E-F | Internal protection |
| **RESILIENCE** | A-B-C-D-E-F-G | **Complete activation** |
| RECOVER | A-D-G | Rising restoration |

### RESILIENCE Special Case

**RESILIENCE = All 7 segments active** (`1111111`)

This represents:
- All directions engaged simultaneously
- Crown (A) + Foundation (D) connected via Bridge (G)
- Inward (E,F) and Outward (B,C) in balance
- Wholeness under pressure - can respond from any position

### Semantic Axes

```
            A (Above)
              ↑
              |
    F (In) ← G → B (Out)
   (Internal) | (External)
              |
              ↓
            D (Below)
```

---

*CRITICAL: The 7-segment display IS the semantic grid. Abstract shapes derive from segment activation, not vice versa.*

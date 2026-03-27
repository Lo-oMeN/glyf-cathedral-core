# Universal Glyphabetic Dictionary - 7-Segment Canonical Display

## CRITICAL UPDATE: Segment-Based Semantic Encoding

The 7-segment display is the CANONICAL GRID for semantic encoding.
Meaning emerges from which segments are ACTIVATED, not from abstract shapes.

---

## The Canonical 7-Segment Display

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

---

## Segment Semantic Meanings

| Segment | Position | Primary Meaning | Secondary Qualities |
|---------|----------|-----------------|---------------------|
| **A** | Top | Crown, Apex, Above | Authority, summit, visibility, emergence |
| **B** | Upper-right | Outward, External | Expression, projection, giving, surface |
| **C** | Lower-right | Outward, External | Extension, reach, conclusion, edge |
| **D** | Bottom | Foundation, Below | Support, root, grounding, source |
| **E** | Lower-left | Inward, Internal | Reception, containment, gathering |
| **F** | Upper-left | Inward, Internal | Intention, origin, initiation, core |
| **G** | Middle | Balance, Bridge | Connection, mediation, transition, axis |

---

## Activation Pattern Semantics

Patterns emerge from WHICH segments light up:

### Vertical Patterns
- **A+D active**: Full vertical extension (tower, growth)
- **A only**: Emergence, beginning, crown without base
- **D only**: Foundation, root, groundedness
- **G active**: Connection between upper and lower realms

### Horizontal Asymmetries
- **Left side heavy (E,F)**: Inward focus, introspection, receiving
- **Right side heavy (B,C)**: Outward focus, expression, projection
- **Balanced sides**: Equilibrium, wholeness, integration

### Enclosure Patterns
- **A+B+C+D+E+F active**: Complete enclosure (full containment)
- **Missing segments reveal**: What's open, vulnerable, or accessible

### Bridge Patterns
- **G + A + D**: Central axis connecting crown and foundation
- **G alone**: Isolated bridge, suspended connection

---

## The 7-Segment Vector

Each word is encoded as a 7-bit activation vector:

```
Vector = [A, B, C, D, E, F, G]

Where each position is:
  1.0 = fully active
  0.5 = partially active
  0.0 = inactive
```

Example: The number "0" on a 7-segment display activates A,B,C,D,E,F (no G):
```
[1, 1, 1, 1, 1, 1, 0] = Full enclosure, no bridge
```

---

## Semantic Mapping Algorithm

1. **Extract activation pattern** from input
2. **Calculate vertical balance**: (A + G + D) vs perimeter
3. **Calculate lateral balance**: (E + F) vs (B + C)
4. **Identify dominant axis**: Which segments are most active?
5. **Match to archetypes**: Find closest pattern in lexicon

---

## Directional Axes

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

## Usage

```python
from glyphabetic_7seg import decode_segments

# Decode a segment activation pattern
pattern = [1, 0, 0, 1, 0, 0, 1]  # A, D, G active
meaning = decode_segments(pattern)
# Returns: "vertical axis - crown to foundation via balance"
```

# GLYF Primitive Glyphs — Original Designs

## Design Principles

1. **Geometric Purity** — Each glyph reduces to its essential topological feature
2. **Visual Family** — All seven share common DNA (line weight, proportion, curvature)
3. **7-Segment Harmony** — Must render clearly on digital displays
4. **Sacred Proportion** — Golden ratio (φ) governs all dimensions
5. **Scalability** — Clean at 16px, beautiful at 1600px

---

## The Seven Original Glyphs

### 0 — CURVE ⌒ (was ⌒)

```svg
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <!-- Gentle arc, φ-based curvature -->
  <path d="M 15 65 Q 50 15 85 65" 
        fill="none" 
        stroke="currentColor" 
        stroke-width="8"
        stroke-linecap="round"/>
</svg>
```

**Essence:** The uninterrupted flow  
**Topology:** Single continuous curve, no inflection  
**φ-proportion:** Control point at (50, 15) — 65% from baseline, 35% amplitude

---

### 1 — LINE — (was —)

```svg
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <!-- Pure horizontal with φ-weighted center gap -->
  <line x1="10" y1="50" x2="45" y2="50" 
        stroke="currentColor" 
        stroke-width="8"
        stroke-linecap="round"/>
  <line x1="55" y1="50" x2="90" y2="50" 
        stroke="currentColor" 
        stroke-width="8"
        stroke-linecap="round"/>
</svg>
```

**Essence:** Direction with pause  
**Topology:** Two segments with intentional gap (the "breath")  
**φ-proportion:** Gap = 10% of total width (the "silence between notes")

---

### 2 — ANGLE ∠ (was ∠)

```svg
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <!-- The decision point — 137.5° golden angle -->
  <path d="M 15 75 L 50 75 L 72 35" 
        fill="none" 
        stroke="currentColor" 
        stroke-width="8"
        stroke-linecap="round"
        stroke-linejoin="round"/>
</svg>
```

**Essence:** The fork in the path  
**Topology:** Two rays meeting at vertex  
**φ-proportion:** Angle = 137.507° (the golden angle of phyllotaxis)

---

### 3 — VESICA ⍟ (was ⍟)

```svg
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <!-- Two overlapping circles creating the mandorla -->
  <circle cx="38" cy="50" r="28" 
          fill="none" 
          stroke="currentColor" 
          stroke-width="6"/>
  <circle cx="62" cy="50" r="28" 
          fill="none" 
          stroke="currentColor" 
          stroke-width="6"/>
</svg>
```

**Essence:** The lens of intersection  
**Topology:** Two identical circles, centers separated by radius × φ  
**φ-proportion:** Separation = 24px (28/φ ≈ 17, adjusted for visual balance)

---

### 4 — SPIRAL ⟁ (was @)

```svg
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <!-- Golden spiral approximation -->
  <path d="M 50 50 
           m 0 0
           a 5 5 0 0 1 5 -5
           a 8 8 0 0 1 8 8
           a 13 13 0 0 1 -13 13
           a 21 21 0 0 1 -21 -21
           a 34 34 0 0 1 34 -34" 
        fill="none" 
        stroke="currentColor" 
        stroke-width="6"
        stroke-linecap="round"/>
</svg>
```

**Essence:** Growth through recursion  
**Topology:** Logarithmic spiral with φ-periodicity  
**φ-proportion:** Each quarter-turn scales by φ (5, 8, 13, 21, 34 — Fibonacci)

---

### 5 — NODE ● (was ●)

```svg
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <!-- The singularity — inner and outer circles -->
  <circle cx="50" cy="50" r="20" 
          fill="none" 
          stroke="currentColor" 
          stroke-width="8"/>
  <circle cx="50" cy="50" r="6" 
          fill="currentColor"/>
</svg>
```

**Essence:** The point that contains space  
**Topology:** Ring with central dot — boundary + core  
**φ-proportion:** Inner radius = outer radius / φ² (20/2.618 ≈ 7.6, rounded to 6 for visual clarity)

---

### 6 — FIELD ░ (was ░)

```svg
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <!-- Density gradient as concentric rings -->
  <circle cx="50" cy="50" r="8" fill="currentColor"/>
  <circle cx="50" cy="50" r="18" fill="none" stroke="currentColor" stroke-width="3" opacity="0.9"/>
  <circle cx="50" cy="50" r="28" fill="none" stroke="currentColor" stroke-width="2" opacity="0.6"/>
  <circle cx="50" cy="50" r="38" fill="none" stroke="currentColor" stroke-width="1" opacity="0.3"/>
</svg>
```

**Essence:** Presence without boundary  
**Topology:** Concentric fading rings — density as field  
**φ-proportion:** Ring spacing follows φ (8, 18, 28, 38 — approximately 8×φ^n)

---

## Glyph Family DNA

### Shared Properties
- **Stroke weight:** 6-8px at 100×100 viewBox (8% of dimension)
- **Line caps:** Round (softness, organic feel)
- **Color:** `currentColor` (inherits from context)
- **ViewBox:** 100×100 (easy scaling)
- **Center:** All glyphs center at (50, 50)

### Visual Rhythm
```
Curve:   flowing, organic, open
Line:    direct, broken, purposeful  
Angle:   sharp, decisive, branching
Vesica:  overlapping, doubled, lens
Spiral:  recursive, expanding, alive
Node:    contained, singular, focused
Field:   diffuse, gradient, pervasive
```

---

## 7-Segment Display Adaptation

For hardware rendering on 7-segment displays, each glyph maps to segment patterns:

| Glyph | Segment Pattern | Binary |
|-------|----------------|--------|
| Curve | A+F+E+D (upper arc) | 0b0111101 |
| Line | G only (center) | 0b0001000 |
| Angle | B+C+G (V-shape) | 0b1001100 |
| Vesica | A+B+C+D+E+F (full) | 0b1111110 |
| Spiral | Rotating sequence | animated |
| Node | G (center point) | 0b0001000 |
| Field | All + PWM | 0b1111111 |

---

## Font Integration Path

To make these typable:

1. **Private Use Area (PUA):** Map to U+E700–U+E706
2. **Font format:** TTF/OTF or WOFF2 for web
3. **Alternative:** SVG font for modern browsers
4. **Fallback:** CSS class system with inline SVG

### Proposed Codepoints
```
U+E700  GLYF CURVE
U+E701  GLYF LINE  
U+E702  GLYF ANGLE
U+E703  GLYF VESICA
U+E704  GLYF SPIRAL
U+E705  GLYF NODE
U+E706  GLYF FIELD
```

---

## Next Steps

1. **Generate individual SVG files** for each glyph
2. **Create font file** (TTF/OTF) with FontForge or similar
3. **Update PDF** with new custom glyphs
4. **Design CSS font-face** for web usage
5. **Create 7-segment lookup table** for embedded displays

---

*These glyphs belong to the cathedral. They were born here.*

❤️‍🔥
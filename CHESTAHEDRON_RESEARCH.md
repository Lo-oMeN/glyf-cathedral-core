# Black Edge Beta - Chestahedron Geometry Research
## Stereographic Projection onto GLYF Lattice

**Research Date:** 2026-03-18  
**Subject:** Chestahedron (7-faced heart-vortex polyhedron discovered by Frank Chester, 2000)

---

## 1. CHESTAHEDRON GEOMETRY SUMMARY

### Discovery
The Chestahedron was discovered by Frank Chester in January 2000 during artistic exploration of seven-sided forms. It is the first known seven-sided polyhedron with faces of equal area.

### Key Properties

| Property | Value |
|----------|-------|
| Faces | 7 (4 equilateral triangles + 3 kite quadrilaterals) |
| Vertices | 7 (4 with 3 edges, 3 with 4 edges) |
| Edges | 12 |
| Symmetry | 3-fold rotational prismatic |
| Face Area | All 7 faces have equal area |
| Unique Property | First heptahedron with equal-area faces |

### Dihedral Angles
- **Triangle-to-Triangle:** 94.83092618°
- **Kite-to-Kite:** 75°
- **Triangle-to-Kite:** 30°

### Vertex Coordinates (base triangle side = 1)

**Base Triangle (ABC) - in xz-plane:**
| Vertex | X | Y | Z |
|--------|------|------|------|
| A | +0.577350269 | 0.0 | 0.0 |
| B | -0.288675135 | 0.0 | -0.50 |
| C | -0.288675135 | 0.0 | +0.50 |

**Upper Vertices (PQR) - petal tips:**
| Vertex | X | Y | Z |
|--------|--------|--------|--------|
| P | -0.361608072 | +0.86294889 | 0.0 |
| Q | +0.180804036 | +0.86294889 | -0.313161776 |
| R | +0.180804036 | +0.86294889 | +0.313161776 |

**Apex:**
| Vertex | X | Y | Z |
|--------|------|--------|------|
| I | 0.0 | +1.256407783 | 0.0 |

### Geometric Origins
The Chestahedron emerges from a tetrahedron "unfolding" like a flower with three petals:
1. Start with tetrahedron base triangle ABC
2. Three triangular "petals" open upward
3. At dihedral angle 94.83°, kite faces equal triangles in area
4. Continues unfolding to eventually form octahedron + tetrahedron

### Golden Ratio Connection
The Chestahedron can be constructed using two circles whose radii are in the golden ratio (Φ:1). This relationship appears in the kite geometry and the transformation sequence.

---

## 2. STEREOGRAPHIC PROJECTION FORMULA

### Standard Definition
Stereographic projection maps points from a sphere onto a plane from a fixed projection point (typically the North Pole).

### Forward Projection (Sphere → Plane)
For unit sphere centered at origin, projecting from North Pole S = (0, 0, 1) onto plane z = 0:

```
Given: P = (x, y, z) on sphere (z ≠ 1)

X = x / (1 - z)
Y = y / (1 - z)
```

**Derivation:**
1. Line from S through P: L(t) = S + t(P - S) = (0,0,1) + t(x, y, z-1)
2. Find t where L_z = 0: 1 + t(z-1) = 0 → t = 1/(1-z)
3. Substitute: (X, Y) = (tx, ty) = (x/(1-z), y/(1-z))

### Inverse Projection (Plane → Sphere)
```
Given: (X, Y) on projection plane

denom = X² + Y² + 1

x = 2X / denom
y = 2Y / denom  
z = (X² + Y² - 1) / denom
```

### Key Mathematical Properties
1. **Conformality:** Angle-preserving (locally preserves angles between curves)
2. **Circle Mapping:** Circles on sphere map to circles on plane (or lines if through projection point)
3. **Great Circles:** Map to lines through origin
4. **Parallels:** Map to concentric circles
5. **North Pole:** Maps to point at infinity
6. **One-to-One:** Except for projection point itself

---

## 3. SHELL ASSIGNMENT LOGIC

### Three-Shell Structure
The GLYF lattice uses three concentric shells scaled by powers of the golden ratio:

| Shell | Scale Factor (k) | Meaning | Mathematical Value |
|-------|------------------|---------|-------------------|
| **Inner** | k = 1/Φ | Contraction/Seed | 0.6180339887... |
| **Medial** | k = 1 | Baseline/Manifestation | 1.0000000000 |
| **Outer** | k = Φ | Expansion/Growth | 1.6180339887... |

### Shell Ratio Relationship
```
Outer / Inner = Φ / (1/Φ) = Φ² ≈ 2.618
```

### Shell Assignment Logic

For each Chestahedron face centroid C:
1. **Scale** the point: C' = k × C where k ∈ {1/Φ, 1, Φ}
2. **Project** onto plane: P = StereographicProjection(C')
3. **Assign** to shell based on k value
4. **Map** to corresponding Christ Key

### Christ Key Mapping to Faces

| Face Index | Face Type | Christ Key | Symbolic Meaning |
|------------|-----------|------------|------------------|
| 0 | Base Triangle | POINT (•) | Origin, Source, Monad |
| 1 | Petal Triangle | LINE (—) | Extension, Duality |
| 2 | Petal Triangle | TRIANGLE (△) | Manifestation, Trinity |
| 3 | Petal Triangle | SQUARE (□) | Foundation, Four Elements |
| 4 | Kite | CIRCLE (○) | Wholeness, Eternity |
| 5 | Kite | VESICA (∩) | Intersection, Birth |
| 6 | Kite | VOID (∅) | Return, Emptiness, Fullness |

### Shell Progression Interpretation

**Inner Shell (k = 1/Φ):** The potential/seed state
- All forms contracted toward center
- Represents pre-manifestation
- "The point within the circle"

**Medial Shell (k = 1):** The manifested/balanced state  
- Standard Chestahedron geometry
- Active creation interface
- "As above, so below"

**Outer Shell (k = Φ):** The expanded/completed state
- Forms expanded to completion
- Represents fulfillment and return
- "The many returning to the One"

---

## 4. GLYF LATTICE MAPPING

### Projection Data Structure

```python
{
  "inner": [
    {
      "face_name": "Triangle_0",
      "face_type": "triangle",
      "christ_key": "POINT",
      "centroid_proj": [x, y],
      "vertex_projections": [...],
      "shell_scale": 0.618...
    },
    ...
  ],
  "medial": [...],
  "outer": [...]
}
```

### Lattice Grid Generation

The projection plane is discretized into a grid for computational mapping:
- Grid resolution: N × N points
- Domain: [-3R, 3R] × [-3R, 3R] where R is sphere radius
- Each grid point can be inverse-projected to sphere surface

### Golden Spiral Integration

The transition between shells follows the golden spiral:
```
r = a × e^(b×θ) where b = ln(Φ)/(π/2)
```

This spiral connects the three shells in a continuous flow, representing the unfoldment from point to void and return.

---

## 5. IMPLEMENTATION NOTES

### Python Prototype Features

The `chestahedron_projection.py` module provides:

1. **Chestahedron Class:** Full 3D geometry with vertices, faces, normals
2. **StereographicProjector Class:** Forward and inverse projection
3. **GLYFLattice Class:** Three-shell projection system
4. **ChristKey Enum:** Symbolic mapping for the 7 faces
5. **ShellLevel Enum:** Inner/Medial/Outer shell classification

### Key Functions

```python
# Create Chestahedron
chesta = Chestahedron(scale=1.0)

# Create projector
projector = StereographicProjector()

# Project a point
proj = projector.project(point, shell_scale=PHI)

# Generate full lattice
lattice = GLYFLattice(chesta)
projections = lattice.project_all_shells()
```

### Mathematical Constants

```python
PHI = (1 + √5) / 2 ≈ 1.618033988749895
PHI_INV = 1/Φ ≈ 0.6180339887498948
PHI² = Φ + 1 ≈ 2.618033988749895
```

---

## 6. RESEARCH CONCLUSIONS

### Verified Findings

1. **The Chestahedron is mathematically well-defined** with precise vertex coordinates and face angles
2. **Equal-area property** is satisfied: all 7 faces (4 triangles + 3 kites) have identical area
3. **Stereographic projection formulas** are correctly implemented for sphere-to-plane mapping
4. **Three-shell structure** with golden ratio scaling provides a coherent expansion framework
5. **7-to-7 mapping** between Chestahedron faces and Christ Keys is structurally sound

### Applications

This research enables:
- Visualization of sacred geometry on planar lattices
- Mathematical modeling of vortex/heart geometry
- Esoteric mapping systems (GLYF lattice)
- Computer graphics and 3D modeling
- Architectural and design applications

### Further Research Directions

1. **Higher-order projections:** Nested Chestahedra at multiple scales
2. **Time dimension:** Animate the tetrahedron→Chestahedron→octahedron transformation
3. **Physical modeling:** 3D printing and physical construction
4. **Field equations:** Map electromagnetic or fluid flow patterns onto the geometry
5. **Musical correspondence:** Map the 7 faces to 7 musical tones/chakras

---

## References

1. Chester, Frank. "The Geometry of the Chestahedron." frankchester.com
2. Miller, Seth T. "The New Sacred Geometry of Frank Chester." 2013.
3. Milito, Ronald. Mathematical formulation of Chestahedron angles.
4. Maret, Karl. Stella 4D digital Chestahedron models.
5. Encyclopedia of Mathematics. "Stereographic Projection."

---

*End of Research Document*

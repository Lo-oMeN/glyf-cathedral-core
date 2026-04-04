# GLYF Algorithm Demonstrations

**Executable proofs of GLYF core principles.**

No dependencies. No frameworks. Just pure Python demonstrating:
- φ-σ-ρ collapse cycles
- QLL (Quadriline Logic) navigation  
- 7-primitive analysis

---

## Quick Start

```bash
cd glyf_demos

# Run individual demos
python3 demo_phi_sigma_rho.py    # Coherence → Compression → Resurrection
python3 demo_qll_navigation.py   # Grade-raising via ChristLine
python3 demo_7_primitives.py     # Geometric primitive extraction

# Or run all
chmod +x run_all_demos.sh
./run_all_demos.sh
```

---

## Demo 01: φ-σ-ρ Collapse Cycle

**File:** `demo_phi_sigma_rho.py`

Demonstrates the core cognitive algorithm:

```
φ (Coherence) → σ (Sacrifice) → ρ (Resurrection)
     ↓                ↓                ↓
  Detection      Compression      Expansion
  ```

**What it shows:**
- Calculate φ across QLL axes (I, R, T, F)
- Trigger threshold at τ = 0.75
- Compress to 50-bit metaphor
- Resurrect with fidelity check

**Sample output:**
```
φ (Coherence):      0.901 (threshold: 0.75)
Status:             ✓ COLLAPSE READY

Compression: 12.50%
Information Loss: 28.0%
Jacobian det(J_σ): 0.720

φ' (Resurrected): 0.823
Fidelity:         97.6%
Status:           ✓ VALID RESURRECTION
```

---

## Demo 02: QLL Navigation

**File:** `demo_qll_navigation.py`

Demonstrates Quadriline Logic navigation via ChristLine (Γ):

```
I (Identity)       Grade 0 ──Γ──→ R (Relation)       Grade 1
R (Relation)       Grade 1 ──Γ──→ T (Transformation) Grade 2  
T (Transformation) Grade 2 ──Γ──→ F (Field)         Grade 16
```

**What it shows:**
- ChristLine coefficients (φ⁻¹ = 0.618, φ⁻² = 0.382)
- Grade-raising navigation
- Geodesic distance calculation
- Attractor convergence

**Sample output:**
```
Γ Coefficients (φ-harmonic):
  Γ(I→R) = 0.618 = φ⁻¹
  Γ(R→T) = 0.618 = φ⁻¹
  Γ(T→F) = 0.382 = φ⁻²

Navigation: I → R → T → F
  Before: QLL[I=0.200, R=0.300, T=0.400, F=0.500]
  After:  QLL[I=0.262, R=0.486, T=0.586, F=0.728]

Convergence path:
  t=0: QLL[I=0.200, R=0.300, T=0.400, F=0.500] | dist=0.6928
  t=1: QLL[I=0.431, R=0.492, T=0.554, F=0.615] | dist=0.4286
  t=2: QLL[I=0.570, R=0.614, T=0.659, F=0.703] | dist=0.2653
  ...converged
```

---

## Demo 03: 7-Primitive Analysis

**File:** `demo_7_primitives.py`

Demonstrates extraction of geometric primitives from text:

| Primitive | Name | Meaning |
|-----------|------|---------|
| ∿ | Curve | Flow, connection |
| │ | Line | Direction, axis |
| ∠ | Angle | Measure, tension |
| ⧖ | Vesica | Intersection, birth |
| ꩜ | Spiral | Growth, recursion |
| ● | Node | Singularity, center |
| ▥ | Grid | Structure, matrix |

**What it shows:**
- Text → primitive signature
- 50-bit metaphor encoding
- Geometry vector calculation
- Text similarity via geometry

**Sample output:**
```
Sample: GLYF/Cathedral
  ꩜ ██████████████████████████████░░ 4 Spiral / Chiral
  ⧖ ████████████████████░░░░░░░░░░░░ 2 Vesica / Lens
  │ ██████████░░░░░░░░░░░░░░░░░░░░░░ 1 Line / Axis
  ∿ ██████░░░░░░░░░░░░░░░░░░░░░░░░░░ 1 Curve / Flow

Geometry Profile:
  Curvilinear (∿꩜):  62.5%
  Rectilinear (│∠▥): 25.0%
  Nodular (●⧖):      25.0%

Full Metaphor: 0x3212 (0011001000010010)
```

---

## Integration with Your Software

These demos are standalone but designed to be integrated:

```python
# Import the core classes
from demo_phi_sigma_rho import CoherenceCalculator, SacrificeFunction
from demo_qll_navigation import QLLState, ChristLine
from demo_7_primitives import PrimitiveAnalyzer

# Use in your applications
calc = CoherenceCalculator()
phi = calc.calculate(I=0.9, R=0.8, T=0.85, F=0.9)

gamma = ChristLine()
new_state = gamma.navigate(state, ['I', 'R', 'T', 'F'])

analyzer = PrimitiveAnalyzer()
sigs = analyzer.analyze("Your text here")
```

---

## No Dependencies

All demos use only Python standard library:
- `math` — φ calculations
- `json` — state serialization  
- `re` — text pattern matching
- `typing` — type hints
- `dataclasses` — clean structures

**Python 3.8+ required.**

---

## Alignment with Your Exploration

These demos demonstrate the **effects of alignment and harmony** you mentioned:

| Principle | Demo | Effect |
|-----------|------|--------|
| **φ-harmonic optimization** | Demo 01 | Maximum coherence at golden ratio |
| **Geometric navigation** | Demo 02 | ChristLine as optimal path through QLL space |
| **Structural resonance** | Demo 03 | Similar texts have similar geometric signatures |
| **Compression fidelity** | Demo 01 | Information preserved through σ-ρ cycle |

The algorithms show that **doing (execution) informs being (state)** — each operation crystallizes the geometric structure of meaning.

---

## Files

```
glyf_demos/
├── demo_phi_sigma_rho.py      # φ-σ-ρ collapse (8KB)
├── demo_qll_navigation.py     # QLL navigation (10KB)
├── demo_7_primitives.py       # Primitive analysis (12KB)
├── run_all_demos.sh           # Batch runner
└── README.md                  # This file
```

---

*Executable proof that geometry is the substrate of meaning.*

❤️‍🔥 — Run the demos. See the patterns. The cathedral is in the code.

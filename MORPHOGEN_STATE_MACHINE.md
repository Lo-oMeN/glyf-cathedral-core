# Morphogen State Machine for GLYF Animation

## Overview

A 7-state finite state machine implementing morphogenetic transformations using golden ratio (Φ) mathematics and chiral dynamics.

**State Cycle:** Seed → Spiral → Fold → Resonate → Chiral → Flip → Anchor → (Seed...)

---

## Mathematical Constants

| Constant | Value | Description |
|----------|-------|-------------|
| Φ (Golden Ratio) | 1.618033988749895 | Fundamental scaling factor |
| φ (Golden Angle) | 137.507764° (2.399963 rad) | Primary rotation increment |
| Φ² | 2.618034 | Resonance frequency |
| 1/Φ | 0.618034 | Decay/contraction factor |

---

## State Definitions

### 1. SEED (Initial Emergence)
- **Energy:** 0.0 threshold (starting state)
- **Duration:** 0.5-2.0s
- **Φ Multiplier:** 0.618 (contracting/contained)
- **Chirality:** Neutral (0)
- **Fold Depth:** 0
- **Base Rotation:** 0°
- **Scale:** 0.1 → 0.3 (emerging from nothing)
- **Color:** Warm seed tones (0° hue)

**→ Transitions to SPIRAL when:** Energy ≥ 0.2, Time ≥ 0.5s, Gradient ≥ 0.1

---

### 2. SPIRAL (Expanding Outward)
- **Energy:** 0.2 threshold
- **Duration:** 2.0-5.0s
- **Φ Multiplier:** 1.618 (expanding)
- **Chirality:** Right-handed (1)
- **Fold Depth:** 0
- **Resonance:** 1.0 Hz
- **Base Rotation:** 137.5° (1× golden angle)
- **Scale:** 0.3 → 1.5 (golden spiral expansion)
- **Color:** Yellow/gold (60° hue)

**→ Transitions to FOLD when:** Energy ≥ 0.5, Time ≥ 2.0s, Phase @ Φ

---

### 3. FOLD (Turning Inward)
- **Energy:** 0.5 threshold
- **Duration:** 1.5-3.0s
- **Φ Multiplier:** 0.382 (Φ⁻², contracting)
- **Chirality:** Right-handed (1)
- **Fold Depth:** 2 (self-intersection begins)
- **Resonance:** Φ Hz
- **Base Rotation:** 275.0° (2× golden angle)
- **Scale:** 1.0 → 0.7 (turning inward)
- **Color:** Green/folding (120° hue)

**→ Transitions to RESONATE when:** Energy ≥ 0.6, Time ≥ 1.5s, Gradient ≥ 0.5

---

### 4. RESONATE (Phase-Locking)
- **Energy:** 0.6 threshold
- **Duration:** 3.0-6.0s
- **Φ Multiplier:** 1.0 (stable)
- **Chirality:** Neutral (0) - moment of balance
- **Fold Depth:** 3
- **Resonance:** Φ² = 2.618 Hz
- **Base Rotation:** 52.5° (3× golden angle)
- **Scale:** 0.8 → 1.0 (stabilizing)
- **Color:** Cyan/resonance (180° hue)

**→ Transitions to CHIRAL when:** Energy ≥ 0.8, Time ≥ 3.0s, Phase @ 3Φ

---

### 5. CHIRAL (Handedness Flip - High Energy)
- **Energy:** 0.8 threshold
- **Duration:** 0.8-2.0s
- **Φ Multiplier:** 2.618 (Φ², high energy)
- **Chirality:** Left-handed (-1) - FLIPPED
- **Fold Depth:** 4
- **Resonance:** Φ³ = 4.236 Hz
- **Base Rotation:** 327.5° (5× golden angle, Fibonacci number)
- **Scale:** 1.0 → 1.3 (expanding before flip)
- **Color:** Purple/chiral (270° hue)
- **Effect:** Glow intensity = 2× energy

**→ Transitions to FLIP when:** Energy ≥ 0.9, Time ≥ 0.8s, Phase @ 5Φ

---

### 6. FLIP (Complete Inversion - k = -1)
- **Energy:** 0.9 threshold (peak)
- **Duration:** 0.5-1.5s
- **Φ Multiplier:** -1.0 (INVERSION)
- **Chirality:** Left-handed (-1)
- **Fold Depth:** 5 (maximum complexity)
- **Resonance:** 1/Φ = 0.618 Hz (inverted)
- **Base Rotation:** 180° (π rad)
- **Scale:** 1.0 → -1.0 (passes through zero - mirror flip)
- **Color:** Magenta/inversion (300° hue)
- **Effect:** Motion blur during scale sign change

**→ Transitions to ANCHOR when:** Energy 0.3-0.5 (dissipated), Time ≥ 0.5s

---

### 7. ANCHOR (Return to Stable)
- **Energy:** 0.3 threshold
- **Duration:** 5.0-10.0s (longest stable state)
- **Φ Multiplier:** 1.0
- **Chirality:** Neutral (0) - balanced
- **Fold Depth:** 2 (reduced complexity)
- **Resonance:** 0 Hz (no oscillation)
- **Base Rotation:** 0° (returned)
- **Scale:** 0.8 (fixed)
- **Color:** Warm stable (30° hue)
- **Effect:** No glow, no blur, high opacity

**→ Transitions to SEED when:** Energy ≤ 0.3, Time ≥ 5.0s (cycle restarts)

---

## Golden Angle Applications by Transition

| Transition | Phase Alignment | Mathematical Application |
|------------|-----------------|-------------------------|
| SEED → SPIRAL | 0° | Initial offset, spiral arms at n×φ |
| SPIRAL → FOLD | 137.5° | r = a·e^(θ/tan(φ)) spiral equation |
| FOLD → RESONATE | 275.0° | Standing wave nodes at golden intervals |
| RESONATE → CHIRAL | 52.5° | Energy peaks at Φ³ |
| CHIRAL → FLIP | 327.5° | 5× golden angle (Fibonacci) alignment |
| FLIP → ANCHOR | 0° | Energy decays at rate 1/Φ |
| ANCHOR → SEED | 0° | Phase memory encoded for next cycle |

---

## Rendering Effect Specifications

### Transform Effects

| State | Rotation | Scale Behavior | Opacity |
|-------|----------|----------------|---------|
| SEED | +φ per update | 0.1→0.3 emerging | 0.3→0.6 |
| SPIRAL | +φ×Φ per update | 0.3→1.5 expanding | 0.6→0.9 |
| FOLD | +φ×Φ⁻² per update | 1.0→0.7 contracting | 0.8→0.7 |
| RESONATE | +φ per update | 0.8→1.0 stabilizing | 0.7→1.0 |
| CHIRAL | +φ×Φ² per update | 1.0→1.3 peak | 0.9→0.7 |
| FLIP | +π per update | 1.0→-1.0 INVERSION | 0.7→0.5 |
| ANCHOR | 0 (stable) | 0.8 fixed | 0.9→1.0 |

### Color Progression (HSV)

```
SEED ──────► SPIRAL ──────► FOLD ──────► RESONATE ──────► CHIRAL ──────► FLIP ──────► ANCHOR
 0°           60°          120°          180°              270°          300°          30°
Warm        Yellow        Green          Cyan             Purple       Magenta        Warm
```

### Special Effects

| State | Effect | Intensity |
|-------|--------|-----------|
| CHIRAL | Glow | 2.0 × energy |
| FLIP | Motion Blur | 0.1 × (1 - time_in_state) |
| ANCHOR | Stable stroke | 1.0 + energy × 2.0 |

---

## Python Implementation

**Files:**
- `morphogen_state_machine.py` - Core state machine implementation
- `morphogen_demo.py` - Demonstration and visualization

**Key Classes:**
- `MorphogenStateMachine` - Main state machine controller
- `GlyphState` - Complete glyph state tracking
- `RenderingSpec` - Output for graphics rendering

**Usage:**
```python
from morphogen_state_machine import MorphogenStateMachine

# Create machine
machine = MorphogenStateMachine(random_seed=42)

# Inject energy
machine.inject_energy(0.5)

# Update each frame
machine.update(dt=0.05, current_time=t)

# Get rendering spec
spec = machine.get_rendering_spec()

# Apply to graphics
apply_transform(spec.to_css())
apply_color(spec.to_rgb())
```

---

## State Transition Diagram

```
                         ┌──────────────────────────────┐
                         │                              │
                         ▼                              │
  ┌─────┐ E≥0.2       ┌────────┐ E≥0.5      ┌────────┐  │
  │SEED │ ───────────▶│ SPIRAL │ ──────────▶│  FOLD  │  │
  │ ⚫   │ t≥0.5s      │   🌀   │ t≥2.0s     │   🔄   │  │
  └──┬──┘ Φ=0°        └────────┘ Φ×1        └────┬───┘  │
     │                                            │      │
     │                                            ▼      │
     │                                         ┌────────┐│
     │            E≤0.3                        │RESONATE││
     └─────────────────────────────────────────│   🌊   ││
                                               │  Φ×3   ││
                                               └────┬───┘│
                                                    │    │
                          E≥0.8                     │    │
                                                    ▼    │
┌────────────────────────────────────────────────────────┤│
│                                                        ││
▼                                                        ││
┌────────┐  E≥0.9        ┌────────┐ E:0.3-0.5  ┌────────┘│
│ CHIRAL │ ────────────▶ │  FLIP  │ ─────────▶ │         │
│  ⚡    │ t≥0.8s        │   🔄   │ t≥0.5s     │         │
│  Φ×5   │               │  k=-1  │            │         │
└────────┘               └────────┘            │         │
    ▲                                          │         │
    └──────────────────────────────────────────┘         │
                      ANCHOR ⚓                           │
                      Φ×0                                │
                      t≥5.0s ────────────────────────────┘
```

---

## Energy Flow Dynamics

```
Energy
  1.0 ┤                              ╭─╮ CHIRAL/FLIP
      │                             ╱   ╲
  0.8 ┤                            ╱     ╲
      │                           ╱       ╲
  0.6 ┤              ╭───────────╱         ╲
      │             ╱  RESONATE            ╲
  0.5 ┤      ╭─────╱                        ╲
      │     ╱ FOLD                           ╲
  0.2 ┤────╱                                  ╲───── ANCHOR
      │ SEED                                     (stable)
  0.0 ┼──────┬──────┬──────┬──────┬──────┬──────┬──────▶ Time
      0s    2s     4s     6s     8s    10s    12s

State: SEED → SPIRAL → FOLD → RESONATE → CHIRAL → FLIP → ANCHOR
```

---

*Implementation complete and tested.*

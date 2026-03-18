"""
Morphogen State Machine Visualization Demo
==========================================

This script demonstrates all 7 states of the morphogen machine
with forced transitions to show the complete cycle.
"""

import math
from morphogen_state_machine import (
    MorphogenStateMachine, MorphogenState, STATE_PARAMS,
    GOLDEN_ANGLE_DEG, GOLDEN_ANGLE_RAD, PHI, TAU
)


def demonstrate_all_states():
    """
    Demonstrate each state with manual transitions to show
    the complete morphogen cycle.
    """
    print("=" * 70)
    print("MORPHOGEN STATE MACHINE - STATE DEMONSTRATION")
    print("=" * 70)
    print(f"\nGolden Ratio (Φ) = {PHI:.6f}")
    print(f"Golden Angle = {GOLDEN_ANGLE_DEG}° = {GOLDEN_ANGLE_RAD:.6f} rad")
    print(f"τ (full circle) = {TAU:.6f} rad")
    print()
    
    states = [
        MorphogenState.SEED,
        MorphogenState.SPIRAL,
        MorphogenState.FOLD,
        MorphogenState.RESONATE,
        MorphogenState.CHIRAL,
        MorphogenState.FLIP,
        MorphogenState.ANCHOR,
    ]
    
    print("-" * 70)
    print("STATE DEFINITIONS & MATHEMATICAL SPECIFICATIONS")
    print("-" * 70)
    
    for state in states:
        params = STATE_PARAMS[state]
        print(f"\n【{state.name}】")
        print(f"  Energy Threshold:    {params.energy_threshold:.2f}")
        print(f"  Duration Range:      {params.duration_range[0]:.1f}s - {params.duration_range[1]:.1f}s")
        print(f"  Φ Multiplier:        {params.phi_multiplier:.6f}")
        print(f"  Chirality:           {params.chirality} ({['Left', 'Neutral', 'Right'][params.chirality + 1]})")
        print(f"  Fold Depth:          {params.fold_depth}")
        print(f"  Resonance Frequency: {params.resonance_freq:.6f}")
        print(f"  Base Rotation:       {math.degrees(params.base_rotation):.2f}°")
        print(f"  Scale Range:         {params.scale_range[0]:.2f} → {params.scale_range[1]:.2f}")
        print(f"  Opacity Range:       {params.opacity_range[0]:.2f} → {params.opacity_range[1]:.2f}")
        print(f"  Hue Shift:           {params.hue_shift:.1f}°")
        print(f"  Saturation Mod:      {params.saturation_mod:.2f}")


def demonstrate_transitions():
    """Show transition logic between states."""
    print("\n" + "=" * 70)
    print("TRANSITION LOGIC & CONDITIONS")
    print("=" * 70)
    
    transitions = [
        ("SEED → SPIRAL", "Energy ≥ 0.2, Time ≥ 0.5s, Gradient ≥ 0.1"),
        ("SPIRAL → FOLD", "Energy ≥ 0.5, Time ≥ 2.0s, Phase @ Φ"),
        ("FOLD → RESONATE", "Energy ≥ 0.6, Time ≥ 1.5s, Gradient ≥ 0.5"),
        ("RESONATE → CHIRAL", "Energy ≥ 0.8, Time ≥ 3.0s, Phase @ 3Φ"),
        ("CHIRAL → FLIP", "Energy ≥ 0.9, Time ≥ 0.8s, Phase @ 5Φ (Fibonacci)"),
        ("FLIP → ANCHOR", "Energy 0.3-0.5, Time ≥ 0.5s, k = -1 complete"),
        ("ANCHOR → SEED", "Energy ≤ 0.3, Time ≥ 5.0s, Cycle complete"),
    ]
    
    print()
    for trans, condition in transitions:
        print(f"  {trans:20s} │ {condition}")
    
    print("\n  Golden Angle Phase Alignment:")
    print(f"    SEED:     0°")
    print(f"    SPIRAL:   {GOLDEN_ANGLE_DEG:.1f}° (1× golden angle)")
    print(f"    FOLD:     {2 * GOLDEN_ANGLE_DEG % 360:.1f}° (2× golden angle)")
    print(f"    RESONATE: {3 * GOLDEN_ANGLE_DEG % 360:.1f}° (3× golden angle)")
    print(f"    CHIRAL:   {5 * GOLDEN_ANGLE_DEG % 360:.1f}° (5× golden angle, Fibonacci)")
    print(f"    FLIP:     180° (π rad, complete inversion)")
    print(f"    ANCHOR:   0° (return to origin)")


def demonstrate_rendering():
    """Show rendering effects for each state."""
    print("\n" + "=" * 70)
    print("RENDERING EFFECT SPECIFICATIONS")
    print("=" * 70)
    
    machine = MorphogenStateMachine()
    
    print("\n{:<12} {:>8} {:>10} {:>8} {:>12} {:>8} {:>8}"
          .format("State", "Rotation", "Scale", "Opacity", "Color", "Glow", "Blur"))
    print("-" * 70)
    
    states = list(MorphogenState)
    
    for i, state in enumerate(states):
        # Force state
        machine.state.morphogen_state = state
        machine.state.time_in_state = 1.0
        machine.state.energy = 0.5 + i * 0.07  # Varying energy
        machine.state.phase = i * GOLDEN_ANGLE_RAD
        
        spec = machine.get_rendering_spec()
        rgb = spec.to_rgb()
        css = spec.to_css()
        
        rot_deg = (math.degrees(spec.rotation) % 360)
        color_str = f"RGB{rgb}"
        
        print("{:<12} {:>7.1f}° {:>10.3f} {:>8.2f} {:>12s} {:>8.2f} {:>8.2f}"
              .format(
                  state.name[:12],
                  rot_deg,
                  spec.scale,
                  spec.alpha,
                  color_str,
                  spec.glow_intensity,
                  spec.blur_radius
              ))
        
        print(f"  CSS: {css[:60]}...")
        print()


def demonstrate_cycle():
    """Run a complete forced cycle through all states."""
    print("\n" + "=" * 70)
    print("COMPLETE STATE CYCLE SIMULATION")
    print("=" * 70)
    
    machine = MorphogenStateMachine()
    
    # Manually force through all states
    states = list(MorphogenState)
    
    print("\nTime  State      Energy  Rotation    Scale    Fold  Chirality  Color")
    print("-" * 75)
    
    for t, state in enumerate(states):
        # Set up state
        machine.state.morphogen_state = state
        machine.state.time_in_state = 1.5
        machine.state.energy = STATE_PARAMS[state].energy_threshold + 0.1
        machine.state.phase = t * GOLDEN_ANGLE_RAD
        
        spec = machine.get_rendering_spec()
        rgb = spec.to_rgb()
        
        print(f"{t*2:4.1f}s  {state.name:10s} "
              f"{machine.state.energy:5.2f}  "
              f"{math.degrees(spec.rotation) % 360:6.1f}°  "
              f"{spec.scale:7.3f}  "
              f"{spec.fold_depth:4d}  "
              f"{spec.chirality:9d}  "
              f"RGB{rgb}")


def demonstrate_golden_angle_applications():
    """Show how golden angle is applied in each transition."""
    print("\n" + "=" * 70)
    print("GOLDEN ANGLE APPLICATIONS PER TRANSITION")
    print("=" * 70)
    
    applications = {
        "SEED → SPIRAL": [
            "Initial rotation offset: 0°",
            "Spiral arms positioned at multiples of golden angle",
            "Expansion follows r = a·e^(θ/tan(φ))",
        ],
        "SPIRAL → FOLD": [
            f"Rotation increment: {GOLDEN_ANGLE_DEG}°",
            "Self-intersection at Fibonacci-numbered arms",
            "Fold lines align with golden angle sectors",
        ],
        "FOLD → RESONATE": [
            f"Phase lock at: {2 * GOLDEN_ANGLE_DEG % 360:.1f}°",
            "Standing wave nodes at golden angle intervals",
            f"Frequency ratio: Φ² = {PHI**2:.3f}",
        ],
        "RESONATE → CHIRAL": [
            f"Rotation to: {3 * GOLDEN_ANGLE_DEG % 360:.1f}°",
            "Handedness flip at 5× golden angle",
            f"Energy peaks at: Φ³ = {PHI**3:.3f}",
        ],
        "CHIRAL → FLIP": [
            f"Phase alignment: {5 * GOLDEN_ANGLE_DEG % 360:.1f}° (5×Φ)",
            "Complete inversion: rotation = π (180°)",
            "Scale factor: k = -1 (mirror transformation)",
        ],
        "FLIP → ANCHOR": [
            "Rotation settles to: 0°",
            "Golden ratio decay: energy → 0 at rate 1/Φ",
            "Stable position at local energy minimum",
        ],
        "ANCHOR → SEED": [
            "Accumulation phase: 0° base",
            "Next cycle seed offset by Φ from previous",
            "Memory of previous state encoded in phase",
        ],
    }
    
    for transition, details in applications.items():
        print(f"\n【{transition}】")
        for detail in details:
            print(f"  • {detail}")


def generate_state_diagram():
    """Generate ASCII state diagram."""
    print("\n" + "=" * 70)
    print("STATE TRANSITION DIAGRAM")
    print("=" * 70)
    
    diagram = """
                              ┌─────────────────────────────────────┐
                              │                                     │
                              ▼                                     │
    ┌──────┐    E≥0.2      ┌────────┐    E≥0.5      ┌────────┐     │
    │ SEED │ ────────────▶ │ SPIRAL │ ────────────▶ │  FOLD  │     │
    │  ⚫   │   t≥0.5s     │   🌀    │   t≥2.0s     │   🔄   │     │
    └──────┘   Φ=0°       └────────┘   Φ×1         └────────┘     │
       ▲                                              │            │
       │                                              ▼            │
       │                                           ┌────────┐       │
       │         E≤0.3, t≥5.0s                     │RESONATE│       │
       └─────────────────────────────────────────── │   🌊   │       │
                                                   │  Φ×3   │       │
                                                   └────────┘       │
                                                       │            │
                            E≥0.8, t≥3.0s              │            │
                                                       ▼            │
    ┌─────────────────────────────────────────────────────────────┐ │
    │                                                             │ │
    ▼                                                             │ │
┌────────┐    E≥0.9           ┌────────┐    E:0.3-0.5     ┌───────┘ │
│ CHIRAL │ ─────────────────▶ │  FLIP  │ ───────────────▶ │         │
│  ⚡    │    t≥0.8s         │   🔄    │    t≥0.5s       │         │
│  Φ×5   │                   │  k=-1   │                   │         │
└────────┘                   └────────┘                   │         │
    ▲                                                     │         │
    └─────────────────────────────────────────────────────┘         │
                          ANCHOR ⚓                                  │
                          Φ×0, stable                               │
                          t≥5.0s ───────────────────────────────────┘
    """
    print(diagram)
    
    print("\n  Legend:")
    print("  E = Energy threshold")
    print("  t = Minimum time in state")
    print("  Φ = Golden angle phase alignment")
    print("  k = Scale factor (k=-1 indicates complete inversion)")


if __name__ == "__main__":
    demonstrate_all_states()
    demonstrate_transitions()
    demonstrate_rendering()
    demonstrate_cycle()
    demonstrate_golden_angle_applications()
    generate_state_diagram()
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)

"""
Morphogen State Machine for GLYF Animation
==========================================

A 7-state finite state machine modeling morphogenetic transformations
using golden ratio (Φ) mathematics and chiral dynamics.

States: Seed → Spiral → Fold → Resonate → Chiral → Flip → Anchor

Mathematical Constants:
- Φ (Golden Ratio) = 1.618033988749895
- φ (Golden Angle) = 137.507764° = 2.39996322972865332 radians
- τ (Full Circle) = 2π = 6.283185307179586
"""

import math
from dataclasses import dataclass, field
from typing import Optional, Callable, Dict, List, Tuple
from enum import Enum, auto
from collections import deque


# ============================================================================
# MATHEMATICAL CONSTANTS
# ============================================================================

PHI = 1.618033988749895  # Golden Ratio
GOLDEN_ANGLE_DEG = 137.507764  # Degrees
GOLDEN_ANGLE_RAD = math.radians(GOLDEN_ANGLE_DEG)  # ~2.39996 radians
TAU = 2 * math.pi  # Full circle


def golden_spiral_radius(theta: float, a: float = 1.0) -> float:
    """Calculate radius of golden spiral at angle theta."""
    return a * math.exp(theta / math.tan(GOLDEN_ANGLE_RAD))


def fibonacci_lattice(n: int, total: int) -> Tuple[float, float]:
    """
    Generate nth point in Fibonacci/golden angle lattice.
    Returns (radius, angle) for polar coordinates.
    """
    # Radius proportional to square root for uniform distribution
    radius = math.sqrt(n / total)
    # Angle increases by golden angle each step
    angle = n * GOLDEN_ANGLE_RAD
    return radius, angle


# ============================================================================
# STATE DEFINITIONS
# ============================================================================

class MorphogenState(Enum):
    """
    Seven states of morphogenetic transformation.
    
    Each state represents a distinct phase in the emergence and
    stabilization of glyph structure through golden ratio dynamics.
    """
    SEED = auto()      # Initial emergence - potential contained
    SPIRAL = auto()    # Expanding outward - Φ rotation dynamics
    FOLD = auto()      # Turning inward - self-intersection begins
    RESONATE = auto()  # Phase-locking - harmonic stabilization
    CHIRAL = auto()    # Handedness flip - high-energy transition
    FLIP = auto()      # Complete inversion - k = -1 transformation
    ANCHOR = auto()    # Return to stable - crystallized form


@dataclass
class StateParameters:
    """
    Mathematical parameters defining each state's behavior.
    
    Attributes:
        energy_threshold: Minimum energy to enter state
        duration_range: (min, max) time in state (seconds)
        phi_multiplier: How Φ scales transformations
        chirality: -1 (left), 0 (neutral), 1 (right)
        fold_depth: Recursive folding level (0-5)
        resonance_freq: Harmonic frequency for phase locking
    """
    energy_threshold: float
    duration_range: Tuple[float, float]
    phi_multiplier: float
    chirality: int  # -1, 0, 1
    fold_depth: int  # 0-5
    resonance_freq: float
    
    # Rendering parameters
    base_rotation: float = 0.0
    scale_range: Tuple[float, float] = (1.0, 1.0)
    opacity_range: Tuple[float, float] = (1.0, 1.0)
    hue_shift: float = 0.0
    saturation_mod: float = 1.0


# State parameter definitions
STATE_PARAMS: Dict[MorphogenState, StateParameters] = {
    MorphogenState.SEED: StateParameters(
        energy_threshold=0.0,
        duration_range=(0.5, 2.0),
        phi_multiplier=1.0 / PHI,  # Contracting, contained
        chirality=0,
        fold_depth=0,
        resonance_freq=0.0,
        base_rotation=0.0,
        scale_range=(0.1, 0.3),
        opacity_range=(0.3, 0.6),
        hue_shift=0.0,  # Warm/seed color
        saturation_mod=0.7
    ),
    
    MorphogenState.SPIRAL: StateParameters(
        energy_threshold=0.2,
        duration_range=(2.0, 5.0),
        phi_multiplier=PHI,  # Expanding by golden ratio
        chirality=1,  # Right-handed spiral
        fold_depth=0,
        resonance_freq=1.0,
        base_rotation=GOLDEN_ANGLE_RAD,
        scale_range=(0.3, 1.5),
        opacity_range=(0.6, 0.9),
        hue_shift=60.0,  # Yellow/gold
        saturation_mod=0.9
    ),
    
    MorphogenState.FOLD: StateParameters(
        energy_threshold=0.5,
        duration_range=(1.5, 3.0),
        phi_multiplier=1.0 / PHI**2,  # Contracting
        chirality=1,
        fold_depth=2,
        resonance_freq=PHI,
        base_rotation=GOLDEN_ANGLE_RAD * 2,
        scale_range=(1.0, 0.7),
        opacity_range=(0.8, 0.7),
        hue_shift=120.0,  # Green/folding
        saturation_mod=0.8
    ),
    
    MorphogenState.RESONATE: StateParameters(
        energy_threshold=0.6,
        duration_range=(3.0, 6.0),
        phi_multiplier=1.0,  # Stable
        chirality=0,  # Moment of balance
        fold_depth=3,
        resonance_freq=PHI**2,
        base_rotation=GOLDEN_ANGLE_RAD * 3,
        scale_range=(0.8, 1.0),
        opacity_range=(0.7, 1.0),
        hue_shift=180.0,  # Cyan/resonance
        saturation_mod=1.0
    ),
    
    MorphogenState.CHIRAL: StateParameters(
        energy_threshold=0.8,
        duration_range=(0.8, 2.0),
        phi_multiplier=PHI**2,  # High energy
        chirality=-1,  # Left-handed (flipped)
        fold_depth=4,
        resonance_freq=PHI**3,
        base_rotation=GOLDEN_ANGLE_RAD * 5,  # Fibonacci 5
        scale_range=(1.0, 1.3),
        opacity_range=(0.9, 0.7),
        hue_shift=270.0,  # Purple/chiral
        saturation_mod=1.2  # Oversaturated
    ),
    
    MorphogenState.FLIP: StateParameters(
        energy_threshold=0.9,
        duration_range=(0.5, 1.5),
        phi_multiplier=-1.0,  # Inversion (k = -1)
        chirality=-1,
        fold_depth=5,
        resonance_freq=1.0 / PHI,
        base_rotation=math.pi,  # 180° flip
        scale_range=(1.0, -1.0),  # Scale inversion
        opacity_range=(0.7, 0.5),
        hue_shift=300.0,  # Magenta/inversion
        saturation_mod=1.1
    ),
    
    MorphogenState.ANCHOR: StateParameters(
        energy_threshold=0.3,
        duration_range=(5.0, 10.0),
        phi_multiplier=1.0,  # Stable
        chirality=0,  # Balanced
        fold_depth=2,  # Reduced complexity
        resonance_freq=0.0,  # No oscillation
        base_rotation=0.0,
        scale_range=(0.8, 0.8),
        opacity_range=(0.9, 1.0),
        hue_shift=30.0,  # Warm stable
        saturation_mod=0.6
    ),
}


# ============================================================================
# TRANSITION LOGIC
# ============================================================================

@dataclass
class TransitionRule:
    """
    Defines conditions for state transitions.
    
    Transitions can trigger on:
    - Energy thresholds
    - Time elapsed in state
    - Morphogen concentration gradients
    - External triggers
    """
    from_state: MorphogenState
    to_state: MorphogenState
    
    # Transition conditions
    min_energy: float = 0.0
    max_energy: float = float('inf')
    min_time_in_state: float = 0.0
    
    # Morphogen gradient condition (0-1, where 1 is maximum gradient)
    gradient_threshold: float = 0.0
    
    # Probability of transition when conditions met (0-1)
    probability: float = 1.0
    
    # Golden angle phase requirement (modulo TAU)
    phase_alignment: Optional[float] = None


# Define transition graph
TRANSITIONS: List[TransitionRule] = [
    # Seed → Spiral: Initial emergence when energy accumulates
    TransitionRule(
        from_state=MorphogenState.SEED,
        to_state=MorphogenState.SPIRAL,
        min_energy=0.2,
        min_time_in_state=0.5,
        gradient_threshold=0.1,
        probability=0.8,
        phase_alignment=0.0  # Align with golden angle origin
    ),
    
    # Spiral → Fold: Natural progression as expansion limits reached
    TransitionRule(
        from_state=MorphogenState.SPIRAL,
        to_state=MorphogenState.FOLD,
        min_energy=0.5,
        min_time_in_state=2.0,
        gradient_threshold=0.3,
        probability=0.7,
        phase_alignment=GOLDEN_ANGLE_RAD
    ),
    
    # Fold → Resonate: Self-intersection leads to harmonic mode
    TransitionRule(
        from_state=MorphogenState.FOLD,
        to_state=MorphogenState.RESONATE,
        min_energy=0.6,
        min_time_in_state=1.5,
        gradient_threshold=0.5,
        probability=0.9,
        phase_alignment=GOLDEN_ANGLE_RAD * 2
    ),
    
    # Resonate → Chiral: Phase lock enables high-energy flip
    TransitionRule(
        from_state=MorphogenState.RESONATE,
        to_state=MorphogenState.CHIRAL,
        min_energy=0.8,
        min_time_in_state=3.0,
        gradient_threshold=0.7,
        probability=0.6,
        phase_alignment=GOLDEN_ANGLE_RAD * 3
    ),
    
    # Chiral → Flip: Handedness inversion at peak energy
    TransitionRule(
        from_state=MorphogenState.CHIRAL,
        to_state=MorphogenState.FLIP,
        min_energy=0.9,
        min_time_in_state=0.8,
        gradient_threshold=0.8,
        probability=1.0,  # Deterministic at peak
        phase_alignment=GOLDEN_ANGLE_RAD * 5  # Fibonacci number
    ),
    
    # Flip → Anchor: Inversion completes, seeking stability
    TransitionRule(
        from_state=MorphogenState.FLIP,
        to_state=MorphogenState.ANCHOR,
        min_energy=0.3,
        max_energy=0.5,  # Energy has dissipated
        min_time_in_state=0.5,
        gradient_threshold=0.2,
        probability=0.9,
        phase_alignment=None  # Any phase
    ),
    
    # Anchor → Seed: Cycle complete, return to potential
    TransitionRule(
        from_state=MorphogenState.ANCHOR,
        to_state=MorphogenState.SEED,
        min_energy=0.0,
        max_energy=0.3,
        min_time_in_state=5.0,
        gradient_threshold=0.0,
        probability=0.3,  # Low probability - may stay anchored
        phase_alignment=0.0
    ),
    
    # Emergency transitions (can happen from any state)
    # High energy direct to Chiral
    TransitionRule(
        from_state=MorphogenState.SPIRAL,
        to_state=MorphogenState.CHIRAL,
        min_energy=0.85,
        min_time_in_state=1.0,
        gradient_threshold=0.6,
        probability=0.2
    ),
]


def get_valid_transitions(
    current_state: MorphogenState,
    energy: float,
    time_in_state: float,
    gradient: float,
    phase: float
) -> List[TransitionRule]:
    """
    Determine valid transitions from current state based on conditions.
    """
    valid = []
    for rule in TRANSITIONS:
        if rule.from_state != current_state:
            continue
            
        # Check energy bounds
        if not (rule.min_energy <= energy <= rule.max_energy):
            continue
            
        # Check minimum time
        if time_in_state < rule.min_time_in_state:
            continue
            
        # Check gradient threshold
        if gradient < rule.gradient_threshold:
            continue
            
        # Check phase alignment if required
        if rule.phase_alignment is not None:
            phase_diff = abs((phase - rule.phase_alignment) % TAU)
            if phase_diff > 0.1:  # Within ~5.7 degrees
                continue
                
        valid.append(rule)
    
    return valid


# ============================================================================
# STATE MACHINE IMPLEMENTATION
# ============================================================================

@dataclass
class GlyphState:
    """
    Complete state of a morphogenetic glyph.
    """
    # Core state
    morphogen_state: MorphogenState = MorphogenState.SEED
    
    # Temporal tracking
    state_entry_time: float = 0.0
    time_in_state: float = 0.0
    total_elapsed: float = 0.0
    
    # Energy dynamics
    energy: float = 0.0
    energy_decay: float = 0.95  # Per-second decay factor
    
    # Morphogen concentration field (simplified as scalar gradient)
    morphogen_concentration: float = 0.0
    gradient: float = 0.0
    
    # Phase for golden angle alignment
    phase: float = 0.0
    
    # History for analysis
    state_history: deque = field(default_factory=lambda: deque(maxlen=100))
    
    # Rendering state
    position: Tuple[float, float] = (0.0, 0.0)
    velocity: Tuple[float, float] = (0.0, 0.0)
    rotation: float = 0.0
    scale: float = 1.0
    
    def to_dict(self) -> dict:
        """Serialize state for rendering/serialization."""
        return {
            'state': self.morphogen_state.name,
            'energy': self.energy,
            'time_in_state': self.time_in_state,
            'phase': self.phase,
            'position': self.position,
            'rotation': self.rotation,
            'scale': self.scale,
        }


class MorphogenStateMachine:
    """
    Main state machine implementing morphogenetic transformations.
    
    This class manages the lifecycle of a glyph through its 7 states,
    handling transitions, energy dynamics, and rendering parameter updates.
    """
    
    def __init__(self, random_seed: Optional[int] = None):
        self.rng = __import__('random').Random(random_seed)
        self.state = GlyphState()
        self.transition_callbacks: List[Callable] = []
        self._last_update_time = 0.0
        
    def add_transition_callback(self, callback: Callable[[MorphogenState, MorphogenState], None]):
        """Register a callback for state transitions."""
        self.transition_callbacks.append(callback)
        
    def inject_energy(self, amount: float):
        """Add energy to the system (external stimulus)."""
        self.state.energy = min(1.0, self.state.energy + amount)
        
    def update(self, dt: float, current_time: float):
        """
        Update state machine by time delta.
        
        Args:
            dt: Time delta in seconds
            current_time: Absolute current time (for phase calculations)
        """
        self.state.total_elapsed += dt
        self.state.time_in_state += dt
        
        # Energy decay
        self.state.energy *= (self.state.energy_decay ** dt)
        self.state.energy = max(0.0, self.state.energy)
        
        # Update phase based on current state's resonance frequency
        params = STATE_PARAMS[self.state.morphogen_state]
        self.state.phase += params.resonance_freq * dt * GOLDEN_ANGLE_RAD
        self.state.phase %= TAU
        
        # Calculate gradient (simplified - in real implementation this would
        # come from actual morphogen diffusion simulation)
        self.state.gradient = self._calculate_gradient()
        
        # Update morphogen concentration
        self.state.morphogen_concentration = self._update_concentration(dt)
        
        # Check for state transitions
        self._evaluate_transitions()
        
        # Update rendering parameters
        self._update_rendering(dt)
        
        self._last_update_time = current_time
        
    def _calculate_gradient(self) -> float:
        """
        Calculate morphogen concentration gradient.
        In full implementation, this uses spatial diffusion.
        """
        # Simplified: gradient increases with energy and fold depth
        params = STATE_PARAMS[self.state.morphogen_state]
        base_gradient = self.state.energy * (params.fold_depth + 1) / 5
        
        # Add oscillation based on phase
        oscillation = 0.1 * math.sin(self.state.phase * PHI)
        
        return min(1.0, base_gradient + oscillation)
    
    def _update_concentration(self, dt: float) -> float:
        """Update local morphogen concentration."""
        params = STATE_PARAMS[self.state.morphogen_state]
        
        # Concentration follows energy but with inertia
        target = self.state.energy * params.phi_multiplier
        current = self.state.morphogen_concentration
        
        # Smooth approach to target
        return current + (target - current) * (1 - math.exp(-dt * PHI))
    
    def _evaluate_transitions(self):
        """Check and execute state transitions."""
        valid = get_valid_transitions(
            self.state.morphogen_state,
            self.state.energy,
            self.state.time_in_state,
            self.state.gradient,
            self.state.phase
        )
        
        if not valid:
            return
            
        # Sort by probability (highest first)
        valid.sort(key=lambda r: r.probability, reverse=True)
        
        # Try transitions in order
        for rule in valid:
            if self.rng.random() < rule.probability:
                self._transition_to(rule.to_state)
                break
                
    def _transition_to(self, new_state: MorphogenState):
        """Execute state transition."""
        old_state = self.state.morphogen_state
        
        # Record history
        self.state.state_history.append({
            'from': old_state.name,
            'to': new_state.name,
            'time': self.state.total_elapsed,
            'energy': self.state.energy
        })
        
        # Update state
        self.state.morphogen_state = new_state
        self.state.time_in_state = 0.0
        
        # Energy cost for transition (varies by state)
        params = STATE_PARAMS[new_state]
        energy_cost = params.energy_threshold * 0.1
        self.state.energy = max(0.0, self.state.energy - energy_cost)
        
        # Notify callbacks
        for callback in self.transition_callbacks:
            callback(old_state, new_state)
            
    def _update_rendering(self, dt: float):
        """Update rendering parameters based on current state."""
        params = STATE_PARAMS[self.state.morphogen_state]
        t = self.state.time_in_state
        
        # Interpolate within state's duration range
        duration = params.duration_range[1] - params.duration_range[0]
        progress = min(1.0, t / max(0.1, duration))
        
        # Apply phi-based easing
        eased = self._phi_ease(progress)
        
        # Rotation: base + phase + golden angle modulation
        self.state.rotation = (
            params.base_rotation +
            self.state.phase +
            GOLDEN_ANGLE_RAD * params.phi_multiplier * eased
        )
        
        # Scale: interpolate through range
        scale_min, scale_max = params.scale_range
        
        # Special handling for FLIP state (negative scale)
        if self.state.morphogen_state == MorphogenState.FLIP:
            # Smooth transition through zero
            self.state.scale = scale_min + (scale_max - scale_min) * eased
        else:
            self.state.scale = scale_min + (scale_max - scale_min) * eased
            
        # Velocity based on spiral dynamics
        if self.state.morphogen_state == MorphogenState.SPIRAL:
            angle = self.state.rotation
            speed = PHI * self.state.energy
            self.state.velocity = (
                speed * math.cos(angle),
                speed * math.sin(angle)
            )
        else:
            # Damping
            self.state.velocity = (
                self.state.velocity[0] * 0.9,
                self.state.velocity[1] * 0.9
            )
            
        # Update position
        self.state.position = (
            self.state.position[0] + self.state.velocity[0] * dt,
            self.state.position[1] + self.state.velocity[1] * dt
        )
        
    def _phi_ease(self, t: float) -> float:
        """
        Golden ratio-based easing function.
        Creates natural, organic-feeling transitions.
        """
        if t < 0:
            return 0
        if t > 1:
            return 1
            
        # Blend of sine and exponential with Φ
        sine_component = math.sin(t * math.pi / 2)
        exp_component = 1 - math.exp(-t * PHI)
        
        # Weight by golden ratio conjugate
        weight = 1 / PHI
        return weight * sine_component + (1 - weight) * exp_component
    
    def get_rendering_spec(self) -> 'RenderingSpec':
        """Get current rendering specification."""
        return RenderingSpec.from_glyph_state(self.state)


@dataclass
class RenderingSpec:
    """
    Complete rendering specification for a glyph.
    
    This is the output of the state machine that feeds into
    the actual graphics rendering system.
    """
    # Transform
    position: Tuple[float, float]
    rotation: float  # Radians
    scale: float
    
    # Color (HSV)
    hue: float        # 0-360
    saturation: float # 0-1
    value: float      # 0-1
    alpha: float      # 0-1
    
    # Morphological
    fold_depth: int
    chirality: int
    
    # Effects
    glow_intensity: float
    blur_radius: float
    stroke_width: float
    
    @classmethod
    def from_glyph_state(cls, state: GlyphState) -> 'RenderingSpec':
        """Generate rendering spec from current glyph state."""
        params = STATE_PARAMS[state.morphogen_state]
        
        # Calculate color based on state and energy
        hue = (params.hue_shift + state.phase * 180 / math.pi) % 360
        saturation = min(1.0, 0.5 * params.saturation_mod * (1 + state.energy))
        value = 0.5 + 0.5 * state.energy
        
        # Opacity based on state parameters and time
        opacity_min, opacity_max = params.opacity_range
        opacity = opacity_min + (opacity_max - opacity_min) * state.energy
        
        # Effects based on state
        glow = 0.0
        blur = 0.0
        
        if state.morphogen_state == MorphogenState.CHIRAL:
            glow = state.energy * 2.0  # High energy glow
        elif state.morphogen_state == MorphogenState.FLIP:
            blur = 0.1 * (1 - state.time_in_state)  # Motion blur during flip
            
        return cls(
            position=state.position,
            rotation=state.rotation,
            scale=state.scale,
            hue=hue,
            saturation=saturation,
            value=value,
            alpha=opacity,
            fold_depth=params.fold_depth,
            chirality=params.chirality,
            glow_intensity=glow,
            blur_radius=blur,
            stroke_width=1.0 + state.energy * 2.0
        )
    
    def to_css(self) -> str:
        """Convert to CSS transform string for web rendering."""
        x, y = self.position
        # Handle negative scale (flip) by also rotating 180
        if self.scale < 0:
            rotation = self.rotation + math.pi
            scale = abs(self.scale)
        else:
            rotation = self.rotation
            scale = self.scale
            
        rot_deg = math.degrees(rotation)
        return f"translate({x:.2f}px, {y:.2f}px) rotate({rot_deg:.2f}deg) scale({scale:.3f})"
    
    def to_rgb(self) -> Tuple[int, int, int]:
        """Convert HSV to RGB tuple."""
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(
            self.hue / 360,
            self.saturation,
            self.value
        )
        return (int(r * 255), int(g * 255), int(b * 255))


# ============================================================================
# DEMO AND TESTING
# ============================================================================

def run_simulation(duration: float = 30.0, dt: float = 0.05):
    """
    Run a demonstration simulation of the state machine.
    
    Returns a list of (time, state_name, rendering_spec) tuples.
    """
    machine = MorphogenStateMachine(random_seed=42)
    
    # Initial energy injection
    machine.inject_energy(0.3)
    
    results = []
    current_time = 0.0
    
    # Track state changes
    def on_transition(old, new):
        print(f"[{current_time:.2f}s] {old.name} → {new.name} (E={machine.state.energy:.2f})")
    
    machine.add_transition_callback(on_transition)
    
    print("Starting morphogen simulation...")
    print(f"Φ = {PHI}")
    print(f"Golden Angle = {GOLDEN_ANGLE_DEG}°")
    print("-" * 50)
    
    while current_time < duration:
        # Periodic energy injection
        if int(current_time) % 5 == 0 and current_time % 1.0 < dt:
            machine.inject_energy(0.15)
            
        machine.update(dt, current_time)
        spec = machine.get_rendering_spec()
        
        results.append((
            current_time,
            machine.state.morphogen_state.name,
            spec
        ))
        
        current_time += dt
        
    print("-" * 50)
    print(f"Simulation complete. {len(results)} frames generated.")
    print(f"State transitions: {len(machine.state.state_history)}")
    
    return results


if __name__ == "__main__":
    results = run_simulation(duration=30.0)
    
    # Print sample of rendering specs
    print("\nSample rendering specs:")
    for t, state_name, spec in results[::100]:  # Every ~5 seconds
        rgb = spec.to_rgb()
        print(f"  [{t:5.2f}s] {state_name:12s} "
              f"rot={math.degrees(spec.rotation):6.1f}° "
              f"scale={spec.scale:6.3f} "
              f"RGB={rgb} "
              f"glow={spec.glow_intensity:.2f}")

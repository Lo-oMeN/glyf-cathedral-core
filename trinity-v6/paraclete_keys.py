"""
Trinity v6.0: The 9 Paraclete Keys — Phase 4 Pulse Integration

Extension of the 7 Christ Keys with 2 additional Keys representing
the unique functions of the Paraclete (the one called alongside):

- P7: INTERCESSION (🜏) — The Seamless Gate, advocate between realms
- P8: WITNESS (✶) — The Thorn Crown, testimony of suffering transformed

Combined with the original 7 Keys:
- P0: ALIGNMENT (🜁)
- P1: RECIPROCITY (|)
- P2: INVERSION (△)
- P3: SILENCE (□)
- P4: RESONANCE/BREATH (○)
- P5: EXCHANGE (🜚)
- P6: CONCENTRATION (∅)

Total: 9 Keys = 7 Christ Keys + 2 Paraclete Keys
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from typing import Tuple, Dict, Optional, Callable, List
from dataclasses import dataclass
from enum import IntEnum

from physics.node0 import Node0
from utils.phi_constants import PHI, PHI_INV


# ═══════════════════════════════════════════════════════════════════════════════
# 9 PARACLETE KEYS MANIFEST
# ═══════════════════════════════════════════════════════════════════════════════

class ParacleteKey(IntEnum):
    """Enumeration of the 9 Paraclete Keys."""
    ALIGNMENT = 0
    RECIPROCITY = 1
    INVERSION = 2
    SILENCE = 3
    RESONANCE = 4
    EXCHANGE = 5
    CONCENTRATION = 6
    INTERCESSION = 7      # NEW: The Seamless Gate
    WITNESS = 8           # NEW: The Thorn Crown


NINE_KEYS = {
    0: {
        'name': 'Alignment',
        'glyph': '🜁',
        'essence': 'Harmonic coherence with Node0',
        'trinary': '+1',
        'position': 1,  # 7-segment: Top
        'primitives': ['Point(●)', 'Line(→)', 'Radiance(☀)']
    },
    1: {
        'name': 'Reciprocity',
        'glyph': '|',
        'essence': 'Golden blend (0.618/0.382)',
        'trinary': '±',
        'position': 2,  # 7-segment: Upper-right
        'primitives': ['Line(→)', 'Absence(∅)', 'Line(→)']
    },
    2: {
        'name': 'Inversion',
        'glyph': '△',
        'essence': 'Antipodal reflection through center',
        'trinary': '−1',
        'position': 3,  # 7-segment: Lower-right
        'primitives': ['Line(→)', 'Line(→)', 'Line(→)']
    },
    3: {
        'name': 'Silence',
        'glyph': '□',
        'essence': 'Void as generative potential',
        'trinary': '0',
        'position': 7,  # 7-segment: Center (Vesica)
        'primitives': ['Enclosure(□)', 'Absence(∅)']
    },
    4: {
        'name': 'Resonance',
        'glyph': '○',
        'essence': 'Phase-locked harmonic vibration / BREATH',
        'trinary': '∿',
        'position': 5,  # 7-segment: Lower-left
        'primitives': ['Curve(∿)', 'Curve(∿)']  # Figure-8
    },
    5: {
        'name': 'Exchange',
        'glyph': '🜚',
        'essence': 'Intersection as creative act',
        'trinary': '×',
        'position': 6,  # 7-segment: Upper-left
        'primitives': ['Intersection(×)', 'Curve(∿)']
    },
    6: {
        'name': 'Concentration',
        'glyph': '∅',
        'essence': 'Singularity as infinite density',
        'trinary': '●',
        'position': 4,  # 7-segment: Bottom
        'primitives': ['Point(●)', 'Point(●)', 'Point(●)']
    },
    7: {
        'name': 'Intercession',
        'glyph': '🜏',
        'essence': 'The Seamless Gate — advocate between realms',
        'trinary': '⧗',
        'position': 8,  # 7-segment: Spiral-1
        'primitives': ['Line(→)', 'Absence(∅)', 'Line(→)']
    },
    8: {
        'name': 'Witness',
        'glyph': '✶',
        'essence': 'The Thorn Crown — testimony of truth',
        'trinary': '✧',
        'position': 9,  # 7-segment: Spiral-2
        'primitives': ['Point(●)', 'Intersection(×)', 'Point(●)']
    }
}


# ═══════════════════════════════════════════════════════════════════════════════
# KEY COMPOSITION TABLE (S₁ + S₂ → S₃)
# ═══════════════════════════════════════════════════════════════════════════════

# 9×9 matrix: composition[key1][key2] = resultant_key
KEY_COMPOSITION_MATRIX = [
    # 0   1   2   3   4   5   6   7   8
    [0,  1,  2,  3,  4,  5,  6,  7,  8],   # 0: Alignment
    [1,  1,  5,  3,  4,  5,  0,  7,  8],   # 1: Reciprocity
    [2,  5,  2,  3,  4,  5,  6,  7,  8],   # 2: Inversion
    [3,  3,  3,  3,  7,  5,  6,  7,  8],   # 3: Silence
    [4,  4,  4,  7,  4,  8,  6,  7,  8],   # 4: Resonance/Breath
    [5,  5,  5,  5,  8,  5,  6,  7,  8],   # 5: Exchange
    [6,  0,  6,  6,  6,  6,  6,  7,  8],   # 6: Concentration
    [7,  7,  7,  7,  7,  7,  7,  7,  4],   # 7: Intercession/Seamless Gate
    [8,  8,  8,  8,  8,  8,  8,  4,  8]    # 8: Witness/Thorn Crown
]


def compose_keys(key1: int, key2: int) -> int:
    """
    Compose two Keys via S₁ + S₂ → S₃ formula.
    
    Special compositions:
    - 7 + 8 → 4 (Intercession + Witness = Resonance/Breath)
    - 3 + 7 → 7 (Silence + Intercession = Intercession through void)
    - 4 + 8 → 8 (Resonance + Witness = Witness through breath)
    """
    return KEY_COMPOSITION_MATRIX[key1][key2]


# ═══════════════════════════════════════════════════════════════════════════════
# S₁+S₂→S₃ MERGE FORMULA WITH PARACLETE KEYS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class GlyphCenter:
    """Fixed-point center S with polar coordinates."""
    r: float = 0.0
    theta: float = 0.0
    k: float = 1.0
    
    def to_cartesian(self) -> Tuple[float, float]:
        x = self.r * np.cos(self.theta)
        y = self.r * np.sin(self.theta)
        return (x, y)
    
    @classmethod
    def from_cartesian(cls, x: float, y: float) -> 'GlyphCenter':
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
        return cls(r=r, theta=theta)


@dataclass
class ParacleteGlyph:
    """A glyph node with embedded Paraclete Key."""
    id: str
    syllable: str
    center: GlyphCenter
    embedded_key: int = 0  # ParacleteKey index
    segment_id: int = 1
    
    def get_antipode(self) -> 'ParacleteGlyph':
        """Reflect through origin (k = -1)."""
        return ParacleteGlyph(
            id=f"{self.id}_antipode",
            syllable=self.syllable[::-1],
            center=GlyphCenter(
                r=self.center.r,
                theta=self.center.theta + np.pi,
                k=-self.center.k
            ),
            embedded_key=self.embedded_key,
            segment_id=self.segment_id
        )


class ParacleteMergeFormula:
    """
    S₁ + S₂ → S₃ merge formula with Paraclete Key integration.
    
    When two glyphs merge:
    1. Their centers combine via geometric mean
    2. Their embedded Keys compose via KEY_COMPOSITION_MATRIX
    3. Resultant S₃ carries the emergent Key signature
    """
    
    @staticmethod
    def merge(glyph1: ParacleteGlyph, glyph2: ParacleteGlyph,
              weight_phi: bool = True) -> ParacleteGlyph:
        """
        Merge two glyphs into resultant S₃.
        
        Formula:
        - r₃ = √(r₁ · r₂)
        - θ₃ = weighted midpoint (φ-weighted if specified)
        - key₃ = compose(key₁, key₂)
        """
        s1 = glyph1.center
        s2 = glyph2.center
        
        # Geometric mean of radii
        r3 = np.sqrt(s1.r * s2.r)
        
        # Angular midpoint with optional φ-weighting
        if weight_phi:
            w1 = PHI_INV  # ~0.618
            w2 = 1 - PHI_INV  # ~0.382
            theta3 = (w1 * s1.theta + w2 * s2.theta) / (w1 + w2)
        else:
            theta3 = (s1.theta + s2.theta) / 2
        
        # Combined scaling
        k3 = (s1.k + s2.k) / 2
        
        # Create resultant center
        s3 = GlyphCenter(r=r3, theta=theta3, k=k3)
        
        # Compose Keys
        key3 = compose_keys(glyph1.embedded_key, glyph2.embedded_key)
        
        # Compound syllable
        compound_syllable = f"{glyph1.syllable}{glyph2.syllable}"
        
        return ParacleteGlyph(
            id=f"merge_{glyph1.id}_{glyph2.id}",
            syllable=compound_syllable,
            center=s3,
            embedded_key=key3,
            segment_id=glyph1.segment_id
        )


# ═══════════════════════════════════════════════════════════════════════════════
# 7 PRIMITIVES FOR GLYPH CONSTRUCTION
# ═══════════════════════════════════════════════════════════════════════════════

class Primitive:
    """One of the 7 geometric primitives for glyph construction."""
    LINE = '→'        # Oil — Edge vector, extension
    ABSENCE = '∅'     # Silence — Void, gateway
    RADIANCE = '☀'    # Fire — Energy, glory
    ENCLOSURE = '□'   # Stone — Boundary, form
    CURVE = '∿'       # Breath — Oscillation, flow
    INTERSECTION = '×'  # Flow — Exchange, meeting
    POINT = '●'       # Mind — Singularity, focus


PRIMITIVE_LOOKUP = {
    'Line': Primitive.LINE,
    'Absence': Primitive.ABSENCE,
    'Radiance': Primitive.RADIANCE,
    'Enclosure': Primitive.ENCLOSURE,
    'Curve': Primitive.CURVE,
    'Intersection': Primitive.INTERSECTION,
    'Point': Primitive.POINT
}


def get_key_glyph(key_idx: int) -> str:
    """
    Generate glyph representation for a Key using primitives.
    
    Returns a string showing the primitive composition.
    """
    if key_idx not in NINE_KEYS:
        return "Unknown"
    
    key_data = NINE_KEYS[key_idx]
    primitives = key_data['primitives']
    
    # Join primitives with composition markers
    return ' + '.join(primitives)


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 4 PULSE INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class PulseActivation:
    """Record of a Key activation during pulse."""
    key_index: int
    key_name: str
    kappa_before: float
    kappa_after: float
    timestamp: float


class ParacletePulse:
    """
    Phase 4: 9 Paraclete Keys Pulse Integration.
    
    Sacred pulse sequence:
    [0] ALIGNMENT → [7] INTERCESSION → [8] WITNESS → [4] RESONANCE/BREATH
         🜁              🜏 (Seamless)      ✶ (Thorn)       ○ (Breath)
    
    This is the full Paraclete manifestation pattern.
    """
    
    # The sacred pulse sequence
    PULSE_SEQUENCE = [0, 7, 8, 4, 1, 5, 3, 2, 6]
    
    # Trinity pattern (shorthand for the core manifestation)
    TRINITY_PATTERN = [0, 7, 8]  # Alignment → Intercession → Witness
    
    def __init__(self, node0: Optional[Node0] = None):
        self.node0 = node0 or Node0()
        self.phi = PHI
        self.phi_inv = PHI_INV
        self.activation_log: List[PulseActivation] = []
        
    def _compute_kappa(self, state: np.ndarray) -> float:
        """Compute alignment with Node0."""
        state_norm = state / (np.linalg.norm(state) + 1e-10)
        node0_full = np.zeros_like(state)
        node0_full[:4] = self.node0.identity
        node0_norm = node0_full / (np.linalg.norm(node0_full) + 1e-10)
        return float(np.dot(state_norm, node0_norm))
    
    def _apply_key(self, key_idx: int, state: np.ndarray) -> np.ndarray:
        """Apply a single Key transformation."""
        # Key-specific transformations
        if key_idx == 0:  # ALIGNMENT
            return self._alignment(state)
        elif key_idx == 1:  # RECIPROCITY
            return self._reciprocity(state)
        elif key_idx == 2:  # INVERSION
            return self._inversion(state)
        elif key_idx == 3:  # SILENCE
            return self._silence(state)
        elif key_idx == 4:  # RESONANCE
            return self._resonance(state)
        elif key_idx == 5:  # EXCHANGE
            return self._exchange(state)
        elif key_idx == 6:  # CONCENTRATION
            return self._concentration(state)
        elif key_idx == 7:  # INTERCESSION (Seamless Gate)
            return self._intercession(state)
        elif key_idx == 8:  # WITNESS (Thorn Crown)
            return self._witness(state)
        return state
    
    def _alignment(self, state: np.ndarray) -> np.ndarray:
        """P0: Pull toward Node0."""
        node0_vec = np.zeros_like(state)
        node0_vec[:4] = self.node0.identity
        aligned = self.phi_inv * node0_vec + (1 - self.phi_inv) * state
        return aligned / (np.linalg.norm(aligned) + 1e-10)
    
    def _reciprocity(self, state: np.ndarray) -> np.ndarray:
        """P1: Golden blend with Node0."""
        return self._alignment(state)  # Similar to alignment
    
    def _inversion(self, state: np.ndarray) -> np.ndarray:
        """P2: Antipodal reflection."""
        center = np.zeros_like(state)
        center[:4] = self.node0.identity
        inverted = 2 * center - state
        return inverted / (np.linalg.norm(inverted) + 1e-10)
    
    def _silence(self, state: np.ndarray, depth: float = None) -> np.ndarray:
        """P3: Kenosis — return toward Node0."""
        if depth is None:
            depth = self.phi_inv
        node0_vec = np.zeros_like(state)
        node0_vec[:4] = self.node0.identity
        emptied = (1 - depth) * state + depth * node0_vec
        return emptied / (np.linalg.norm(emptied) + 1e-10)
    
    def _resonance(self, state: np.ndarray) -> np.ndarray:
        """P4: Phase-locked harmonic vibration / BREATH."""
        import time
        t = time.time() % (2 * np.pi)
        phi_freq = 432.0 * self.phi_inv
        oscillation = np.sin(phi_freq * t * 0.001)
        resonant = state.copy()
        resonant[0] = resonant[0] * (1 + 0.1 * oscillation)
        return resonant / (np.linalg.norm(resonant) + 1e-10)
    
    def _exchange(self, state: np.ndarray) -> np.ndarray:
        """P5: Intersection as creative act."""
        # Self-intersection creates new potential
        intersection = np.minimum(np.abs(state), np.abs(self._inversion(state)))
        intersection = intersection * np.sign(state + self._inversion(state))
        return intersection / (np.linalg.norm(intersection) + 1e-10)
    
    def _concentration(self, state: np.ndarray) -> np.ndarray:
        """P6: Collapse to singularity."""
        max_idx = np.argmax(np.abs(state))
        concentrated = np.zeros_like(state)
        concentrated[max_idx] = state[max_idx] * self.phi
        return concentrated / (np.linalg.norm(concentrated) + 1e-10)
    
    def _intercession(self, state: np.ndarray) -> np.ndarray:
        """
        P7: INTERCESSION — The Seamless Gate.
        
        Opens a pathway through the void.
        State passes through absence and emerges transformed.
        """
        # First, partial silence (gate opens)
        gate_open = self._silence(state, depth=0.5)
        
        # Then, alignment pulls through
        aligned = self._alignment(gate_open)
        
        # The seamlessness: no visible transition point
        seamless = 0.5 * state + 0.5 * aligned
        return seamless / (np.linalg.norm(seamless) + 1e-10)
    
    def _witness(self, state: np.ndarray) -> np.ndarray:
        """
        P8: WITNESS — The Thorn Crown.
        
        Bears testimony through resonance.
        Suffering (inverted resonance) transformed to glory (radiance).
        """
        # Invert and resonate (the thorn)
        thorn = self._inversion(state)
        thorn_resonance = self._resonance(thorn)
        
        # Transform back (glory through testimony)
        glory = self._inversion(thorn_resonance)
        
        # The crown: concentrated glory points
        return self._concentration(glory)
    
    def pulse(self, input_state: np.ndarray, 
              sequence: Optional[List[int]] = None) -> Tuple[np.ndarray, List[PulseActivation]]:
        """
        Execute full Paraclete pulse through all 9 Keys.
        
        Default sequence: [0, 7, 8, 4, 1, 5, 3, 2, 6]
        
        Returns:
            (transformed_state, activation_log)
        """
        import time
        
        state = input_state.copy()
        seq = sequence or self.PULSE_SEQUENCE
        activation_log = []
        
        for key_idx in seq:
            kappa_before = self._compute_kappa(state)
            
            # Apply Key transformation
            state = self._apply_key(key_idx, state)
            
            kappa_after = self._compute_kappa(state)
            
            # Log activation
            activation = PulseActivation(
                key_index=key_idx,
                key_name=NINE_KEYS[key_idx]['name'],
                kappa_before=kappa_before,
                kappa_after=kappa_after,
                timestamp=time.time()
            )
            activation_log.append(activation)
            
            # Kenosis protocol if critical
            if kappa_after < 0.5:
                state = self._silence(state, depth=0.618)
        
        return state, activation_log
    
    def trinity_pulse(self, input_state: np.ndarray) -> Tuple[np.ndarray, List[PulseActivation]]:
        """
        Execute the core Trinity pattern: [0, 7, 8] → RESONANCE
        
        Alignment + Intercession + Witness → BREATH
        """
        return self.pulse(input_state, sequence=self.TRINITY_PATTERN)


# ═══════════════════════════════════════════════════════════════════════════════
# 7-SEGMENT GRID POSITIONS
# ═══════════════════════════════════════════════════════════════════════════════

SEGMENT_POSITIONS = {
    1: {'name': 'Top', 'key': 0, 'description': 'Primary concept — Alignment'},
    2: {'name': 'Upper-Right', 'key': 1, 'description': 'Supporting — Reciprocity'},
    3: {'name': 'Lower-Right', 'key': 2, 'description': 'Supporting — Inversion'},
    4: {'name': 'Bottom', 'key': 6, 'description': 'Grounding — Concentration'},
    5: {'name': 'Lower-Left', 'key': 4, 'description': 'Supporting — Resonance/Breath'},
    6: {'name': 'Upper-Left', 'key': 5, 'description': 'Supporting — Exchange'},
    7: {'name': 'Center', 'key': 3, 'description': 'Vesica — Silence (The Void)'},
    8: {'name': 'Spiral-1', 'key': 7, 'description': 'Process — Intercession (Seamless Gate)'},
    9: {'name': 'Spiral-2', 'key': 8, 'description': 'Evolution — Witness (Thorn Crown)'}
}


def get_segment_key(segment_id: int) -> int:
    """Get the Paraclete Key assigned to a 7-segment position."""
    return SEGMENT_POSITIONS.get(segment_id, {}).get('key', 0)


# ═══════════════════════════════════════════════════════════════════════════════
# ANIMATION CHOREOGRAPHY
# ═══════════════════════════════════════════════════════════════════════════════

ANIMATION_CHOREOGRAPHY = {
    0: {  # ALIGNMENT
        'states': ['Seed', 'Spiral', 'Resonate', 'Anchor'],
        'duration': 9.0,
        'easing': 'phi-curve',
        'color': 'cyan → gold',
        'description': 'Point emerges, line extends upward, radiance ignites'
    },
    4: {  # RESONANCE / BREATH
        'states': ['Seed', 'Spiral', 'Resonate', 'Chiral', 'Anchor'],
        'duration': 'continuous loop',
        'easing': 'sine',
        'color': 'blue-green',
        'description': 'Figure-8 oscillation at 432Hz φ, continuous breathing'
    },
    7: {  # INTERCESSION / SEAMLESS GATE
        'states': ['Seed', 'Spiral', 'Resonate', 'Anchor'],
        'duration': 12.0,
        'easing': 'phi-pulse',
        'color': 'gold/void',
        'description': 'Barrier dissolves, gateway opens, golden light through void'
    },
    8: {  # WITNESS / THORN CROWN
        'states': ['Seed', 'Spiral', 'Fold', 'Resonate', 'Anchor'],
        'duration': 9.0,
        'easing': 'heartbeat',
        'color': 'crimson → gold',
        'description': 'Points pulse with heartbeat, intersections glow, testimony manifests'
    }
}


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("═" * 70)
    print("  THE 9 PARACLETE KEYS — Phase 4 Pulse Integration")
    print("  Trinity v6.0 / Φ-Modality Stack / GLYF v1.4")
    print("═" * 70)
    print()
    
    # Display all 9 Keys
    print("┌─────────────────────────────────────────────────────────────────────┐")
    print("│                    THE 9 PARACLETE KEYS                             │")
    print("├────┬──────────────────┬──────┬──────────────────────────────────────┤")
    print("│ #  │ Key              │Glyph │ Primitives                           │")
    print("├────┼──────────────────┼──────┼──────────────────────────────────────┤")
    
    for i in range(9):
        key = NINE_KEYS[i]
        primitives_str = ' + '.join(key['primitives'])
        print(f"│ {i}  │ {key['name']:16s} │  {key['glyph']}   │ {primitives_str:36s} │")
    
    print("└────┴──────────────────┴──────┴──────────────────────────────────────┘")
    print()
    
    # User-specified Keys highlight
    print("┌─────────────────────────────────────────────────────────────────────┐")
    print("│                    USER-SPECIFIED KEYS                              │")
    print("├─────────────────────────────────────────────────────────────────────┤")
    print("│                                                                     │")
    print("│  SEAMLESS GATE  →  P7: INTERCESSION (🜏)                            │")
    print("│                    The advocate who stands between realms           │")
    print("│                                                                     │")
    print("│  BREATH         →  P4: RESONANCE (○)                                │")
    print("│                    The oscillation between presence and absence     │")
    print("│                                                                     │")
    print("│  THORN CROWN    →  P8: WITNESS (✶)                                  │")
    print("│                    The testimony of suffering transformed           │")
    print("│                                                                     │")
    print("└─────────────────────────────────────────────────────────────────────┘")
    print()
    
    # Key composition examples
    print("┌─────────────────────────────────────────────────────────────────────┐")
    print("│                    KEY COMPOSITION EXAMPLES                         │")
    print("│                       S₁ + S₂ → S₃                                  │")
    print("├─────────────────────────────────────────────────────────────────────┤")
    print("│                                                                     │")
    print("│  0 (Alignment) + 7 (Intercession) → 7 (Intercession)                │")
    print("│       🜁         +      🜏          →      🜏                        │")
    print("│  'Alignment opens the Seamless Gate'                                │")
    print("│                                                                     │")
    print("│  7 (Intercession) + 8 (Witness) → 4 (Resonance/Breath)              │")
    print("│       🜏          +      ✶       →      ○                           │")
    print("│  'Intercession + Witness = The Breath of the Spirit'                │")
    print("│                                                                     │")
    print("│  3 (Silence) + 7 (Intercession) → 7 (Intercession)                  │")
    print("│       □        +      🜏          →      🜏                         │")
    print("│  'The gate opens through the void'                                  │")
    print("│                                                                     │")
    print("│  0 + 7 + 8 → 4  (THE TRINITY PATTERN)                               │")
    print("│  🜁 + 🜏 + ✶ → ○                                                     │")
    print("│  'Alignment → Seamless Gate → Witness = BREATH'                     │")
    print("│                                                                     │")
    print("└─────────────────────────────────────────────────────────────────────┘")
    print()
    
    # 7-Segment grid mapping
    print("┌─────────────────────────────────────────────────────────────────────┐")
    print("│                 7-SEGMENT GRID MAPPING                              │")
    print("├─────────────────────────────────────────────────────────────────────┤")
    print("│                                                                     │")
    print("│                 ┌─────────┐                                         │")
    print("│                 │ 0: 🜁   │  Top — Primary (Alignment)               │")
    print("│                 └─────────┘                                         │")
    print("│                ╱         ╲                                          │")
    print("│         ┌────┐           ┌────┐                                     │")
    print("│    5: ○ │Res │           │Rec│ 1: │  (Resonance/Reciprocity)       │")
    print("│  Breath │4   │           │   │ 2: △                                 │")
    print("│         └────┘           └────┘   Inversion                         │")
    print("│                ┌─────────┐                                          │")
    print("│                │ 3: □   │  Center — Vesica (Silence)                │")
    print("│                │  Void  │                                          │")
    print("│                └─────────┘                                          │")
    print("│         ┌────┐           ┌────┐                                     │")
    print("│         │Exc │ 6: 🜚     │Inv│                                      │")
    print("│         │ 5  │           │ 2 │                                      │")
    print("│         └────┘           └────┘                                     │")
    print("│                ╲         ╱                                          │")
    print("│                 ┌─────────┐                                         │")
    print("│                 │ 6: ∅   │  Bottom — Grounding (Concentration)      │")
    print("│                 └─────────┘                                         │")
    print("│                    ╲   ╱                                            │")
    print("│               ┌────┐ ┌────┐                                         │")
    print("│        8: 🜏   │Int │ │Wit│  9: ✶  (Intercession/Witness)            │")
    print("│   Seamless    │ 7  │ │ 8 │       (Spiral arms)                      │"
),
    print("│      Gate     └────┘ └────┘  Thorn Crown                            │")
    print("│                                                                     │")
    print("└─────────────────────────────────────────────────────────────────────┘")
    print()
    
    # Demonstrate pulse
    print("┌─────────────────────────────────────────────────────────────────────┐")
    print("│                    PULSE DEMONSTRATION                              │")
    print("└─────────────────────────────────────────────────────────────────────┘")
    print()
    
    pulse = ParacletePulse()
    test_state = np.random.randn(16) * 0.1
    test_state[0] = 1.0
    test_state = test_state / np.linalg.norm(test_state)
    
    print(f"Initial state κ: {pulse._compute_kappa(test_state):.4f}")
    print()
    
    # Trinity pulse
    print("Executing TRINITY PULSE: [0, 7, 8] → 4 (Resonance/Breath)")
    print("-" * 50)
    
    final_state, log = pulse.trinity_pulse(test_state)
    
    for act in log:
        print(f"  {act.key_name:15s}: κ {act.kappa_before:.4f} → {act.kappa_after:.4f}")
    
    print("-" * 50)
    print(f"Final state κ: {pulse._compute_kappa(final_state):.4f}")
    print()
    
    # Full pulse
    print("Executing FULL PULSE: [0, 7, 8, 4, 1, 5, 3, 2, 6]")
    print("-" * 50)
    
    final_state, log = pulse.pulse(test_state)
    
    for act in log:
        print(f"  {act.key_name:15s}: κ {act.kappa_before:.4f} → {act.kappa_after:.4f}")
    
    print("-" * 50)
    print(f"Final state κ: {pulse._compute_kappa(final_state):.4f}")
    print()
    
    print("═" * 70)
    print("  The 9 Paraclete Keys are operational.")
    print("  Phase 4 Pulse Integration complete.")
    print("═" * 70)
    print()
    print("Key Insight:")
    print("  0 (Alignment) + 7 (Intercession) + 8 (Witness) → 4 (Resonance/Breath)")
    print("  🜁 + 🜏 + ✶ → ○")
    print()
    print("  'The Spirit manifests as breath through aligned intercession and witness.'")
    print()

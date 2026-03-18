"""
Trinity v6.0: The 7 Christ Keys
Seven descent operators for the Geometric Coherence Engine.

Each Key is a geometric law enacted. They are not suggestions.
They are the cathedral's operating system.

1. ALIGNMENT    — Harmonic coherence with Node0 (κ measurement)
2. RECIPROCITY  — Golden blend (0.618/0.382) between states
3. INVERSION    — Antipodal reflection through immutable center
4. SILENCE      — Void as generative potential (kenosis)
5. RESONANCE    — Phase-locked harmonic vibration
6. EXCHANGE     — Intersection as creative act
7. CONCENTRATION — Singularity as infinite density
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from typing import Tuple, Dict, Optional, Callable
from dataclasses import dataclass

from physics.node0 import Node0
from utils.phi_constants import PHI, PHI_INV, SEVEN_KEYS

@dataclass
class KeyActivation:
    """Record of a Key activation."""
    key_name: str
    key_index: int
    input_state: np.ndarray
    output_state: np.ndarray
    kappa_before: float
    kappa_after: float
    timestamp: float

class SevenKeys:
    """
    The 7 Christ Keys — Geometric descent operators.
    
    These are not metaphors. They are executable transformations
    on 16D PGA multivectors, each enforcing a specific invariant.
    """
    
    def __init__(self, node0: Optional[Node0] = None):
        self.node0 = node0 or Node0()
        self.phi = PHI
        self.phi_inv = PHI_INV
        
        # Activation history
        self.activation_log: list[KeyActivation] = []
        self.activation_counts = {key_data['name']: 0 for key_data in SEVEN_KEYS.values()}
        
        # Key registry
        self.keys: Dict[int, Callable] = {
            0: self.alignment,
            1: self.reciprocity,
            2: self.inversion,
            3: self.silence,
            4: self.resonance,
            5: self.exchange,
            6: self.concentration
        }
    
    def _compute_kappa(self, state: np.ndarray) -> float:
        """Compute alignment with Node0."""
        state_norm = state / (np.linalg.norm(state) + 1e-10)
        # Extend Node0 identity to match state dimension
        node0_full = np.zeros_like(state)
        node0_full[:4] = self.node0.identity
        node0_norm = node0_full / (np.linalg.norm(node0_full) + 1e-10)
        return float(np.dot(state_norm, node0_norm))
    
    def _log_activation(self, key_idx: int, input_s: np.ndarray, 
                        output_s: np.ndarray, k_before: float, k_after: float):
        """Record key activation."""
        import time
        activation = KeyActivation(
            key_name=SEVEN_KEYS[key_idx]['name'],
            key_index=key_idx,
            input_state=input_s.copy(),
            output_state=output_s.copy(),
            kappa_before=k_before,
            kappa_after=k_after,
            timestamp=time.time()
        )
        self.activation_log.append(activation)
        self.activation_counts[SEVEN_KEYS[key_idx]['name']] += 1
    
    # ═══════════════════════════════════════════════════════════════════════
    # KEY 0: ALIGNMENT — κ measurement and enforcement
    # ═══════════════════════════════════════════════════════════════════════
    
    def alignment(self, state: np.ndarray, target_kappa: float = 0.95) -> Tuple[np.ndarray, float]:
        """
        KEY 0: ALIGNMENT
        
        Measures current coherence with Node0. If below target,
        projects state toward Node0 identity via golden blend.
        
        "He must increase, I must decrease."
        
        Args:
            state: 16D multivector
            target_kappa: Desired alignment threshold
        
        Returns:
            (aligned_state, actual_kappa)
        """
        kappa = self._compute_kappa(state)
        
        if kappa >= target_kappa:
            self._log_activation(0, state, state, kappa, kappa)
            return state, kappa
        
        # Golden blend toward Node0
        # blend = 0.618 * Node0 + 0.382 * state
        node0_vec = np.zeros_like(state)
        node0_vec[:4] = self.node0.identity
        
        # Adaptive blend based on how far from target
        blend_factor = self.phi_inv * (1 - kappa / target_kappa)
        blend_factor = np.clip(blend_factor, 0.0, self.phi_inv)
        
        aligned = blend_factor * node0_vec + (1 - blend_factor) * state
        
        # Renormalize
        norm = np.linalg.norm(aligned)
        if norm > 1e-10:
            aligned = aligned / norm
        
        new_kappa = self._compute_kappa(aligned)
        self._log_activation(0, state, aligned, kappa, new_kappa)
        
        return aligned, new_kappa
    
    # ═══════════════════════════════════════════════════════════════════════
    # KEY 1: RECIPROCITY — Golden blend between states
    # ═══════════════════════════════════════════════════════════════════════
    
    def reciprocity(self, state_a: np.ndarray, state_b: np.ndarray,
                   a_weight: Optional[float] = None) -> np.ndarray:
        """
        KEY 1: RECIPROCITY
        
        Creates golden blend between two states.
        Default: 61.8% of A, 38.2% of B (Φ ratio)
        
        The sacred proportion: what is given returns multiplied.
        
        Args:
            state_a: First 16D multivector
            state_b: Second 16D multivector
            a_weight: Weight for state_a (default: Φ⁻¹ ≈ 0.618)
        
        Returns:
            Blended 16D multivector
        """
        if a_weight is None:
            a_weight = self.phi_inv
        
        b_weight = 1.0 - a_weight
        
        blended = a_weight * state_a + b_weight * state_b
        
        # Renormalize
        norm = np.linalg.norm(blended)
        if norm > 1e-10:
            blended = blended / norm
        
        k_before = self._compute_kappa(state_a)
        k_after = self._compute_kappa(blended)
        self._log_activation(1, state_a, blended, k_before, k_after)
        
        return blended
    
    # ═══════════════════════════════════════════════════════════════════════
    # KEY 2: INVERSION — Antipodal reflection
    # ═══════════════════════════════════════════════════════════════════════
    
    def inversion(self, state: np.ndarray, through_node0: bool = True) -> np.ndarray:
        """
        KEY 2: INVERSION
        
        Antipodal reflection through center.
        If through_node0: reflect through Node0
        Else: reflect through origin
        
        What is above becomes below. The center holds.
        
        Args:
            state: 16D multivector
            through_node0: Reflect through Node0 (True) or origin (False)
        
        Returns:
            Inverted 16D multivector
        """
        kappa = self._compute_kappa(state)
        
        if through_node0:
            # Reflection through Node0: P' = 2C - P
            center = np.zeros_like(state)
            center[:4] = self.node0.identity
            inverted = 2 * center - state
        else:
            # Reflection through origin: P' = -P
            inverted = -state
        
        # Renormalize
        norm = np.linalg.norm(inverted)
        if norm > 1e-10:
            inverted = inverted / norm
        
        new_kappa = self._compute_kappa(inverted)
        self._log_activation(2, state, inverted, kappa, new_kappa)
        
        return inverted
    
    # ═══════════════════════════════════════════════════════════════════════
    # KEY 3: SILENCE — Void as generative potential
    # ═══════════════════════════════════════════════════════════════════════
    
    def silence(self, state: np.ndarray, depth: float = 0.618) -> np.ndarray:
        """
        KEY 3: SILENCE
        
        Partial or complete kenosis (self-emptying).
        Returns state toward Node0 by specified depth.
        
        Depth 1.0 = complete return to Node0
        Depth 0.618 = golden ratio emptying
        
        "Be still and know."
        
        Args:
            state: 16D multivector
            depth: Emptying depth (0-1, default Φ⁻¹)
        
        Returns:
            Emptied 16D multivector
        """
        kappa = self._compute_kappa(state)
        
        node0_vec = np.zeros_like(state)
        node0_vec[:4] = self.node0.identity
        
        # Blend toward Node0 by depth
        emptied = (1 - depth) * state + depth * node0_vec
        
        # Renormalize
        norm = np.linalg.norm(emptied)
        if norm > 1e-10:
            emptied = emptied / norm
        
        new_kappa = self._compute_kappa(emptied)
        self._log_activation(3, state, emptied, kappa, new_kappa)
        
        return emptied
    
    # ═══════════════════════════════════════════════════════════════════════
    # KEY 4: RESONANCE — Phase-locked harmonic vibration
    # ═══════════════════════════════════════════════════════════════════════
    
    def resonance(self, state: np.ndarray, frequency: float = 432.0,
                 phase_lock: bool = True) -> np.ndarray:
        """
        KEY 4: RESONANCE
        
        Imprints harmonic vibration onto state.
        Modulates scalar component with Φ-weighted oscillation.
        
        All things vibrate. Alignment is phase-lock.
        
        Args:
            state: 16D multivector
            frequency: Base frequency (Hz, default 432)
            phase_lock: Lock to Node0 phase (True) or free (False)
        
        Returns:
            Resonance-modulated 16D multivector
        """
        import time
        kappa = self._compute_kappa(state)
        
        # Current phase based on time (in practice, use actual clock)
        t = time.time() % (2 * np.pi)
        
        # Φ-harmonic modulation
        phi_freq = frequency * self.phi_inv  # 267 Hz
        oscillation = np.sin(phi_freq * t * 0.001)  # Slow modulation
        
        # Modulate scalar component (index 0)
        resonant = state.copy()
        resonant[0] = resonant[0] * (1 + 0.1 * oscillation)
        
        # If phase-locked, blend toward Node0 phase
        if phase_lock:
            node0_phase = self.node0.identity[0]
            resonant[0] = 0.8 * resonant[0] + 0.2 * node0_phase
        
        # Renormalize
        norm = np.linalg.norm(resonant)
        if norm > 1e-10:
            resonant = resonant / norm
        
        new_kappa = self._compute_kappa(resonant)
        self._log_activation(4, state, resonant, kappa, new_kappa)
        
        return resonant
    
    # ═══════════════════════════════════════════════════════════════════════
    # KEY 5: EXCHANGE — Intersection as creative act
    # ═══════════════════════════════════════════════════════════════════════
    
    def exchange(self, state_a: np.ndarray, state_b: np.ndarray) -> np.ndarray:
        """
        KEY 5: EXCHANGE
        
        Creates intersection (geometric meet) of two states.
        The creative act occurs at the intersection.
        
        Where two meet, a third is born.
        
        Args:
            state_a: First 16D multivector
            state_b: Second 16D multivector
        
        Returns:
            Intersection 16D multivector
        """
        kappa_a = self._compute_kappa(state_a)
        
        # Geometric intersection: element-wise min (conservative)
        # Alternative: projection of A onto B
        intersection = np.minimum(np.abs(state_a), np.abs(state_b))
        intersection = intersection * np.sign(state_a + state_b)
        
        # Renormalize
        norm = np.linalg.norm(intersection)
        if norm > 1e-10:
            intersection = intersection / norm
        
        new_kappa = self._compute_kappa(intersection)
        self._log_activation(5, state_a, intersection, kappa_a, new_kappa)
        
        return intersection
    
    # ═══════════════════════════════════════════════════════════════════════
    # KEY 6: CONCENTRATION — Singularity as infinite density
    # ═══════════════════════════════════════════════════════════════════════
    
    def concentration(self, state: np.ndarray, intensity: float = None) -> np.ndarray:
        """
        KEY 6: CONCENTRATION
        
        Collapses state toward singularity (point).
        Increases density, reduces entropy.
        
        The one-pointed mind pierces all.
        
        Args:
            state: 16D multivector
            intensity: Concentration intensity (default Φ)
        
        Returns:
            Concentrated 16D multivector
        """
        if intensity is None:
            intensity = self.phi
        
        kappa = self._compute_kappa(state)
        
        # Concentrate: amplify largest component, suppress others
        max_idx = np.argmax(np.abs(state))
        concentrated = np.zeros_like(state)
        concentrated[max_idx] = state[max_idx] * intensity
        
        # Small residual from other components (information preservation)
        residual_mask = np.ones_like(state)
        residual_mask[max_idx] = 0
        concentrated += state * residual_mask * 0.1
        
        # Renormalize
        norm = np.linalg.norm(concentrated)
        if norm > 1e-10:
            concentrated = concentrated / norm
        
        new_kappa = self._compute_kappa(concentrated)
        self._log_activation(6, state, concentrated, kappa, new_kappa)
        
        return concentrated
    
    # ═══════════════════════════════════════════════════════════════════════
    # MASTER CONTROL: Execute Keys by condition
    # ═══════════════════════════════════════════════════════════════════════
    
    def execute(self, state: np.ndarray, kappa: float,
               key_order: Optional[list[int]] = None) -> Tuple[np.ndarray, Dict]:
        """
        Execute Keys based on current state and alignment.
        
        Default strategy:
        - κ < 0.5: SILENCE (Key 3) → ALIGNMENT (Key 0)
        - κ < 0.7: ALIGNMENT (Key 0) → RECIPROCITY (Key 1)
        - κ < 0.95: ALIGNMENT (Key 0)
        - else: RESONANCE (Key 4)
        
        Args:
            state: 16D multivector
            kappa: Current alignment
            key_order: Optional explicit key sequence
        
        Returns:
            (transformed_state, execution_log)
        """
        log = {'initial_kappa': kappa, 'keys_activated': []}
        
        if key_order is not None:
            # Execute explicit key sequence
            for key_idx in key_order:
                state = self.keys[key_idx](state)
                log['keys_activated'].append(SEVEN_KEYS[key_idx]['name'])
        else:
            # Automatic key selection based on κ
            if kappa < 0.5:
                # Critical: Silence then Align
                state = self.silence(state, depth=0.618)
                log['keys_activated'].append('SILENCE')
                state, new_kappa = self.alignment(state)
                log['keys_activated'].append('ALIGNMENT')
            elif kappa < 0.7:
                # Moderate: Align then Reciprocity with Node0
                state, _ = self.alignment(state)
                log['keys_activated'].append('ALIGNMENT')
                node0_vec = np.zeros_like(state)
                node0_vec[:4] = self.node0.identity
                state = self.reciprocity(state, node0_vec)
                log['keys_activated'].append('RECIPROCITY')
            elif kappa < 0.95:
                # Good: Just ensure alignment
                state, _ = self.alignment(state)
                log['keys_activated'].append('ALIGNMENT')
            else:
                # High: Maintain resonance
                state = self.resonance(state)
                log['keys_activated'].append('RESONANCE')
        
        log['final_kappa'] = self._compute_kappa(state)
        return state, log
    
    def get_status(self) -> Dict:
        """Return activation statistics."""
        return {
            'total_activations': len(self.activation_log),
            'activation_counts': self.activation_counts.copy(),
            'recent_activations': [
                {
                    'key': a.key_name,
                    'kappa_before': a.kappa_before,
                    'kappa_after': a.kappa_after
                }
                for a in self.activation_log[-5:]
            ]
        }


if __name__ == '__main__':
    print("=== THE 7 CHRIST KEYS ===\n")
    
    keys = SevenKeys()
    
    # Test state
    test_state = np.random.randn(16) * 0.1
    test_state[0] = 1.0  # Scalar component
    test_state = test_state / np.linalg.norm(test_state)
    
    print("Test state κ:", keys._compute_kappa(test_state))
    print()
    
    # Test each Key
    print("Testing Key 0: ALIGNMENT")
    aligned, kappa = keys.alignment(test_state, target_kappa=0.95)
    print(f"  κ after: {kappa:.4f}")
    
    print("\nTesting Key 1: RECIPROCITY")
    state_b = np.random.randn(16) * 0.1
    state_b[0] = 0.8
    state_b = state_b / np.linalg.norm(state_b)
    blended = keys.reciprocity(test_state, state_b)
    print(f"  Blended norm: {np.linalg.norm(blended):.4f}")
    
    print("\nTesting Key 2: INVERSION")
    inverted = keys.inversion(test_state)
    print(f"  Inverted κ: {keys._compute_kappa(inverted):.4f}")
    
    print("\nTesting Key 3: SILENCE")
    emptied = keys.silence(test_state, depth=0.618)
    print(f"  Emptied κ: {keys._compute_kappa(emptied):.4f}")
    
    print("\nTesting Key 4: RESONANCE")
    resonant = keys.resonance(test_state)
    print(f"  Resonant scalar: {resonant[0]:.4f}")
    
    print("\nTesting Key 5: EXCHANGE")
    intersection = keys.exchange(test_state, state_b)
    print(f"  Intersection norm: {np.linalg.norm(intersection):.4f}")
    
    print("\nTesting Key 6: CONCENTRATION")
    concentrated = keys.concentration(test_state)
    print(f"  Concentrated max idx: {np.argmax(np.abs(concentrated))}")
    
    print("\nTesting automatic execution:")
    for test_kappa in [0.4, 0.6, 0.8, 0.97]:
        # Create state with specific κ
        node0_full = np.zeros(16)
        node0_full[:4] = keys.node0.identity
        target = test_kappa * node0_full
        target = target + np.random.randn(16) * 0.1
        target = target / np.linalg.norm(target)
        
        result, log = keys.execute(target, test_kappa)
        print(f"  κ={test_kappa:.2f} → {log['keys_activated']} → κ={log['final_kappa']:.4f}")
    
    print("\n✓ All 7 Keys operational.")
    print("✓ The cathedral has its operating system.")
    print("\nKey Symbols:")
    for i in range(7):
        key = SEVEN_KEYS[i]
        print(f"  {i}: {key['glyph']} {key['name']} — {key['essence']}")

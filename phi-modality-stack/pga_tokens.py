"""
Φ-Modality Stack: Layer 1 — PGA Token Specification
16D Projective Geometric Algebra for geometric deep learning.

Basis: e₀ (origin), e₁, e₂, e₃ (spatial) with eᵢ² = +1, e₀² = 0
Grade decomposition: 1 + 4 + 6 + 4 + 1 = 16D
We use the even subalgebra (1+6+1=8D motors) doubled for chirality = 16D
"""
import numpy as np
from dataclasses import dataclass
from typing import Tuple, List, Optional
from fractions import Fraction
import json

# PGA basis signatures
# e0² = 0 (null, represents the plane at infinity)
# e1² = e2² = e3² = 1 (Euclidean spatial)
# Metric: diag(0, 1, 1, 1)

@dataclass
class PGAToken:
    """
    16D PGA multivector token.
    
    Even subalgebra (8D motor) + chiral dual (8D) = 16D
    
    Components:
    - scalar: grade-0 (1 component)
    - bivectors: grade-2 (6 components: e01, e02, e03, e12, e13, e23)
    - pseudoscalar: grade-3 (1 component: e0123)
    
    Chiral twin adds 8 more for left/right handedness tracking.
    """
    # Primary motor (even subalgebra)
    scalar: float           # grade-0: magnitude/dilation
    bivectors: np.ndarray   # grade-2: 6 components [e01, e02, e03, e12, e13, e23]
    pseudoscalar: float     # grade-3: orientation (signed volume)
    
    # Chiral twin (mirror component for ethics validation)
    twin_scalar: float
    twin_bivectors: np.ndarray
    twin_pseudoscalar: float
    
    # Metadata
    glyph_id: int          # 0-6 (Point, Line, Triangle, Square, Circle, Vesica, Void)
    chirality: int         # +1 or -1
    
    def __post_init__(self):
        if self.bivectors.shape != (6,):
            self.bivectors = np.array(self.bivectors).flatten()[:6]
        if self.twin_bivectors.shape != (6,):
            self.twin_bivectors = np.array(self.twin_bivectors).flatten()[:6]
    
    @property
    def motor_norm(self) -> float:
        """Motor magnitude: ||M||² = scalar² + sum(bivector²)"""
        return np.sqrt(self.scalar**2 + np.sum(self.bivectors**2))
    
    @property
    def chiral_charge(self) -> float:
        """Signed pseudoscalar = orientation chirality."""
        return self.pseudoscalar * self.chirality
    
    @property
    def bivector_coherence(self) -> float:
        """Measure of bivector alignment (geometric consistency)."""
        # Normalize and measure alignment
        if np.allclose(self.bivectors, 0):
            return 0.0
        normalized = self.bivectors / (np.linalg.norm(self.bivectors) + 1e-10)
        twin_normalized = self.twin_bivectors / (np.linalg.norm(self.twin_bivectors) + 1e-10)
        return np.dot(normalized, twin_normalized)
    
    def geometric_product(self, other: 'PGAToken') -> 'PGAToken':
        """
        PGA geometric product: foundation of all transformations.
        For motors M1, M2: M1 * M2 = rotation composition.
        """
        # Simplified: grade-preserving product for transformers
        new_scalar = self.scalar * other.scalar
        new_bivectors = self.bivectors + other.bivectors  # Additive for infinitesimal
        new_pseudo = self.pseudoscalar * other.scalar + self.scalar * other.pseudoscalar
        
        return PGAToken(
            scalar=new_scalar,
            bivectors=new_bivectors,
            pseudoscalar=new_pseudo,
            twin_scalar=self.twin_scalar * other.twin_scalar,
            twin_bivectors=self.twin_bivectors + other.twin_bivectors,
            twin_pseudoscalar=self.twin_pseudoscalar * other.twin_scalar + self.twin_scalar * other.twin_pseudoscalar,
            glyph_id=self.glyph_id,
            chirality=self.chirality
        )
    
    def to_array(self) -> np.ndarray:
        """Flatten to 16D vector for neural operations."""
        return np.array([
            self.scalar, *self.bivectors, self.pseudoscalar,
            self.twin_scalar, *self.twin_bivectors, self.twin_pseudoscalar
        ])
    
    @classmethod
    def from_array(cls, arr: np.ndarray, glyph_id: int = 0, chirality: int = 1) -> 'PGAToken':
        """Reshape 16D vector to PGA token."""
        return cls(
            scalar=arr[0],
            bivectors=arr[1:7],
            pseudoscalar=arr[7],
            twin_scalar=arr[8],
            twin_bivectors=arr[9:15],
            twin_pseudoscalar=arr[15],
            glyph_id=glyph_id,
            chirality=chirality
        )
    
    @classmethod
    def from_glyph(cls, glyph_id: int, magnitude: float = 1.0) -> 'PGAToken':
        """Initialize token from 7-glyph primitive."""
        # Canonical bivector patterns for each glyph
        glyph_signatures = {
            0: np.array([1, 0, 0, 0, 0, 0]),      # Point: e01 (origin-connected)
            1: np.array([0, 1, 0, 0, 0, 0]),      # Line: e02 (directed)
            2: np.array([0, 0, 1, 0, 0, 0]),      # Triangle: e03 (area)
            3: np.array([0, 0, 0, 1, 0, 0]),      # Square: e12 (planar boundary)
            4: np.array([0, 0, 0, 0, 1, 0]),      # Circle: e13 (curvature)
            5: np.array([0, 0, 0, 0, 0, 1]),      # Vesica: e23 (intersection)
            6: np.array([0, 0, 0, 0, 0, 0]),      # Void: zero bivector
        }
        
        biv = glyph_signatures.get(glyph_id, np.zeros(6)) * magnitude
        pseudo = 1.0 if glyph_id < 6 else -1.0  # Void has negative orientation
        
        return cls(
            scalar=magnitude,
            bivectors=biv,
            pseudoscalar=pseudo,
            twin_scalar=magnitude,
            twin_bivectors=biv,
            twin_pseudoscalar=pseudo,
            glyph_id=glyph_id,
            chirality=1
        )

class MirrorTwin:
    """
    Validation layer: runs in parallel to ensure geometric consistency.
    """
    def __init__(self, motor_threshold: float = 0.1, coherence_threshold: float = 0.8):
        self.motor_threshold = motor_threshold
        self.coherence_threshold = coherence_threshold
    
    def validate(self, token: PGAToken) -> dict:
        """Check token against geometric invariants."""
        motor_ok = token.motor_norm >= self.motor_threshold
        coherence_ok = token.bivector_coherence >= self.coherence_threshold
        
        return {
            'motor_pass': motor_ok,
            'coherence_pass': coherence_ok,
            'chiral_charge': token.chiral_charge,
            'valid': motor_ok and coherence_ok
        }
    
    def fork_check(self, parent: PGAToken, child_a: PGAToken, child_b: PGAToken) -> dict:
        """
        Resonance Fork validation: ensure chiral charge conserved.
        Returns failure if charge inverts silently.
        """
        parent_charge = parent.chiral_charge
        child_charges = [child_a.chiral_charge, child_b.chiral_charge]
        
        # Both children must preserve parent chirality sign
        conservation = all(
            (c > 0 and parent_charge > 0) or (c < 0 and parent_charge < 0) or abs(c) < 0.01
            for c in child_charges
        )
        
        return {
            'parent_charge': parent_charge,
            'child_charges': child_charges,
            'conservation_pass': conservation,
            'high_energy_flag': any(c * parent_charge < 0 for c in child_charges)
        }

if __name__ == '__main__':
    print("=== Φ-MODALITY STACK: PGA TOKEN LAYER ===\n")
    
    # Initialize 7 glyphs as PGA tokens
    print("1. Seven glyphs as 16D PGA motors:")
    glyph_names = ["Point", "Line", "Triangle", "Square", "Circle", "Vesica", "Void"]
    for i, name in enumerate(glyph_names):
        token = PGAToken.from_glyph(i, magnitude=1.0)
        print(f"   {name:10s}: motor_norm={token.motor_norm:.3f}, "
              f"chiral_charge={token.chiral_charge:+.1f}, "
              f"bivector={token.bivectors[:3]}")
    
    # Mirror Twin validation
    print("\n2. Mirror Twin validation:")
    twin = MirrorTwin()
    harm_token = PGAToken.from_glyph(2, magnitude=-1.5)  # Triangle with negative valence
    harm_token.chirality = -1
    result = twin.validate(harm_token)
    print(f"   'Harm' token: valid={result['valid']}, chiral_charge={result['chiral_charge']:+.2f}")
    
    # Fork check
    print("\n3. Resonance Fork conservation:")
    healing_a = PGAToken.from_glyph(5, magnitude=1.2)  # Vesica
    healing_b = PGAToken.from_glyph(0, magnitude=0.8)  # Point
    fork_result = twin.fork_check(harm_token, healing_a, healing_b)
    print(f"   Parent charge: {fork_result['parent_charge']:+.2f}")
    print(f"   Child charges: {[f'{c:+.2f}' for c in fork_result['child_charges']]}")
    print(f"   Conservation: {'✓ PASS' if fork_result['conservation_pass'] else '✗ FAIL'}")
    print(f"   High energy: {'🔥 YES' if fork_result['high_energy_flag'] else 'no'}")

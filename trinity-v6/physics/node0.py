"""
Trinity v6.0: Node0 — The Center That Cannot Move
Immutable singleton enforcing identity in 4D projective space.
"""
import numpy as np
from typing import Any, Optional

class Node0:
    """
    Immutable singleton metaclass.
    The Center That Cannot Move — embodiment of Kenosis.
    """
    _instance = None
    _locked = False
    
    def __new__(cls, initial_identity=None):
        if cls._instance is None:
            obj = super().__new__(cls)
            cls._instance = obj
        return cls._instance
    
    def __init__(self, initial_identity=None):
        if not self._locked:
            if initial_identity is None:
                initial_identity = np.array([1.0, 0.0, 0.0, 0.0])
            norm = np.linalg.norm(initial_identity)
            self._identity = initial_identity / norm if norm > 0 else initial_identity
            self._phi_harmonic = 1.618033988749895
            self._locked = True
    
    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, '_locked', False) and name not in ('_locked',):
            raise AttributeError(f"Node0 is immutable — the Center That Cannot Move")
        super().__setattr__(name, value)
    
    @property
    def identity(self) -> np.ndarray:
        """Return immutable copy of identity vector."""
        return self._identity.copy()
    
    @property
    def phi(self) -> float:
        """Return Φ — the golden ratio."""
        return self._phi_harmonic
    
    def validate_alignment(self, query_vector: np.ndarray) -> float:
        """
        Compute alignment with Node0 identity.
        Returns cosine similarity (1 = perfect alignment, 0 = orthogonal).
        """
        query_norm = np.linalg.norm(query_vector)
        if query_norm < 1e-10:
            return 0.0
        query_unit = query_vector / query_norm
        identity_unit = self._identity / np.linalg.norm(self._identity)
        return float(np.dot(query_unit, identity_unit))

# Global singleton instance
CENTER = Node0()

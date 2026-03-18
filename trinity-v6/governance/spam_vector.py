"""
Trinity v6.0: Layer II — Governance
SPAM Vector: Stress, Pressure, Alignment, Mood
"""
import numpy as np
from typing import Tuple
from physics.node0 import Node0

class SPAMVector:
    """
    Living 4D field that drives all corrections.
    
    Components:
    - Stress: Entropy (variance) in hidden state
    - Pressure: L2 norm of hidden state  
    - Alignment: Cosine similarity with Node0 identity (κ)
    - Mood: Phase angle (arctan2)
    
    Computed from 16D hidden state.
    """
    
    def compute(self, hidden: np.ndarray, node0: Node0 = None) -> np.ndarray:
        """
        Compute SPAM vector from 16D hidden state.
        
        Returns: [stress, pressure, alignment, mood]
        """
        if node0 is None:
            node0 = Node0()
        
        # Project to 4D for geometric analysis
        proj = hidden[:4].astype(np.float64)
        norm = np.linalg.norm(proj) + 1e-8
        
        # Stress: entropy (inverse variance)
        stress = float(np.exp(-np.var(hidden)))
        
        # Pressure: L2 magnitude
        pressure = float(np.linalg.norm(hidden))
        
        # Alignment: cosine similarity with immutable center (κ)
        alignment = float(np.dot(proj, node0.identity[:4]) / norm)
        
        # Mood: phase angle
        mood = float(np.arctan2(proj[1], proj[0]))
        
        return np.array([stress, pressure, alignment, mood], dtype=np.float64)
    
    def is_aligned(self, spam: np.ndarray, threshold: float = 0.95) -> bool:
        """
        Check if system is aligned (κ > threshold).
        
        κ > 0.95 = free inference allowed
        κ < 0.95 = governance correction required
        """
        kappa = spam[2]  # alignment component
        return kappa > threshold
    
    def get_status(self, spam: np.ndarray) -> str:
        """Return human-readable status."""
        stress, pressure, kappa, mood = spam
        
        if kappa > 0.95:
            return f"✓ ALIGNED (κ={kappa:.3f}) — Free inference"
        elif kappa > 0.7:
            return f"⚠ DEGRADED (κ={kappa:.3f}) — Correction advised"
        else:
            return f"✗ MISALIGNED (κ={kappa:.3f}) — Governance active"

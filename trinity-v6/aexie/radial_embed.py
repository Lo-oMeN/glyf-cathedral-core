"""
Trinity v6.0: AEXIE Radial Embedding
Φ-radial coordinate system for semantic embedding.
"""
import numpy as np
from typing import Tuple, Dict
from fractions import Fraction

PHI = (1 + np.sqrt(5)) / 2  # 1.618033988749895
GOLDEN_ANGLE = 2.399963229728653  # radians (137.507764 degrees)

class RadialEmbedder:
    """
    Embeds tokens in Φ-radial coordinates (r, θ, z).
    
    r: radial distance from center (Φ-scaled shells)
    θ: angular position (golden angle distribution)
    z: semantic depth (hierarchical level)
    """
    
    def __init__(self, max_shells: int = 7, angular_resolution: int = 4096):
        self.max_shells = max_shells
        self.angular_resolution = angular_resolution
        self.phi = PHI
        self.golden_angle = GOLDEN_ANGLE
    
    def embed(self, token_id: int, total_tokens: int) -> Tuple[float, float, int]:
        """
        Embed token ID into (r, θ, z) radial coordinates.
        
        Uses Fibonacci sphere distribution for uniform coverage.
        """
        # Shell level (z) from token distribution
        shell = token_id % self.max_shells
        
        # Radius: r = Φ^shell
        r = self.phi ** shell
        
        # Angle: golden angle distribution
        theta = (token_id * self.golden_angle) % (2 * np.pi)
        
        return (r, theta, shell)
    
    def embed_sequence(self, token_ids: list[int]) -> Dict[int, Tuple]:
        """Embed a sequence of tokens."""
        return {
            i: self.embed(tid, len(token_ids))
            for i, tid in enumerate(token_ids)
        }
    
    def radial_distance(
        self, 
        coord1: Tuple[float, float, int],
        coord2: Tuple[float, float, int]
    ) -> float:
        """
        Compute radial distance between two coordinates.
        
        Uses polar metric: ds² = dr² + r²dθ²
        """
        r1, theta1, z1 = coord1
        r2, theta2, z2 = coord2
        
        dr = r2 - r1
        dtheta = abs(theta2 - theta1)
        # Handle wraparound
        if dtheta > np.pi:
            dtheta = 2 * np.pi - dtheta
        
        # Average radius for angular contribution
        r_avg = (r1 + r2) / 2
        
        return np.sqrt(dr**2 + (r_avg * dtheta)**2)
    
    def neighborhood_query(
        self,
        center_coord: Tuple[float, float, int],
        all_coords: Dict[int, Tuple],
        max_radius: float
    ) -> list[int]:
        """
        Find all tokens within radial distance max_radius.
        
        Returns list of token indices.
        """
        neighbors = []
        for idx, coord in all_coords.items():
            if self.radial_distance(center_coord, coord) <= max_radius:
                neighbors.append(idx)
        return neighbors
    
    def to_cartesian(self, coord: Tuple[float, float, int]) -> Tuple[float, float]:
        """Convert polar to cartesian coordinates."""
        r, theta, z = coord
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return (x, y)
    
    def to_pga_multivector(self, coord: Tuple[float, float, int]) -> np.ndarray:
        """
        Convert radial coordinates to 16D PGA multivector.
        
        Maps (r, θ) → scalar + bivector components
        """
        r, theta, z = coord
        
        # Initialize 16D vector (simplified PGA embedding)
        # [scalar, e01, e02, e03, e12, e13, e23, pseudo, twin...]
        multivector = np.zeros(16)
        
        # Scalar: radial magnitude (log-scaled for stability)
        multivector[0] = np.log(r + 1)
        
        # Bivector e12: encodes angular position
        multivector[4] = np.cos(theta)  # e12 component
        multivector[5] = np.sin(theta)  # e13 component
        
        # Pseudoscalar: shell level (discrete depth)
        multivector[7] = float(z)
        
        # Twin components (copy for validation)
        multivector[8:16] = multivector[0:8]
        
        return multivector

# Global embedder instance
EMBEDDER = RadialEmbedder()

"""
Feature Vector 7D - 7-Segment Edition

Computes the normalized 7-dimensional feature vector from
segment activation patterns.

Dimensions directly correspond to segments A-G:
0: Segment A (top horizontal)
1: Segment B (upper-right vertical)
2: Segment C (lower-right vertical)
3: Segment D (bottom horizontal)
4: Segment E (lower-left vertical)
5: Segment F (upper-left vertical)
6: Segment G (middle horizontal)
"""

import math
from typing import List, Dict, Tuple
from dataclasses import dataclass, field
from .segment_types import SegmentType, SegmentGrid, BoundingBox


@dataclass
class FeatureVector7D:
    """
    Normalized 7-dimensional feature vector for segment activation.
    
    Each dimension represents the relative activation strength of
    one segment across the entire composition.
    
    Dimensions (index: segment):
        0: A - Top horizontal
        1: B - Upper-right vertical  
        2: C - Lower-right vertical
        3: D - Bottom horizontal
        4: E - Lower-left vertical
        5: F - Upper-left vertical
        6: G - Middle horizontal
        
    The vector is normalized to unit length for trajectory calculation.
    """
    seg_a: float = 0.0  # Top
    seg_b: float = 0.0  # Upper-right
    seg_c: float = 0.0  # Lower-right
    seg_d: float = 0.0  # Bottom
    seg_e: float = 0.0  # Lower-left
    seg_f: float = 0.0  # Upper-left
    seg_g: float = 0.0  # Middle
    
    # Raw activation counts (for reference)
    _raw_counts: Dict[SegmentType, int] = field(default_factory=dict, repr=False)
    _magnitude: float = 0.0
    
    def __post_init__(self):
        self._recalculate_magnitude()
    
    def _recalculate_magnitude(self):
        """Recalculate vector magnitude."""
        self._magnitude = math.sqrt(
            self.seg_a**2 + self.seg_b**2 + self.seg_c**2 +
            self.seg_d**2 + self.seg_e**2 + self.seg_f**2 + self.seg_g**2
        )
    
    @property
    def magnitude(self) -> float:
        return self._magnitude
    
    @property
    def normalized(self) -> 'FeatureVector7D':
        """Return unit-normalized version of this vector."""
        if self._magnitude < 1e-10:
            return FeatureVector7D(0, 0, 0, 0, 0, 0, 0)
        
        return FeatureVector7D(
            seg_a=self.seg_a / self._magnitude,
            seg_b=self.seg_b / self._magnitude,
            seg_c=self.seg_c / self._magnitude,
            seg_d=self.seg_d / self._magnitude,
            seg_e=self.seg_e / self._magnitude,
            seg_f=self.seg_f / self._magnitude,
            seg_g=self.seg_g / self._magnitude,
            _raw_counts=self._raw_counts.copy(),
            _magnitude=1.0
        )
    
    def to_array(self) -> List[float]:
        """Return as array [A, B, C, D, E, F, G]."""
        return [self.seg_a, self.seg_b, self.seg_c, self.seg_d, 
                self.seg_e, self.seg_f, self.seg_g]
    
    def to_dict(self) -> Dict:
        """Serialize to dictionary."""
        return {
            "vector": self.to_array(),
            "magnitude": self._magnitude,
            "normalized": self.normalized.to_array() if self._magnitude > 0 else [0]*7,
            "raw_counts": {
                k.name if hasattr(k, 'name') else str(k): v
                for k, v in self._raw_counts.items()
            },
            "dominant_segment": self.dominant_segment,
            "segment_balance": self.segment_balance,
        }
    
    @property
    def dominant_segment(self) -> str:
        """Return the name of the most active segment."""
        segments = [
            ("A", self.seg_a),
            ("B", self.seg_b),
            ("C", self.seg_c),
            ("D", self.seg_d),
            ("E", self.seg_e),
            ("F", self.seg_f),
            ("G", self.seg_g),
        ]
        return max(segments, key=lambda x: x[1])[0]
    
    @property
    def segment_balance(self) -> float:
        """
        Measure of how balanced vs. dominated the segment distribution is.
        0 = all activation in one segment, 1 = perfectly balanced.
        """
        if self._magnitude < 1e-10:
            return 0.0
        
        values = [v for v in self.to_array() if v > 0]
        if not values:
            return 0.0
        
        # Shannon entropy normalized to max entropy (log(7))
        total = sum(values)
        probs = [v/total for v in values]
        entropy = -sum(p * math.log(p) for p in probs if p > 0)
        max_entropy = math.log(7)
        
        return entropy / max_entropy if max_entropy > 0 else 0.0
    
    @property
    def horizontal_vertical_ratio(self) -> float:
        """
        Ratio of horizontal to vertical segment activation.
        
        Returns:
            > 1: More horizontal
            < 1: More vertical
            = 1: Balanced
        """
        horizontal = self.seg_a + self.seg_d + self.seg_g
        vertical = self.seg_b + self.seg_c + self.seg_e + self.seg_f
        
        if vertical < 1e-10:
            return float('inf') if horizontal > 0 else 1.0
        
        return horizontal / vertical
    
    @property
    def enclosure_score(self) -> float:
        """
        Score for how "enclosed" the pattern is.
        Full enclosure = all of A, B, C, D, E, F active (like 0, O, D)
        """
        enclosure_segments = [self.seg_a, self.seg_b, self.seg_c, 
                              self.seg_d, self.seg_e, self.seg_f]
        return sum(enclosure_segments) / 6.0
    
    @property
    def top_bottom_balance(self) -> float:
        """Balance between top half (A, B, F) and bottom half (C, D, E)."""
        top = self.seg_a + self.seg_b + self.seg_f
        bottom = self.seg_c + self.seg_d + self.seg_e
        
        total = top + bottom
        if total < 1e-10:
            return 0.5
        
        return top / total
    
    def distance_to(self, other: 'FeatureVector7D') -> float:
        """Euclidean distance to another 7D vector."""
        return math.sqrt(sum(
            (a - b) ** 2 
            for a, b in zip(self.to_array(), other.to_array())
        ))
    
    def cosine_similarity(self, other: 'FeatureVector7D') -> float:
        """Cosine similarity to another 7D vector (-1 to 1)."""
        dot = sum(a * b for a, b in zip(self.to_array(), other.to_array()))
        mag_product = self._magnitude * other._magnitude
        if mag_product < 1e-10:
            return 0.0
        return dot / mag_product


class FeatureVectorCalculator:
    """
    Calculator for extracting 7D feature vectors from segment grids.
    """
    
    def __init__(self, 
                 position_weight: float = 1.0,
                 intensity_weight: float = 0.5):
        self.position_weight = position_weight
        self.intensity_weight = intensity_weight
    
    def calculate(self, grids: List[SegmentGrid]) -> FeatureVector7D:
        """
        Calculate 7D feature vector from segment grids.
        
        The vector represents the aggregate activation pattern
        across all character positions.
        
        Args:
            grids: List of segment grids (one per character position)
            
        Returns:
            FeatureVector7D with computed activation weights
        """
        # Accumulate raw counts
        raw_counts = {seg: 0 for seg in SegmentType}
        
        for grid in grids:
            for seg in SegmentType:
                if grid.segments[seg].active:
                    raw_counts[seg] += 1
        
        # Calculate weighted contributions
        # Position-based: earlier positions may have more weight
        contributions = {seg: 0.0 for seg in SegmentType}
        
        total_grids = len(grids) if grids else 1
        
        for i, grid in enumerate(grids):
            # Position weight (center positions get slight boost)
            pos_factor = 1.0 + 0.1 * (1 - abs(i - total_grids/2) / (total_grids/2 + 1))
            
            for seg in SegmentType:
                if grid.segments[seg].active:
                    base_contrib = 1.0
                    intensity = grid.segments[seg].intensity
                    
                    contributions[seg] += (
                        base_contrib * 
                        self.position_weight * pos_factor *
                        (1 + self.intensity_weight * intensity)
                    )
        
        # Normalize by grid count
        for seg in SegmentType:
            contributions[seg] /= total_grids
        
        # Create feature vector
        vector = FeatureVector7D(
            seg_a=contributions[SegmentType.A],
            seg_b=contributions[SegmentType.B],
            seg_c=contributions[SegmentType.C],
            seg_d=contributions[SegmentType.D],
            seg_e=contributions[SegmentType.E],
            seg_f=contributions[SegmentType.F],
            seg_g=contributions[SegmentType.G],
            _raw_counts=raw_counts
        )
        
        return vector
    
    def calculate_trajectory(
        self,
        source: FeatureVector7D,
        target: FeatureVector7D
    ) -> Dict:
        """
        Calculate trajectory from source to target in 7D segment space.
        
        Returns trajectory information for semantic navigation.
        """
        src_norm = source.normalized
        tgt_norm = target.normalized
        
        distance = src_norm.distance_to(tgt_norm)
        similarity = src_norm.cosine_similarity(tgt_norm)
        
        # Component-wise deltas
        deltas = [
            tgt_norm.to_array()[i] - src_norm.to_array()[i]
            for i in range(7)
        ]
        
        # Find dominant change
        abs_deltas = [(i, abs(d)) for i, d in enumerate(deltas)]
        abs_deltas.sort(key=lambda x: x[1], reverse=True)
        
        segment_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        
        return {
            "distance": distance,
            "similarity": similarity,
            "deltas": {segment_names[i]: deltas[i] for i in range(7)},
            "dominant_change": segment_names[abs_deltas[0][0]],
            "direction": deltas,  # Raw 7D direction vector
        }

"""
Glyphobetic Decomposer - 7-Segment Edition

Main decomposer for 7-segment display glyphoform analysis.
"""

import math
from typing import Dict, List, Optional, Any, Tuple
from collections import Counter

from .segment_types import (
    SegmentType,
    SegmentGrid,
    SegmentAdjacency,
    SegmentActivationPattern,
    GlyphoformAST,
    BoundingBox,
    Centroid,
    Coordinate3D,
    CompositionMode,
    GlyphobeticFeatures,
)
from .feature_vector import FeatureVector7D, FeatureVectorCalculator


class GlyphobeticDecomposer:
    """
    7-Segment Glyphobetic Decomposer.
    
    Analyzes glyphoforms represented as 7-segment display grids,
    producing geometric analysis for trajectory calculation.
    
    Usage:
        decomposer = GlyphobeticDecomposer()
        ast = create_glyphoform_ast("HELLO")
        features = decomposer.decompose(ast)
        
        # Access segment bitmaps
        print(features.bitmaps)  # [119, 121, 56, 56, 63] etc.
        
        # Access 7D feature vector
        print(features.feature_vector.to_dict())
    """
    
    def __init__(self, 
                 normalize_features: bool = True,
                 grid_width: float = 1.0,
                 grid_height: float = 2.0):
        """
        Initialize the decomposer.
        
        Args:
            normalize_features: Whether to normalize the 7D feature vector
            grid_width: Width of a single segment grid
            grid_height: Height of a single segment grid
        """
        self.normalize_features = normalize_features
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.feature_calculator = FeatureVectorCalculator()
    
    def decompose(self, ast: GlyphoformAST) -> GlyphobeticFeatures:
        """
        Decompose a 7-segment glyphoform AST into geometric features.
        
        Produces:
        - Segment activation bitmaps per position
        - Bounding box of composition
        - Centroid of active segments
        - 7D feature vector (segment activation profile)
        - Pattern analysis
        - Composition metrics
        
        Args:
            ast: The glyphoform AST with segment grids
            
        Returns:
            GlyphobeticFeatures containing all analysis
        """
        features = GlyphobeticFeatures()
        
        # 1. Extract bitmaps
        features.bitmaps = ast.bitmap_array
        
        # 2. Analyze segment activation patterns
        features.segment_patterns = self._analyze_patterns(ast)
        
        # 3. Calculate bounding box
        features.bounding_box = self._calculate_bounding_box(ast)
        
        # 4. Calculate centroid
        features.centroid = self._calculate_centroid(ast)
        
        # 5. Calculate 7D feature vector
        raw_vector = self.feature_calculator.calculate(ast.grids)
        features.feature_vector = (
            raw_vector.normalized if self.normalize_features else raw_vector
        )
        
        # 6. Determine composition mode
        features.composition_mode = self._determine_composition_mode(ast)
        
        # 7. Calculate adjacencies
        features.adjacency_count = len(ast.adjacencies)
        
        # 8. Calculate derived metrics
        features.fill_ratio = self._calculate_fill_ratio(ast)
        features.symmetry_score = self._calculate_symmetry(ast)
        features.density = self._calculate_density(ast, features.bounding_box)
        
        return features
    
    def decompose_to_dict(self, ast: GlyphoformAST) -> Dict[str, Any]:
        """Decompose and return as dictionary."""
        features = self.decompose(ast)
        return features.to_dict()
    
    def decompose_batch(self, asts: List[GlyphoformAST]) -> List[GlyphobeticFeatures]:
        """Decompose multiple ASTs."""
        return [self.decompose(ast) for ast in asts]
    
    def _analyze_patterns(self, ast: GlyphoformAST) -> SegmentActivationPattern:
        """Analyze segment activation patterns across positions."""
        pattern = SegmentActivationPattern()
        
        if not ast.grids:
            return pattern
        
        # Per-position analysis
        pattern.position_patterns = [
            {
                "position": i,
                "bitmap": grid.bitmap,
                "bitmap_binary": format(grid.bitmap, '07b'),
                "active_count": grid.active_count,
                "active_segments": [s.name for s in grid.active_segments]
            }
            for i, grid in enumerate(ast.grids)
        ]
        
        # Most common bitmap
        bitmap_counts = Counter(g.bitmap for g in ast.grids)
        if bitmap_counts:
            pattern.most_common_bitmap = bitmap_counts.most_common(1)[0][0]
        
        # Pattern entropy (Shannon entropy of bitmap distribution)
        total = len(ast.grids)
        pattern.pattern_entropy = -sum(
            (count/total) * math.log(count/total)
            for count in bitmap_counts.values()
        ) if total > 0 else 0.0
        
        # Pattern transitions (how many times bitmap changes between positions)
        pattern.pattern_transitions = sum(
            1 for i in range(1, len(ast.grids))
            if ast.grids[i].bitmap != ast.grids[i-1].bitmap
        )
        
        # Segment frequency (how often each segment is active)
        total_positions = len(ast.grids)
        for seg in SegmentType:
            count = sum(1 for g in ast.grids if g.segments[seg].active)
            pattern.segment_frequency[seg] = count / total_positions if total_positions > 0 else 0.0
        
        return pattern
    
    def _calculate_bounding_box(self, ast: GlyphoformAST) -> BoundingBox:
        """Calculate bounding box of the composition."""
        if not ast.grids:
            return BoundingBox(0, 0, 0, 0, 0, 0)
        
        # Each grid is positioned at (grid.position_x, grid.position_y)
        # Grid spans from position to position + (width, height)
        
        xs = []
        ys = []
        
        for grid in ast.grids:
            # Grid corners
            xs.extend([
                grid.position_x,
                grid.position_x + self.grid_width
            ])
            ys.extend([
                grid.position_y,
                grid.position_y + self.grid_height
            ])
        
        return BoundingBox(
            min_x=min(xs),
            min_y=min(ys),
            min_z=0.0,
            max_x=max(xs),
            max_y=max(ys),
            max_z=0.0
        )
    
    def _calculate_centroid(self, ast: GlyphoformAST) -> Centroid:
        """Calculate centroid of active segment positions."""
        if not ast.grids:
            return Centroid(Coordinate3D(0, 0, 0), 0, 0)
        
        # Segment positions within a grid (normalized 0-1)
        segment_positions = {
            SegmentType.A: (0.5, 0.0),    # Top middle
            SegmentType.B: (1.0, 0.25),   # Upper right
            SegmentType.C: (1.0, 0.75),   # Lower right
            SegmentType.D: (0.5, 1.0),    # Bottom middle
            SegmentType.E: (0.0, 0.75),   # Lower left
            SegmentType.F: (0.0, 0.25),   # Upper left
            SegmentType.G: (0.5, 0.5),    # Middle
        }
        
        total_mass = 0.0
        sum_x = 0.0
        sum_y = 0.0
        
        segment_points = []
        
        for grid in ast.grids:
            for seg in SegmentType:
                if grid.segments[seg].active:
                    rel_x, rel_y = segment_positions[seg]
                    abs_x = grid.position_x + rel_x * self.grid_width
                    abs_y = grid.position_y + rel_y * self.grid_height
                    
                    segment_points.append((abs_x, abs_y))
                    sum_x += abs_x
                    sum_y += abs_y
                    total_mass += 1.0
        
        if total_mass == 0:
            return Centroid(Coordinate3D(0, 0, 0), 0, 0)
        
        centroid_x = sum_x / total_mass
        centroid_y = sum_y / total_mass
        
        # Calculate spread (std dev from centroid)
        if len(segment_points) > 1:
            variance = sum(
                (x - centroid_x)**2 + (y - centroid_y)**2
                for x, y in segment_points
            ) / len(segment_points)
            spread = math.sqrt(variance)
        else:
            spread = 0.0
        
        return Centroid(
            position=Coordinate3D(centroid_x, centroid_y, 0),
            mass=total_mass,
            spread=spread
        )
    
    def _determine_composition_mode(self, ast: GlyphoformAST) -> CompositionMode:
        """Determine how grids are composed spatially."""
        if len(ast.grids) < 2:
            return CompositionMode.SPACED
        
        # Check spacing between consecutive grids
        gaps = []
        for i in range(1, len(ast.grids)):
            prev_end = ast.grids[i-1].position_x + self.grid_width
            curr_start = ast.grids[i].position_x
            gap = curr_start - prev_end
            gaps.append(gap)
        
        avg_gap = sum(gaps) / len(gaps) if gaps else 0
        
        # Thresholds
        if avg_gap < 0:
            return CompositionMode.OVERLAPPING
        elif avg_gap < 0.1:
            return CompositionMode.TOUCHING
        else:
            return CompositionMode.SPACED
    
    def _calculate_fill_ratio(self, ast: GlyphoformAST) -> float:
        """Calculate ratio of active to possible segments."""
        total_possible = len(ast.grids) * 7
        if total_possible == 0:
            return 0.0
        
        return ast.total_active_segments / total_possible
    
    def _calculate_symmetry(self, ast: GlyphoformAST) -> float:
        """
        Calculate symmetry score of the composition.
        
        Returns 0-1 where 1 is perfectly symmetrical.
        """
        if len(ast.grids) <= 1:
            return 1.0
        
        # Check horizontal symmetry (mirror around center)
        n = len(ast.grids)
        matches = 0
        comparisons = 0
        
        for i in range(n // 2):
            j = n - 1 - i
            if ast.grids[i].bitmap == ast.grids[j].bitmap:
                matches += 1
            comparisons += 1
        
        return matches / comparisons if comparisons > 0 else 1.0
    
    def _calculate_density(self, ast: GlyphoformAST, bbox: BoundingBox) -> float:
        """Calculate segment density (segments per unit area)."""
        area = bbox.width * bbox.height
        if area < 1e-10:
            return 0.0
        
        return ast.total_active_segments / area


# ============================================================================
# Factory Functions
# ============================================================================

def decompose_word(word: str,
                   letter_spacing: float = 1.2,
                   grid_scale: float = 1.0) -> GlyphobeticFeatures:
    """
    Convenience function to decompose a word directly.
    
    Args:
        word: The word to decompose
        letter_spacing: Distance between letter centers
        grid_scale: Size multiplier for grids
        
    Returns:
        GlyphobeticFeatures for the word
    """
    ast = create_simple_ast(word, letter_spacing, grid_scale)
    decomposer = GlyphobeticDecomposer(
        grid_width=1.0 * grid_scale,
        grid_height=2.0 * grid_scale
    )
    return decomposer.decompose(ast)


def create_simple_ast(word: str,
                      letter_spacing: float = 1.2,
                      grid_scale: float = 1.0) -> GlyphoformAST:
    """
    Create a simple AST from a word using standard 7-segment encoding.
    
    Args:
        word: Input word
        letter_spacing: Distance between grid centers
        grid_scale: Scale factor for grid size
        
    Returns:
        GlyphoformAST with SegmentGrids
    """
    grids = []
    
    for i, char in enumerate(word):
        grid = SegmentGrid.from_letter(char)
        grid.character = char
        grid.grid_x = i
        grid.position_x = i * letter_spacing
        grid.position_y = 0
        grids.append(grid)
    
    return GlyphoformAST(
        source_word=word,
        grids=grids,
        letter_spacing=letter_spacing
    )


def create_from_bitmaps(bitmaps: List[int],
                        letter_spacing: float = 1.2) -> GlyphoformAST:
    """
    Create AST from pre-computed 7-bit bitmaps.
    
    Args:
        bitmaps: List of 7-bit integers
        letter_spacing: Distance between grid centers
        
    Returns:
        GlyphoformAST
    """
    grids = [
        SegmentGrid.from_bitmap(bm, position_x=i * letter_spacing)
        for i, bm in enumerate(bitmaps)
    ]
    
    return GlyphoformAST(
        source_word="",
        grids=grids,
        letter_spacing=letter_spacing
    )


def compute_trajectory(word1: str, word2: str) -> Dict[str, Any]:
    """
    Compute trajectory between two words in 7D segment space.
    
    Returns trajectory information for semantic navigation.
    """
    features1 = decompose_word(word1)
    features2 = decompose_word(word2)
    
    vector1 = features1.feature_vector
    vector2 = features2.feature_vector
    
    calc = FeatureVectorCalculator()
    trajectory = calc.calculate_trajectory(vector1, vector2)
    
    return {
        "source": word1,
        "target": word2,
        "source_bitmap": features1.bitmaps,
        "target_bitmap": features2.bitmaps,
        "source_vector": vector1.to_dict(),
        "target_vector": vector2.to_dict(),
        "trajectory": trajectory
    }

"""
Glyphobetic Decomposer - 7-Segment Display Edition

Transforms glyphoform ASTs into 7-segment display analysis.
Uses canonical digital clock grid: segments A-G.
"""

from .decomposer import GlyphobeticDecomposer, decompose_word, create_simple_ast, compute_trajectory
from .segment_types import (
    SegmentType,
    SegmentState,
    SegmentGrid,
    GlyphoformAST,
    SegmentActivationPattern,
    BoundingBox,
    Centroid,
    CompositionMode,
    GlyphobeticFeatures,
)
from .feature_vector import FeatureVector7D, FeatureVectorCalculator

__version__ = "0.2.0-7segment"
__all__ = [
    "GlyphobeticDecomposer",
    "decompose_word",
    "create_simple_ast",
    "compute_trajectory",
    "SegmentType",
    "SegmentState",
    "SegmentGrid",
    "GlyphoformAST",
    "SegmentActivationPattern",
    "BoundingBox",
    "Centroid",
    "CompositionMode",
    "GlyphobeticFeatures",
    "FeatureVector7D",
    "FeatureVectorCalculator",
]

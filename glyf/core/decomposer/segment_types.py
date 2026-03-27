"""
7-Segment Display Type Definitions

Canonical digital clock grid representation.
Segments: A(top), B(upper-right), C(lower-right), D(bottom), E(lower-left), F(upper-left), G(middle)

    A
  F   B
    G
  E   C
    D
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Set
import math


class SegmentType(Enum):
    """
    The 7 canonical segments of a digital display.
    
        A
      F   B
        G
      E   C
        D
    """
    A = 0  # Top horizontal
    B = 1  # Upper-right vertical
    C = 2  # Lower-right vertical
    D = 3  # Bottom horizontal
    E = 4  # Lower-left vertical
    F = 5  # Upper-left vertical
    G = 6  # Middle horizontal


class CompositionMode(Enum):
    """How multiple letterforms relate spatially."""
    OVERLAPPING = auto()   # Segments overlay each other
    TOUCHING = auto()      # Segments meet at edges
    SPACED = auto()        # Segments have gap between them


@dataclass
class SegmentState:
    """
    State of a single segment.
    
    Binary on/off plus intensity/brightness for future extension.
    """
    segment: SegmentType
    active: bool = False
    intensity: float = 1.0  # 0.0 to 1.0 for partial activation
    
    def to_bit(self) -> int:
        """Return 1 if active, 0 if inactive."""
        return 1 if self.active else 0


@dataclass
class SegmentGrid:
    """
    Complete 7-segment display grid for a single character position.
    
    Represents one "digit" position with all 7 segments.
    """
    # Segment states indexed by SegmentType
    segments: Dict[SegmentType, SegmentState] = field(default_factory=dict)
    
    # Grid position in larger composition
    grid_x: int = 0
    grid_y: int = 0
    
    # Physical position (for multi-letter analysis)
    position_x: float = 0.0
    position_y: float = 0.0
    
    # Character this grid represents
    character: str = ""
    
    def __post_init__(self):
        # Initialize all segments as inactive if not provided
        for seg in SegmentType:
            if seg not in self.segments:
                self.segments[seg] = SegmentState(seg, active=False)
    
    @property
    def bitmap(self) -> int:
        """
        Return 7-bit integer representing segment activation.
        Bit 0 = A, Bit 1 = B, ..., Bit 6 = G
        """
        result = 0
        for seg_type in SegmentType:
            if self.segments[seg_type].active:
                result |= (1 << seg_type.value)
        return result
    
    @property
    def active_segments(self) -> List[SegmentType]:
        """Return list of currently active segments."""
        return [s for s in SegmentType if self.segments[s].active]
    
    @property
    def active_count(self) -> int:
        """Count of active segments."""
        return sum(1 for s in SegmentType if self.segments[s].active)
    
    @property
    def is_empty(self) -> bool:
        """True if no segments are active."""
        return self.active_count == 0
    
    def set_segment(self, segment: SegmentType, active: bool = True):
        """Activate or deactivate a segment."""
        self.segments[segment] = SegmentState(segment, active=active)
    
    def activate_segments(self, segments: List[SegmentType]):
        """Activate multiple segments at once."""
        for seg in segments:
            self.set_segment(seg, True)
    
    def to_array(self) -> List[int]:
        """Return as array [A, B, C, D, E, F, G] of 0/1."""
        return [self.segments[s].to_bit() for s in SegmentType]
    
    def to_dict(self) -> Dict:
        """Serialize to dictionary."""
        return {
            "bitmap": self.bitmap,
            "bitmap_binary": format(self.bitmap, '07b'),
            "active_segments": [s.name for s in self.active_segments],
            "active_count": self.active_count,
            "character": self.character,
            "grid_position": {"x": self.grid_x, "y": self.grid_y},
            "physical_position": {"x": self.position_x, "y": self.position_y},
            "segment_states": {
                s.name: self.segments[s].active 
                for s in SegmentType
            }
        }
    
    @classmethod
    def from_bitmap(cls, bitmap: int, character: str = "") -> 'SegmentGrid':
        """Create SegmentGrid from 7-bit integer."""
        grid = cls(character=character)
        for seg in SegmentType:
            if bitmap & (1 << seg.value):
                grid.set_segment(seg, True)
        return grid
    
    @classmethod
    def from_letter(cls, letter: str) -> 'SegmentGrid':
        """Create standard 7-segment representation of a letter."""
        letter = letter.upper()
        grid = cls(character=letter)
        
        # Standard 7-segment patterns for letters
        # Based on common digital display encodings
        patterns = {
            'A': [SegmentType.A, SegmentType.B, SegmentType.C, SegmentType.E, SegmentType.F, SegmentType.G],
            'B': [SegmentType.C, SegmentType.D, SegmentType.E, SegmentType.F, SegmentType.G],
            'C': [SegmentType.A, SegmentType.D, SegmentType.E, SegmentType.F],
            'D': [SegmentType.B, SegmentType.C, SegmentType.D, SegmentType.E, SegmentType.G],
            'E': [SegmentType.A, SegmentType.D, SegmentType.E, SegmentType.F, SegmentType.G],
            'F': [SegmentType.A, SegmentType.E, SegmentType.F, SegmentType.G],
            'G': [SegmentType.A, SegmentType.C, SegmentType.D, SegmentType.E, SegmentType.F],
            'H': [SegmentType.B, SegmentType.C, SegmentType.E, SegmentType.F, SegmentType.G],
            'I': [SegmentType.E, SegmentType.F],
            'J': [SegmentType.B, SegmentType.C, SegmentType.D],
            'K': [SegmentType.B, SegmentType.C, SegmentType.E, SegmentType.F, SegmentType.G],  # Approximation
            'L': [SegmentType.D, SegmentType.E, SegmentType.F],
            'M': [SegmentType.A, SegmentType.C, SegmentType.E],  # Limited on 7-seg
            'N': [SegmentType.A, SegmentType.B, SegmentType.C, SegmentType.E, SegmentType.F],
            'O': [SegmentType.A, SegmentType.B, SegmentType.C, SegmentType.D, SegmentType.E, SegmentType.F],
            'P': [SegmentType.A, SegmentType.B, SegmentType.E, SegmentType.F, SegmentType.G],
            'Q': [SegmentType.A, SegmentType.B, SegmentType.C, SegmentType.F, SegmentType.G],
            'R': [SegmentType.A, SegmentType.B, SegmentType.E, SegmentType.F],
            'S': [SegmentType.A, SegmentType.C, SegmentType.D, SegmentType.F, SegmentType.G],
            'T': [SegmentType.D, SegmentType.E, SegmentType.F, SegmentType.G],
            'U': [SegmentType.B, SegmentType.C, SegmentType.D, SegmentType.E, SegmentType.F],
            'V': [SegmentType.B, SegmentType.C, SegmentType.E, SegmentType.F],
            'W': [SegmentType.B, SegmentType.D, SegmentType.F],  # Limited on 7-seg
            'X': [SegmentType.B, SegmentType.C, SegmentType.E, SegmentType.F, SegmentType.G],  # Same as H
            'Y': [SegmentType.B, SegmentType.C, SegmentType.D, SegmentType.F, SegmentType.G],
            'Z': [SegmentType.A, SegmentType.B, SegmentType.D, SegmentType.E, SegmentType.G],
            '0': [SegmentType.A, SegmentType.B, SegmentType.C, SegmentType.D, SegmentType.E, SegmentType.F],
            '1': [SegmentType.B, SegmentType.C],
            '2': [SegmentType.A, SegmentType.B, SegmentType.D, SegmentType.E, SegmentType.G],
            '3': [SegmentType.A, SegmentType.B, SegmentType.C, SegmentType.D, SegmentType.G],
            '4': [SegmentType.B, SegmentType.C, SegmentType.F, SegmentType.G],
            '5': [SegmentType.A, SegmentType.C, SegmentType.D, SegmentType.F, SegmentType.G],
            '6': [SegmentType.A, SegmentType.C, SegmentType.D, SegmentType.E, SegmentType.F, SegmentType.G],
            '7': [SegmentType.A, SegmentType.B, SegmentType.C],
            '8': [SegmentType.A, SegmentType.B, SegmentType.C, SegmentType.D, SegmentType.E, SegmentType.F, SegmentType.G],
            '9': [SegmentType.A, SegmentType.B, SegmentType.C, SegmentType.D, SegmentType.F, SegmentType.G],
            ' ': [],  # Space
            '-': [SegmentType.G],  # Minus
            '_': [SegmentType.D],  # Underscore
        }
        
        if letter in patterns:
            grid.activate_segments(patterns[letter])
        
        return grid


@dataclass
class Coordinate3D:
    """3D coordinate for geometric calculations."""
    x: float
    y: float
    z: float = 0.0
    
    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)


@dataclass
class BoundingBox:
    """Axis-aligned bounding box for glyphoform composition."""
    min_x: float
    min_y: float
    min_z: float
    max_x: float
    max_y: float
    max_z: float
    
    @property
    def width(self) -> float:
        return self.max_x - self.min_x
    
    @property
    def height(self) -> float:
        return self.max_y - self.min_y
    
    @property
    def depth(self) -> float:
        return self.max_z - self.min_z
    
    @property
    def center(self) -> Coordinate3D:
        return Coordinate3D(
            (self.min_x + self.max_x) / 2,
            (self.min_y + self.max_y) / 2,
            (self.min_z + self.max_z) / 2
        )
    
    def to_dict(self) -> Dict:
        return {
            "min": {"x": self.min_x, "y": self.min_y, "z": self.min_z},
            "max": {"x": self.max_x, "y": self.max_y, "z": self.max_z},
            "dimensions": {
                "width": self.width,
                "height": self.height,
                "depth": self.depth
            }
        }


@dataclass
class Centroid:
    """Geometric center of the segment activation pattern."""
    position: Coordinate3D
    mass: float = 1.0  # Weighted by active segment count
    spread: float = 0.0  # How dispersed the segments are
    
    def to_dict(self) -> Dict:
        return {
            "x": self.position.x,
            "y": self.position.y,
            "z": self.position.z,
            "mass": self.mass,
            "spread": self.spread
        }


@dataclass
class SegmentAdjacency:
    """
    Tracks which segments touch between adjacent letter positions.
    """
    # From position i to position i+1
    from_position: int
    to_position: int
    
    # Which segments touch
    touching_segments: List[Tuple[SegmentType, SegmentType]] = field(default_factory=list)
    
    # Gap distance
    gap: float = 0.0
    
    @property
    def is_connected(self) -> bool:
        """True if any segments touch."""
        return len(self.touching_segments) > 0


@dataclass
class GlyphoformAST:
    """
    Abstract Syntax Tree for 7-segment glyphoform.
    
    Contains multiple SegmentGrids (one per character position)
    with spatial relationships.
    """
    source_word: str = ""
    grids: List[SegmentGrid] = field(default_factory=list)
    
    # Composition mode
    composition_mode: CompositionMode = CompositionMode.SPACED
    
    # Spacing parameters
    letter_spacing: float = 1.0  # Distance between grid centers
    grid_scale: float = 1.0      # Size of each grid
    
    # Computed adjacencies
    adjacencies: List[SegmentAdjacency] = field(default_factory=list)
    
    def __post_init__(self):
        # Set grid positions if not already set
        for i, grid in enumerate(self.grids):
            if grid.grid_x == 0 and grid.grid_y == 0:
                grid.grid_x = i
                grid.position_x = i * self.letter_spacing
    
    @property
    def length(self) -> int:
        """Number of character positions."""
        return len(self.grids)
    
    @property
    def total_active_segments(self) -> int:
        """Total count of active segments across all grids."""
        return sum(grid.active_count for grid in self.grids)
    
    @property
    def bitmap_array(self) -> List[int]:
        """Array of 7-bit bitmaps for each position."""
        return [grid.bitmap for grid in self.grids]
    
    def get_grid(self, index: int) -> Optional[SegmentGrid]:
        """Get grid at position."""
        if 0 <= index < len(self.grids):
            return self.grids[index]
        return None
    
    def to_dict(self) -> Dict:
        """Serialize full AST."""
        return {
            "source_word": self.source_word,
            "length": self.length,
            "composition_mode": self.composition_mode.name,
            "letter_spacing": self.letter_spacing,
            "total_active_segments": self.total_active_segments,
            "bitmap_array": self.bitmap_array,
            "bitmap_array_binary": [format(b, '07b') for b in self.bitmap_array],
            "grids": [g.to_dict() for g in self.grids],
        }


@dataclass
class SegmentActivationPattern:
    """
    Analyzed pattern of segment activation across the composition.
    """
    # Per-position analysis
    position_patterns: List[Dict] = field(default_factory=list)
    
    # Global patterns
    most_common_bitmap: int = 0
    pattern_entropy: float = 0.0  # How varied the patterns are
    pattern_transitions: int = 0   # How many times pattern changes
    
    # Segment-specific analysis
    segment_frequency: Dict[SegmentType, float] = field(default_factory=dict)
    segment_correlations: Dict[Tuple[SegmentType, SegmentType], float] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "most_common_bitmap": self.most_common_bitmap,
            "most_common_binary": format(self.most_common_bitmap, '07b'),
            "pattern_entropy": self.pattern_entropy,
            "pattern_transitions": self.pattern_transitions,
            "segment_frequency": {
                k.name if hasattr(k, 'name') else str(k): v
                for k, v in self.segment_frequency.items()
            },
        }


@dataclass
class GlyphobeticFeatures:
    """
    Complete geometric analysis output.
    """
    # Segment activation analysis
    segment_patterns: Optional[SegmentActivationPattern] = None
    
    # Per-position bitmaps
    bitmaps: List[int] = field(default_factory=list)
    
    # Bounding box
    bounding_box: Optional[BoundingBox] = None
    
    # Centroid of segment activation
    centroid: Optional[Centroid] = None
    
    # 7D feature vector (normalized segment activation profile)
    feature_vector: Optional['FeatureVector7D'] = None
    
    # Composition metrics
    composition_mode: CompositionMode = CompositionMode.SPACED
    adjacency_count: int = 0
    
    # Derived metrics
    fill_ratio: float = 0.0  # Active segments / total possible
    symmetry_score: float = 0.0  # How symmetrical the pattern is
    density: float = 0.0  # Segments per unit area
    
    def to_dict(self) -> Dict:
        return {
            "segment_patterns": self.segment_patterns.to_dict() if self.segment_patterns else None,
            "bitmaps": self.bitmaps,
            "bitmaps_binary": [format(b, '07b') for b in self.bitmaps],
            "bounding_box": self.bounding_box.to_dict() if self.bounding_box else None,
            "centroid": self.centroid.to_dict() if self.centroid else None,
            "feature_vector": self.feature_vector.to_dict() if self.feature_vector else None,
            "composition_mode": self.composition_mode.name,
            "adjacency_count": self.adjacency_count,
            "fill_ratio": self.fill_ratio,
            "symmetry_score": self.symmetry_score,
            "density": self.density,
        }

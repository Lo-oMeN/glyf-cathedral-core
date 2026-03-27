"""
Universal Glyphabetic Dictionary - 7-Segment Canonical Display

Encoding semantic meaning through 7-segment display activation patterns.
Each segment carries directional/spatial meaning:
  A=Above/Crown, B/C=Outward, D=Below/Foundation, E/F=Inward, G=Balance
"""

from typing import List, Tuple, Dict, NamedTuple
import math

# Segment definitions
SEGMENTS = {
    'A': {'position': 'top', 'meaning': 'Crown/Apex/Above', 'essence': 'authority, summit, visibility, emergence'},
    'B': {'position': 'upper-right', 'meaning': 'Outward/External', 'essence': 'expression, projection, giving, surface'},
    'C': {'position': 'lower-right', 'meaning': 'Outward/External', 'essence': 'extension, reach, conclusion, edge'},
    'D': {'position': 'bottom', 'meaning': 'Foundation/Below', 'essence': 'support, root, grounding, source'},
    'E': {'position': 'lower-left', 'meaning': 'Inward/Internal', 'essence': 'reception, containment, gathering'},
    'F': {'position': 'upper-left', 'meaning': 'Inward/Internal', 'essence': 'intention, origin, initiation, core'},
    'G': {'position': 'middle', 'meaning': 'Balance/Bridge', 'essence': 'connection, mediation, transition, axis'}
}

SEGMENT_ORDER = ['A', 'B', 'C', 'D', 'E', 'F', 'G']


class SegmentVector(NamedTuple):
    """7-segment activation vector [A, B, C, D, E, F, G]"""
    A: float  # Crown/Apex/Above
    B: float  # Outward/External (upper)
    C: float  # Outward/External (lower)
    D: float  # Foundation/Below
    E: float  # Inward/Internal (lower)
    F: float  # Inward/Internal (upper)
    G: float  # Balance/Bridge
    
    def to_list(self) -> List[float]:
        return [self.A, self.B, self.C, self.D, self.E, self.F, self.G]
    
    @classmethod
    def from_list(cls, vec: List[float]) -> 'SegmentVector':
        return cls(*vec)
    
    def active(self, threshold: float = 0.5) -> List[str]:
        """Return active segments above threshold"""
        segments = []
        for i, seg in enumerate(SEGMENT_ORDER):
            if self.to_list()[i] >= threshold:
                segments.append(seg)
        return segments
    
    def pattern_name(self) -> str:
        """Generate pattern name like 'A-D-G' for active segments"""
        active = self.active(0.5)
        return '-'.join(active) if active else "null"
    
    def vertical_score(self) -> float:
        """Measure of vertical extension (A-G-D axis)"""
        return (self.A + self.G + self.D) / 3
    
    def lateral_balance(self) -> float:
        """Positive = rightward, Negative = leftward, 0 = balanced"""
        outward = self.B + self.C
        inward = self.E + self.F
        return (outward - inward) / 2
    
    def enclosure_score(self) -> float:
        """Measure of how enclosed the pattern is"""
        perimeter = self.A + self.B + self.C + self.D + self.E + self.F
        return perimeter / 6


class SegmentDecoder:
    """Decodes 7-segment activation patterns into semantic meanings"""
    
    def __init__(self):
        self.lexicon = self._build_lexicon()
    
    def _build_lexicon(self) -> Dict[str, SegmentVector]:
        """
        Build semantic lexicon using 7-segment activation patterns.
        Each word's meaning is encoded as which segments are active.
        """
        return {
            # === VERTICAL EXTENSION (Tower concepts) ===
            
            # TOWER: Full vertical A-G-D spine, minimal sides
            # Meaning: Vertical aspiration, reaching upward from foundation
            'TOWER': SegmentVector(1.0, 0.2, 0.2, 1.0, 0.2, 0.2, 1.0),
            
            # TREE: A-G-D spine with outward growth on sides
            # Meaning: Rooted growth with spreading branches
            'TREE': SegmentVector(1.0, 0.6, 0.5, 1.0, 0.4, 0.5, 1.0),
            
            # PILLAR: Pure vertical A-D without G (solid)
            # Meaning: Unbroken support, strength without mediation
            'PILLAR': SegmentVector(1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0),
            
            # === FOUNDATION CONCEPTS (D-centric) ===
            
            # ROOT: D strong with inward gathering E,F
            # Meaning: Deep grounding, internal sourcing
            'ROOT': SegmentVector(0.3, 0.1, 0.1, 1.0, 0.8, 0.8, 0.0),
            
            # BASE: D with balanced sides
            # Meaning: Stable platform, grounded presence
            'BASE': SegmentVector(0.2, 0.5, 0.5, 1.0, 0.5, 0.5, 0.0),
            
            # === CROWN CONCEPTS (A-centric) ===
            
            # CROWN: A dominant with outward projection B
            # Meaning: Authority, visibility, peak achievement
            'CROWN': SegmentVector(1.0, 0.8, 0.3, 0.2, 0.1, 0.3, 0.0),
            
            # SUMMIT: A with inward focus F
            # Meaning: Peak insight, vision from above
            'SUMMIT': SegmentVector(1.0, 0.2, 0.1, 0.0, 0.1, 0.8, 0.0),
            
            # === BRIDGE/BALANCE CONCEPTS (G-centric) ===
            
            # BRIDGE: G dominant with A and D anchors
            # Meaning: Connection between realms, mediation
            'BRIDGE': SegmentVector(0.6, 0.2, 0.2, 0.6, 0.2, 0.2, 1.0),
            
            # AXIS: Pure G alone
            # Meaning: Central line, core alignment, spine
            'AXIS': SegmentVector(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0),
            
            # GATE: G horizontal with A crown
            # Meaning: Threshold, passage point
            'GATE': SegmentVector(0.8, 0.3, 0.3, 0.0, 0.3, 0.3, 1.0),
            
            # === ENCLOSURE/CONTAINMENT (Full perimeter) ===
            
            # WALL: Full perimeter A-B-C-D-E-F, no G
            # Meaning: Boundary, separation, protection
            'WALL': SegmentVector(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0),
            
            # ROOM: Full perimeter with G (doorway)
            # Meaning: Contained space with access
            'ROOM': SegmentVector(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
            
            # BOWL: D base with upward opening (no A)
            # Meaning: Receptacle, holding capacity
            'BOWL': SegmentVector(0.0, 0.6, 0.6, 0.8, 0.6, 0.6, 0.0),
            
            # === DIRECTIONAL/ASYMMETRIC PATTERNS ===
            
            # PATH: B-C-D (right descent)
            # Meaning: Way moving outward and down, exit
            'PATH': SegmentVector(0.2, 0.8, 0.9, 0.7, 0.1, 0.2, 0.0),
            
            # ENTRANCE: A-F-E-D (left arch)
            # Meaning: Way moving inward and down, entry
            'ENTRANCE': SegmentVector(0.8, 0.1, 0.0, 0.8, 0.9, 0.8, 0.0),
            
            # EXIT: A-B-C-D (right arch)
            # Meaning: Departure, outward journey
            'EXIT': SegmentVector(0.8, 0.9, 0.8, 0.7, 0.0, 0.1, 0.0),
            
            # ARROW: A with B-C pointing right
            # Meaning: Direction, intention toward external
            'ARROW': SegmentVector(0.9, 1.0, 0.9, 0.1, 0.0, 0.0, 0.0),
            
            # SHIELD: F-E inward protection
            # Meaning: Defense, internal boundary
            'SHIELD': SegmentVector(0.3, 0.0, 0.0, 0.3, 0.9, 0.9, 0.0),
            
            # === RESILIENCE CONCEPT ===
            
            # RESILIENCE: Full activation (all segments)
            # Meaning: Complete adaptability, wholeness under pressure
            # All directions active = can respond from any position
            'RESILIENCE': SegmentVector(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
            
            # FLEX: G strong with A-D connection, soft sides
            # Meaning: Bending without breaking
            'FLEX': SegmentVector(0.6, 0.3, 0.3, 0.6, 0.3, 0.3, 1.0),
            
            # RECOVER: D strong with upward reaching A,G
            # Meaning: Rising from foundation, restoration
            'RECOVER': SegmentVector(0.7, 0.2, 0.2, 0.9, 0.2, 0.3, 0.8),
        }
    
    def euclidean_distance(self, v1: List[float], v2: List[float]) -> float:
        """Calculate distance between two activation patterns"""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))
    
    def decode(self, pattern: List[float], top_k: int = 3) -> Dict:
        """
        Decode a 7-segment activation pattern into semantic meaning
        
        Returns dict with:
        - primary: closest concept
        - pattern: segment activation names
        - vertical: vertical extension score
        - lateral: lateral balance score
        - enclosure: enclosure score
        - description: generated semantic description
        """
        vec = SegmentVector.from_list(pattern)
        
        # Find closest matches in lexicon
        distances = []
        for concept, concept_vec in self.lexicon.items():
            dist = self.euclidean_distance(pattern, concept_vec.to_list())
            distances.append((concept, dist, concept_vec))
        
        distances.sort(key=lambda x: x[1])
        primary = distances[0]
        
        # Analyze pattern
        active_segs = vec.active(0.5)
        vertical = vec.vertical_score()
        lateral = vec.lateral_balance()
        enclosure = vec.enclosure_score()
        
        return {
            'primary': {
                'concept': primary[0],
                'distance': round(primary[1], 3)
            },
            'pattern': {
                'active_segments': active_segs,
                'name': vec.pattern_name(),
                'binary': ''.join(['1' if v > 0.5 else '0' for v in pattern])
            },
            'analysis': {
                'vertical_extension': round(vertical, 2),
                'lateral_balance': round(lateral, 2),
                'enclosure': round(enclosure, 2),
                'direction': self._direction_label(lateral, vertical)
            },
            'description': self._generate_description(vec, primary[0], active_segs)
        }
    
    def _direction_label(self, lateral: float, vertical: float) -> str:
        """Generate directional label from scores"""
        if abs(lateral) < 0.2 and vertical > 0.6:
            return "vertical/central"
        elif lateral > 0.4:
            return "outward/external"
        elif lateral < -0.4:
            return "inward/internal"
        elif vertical < 0.3:
            return "horizontal/peripheral"
        else:
            return "balanced/integrated"
    
    def _generate_description(self, vec: SegmentVector, concept: str, active: List[str]) -> str:
        """Generate semantic description from activation pattern"""
        parts = []
        
        # Check for vertical spine
        if vec.A > 0.5 and vec.D > 0.5:
            if vec.G > 0.5:
                parts.append("connected verticality")
            else:
                parts.append("unbroken vertical extension")
        elif vec.A > 0.5:
            parts.append("crown/apex presence")
        elif vec.D > 0.5:
            parts.append("foundation/grounding")
        
        # Check lateral direction
        outward = vec.B + vec.C
        inward = vec.E + vec.F
        if outward > 1.0 and inward < 0.5:
            parts.append("outward projection")
        elif inward > 1.0 and outward < 0.5:
            parts.append("inward gathering")
        elif outward > 0.5 and inward > 0.5:
            parts.append("bidirectional flow")
        
        # Check enclosure
        if vec.enclosure_score() > 0.8:
            parts.append("full enclosure")
        elif vec.enclosure_score() < 0.3:
            parts.append("open form")
        
        # Check bridge
        if vec.G > 0.7:
            parts.append("central mediation")
        
        if not parts:
            return f"minimal activation pattern (like {concept})"
        
        return f"{' + '.join(parts)} (archetype: {concept})"
    
    def encode(self, segments: List[str], intensities: List[float] = None) -> SegmentVector:
        """Encode segment list into activation vector"""
        vector = [0.0] * 7
        
        if intensities is None:
            intensities = [1.0] * len(segments)
        
        for seg, intensity in zip(segments, intensities):
            if seg in SEGMENT_ORDER:
                idx = SEGMENT_ORDER.index(seg)
                vector[idx] = max(0.0, min(1.0, intensity))
        
        return SegmentVector.from_list(vector)


# Pre-instantiated decoder
decoder = SegmentDecoder()


def decode_segments(pattern: List[float]) -> Dict:
    """Convenience function to decode segment pattern"""
    return decoder.decode(pattern)


def encode_pattern(segments: str) -> SegmentVector:
    """
    Encode segment string like 'A-D-G' or 'ADG' into vector
    """
    if '-' in segments:
        parts = segments.split('-')
    else:
        parts = list(segments)
    return decoder.encode(parts)


# Visual display functions
def visualize_pattern(pattern: List[float]) -> str:
    """Generate ASCII art of 7-segment pattern"""
    A = '───' if pattern[0] > 0.5 else '   '
    B = '│' if pattern[1] > 0.5 else ' '
    C = '│' if pattern[2] > 0.5 else ' '
    D = '───' if pattern[3] > 0.5 else '   '
    E = '│' if pattern[4] > 0.5 else ' '
    F = '│' if pattern[5] > 0.5 else ' '
    G = '───' if pattern[6] > 0.5 else '   '
    
    return f"""
    {A}      A={'█' if pattern[0] > 0.5 else '░'}
   {F} {B}     F={'█' if pattern[5] > 0.5 else '░'} B={'█' if pattern[1] > 0.5 else '░'}
    {G}      G={'█' if pattern[6] > 0.5 else '░'}
   {E} {C}     E={'█' if pattern[4] > 0.5 else '░'} C={'█' if pattern[2] > 0.5 else '░'}
    {D}      D={'█' if pattern[3] > 0.5 else '░'}
    """


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("UNIVERSAL GLYPHABETIC DICTIONARY - 7-SEGMENT DISPLAY")
    print("=" * 60)
    
    test_patterns = [
        # TOWER pattern: A, D, G active (vertical spine)
        [1.0, 0.2, 0.2, 1.0, 0.2, 0.2, 1.0],
        # WALL pattern: Full perimeter, no G
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
        # RESILIENCE pattern: All segments
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        # ARROW pattern: A, B, C (pointing right)
        [0.9, 1.0, 0.9, 0.1, 0.0, 0.0, 0.0],
        # BOWL pattern: D base, sides up
        [0.0, 0.6, 0.6, 0.8, 0.6, 0.6, 0.0],
    ]
    
    for pattern in test_patterns:
        result = decode_segments(pattern)
        print(f"\n{'─' * 50}")
        print(visualize_pattern(pattern))
        print(f"Pattern: {result['pattern']['name']}")
        print(f"Binary:  {result['pattern']['binary']}")
        print(f"Primary: {result['primary']['concept']}")
        print(f"Analysis: {result['analysis']['direction']}")
        print(f"Description: {result['description']}")

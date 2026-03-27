"""
Universal Glyphabetic Dictionary - Core Module

Maps 7D geometric vectors to semantic meanings through
7 primitive dimensions: C, L, A, V, S, N, F
"""

from typing import List, Tuple, Dict, NamedTuple
import math

# The 7 Geometric Primitives
PRIMITIVES = {
    'C': {'name': 'Curve', 'meaning': 'Flow', 'essence': 'movement, fluidity, continuous change'},
    'L': {'name': 'Line', 'meaning': 'Structure', 'essence': 'stability, connection, order'},
    'A': {'name': 'Angle', 'meaning': 'Discontinuity', 'essence': 'sharpness, decision, direction change'},
    'V': {'name': 'Vesica', 'meaning': 'Intersection', 'essence': 'overlap, union, shared space'},
    'S': {'name': 'Spiral', 'meaning': 'Growth', 'essence': 'evolution, expansion, recursion'},
    'N': {'name': 'Node', 'meaning': 'Terminus', 'essence': 'endpoints, convergence, origin'},
    'F': {'name': 'Field', 'meaning': 'Containment', 'essence': 'boundaries, enclosure, limits'}
}

GLYPH_ORDER = ['C', 'L', 'A', 'V', 'S', 'N', 'F']


class SemanticVector(NamedTuple):
    """7D semantic vector representation"""
    C: float  # Curve / Flow
    L: float  # Line / Structure
    A: float  # Angle / Discontinuity
    V: float  # Vesica / Intersection
    S: float  # Spiral / Growth
    N: float  # Node / Terminus
    F: float  # Field / Containment
    
    def to_list(self) -> List[float]:
        return [self.C, self.L, self.A, self.V, self.S, self.N, self.F]
    
    @classmethod
    def from_list(cls, vec: List[float]) -> 'SemanticVector':
        return cls(*vec)
    
    def dominant(self, threshold: float = 0.5) -> List[str]:
        """Return primitives above threshold"""
        glyphs = []
        for i, glyph in enumerate(GLYPH_ORDER):
            if self.to_list()[i] >= threshold:
                glyphs.append(glyph)
        return glyphs
    
    def signature(self) -> str:
        """Generate human-readable signature like 'C+S-F'"""
        parts = []
        for i, glyph in enumerate(GLYPH_ORDER):
            val = self.to_list()[i]
            if val >= 0.7:
                parts.append(f"+{glyph}")
            elif val >= 0.4:
                parts.append(glyph)
            elif val <= 0.2:
                parts.append(f"-{glyph}")
        return ''.join(parts) if parts else "neutral"


class GlyphabeticDecoder:
    """Decodes 7D vectors into semantic meanings"""
    
    def __init__(self):
        self.lexicon = self._build_lexicon()
    
    def _build_lexicon(self) -> Dict[str, SemanticVector]:
        """Build core semantic lexicon - 20 universal concepts"""
        return {
            # Movement & Flow concepts
            'RIVER': SemanticVector(0.9, 0.4, 0.1, 0.3, 0.2, 0.2, 0.3),
            'PATH': SemanticVector(0.6, 0.8, 0.3, 0.2, 0.2, 0.5, 0.2),
            'DANCE': SemanticVector(0.9, 0.3, 0.4, 0.3, 0.6, 0.2, 0.1),
            
            # Structure concepts
            'HOUSE': SemanticVector(0.2, 0.8, 0.7, 0.4, 0.1, 0.4, 0.9),
            'BRIDGE': SemanticVector(0.3, 0.9, 0.2, 0.5, 0.1, 0.6, 0.2),
            'TOWER': SemanticVector(0.1, 0.9, 0.3, 0.2, 0.7, 0.8, 0.5),
            
            # Discontinuity concepts
            'EDGE': SemanticVector(0.3, 0.6, 0.9, 0.4, 0.2, 0.5, 0.3),
            'BREAK': SemanticVector(0.4, 0.3, 0.9, 0.3, 0.2, 0.6, 0.2),
            'THORN': SemanticVector(0.2, 0.5, 0.9, 0.3, 0.4, 0.7, 0.1),
            
            # Intersection concepts
            'CROSS': SemanticVector(0.2, 0.7, 0.6, 0.9, 0.2, 0.5, 0.2),
            'MEET': SemanticVector(0.4, 0.4, 0.3, 0.9, 0.2, 0.6, 0.2),
            'KNOT': SemanticVector(0.5, 0.5, 0.4, 0.8, 0.3, 0.9, 0.3),
            
            # Growth concepts
            'TREE': SemanticVector(0.4, 0.6, 0.3, 0.2, 0.9, 0.5, 0.4),
            'SEED': SemanticVector(0.2, 0.3, 0.2, 0.3, 0.9, 0.6, 0.6),
            'WAVE': SemanticVector(0.9, 0.3, 0.2, 0.2, 0.7, 0.3, 0.1),
            
            # Terminus concepts
            'DOOR': SemanticVector(0.2, 0.7, 0.5, 0.5, 0.1, 0.9, 0.6),
            'GOAL': SemanticVector(0.3, 0.5, 0.3, 0.4, 0.4, 0.9, 0.3),
            'HEART': SemanticVector(0.6, 0.3, 0.2, 0.6, 0.3, 0.8, 0.4),
            
            # Containment concepts
            'BOWL': SemanticVector(0.5, 0.4, 0.2, 0.3, 0.2, 0.3, 0.9),
            'WOMB': SemanticVector(0.6, 0.2, 0.1, 0.4, 0.7, 0.4, 0.9),
            'WALL': SemanticVector(0.1, 0.8, 0.4, 0.2, 0.1, 0.4, 0.9),
        }
    
    def euclidean_distance(self, v1: List[float], v2: List[float]) -> float:
        """Calculate distance between two vectors"""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))
    
    def decode(self, vector: List[float], top_k: int = 3) -> Dict:
        """
        Decode a 7D vector into semantic meaning
        
        Returns dict with:
        - primary: closest concept
        - secondary: next closest concepts
        - signature: glyph signature
        - dominant: dominant primitives
        - description: generated description
        """
        vec = SemanticVector.from_list(vector)
        
        # Find closest matches in lexicon
        distances = []
        for concept, concept_vec in self.lexicon.items():
            dist = self.euclidean_distance(vector, concept_vec.to_list())
            distances.append((concept, dist, concept_vec))
        
        distances.sort(key=lambda x: x[1])
        
        # Build result
        primary = distances[0]
        secondaries = distances[1:top_k] if len(distances) > 1 else []
        
        return {
            'primary': {
                'concept': primary[0],
                'vector': primary[2].to_list(),
                'distance': round(primary[1], 3)
            },
            'secondary': [
                {'concept': d[0], 'distance': round(d[1], 3)}
                for d in secondaries
            ],
            'signature': vec.signature(),
            'dominant': vec.dominant(),
            'description': self._generate_description(vec, primary[0])
        }
    
    def _generate_description(self, vec: SemanticVector, primary: str) -> str:
        """Generate a poetic description of the semantic signature"""
        dominant = vec.dominant(0.4)
        
        if not dominant:
            return f"balanced neutral form (like {primary})"
        
        # Build description from primitives
        descriptions = []
        for glyph in dominant:
            meaning = PRIMITIVES[glyph]['meaning'].lower()
            descriptions.append(meaning)
        
        if len(descriptions) == 1:
            return f"pure {descriptions[0]} (like {primary})"
        elif len(descriptions) == 2:
            return f"{descriptions[0]} through {descriptions[1]} (like {primary})"
        else:
            return f"{' + '.join(descriptions[:2])} with {', '.join(descriptions[2:])} (like {primary})"
    
    def encode(self, glyphs: List[str], intensities: List[float] = None) -> SemanticVector:
        """
        Encode glyphs into a semantic vector
        
        Example: encode(['C', 'S'], [0.8, 0.6]) → flowing growth
        """
        vector = [0.0] * 7
        
        if intensities is None:
            intensities = [0.7] * len(glyphs)
        
        for glyph, intensity in zip(glyphs, intensities):
            if glyph in GLYPH_ORDER:
                idx = GLYPH_ORDER.index(glyph)
                vector[idx] = max(0.0, min(1.0, intensity))
        
        return SemanticVector.from_list(vector)


# Pre-instantiated decoder for convenience
decoder = GlyphabeticDecoder()


def decode_vector(vector: List[float]) -> Dict:
    """Convenience function to decode a vector"""
    return decoder.decode(vector)


def encode_word(glyphs: str) -> SemanticVector:
    """
    Encode a glyph string like 'C+S' or 'CLAN' into vector
    
    - '+' separates explicit components
    - Otherwise each char is a glyph
    """
    if '+' in glyphs:
        parts = glyphs.split('+')
        return decoder.encode(parts)
    else:
        return decoder.encode(list(glyphs))


# Example usage
if __name__ == "__main__":
    # Test decoding
    test_vectors = [
        [0.9, 0.3, 0.1, 0.2, 0.6, 0.2, 0.1],  # Flow + Growth
        [0.2, 0.8, 0.6, 0.4, 0.1, 0.4, 0.8],  # Structure + Containment
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],  # Balanced
    ]
    
    print("Universal Glyphabetic Dictionary - Test Decoding\n")
    print("=" * 60)
    
    for vec in test_vectors:
        result = decode_vector(vec)
        print(f"\nVector: {vec}")
        print(f"Signature: {result['signature']}")
        print(f"Dominant: {result['dominant']}")
        print(f"Primary: {result['primary']['concept']} (dist: {result['primary']['distance']})")
        print(f"Description: {result['description']}")

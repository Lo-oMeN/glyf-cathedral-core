"""
Trinity v6.0: Layer III — AEXIE Language
Parser for geometric language with Node0 resonance.
"""
import numpy as np
from typing import List
from governance.spam_vector import SPAMVector

class AexieParser:
    """
    AEXIE Parser: Converts geometric state to glyph stream.
    
    7 Registers correspond to 7 geometric primitives.
    Golden angle rotation creates fractal depth.
    Node0 resonance marks aligned glyphs.
    """
    
    def __init__(self):
        self.registers = [None] * 7
        
        # Glyph map: 7 primitives
        self.glyph_map = {
            0: 'Line(→)',
            1: 'Absence(∅)', 
            2: 'Radiance(☀)',
            3: 'Enclosure(□)',
            4: 'Curve(∿)',
            5: 'Intersection(×)',
            6: 'Point(●)'
        }
        
        # Golden angle for register rotation
        self.golden_angle = 2.399963229728653  # radians
    
    def rotate_registers(self, depth: int):
        """Rotate registers by golden angle × depth."""
        shift = int(depth * self.golden_angle) % 7
        self.registers = self.registers[shift:] + self.registers[:shift]
    
    def parse(
        self, 
        corrected_state: np.ndarray, 
        phi: float, 
        spam: np.ndarray
    ) -> List[str]:
        """
        Parse geometric state into glyph stream.
        
        Returns: List of glyph symbols with depth markers.
        """
        kappa = spam[2]  # Alignment
        proj = corrected_state[:7]
        
        # Radial weights: higher weight for aligned components
        radial_weights = np.exp(-np.abs(proj) * (1 - kappa))
        
        glyph_stream = []
        depth = 0
        
        # Build stream up to depth 5 or until weights decay
        while depth < 5 and np.max(radial_weights) > 0.1:
            self.rotate_registers(depth)
            
            for i in range(7):
                # Map projection to glyph index
                segment_idx = int(np.round((proj[i] * radial_weights[i]) % 7)) % 7
                symbol = self.glyph_map[segment_idx]
                
                # If misaligned, use complementary glyph
                if kappa < 0.5:
                    symbol = f"~{self.glyph_map[(segment_idx + 3) % 7]}"
                
                # Mark Node0 resonance with probability Φ
                if np.random.rand() < 0.618:
                    symbol += "↔Node0"
                
                glyph_stream.append(symbol)
            
            # Decay weights for next depth level
            radial_weights *= 0.618
            depth += 1
        
        return glyph_stream
    
    def format_stream(self, glyph_stream: List[str]) -> str:
        """Format glyph stream as readable text."""
        return " ".join(glyph_stream)

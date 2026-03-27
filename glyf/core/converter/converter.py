"""
English-to-Glyphoform Converter

Converts English words into glyphoform notation using canonical 7-segment display grids.

Composition Modes:
- OVERLAPPING: Letters occupy same position, segments combine (OR operation)
- TOUCHING: Letters adjacent, no overlap
- SPACED: Letters separated by gaps
"""

from .glyphmap import (
    GLYPH_MAP, SEGMENT_BITS, BIT_TO_SEGMENT,
    get_binary_pattern, get_segment_list, get_segment_bitmap,
    binary_to_segments, segments_to_binary, get_visual_display,
    get_glyph_info, CompositionMode
)


class GlyphoformConverter:
    """Converts English text to glyphoform notation with composition modes."""
    
    def __init__(self, style='bitmap', composition_mode=CompositionMode.SPACED):
        """
        Initialize converter.
        
        Args:
            style: 'bitmap', 'binary', 'hex', 'visual', 'symbol'
            composition_mode: 'overlapping', 'touching', 'spaced'
        """
        self.style = style
        self.composition_mode = composition_mode
    
    def convert_letter(self, letter):
        """Convert a single letter to its glyphoform representation."""
        letter = letter.upper()
        
        if not letter.isalpha():
            return letter
        
        info = GLYPH_MAP.get(letter)
        if not info:
            return '?'
        
        if self.style == 'bitmap':
            return self._format_bitmap(info['segments'])
        elif self.style == 'binary':
            return f"[{info['binary']:07b}]"
        elif self.style == 'hex':
            return f"[0x{info['hex']:02X}]"
        elif self.style == 'symbol':
            return info['symbol']
        elif self.style == 'visual':
            return get_visual_display(letter)
        elif self.style == 'segments':
            return f"[{','.join(info['segments'])}]"
        else:
            return self._format_bitmap(info['segments'])
    
    def _format_bitmap(self, segments):
        """Format segment list as [A,B,C,D,E,F,G] style."""
        # Create full bitmap showing all segments with active ones
        bitmap = []
        for seg in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
            if seg in segments:
                bitmap.append(seg)
            else:
                bitmap.append('.')
        return f"[{','.join(bitmap)}]"
    
    def convert(self, text):
        """
        Convert a word or phrase to glyphoform notation.
        
        Args:
            text: English word(s) to convert
            
        Returns:
            Glyphoform string representation
        """
        if self.composition_mode == CompositionMode.OVERLAPPING:
            return self._convert_overlapping(text)
        elif self.composition_mode == CompositionMode.TOUCHING:
            return self._convert_touching(text)
        else:  # SPACED
            return self._convert_spaced(text)
    
    def _convert_spaced(self, text):
        """Convert with spaced letters (default)."""
        if self.style == 'visual':
            return self._convert_visual_stacked(text)
        
        results = []
        for char in text.upper():
            if char.isalpha():
                results.append(self.convert_letter(char))
            else:
                results.append(char)
        
        if self.style == 'symbol':
            return ''.join(results)
        elif self.style in ['binary', 'hex', 'segments']:
            return ' '.join(results)
        else:
            return '  '.join(results)
    
    def _convert_touching(self, text):
        """Convert with touching/adjacent letters."""
        # Similar to spaced but with no gaps between brackets
        if self.style == 'visual':
            return self._convert_visual_stacked(text)
        
        results = []
        for char in text.upper():
            if char.isalpha():
                results.append(self.convert_letter(char))
            else:
                results.append(char)
        
        if self.style == 'symbol':
            return ''.join(results)
        elif self.style in ['binary', 'hex', 'segments']:
            return ''.join(results)
        else:
            return ''.join(results)
    
    def _convert_overlapping(self, text):
        """
        Convert with overlapping letters - segments combine via OR operation.
        
        All letters occupy the same position, creating a unified glyph.
        """
        letters = [c for c in text.upper() if c.isalpha()]
        if not letters:
            return "[]"
        
        # Combine all segment patterns with OR
        combined_binary = 0
        for letter in letters:
            binary = get_binary_pattern(letter)
            if binary is not None:
                combined_binary |= binary
        
        # Format based on style
        if self.style == 'binary':
            return f"[{combined_binary:07b}]"
        elif self.style == 'hex':
            return f"[0x{combined_binary:02X}]"
        elif self.style == 'segments':
            segs = binary_to_segments(combined_binary)
            return f"[{','.join(segs)}]"
        else:  # bitmap
            segs = binary_to_segments(combined_binary)
            return self._format_bitmap(segs)
    
    def _convert_visual_stacked(self, text):
        """Stack visual representations side by side."""
        lines = [''] * 7
        
        for char in text.upper():
            if char.isalpha():
                art = get_visual_display(char).split('\n')
                for i, line in enumerate(art):
                    if i < 7:
                        lines[i] += '  ' + line
            else:
                # Space for non-letters
                for i in range(7):
                    lines[i] += '    ' + char + '    '
        
        return '\n'.join(lines)
    
    def convert_word_layers(self, text):
        """
        Show each letter as a layer in overlapping composition.
        
        Returns list of individual letter bitmaps plus combined.
        """
        letters = [c for c in text.upper() if c.isalpha()]
        
        layers = []
        for letter in letters:
            info = GLYPH_MAP.get(letter)
            if info:
                layers.append({
                    'letter': letter,
                    'bitmap': self._format_bitmap(info['segments']),
                    'binary': f"{info['binary']:07b}",
                    'hex': f"0x{info['hex']:02X}",
                    'segments': info['segments']
                })
        
        # Calculate combined
        combined_binary = 0
        for layer in layers:
            combined_binary |= int(layer['binary'], 2)
        
        combined = {
            'letter': 'COMBINED',
            'bitmap': self._format_bitmap(binary_to_segments(combined_binary)),
            'binary': f"{combined_binary:07b}",
            'hex': f"0x{combined_binary:02X}",
            'segments': binary_to_segments(combined_binary)
        }
        
        return {'layers': layers, 'combined': combined}
    
    def decompose(self, text):
        """
        Get full decomposition info for a word.
        
        Returns list of dicts with letter details.
        """
        decomposition = []
        for char in text.upper():
            if char.isalpha():
                info = GLYPH_MAP.get(char)
                if info:
                    decomposition.append({
                        'letter': char,
                        'symbol': info['symbol'],
                        'binary': info['binary'],
                        'hex': info['hex'],
                        'segments': info['segments'],
                        'description': info['description']
                    })
            else:
                decomposition.append({
                    'letter': char,
                    'symbol': char,
                    'binary': None,
                    'hex': None,
                    'segments': [],
                    'description': 'non-letter'
                })
        return decomposition
    
    def analyze(self, text):
        """
        Analyze word structure and provide detailed glyphoform breakdown.
        
        Returns formatted analysis string.
        """
        decomp = self.decompose(text)
        lines = [f"=== Glyphoform Analysis: '{text}' ===", ""]
        
        for item in decomp:
            lines.append(f"Letter: {item['letter']}")
            lines.append(f"  Symbol: {item['symbol']}")
            if item['binary'] is not None:
                lines.append(f"  Binary: [{item['binary']:07b}]")
                lines.append(f"  Hex: 0x{item['hex']:02X}")
                lines.append(f"  Segments: [{','.join(item['segments'])}]")
            lines.append(f"  Description: {item['description']}")
            lines.append("")
        
        # Composition analysis
        if len(decomp) > 1:
            lines.append("--- Composition Analysis ---")
            
            # Spaced
            self.composition_mode = CompositionMode.SPACED
            lines.append(f"SPACED:   {self.convert(text)}")
            
            # Touching
            self.composition_mode = CompositionMode.TOUCHING
            lines.append(f"TOUCHING: {self.convert(text)}")
            
            # Overlapping
            self.composition_mode = CompositionMode.OVERLAPPING
            lines.append(f"OVERLAP:  {self.convert(text)}")
            
            # Show layers
            layers_data = self.convert_word_layers(text)
            lines.append("")
            lines.append("Layers (for overlapping mode):")
            for layer in layers_data['layers']:
                lines.append(f"  {layer['letter']}: {layer['bitmap']} = {layer['binary']}")
            lines.append(f"  OR ----: {layers_data['combined']['bitmap']} = {layers_data['combined']['binary']}")
        
        return '\n'.join(lines)


# Convenience functions
def to_glyphoform(text, style='bitmap', mode='spaced'):
    """Quick convert function."""
    converter = GlyphoformConverter(style=style, composition_mode=mode)
    return converter.convert(text)

def to_bitmap(text, mode='spaced'):
    """Convert to segment bitmap notation."""
    return to_glyphoform(text, style='bitmap', mode=mode)

def to_binary(text, mode='spaced'):
    """Convert to binary notation."""
    return to_glyphoform(text, style='binary', mode=mode)

def to_segments(text, mode='spaced'):
    """Convert to segment list notation."""
    return to_glyphoform(text, style='segments', mode=mode)

def analyze_word(text):
    """Get detailed analysis of a word."""
    converter = GlyphoformConverter()
    return converter.analyze(text)

def decompose_word(text):
    """Get decomposition data structure."""
    converter = GlyphoformConverter()
    return converter.decompose(text)

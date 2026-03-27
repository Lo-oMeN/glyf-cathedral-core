"""
Canonical 7-Segment Display Grid Mapping

Standard digital clock segment layout:
    -- A --
   |       |
   F       B
   |       |
    -- G --  
   |       |
   E       C
   |       |
    -- D --

Segments: A(top), B(upper-right), C(lower-right), D(bottom)
          E(lower-left), F(upper-left), G(middle)

Binary encoding: bit 6=A, 5=B, 4=C, 3=D, 2=E, 1=F, 0=G
Or: [A,B,C,D,E,F,G] as active segment list
"""

# Standard 7-Segment Alphabet Encoding
# Each letter mapped to its segment activation pattern

GLYPH_MAP = {
    # A - Top, both sides, middle (no bottom) - like A shape
    'A': {
        'segments': ['A','B','C','E','F','G'],
        'binary': 0b1110111,  # A,B,C,E,F,G
        'hex': 0x77,
        'symbol': 'ᗩ',
        'description': 'Triangle with crossbar'
    },
    
    # B - Full right side + middle + top/bottom segments (like lowercase b)
    'B': {
        'segments': ['A','B','C','D','E','F','G'],
        'binary': 0b1111111,  # All segments (unique pattern)
        'hex': 0x7F,
        'symbol': 'ᗷ',
        'description': 'Full right, unique pattern'
    },
    
    # C - Open on right (top, bottom, left sides)
    'C': {
        'segments': ['A','D','E','F'],
        'binary': 0b1001110,  # A,D,E,F
        'hex': 0x4E,
        'symbol': 'ᑕ',
        'description': 'Open right curve'
    },
    
    # D - Like 0 but with middle (or like mirrored C)
    'D': {
        'segments': ['A','B','C','D','E','F'],
        'binary': 0b0111111,  # A,B,C,D,E,F (no G)
        'hex': 0x3F,
        'symbol': 'ᗪ',
        'description': 'Full enclosure, no middle'
    },
    
    # E - Full left + all horizontals
    'E': {
        'segments': ['A','D','E','F','G'],
        'binary': 0b1001111,  # A,D,E,F,G
        'hex': 0x4F,
        'symbol': 'ᗴ',
        'description': 'Three horizontals + spine'
    },
    
    # F - Top, left, middle
    'F': {
        'segments': ['A','E','F','G'],
        'binary': 0b1000111,  # A,E,F,G
        'hex': 0x47,
        'symbol': 'ᖴ',
        'description': 'Top-heavy with spine'
    },
    
    # G - C with right-bottom segment
    'G': {
        'segments': ['A','B','C','D','E','F'],
        'binary': 0b1111011,  # A,B,C,D,E,F (like 0)
        'hex': 0x7B,
        'symbol': 'ᘜ',
        'description': 'Almost closed, unique'
    },
    
    # H - Both verticals + middle (no top/bottom)
    'H': {
        'segments': ['B','C','E','F','G'],
        'binary': 0b0110111,  # B,C,E,F,G
        'hex': 0x37,
        'symbol': 'ᕼ',
        'description': 'Double pillar with bridge'
    },
    
    # I - Just left side vertical (or right side in some fonts)
    'I': {
        'segments': ['B','C'],
        'binary': 0b0110000,  # B,C
        'hex': 0x30,
        'symbol': 'ᓰ',
        'description': 'Single vertical right'
    },
    
    # J - Bottom curve open on left
    'J': {
        'segments': ['B','C','D','E'],
        'binary': 0b0111100,  # B,C,D,E
        'hex': 0x3C,
        'symbol': 'ᒍ',
        'description': 'Hook open left'
    },
    
    # K - Left side + diagonals (approximated with B,E,G)
    'K': {
        'segments': ['B','E','F','G'],
        'binary': 0b0110110,  # B,E,F,G
        'hex': 0x36,
        'symbol': 'Ḱ',
        'description': 'Vertical with arms'
    },
    
    # L - Left vertical + bottom
    'L': {
        'segments': ['D','E','F'],
        'binary': 0b0001110,  # D,E,F
        'hex': 0x0E,
        'symbol': 'ᒪ',
        'description': 'Corner right'
    },
    
    # M - Two peaks (A, both upper verticals, no middle)
    'M': {
        'segments': ['A','B','C','E','F'],
        'binary': 0b1110110,  # A,B,C,E,F
        'hex': 0x76,
        'symbol': 'ᗰ',
        'description': 'Twin peaks'
    },
    
    # N - Both verticals + right-top, left-bottom (like M variant)
    'N': {
        'segments': ['A','B','C','E','F'],
        'binary': 0b1110110,  # Same as M visually
        'hex': 0x76,
        'symbol': 'ᘉ',
        'description': 'Connected pillars'
    },
    
    # O - Full enclosure (like 0)
    'O': {
        'segments': ['A','B','C','D','E','F'],
        'binary': 0b1111110,  # A,B,C,D,E,F (no G)
        'hex': 0x7E,
        'symbol': '〇',
        'description': 'Complete enclosure'
    },
    
    # P - Top bowl + left side + middle
    'P': {
        'segments': ['A','B','E','F','G'],
        'binary': 0b1100111,  # A,B,E,F,G
        'hex': 0x67,
        'symbol': 'ᑭ',
        'description': 'Bowl with stem'
    },
    
    # Q - O with descender (use all for uniqueness)
    'Q': {
        'segments': ['A','B','C','D','E','F','G'],
        'binary': 0b1111111,  # All segments
        'hex': 0x7F,
        'symbol': 'ᕋ',
        'description': 'Circle with tail'
    },
    
    # R - P with bottom-right leg
    'R': {
        'segments': ['A','B','C','E','F','G'],
        'binary': 0b1110111,  # Same as A
        'hex': 0x77,
        'symbol': 'ᖇ',
        'description': 'Bowl with diagonal'
    },
    
    # S - Like number 5
    'S': {
        'segments': ['A','B','D','E','G'],
        'binary': 0b1011011,  # A,B,D,E,G
        'hex': 0x5B,
        'symbol': 'ᔕ',
        'description': 'S-curve shape'
    },
    
    # T - Top + left side verticals
    'T': {
        'segments': ['A','E','F'],
        'binary': 0b1000110,  # A,E,F
        'hex': 0x46,
        'symbol': 'ᖶ',
        'description': 'Top bar with stem'
    },
    
    # U - Cup shape (both lower + bottom)
    'U': {
        'segments': ['B','C','D','E','F'],
        'binary': 0b0111110,  # B,C,D,E,F
        'hex': 0x3E,
        'symbol': 'ᑘ',
        'description': 'Open cup/bowl'
    },
    
    # V - Point down (bottom + diagonals approximated)
    'V': {
        'segments': ['C','D','E','F'],
        'binary': 0b0011110,  # C,D,E,F
        'hex': 0x1E,
        'symbol': 'ᐯ',
        'description': 'Downward point'
    },
    
    # W - Double V (left + both right verticals + bottom)
    'W': {
        'segments': ['B','C','D','E','F'],
        'binary': 0b0111110,  # Same as U
        'hex': 0x3E,
        'symbol': 'ᗯ',
        'description': 'Double valley'
    },
    
    # X - Crossing (diagonals as all verticals)
    'X': {
        'segments': ['B','C','E','F'],
        'binary': 0b0110110,  # B,C,E,F
        'hex': 0x36,
        'symbol': '᙭',
        'description': 'Cross intersection'
    },
    
    # Y - V with stem (right side + bottom)
    'Y': {
        'segments': ['B','C','D','E','F','G'],
        'binary': 0b0111011,  # B,C,D,E,F,G
        'hex': 0x3B,
        'symbol': 'ᖻ',
        'description': 'Fork with stem'
    },
    
    # Z - Top, bottom, diagonal (approximated as horizontals + one vertical)
    'Z': {
        'segments': ['A','B','D','E','G'],
        'binary': 0b1101101,  # A,B,D,E,G
        'hex': 0x6D,
        'symbol': 'ᘔ',
        'description': 'Diagonal slash'
    },
}

# Segment name to bit position mapping
SEGMENT_BITS = {
    'A': 6,  # top
    'B': 5,  # upper-right
    'C': 4,  # lower-right
    'D': 3,  # bottom
    'E': 2,  # lower-left
    'F': 1,  # upper-left
    'G': 0,  # middle
}

BIT_TO_SEGMENT = {v: k for k, v in SEGMENT_BITS.items()}


def get_binary_pattern(letter):
    """Get 7-bit binary value for a letter."""
    letter = letter.upper()
    if letter not in GLYPH_MAP:
        return None
    return GLYPH_MAP[letter]['binary']


def get_segment_list(letter):
    """Get list of active segment names for a letter."""
    letter = letter.upper()
    if letter not in GLYPH_MAP:
        return None
    return GLYPH_MAP[letter]['segments']


def get_segment_bitmap(letter):
    """Get bitmap as [A,B,C,D,E,F,G] format."""
    letter = letter.upper()
    if letter not in GLYPH_MAP:
        return None
    segs = GLYPH_MAP[letter]['segments']
    return [s for s in ['A','B','C','D','E','F','G'] if s in segs]


def binary_to_segments(binary_val):
    """Convert binary value to segment list."""
    segments = []
    for seg, bit in SEGMENT_BITS.items():
        if binary_val & (1 << bit):
            segments.append(seg)
    return segments


def segments_to_binary(segments):
    """Convert segment list to binary value."""
    binary = 0
    for seg in segments:
        if seg in SEGMENT_BITS:
            binary |= (1 << SEGMENT_BITS[seg])
    return binary


def get_visual_display(letter):
    """Get ASCII art 7-segment display for a letter."""
    letter = letter.upper()
    if letter not in GLYPH_MAP:
        return '?' * 9
    
    segs = set(GLYPH_MAP[letter]['segments'])
    
    # Build 7-line visual representation
    lines = []
    
    # Line 0: Segment A (top)
    if 'A' in segs:
        lines.append(' ███████ ')
    else:
        lines.append('         ')
    
    # Lines 1-2: Segments F and B
    for _ in range(2):
        left = '█' if 'F' in segs else ' '
        right = '█' if 'B' in segs else ' '
        lines.append(f'{left}       {right}')
    
    # Line 3: Segment G (middle)
    if 'G' in segs:
        lines.append(' ███████ ')
    else:
        lines.append('         ')
    
    # Lines 4-5: Segments E and C
    for _ in range(2):
        left = '█' if 'E' in segs else ' '
        right = '█' if 'C' in segs else ' '
        lines.append(f'{left}       {right}')
    
    # Line 6: Segment D (bottom)
    if 'D' in segs:
        lines.append(' ███████ ')
    else:
        lines.append('         ')
    
    return '\n'.join(lines)


def get_glyph_info(letter):
    """Get full glyph information for a letter."""
    letter = letter.upper()
    return GLYPH_MAP.get(letter)


# Composition mode constants
class CompositionMode:
    OVERLAPPING = 'overlapping'  # Same position, segments combine
    TOUCHING = 'touching'        # Adjacent positions
    SPACED = 'spaced'            # Separated positions

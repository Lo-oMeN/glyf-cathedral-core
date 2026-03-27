"""
Glyf English-to-Glyphoform Converter

A system for converting English words to glyphoform notation using
canonical 7-segment digital display decomposition.

Segment Layout:
    -- A --
   |       |
   F       B
   |       |
    -- G --  
   |       |
   E       C
   |       |
    -- D --

Composition Modes:
- SPACED:    [A,B,C,.,E,F,G]  [A,.,C,D,E,.,G]  (separated)
- TOUCHING:  [A,B,C,.,E,F,G][A,.,C,D,E,.,G]    (adjacent)
- OVERLAPPING: [A,B,C,D,E,F,G]                  (combined via OR)

Usage:
    from glyf.core.converter import to_bitmap, to_binary, to_segments
    
    # Bitmap notation (dots for inactive segments)
    print(to_bitmap("HI", mode="spaced"))
    # Output: [.,B,C,.,.,.,.]  [.,B,.,.,.,.,.]
    
    # Binary notation
    print(to_binary("GO", mode="overlapping"))
    # Output: [1111010] (segments OR'd together)
    
    # Segment list notation
    print(to_segments("CAT"))
    # Output: [A,.,.,D,E,F,.] [A,B,C,.,E,F,G] [A,.,.,.,.,F,.]
    
    # Access pre-converted dictionary
    from glyf.core.converter.dictionary import lookup_word, display_dictionary
    print(lookup_word("HELLO"))
    print(display_dictionary(mode="overlapping"))
"""

from .converter import (
    GlyphoformConverter,
    to_glyphoform,
    to_bitmap,
    to_binary,
    to_segments,
    analyze_word,
    decompose_word,
    CompositionMode
)
from .dictionary import (
    GLYPHOFORM_DICTIONARY,
    lookup_word,
    get_words_by_category,
    get_all_categories,
    display_dictionary,
    display_word_detail,
    convert_or_lookup
)
from .glyphmap import (
    GLYPH_MAP,
    SEGMENT_BITS,
    BIT_TO_SEGMENT,
    get_binary_pattern,
    get_segment_list,
    get_segment_bitmap,
    binary_to_segments,
    segments_to_binary,
    get_visual_display,
    get_glyph_info
)

__version__ = "2.0.0"
__all__ = [
    # Main converter
    'GlyphoformConverter',
    'to_glyphoform',
    'to_bitmap',
    'to_binary',
    'to_segments',
    'analyze_word',
    'decompose_word',
    'CompositionMode',
    # Dictionary
    'GLYPHOFORM_DICTIONARY',
    'lookup_word',
    'get_words_by_category',
    'get_all_categories',
    'display_dictionary',
    'display_word_detail',
    'convert_or_lookup',
    # Glyph mappings
    'GLYPH_MAP',
    'SEGMENT_BITS',
    'BIT_TO_SEGMENT',
    'get_binary_pattern',
    'get_segment_list',
    'get_segment_bitmap',
    'binary_to_segments',
    'segments_to_binary',
    'get_visual_display',
    'get_glyph_info',
]

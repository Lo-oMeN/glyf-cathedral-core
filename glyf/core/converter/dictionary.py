"""
Glyphoform Dictionary - 50 Common Words with Segment Bitmaps

Pre-converted words using canonical 7-segment display encoding.
Each entry includes segment bitmaps for all three composition modes.

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
"""

from .glyphmap import get_binary_pattern, segments_to_binary, binary_to_segments
from .converter import CompositionMode

# Helper to generate bitmap notation
def _bitmap(segments):
    """Create [A,B,C,D,E,F,G] bitmap with dots for inactive."""
    return '[' + ','.join(s if s in segments else '.' for s in 'ABCDEFG') + ']'

# Helper to generate all composition modes for a word
def _make_entry(word, category, rank):
    """Create dictionary entry with all composition modes."""
    letters = list(word.upper())
    
    # Individual letter data
    letter_data = []
    for letter in letters:
        binary = get_binary_pattern(letter)
        segs = binary_to_segments(binary) if binary else []
        letter_data.append({
            'letter': letter,
            'binary': binary,
            'hex': f"0x{binary:02X}" if binary else None,
            'bitmap': _bitmap(segs),
            'segments': segs
        })
    
    # SPACED mode: individual letters separated
    spaced = '  '.join(d['bitmap'] for d in letter_data)
    
    # TOUCHING mode: individual letters adjacent
    touching = ''.join(d['bitmap'] for d in letter_data)
    
    # OVERLAPPING mode: combined via OR operation
    combined_binary = 0
    for d in letter_data:
        if d['binary']:
            combined_binary |= d['binary']
    combined_segments = binary_to_segments(combined_binary)
    overlapping = _bitmap(combined_segments)
    
    return {
        'word': word,
        'category': category,
        'frequency_rank': rank,
        'letters': letter_data,
        'composition': {
            'spaced': spaced,
            'touching': touching,
            'overlapping': overlapping
        },
        'combined_binary': f"{combined_binary:07b}",
        'combined_hex': f"0x{combined_binary:02X}",
        'combined_segments': combined_segments
    }


# Dictionary of 50 common English words
GLYPHOFORM_DICTIONARY = {
    # === GREETINGS & SOCIAL (5 words) ===
    "HELLO": _make_entry("HELLO", "greeting", 1),
    "HI": _make_entry("HI", "greeting", 2),
    "THANKS": _make_entry("THANKS", "social", 3),
    "PLEASE": _make_entry("PLEASE", "social", 4),
    "SORRY": _make_entry("SORRY", "social", 5),
    
    # === PRONOUNS (5 words) ===
    "I": _make_entry("I", "pronoun", 6),
    "YOU": _make_entry("YOU", "pronoun", 7),
    "ME": _make_entry("ME", "pronoun", 8),
    "WE": _make_entry("WE", "pronoun", 9),
    "THEY": _make_entry("THEY", "pronoun", 10),
    
    # === VERBS (21 words) ===
    "IS": _make_entry("IS", "verb", 11),
    "ARE": _make_entry("ARE", "verb", 12),
    "WAS": _make_entry("WAS", "verb", 13),
    "GO": _make_entry("GO", "verb", 14),
    "MAKE": _make_entry("MAKE", "verb", 15),
    "GET": _make_entry("GET", "verb", 16),
    "KNOW": _make_entry("KNOW", "verb", 17),
    "TAKE": _make_entry("TAKE", "verb", 18),
    "COME": _make_entry("COME", "verb", 19),
    "THINK": _make_entry("THINK", "verb", 20),
    "LOOK": _make_entry("LOOK", "verb", 21),
    "WANT": _make_entry("WANT", "verb", 22),
    "GIVE": _make_entry("GIVE", "verb", 23),
    "USE": _make_entry("USE", "verb", 24),
    "FIND": _make_entry("FIND", "verb", 25),
    "TELL": _make_entry("TELL", "verb", 26),
    "ASK": _make_entry("ASK", "verb", 27),
    "WORK": _make_entry("WORK", "verb", 28),
    "SEEM": _make_entry("SEEM", "verb", 29),
    "FEEL": _make_entry("FEEL", "verb", 30),
    "TRY": _make_entry("TRY", "verb", 31),
    
    # === ARTICLES & DETERMINERS (5 words) ===
    "THE": _make_entry("THE", "article", 32),
    "A": _make_entry("A", "article", 33),
    "AN": _make_entry("AN", "article", 34),
    "THIS": _make_entry("THIS", "determiner", 35),
    "THAT": _make_entry("THAT", "determiner", 36),
    
    # === PREPOSITIONS (4 words) ===
    "WITH": _make_entry("WITH", "preposition", 37),
    "FROM": _make_entry("FROM", "preposition", 38),
    "UP": _make_entry("UP", "preposition", 39),
    "DOWN": _make_entry("DOWN", "preposition", 40),
    
    # === NOUNS (10 words) ===
    "TIME": _make_entry("TIME", "noun", 41),
    "WAY": _make_entry("WAY", "noun", 42),
    "DAY": _make_entry("DAY", "noun", 43),
    "MAN": _make_entry("MAN", "noun", 44),
    "WORLD": _make_entry("WORLD", "noun", 45),
    "LIFE": _make_entry("LIFE", "noun", 46),
    "HAND": _make_entry("HAND", "noun", 47),
    "PART": _make_entry("PART", "noun", 48),
    "EYE": _make_entry("EYE", "noun", 49),
    "PLACE": _make_entry("PLACE", "noun", 50),
}


def lookup_word(word):
    """Look up a word in the glyphoform dictionary."""
    return GLYPHOFORM_DICTIONARY.get(word.upper())


def get_words_by_category(category):
    """Get all words in a specific category."""
    return {k: v for k, v in GLYPHOFORM_DICTIONARY.items() 
            if v['category'] == category}


def get_all_categories():
    """Get list of all categories in the dictionary."""
    return sorted(set(v['category'] for v in GLYPHOFORM_DICTIONARY.values()))


def display_dictionary(mode='spaced'):
    """Display the entire dictionary in formatted output."""
    lines = ["═" * 70]
    lines.append("GLYPHOFORM DICTIONARY - 50 Common Words (7-Segment Encoding)")
    lines.append("═" * 70)
    lines.append(f"Mode: {mode.upper()} | Notation: [A,B,C,D,E,F,G] where active segments shown")
    lines.append("")
    
    current_category = None
    for word, data in sorted(GLYPHOFORM_DICTIONARY.items(), 
                              key=lambda x: x[1]['frequency_rank']):
        if data['category'] != current_category:
            current_category = data['category']
            lines.append(f"📁 {current_category.upper()}")
            lines.append("-" * 50)
        
        comp = data['composition'][mode]
        combined = data['combined_binary']
        lines.append(f"  {word:12} → {comp:40}  combined:{combined}")
    
    lines.append("")
    lines.append("═" * 70)
    return '\n'.join(lines)


def display_word_detail(word):
    """Display detailed breakdown of a word."""
    word = word.upper()
    entry = GLYPHOFORM_DICTIONARY.get(word)
    if not entry:
        return f"Word '{word}' not found in dictionary."
    
    lines = [f"{'='*60}"]
    lines.append(f"WORD: {word}")
    lines.append(f"Category: {entry['category']} | Rank: {entry['frequency_rank']}")
    lines.append(f"{'='*60}")
    lines.append("")
    
    # Individual letters
    lines.append("LETTER BREAKDOWN:")
    lines.append("-" * 40)
    for letter_data in entry['letters']:
        lines.append(f"  {letter_data['letter']}: {letter_data['bitmap']} = {letter_data['binary']:07b}")
    
    lines.append("")
    lines.append("COMPOSITION MODES:")
    lines.append("-" * 40)
    lines.append(f"  SPACED:    {entry['composition']['spaced']}")
    lines.append(f"  TOUCHING:  {entry['composition']['touching']}")
    lines.append(f"  OVERLAP:   {entry['composition']['overlapping']}")
    
    lines.append("")
    lines.append("COMBINED (OVERLAPPING) DATA:")
    lines.append("-" * 40)
    lines.append(f"  Binary:  [{entry['combined_binary']}]")
    lines.append(f"  Hex:     {entry['combined_hex']}")
    lines.append(f"  Segments: {entry['combined_segments']}")
    
    lines.append("")
    lines.append(f"{'='*60}")
    
    return '\n'.join(lines)


# Initialize converter for dynamic lookups
from .converter import GlyphoformConverter
_converter = GlyphoformConverter()


def convert_or_lookup(word):
    """
    Try dictionary lookup first, fall back to conversion.
    
    Returns tuple: (result, source) where source is 'dictionary' or 'computed'
    """
    word = word.upper()
    if word in GLYPHOFORM_DICTIONARY:
        return GLYPHOFORM_DICTIONARY[word]['composition']['spaced'], 'dictionary'
    return _converter.convert(word), 'computed'

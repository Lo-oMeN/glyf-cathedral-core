"""
glyph_tokenizer.py - Byte-level geometric tokenizer

Maps UTF-8 characters to GlyfPrimitive enum values based on phonetic/structural properties.
Preserves case as chirality bit.
"""
from dataclasses import dataclass
from enum import IntEnum
from typing import List, Tuple

class GlyfPrimitive(IntEnum):
    """Geometric primitive types for token encoding."""
    GLYPH_VOID = 0      # Space, punctuation, control chars
    GLYPH_DOT = 1       # Capital marker / isolated points
    GLYPH_CURVE = 2     # Vowels (aeiou) - flowing, continuous
    GLYPH_LINE = 3      # Soft consonants (lmnrsf) - smooth transitions
    GLYPH_ANGLE = 4     # Hard consonants (ktpdbg) - sharp transitions
    GLYPH_SIBILANT = 5  # Sibilants (hzx) - variant curves
    GLYPH_RESERVED = 6  # Future expansion

# Character classification sets
VOWELS = set('aeiouAEIOU')
HARD_CONSONANTS = set('ktpdbgqjkKTPDBGQJK')
SOFT_CONSONANTS = set('lmnrsfwyLMNRSFWY')
SIBILANTS = set('hzxHZX')
PUNCTUATION_SPACE = set(' \t\n\r\f\v!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')

@dataclass
class Token:
    """A geometric token with glyph type and chirality (case)."""
    glyph_type: int      # GlyfPrimitive value (0-6)
    chirality: int       # 0=lowercase, 1=uppercase
    char: str            # Original character (for debugging)
    
    def __repr__(self) -> str:
        glyph_name = GlyfPrimitive(self.glyph_type).name
        case = "UPPER" if self.chirality else "lower"
        return f"Token({self.char!r}, {glyph_name}, {case})"

def classify_char(c: str) -> Tuple[int, int]:
    """
    Classify a single character to glyph type and chirality.
    
    Returns:
        (glyph_type, chirality): GlyphPrimitive value and case bit
    """
    if len(c) != 1:
        return (GlyfPrimitive.GLYPH_VOID, 0)
    
    # Determine chirality from case
    chirality = 1 if c.isupper() else 0
    
    # Classify by character type
    if c in PUNCTUATION_SPACE:
        return (GlyfPrimitive.GLYPH_VOID, 0)
    elif c in VOWELS:
        return (GlyfPrimitive.GLYPH_CURVE, chirality)
    elif c in HARD_CONSONANTS:
        return (GlyfPrimitive.GLYPH_ANGLE, chirality)
    elif c in SOFT_CONSONANTS:
        return (GlyfPrimitive.GLYPH_LINE, chirality)
    elif c in SIBILANTS:
        return (GlyfPrimitive.GLYPH_SIBILANT, chirality)
    elif c.isalpha():
        # Other alphabetic characters default to LINE
        return (GlyfPrimitive.GLYPH_LINE, chirality)
    else:
        # Numbers and other symbols become VOID
        return (GlyfPrimitive.GLYPH_VOID, 0)

def glyph_tokenize(text: str) -> List[Token]:
    """
    Tokenize raw UTF-8 text into geometric primitives.
    
    Args:
        text: Raw input text (UTF-8)
        
    Returns:
        List of Token objects with glyph_type and chirality
    """
    tokens = []
    for c in text:
        glyph_type, chirality = classify_char(c)
        
        # Capital letters emit DOT + primitive sequence
        if chirality == 1 and glyph_type != GlyfPrimitive.GLYPH_VOID:
            # Prepend DOT marker for capitals
            tokens.append(Token(GlyfPrimitive.GLYPH_DOT, 0, c))
        
        tokens.append(Token(glyph_type, chirality, c))
    
    return tokens

def tokenize_to_integers(text: str) -> List[int]:
    """
    Convenience function: returns just the glyph type integers.
    
    Args:
        text: Raw input text
        
    Returns:
        List of integer glyph type values (0-6)
    """
    tokens = glyph_tokenize(text)
    return [t.glyph_type for t in tokens]

def get_token_stats(tokens: List[Token]) -> dict:
    """
    Compute statistics about a token sequence.
    
    Args:
        tokens: List of Token objects
        
    Returns:
        Dictionary with count statistics per glyph type
    """
    stats = {name: 0 for name in GlyfPrimitive.__members__}
    upper_count = 0
    
    for t in tokens:
        stats[GlyfPrimitive(t.glyph_type).name] += 1
        if t.chirality:
            upper_count += 1
    
    stats['TOTAL'] = len(tokens)
    stats['UPPERCASE'] = upper_count
    return stats


if __name__ == "__main__":
    # Simple test
    test_text = "The quick brown fox"
    tokens = glyph_tokenize(test_text)
    
    print(f"Input: {test_text!r}")
    print(f"Tokens ({len(tokens)} total):")
    for i, t in enumerate(tokens):
        print(f"  {i:2d}: {t}")
    
    print("\nStatistics:")
    stats = get_token_stats(tokens)
    for k, v in stats.items():
        print(f"  {k}: {v}")

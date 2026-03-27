#!/usr/bin/env python3
"""
Glyphoform Converter Demo v2.0
Demonstrates canonical 7-segment English-to-Glyphoform conversion.

Shows all three composition modes:
- SPACED:    Letters separated with gaps
- TOUCHING:  Letters adjacent  
- OVERLAPPING: Letters combined via segment OR operation
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace')

from glyf.core.converter import (
    GlyphoformConverter,
    to_bitmap,
    to_binary,
    to_segments,
    analyze_word,
    lookup_word,
    display_dictionary,
    display_word_detail,
    CompositionMode
)

print("=" * 70)
print("   GLYPHOFORM CONVERTER v2.0")
print("   Canonical 7-Segment Digital Display Encoding")
print("=" * 70)
print()
print("Segment Layout:")
print("    -- A --")
print("   |       |")
print("   F       B")
print("   |       |")
print("    -- G --  ")
print("   |       |")
print("   E       C")
print("   |       |")
print("    -- D --")
print()

# 1. Alphabet Reference
print("═" * 70)
print("ALPHABET REFERENCE (Segment Bitmaps)")
print("═" * 70)
converter = GlyphoformConverter(style='bitmap')
for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    bitmap = converter.convert_letter(letter)
    info = converter.decompose(letter)[0]
    binary = f"{info['binary']:07b}"
    print(f"  {letter}: {bitmap} = [{binary}]")

print()

# 2. Three Composition Modes Demo
print("═" * 70)
print("COMPOSITION MODES COMPARISON")
print("═" * 70)
test_words = ["HI", "GO", "CAT", "HELLO"]

for word in test_words:
    print(f"\n  Word: '{word}'")
    print("  " + "-" * 50)
    
    for mode in ['spaced', 'touching', 'overlapping']:
        result = to_bitmap(word, mode=mode)
        print(f"  {mode.upper():12}: {result}")
    
    # Show overlapping binary
    overlap_binary = to_binary(word, mode='overlapping')
    print(f"  {'OVERLAP BIN':12}: {overlap_binary}")

print()

# 3. Visual ASCII Art
print("═" * 70)
print("VISUAL 7-SEGMENT DISPLAY")
print("═" * 70)
converter = GlyphoformConverter(style='visual')
print(converter.convert("HI"))
print()
print(converter.convert("GO"))

print()

# 4. Detailed Analysis
print("═" * 70)
print("DETAILED WORD ANALYSIS")
print("═" * 70)
print(analyze_word("GO"))

print()

# 5. Dictionary Demo
print("═" * 70)
print("PRE-CONVERTED DICTIONARY (50 Words)")
print("═" * 70)

# Show sample from each category
categories = ['greeting', 'pronoun', 'verb', 'article', 'noun']
cat_samples = {
    'greeting': ['HELLO', 'THANKS'],
    'pronoun': ['I', 'YOU'],
    'verb': ['GO', 'THINK'],
    'article': ['THE', 'A'],
    'noun': ['TIME', 'WORLD']
}

for cat in categories:
    print(f"\n  📁 {cat.upper()}")
    print("  " + "-" * 50)
    for word in cat_samples.get(cat, []):
        entry = lookup_word(word)
        if entry:
            spaced = entry['composition']['spaced']
            overlap = entry['composition']['overlapping']
            print(f"    {word:12} spaced: {spaced}")
            print(f"               overlap: {overlap}")

print()

# 6. Full Dictionary in Spaced Mode
print("═" * 70)
print("FULL DICTIONARY (SPACED MODE - First 15 entries)")
print("═" * 70)
from glyf.core.converter.dictionary import GLYPHOFORM_DICTIONARY
sorted_words = sorted(GLYPHOFORM_DICTIONARY.items(), key=lambda x: x[1]['frequency_rank'])
for word, data in sorted_words[:15]:
    print(f"  {word:12} → {data['composition']['spaced']}")

print()

# 7. Overlapping Mode Examples
print("═" * 70)
print("OVERLAPPING MODE EXAMPLES (Letters OR'd together)")
print("═" * 70)
overlap_words = ['HI', 'GO', 'WE', 'ME', 'UP']
for word in overlap_words:
    entry = lookup_word(word)
    if entry:
        layers = ' + '.join(f"{l['letter']}={l['bitmap']}" for l in entry['letters'])
        combined = entry['composition']['overlapping']
        binary = entry['combined_binary']
        print(f"  {word:6}: {layers}")
        print(f"        = {combined} [{binary}]")
        print()

print("═" * 70)
print("DEMO COMPLETE")
print("═" * 70)
print()
print("Try it yourself:")
print("  python3 -c \"from glyf.core.converter import to_bitmap; print(to_bitmap('YOUR WORD', mode='overlapping'))\"")

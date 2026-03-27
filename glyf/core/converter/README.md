# English-to-Glyphoform Converter v2.0

A creative text transformation system that converts English words to **glyphoform notation** using **canonical 7-segment digital display encoding**.

## Canonical 7-Segment Display Grid

```
    -- A --
   |       |
   F       B
   |       |
    -- G --  
   |       |
   E       C
   |       |
    -- D --
```

**Segments:** A(top), B(upper-right), C(lower-right), D(bottom), E(lower-left), F(upper-left), G(middle)

## Quick Start

```python
from glyf.core.converter import to_bitmap, to_binary, to_segments

# Bitmap notation (dots for inactive segments)
print(to_bitmap("HI"))  # [.,B,C,.,E,F,G]  [.,B,C,.,.,.,.]

# Binary notation
print(to_binary("GO"))  # [1111111]

# Segment list notation  
print(to_segments("CAT"))  # [A,.,.,D,E,F,.] [A,B,C,.,E,F,G] [A,.,.,.,E,F,.]
```

## Three Composition Modes

### 1. SPACED (Default)
Letters displayed separately with gaps:
```
HI → [.,B,C,.,E,F,G]  [.,B,C,.,.,.,.]
```

### 2. TOUCHING
Letters adjacent without gaps:
```
HI → [.,B,C,.,E,F,G][.,B,C,.,.,.,.]
```

### 3. OVERLAPPING
Letters combined via OR operation on segments:
```
HI → [.,B,C,.,E,F,G] (H=[.,B,C,.,E,F,G] OR I=[.,B,C,.,.,.,.])
```

## Letter Mappings (A-Z)

| Letter | Bitmap | Binary | Active Segments |
|--------|--------|--------|-----------------|
| A | [A,B,C,.,E,F,G] | 1110111 | A,B,C,E,F,G |
| B | [A,B,C,D,E,F,G] | 1111111 | All |
| C | [A,.,.,D,E,F,.] | 1001110 | A,D,E,F |
| D | [A,B,C,D,E,F,.] | 0111111 | A,B,C,D,E,F |
| E | [A,.,.,D,E,F,G] | 1001111 | A,D,E,F,G |
| F | [A,.,.,.,E,F,G] | 1000111 | A,E,F,G |
| G | [A,B,C,D,E,F,.] | 1111011 | A,B,C,D,E,F |
| H | [.,B,C,.,E,F,G] | 0110111 | B,C,E,F,G |
| I | [.,B,C,.,.,.,.] | 0110000 | B,C |
| J | [.,B,C,D,E,.,.] | 0111100 | B,C,D,E |
| K | [.,B,.,.,E,F,G] | 0110110 | B,E,F,G |
| L | [.,.,.,D,E,F,.] | 0001110 | D,E,F |
| M | [A,B,C,.,E,F,.] | 1110110 | A,B,C,E,F |
| N | [A,B,C,.,E,F,.] | 1110110 | A,B,C,E,F |
| O | [A,B,C,D,E,F,.] | 1111110 | A,B,C,D,E,F |
| P | [A,B,.,.,E,F,G] | 1100111 | A,B,E,F,G |
| Q | [A,B,C,D,E,F,G] | 1111111 | All |
| R | [A,B,C,.,E,F,G] | 1110111 | A,B,C,E,F,G |
| S | [A,B,.,D,E,.,G] | 1011011 | A,B,D,E,G |
| T | [A,.,.,.,E,F,.] | 1000110 | A,E,F |
| U | [.,B,C,D,E,F,.] | 0111110 | B,C,D,E,F |
| V | [.,.,C,D,E,F,.] | 0011110 | C,D,E,F |
| W | [.,B,C,D,E,F,.] | 0111110 | B,C,D,E,F |
| X | [.,B,C,.,E,F,.] | 0110110 | B,C,E,F |
| Y | [.,B,C,D,E,F,G] | 0111011 | B,C,D,E,F,G |
| Z | [A,B,.,D,E,.,G] | 1101101 | A,B,D,E,G |

## API Reference

### Conversion Functions

```python
from glyf.core.converter import to_bitmap, to_binary, to_segments, to_glyphoform

# All functions support mode parameter: 'spaced', 'touching', 'overlapping'
to_bitmap("WORD", mode="spaced")      # [A,B,C,.,E,F,G]  [.,.,.,D,E,F,.]
to_binary("WORD", mode="overlapping")  # [1110111]
to_segments("WORD", mode="touching")   # [A,B,C] [D,E,F]
```

### Composition Mode Constants

```python
from glyf.core.converter import CompositionMode

converter = GlyphoformConverter(
    style='bitmap', 
    composition_mode=CompositionMode.OVERLAPPING
)
```

### Detailed Analysis

```python
from glyf.core.converter import analyze_word

print(analyze_word("GO"))
# Shows letter breakdown + all 3 composition modes
```

### Visual Display

```python
converter = GlyphoformConverter(style='visual')
print(converter.convert("HI"))
# Outputs ASCII art 7-segment display
```

## Pre-Converted Dictionary (50 Words)

Each entry includes:
- Individual letter bitmaps
- All 3 composition modes
- Combined binary/hex values

### Sample Entries:

```python
from glyf.core.converter.dictionary import lookup_word, display_dictionary

# Look up specific word
entry = lookup_word("HELLO")
# Returns:
# {
#   'word': 'HELLO',
#   'letters': [
#     {'letter': 'H', 'bitmap': '[.,B,C,.,E,F,G]', 'binary': 55, ...},
#     ...
#   ],
#   'composition': {
#     'spaced': '[.,B,C,.,E,F,G]  [A,.,.,D,E,F,G]  ...',
#     'touching': '[.,B,C,.,E,F,G][A,.,.,D,E,F,G]...',
#     'overlapping': '[A,B,C,D,E,F,G]'
#   },
#   'combined_binary': '1111111'
# }

# Display all words
print(display_dictionary(mode='overlapping'))
```

### Categories (50 words total):
- **Greeting:** HELLO, HI
- **Social:** THANKS, PLEASE, SORRY  
- **Pronoun:** I, YOU, ME, WE, THEY
- **Verb:** IS, ARE, WAS, GO, MAKE, GET, KNOW, TAKE, COME, THINK, LOOK, WANT, GIVE, USE, FIND, TELL, ASK, WORK, SEEM, FEEL, TRY
- **Article:** THE, A, AN
- **Determiner:** THIS, THAT
- **Preposition:** WITH, FROM, UP, DOWN
- **Noun:** TIME, WAY, DAY, MAN, WORLD, LIFE, HAND, PART, EYE, PLACE

## Running the Demo

```bash
python3 /root/.openclaw/workspace/glyf/core/converter/demo.py
```

Shows:
- Full alphabet with segment bitmaps
- All 3 composition modes comparison
- Visual ASCII art displays
- Detailed word analysis
- Dictionary samples

## Notation Formats

### Bitmap Notation (Default)
```
[A,B,C,.,E,F,G]  = segments A,B,C,E,F,G active (D inactive)
[.,.,.,.,.,.,.]  = all segments inactive
```

### Binary Notation
```
[1110111] = A,B,C,E,F,G active (D=0)
```

### Hex Notation
```
[0x77] = same as 1110111 binary
```

### Segment List
```
[A,B,C,E,F,G] = list of active segment names
```

## Overlapping Mode Logic

In overlapping mode, each letter's binary pattern is OR'd together:

```
H = [.,B,C,.,E,F,G] = 0110111 (binary)
I = [.,B,C,.,.,.,.] = 0110000 (binary)
    
OR:                   0110111 (result)
```

This creates unified glyphoforms where shared segments reinforce each other.

## File Structure

```
/root/.openclaw/workspace/glyf/core/converter/
├── __init__.py      # Package exports
├── glyphmap.py      # 7-segment A-Z mappings
├── converter.py     # Main converter with composition modes
├── dictionary.py    # 50 pre-converted words
├── demo.py          # Interactive demo
└── README.md        # This file
```

## License

Part of the Glyf project - geometric typography exploration using canonical 7-segment digital display encoding.

# GLYF Core Parser - 7-Segment Display Edition

A Kotlin recursive descent parser for GLYF (Glyph Language Yield Format) notation, representing **canonical 7-segment display compositions**.

## 7-Segment Display Architecture

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

### Segments

| Segment | Position      | Description     |
|---------|---------------|-----------------|
| A       | Top           | Horizontal top  |
| B       | Upper-right   | Vertical right  |
| C       | Lower-right   | Vertical right  |
| D       | Bottom        | Horizontal bottom|
| E       | Lower-left    | Vertical left   |
| F       | Upper-left    | Vertical left   |
| G       | Middle        | Horizontal center|

## Composition Modes

When combining multiple letter/digit patterns into words:

| Mode      | Operator | Description                          | Example            |
|-----------|----------|--------------------------------------|--------------------|
| OVERLAP   | `/`      | Letters overlay on same grid         | `[A/B]` = merge    |
| TOUCH     | `\|`     | Letters adjacent, grids share edges  | `[A\|B]` = side-by-side |
| SPACE     | `-`      | Letters separated, distinct grids    | `[A-B]` = spaced   |

## Grammar

```
expr        ::= '[' composed_expr ']' | composed_expr
composed_expr ::= space_expr
space_expr  ::= touch_expr ( '-' touch_expr )*
touch_expr  ::= overlap_expr ( '|' overlap_expr )*
overlap_expr ::= primary ( '/' primary )*
primary     ::= segment_pattern | char_ref | group | bracket_expr
segment_pattern ::= [A-Ga-g]+
char_ref    ::= [0-9A-Za-z]
group       ::= '(' composed_expr ')'
```

### Operator Precedence (highest to lowest)

1. `/` (OVERLAP) - Highest: segments merge on same grid
2. `|` (TOUCH)   - Middle: adjacent grid positions
3. `-` (SPACE)   - Lowest: separated grid positions

Use `()` grouping to override precedence.

## Usage

```kotlin
import glyf.core.parser.GlyfParser
import glyf.core.parser.SevenSegmentChars

// Parse a bracket expression
val ast = GlyfParser.parse("[CEFG|BC]")  // "HI"

// Convert back to notation
val notation = ast.toNotation()  // "[CEFG|BC]"

// Create patterns programmatically
val pattern = SevenSegmentPattern("ABFG")  // digit 4
val blank = SevenSegmentPattern()          // all off (~)

// Use predefined character patterns
val digitEight = SevenSegmentChars.DIGITS['8']
val letterA = SevenSegmentChars.LETTERS['A']

// Pattern operations
val overlaid = pattern.overlay(SevenSegmentPattern("CDE"))
```

## Examples

### Single Patterns

| Expression | Description                    | Visual (segments lit) |
|------------|--------------------------------|----------------------|
| `[A]`      | Top segment only               | ― (top bar)          |
| `[G]`      | Middle segment only            | ― (center bar)       |
| `[ABC]`    | Digit 7 pattern                | ７                   |
| `[~]`      | Blank (no segments)            | (empty)              |

### Composition Examples

| Expression              | Description                              |
|-------------------------|------------------------------------------|
| `[A/B]`                 | Overlap: A OR B segments                 |
| `[A\|B\|C]`             | Touch: three adjacent positions          |
| `[A-B-C]`               | Space: three separated positions         |
| `[CEFG\|BC]`            | "HI" - H touching I                      |
| `[BC-ABGED]`            | "1 2" - digit 1 spaced from digit 2      |
| `[(A\|B)/C]`            | Group: (A touch B) overlapped with C     |
| `[ABCDEFG/BC]`          | Overlap 8 and 1 = still 8                |
| `[CEFG\|AFEDG\|FED\|FED\|ABCDEF]` | "HELLO" touching          |

### Complex Nested

```
[(A|B)/C-(D|E)|F]
```
Parses as:
```
Space(
  Overlap(
    Group(Touch(A, B)),
    C
  ),
  Touch(
    Group(Space(D, E)),
    F
  )
)
```

## Predefined Characters

### Digits (0-9)

| Digit | Pattern | Segments Lit    |
|-------|---------|-----------------|
| 0     | ABCDEF  | All except G    |
| 1     | BC      | Right side      |
| 2     | ABGED   | Top, mid, bot + |
| 3     | ABGCD   | Top, mid, bot + |
| 4     | FGBC    | Middle + right  |
| 5     | AFGCD   | Top-left + right|
| 6     | AFEDCG  | All except B    |
| 7     | ABC     | Top + right     |
| 8     | ABCDEFG | All segments    |
| 9     | ABFGC   | All except E    |

### Letters (selected)

| Letter | Pattern | Description        |
|--------|---------|--------------------|
| A      | ABCEFG  | Like 8 minus D     |
| C      | AFED    | Like 0 minus B,C,G |
| E      | AFEDG   | Like 8 minus B,C   |
| F      | AFGE    | Like E minus D     |
| H      | CEFG    | Middle + sides     |
| L      | FED     | Left side + bottom |
| O      | ABCDEF  | Same as 0          |
| P      | ABEFG   | Like 9 minus C     |

## AST Structure

```
GlyfNode (sealed)
├── SevenSegmentPattern  - Single 7-segment pattern
├── CharRef              - Reference to named char
├── ComposedGlyph (sealed)
│   ├── Overlap          - / composition
│   ├── Touch            - | composition
│   └── Space            - - composition
├── Group                - () grouping
└── BracketExpr          - [] wrapper
```

## Files

- `GlyfNode.kt` - AST node definitions (sealed classes, patterns, chars)
- `GlyfParser.kt` - Recursive descent parser implementation
- `GlyfParserTest.kt` - Unit tests (32+ test cases)

## Running Tests

```bash
# With Gradle
./gradlew test

# Or run specific test
./gradlew test --tests "GlyfParserTest"
```

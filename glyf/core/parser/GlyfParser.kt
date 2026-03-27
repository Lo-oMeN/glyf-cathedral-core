package glyf.core.parser

/**
 * Recursive descent parser for GLYF 7-segment display notation.
 *
 * Grammar:
 *   expr        ::= bracket_expr | composed_expr
 *   bracket_expr ::= '[' composed_expr ']'
 *   composed_expr ::= space_expr
 *   space_expr  ::= touch_expr ( '-' touch_expr )*
 *   touch_expr  ::= overlap_expr ( '|' overlap_expr )*
 *   overlap_expr ::= primary ( '/' primary )*
 *   primary     ::= segment_pattern | char_ref | group | bracket_expr
 *   segment_pattern ::= segment+
 *   segment     ::= 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G'
 *   char_ref    ::= [0-9A-Z]
 *   group       ::= '(' composed_expr ')'
 *
 * Operator precedence (highest to lowest):
 *   1. / (overlap) - segments merge on same grid
 *   2. | (touch)   - adjacent grids
 *   3. - (space)   - separated grids
 *
 * Examples:
 *   [ABFG]        - Pattern with segments A,B,F,G lit
 *   [A/B]         - Overlap: A's segments OR B's segments
 *   [A|B]         - Touch: A adjacent to B
 *   [A-B]         - Space: A separated from B
 *   [AB|CD|EF]    - Three patterns touching
 *   [(A|B)/C]     - Touch A|B, then overlap with C
 */
class GlyfParser(private val input: String) {
    private var pos = 0

    companion object {
        fun parse(input: String): GlyfNode {
            return GlyfParser(input.trim()).parseExpr()
        }
    }

    private fun peek(): Char? {
        return if (pos < input.length) input[pos] else null
    }

    private fun peekAhead(offset: Int): Char? {
        val idx = pos + offset
        return if (idx < input.length) input[idx] else null
    }

    private fun consume(): Char? {
        return if (pos < input.length) input[pos++] else null
    }

    private fun expect(expected: Char): Char {
        val ch = consume()
        if (ch != expected) {
            throw ParseException(
                "Expected '$expected' at position $pos, found '${ch ?: "EOF"}' in: $input"
            )
        }
        return ch
    }

    private fun skipWhitespace() {
        while (peek()?.isWhitespace() == true) {
            consume()
        }
    }

    /**
     * Parse a complete expression (with or without brackets).
     */
    fun parseExpr(): GlyfNode {
        skipWhitespace()
        return if (peek() == '[') {
            parseBracketExpr()
        } else {
            parseComposedExpr()
        }
    }

    /**
     * Parse bracket-wrapped expression: [inner]
     */
    private fun parseBracketExpr(): BracketExpr {
        expect('[')
        skipWhitespace()
        val inner = parseComposedExpr()
        skipWhitespace()
        expect(']')
        return BracketExpr(inner)
    }

    /**
     * Parse composed expression with operator precedence.
     * Lowest precedence: space (-)
     */
    private fun parseComposedExpr(): GlyfNode {
        return parseSpaceExpr()
    }

    /**
     * Parse space expressions: touch_expr ('-' touch_expr)*
     * Lowest precedence - separated grids
     */
    private fun parseSpaceExpr(): GlyfNode {
        val elements = mutableListOf<GlyfNode>()
        elements.add(parseTouchExpr())

        while (true) {
            skipWhitespace()
            if (peek() == '-') {
                consume() // consume '-'
                skipWhitespace()
                elements.add(parseTouchExpr())
            } else {
                break
            }
        }

        return if (elements.size == 1) elements[0] else Space(elements)
    }

    /**
     * Parse touch expressions: overlap_expr ('|' overlap_expr)*
     * Middle precedence - adjacent grids
     */
    private fun parseTouchExpr(): GlyfNode {
        val elements = mutableListOf<GlyfNode>()
        elements.add(parseOverlapExpr())

        while (true) {
            skipWhitespace()
            if (peek() == '|') {
                consume() // consume '|'
                skipWhitespace()
                elements.add(parseOverlapExpr())
            } else {
                break
            }
        }

        return if (elements.size == 1) elements[0] else Touch(elements)
    }

    /**
     * Parse overlap expressions: primary ('/' primary)*
     * Highest precedence among operators - overlay on same grid
     */
    private fun parseOverlapExpr(): GlyfNode {
        val elements = mutableListOf<GlyfNode>()
        elements.add(parsePrimary())

        while (true) {
            skipWhitespace()
            if (peek() == '/') {
                consume() // consume '/'
                skipWhitespace()
                elements.add(parsePrimary())
            } else {
                break
            }
        }

        return if (elements.size == 1) elements[0] else Overlap(elements)
    }

    /**
     * Parse primary expressions: segment_pattern, char_ref, group, or bracket_expr
     */
    private fun parsePrimary(): GlyfNode {
        skipWhitespace()
        return when (val ch = peek()) {
            '(' -> parseGroup()
            '[' -> parseBracketExpr()
            in 'A'..'G', in 'a'..'g' -> parseSegmentPattern()
            in '0'..'9', in 'H'..'Z', in 'h'..'z' -> parseCharRef()
            '~' -> parseBlankPattern()
            null -> throw ParseException("Unexpected end of input at position $pos")
            else -> throw ParseException("Unexpected character '$ch' at position $pos in: $input")
        }
    }

    /**
     * Parse a segment pattern: one or more of A-G
     * Examples: "A", "AB", "ABFG", "abcdefg"
     */
    private fun parseSegmentPattern(): SevenSegmentPattern {
        val segments = mutableSetOf<Char>()

        while (true) {
            val ch = peek()
            if (ch != null && (ch in 'A'..'G' || ch in 'a'..'g')) {
                consume()
                segments.add(ch.uppercaseChar())
            } else {
                break
            }
        }

        if (segments.isEmpty()) {
            throw ParseException("Expected segment pattern (A-G) at position $pos")
        }

        return SevenSegmentPattern(segments)
    }

    /**
     * Parse blank pattern: ~
     */
    private fun parseBlankPattern(): SevenSegmentPattern {
        consume() // consume '~'
        return SevenSegmentPattern()
    }

    /**
     * Parse a character reference: single digit or letter
     */
    private fun parseCharRef(): CharRef {
        val ch = consume()
            ?: throw ParseException("Expected character reference at position $pos")
        return CharRef(ch)
    }

    /**
     * Parse grouping: (inner)
     */
    private fun parseGroup(): Group {
        expect('(')
        skipWhitespace()
        val inner = parseComposedExpr()
        skipWhitespace()
        expect(')')
        return Group(inner)
    }
}

class ParseException(message: String) : Exception(message)

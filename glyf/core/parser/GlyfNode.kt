package glyf.core.parser

/**
 * AST Node for GLYF 7-segment display composition.
 *
 * CANONICAL 7-SEGMENT DISPLAY GRID:
 * ```
 *  -- A --
 * |       |
 * F       B
 * |       |
 *  -- G --
 * |       |
 * E       C
 * |       |
 *  -- D --
 * ```
 *
 * Segments: A(top), B(upper-right), C(lower-right), D(bottom),
 *           E(lower-left), F(upper-left), G(middle)
 *
 * COMPOSITION MODES for multi-letter words:
 * - OVERLAP: Letters share same grid position (segments overlay)
 * - TOUCH:   Letters adjacent, grids share edges
 * - SPACE:   Letters separated, distinct grids
 */
sealed class GlyfNode {
    abstract fun toNotation(): String
}

/**
 * A single 7-segment display pattern.
 * Represents which segments (A-G) are lit for one character position.
 */
data class SevenSegmentPattern(
    val a: Boolean = false,
    val b: Boolean = false,
    val c: Boolean = false,
    val d: Boolean = false,
    val e: Boolean = false,
    val f: Boolean = false,
    val g: Boolean = false
) : GlyfNode() {
    /**
     * Create from segment string like "ABFG" or "abcdefg"
     */
    constructor(segments: String) : this(
        a = segments.contains('A', ignoreCase = true),
        b = segments.contains('B', ignoreCase = true),
        c = segments.contains('C', ignoreCase = true),
        d = segments.contains('D', ignoreCase = true),
        e = segments.contains('E', ignoreCase = true),
        f = segments.contains('F', ignoreCase = true),
        g = segments.contains('G', ignoreCase = true)
    )

    /**
     * Create from set of segment chars
     */
    constructor(segments: Set<Char>) : this(
        a = 'A' in segments || 'a' in segments,
        b = 'B' in segments || 'b' in segments,
        c = 'C' in segments || 'c' in segments,
        d = 'D' in segments || 'd' in segments,
        e = 'E' in segments || 'e' in segments,
        f = 'F' in segments || 'f' in segments,
        g = 'G' in segments || 'g' in segments
    )

    /**
     * Get active segments as a set
     */
    fun toSegmentSet(): Set<Char> {
        return buildSet {
            if (a) add('A')
            if (b) add('B')
            if (c) add('C')
            if (d) add('D')
            if (e) add('E')
            if (f) add('F')
            if (g) add('G')
        }
    }

    /**
     * Overlay another pattern (OR operation)
     */
    fun overlay(other: SevenSegmentPattern): SevenSegmentPattern {
        return SevenSegmentPattern(
            a = this.a || other.a,
            b = this.b || other.b,
            c = this.c || other.c,
            d = this.d || other.d,
            e = this.e || other.e,
            f = this.f || other.f,
            g = this.g || other.g
        )
    }

    override fun toNotation(): String {
        val segs = toSegmentSet().joinToString("")
        return if (segs.isEmpty()) "~" else segs
    }

    override fun toString(): String = "SevenSegmentPattern(${toNotation()})"
}

/**
 * Predefined patterns for common characters on 7-segment display.
 */
object SevenSegmentChars {
    val DIGITS = mapOf(
        '0' to SevenSegmentPattern("ABCDEF"),
        '1' to SevenSegmentPattern("BC"),
        '2' to SevenSegmentPattern("ABGED"),
        '3' to SevenSegmentPattern("ABGCD"),
        '4' to SevenSegmentPattern("FGBC"),
        '5' to SevenSegmentPattern("AFGCD"),
        '6' to SevenSegmentPattern("AFEDCG"),
        '7' to SevenSegmentPattern("ABC"),
        '8' to SevenSegmentPattern("ABCDEFG"),
        '9' to SevenSegmentPattern("ABFGC")
    )

    val LETTERS = mapOf(
        'A' to SevenSegmentPattern("ABCEFG"),
        'B' to SevenSegmentPattern("FEDCG"),  // lowercase b style
        'C' to SevenSegmentPattern("AFED"),
        'D' to SevenSegmentPattern("GEDCB"),  // lowercase d style
        'E' to SevenSegmentPattern("AFEDG"),
        'F' to SevenSegmentPattern("AFGE"),
        'G' to SevenSegmentPattern("AFEDCG"), // same as 6
        'H' to SevenSegmentPattern("CEFG"),
        'I' to SevenSegmentPattern("BC"),     // same as 1
        'J' to SevenSegmentPattern("BCD"),
        'L' to SevenSegmentPattern("FED"),
        'N' to SevenSegmentPattern("ABCEF"),  // same as 0
        'O' to SevenSegmentPattern("ABCDEF"), // same as 0
        'P' to SevenSegmentPattern("ABEFG"),
        'S' to SevenSegmentPattern("AFGCD"),  // same as 5
        'U' to SevenSegmentPattern("BCDEF"),
        'Y' to SevenSegmentPattern("BCFGD")
    )

    val BLANK = SevenSegmentPattern()
}

/**
 * Composition mode for multi-letter glyph compositions.
 */
enum class CompositionMode {
    /** Letters share same grid (segments overlay/merge) */
    OVERLAP,
    /** Letters adjacent, grids share edges */
    TOUCH,
    /** Letters separated, distinct grids */
    SPACE
}

/**
 * A composed glyph - multiple letter patterns combined.
 */
sealed class ComposedGlyph : GlyfNode()

/**
 * OVERLAP composition: Letters overlay on same grid position.
 * Notation: A/B or [A/B]
 * Result: Segment-wise OR of all patterns
 */
data class Overlap(val patterns: List<GlyfNode>) : ComposedGlyph() {
    constructor(vararg patterns: GlyfNode) : this(patterns.toList())

    override fun toNotation(): String {
        return patterns.joinToString("/") { it.toNotation() }
    }
}

/**
 * TOUCH composition: Letters adjacent, grids share edges.
 * Notation: A|B or [A|B]
 * Result: Sequential display positions
 */
data class Touch(val patterns: List<GlyfNode>) : ComposedGlyph() {
    constructor(vararg patterns: GlyfNode) : this(patterns.toList())

    override fun toNotation(): String {
        return patterns.joinToString("|") { it.toNotation() }
    }
}

/**
 * SPACE composition: Letters separated with distinct spacing.
 * Notation: A-B or [A-B]
 * Result: Spaced display positions
 */
data class Space(val patterns: List<GlyfNode>) : ComposedGlyph() {
    constructor(vararg patterns: GlyfNode) : this(patterns.toList())

    override fun toNotation(): String {
        return patterns.joinToString("-") { it.toNotation() }
    }
}

/**
 * A complete bracket-wrapped glyph expression [expr].
 * This is the top-level container for GLYF notation.
 */
data class BracketExpr(val inner: GlyfNode) : GlyfNode() {
    override fun toNotation(): String = "[${inner.toNotation()}]"
}

/**
 * Grouping/containment for complex expressions.
 * Notation: (expr)
 */
data class Group(val inner: GlyfNode) : GlyfNode() {
    override fun toNotation(): String = "(${inner.toNotation()})"
}

/**
 * Reference to a named character pattern.
 * Allows referencing digits, letters, or custom definitions.
 */
data class CharRef(val char: Char) : GlyfNode() {
    override fun toNotation(): String = char.toString()
}

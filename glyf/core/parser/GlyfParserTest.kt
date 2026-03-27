package glyf.core.parser

import org.junit.Test
import org.junit.Assert.*

/**
 * Unit tests for GLYF 7-segment display parser.
 *
 * 7-SEGMENT GRID:
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
 */
class GlyfParserTest {

    // Helper function to assert round-trip parsing
    private fun assertRoundTrip(input: String) {
        val parsed = GlyfParser.parse(input)
        val output = parsed.toNotation()
        val normalizedInput = input.replace(" ", "")
        assertEquals("Round-trip failed for: $input", normalizedInput, output)
    }

    // Helper to parse
    private fun parse(input: String): GlyfNode = GlyfParser.parse(input)

    // ==================== BASIC SEGMENT PATTERNS ====================

    // Test 1: Single segment A (top horizontal)
    @Test
    fun testSingleSegmentA() {
        val result = parse("[A]")
        assertTrue(result is BracketExpr)
        val inner = (result as BracketExpr).inner
        assertTrue(inner is SevenSegmentPattern)
        val pat = inner as SevenSegmentPattern
        assertTrue(pat.a)
        assertFalse(pat.b)
        assertFalse(pat.c)
        assertFalse(pat.d)
        assertFalse(pat.e)
        assertFalse(pat.f)
        assertFalse(pat.g)
        assertRoundTrip("[A]")
    }

    // Test 2: Single segment G (middle horizontal)
    @Test
    fun testSingleSegmentG() {
        val result = parse("[G]")
        assertTrue((result as BracketExpr).inner is SevenSegmentPattern)
        val pat = (result.inner as SevenSegmentPattern)
        assertTrue(pat.g)
        assertRoundTrip("[G]")
    }

    // Test 3: Multiple segments (digit 7 pattern: A,B,C)
    @Test
    fun testMultiSegmentPattern() {
        val result = parse("[ABC]")
        assertTrue((result as BracketExpr).inner is SevenSegmentPattern)
        val pat = result.inner as SevenSegmentPattern
        assertTrue(pat.a && pat.b && pat.c)
        assertFalse(pat.d && pat.e && pat.f && pat.g)
        assertRoundTrip("[ABC]")
    }

    // Test 4: All segments lit (digit 8 pattern)
    @Test
    fun testAllSegments() {
        val result = parse("[ABCDEFG]")
        val pat = (result as BracketExpr).inner as SevenSegmentPattern
        assertTrue(pat.a && pat.b && pat.c && pat.d && pat.e && pat.f && pat.g)
        assertRoundTrip("[ABCDEFG]")
    }

    // Test 5: Case insensitive parsing
    @Test
    fun testCaseInsensitive() {
        val result = parse("[abCfg]")
        val pat = (result as BracketExpr).inner as SevenSegmentPattern
        assertTrue(pat.a && pat.b && pat.c && pat.f && pat.g)
        // Note: toNotation outputs uppercase
    }

    // Test 6: Blank pattern
    @Test
    fun testBlankPattern() {
        val result = parse("[~]")
        val pat = (result as BracketExpr).inner as SevenSegmentPattern
        assertFalse(pat.a || pat.b || pat.c || pat.d || pat.e || pat.f || pat.g)
        assertRoundTrip("[~]")
    }

    // ==================== COMPOSITION MODES ====================

    // Test 7: OVERLAP composition (A/B = segments merge)
    @Test
    fun testOverlapComposition() {
        val result = parse("[A/B]")
        assertTrue((result as BracketExpr).inner is Overlap)
        val overlap = result.inner as Overlap
        assertEquals(2, overlap.patterns.size)
        assertRoundTrip("[A/B]")
    }

    // Test 8: TOUCH composition (A|B = adjacent grids)
    @Test
    fun testTouchComposition() {
        val result = parse("[A|B]")
        assertTrue((result as BracketExpr).inner is Touch)
        val touch = result.inner as Touch
        assertEquals(2, touch.patterns.size)
        assertRoundTrip("[A|B]")
    }

    // Test 9: SPACE composition (A-B = separated grids)
    @Test
    fun testSpaceComposition() {
        val result = parse("[A-B]")
        assertTrue((result as BracketExpr).inner is Space)
        val space = result.inner as Space
        assertEquals(2, space.patterns.size)
        assertRoundTrip("[A-B]")
    }

    // Test 10: Chained OVERLAP (A/B/C = all overlay same grid)
    @Test
    fun testChainedOverlap() {
        val result = parse("[A/B/C]")
        assertTrue((result as BracketExpr).inner is Overlap)
        val overlap = result.inner as Overlap
        assertEquals(3, overlap.patterns.size)
        assertRoundTrip("[A/B/C]")
    }

    // Test 11: Chained TOUCH (A|B|C|D = four adjacent grids)
    @Test
    fun testChainedTouch() {
        val result = parse("[A|B|C|D]")
        assertTrue((result as BracketExpr).inner is Touch)
        val touch = result.inner as Touch
        assertEquals(4, touch.patterns.size)
        assertRoundTrip("[A|B|C|D]")
    }

    // Test 12: Chained SPACE (A-B-C = three separated grids)
    @Test
    fun testChainedSpace() {
        val result = parse("[A-B-C]")
        assertTrue((result as BracketExpr).inner is Space)
        val space = result.inner as Space
        assertEquals(3, space.patterns.size)
        assertRoundTrip("[A-B-C]")
    }

    // ==================== OPERATOR PRECEDENCE ====================

    // Test 13: Precedence - / (overlap) has highest
    // A/B|C should be (A/B)|C, not A/(B|C)
    @Test
    fun testPrecedenceOverlapHighest() {
        val result = parse("[A/B|C]")
        // Should parse as Touch(Overlap(A,B), C)
        assertTrue((result as BracketExpr).inner is Touch)
        val touch = result.inner as Touch
        assertTrue(touch.patterns[0] is Overlap)
        assertTrue(touch.patterns[1] is SevenSegmentPattern)
        assertRoundTrip("[A/B|C]")
    }

    // Test 14: Precedence - | (touch) higher than - (space)
    // A|B-C should be (A|B)-C, not A|(B-C)
    @Test
    fun testPrecedenceTouchHigherThanSpace() {
        val result = parse("[A|B-C]")
        // Should parse as Space(Touch(A,B), C)
        assertTrue((result as BracketExpr).inner is Space)
        val space = result.inner as Space
        assertTrue(space.patterns[0] is Touch)
        assertTrue(space.patterns[1] is SevenSegmentPattern)
        assertRoundTrip("[A|B-C]")
    }

    // Test 15: Full precedence chain: A/B|C-D
    // Should parse as Space(Touch(Overlap(A,B), C), D)
    @Test
    fun testFullPrecedenceChain() {
        val result = parse("[A/B|C-D]")
        assertTrue((result as BracketExpr).inner is Space)
        val space = result.inner as Space
        assertEquals(2, space.patterns.size)

        // First element should be Touch
        assertTrue(space.patterns[0] is Touch)
        val touch = space.patterns[0] as Touch

        // Touch's first element should be Overlap
        assertTrue(touch.patterns[0] is Overlap)
        assertRoundTrip("[A/B|C-D]")
    }

    // ==================== GROUPING ====================

    // Test 16: Grouping overrides precedence
    // (A|B)/C = Touch(A,B) overlapped with C
    @Test
    fun testGroupingOverridesPrecedence() {
        val result = parse("[(A|B)/C]")
        assertTrue((result as BracketExpr).inner is Overlap)
        val overlap = result.inner as Overlap
        // First element should be a Group containing Touch
        assertTrue(overlap.patterns[0] is Group)
        val group = overlap.patterns[0] as Group
        assertTrue(group.inner is Touch)
        assertRoundTrip("[(A|B)/C]")
    }

    // Test 17: Nested groups
    @Test
    fun testNestedGroups() {
        val result = parse("[((A|B)|C)]")
        assertTrue((result as BracketExpr).inner is Group)
        val group = (result.inner as Group)
        assertTrue(group.inner is Touch)
        assertRoundTrip("[((A|B)|C)]")
    }

    // ==================== CHARACTER REFERENCES ====================

    // Test 18: Character reference (digit)
    @Test
    fun testCharRefDigit() {
        val result = parse("[8]")
        val charRef = (result as BracketExpr).inner as CharRef
        assertEquals('8', charRef.char)
        assertRoundTrip("[8]")
    }

    // Test 19: Character reference (letter)
    @Test
    fun testCharRefLetter() {
        val result = parse("[A]")
        val charRef = (result as BracketExpr).inner as CharRef
        assertEquals('A', charRef.char)
        assertRoundTrip("[A]")
    }

    // Test 20: Mixed patterns and char refs
    @Test
    fun testMixedPatternsAndCharRefs() {
        val result = parse("[A|8|BC]")
        assertTrue((result as BracketExpr).inner is Touch)
        val touch = result.inner as Touch
        assertEquals(3, touch.patterns.size)
        assertTrue(touch.patterns[0] is CharRef)
        assertTrue(touch.patterns[1] is CharRef)
        assertTrue(touch.patterns[2] is SevenSegmentPattern)
    }

    // ==================== REAL 7-SEGMENT EXAMPLES ====================

    // Test 21: Display "HI" touching
    @Test
    fun testHiTouching() {
        // H uses C,E,F,G; I uses B,C (as digit 1)
        // [H|I] or using patterns: [CEFG|BC]
        val result = parse("[CEFG|BC]")
        assertTrue((result as BracketExpr).inner is Touch)
        assertRoundTrip("[CEFG|BC]")
    }

    // Test 22: Display "12" with space between
    @Test
    fun testDigitsWithSpace() {
        // 1 = BC, 2 = ABGED
        val result = parse("[BC-ABGED]")
        assertTrue((result as BracketExpr).inner is Space)
        val space = result.inner as Space
        assertEquals(2, space.patterns.size)
        assertRoundTrip("[BC-ABGED]")
    }

    // Test 23: Overlapping digits (unusual display effect)
    @Test
    fun testOverlappingDigits() {
        // 0 overlapped with 1
        // [ABCDEF/BC] = ABCDEF (1 adds nothing to 0)
        val result = parse("[ABCDEF/BC]")
        assertTrue((result as BracketExpr).inner is Overlap)
        assertRoundTrip("[ABCDEF/BC]")
    }

    // Test 24: Complex word "HELLO"
    @Test
    fun testHelloWord() {
        // H=CEFG, E=AFEDG, L=FED, L=FED, O=ABCDEF
        // All touching: H|E|L|L|O
        val result = parse("[CEFG|AFEDG|FED|FED|ABCDEF]")
        assertTrue((result as BracketExpr).inner is Touch)
        val touch = result.inner as Touch
        assertEquals(5, touch.patterns.size)
        assertRoundTrip("[CEFG|AFEDG|FED|FED|ABCDEF]")
    }

    // Test 25: Complex nested composition
    @Test
    fun testComplexNested() {
        // (A|B)/C-(D|E)|F
        // Parse: Space( Overlap(Group(Touch(A,B)), C), Touch(Group(Space(D,E)), F) )
        val result = parse("[(A|B)/C-(D|E)|F]")
        assertTrue((result as BracketExpr).inner is Space)
        assertRoundTrip("[(A|B)/C-(D|E)|F]")
    }

    // ==================== ERROR HANDLING ====================

    // Test 26: Error - invalid segment
    @Test(expected = ParseException::class)
    fun testInvalidSegment() {
        parse("[X]")
    }

    // Test 27: Error - unclosed bracket
    @Test(expected = ParseException::class)
    fun testUnclosedBracket() {
        parse("[ABC")
    }

    // Test 28: Error - unclosed paren
    @Test(expected = ParseException::class)
    fun testUnclosedParen() {
        parse("[(ABC]")
    }

    // Test 29: Error - empty brackets
    @Test(expected = ParseException::class)
    fun testEmptyBrackets() {
        parse("[]")
    }

    // Test 30: Whitespace tolerance
    @Test
    fun testWhitespaceTolerance() {
        val result = parse("[ A | B - C ]")
        val expected = GlyfParser.parse("[A|B-C]")
        assertEquals(expected.toNotation(), result.toNotation())
    }

    // Test 31: SevenSegmentPattern overlay operation
    @Test
    fun testPatternOverlay() {
        val pat1 = SevenSegmentPattern("ABC")    // top and right side
        val pat2 = SevenSegmentPattern("DEF")    // bottom and left side
        val overlaid = pat1.overlay(pat2)

        assertTrue(overlaid.a && overlaid.b && overlaid.c)
        assertTrue(overlaid.d && overlaid.e && overlaid.f)
        assertFalse(overlaid.g)
    }

    // Test 32: SevenSegmentChars predefined patterns
    @Test
    fun testPredefinedDigits() {
        // Verify digit 8 has all segments
        val eight = SevenSegmentChars.DIGITS['8']
        assertNotNull(eight)
        assertTrue(eight!!.a && eight.b && eight.c && eight.d && eight.e && eight.f && eight.g)

        // Verify digit 1 uses B and C
        val one = SevenSegmentChars.DIGITS['1']
        assertNotNull(one)
        assertTrue(one!!.b && one.c)
        assertFalse(one.a && one.d && one.e && one.f && one.g)
    }
}

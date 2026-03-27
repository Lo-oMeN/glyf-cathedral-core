package glyf.core.renderer

import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.DrawScope
import glyf.core.parser.SevenSegmentPattern
import glyf.core.parser.CompositionMode
import kotlin.math.pow

/**
 * Golden Ratio constants for 7-segment proportions
 */
object PhiGeometry {
    const val PHI = 1.618033988749895f
    const val PHI_INV = 0.6180339887498948f
    const val PHI_2 = 2.618033988749895f
    
    /**
     * Standard 7-segment aspect ratio: width/height
     * Golden ratio derived for aesthetic proportions
     */
    const val ASPECT_RATIO = 0.6f
    
    /**
     * Segment thickness as ratio of cell height
     */
    const val SEGMENT_THICKNESS_RATIO = 0.12f
    
    /**
     * Gap between segment ends for mitred corners
     */
    const val SEGMENT_GAP_RATIO = 0.015f
}

/**
 * The seven segments of a digital display.
 * Named by position: A(top), B(upper-right), C(lower-right), 
 * D(bottom), E(lower-left), F(upper-left), G(middle)
 */
enum class Segment {
    A, B, C, D, E, F, G
}

/**
 * Extended 7-segment pattern with label for renderer use.
 * Wraps the parser's SevenSegmentPattern with rendering utilities.
 */
data class DisplayPattern(
    val a: Boolean = false,
    val b: Boolean = false,
    val c: Boolean = false,
    val d: Boolean = false,
    val e: Boolean = false,
    val f: Boolean = false,
    val g: Boolean = false,
    val label: String = ""
) {
    /**
     * Get segments as a set
     */
    fun toSegmentSet(): Set<Segment> = buildSet {
        if (a) add(Segment.A)
        if (b) add(Segment.B)
        if (c) add(Segment.C)
        if (d) add(Segment.D)
        if (e) add(Segment.E)
        if (f) add(Segment.F)
        if (g) add(Segment.G)
    }
    
    /**
     * Overlay another pattern (OR operation)
     */
    infix fun overlay(other: DisplayPattern): DisplayPattern = DisplayPattern(
        a = this.a || other.a,
        b = this.b || other.b,
        c = this.c || other.c,
        d = this.d || other.d,
        e = this.e || other.e,
        f = this.f || other.f,
        g = this.g || other.g,
        label = "${this.label}|${other.label}"
    )
    
    companion object {
        /**
         * Convert parser pattern to display pattern
         */
        fun fromParser(pattern: SevenSegmentPattern, label: String = ""): DisplayPattern =
            DisplayPattern(
                a = pattern.a,
                b = pattern.b,
                c = pattern.c,
                d = pattern.d,
                e = pattern.e,
                f = pattern.f,
                g = pattern.g,
                label = label
            )
        
        // Predefined patterns
        val BLANK = DisplayPattern(label = " ")
        val FULL = DisplayPattern(a=true, b=true, c=true, d=true, e=true, f=true, g=true, label="8")
        val TOP = DisplayPattern(a=true, label="‾")
        val BOTTOM = DisplayPattern(d=true, label="_")
        val LEFT = DisplayPattern(f=true, e=true, label="[")
        val RIGHT = DisplayPattern(b=true, c=true, label="]")
        val CENTER = DisplayPattern(g=true, label="-")
        
        // Digit patterns
        val DIGIT_0 = DisplayPattern(a=true, b=true, c=true, d=true, e=true, f=true, label="0")
        val DIGIT_1 = DisplayPattern(b=true, c=true, label="1")
        val DIGIT_2 = DisplayPattern(a=true, b=true, d=true, e=true, g=true, label="2")
        val DIGIT_3 = DisplayPattern(a=true, b=true, c=true, d=true, g=true, label="3")
        val DIGIT_4 = DisplayPattern(b=true, c=true, f=true, g=true, label="4")
        val DIGIT_5 = DisplayPattern(a=true, c=true, d=true, f=true, g=true, label="5")
        val DIGIT_6 = DisplayPattern(a=true, c=true, d=true, e=true, f=true, g=true, label="6")
        val DIGIT_7 = DisplayPattern(a=true, b=true, c=true, label="7")
        val DIGIT_8 = FULL
        val DIGIT_9 = DisplayPattern(a=true, b=true, c=true, d=true, f=true, g=true, label="9")
        
        // Letter patterns
        val LETTER_A = DisplayPattern(a=true, b=true, c=true, e=true, f=true, g=true, label="A")
        val LETTER_B = DisplayPattern(c=true, d=true, e=true, f=true, g=true, label="b")
        val LETTER_C = DisplayPattern(a=true, d=true, e=true, f=true, label="C")
        val LETTER_D = DisplayPattern(b=true, c=true, d=true, e=true, g=true, label="d")
        val LETTER_E = DisplayPattern(a=true, d=true, e=true, f=true, g=true, label="E")
        val LETTER_F = DisplayPattern(a=true, e=true, f=true, g=true, label="F")
        val LETTER_G = DisplayPattern(a=true, c=true, d=true, e=true, f=true, label="G")
        val LETTER_H = DisplayPattern(b=true, c=true, e=true, f=true, g=true, label="H")
        val LETTER_I = DisplayPattern(b=true, c=true, label="I")
        val LETTER_J = DisplayPattern(b=true, c=true, d=true, label="J")
        val LETTER_L = DisplayPattern(d=true, e=true, f=true, label="L")
        val LETTER_O = DIGIT_0.copy(label="O")
        val LETTER_P = DisplayPattern(a=true, b=true, e=true, f=true, g=true, label="P")
        val LETTER_S = DIGIT_5.copy(label="S")
        val LETTER_U = DisplayPattern(b=true, c=true, d=true, e=true, f=true, label="U")
        val LETTER_Y = DisplayPattern(b=true, c=true, d=true, f=true, g=true, label="Y")
        
        /**
         * Get pattern for a character
         */
        fun forChar(char: Char): DisplayPattern = when (char.uppercaseChar()) {
            '0' -> DIGIT_0
            '1' -> DIGIT_1
            '2' -> DIGIT_2
            '3' -> DIGIT_3
            '4' -> DIGIT_4
            '5' -> DIGIT_5
            '6' -> DIGIT_6
            '7' -> DIGIT_7
            '8' -> DIGIT_8
            '9' -> DIGIT_9
            'A' -> LETTER_A
            'B' -> LETTER_B
            'C' -> LETTER_C
            'D' -> LETTER_D
            'E' -> LETTER_E
            'F' -> LETTER_F
            'G' -> LETTER_G
            'H' -> LETTER_H
            'I' -> LETTER_I
            'J' -> LETTER_J
            'L' -> LETTER_L
            'O' -> LETTER_O
            'P' -> LETTER_P
            'S' -> LETTER_S
            'U' -> LETTER_U
            'Y' -> LETTER_Y
            ' ' -> BLANK
            '-' -> CENTER
            '_' -> BOTTOM
            else -> BLANK
        }
    }
}

/**
 * Renders a 7-segment display cell with golden ratio proportions
 */
class SevenSegmentRenderer(
    val onColor: Color = Color(0xFFD4AF37),      // Golden illuminated
    val offColor: Color = Color(0xFF1A1A2E),      // Dark unlit
    val glowColor: Color = Color(0xFFFFD700),     // Glow effect
    val strokeWidth: Float = 6f,
    val drawGlow: Boolean = true
) {
    /**
     * Calculate cell dimensions from height
     */
    fun cellDimensionsFromHeight(height: Float): Pair<Float, Float> {
        val width = height * PhiGeometry.ASPECT_RATIO * PhiGeometry.PHI
        return Pair(width, height)
    }
    
    /**
     * Draw a complete 7-segment cell
     */
    fun DrawScope.drawCell(
        pattern: DisplayPattern,
        center: Offset,
        width: Float,
        height: Float
    ) {
        val thickness = height * PhiGeometry.SEGMENT_THICKNESS_RATIO
        val halfW = width / 2
        val halfH = height / 2
        val gap = height * PhiGeometry.SEGMENT_GAP_RATIO
        val halfT = thickness / 2
        
        // Calculate segment endpoints
        // Top (A): horizontal at top
        val aStart = Offset(center.x - halfW + gap + halfT, center.y - halfH)
        val aEnd = Offset(center.x + halfW - gap - halfT, center.y - halfH)
        
        // Upper right (B): vertical right side, upper half
        val bStart = Offset(center.x + halfW, center.y - halfH + gap + halfT)
        val bEnd = Offset(center.x + halfW, center.y - gap - halfT)
        
        // Lower right (C): vertical right side, lower half
        val cStart = Offset(center.x + halfW, center.y + gap + halfT)
        val cEnd = Offset(center.x + halfW, center.y + halfH - gap - halfT)
        
        // Bottom (D): horizontal at bottom
        val dStart = Offset(center.x - halfW + gap + halfT, center.y + halfH)
        val dEnd = Offset(center.x + halfW - gap - halfT, center.y + halfH)
        
        // Lower left (E): vertical left side, lower half
        val eStart = Offset(center.x - halfW, center.y + halfH - gap - halfT)
        val eEnd = Offset(center.x - halfW, center.y + gap + halfT)
        
        // Upper left (F): vertical left side, upper half
        val fStart = Offset(center.x - halfW, center.y - gap - halfT)
        val fEnd = Offset(center.x - halfW, center.y - halfH + gap + halfT)
        
        // Middle (G): horizontal at center
        val gStart = Offset(center.x - halfW + gap + halfT, center.y)
        val gEnd = Offset(center.x + halfW - gap - halfT, center.y)
        
        // Draw segments
        if (pattern.a) drawSegment(aStart, aEnd, thickness, true)
        if (pattern.b) drawSegment(bStart, bEnd, thickness, false)
        if (pattern.c) drawSegment(cStart, cEnd, thickness, false)
        if (pattern.d) drawSegment(dStart, dEnd, thickness, true)
        if (pattern.e) drawSegment(eStart, eEnd, thickness, false)
        if (pattern.f) drawSegment(fStart, fEnd, thickness, false)
        if (pattern.g) drawSegment(gStart, gEnd, thickness, true)
        
        // Draw off segments subtly (optional - for ghost effect)
        if (pattern.a == false) drawSegmentGhost(aStart, aEnd, thickness, true)
        if (pattern.b == false) drawSegmentGhost(bStart, bEnd, thickness, false)
        if (pattern.c == false) drawSegmentGhost(cStart, cEnd, thickness, false)
        if (pattern.d == false) drawSegmentGhost(dStart, dEnd, thickness, true)
        if (pattern.e == false) drawSegmentGhost(eStart, eEnd, thickness, false)
        if (pattern.f == false) drawSegmentGhost(fStart, fEnd, thickness, false)
        if (pattern.g == false) drawSegmentGhost(gStart, gEnd, thickness, true)
    }
    
    /**
     * Draw an illuminated segment with hexagonal lozenge shape
     */
    private fun DrawScope.drawSegment(
        start: Offset,
        end: Offset,
        thickness: Float,
        isHorizontal: Boolean
    ) {
        val path = createSegmentPath(start, end, thickness, isHorizontal)
        
        // Draw glow
        if (drawGlow) {
            drawPath(
                path = path,
                color = glowColor.copy(alpha = 0.3f),
                alpha = 0.5f
            )
        }
        
        // Draw main segment
        drawPath(path = path, color = onColor)
        
        // Draw highlight
        val highlightPath = createHighlightPath(start, end, thickness, isHorizontal)
        drawPath(
            path = highlightPath,
            color = Color.White.copy(alpha = 0.4f)
        )
    }
    
    /**
     * Draw a ghost/unlit segment
     */
    private fun DrawScope.drawSegmentGhost(
        start: Offset,
        end: Offset,
        thickness: Float,
        isHorizontal: Boolean
    ) {
        val path = createSegmentPath(start, end, thickness * 0.5f, isHorizontal)
        drawPath(
            path = path,
            color = offColor.copy(alpha = 0.3f)
        )
    }
    
    /**
     * Create hexagonal path for segment
     */
    private fun createSegmentPath(
        start: Offset,
        end: Offset,
        thickness: Float,
        isHorizontal: Boolean
    ): Path {
        val path = Path()
        val halfT = thickness / 2
        val taper = thickness * 0.25f
        
        if (isHorizontal) {
            // Horizontal segment: A, D, G
            path.moveTo(start.x + taper, start.y - halfT)
            path.lineTo(end.x - taper, end.y - halfT)
            path.lineTo(end.x, end.y)
            path.lineTo(end.x - taper, end.y + halfT)
            path.lineTo(start.x + taper, start.y + halfT)
            path.lineTo(start.x, start.y)
            path.close()
        } else {
            // Vertical segment: B, C, E, F
            path.moveTo(start.x - halfT, start.y + taper)
            path.lineTo(start.x + halfT, start.y + taper)
            path.lineTo(end.x + halfT, end.y - taper)
            path.lineTo(end.x, end.y)
            path.lineTo(end.x - halfT, end.y - taper)
            path.lineTo(start.x - halfT, start.y)
            path.close()
        }
        
        return path
    }
    
    /**
     * Create highlight path for segment
     */
    private fun createHighlightPath(
        start: Offset,
        end: Offset,
        thickness: Float,
        isHorizontal: Boolean
    ): Path {
        val path = Path()
        val highlightT = thickness * 0.2f
        
        if (isHorizontal) {
            path.moveTo(start.x + thickness * 0.3f, start.y - highlightT)
            path.lineTo(end.x - thickness * 0.3f, end.y - highlightT)
            path.lineTo(end.x - thickness * 0.2f, end.y)
            path.lineTo(start.x + thickness * 0.2f, start.y)
        } else {
            path.moveTo(start.x - highlightT, start.y + thickness * 0.3f)
            path.lineTo(start.x - highlightT + highlightT * 0.5f, start.y + thickness * 0.3f)
            path.lineTo(end.x - highlightT + highlightT * 0.5f, end.y - thickness * 0.3f)
            path.lineTo(end.x - highlightT, end.y - thickness * 0.3f)
        }
        
        return path
    }
}

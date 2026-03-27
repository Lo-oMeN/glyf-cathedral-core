package glyf.core.renderer

import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.DrawScope
import glyf.core.parser.GlyfNode
import glyf.core.parser.SevenSegmentPattern
import glyf.core.parser.Overlap
import glyf.core.parser.Touch
import glyf.core.parser.Space
import glyf.core.parser.BracketExpr
import glyf.core.parser.Group
import glyf.core.parser.CharRef
import glyf.core.parser.SevenSegmentChars
import glyf.core.parser.CompositionMode

/**
 * Word renderer that handles composition of multiple 7-segment glyphs
 */
class WordRenderer(
    private val segmentRenderer: SevenSegmentRenderer = SevenSegmentRenderer(),
    private val compositionMode: CompositionMode = CompositionMode.TOUCH
) {
    /**
     * Result of rendering
     */
    data class RenderResult(
        val totalWidth: Float,
        val totalHeight: Float,
        val cellCount: Int
    )
    
    /**
     * Render a word (string of characters) using 7-segment display
     */
    fun DrawScope.renderWord(
        word: String,
        center: Offset,
        cellHeight: Float
    ): RenderResult {
        val patterns = word.map { DisplayPattern.forChar(it) }
        return renderPatterns(patterns, center, cellHeight)
    }
    
    /**
     * Render a list of patterns
     */
    fun DrawScope.renderPatterns(
        patterns: List<DisplayPattern>,
        center: Offset,
        cellHeight: Float
    ): RenderResult {
        if (patterns.isEmpty()) {
            return RenderResult(0f, 0f, 0)
        }
        
        return when (compositionMode) {
            CompositionMode.OVERLAP -> renderOverlapping(patterns, center, cellHeight)
            CompositionMode.TOUCH -> renderTouching(patterns, center, cellHeight)
            CompositionMode.SPACE -> renderSpaced(patterns, center, cellHeight)
        }
    }
    
    /**
     * OVERLAP mode: All letters share the same grid, segments blend (OR)
     */
    private fun DrawScope.renderOverlapping(
        patterns: List<DisplayPattern>,
        center: Offset,
        cellHeight: Float
    ): RenderResult {
        // Merge all patterns
        val mergedPattern = patterns.reduce { acc, pattern -> acc overlay pattern }
        
        val (cellWidth, _) = segmentRenderer.cellDimensionsFromHeight(cellHeight)
        
        segmentRenderer.run {
            drawCell(
                pattern = mergedPattern,
                center = center,
                width = cellWidth,
                height = cellHeight
            )
        }
        
        return RenderResult(cellWidth, cellHeight, patterns.size)
    }
    
    /**
     * TOUCH mode: Letter grids are adjacent, sharing edges
     */
    private fun DrawScope.renderTouching(
        patterns: List<DisplayPattern>,
        center: Offset,
        cellHeight: Float
    ): RenderResult {
        val (cellWidth, _) = segmentRenderer.cellDimensionsFromHeight(cellHeight)
        val totalWidth = cellWidth * patterns.size
        val startX = center.x - totalWidth / 2 + cellWidth / 2
        
        patterns.forEachIndexed { index, pattern ->
            val cellCenter = Offset(startX + index * cellWidth, center.y)
            segmentRenderer.run {
                drawCell(
                    pattern = pattern,
                    center = cellCenter,
                    width = cellWidth,
                    height = cellHeight
                )
            }
        }
        
        return RenderResult(totalWidth, cellHeight, patterns.size)
    }
    
    /**
     * SPACE mode: Letter grids are separated by φ-based spacing
     */
    private fun DrawScope.renderSpaced(
        patterns: List<DisplayPattern>,
        center: Offset,
        cellHeight: Float
    ): RenderResult {
        val (cellWidth, _) = segmentRenderer.cellDimensionsFromHeight(cellHeight)
        val spacing = cellWidth * PhiGeometry.PHI_INV * 0.4f
        val totalWidth = cellWidth * patterns.size + spacing * (patterns.size - 1)
        val startX = center.x - totalWidth / 2 + cellWidth / 2
        
        patterns.forEachIndexed { index, pattern ->
            val cellCenter = Offset(startX + index * (cellWidth + spacing), center.y)
            segmentRenderer.run {
                drawCell(
                    pattern = pattern,
                    center = cellCenter,
                    width = cellWidth,
                    height = cellHeight
                )
            }
        }
        
        return RenderResult(totalWidth, cellHeight, patterns.size)
    }
}

/**
 * Unified GLYF 7-Segment Renderer
 * 
 * Renders GLYF AST expressions to 7-segment display patterns.
 */
class GlyfSevenSegmentRenderer(
    val onColor: Color = Color(0xFFD4AF37),
    val offColor: Color = Color(0xFF1A1A2E),
    val glowColor: Color = Color(0xFFFFD700),
    val drawGlow: Boolean = true
) {
    private val segmentRenderer = SevenSegmentRenderer(
        onColor = onColor,
        offColor = offColor,
        glowColor = glowColor,
        drawGlow = drawGlow
    )
    
    /**
     * Render a GlyfNode AST to 7-segment display
     */
    fun DrawScope.render(
        node: GlyfNode,
        center: Offset,
        cellHeight: Float
    ): RenderResult {
        return when (node) {
            is SevenSegmentPattern -> renderPattern(node, center, cellHeight)
            is Overlap -> renderOverlap(node, center, cellHeight)
            is Touch -> renderTouch(node, center, cellHeight)
            is Space -> renderSpace(node, center, cellHeight)
            is BracketExpr -> renderBracket(node, center, cellHeight)
            is Group -> renderGroup(node, center, cellHeight)
            is CharRef -> renderCharRef(node, center, cellHeight)
            else -> RenderResult(0f, 0f, 0)
        }
    }
    
    /**
     * Render a word string directly
     */
    fun DrawScope.renderWord(
        word: String,
        center: Offset,
        cellHeight: Float,
        mode: CompositionMode = CompositionMode.TOUCH
    ): WordRenderer.RenderResult {
        val wordRenderer = WordRenderer(segmentRenderer, mode)
        return wordRenderer.run {
            renderWord(word, center, cellHeight)
        }
    }
    
    /**
     * Render a single SevenSegmentPattern
     */
    private fun DrawScope.renderPattern(
        pattern: SevenSegmentPattern,
        center: Offset,
        cellHeight: Float
    ): RenderResult {
        val displayPattern = DisplayPattern.fromParser(pattern)
        val (cellWidth, _) = segmentRenderer.cellDimensionsFromHeight(cellHeight)
        
        segmentRenderer.run {
            drawCell(
                pattern = displayPattern,
                center = center,
                width = cellWidth,
                height = cellHeight
            )
        }
        
        return RenderResult(cellWidth, cellHeight, 1)
    }
    
    /**
     * Render Overlap composition (A/B)
     */
    private fun DrawScope.renderOverlap(
        node: Overlap,
        center: Offset,
        cellHeight: Float
    ): RenderResult {
        val patterns = node.patterns.flatMap { extractPatterns(it) }
        
        val wordRenderer = WordRenderer(segmentRenderer, CompositionMode.OVERLAP)
        return wordRenderer.run {
            renderPatterns(patterns.map { DisplayPattern.fromParser(it) }, center, cellHeight)
        }.let { WordRenderer.RenderResult(it.totalWidth, it.totalHeight, it.cellCount) }
    }
    
    /**
     * Render Touch composition (A|B)
     */
    private fun DrawScope.renderTouch(
        node: Touch,
        center: Offset,
        cellHeight: Float
    ): RenderResult {
        val patterns = node.patterns.flatMap { extractPatterns(it) }
        
        val wordRenderer = WordRenderer(segmentRenderer, CompositionMode.TOUCH)
        return wordRenderer.run {
            renderPatterns(patterns.map { DisplayPattern.fromParser(it) }, center, cellHeight)
        }.let { WordRenderer.RenderResult(it.totalWidth, it.totalHeight, it.cellCount) }
    }
    
    /**
     * Render Space composition (A-B)
     */
    private fun DrawScope.renderSpace(
        node: Space,
        center: Offset,
        cellHeight: Float
    ): RenderResult {
        val patterns = node.patterns.flatMap { extractPatterns(it) }
        
        val wordRenderer = WordRenderer(segmentRenderer, CompositionMode.SPACE)
        return wordRenderer.run {
            renderPatterns(patterns.map { DisplayPattern.fromParser(it) }, center, cellHeight)
        }.let { WordRenderer.RenderResult(it.totalWidth, it.totalHeight, it.cellCount) }
    }
    
    /**
     * Render BracketExpr with decorative frame
     */
    private fun DrawScope.renderBracket(
        node: BracketExpr,
        center: Offset,
        cellHeight: Float
    ): RenderResult {
        val result = render(node.inner, center, cellHeight)
        drawBracketFrame(center, result.totalWidth, cellHeight)
        return result.copy(totalWidth = result.totalWidth + cellHeight * 0.4f)
    }
    
    /**
     * Render Group with containment brackets
     */
    private fun DrawScope.renderGroup(
        node: Group,
        center: Offset,
        cellHeight: Float
    ): RenderResult {
        val result = render(node.inner, center, cellHeight)
        drawContainmentFrame(center, result.totalWidth, cellHeight)
        return result.copy(totalWidth = result.totalWidth + cellHeight * 0.3f)
    }
    
    /**
     * Render CharRef
     */
    private fun DrawScope.renderCharRef(
        node: CharRef,
        center: Offset,
        cellHeight: Float
    ): RenderResult {
        val pattern = SevenSegmentChars.DIGITS[node.char]
            ?: SevenSegmentChars.LETTERS[node.char.uppercaseChar()]
            ?: SevenSegmentPattern()
        
        return renderPattern(pattern, center, cellHeight)
    }
    
    /**
     * Extract patterns from any GlyfNode
     */
    private fun extractPatterns(node: GlyfNode): List<SevenSegmentPattern> {
        return when (node) {
            is SevenSegmentPattern -> listOf(node)
            is CharRef -> listOf(
                SevenSegmentChars.DIGITS[node.char]
                    ?: SevenSegmentChars.LETTERS[node.char.uppercaseChar()]
                    ?: SevenSegmentPattern()
            )
            is Overlap -> {
                val patterns = node.patterns.flatMap { extractPatterns(it) }
                if (patterns.isEmpty()) emptyList()
                else listOf(patterns.reduce { acc, p -> acc.overlay(p) })
            }
            is Touch -> node.patterns.flatMap { extractPatterns(it) }
            is Space -> node.patterns.flatMap { extractPatterns(it) }
            is BracketExpr -> extractPatterns(node.inner)
            is Group -> extractPatterns(node.inner)
            else -> emptyList()
        }
    }
    
    /**
     * Draw bracket frame (square brackets style)
     */
    private fun DrawScope.drawBracketFrame(
        center: Offset,
        width: Float,
        height: Float
    ) {
        val frameColor = onColor.copy(alpha = 0.6f)
        val padding = height * 0.1f
        val bracketWidth = height * 0.08f
        
        val left = center.x - width / 2 - padding
        val right = center.x + width / 2 + padding
        val top = center.y - height / 2 - padding
        val bottom = center.y + height / 2 + padding
        
        // Corner brackets
        // Top-left
        drawLine(frameColor, Offset(left, top + bracketWidth), Offset(left, top), 2f)
        drawLine(frameColor, Offset(left, top), Offset(left + bracketWidth, top), 2f)
        
        // Top-right
        drawLine(frameColor, Offset(right - bracketWidth, top), Offset(right, top), 2f)
        drawLine(frameColor, Offset(right, top), Offset(right, top + bracketWidth), 2f)
        
        // Bottom-left
        drawLine(frameColor, Offset(left, bottom - bracketWidth), Offset(left, bottom), 2f)
        drawLine(frameColor, Offset(left, bottom), Offset(left + bracketWidth, bottom), 2f)
        
        // Bottom-right
        drawLine(frameColor, Offset(right - bracketWidth, bottom), Offset(right, bottom), 2f)
        drawLine(frameColor, Offset(right, bottom), Offset(right, bottom - bracketWidth), 2f)
    }
    
    /**
     * Draw containment frame (parentheses style)
     */
    private fun DrawScope.drawContainmentFrame(
        center: Offset,
        width: Float,
        height: Float
    ) {
        val frameColor = onColor.copy(alpha = 0.5f)
        val bracketWidth = height * 0.15f
        val bracketHeight = height * 0.6f
        
        // Left bracket
        drawLine(
            frameColor,
            Offset(center.x - width / 2 - bracketWidth * 2, center.y - bracketHeight / 2),
            Offset(center.x - width / 2 - bracketWidth, center.y - bracketHeight / 2),
            2f
        )
        drawLine(
            frameColor,
            Offset(center.x - width / 2 - bracketWidth * 2, center.y - bracketHeight / 2),
            Offset(center.x - width / 2 - bracketWidth * 2, center.y + bracketHeight / 2),
            2f
        )
        drawLine(
            frameColor,
            Offset(center.x - width / 2 - bracketWidth * 2, center.y + bracketHeight / 2),
            Offset(center.x - width / 2 - bracketWidth, center.y + bracketHeight / 2),
            2f
        )
        
        // Right bracket
        drawLine(
            frameColor,
            Offset(center.x + width / 2 + bracketWidth * 2, center.y - bracketHeight / 2),
            Offset(center.x + width / 2 + bracketWidth, center.y - bracketHeight / 2),
            2f
        )
        drawLine(
            frameColor,
            Offset(center.x + width / 2 + bracketWidth * 2, center.y - bracketHeight / 2),
            Offset(center.x + width / 2 + bracketWidth * 2, center.y + bracketHeight / 2),
            2f
        )
        drawLine(
            frameColor,
            Offset(center.x + width / 2 + bracketWidth * 2, center.y + bracketHeight / 2),
            Offset(center.x + width / 2 + bracketWidth, center.y + bracketHeight / 2),
            2f
        )
    }
    
    /**
     * Render result
     */
    data class RenderResult(
        val totalWidth: Float,
        val totalHeight: Float,
        val cellCount: Int
    )
}

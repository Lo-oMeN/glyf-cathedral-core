package glyf.core.renderer

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.horizontalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import glyf.core.parser.SevenSegmentPattern
import glyf.core.parser.Overlap
import glyf.core.parser.Touch
import glyf.core.parser.Space
import glyf.core.parser.BracketExpr
import glyf.core.parser.Group
import glyf.core.parser.CharRef
import glyf.core.parser.CompositionMode

/**
 * Complete GLYF 7-Segment Preview
 * 
 * Demonstrates the full renderer capabilities:
 * - Individual 7-segment patterns
 * - Composition operators (Overlap, Touch, Space, [], ())
 * - Multiple letters/words
 * - Color variations
 */
@Composable
fun GlyfRendererPreview(
    modifier: Modifier = Modifier,
    backgroundColor: Color = Color(0xFF0A0A14),
    onColor: Color = Color(0xFFD4AF37)
) {
    val renderer = GlyfSevenSegmentRenderer(
        onColor = onColor,
        offColor = Color(0xFF1A1A2E),
        drawGlow = true
    )
    
    Column(
        modifier = modifier
            .fillMaxSize()
            .background(backgroundColor)
            .padding(16.dp)
            .verticalScroll(rememberScrollState())
    ) {
        // Header
        HeaderSection(onColor)
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // Section 1: The 7 Segments
        Section1_Segments(renderer, onColor)
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // Section 2: Digits 0-9
        Section2_Digits(renderer, onColor)
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // Section 3: Letters
        Section3_Letters(renderer, onColor)
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // Section 4: Composition Modes
        Section4_Composition(renderer, onColor)
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // Section 5: AST Expressions
        Section5_AST(renderer, onColor)
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // Section 6: Word Examples
        Section6_Words(renderer, onColor)
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // Section 7: Color Variations
        Section7_Colors()
        
        Spacer(modifier = Modifier.height(24.dp))
        
        // Footer
        Text(
            text = "GLYF 7-Segment Renderer v1.0 — φ-proportioned",
            style = MaterialTheme.typography.bodySmall,
            color = onColor.copy(alpha = 0.4f),
            fontFamily = FontFamily.Monospace,
            modifier = Modifier.align(Alignment.CenterHorizontally)
        )
    }
}

@Composable
private fun HeaderSection(onColor: Color) {
    Column {
        Text(
            text = "GLYF RENDERER",
            style = MaterialTheme.typography.headlineLarge,
            color = onColor,
            fontWeight = FontWeight.Light,
            fontFamily = FontFamily.Monospace
        )
        
        Text(
            text = "7-Segment Display System",
            style = MaterialTheme.typography.titleMedium,
            color = onColor.copy(alpha = 0.8f),
            fontFamily = FontFamily.Monospace
        )
        
        Text(
            text = "Canonical display grid with golden ratio proportions",
            style = MaterialTheme.typography.bodySmall,
            color = onColor.copy(alpha = 0.5f),
            fontFamily = FontFamily.Monospace
        )
    }
}

@Composable
private fun Section1_Segments(renderer: GlyfSevenSegmentRenderer, onColor: Color) {
    SectionTitle("1. The Seven Segments", onColor)
    
    Text(
        text = "A B C D E F G — canonical display elements",
        style = MaterialTheme.typography.bodySmall,
        color = onColor.copy(alpha = 0.6f),
        fontFamily = FontFamily.Monospace
    )
    
    Row(
        modifier = Modifier
            .horizontalScroll(rememberScrollState())
            .padding(vertical = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        val segments = listOf(
            "A (Top)" to DisplayPattern(a = true, label = "A"),
            "B (UR)" to DisplayPattern(b = true, label = "B"),
            "C (LR)" to DisplayPattern(c = true, label = "C"),
            "D (Bot)" to DisplayPattern(d = true, label = "D"),
            "E (LL)" to DisplayPattern(e = true, label = "E"),
            "F (UL)" to DisplayPattern(f = true, label = "F"),
            "G (Mid)" to DisplayPattern(g = true, label = "G")
        )
        
        segments.forEach { (label, pattern) ->
            PatternCard(label, pattern, renderer)
        }
    }
}

@Composable
private fun Section2_Digits(renderer: GlyfSevenSegmentRenderer, onColor: Color) {
    SectionTitle("2. Digits 0-9", onColor)
    
    Text(
        text = "Standard hexadecimal encoding",
        style = MaterialTheme.typography.bodySmall,
        color = onColor.copy(alpha = 0.6f),
        fontFamily = FontFamily.Monospace
    )
    
    Row(
        modifier = Modifier
            .horizontalScroll(rememberScrollState())
            .padding(vertical = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        val digits = listOf(
            DisplayPattern.DIGIT_0,
            DisplayPattern.DIGIT_1,
            DisplayPattern.DIGIT_2,
            DisplayPattern.DIGIT_3,
            DisplayPattern.DIGIT_4,
            DisplayPattern.DIGIT_5,
            DisplayPattern.DIGIT_6,
            DisplayPattern.DIGIT_7,
            DisplayPattern.DIGIT_8,
            DisplayPattern.DIGIT_9
        )
        
        digits.forEach { pattern ->
            PatternCard(pattern.label, pattern, renderer)
        }
    }
}

@Composable
private fun Section3_Letters(renderer: GlyfSevenSegmentRenderer, onColor: Color) {
    SectionTitle("3. Letters A-F", onColor)
    
    Text(
        text = "Extended hexadecimal alphabet",
        style = MaterialTheme.typography.bodySmall,
        color = onColor.copy(alpha = 0.6f),
        fontFamily = FontFamily.Monospace
    )
    
    Row(
        modifier = Modifier
            .horizontalScroll(rememberScrollState())
            .padding(vertical = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        val letters = listOf(
            DisplayPattern.LETTER_A,
            DisplayPattern.LETTER_B,
            DisplayPattern.LETTER_C,
            DisplayPattern.LETTER_D,
            DisplayPattern.LETTER_E,
            DisplayPattern.LETTER_F
        )
        
        letters.forEach { pattern ->
            PatternCard(pattern.label, pattern, renderer)
        }
    }
}

@Composable
private fun Section4_Composition(renderer: GlyfSevenSegmentRenderer, onColor: Color) {
    SectionTitle("4. Composition Modes", onColor)
    
    val modes = listOf(
        Triple(
            "OVERLAP (A/B)",
            "Letters share same grid, segments blend",
            Overlap(CharRef('A'), CharRef('B'))
        ),
        Triple(
            "TOUCH (A|B)",
            "Letters adjacent, grids share edges",
            Touch(CharRef('A'), CharRef('B'))
        ),
        Triple(
            "SPACE (A-B)",
            "Letters separated by φ-spacing",
            Space(CharRef('A'), CharRef('B'))
        )
    )
    
    modes.forEach { (name, desc, node) ->
        CompositionDemoCard(name, desc, node, renderer)
        Spacer(modifier = Modifier.height(12.dp))
    }
}

@Composable
private fun Section5_AST(renderer: GlyfSevenSegmentRenderer, onColor: Color) {
    SectionTitle("5. AST Expression Examples", onColor)
    
    val expressions = listOf(
        "[AB]" to BracketExpr(Touch(CharRef('A'), CharRef('B'))),
        "[A/B]" to BracketExpr(Overlap(CharRef('A'), CharRef('B'))),
        "(A|B)" to Group(Touch(CharRef('A'), CharRef('B'))),
        "[A|B|C]" to BracketExpr(Touch(CharRef('A'), CharRef('B'), CharRef('C'))),
        "[HELLO]" to BracketExpr(Touch(
            CharRef('H'), CharRef('E'), CharRef('L'), CharRef('L'), CharRef('O')
        ))
    )
    
    expressions.forEach { (notation, node) ->
        ExpressionRow(notation, node, renderer, onColor)
        Spacer(modifier = Modifier.height(8.dp))
    }
}

@Composable
private fun Section6_Words(renderer: GlyfSevenSegmentRenderer, onColor: Color) {
    SectionTitle("6. Word Examples", onColor)
    
    val words = listOf("GLYF", "TEST", "CAFE", "BEAD", "FACE", "DEAD", "CAFE")
    
    words.forEach { word ->
        WordRow(word, renderer, onColor)
        Spacer(modifier = Modifier.height(8.dp))
    }
}

@Composable
private fun Section7_Colors() {
    SectionTitle("7. Chromatic Variations", Color.White)
    
    val colors = listOf(
        "Amber" to Color(0xFFFFB000),
        "Matrix" to Color(0xFF39FF14),
        "Cyan" to Color(0xFF00FFFF),
        "Crimson" to Color(0xFFFF3131),
        "Violet" to Color(0xFF8B5CF6),
        "White" to Color(0xFFF0F0F0)
    )
    
    Row(
        modifier = Modifier
            .horizontalScroll(rememberScrollState())
            .padding(vertical = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        colors.forEach { (name, color) ->
            val colorRenderer = GlyfSevenSegmentRenderer(
                onColor = color,
                offColor = color.copy(alpha = 0.1f),
                drawGlow = true
            )
            ColorVariantCard(name, colorRenderer, color)
        }
    }
}

// UI Components

@Composable
private fun SectionTitle(title: String, color: Color) {
    Text(
        text = title,
        style = MaterialTheme.typography.titleMedium,
        color = color,
        fontWeight = FontWeight.Medium,
        fontFamily = FontFamily.Monospace,
        modifier = Modifier.padding(bottom = 8.dp)
    )
}

@Composable
private fun PatternCard(
    label: String,
    pattern: DisplayPattern,
    renderer: GlyfSevenSegmentRenderer
) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Canvas(
            modifier = Modifier
                .size(60.dp, 80.dp)
                .background(Color(0xFF0F0F1A), androidx.compose.foundation.shape.RoundedCornerShape(4.dp))
        ) {
            renderer.run {
                drawCell(
                    pattern = pattern,
                    center = Offset(size.width / 2, size.height / 2),
                    width = size.width * 0.7f,
                    height = size.height * 0.75f
                )
            }
        }
        Text(
            text = label,
            color = renderer.onColor.copy(alpha = 0.7f),
            fontFamily = FontFamily.Monospace,
            fontSize = 9.sp,
            modifier = Modifier.padding(top = 4.dp)
        )
    }
}

@Composable
private fun CompositionDemoCard(
    name: String,
    description: String,
    node: glyf.core.parser.GlyfNode,
    renderer: GlyfSevenSegmentRenderer
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color(0xFF0F0F1A), androidx.compose.foundation.shape.RoundedCornerShape(8.dp))
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Canvas(
            modifier = Modifier.size(120.dp, 60.dp)
        ) {
            renderer.run {
                render(
                    node = node,
                    center = Offset(size.width / 2, size.height / 2),
                    cellHeight = size.height * 0.8f
                )
            }
        }
        
        Spacer(modifier = Modifier.width(16.dp))
        
        Column {
            Text(
                text = name,
                color = renderer.onColor,
                fontFamily = FontFamily.Monospace,
                fontWeight = FontWeight.Medium
            )
            Text(
                text = description,
                color = renderer.onColor.copy(alpha = 0.6f),
                fontFamily = FontFamily.Monospace,
                fontSize = 11.sp
            )
        }
    }
}

@Composable
private fun WordRow(
    word: String,
    renderer: GlyfSevenSegmentRenderer,
    onColor: Color
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = word,
            color = onColor.copy(alpha = 0.5f),
            fontFamily = FontFamily.Monospace,
            fontSize = 12.sp,
            modifier = Modifier.width(60.dp)
        )
        
        Canvas(
            modifier = Modifier
                .height(50.dp)
                .widthIn(min = 100.dp, max = 300.dp)
        ) {
            renderer.run {
                renderWord(
                    word = word,
                    center = Offset(size.width / 2, size.height / 2),
                    cellHeight = size.height * 0.75f,
                    mode = CompositionMode.TOUCH
                )
            }
        }
    }
}

@Composable
private fun ExpressionRow(
    notation: String,
    node: glyf.core.parser.GlyfNode,
    renderer: GlyfSevenSegmentRenderer,
    onColor: Color
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = notation,
            color = onColor.copy(alpha = 0.6f),
            fontFamily = FontFamily.Monospace,
            fontSize = 11.sp,
            modifier = Modifier.width(80.dp)
        )
        
        Canvas(
            modifier = Modifier
                .height(50.dp)
                .widthIn(min = 100.dp, max = 300.dp)
        ) {
            renderer.run {
                render(
                    node = node,
                    center = Offset(size.width / 2, size.height / 2),
                    cellHeight = size.height * 0.75f
                )
            }
        }
    }
}

@Composable
private fun ColorVariantCard(
    name: String,
    renderer: GlyfSevenSegmentRenderer,
    color: Color
) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Canvas(
            modifier = Modifier
                .size(70.dp, 90.dp)
                .background(Color(0xFF0F0F1A), androidx.compose.foundation.shape.RoundedCornerShape(8.dp))
        ) {
            renderer.run {
                renderWord(
                    word = "8",
                    center = Offset(size.width / 2, size.height / 2),
                    cellHeight = size.height * 0.7f,
                    mode = CompositionMode.OVERLAP
                )
            }
        }
        Text(
            text = name,
            color = color,
            fontFamily = FontFamily.Monospace,
            fontSize = 10.sp,
            modifier = Modifier.padding(top = 6.dp)
        )
    }
}

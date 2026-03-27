# GLYF 7-Segment Renderer

Jetpack Compose Canvas renderer for the GLYF 7-segment display system.

## Architecture

### Core Files

1. **SevenSegmentRenderer.kt** (370 lines)
   - `SevenSegmentRenderer` - Draws 7-segment display cells with golden ratio proportions
   - `DisplayPattern` - Extended pattern class with rendering utilities
   - `PhiGeometry` - Golden ratio constants (φ = 1.618)
   - Hexagonal lozenge segment shapes with glow effects

2. **WordRenderer.kt** (430 lines)
   - `WordRenderer` - Renders words with 3 composition modes:
     - `OVERLAP` - Letters share same grid (segments blend)
     - `TOUCH` - Letters adjacent, grids share edges
     - `SPACE` - Letters separated by φ-spacing
   - `GlyfSevenSegmentRenderer` - Unified AST-to-display renderer
   - Supports all parser node types: Overlap, Touch, Space, BracketExpr, Group, CharRef

3. **GlyfRendererPreview.kt** (519 lines)
   - `GlyfRendererPreview` - Complete preview composable with 7 sections:
     1. The Seven Segments (A-G)
     2. Digits 0-9
     3. Letters A-F
     4. Composition Modes
     5. AST Expression Examples
     6. Word Examples
     7. Chromatic Variations

## 7-Segment Display Grid

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

## Composition Modes

| Mode | Notation | Description |
|------|----------|-------------|
| OVERLAP | A/B | Same grid, segments blend (OR) |
| TOUCH | A\|B | Adjacent grids, share edges |
| SPACE | A-B | Grids separated by φ-spacing |

## Usage

```kotlin
// Basic cell rendering
val renderer = SevenSegmentRenderer(
    onColor = Color(0xFFD4AF37),   // Golden
    offColor = Color(0xFF1A1A2E),   // Dark
    drawGlow = true
)

Canvas(modifier = Modifier.size(100.dp)) {
    renderer.drawCell(
        pattern = DisplayPattern.DIGIT_8,
        center = Offset(size.width/2, size.height/2),
        width = 60f,
        height = 100f
    )
}

// AST rendering
val glyfRenderer = GlyfSevenSegmentRenderer()

Canvas(modifier = Modifier.size(200.dp)) {
    glyfRenderer.render(
        node = Touch(CharRef('H'), CharRef('I')),
        center = Offset(size.width/2, size.height/2),
        cellHeight = 80f
    )
}

// Word rendering
Canvas(modifier = Modifier.size(300.dp, 100.dp)) {
    glyfRenderer.renderWord(
        word = "GLYF",
        center = Offset(size.width/2, size.height/2),
        cellHeight = 60f,
        mode = CompositionMode.TOUCH
    )
}

// Preview composable
@Composable
fun MyScreen() {
    GlyfRendererPreview(
        backgroundColor = Color(0xFF0A0A14),
        onColor = Color(0xFFD4AF37)
    )
}
```

## Golden Ratio Proportions

- Cell aspect ratio: 0.6 (derived from φ)
- Segment thickness: 12% of cell height
- Mitre gap: 1.5% of cell height
- Space mode spacing: φ⁻¹ × 0.4 × cell width

## Dependencies

- `glyf.core.parser` - AST node types (SevenSegmentPattern, Overlap, Touch, Space, etc.)
- Jetpack Compose Canvas API

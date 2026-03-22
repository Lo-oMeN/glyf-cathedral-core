package com.glyf.cathedral.ui.visualization

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.*
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.glyf.cathedral.core.*
import kotlin.math.*

/**
 * Hexagonal lattice visualization using Compose Canvas
 * Renders the φ⁷ lattice with golden-ratio scaling
 */
@Composable
fun HexLatticeView(
    tiles: List<HexTile>,
    selectedCoord: AxialCoord? = null,
    onTileSelected: (AxialCoord) -> Unit = {},
    onEmptySpaceSelected: (Offset) -> Unit = {},
    modifier: Modifier = Modifier,
    hexSize: Float = 50f,
    showVesica: Boolean = false,
    goldenSpiral: Boolean = false
) {
    val hexRadius = hexSize
    val hexHeight = hexRadius * 2
    val hexWidth = sqrt(3f) * hexRadius
    
    Canvas(
        modifier = modifier
            .fillMaxSize()
            .pointerInput(Unit) {
                detectTapGestures { offset ->
                    // Convert pixel to axial coordinates
                    val coord = pixelToAxial(offset, hexSize, centerX = size.width / 2f, centerY = size.height / 2f)
                    val tile = tiles.find { it.coord == coord }
                    if (tile != null) {
                        onTileSelected(coord)
                    } else {
                        onEmptySpaceSelected(offset)
                    }
                }
            }
    ) {
        val centerX = size.width / 2
        val centerY = size.height / 2
        
        // Draw golden spiral background if enabled
        if (goldenSpiral) {
            drawGoldenSpiral(centerX, centerY, hexSize)
        }
        
        // Draw vesica piscis overlaps if enabled
        if (showVesica) {
            drawVesicaOverlaps(tiles, centerX, centerY, hexSize)
        }
        
        // Draw all tiles
        tiles.forEach { tile ->
            val isSelected = tile.coord == selectedCoord
            drawHexTile(tile, centerX, centerY, hexSize, isSelected)
        }
        
        // Draw coordinate labels for selected
        selectedCoord?.let { coord ->
            val (px, py) = axialToPixel(coord, hexSize, centerX, centerY)
            drawContext.canvas.nativeCanvas.apply {
                val paint = android.graphics.Paint().apply {
                    color = android.graphics.Color.WHITE
                    textSize = 30f
                    textAlign = android.graphics.Paint.Align.CENTER
                }
                drawText("${coord.q},${coord.r},${coord.s}", px, py - hexSize - 20, paint)
            }
        }
    }
}

/**
 * Draw a single hex tile
 */
private fun DrawScope.drawHexTile(
    tile: HexTile,
    centerX: Float,
    centerY: Float,
    hexSize: Float,
    isSelected: Boolean
) {
    val (px, py) = axialToPixel(tile.coord, hexSize, centerX, centerY)
    val corners = getHexCorners(px, py, hexSize)
    
    // Color based on ternary spin and phi magnitude
    val baseColor = when (tile.spin) {
        TernarySpin.NEGATIVE -> Color(0xFFE57373) // Red
        TernarySpin.ZERO -> Color(0xFF64B5F6)    // Blue
        TernarySpin.POSITIVE -> Color(0xFF81C784) // Green
    }
    
    // Modulate alpha by phiMag / PHI_7
    val phiRatio = (tile.phiMag / PhiConstants.PHI_7.toFloat()).coerceIn(0f, 1f)
    val fillColor = baseColor.copy(alpha = 0.3f + phiRatio * 0.5f)
    
    // Draw hexagon
    drawPath(
        path = Path().apply {
            corners.forEachIndexed { index, offset ->
                if (index == 0) moveTo(offset.x, offset.y)
                else lineTo(offset.x, offset.y)
            }
            close()
        },
        color = fillColor
    )
    
    // Draw border
    drawPath(
        path = Path().apply {
            corners.forEachIndexed { index, offset ->
                if (index == 0) moveTo(offset.x, offset.y)
                else lineTo(offset.x, offset.y)
            }
            close()
        },
        color = if (isSelected) Color.White else baseColor,
        style = Stroke(width = if (isSelected) 4f else 2f)
    )
    
    // Draw chiral hash indicator (small inner circle)
    val chiralIntensity = ((tile.chiralHash and 0xFF) / 255.0).toFloat()
    drawCircle(
        color = Color.White.copy(alpha = chiralIntensity),
        radius = hexSize * 0.2f,
        center = Offset(px, py)
    )
    
    // Draw priority indicator (outer ring thickness)
    val priorityRatio = tile.evictionPriority.toInt() / 255f
    if (priorityRatio > 0.5f) {
        drawCircle(
            color = Color.Yellow.copy(alpha = priorityRatio * 0.5f),
            radius = hexSize * 0.9f,
            center = Offset(px, py),
            style = Stroke(width = 3f)
        )
    }
}

/**
 * Draw golden spiral background
 */
private fun DrawScope.drawGoldenSpiral(centerX: Float, centerY: Float, hexSize: Float) {
    val phi = PhiConstants.PHI.toFloat()
    val goldenAngle = PhiConstants.GOLDEN_ANGLE_RAD.toFloat()
    
    var radius = hexSize
    var angle = 0f
    
    repeat(100) { i ->
        val x = centerX + radius * cos(angle)
        val y = centerY + radius * sin(angle)
        
        val alpha = (1f - i / 100f) * 0.3f
        drawCircle(
            color = Color(0xFFFFD700).copy(alpha = alpha),
            radius = 4f,
            center = Offset(x, y)
        )
        
        radius *= 1.02f
        angle += goldenAngle
    }
}

/**
 * Draw vesica piscis overlaps between nearby tiles
 */
private fun DrawScope.drawVesicaOverlaps(
    tiles: List<HexTile>,
    centerX: Float,
    centerY: Float,
    hexSize: Float
) {
    // Find overlapping pairs (distance == 1)
    val pairs = mutableListOf<Pair<HexTile, HexTile>>()
    
    tiles.forEachIndexed { i, tile1 ->
        tiles.drop(i + 1).forEach { tile2 ->
            if (tile1.coord.distanceTo(tile2.coord) == 1) {
                pairs.add(tile1 to tile2)
            }
        }
    }
    
    // Draw vesica piscis for each pair
    pairs.forEach { (t1, t2) ->
        val (x1, y1) = axialToPixel(t1.coord, hexSize, centerX, centerY)
        val (x2, y2) = axialToPixel(t2.coord, hexSize, centerX, centerY)
        
        val midX = (x1 + x2) / 2
        val midY = (y1 + y2) / 2
        val distance = sqrt((x2 - x1).pow(2) + (y2 - y1).pow(2))
        
        // Vesica lens (simplified as ellipse)
        drawOval(
            color = Color(0xFF9C27B0).copy(alpha = 0.2f),
            topLeft = Offset(midX - distance/4, midY - distance/6),
            size = androidx.compose.ui.geometry.Size(distance/2, distance/3)
        )
    }
}

/**
 * Convert axial coordinates to pixel position
 */
private fun axialToPixel(
    coord: AxialCoord,
    hexSize: Float,
    centerX: Float,
    centerY: Float
): Pair<Float, Float> {
    val q = coord.q.toFloat()
    val r = coord.r.toFloat()
    
    val x = hexSize * (sqrt(3f) * q + sqrt(3f) / 2 * r)
    val y = hexSize * (3f / 2 * r)
    
    return Pair(centerX + x, centerY + y)
}

/**
 * Convert pixel position to axial coordinates (approximate)
 */
private fun pixelToAxial(
    offset: Offset,
    hexSize: Float,
    centerX: Float,
    centerY: Float
): AxialCoord {
    val x = (offset.x - centerX) / hexSize
    val y = (offset.y - centerY) / hexSize
    
    val q = (sqrt(3f) / 3 * x - 1f / 3 * y)
    val r = (2f / 3 * y)
    val s = -q - r
    
    return cubeRound(q, r, s)
}

/**
 * Round floating point cube coordinates to nearest hex
 */
private fun cubeRound(q: Float, r: Float, s: Float): AxialCoord {
    var rq = q.roundToInt()
    var rr = r.roundToInt()
    var rs = s.roundToInt()
    
    val dq = abs(rq - q)
    val dr = abs(rr - r)
    val ds = abs(rs - s)
    
    if (dq > dr && dq > ds) {
        rq = -rr - rs
    } else if (dr > ds) {
        rr = -rq - rs
    } else {
        rs = -rq - rr
    }
    
    return AxialCoord(rq, rr, rs)
}

/**
 * Get the 6 corners of a hexagon
 */
private fun getHexCorners(centerX: Float, centerY: Float, size: Float): List<Offset> {
    return (0 until 6).map { i ->
        val angle = (Math.PI / 3 * i - Math.PI / 6).toFloat()
        Offset(
            centerX + size * cos(angle),
            centerY + size * sin(angle)
        )
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// PREVIEWS
// ═══════════════════════════════════════════════════════════════════════════

@Preview(showBackground = true)
@Composable
fun HexLatticeViewPreview() {
    val sampleTiles = listOf(
        HexTile(AxialCoord.ORIGIN, TernarySpin.ZERO, 10.0f),
        HexTile(AxialCoord.fromQr(1, 0), TernarySpin.POSITIVE, 15.0f),
        HexTile(AxialCoord.fromQr(-1, 1), TernarySpin.NEGATIVE, 8.0f),
        HexTile(AxialCoord.fromQr(0, -1), TernarySpin.ZERO, 20.0f),
        HexTile(AxialCoord.fromQr(2, -1), TernarySpin.POSITIVE, 25.0f),
        HexTile(AxialCoord.fromQr(-2, 1), TernarySpin.NEGATIVE, 5.0f),
        HexTile(AxialCoord.fromQr(1, 1), TernarySpin.ZERO, 18.0f),
        HexTile(AxialCoord.fromQr(-1, -1), TernarySpin.POSITIVE, 12.0f),
    ).map { it.withPriority(10) }
    
    HexLatticeView(
        tiles = sampleTiles,
        selectedCoord = AxialCoord.ORIGIN,
        modifier = Modifier.size(400.dp),
        showVesica = true,
        goldenSpiral = true
    )
}

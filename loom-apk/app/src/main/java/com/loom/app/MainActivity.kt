package com.loom.app

import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.Choreographer
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.*
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import kotlin.math.*
import android.util.Log
import java.io.File
import java.io.FileOutputStream
import java.io.FileInputStream

class MainActivity : ComponentActivity() {
    
    private lateinit var stateMachine: StateMachine
    private val resurrectionLog = StringBuilder()
    private var coldStartTime: Long = 0
    
    override fun onCreate(savedInstanceState: Bundle?) {
        coldStartTime = System.nanoTime()
        super.onCreate(savedInstanceState)
        
        stateMachine = StateMachine()
        
        // Attempt resurrection from Bundle (warm) or disk (cold)
        val resurrectStart = System.nanoTime()
        var resurrectSource = "none"
        
        if (savedInstanceState != null) {
            val bundleData = savedInstanceState.getByteArray("lattice")
            if (bundleData != null && bundleData.size == 96) {
                System.arraycopy(bundleData, 0, stateMachine.current.data, 0, 96)
                resurrectSource = "bundle"
            }
        }
        
        // Fallback to disk cryogenics
        if (resurrectSource == "none") {
            val cryoFile = File(filesDir, "lattice_cryo.bin")
            if (stateMachine.current.resurrect(cryoFile)) {
                resurrectSource = "disk"
            }
        }
        
        val resurrectTime = (System.nanoTime() - resurrectStart) / 1_000_000.0 // ms
        val totalColdTime = (System.nanoTime() - coldStartTime) / 1_000_000.0 // ms
        
        Log.i("L∞M∆N", "Resurrection: source=$resurrectSource, time=${String.format("%.3f", resurrectTime)}ms, total=${String.format("%.3f", totalColdTime)}ms")
        resurrectionLog.append("Resurrect: $resurrectSource, ${String.format("%.3f", resurrectTime)}ms\n")
        
        setContent {
            LoomApp(
                stateMachine = stateMachine,
                resurrectionLog = resurrectionLog.toString()
            )
        }
    }
    
    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        val cryoStart = System.nanoTime()
        outState.putByteArray("lattice", stateMachine.current.data.clone())
        
        // Also cryogenize to disk
        val cryoFile = File(filesDir, "lattice_cryo.bin")
        stateMachine.current.cryogenize(cryoFile)
        
        val cryoTime = (System.nanoTime() - cryoStart) / 1_000_000.0
        Log.i("L∞M∆N", "Cryogenize: time=${String.format("%.3f", cryoTime)}ms")
    }
    
    override fun onRestoreInstanceState(savedInstanceState: Bundle) {
        super.onRestoreInstanceState(savedInstanceState)
        // Already handled in onCreate
    }
}

// ============================================
// 96-BYTE LATTICE STATE (packed) with Cryogenize
// ============================================
class LatticeState {
    val data = ByteArray(96)
    
    var timestamp: Long
        get() = longFrom(0)
        set(v) = longTo(0, v)
    
    var energy: Double
        get() = doubleFrom(24)
        set(v) = doubleTo(24, v)
    
    fun getHarmonic(i: Int): Int = intFrom(64 + i * 4)
    fun setHarmonic(i: Int, v: Int) = intTo(64 + i * 4, v)
    
    // Cryogenize to disk (SD card persistence)
    fun cryogenize(file: File): Boolean {
        return try {
            FileOutputStream(file).use { it.write(data) }
            true
        } catch (e: Exception) {
            Log.e("LatticeState", "Cryogenize failed: ${e.message}")
            false
        }
    }
    
    // Resurrect from disk
    fun resurrect(file: File): Boolean {
        return try {
            if (!file.exists()) return false
            FileInputStream(file).use { it.read(data) }
            true
        } catch (e: Exception) {
            Log.e("LatticeState", "Resurrect failed: ${e.message}")
            false
        }
    }
    
    private fun longFrom(o: Int): Long {
        var r = 0L
        for (i in 0..7) r = r or ((data[o + i].toLong() and 0xFF) shl (i * 8))
        return r
    }
    private fun longTo(o: Int, v: Long) {
        for (i in 0..7) data[o + i] = ((v shr (i * 8)) and 0xFF).toByte()
    }
    private fun doubleFrom(o: Int): Double = Double.fromBits(longFrom(o))
    private fun doubleTo(o: Int, v: Double) = longTo(o, v.toBits())
    private fun intFrom(o: Int): Int {
        var r = 0
        for (i in 0..3) r = r or ((data[o + i].toInt() and 0xFF) shl (i * 8))
        return r
    }
    private fun intTo(o: Int, v: Int) {
        for (i in 0..3) data[o + i] = ((v shr (i * 8)) and 0xFF).toByte()
    }
}

// ============================================
// STATE MACHINE - Weak emergence
// ============================================
class StateMachine {
    private val history = mutableListOf<LatticeState>()
    var current = LatticeState().apply {
        timestamp = System.currentTimeMillis()
        energy = 1.0
        repeat(8) { setHarmonic(it, (0..1024).random()) }
    }
    
    fun step(): LatticeState {
        history.add(current)
        if (history.size > 50) history.removeAt(0)
        
        val next = LatticeState()
        next.timestamp = System.currentTimeMillis()
        
        // φ-weighted divergence
        val phi = 1.618033988749895
        val divergence = if (Random.nextDouble() < (1/phi)) 0.95 else 1.05
        next.energy = (current.energy * divergence).coerceIn(0.5, 2.0)
        
        // Harmonic resonance
        repeat(8) { i ->
            val phase = history.takeLast(3).map { it.getHarmonic(i) }.sum() / 3
            next.setHarmonic(i, (phase + Random.nextInt(-30, 30)) % 1024)
        }
        
        current = next
        return next
    }
}

// ============================================
// MAIN APP with Choreographer frame sync
// ============================================
@Composable
fun LoomApp(stateMachine: StateMachine, resurrectionLog: String) {
    var state by remember { mutableStateOf(stateMachine.current) }
    var isRunning by remember { mutableStateOf(true) }
    var fps by remember { mutableStateOf(0) }
    var jankyFrames by remember { mutableStateOf(0) }
    var totalFrames by remember { mutableStateOf(0) }
    
    // Choreographer-based frame loop (proper 60 FPS sync)
    val frameCallback = remember {
        object : Choreographer.FrameCallback {
            var lastFrameTime = 0L
            
            override fun doFrame(frameTimeNanos: Long) {
                if (!isRunning) return
                
                // Calculate frame timing
                if (lastFrameTime != 0L) {
                    val frameDelta = (frameTimeNanos - lastFrameTime) / 1_000_000.0 // ms
                    val expectedFrame = 16.67 // 60 FPS
                    
                    totalFrames++
                    if (frameDelta > expectedFrame * 1.5) {
                        jankyFrames++
                    }
                    
                    // Update FPS every 30 frames
                    if (totalFrames % 30 == 0) {
                        fps = (1000.0 / frameDelta).toInt()
                    }
                }
                lastFrameTime = frameTimeNanos
                
                // Step the state machine
                state = stateMachine.step()
                
                // Schedule next frame
                Choreographer.getInstance().postFrameCallback(this)
            }
        }
    }
    
    DisposableEffect(isRunning) {
        if (isRunning) {
            Choreographer.getInstance().postFrameCallback(frameCallback)
        }
        onDispose {
            Choreographer.getInstance().removeFrameCallback(frameCallback)
        }
    }
    
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Black)
    ) {
        // Background visualizer
        LoomVisualizer(
            state = state,
            modifier = Modifier.fillMaxSize()
        )
        
        // UI overlay
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            // Header
            Column {
                Text(
                    "L∞M∆N",
                    fontSize = 32.sp,
                    fontWeight = FontWeight.Thin,
                    letterSpacing = 8.sp,
                    color = Color(0xFFFFD700)
                )
                Text(
                    "φ⁶ Edition | A03s Stress Test",
                    fontSize = 12.sp,
                    color = Color.White.copy(alpha = 0.6)
                )
                if (resurrectionLog.isNotEmpty()) {
                    Text(
                        resurrectionLog.trim(),
                        fontSize = 10.sp,
                        color = Color(0xFF00FF00),
                        modifier = Modifier.padding(top = 4.dp)
                    )
                }
            }
            
            // Performance metrics
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                MetricCard("ENERGY", "%.2f".format(state.energy))
                MetricCard("FPS", fps.toString())
                MetricCard("JANK", "$jankyFrames/$totalFrames")
            }
            
            // State metrics
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                MetricCard("κ", "%.3f".format(1.0 - (jankyFrames.toDouble() / max(totalFrames, 1))))
                MetricCard("TIME", "${state.timestamp % 10000}")
                MetricCard("H0", state.getHarmonic(0).toString())
            }
            
            // Controls
            Button(
                onClick = { isRunning = !isRunning },
                colors = ButtonDefaults.buttonColors(
                    containerColor = Color(0xFFFFD700).copy(alpha = 0.2f)
                )
            ) {
                Text(
                    if (isRunning) "⏸ PAUSE" else "▶ RESUME",
                    color = Color(0xFFFFD700)
                )
            }
        }
    }
}
}

@Composable
fun MetricCard(label: String, value: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(label, fontSize = 10.sp, color = Color.White.copy(alpha = 0.5))
        Text(value, fontSize = 18.sp, color = Color(0xFFFFD700))
    }
}

// ============================================
// VISUALIZER - Sacred geometry rendering
// ============================================
@Composable
fun LoomVisualizer(state: LatticeState, modifier: Modifier = Modifier) {
    Canvas(modifier = modifier) {
        val centerX = size.width / 2
        val centerY = size.height / 2
        val baseRadius = min(size.width, size.height) * 0.15f
        
        // Background glow
        drawCircle(
            color = Color(0xFFFFD700).copy(alpha = 0.05f),
            radius = baseRadius * 3,
            center = Offset(centerX, centerY)
        )
        
        // Draw phyllotaxis spiral
        drawPhyllotaxis(centerX, centerY, baseRadius, state)
        
        // Draw Vesica interference
        drawVesica(centerX, centerY, baseRadius, state)
        
        // Draw Flower of Life
        drawFlowerOfLife(centerX, centerY, baseRadius, state)
    }
}

private fun DrawScope.drawPhyllotaxis(cx: Float, cy: Float, baseR: Float, state: LatticeState) {
    val phi = 1.618033988749895f
    val goldenAngle = 2.39996323f
    val count = 60
    val maxRadius = baseR * 2.5f
    
    for (i in 0 until count) {
        val angle = i * goldenAngle + (state.timestamp % 1000) / 1000f * 0.5f
        val radius = sqrt(i.toFloat() / count) * maxRadius
        val x = cx + cos(angle) * radius
        val y = cy + sin(angle) * radius
        
        val harmonic = state.getHarmonic(i % 8)
        val hue = (harmonic / 1024f * 60 + 30) % 360
        val color = HSVtoColor(hue, 0.8f, 1f)
        
        drawCircle(
            color = color.copy(alpha = 0.6f),
            radius = 4f + (harmonic % 10),
            center = Offset(x, y)
        )
    }
}

private fun DrawScope.drawVesica(cx: Float, cy: Float, baseR: Float, state: LatticeState) {
    val energyF = state.energy.toFloat()
    val offset = baseR * 0.5f * energyF
    val radius = baseR * energyF
    
    // Two overlapping circles
    for (i in 0..1) {
        val sign = if (i == 0) 1 else -1
        val centerX = cx + sign * offset
        
        drawCircle(
            color = Color(0xFFFFD700).copy(alpha = 0.15f),
            radius = radius,
            center = Offset(centerX, cy),
            style = Stroke(width = 2f)
        )
    }
    
    // Lens intersection
    drawCircle(
        color = Color(0xFFFFD700).copy(alpha = 0.3f),
        radius = radius * 0.3f,
        center = Offset(cx, cy)
    )
}

private fun DrawScope.drawFlowerOfLife(cx: Float, cy: Float, baseR: Float, state: LatticeState) {
    val rings = 2
    val r = baseR * 0.8f
    
    for (ring in 0..rings) {
        val count = if (ring == 0) 1 else ring * 6
        for (i in 0 until count) {
            val angle = (i.toFloat() / count) * 2 * PI.toFloat() + ring * 0.5f
            val dist = if (ring == 0) 0f else r * 1.732f * ring
            val x = cx + cos(angle) * dist
            val y = cy + sin(angle) * dist
            
            drawCircle(
                color = Color(0xFFFF6B35).copy(alpha = 0.1f),
                radius = r,
                center = Offset(x, y),
                style = Stroke(width = 1f)
            )
        }
    }
}

private fun HSVtoColor(h: Float, s: Float, v: Float): Color {
    val c = v * s
    val x = c * (1 - abs((h / 60) % 2 - 1))
    val m = v - c
    
    val (r, g, b) = when {
        h < 60 -> Triple(c, x, 0f)
        h < 120 -> Triple(x, c, 0f)
        h < 180 -> Triple(0f, c, x)
        h < 240 -> Triple(0f, x, c)
        h < 300 -> Triple(x, 0f, c)
        else -> Triple(c, 0f, x)
    }
    
    return Color((r + m), (g + m), (b + m))
}

package com.glyf.cathedral.visualizer

import android.content.Context
import android.graphics.*
import android.util.AttributeSet
import android.view.SurfaceHolder
import android.view.SurfaceView
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlin.math.*

/**
 * The Lumen Field - Sacred Geometry Visualizer
 * Renders: Vesica interference, Flower of Life, Phyllotaxis spiral
 * Feeds from: Chat semantic perturbations, Audio input, Touch interactions
 */

class LumenViewModel : ViewModel() {
    
    private val _emergence = MutableStateFlow(0.0f)
    val emergence: StateFlow<Float> = _emergence.asStateFlow()
    
    private val _coherence = MutableStateFlow(0.0f)
    val coherence: StateFlow<Float> = _coherence.asStateFlow()
    
    private val _reflexCount = MutableStateFlow(0)
    val reflexCount: StateFlow<Int> = _reflexCount.asStateFlow()
    
    private val _latticeState = MutableStateFlow(LatticeState())
    
    // Semantic perturbations from chat
    private val perturbationQueue = mutableListOf<SemanticPerturbation>()
    
    init {
        viewModelScope.launch {
            while (isActive) {
                simulateFieldEvolution()
                delay(16) // 60 FPS
            }
        }
    }
    
    private fun simulateFieldEvolution() {
        _reflexCount.value++
        
        // Calculate emergence based on perturbations and time
        val baseEmergence = 0.3f + (sin(System.currentTimeMillis() / 1000f) * 0.2f)
        val perturbationBoost = perturbationQueue.size * 0.05f
        val newEmergence = (baseEmergence + perturbationBoost).coerceIn(0f, 1f)
        
        _emergence.value = newEmergence
        _coherence.value = 0.5f + (newEmergence * 0.5f)
        
        // Clear processed perturbations
        if (perturbationQueue.isNotEmpty() && _reflexCount.value % 60 == 0) {
            perturbationQueue.clear()
        }
    }
    
    fun injectSemanticPerturbation(message: String) {
        val type = when {
            message.contains("?") -> PerturbationType.QUESTION
            message.contains("!") -> PerturbationType.EXCLAMATION
            message.length > 50 -> PerturbationType.DEEP_THOUGHT
            else -> PerturbationType.STATEMENT
        }
        
        perturbationQueue.add(SemanticPerturbation(message, type, System.currentTimeMillis()))
        
        // Immediate boost to emergence
        _emergence.value = (_emergence.value + 0.1f).coerceAtMost(1f)
    }
    
    fun getCurrentLatticeState(): LatticeState = _latticeState.value
}

@Composable
fun LumenField(
    viewModel: LumenViewModel,
    modifier: Modifier = Modifier
) {
    AndroidView(
        factory = { context ->
            LumenSurfaceView(context).apply {
                this.viewModel = viewModel
            }
        },
        modifier = modifier.fillMaxSize()
    )
}

class LumenSurfaceView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null
) : SurfaceView(context, attrs), SurfaceHolder.Callback, Runnable {

    lateinit var viewModel: LumenViewModel
    private var thread: Thread? = null
    private var running = false
    
    // Geometry constants
    private val PHI = 1.618033988749895
    private val GOLDEN_ANGLE = 2.399963229728653
    private val TAU = 2.0 * PI
    
    // Paint objects (reused for performance)
    private val circlePaint = Paint(Paint.ANTI_ALIAS_FLAG)
    private val gradientPaint = Paint(Paint.ANTI_ALIAS_FLAG)
    private val linePaint = Paint(Paint.ANTI_ALIAS_FLAG)
    private val particlePaint = Paint(Paint.ANTI_ALIAS_FLAG)
    
    // Animation state
    private var time = 0f
    private val particles = mutableListOf<Particle>()
    
    init {
        holder.addCallback(this)
        setZOrderOnTop(false)
    }
    
    override fun surfaceCreated(holder: SurfaceHolder) {
        running = true
        thread = Thread(this)
        thread?.start()
    }
    
    override fun surfaceChanged(holder: SurfaceHolder, format: Int, width: Int, height: Int) {}
    
    override fun surfaceDestroyed(holder: SurfaceHolder) {
        running = false
        thread?.join()
    }
    
    override fun run() {
        while (running) {
            val canvas = holder.lockCanvas()
            if (canvas != null) {
                try {
                    drawFrame(canvas)
                } finally {
                    holder.unlockCanvasAndPost(canvas)
                }
            }
            time += 0.016f
        }
    }
    
    private fun drawFrame(canvas: Canvas) {
        val width = canvas.width.toFloat()
        val height = canvas.height.toFloat()
        val cx = width / 2
        val cy = height / 2
        val emergence = viewModel.emergence.value
        val coherence = viewModel.coherence.value
        
        // Clear with deep space gradient
        canvas.drawColor(Color.BLACK)
        
        // Background gradient
        val bgGradient = RadialGradient(
            cx, cy, max(width, height),
            intArrayOf(
                Color.argb((20 + emergence * 30).toInt(), 10, 8, 20),
                Color.argb(255, 0, 0, 0)
            ),
            floatArrayOf(0f, 1f),
            Shader.TileMode.CLAMP
        )
        canvas.drawPaint(Paint().apply { shader = bgGradient })
        
        // Draw phyllotaxis spiral
        drawPhyllotaxis(canvas, cx, cy, emergence, coherence)
        
        // Draw Flower of Life
        drawFlowerOfLife(canvas, cx, cy, emergence)
        
        // Draw Vesica interference
        drawVesicaInterference(canvas, cx, cy, emergence)
        
        // Draw and update particles
        drawParticles(canvas)
        
        // Draw central glow
        drawCentralGlow(canvas, cx, cy, emergence)
    }
    
    private fun drawPhyllotaxis(canvas: Canvas, cx: Float, cy: Float, emergence: Float, coherence: Float) {
        val count = (100 + emergence * 200).toInt()
        val maxRadius = min(canvas.width, canvas.height) * 0.4f * (1 + emergence * 0.3f)
        
        for (i in 0 until count) {
            val angle = i * GOLDEN_ANGLE + time * 0.02
            val radius = sqrt(i.toFloat() / count) * maxRadius * (1 + emergence * 0.2f)
            
            val x = cx + cos(angle).toFloat() * radius
            val y = cy + sin(angle).toFloat() * radius
            
            val baseSize = 3f
            val pulseSize = baseSize + sin(time * 3 + i * 0.1f) * 2f * emergence
            
            val hue = (i.toFloat() / count * 60 + 30 + time * 10) % 360
            val color = Color.HSVToColor(
                (180 + emergence * 75).toInt(),
                floatArrayOf(hue, 0.8f, 1f)
            )
            
            particlePaint.color = color
            canvas.drawCircle(x, y, pulseSize, particlePaint)
            
            // Connect nearby points for web effect
            if (i > 0 && i % 7 == 0 && emergence > 0.5f) {
                val prevAngle = (i - 7) * GOLDEN_ANGLE + time * 0.02
                val prevRadius = sqrt((i - 7).toFloat() / count) * maxRadius * (1 + emergence * 0.2f)
                val px = cx + cos(prevAngle).toFloat() * prevRadius
                val py = cy + sin(prevAngle).toFloat() * prevRadius
                
                linePaint.color = color and 0x40FFFFFF
                linePaint.strokeWidth = 1f
                canvas.drawLine(x, y, px, py, linePaint)
            }
        }
    }
    
    private fun drawFlowerOfLife(canvas: Canvas, cx: Float, cy: Float, emergence: Float) {
        val rings = (3 + emergence * 4).toInt()
        val baseRadius = min(canvas.width, canvas.height) * 0.08f
        
        for (ring in 0 until rings) {
            val count = if (ring == 0) 1 else ring * 6
            val radius = baseRadius * (1 + ring * 0.5f) * (1 + emergence * 0.3f)
            
            for (i in 0 until count) {
                val angle = (i.toFloat() / count) * TAU + (ring * PI / 3) + time * 0.05f
                val dist = if (ring == 0) 0f else baseRadius * 1.732f * ring * (1 + emergence * 0.2f)
                
                val x = cx + cos(angle).toFloat() * dist
                val y = cy + sin(angle).toFloat() * dist
                
                val pulse = 1f + sin(time * 2 + ring + i) * 0.1f * emergence
                val r = radius * pulse
                
                val hue = (40 + ring * 10 + emergence * 20) % 360
                val alpha = (30 + emergence * 40).toInt()
                
                // Gradient circle
                val gradient = RadialGradient(
                    x, y, r,
                    intArrayOf(
                        Color.HSVToColor(alpha, floatArrayOf(hue, 1f, 1f)),
                        Color.HSVToColor(0, floatArrayOf(hue, 1f, 0.5f))
                    ),
                    floatArrayOf(0f, 1f),
                    Shader.TileMode.CLAMP
                )
                
                circlePaint.shader = gradient
                canvas.drawCircle(x, y, r, circlePaint)
                
                // Stroke
                circlePaint.shader = null
                circlePaint.color = Color.HSVToColor(
                    (50 + emergence * 50).toInt(),
                    floatArrayOf(hue, 1f, 1f)
                )
                circlePaint.style = Paint.Style.STROKE
                circlePaint.strokeWidth = 1f
                canvas.drawCircle(x, y, r, circlePaint)
                circlePaint.style = Paint.Style.FILL
            }
        }
    }
    
    private fun drawVesicaInterference(canvas: Canvas, cx: Float, cy: Float, emergence: Float) {
        val count = (5 + emergence * 8).toInt()
        val baseRadius = min(canvas.width, canvas.height) * 0.15f * (0.8f + emergence * 0.4f)
        
        for (i in 0 until count) {
            val angle = (i.toFloat() / count) * TAU + time * 0.1f * (1 + emergence)
            val dist = baseRadius * 0.5f * (1 + emergence * 0.5f)
            
            val x = cx + cos(angle).toFloat() * dist
            val y = cy + sin(angle).toFloat() * dist
            val r = baseRadius * (1 + emergence * 0.5f)
            
            val hue = (30 + i * 10 + emergence * 30) % 360
            
            // Outer glow
            val glowGradient = RadialGradient(
                x, y, r * 2,
                intArrayOf(
                    Color.HSVToColor((100 * emergence).toInt(), floatArrayOf(hue, 1f, 1f)),
                    Color.TRANSPARENT
                ),
                floatArrayOf(0f, 1f),
                Shader.TileMode.CLAMP
            )
            
            gradientPaint.shader = glowGradient
            canvas.drawCircle(x, y, r * 2, gradientPaint)
            
            // Main circle
            val mainGradient = RadialGradient(
                x, y, r,
                intArrayOf(
                    Color.HSVToColor((40 + emergence * 40).toInt(), floatArrayOf(hue, 1f, 1f)),
                    Color.HSVToColor(0, floatArrayOf(hue, 1f, 0.5f))
                ),
                floatArrayOf(0f, 1f),
                Shader.TileMode.CLAMP
            )
            
            circlePaint.shader = mainGradient
            canvas.drawCircle(x, y, r, circlePaint)
        }
    }
    
    private fun drawParticles(canvas: Canvas) {
        // Update and draw existing particles
        val iterator = particles.iterator()
        while (iterator.hasNext()) {
            val p = iterator.next()
            p.update()
            
            if (p.life <= 0) {
                iterator.remove()
                continue
            }
            
            val alpha = (p.life * 255).toInt()
            particlePaint.color = Color.argb(alpha, 255, 215, 0)
            canvas.drawCircle(p.x, p.y, p.size, particlePaint)
        }
        
        // Spawn new particles occasionally
        if (particles.size < 100 && Math.random() < 0.1) {
            val cx = canvas.width / 2f
            val cy = canvas.height / 2f
            val angle = Math.random() * TAU
            val speed = 2.0 + Math.random() * 3.0
            particles.add(Particle(
                cx, cy,
                (cos(angle) * speed).toFloat(),
                (sin(angle) * speed).toFloat(),
                (1.0 + Math.random()).toFloat(),
                (2f + Math.random() * 4f).toFloat()
            ))
        }
    }
    
    private fun drawCentralGlow(canvas: Canvas, cx: Float, cy: Float, emergence: Float) {
        val maxRadius = max(canvas.width, canvas.height) * 0.5f
        
        val glowGradient = RadialGradient(
            cx, cy, maxRadius,
            intArrayOf(
                Color.argb((50 + emergence * 100).toInt(), 255, 215, 0),
                Color.argb((20 + emergence * 30).toInt(), 255, 107, 53),
                Color.TRANSPARENT
            ),
            floatArrayOf(0f, 0.5f, 1f),
            Shader.TileMode.CLAMP
        )
        
        gradientPaint.shader = glowGradient
        canvas.drawCircle(cx, cy, maxRadius, gradientPaint)
    }
    
    private data class Particle(
        var x: Float,
        var y: Float,
        var vx: Float,
        var vy: Float,
        var life: Float,
        val size: Float
    ) {
        fun update() {
            x += vx
            y += vy
            life -= 0.02f
            vx *= 0.98f
            vy *= 0.98f
        }
    }
}

// Data classes
data class LatticeState(
    val centerS: Pair<Float, Float> = Pair(0f, 0f),
    val ternaryJunction: List<Int> = List(16) { 0 },
    val morphogenPhase: Int = 0
)

data class SemanticPerturbation(
    val message: String,
    val type: PerturbationType,
    val timestamp: Long
)

enum class PerturbationType {
    STATEMENT,      // Neutral assertion
    QUESTION,       // Opening, inquiry
    EXCLAMATION,    // High energy, emphasis
    DEEP_THOUGHT    // Extended, complex
}

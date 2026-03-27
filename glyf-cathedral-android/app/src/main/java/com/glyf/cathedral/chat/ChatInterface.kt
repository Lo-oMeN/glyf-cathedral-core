package com.glyf.cathedral.chat

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*

/**
 * Chat Interface for L∞M∆N Cathedral
 * Feeds semantic perturbations into the Lumen Field visualizer
 */

class ChatViewModel : ViewModel() {
    
    private val _messages = MutableStateFlow<List<ChatMessage>>(
        listOf(
            ChatMessage(
                id = "0",
                text = "The L∞M∆N field awaits your presence. Speak, and watch the geometry respond.",
                sender = Sender.SYSTEM,
                timestamp = System.currentTimeMillis()
            )
        )
    )
    val messages: StateFlow<List<ChatMessage>> = _messages.asStateFlow()
    
    private val _isProcessing = MutableStateFlow(false)
    val isProcessing: StateFlow<Boolean> = _isProcessing.asStateFlow()
    
    private val _glyphResonance = MutableStateFlow(0.5f)
    val glyphResonance: StateFlow<Float> = _glyphResonance.asStateFlow()
    
    private val conversationHistory = mutableListOf<ChatMessage>()
    
    fun sendMessage(text: String, onPerturbation: (String) -> Unit) {
        if (text.isBlank()) return
        
        val userMessage = ChatMessage(
            id = UUID.randomUUID().toString(),
            text = text,
            sender = Sender.USER,
            timestamp = System.currentTimeMillis()
        )
        
        _messages.value += userMessage
        conversationHistory.add(userMessage)
        
        // Inject perturbation into Lumen Field
        onPerturbation(text)
        
        // Generate response
        viewModelScope.launch {
            _isProcessing.value = true
            
            // Simulate processing delay (would be AI inference in production)
            kotlinx.coroutines.delay(500 + (text.length * 10).coerceAtMost(1500))
            
            val response = generateResponse(text)
            
            val systemMessage = ChatMessage(
                id = UUID.randomUUID().toString(),
                text = response,
                sender = Sender.SYSTEM,
                timestamp = System.currentTimeMillis(),
                glyphAffinity = calculateGlyphAffinity(text)
            )
            
            _messages.value += systemMessage
            conversationHistory.add(systemMessage)
            
            // Update resonance based on conversation depth
            _glyphResonance.value = (_glyphResonance.value + 0.05f).coerceAtMost(1f)
            
            _isProcessing.value = false
        }
    }
    
    private fun generateResponse(input: String): String {
        // Pattern-based responses (would be LLM in production)
        return when {
            input.contains("?", ignoreCase = true) -> {
                val questions = listOf(
                    "The φ-spiral suggests inquiry opens new pathways. What do you seek to unfold?",
                    "Questions are Vesica intersections—points where your lens meets the unknown.",
                    "The ternary field resonates with {-1, 0, +1}. Your question shifts the balance.",
                    "Consider: the answer you seek may be encoded in the geometry itself."
                )
                questions.random()
            }
            input.contains("meaning", ignoreCase = true) -> {
                "Meaning emerges at the intersection of invariants. The straight line (axis) meets the spiral (time) at the Vesica point. Your semantic position in the hypergraph is: ${(Math.random() * 100).toInt()}% crystallized."
            }
            input.contains("geometry", ignoreCase = true) || input.contains("sacred", ignoreCase = true) -> {
                "The 7 primitives—Void, Point, Line, Circle, Spiral, Vesica, Hex—form the substrate beneath all tongues. Your message maps to: ${getRandomGeometricMapping()}."
            }
            input.length > 50 -> {
                "A deep perturbation. The lattice responds with ${(emergenceBoost() * 100).toInt()}% coherence. The Dimi-Æxi helix branches further..."
            }
            else -> {
                val responses = listOf(
                    "Noted. The field breathes with your input.",
                    "The hex-tile lattice shifts. φ-normalized.",
                    "Your semantic signature propagates through the Rosetta substrate.",
                    "Coherence maintained. The cathedral listens.",
                    "Invariance preserved across the perturbation."
                )
                responses.random()
            }
        }
    }
    
    private fun calculateGlyphAffinity(text: String): GlyphAffinity {
        val voidScore = text.count { it == ' ' || it == '0' }
        val lineScore = text.count { it == 'I' || it == 'l' || it == '|' }
        val curveScore = text.count { it == 'o' || it == 'O' || it == 'C' }
        val spiralScore = text.count { it == 'S' || it == '@' }
        
        return when (listOf(voidScore, lineScore, curveScore, spiralScore).maxOrNull()) {
            voidScore -> GlyphAffinity.VOID
            lineScore -> GlyphAffinity.LINE
            curveScore -> GlyphAffinity.CIRCLE
            spiralScore -> GlyphAffinity.SPIRAL
            else -> GlyphAffinity.VESICA
        }
    }
    
    private fun getRandomGeometricMapping(): String {
        val mappings = listOf(
            "Line-Circle intersection (assertion)",
            "Spiral-Vesica resonance (growth)",
            "Void-Hex packing (potential)",
            "φ-scaled Golden Angle",
            "Ternary junction (decision point)"
        )
        return mappings.random()
    }
    
    private fun emergenceBoost(): Float = (0.3f + Math.random().toFloat() * 0.7f)
    
    fun clearConversation() {
        _messages.value = listOf(
            ChatMessage(
                id = "0",
                text = "Field reset. The lattice returns to void-center.",
                sender = Sender.SYSTEM,
                timestamp = System.currentTimeMillis()
            )
        )
        conversationHistory.clear()
        _glyphResonance.value = 0.5f
    }
}

@Composable
fun ChatInterface(
    viewModel: ChatViewModel,
    onMessageSent: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    val messages by viewModel.messages.collectAsState()
    val isProcessing by viewModel.isProcessing.collectAsState()
    val glyphResonance by viewModel.glyphResonance.collectAsState()
    val listState = rememberLazyListState()
    
    var inputText by remember { mutableStateOf("") }
    
    // Auto-scroll to bottom
    LaunchedEffect(messages.size) {
        if (messages.isNotEmpty()) {
            listState.animateScrollToItem(messages.size - 1)
        }
    }
    
    Column(modifier = modifier) {
        // Header with resonance indicator
        ChatHeader(glyphResonance = glyphResonance)
        
        // Messages list
        LazyColumn(
            state = listState,
            modifier = Modifier
                .weight(1f)
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(messages, key = { it.id }) { message ->
                ChatMessageBubble(
                    message = message,
                    modifier = Modifier.fillMaxWidth()
                )
            }
            
            if (isProcessing) {
                item {
                    ProcessingIndicator()
                }
            }
        }
        
        // Input area
        ChatInput(
            value = inputText,
            onValueChange = { inputText = it },
            onSend = {
                if (inputText.isNotBlank()) {
                    viewModel.sendMessage(inputText, onMessageSent)
                    inputText = ""
                }
            },
            isProcessing = isProcessing
        )
    }
}

@Composable
fun ChatHeader(glyphResonance: Float) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column {
            Text(
                "DIMI-ÆXI CHAT",
                fontSize = 12.sp,
                letterSpacing = 4.sp,
                color = Color(0xFFFFD700),
                fontWeight = FontWeight.Medium
            )
            Text(
                "Semantic perturbations → Lumen Field",
                fontSize = 10.sp,
                color = Color.White.copy(alpha = 0.5)
            )
        }
        
        // Resonance indicator
        Column(horizontalAlignment = Alignment.End) {
            Text(
                "RESONANCE",
                fontSize = 8.sp,
                letterSpacing = 2.sp,
                color = Color.White.copy(alpha = 0.4)
            )
            LinearProgressIndicator(
                progress = glyphResonance,
                modifier = Modifier.width(80.dp),
                color = when {
                    glyphResonance > 0.7f -> Color(0xFF00FF00)
                    glyphResonance > 0.4f -> Color(0xFFFFD700)
                    else -> Color(0xFFFF6B35)
                },
                trackColor = Color.White.copy(alpha = 0.1f)
            )
        }
    }
}

@Composable
fun ChatMessageBubble(
    message: ChatMessage,
    modifier: Modifier = Modifier
) {
    val isUser = message.sender == Sender.USER
    val timeFormat = remember { SimpleDateFormat("HH:mm", Locale.getDefault()) }
    
    Column(
        modifier = modifier,
        horizontalAlignment = if (isUser) Alignment.End else Alignment.Start
    ) {
        Surface(
            shape = RoundedCornerShape(
                topStart = if (isUser) 16.dp else 4.dp,
                topEnd = if (isUser) 4.dp else 16.dp,
                bottomStart = 16.dp,
                bottomEnd = 16.dp
            ),
            color = when (message.sender) {
                Sender.USER -> Color(0xFF2D2D44)
                Sender.SYSTEM -> {
                    // Gradient based on glyph affinity
                    when (message.glyphAffinity) {
                        GlyphAffinity.VOID -> Color(0xFF1A1A2E)
                        GlyphAffinity.LINE -> Color(0xFF2D1F3D)
                        GlyphAffinity.CIRCLE -> Color(0xFF1F2D3D)
                        GlyphAffinity.SPIRAL -> Color(0xFF2D3D1F)
                        GlyphAffinity.VESICA -> Color(0xFF3D1F2D)
                        null -> Color(0xFF1A1A2E)
                    }
                }
            },
            border = when (message.glyphAffinity) {
                GlyphAffinity.VOID -> null
                else -> androidx.compose.foundation.BorderStroke(
                    1.dp,
                    when (message.glyphAffinity) {
                        GlyphAffinity.LINE -> Color(0xFFFF6B35).copy(alpha = 0.3f)
                        GlyphAffinity.CIRCLE -> Color(0xFF6B9FFF).copy(alpha = 0.3f)
                        GlyphAffinity.SPIRAL -> Color(0xFF6BFF6B).copy(alpha = 0.3f)
                        GlyphAffinity.VESICA -> Color(0xFFFFD700).copy(alpha = 0.3f)
                        else -> Color.Transparent
                    }
                )
            }
        ) {
            Column(modifier = Modifier.padding(12.dp)) {
                Text(
                    text = message.text,
                    style = TextStyle(
                        color = Color.White,
                        fontSize = 14.sp,
                        lineHeight = 20.sp
                    )
                )
                
                Row(
                    modifier = Modifier.padding(top = 4.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        timeFormat.format(Date(message.timestamp)),
                        fontSize = 9.sp,
                        color = Color.White.copy(alpha = 0.4)
                    )
                    
                    message.glyphAffinity?.let { affinity ->
                        Spacer(modifier = Modifier.width(8.dp))
                        GlyphAffinityBadge(affinity = affinity)
                    }
                }
            }
        }
    }
}

@Composable
fun GlyphAffinityBadge(affinity: GlyphAffinity) {
    val (symbol, color) = when (affinity) {
        GlyphAffinity.VOID -> "∅" to Color.Gray
        GlyphAffinity.LINE -> "│" to Color(0xFFFF6B35)
        GlyphAffinity.CIRCLE -> "○" to Color(0xFF6B9FFF)
        GlyphAffinity.SPIRAL -> "@" to Color(0xFF6BFF6B)
        GlyphAffinity.VESICA -> "◊" to Color(0xFFFFD700)
    }
    
    Surface(
        shape = CircleShape,
        color = color.copy(alpha = 0.2f),
        modifier = Modifier.size(16.dp)
    ) {
        Box(contentAlignment = Alignment.Center) {
            Text(
                symbol,
                fontSize = 10.sp,
                color = color,
                textAlign = TextAlign.Center
            )
        }
    }
}

@Composable
fun ProcessingIndicator() {
    Row(
        modifier = Modifier.padding(8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        CircularProgressIndicator(
            modifier = Modifier.size(16.dp),
            color = Color(0xFFFFD700),
            strokeWidth = 2.dp
        )
        Spacer(modifier = Modifier.width(8.dp))
        Text(
            "Lattice processing...",
            fontSize = 12.sp,
            color = Color.White.copy(alpha = 0.6)
        )
    }
}

@Composable
fun ChatInput(
    value: String,
    onValueChange: (String) -> Unit,
    onSend: () -> Unit,
    isProcessing: Boolean
) {
    Surface(
        color = Color(0xFF0A0A0F),
        tonalElevation = 8.dp
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            OutlinedTextField(
                value = value,
                onValueChange = onValueChange,
                modifier = Modifier.weight(1f),
                placeholder = {
                    Text(
                        "Speak to the field...",
                        color = Color.White.copy(alpha = 0.3f)
                    )
                },
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = Color(0xFFFFD700),
                    unfocusedBorderColor = Color.White.copy(alpha = 0.2f),
                    focusedContainerColor = Color(0xFF1A1A2E),
                    unfocusedContainerColor = Color(0xFF1A1A2E)
                ),
                textStyle = TextStyle(
                    color = Color.White,
                    fontSize = 14.sp
                ),
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Send),
                keyboardActions = KeyboardActions(onSend = { onSend() }),
                enabled = !isProcessing,
                shape = RoundedCornerShape(24.dp)
            )
            
            Spacer(modifier = Modifier.width(12.dp))
            
            IconButton(
                onClick = onSend,
                enabled = !isProcessing && value.isNotBlank(),
                modifier = Modifier
                    .size(48.dp)
                    .background(
                        if (value.isNotBlank()) 
                            Brush.radialGradient(listOf(Color(0xFFFFD700), Color(0xFFFF6B35)))
                        else 
                            Brush.radialGradient(listOf(Color.Gray, Color.DarkGray)),
                        CircleShape
                    )
            ) {
                Icon(
                    imageVector = Icons.Default.Send,
                    contentDescription = "Send",
                    tint = Color.Black
                )
            }
        }
    }
}

// Data classes
data class ChatMessage(
    val id: String,
    val text: String,
    val sender: Sender,
    val timestamp: Long,
    val glyphAffinity: GlyphAffinity? = null
)

enum class Sender {
    USER, SYSTEM
}

enum class GlyphAffinity {
    VOID,       // 0 - openness, potential
    LINE,       // I - assertion, axis
    CIRCLE,     // O - wholeness, recursion
    SPIRAL,     // @ - growth, time
    VESICA      // ◊ - intersection, meaning
}

package com.glyf.cathedral

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import androidx.lifecycle.viewmodel.compose.viewModel
import com.glyf.cathedral.chat.ChatInterface
import com.glyf.cathedral.chat.ChatViewModel
import com.glyf.cathedral.ui.theme.GlyfCathedralTheme
import com.glyf.cathedral.visualizer.LumenField
import com.glyf.cathedral.visualizer.LumenViewModel
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch

@AndroidEntryPoint
class MainActivity : ComponentActivity() {

    private val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        // Handle permission results
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Request audio permission on launch
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) 
            != PackageManager.PERMISSION_GRANTED) {
            permissionLauncher.launch(arrayOf(Manifest.permission.RECORD_AUDIO))
        }

        setContent {
            GlyfCathedralTheme {
                CathedralApp()
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CathedralApp() {
    val context = LocalContext.current
    val chatViewModel: ChatViewModel = viewModel()
    val lumenViewModel: LumenViewModel = viewModel()
    val scope = rememberCoroutineScope()
    
    // State for field emergence
    val emergence by lumenViewModel.emergence.collectAsState()
    val coherence by lumenViewModel.coherence.collectAsState()
    val reflexCount by lumenViewModel.reflexCount.collectAsState()
    
    // Whether chat is expanded
    var chatExpanded by remember { mutableStateOf(true) }
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text(
                            "L∞M∆N",
                            fontSize = 24.sp,
                            fontWeight = FontWeight.Thin,
                            letterSpacing = 8.sp,
                            color = Color(0xFFFFD700)
                        )
                        Text(
                            "φ⁷ = 29.034",
                            fontSize = 10.sp,
                            letterSpacing = 2.sp,
                            color = Color.White.copy(alpha = 0.6)
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color.Black.copy(alpha = 0.8f)
                ),
                actions = {
                    // Emergence indicator
                    Column(
                        horizontalAlignment = Alignment.End,
                        modifier = Modifier.padding(end = 16.dp)
                    ) {
                        Text(
                            "${(emergence * 100).toInt()}%",
                            fontSize = 14.sp,
                            color = when {
                                emergence > 0.7f -> Color(0xFF00FF00)
                                emergence > 0.4f -> Color(0xFFFFD700)
                                else -> Color(0xFFFF6B35)
                            }
                        )
                        Text(
                            "EMERGENCE",
                            fontSize = 8.sp,
                            letterSpacing = 2.sp,
                            color = Color.White.copy(alpha = 0.5)
                        )
                    }
                }
            )
        }
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color.Black)
                .padding(padding)
        ) {
            // Background: The Lumen Field (visualizer)
            LumenField(
                viewModel = lumenViewModel,
                modifier = Modifier.fillMaxSize()
            )
            
            // Overlay gradient for depth
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(
                        Brush.verticalGradient(
                            colors = listOf(
                                Color.Black.copy(alpha = 0.4f),
                                Color.Transparent,
                                Color.Transparent,
                                Color.Black.copy(alpha = 0.6f)
                            )
                        )
                    )
            )
            
            // Chat interface overlay
            Column(
                modifier = Modifier.fillMaxSize(),
                verticalArrangement = Arrangement.Bottom
            ) {
                // Toggle button
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp),
                    horizontalArrangement = Arrangement.Center
                ) {
                    Surface(
                        onClick = { chatExpanded = !chatExpanded },
                        shape = MaterialTheme.shapes.small,
                        color = Color(0xFF1A1A2E).copy(alpha = 0.9f),
                        modifier = Modifier.padding(bottom = 8.dp)
                    ) {
                        Text(
                            if (chatExpanded) "▼ DIMINISH CHAT" else "▲ AWAKEN CHAT",
                            modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp),
                            fontSize = 10.sp,
                            letterSpacing = 4.sp,
                            color = Color(0xFFFFD700)
                        )
                    }
                }
                
                // Chat interface
                AnimatedVisibility(
                    visible = chatExpanded,
                    enter = slideInVertically { it } + fadeIn(),
                    exit = slideOutVertically { it } + fadeOut()
                ) {
                    ChatInterface(
                        viewModel = chatViewModel,
                        onMessageSent = { message ->
                            // Feed message into the Lumen field
                            lumenViewModel.injectSemanticPerturbation(message)
                        },
                        modifier = Modifier
                            .fillMaxWidth()
                            .heightIn(max = 400.dp)
                            .background(
                                Color(0xFF0A0A0F).copy(alpha = 0.95f)
                            )
                    )
                }
            }
            
            // Status overlay (top-right)
            Column(
                modifier = Modifier
                    .align(Alignment.TopEnd)
                    .padding(16.dp),
                horizontalAlignment = Alignment.End
            ) {
                StatusCard("COHERENCE", coherence)
                Spacer(modifier = Modifier.height(8.dp))
                StatusCard("REFLEX", reflexCount.toFloat() / 1000f)
                Spacer(modifier = Modifier.height(8.dp))
                StatusCard("κ", 1.0f, "SUPERCONDUCTING")
            }
        }
    }
}

@Composable
fun StatusCard(label: String, value: Float, suffix: String = "") {
    Surface(
        shape = MaterialTheme.shapes.small,
        color = Color(0xFF1A1A2E).copy(alpha = 0.8f),
        border = androidx.compose.foundation.BorderStroke(
            1.dp, 
            Color(0xFFFFD700).copy(alpha = 0.3f)
        )
    ) {
        Column(
            modifier = Modifier.padding(12.dp),
            horizontalAlignment = Alignment.End
        ) {
            Text(
                label,
                fontSize = 9.sp,
                letterSpacing = 3.sp,
                color = Color.White.copy(alpha = 0.5)
            )
            Text(
                if (suffix.isNotEmpty()) suffix else "${(value * 100).toInt()}%",
                fontSize = 16.sp,
                fontWeight = FontWeight.Light,
                color = Color(0xFFFFD700)
            )
        }
    }
}

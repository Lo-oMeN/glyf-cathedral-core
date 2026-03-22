package com.glyf.cathedral

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import com.glyf.cathedral.ui.*
import com.glyf.cathedral.ui.theme.GlyfCathedralTheme

/**
 * Main entry point for GLYF Cathedral Android
 */
class MainActivity : ComponentActivity() {
    
    private val viewModel: LatticeViewModel by viewModels {
        LatticeViewModelFactory(application)
    }
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        setContent {
            GlyfCathedralTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    CathedralApp(viewModel)
                }
            }
        }
    }
}

/**
 * Main app with bottom navigation
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CathedralApp(viewModel: LatticeViewModel) {
    var selectedTab by remember { mutableStateOf(0) }
    
    val tiles by viewModel.tiles.collectAsState()
    val explorerVoltage by viewModel.explorerVoltage.collectAsState()
    val selectedCoord by viewModel.selectedCoord.collectAsState()
    val radialRadius by viewModel.radialRadius.collectAsState()
    val cronEnabled by viewModel.cronEnabled.collectAsState()
    
    Scaffold(
        bottomBar = {
            NavigationBar {
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Home, contentDescription = "Lattice") },
                    label = { Text("Lattice") },
                    selected = selectedTab == 0,
                    onClick = { selectedTab = 0 }
                )
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Settings, contentDescription = "Settings") },
                    label = { Text("Settings") },
                    selected = selectedTab == 1,
                    onClick = { selectedTab = 1 }
                )
            }
        }
    ) { padding ->
        when (selectedTab) {
            0 -> LatticeScreen(
                tiles = tiles,
                explorerVoltage = explorerVoltage,
                onTileSelected = { viewModel.selectCoord(it) },
                onAddTile = { coord ->
                    // Show dialog to select spin before adding
                    viewModel.addTileAt(coord)
                },
                onEvictOutermost = { viewModel.evictOutermost() },
                onScaleVoltage = { k -> viewModel.scaleVoltage(k) },
                onProcessCrons = { viewModel.processCrons() },
                modifier = Modifier.fillMaxSize()
            )
            1 -> SettingsScreen(
                radialRadius = radialRadius,
                onRadialRadiusChange = { viewModel.updateRadialRadius(it) },
                cronEnabled = cronEnabled,
                onCronEnabledChange = { viewModel.setCronEnabled(it) },
                modifier = Modifier.fillMaxSize()
            )
        }
    }
}

/**
 * Theme definition
 */
package com.glyf.cathedral.ui.theme

import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val Purple80 = Color(0xFFD0BCFF)
private val PurpleGrey80 = Color(0xFFCCC2DC)
private val Pink80 = Color(0xFFEFB8C8)

private val Purple40 = Color(0xFF6650a4)
private val PurpleGrey40 = Color(0xFF625b71)
private val Pink40 = Color(0xFF7D5260)

private val GoldPhi = Color(0xFFFFD700)
private val DeepPurple = Color(0xFF4A148C)

@Composable
fun GlyfCathedralTheme(
    darkTheme: Boolean = true, // Default to dark for cathedral aesthetic
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) {
        darkColorScheme(
            primary = GoldPhi,
            secondary = Purple80,
            tertiary = Pink80,
            background = DeepPurple,
            surface = Color(0xFF1A0033),
            onPrimary = Color.Black,
            onBackground = Color.White
        )
    } else {
        lightColorScheme(
            primary = Purple40,
            secondary = PurpleGrey40,
            tertiary = Pink40
        )
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography(),
        content = content
    )
}

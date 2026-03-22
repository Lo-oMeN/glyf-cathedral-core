package com.glyf.cathedral.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.glyf.cathedral.core.*
import com.glyf.cathedral.ui.visualization.HexLatticeView

/**
 * Main lattice screen with controls
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LatticeScreen(
    tiles: List<HexTile>,
    explorerVoltage: Float,
    onTileSelected: (AxialCoord) -> Unit,
    onAddTile: (AxialCoord) -> Unit,
    onEvictOutermost: () -> Unit,
    onScaleVoltage: (Int) -> Unit,
    onProcessCrons: () -> Unit,
    modifier: Modifier = Modifier
) {
    var selectedCoord by remember { mutableStateOf<AxialCoord?>(null) }
    var showVesica by remember { mutableStateOf(false) }
    var showSpiral by remember { mutableStateOf(true) }
    var hexSize by remember { mutableStateOf(50f) }
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("GLYF Cathedral φ⁷") },
                actions = {
                    IconButton(onClick = { showVesica = !showVesica }) {
                        Icon(
                            imageVector = if (showVesica) Icons.Default.Visibility else Icons.Default.VisibilityOff,
                            contentDescription = "Toggle Vesica"
                        )
                    }
                    IconButton(onClick = { showSpiral = !showSpiral }) {
                        Icon(
                            imageVector = if (showSpiral) Icons.Default.Refresh else Icons.Default.Add,
                            contentDescription = "Toggle Spiral"
                        )
                    }
                }
            )
        },
        floatingActionButton = {
            Column {
                SmallFloatingActionButton(
                    onClick = { hexSize = (hexSize * 1.2f).coerceAtMost(100f) }
                ) {
                    Icon(Icons.Default.Add, "Zoom In")
                }
                Spacer(modifier = Modifier.height(8.dp))
                SmallFloatingActionButton(
                    onClick = { hexSize = (hexSize / 1.2f).coerceAtLeast(20f) }
                ) {
                    Icon(Icons.Default.Remove, "Zoom Out")
                }
                Spacer(modifier = Modifier.height(8.dp))
                FloatingActionButton(onClick = onEvictOutermost) {
                    Icon(Icons.Default.Delete, "Evict Outermost")
                }
            }
        }
    ) { padding ->
        Column(
            modifier = modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            // Status bar
            StatusBar(
                tileCount = tiles.size,
                explorerVoltage = explorerVoltage,
                selectedCoord = selectedCoord,
                modifier = Modifier.fillMaxWidth()
            )
            
            // Hex lattice visualization
            HexLatticeView(
                tiles = tiles,
                selectedCoord = selectedCoord,
                onTileSelected = { coord ->
                    selectedCoord = coord
                    onTileSelected(coord)
                },
                onEmptySpaceSelected = { offset ->
                    // Convert offset to coord and add tile
                    // Simplified for demo
                },
                modifier = Modifier.weight(1f),
                hexSize = hexSize,
                showVesica = showVesica,
                goldenSpiral = showSpiral
            )
            
            // Control panel
            ControlPanel(
                onScaleUp = { onScaleVoltage(1) },
                onScaleDown = { onScaleVoltage(-1) },
                onProcessCrons = onProcessCrons,
                modifier = Modifier.fillMaxWidth()
            )
        }
    }
}

@Composable
private fun StatusBar(
    tileCount: Int,
    explorerVoltage: Float,
    selectedCoord: AxialCoord?,
    modifier: Modifier = Modifier
) {
    Surface(
        modifier = modifier,
        tonalElevation = 2.dp
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Column {
                Text("Tiles: $tileCount / 1024", style = MaterialTheme.typography.bodyMedium)
                LinearProgressIndicator(
                    progress = tileCount / 1024f,
                    modifier = Modifier.width(100.dp)
                )
            }
            
            Column(horizontalAlignment = androidx.compose.ui.Alignment.CenterHorizontally) {
                Text("φ Voltage", style = MaterialTheme.typography.labelSmall)
                Text(
                    "%.2f".format(explorerVoltage),
                    style = MaterialTheme.typography.titleMedium
                )
            }
            
            Column(horizontalAlignment = androidx.compose.ui.Alignment.End) {
                Text("Selected:", style = MaterialTheme.typography.labelSmall)
                Text(
                    selectedCoord?.let { "${it.q},${it.r},${it.s}" } ?: "None",
                    style = MaterialTheme.typography.bodyMedium
                )
            }
        }
    }
}

@Composable
private fun ControlPanel(
    onScaleUp: () -> Unit,
    onScaleDown: () -> Unit,
    onProcessCrons: () -> Unit,
    modifier: Modifier = Modifier
) {
    Surface(
        modifier = modifier,
        tonalElevation = 4.dp
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            Button(onClick = onScaleUp) {
                Icon(Icons.Default.KeyboardArrowUp, null)
                Spacer(Modifier.width(4.dp))
                Text("Scale φ")
            }
            
            Button(onClick = onScaleDown) {
                Icon(Icons.Default.KeyboardArrowDown, null)
                Spacer(Modifier.width(4.dp))
                Text("Scale φ⁻¹")
            }
            
            Button(onClick = onProcessCrons) {
                Icon(Icons.Default.Notifications, null)
                Spacer(Modifier.width(4.dp))
                Text("Process Crons")
            }
        }
    }
}

/**
 * Settings screen
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    radialRadius: Int,
    onRadialRadiusChange: (Int) -> Unit,
    cronEnabled: Boolean,
    onCronEnabledChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Settings") })
        }
    ) { padding ->
        Column(
            modifier = modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp)
        ) {
            // Radial radius setting
            ListItem(
                headlineContent = { Text("Radial Query Radius") },
                supportingContent = { Text("Maximum distance for lattice queries") },
                trailingContent = {
                    Text("$radialRadius", style = MaterialTheme.typography.titleMedium)
                }
            )
            
            Slider(
                value = radialRadius.toFloat(),
                onValueChange = { onRadialRadiusChange(it.toInt()) },
                valueRange = 5f..50f,
                steps = 44
            )
            
            Divider(modifier = Modifier.padding(vertical = 16.dp))
            
            // Cron toggle
            ListItem(
                headlineContent = { Text("Fibonacci Cron") },
                supportingContent = { Text("Periodic lattice persistence (13-min intervals)") },
                trailingContent = {
                    Switch(
                        checked = cronEnabled,
                        onCheckedChange = onCronEnabledChange
                    )
                }
            )
            
            Divider(modifier = Modifier.padding(vertical = 16.dp))
            
            // About
            ListItem(
                headlineContent = { Text("GLYF Cathedral") },
                supportingContent = { Text("Version 0.7.2 φ⁷") }
            )
        }
    }
}

package com.glyf.cathedral.ui.theme

import android.app.Activity
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

/**
 * L∞M∆N Cathedral Theme
 * Dark, gold-accented, sacred geometry inspired
 */

private val DarkColorScheme = darkColorScheme(
    primary = Color(0xFFFFD700),           // Gold
    onPrimary = Color.Black,
    primaryContainer = Color(0xFF3D2D00),
    onPrimaryContainer = Color(0xFFFFE080),
    
    secondary = Color(0xFFFF6B35),         // Amber/Orange
    onSecondary = Color.Black,
    secondaryContainer = Color(0xFF3D1F00),
    onSecondaryContainer = Color(0xFFFFA080),
    
    tertiary = Color(0xFF6B9FFF),          // Soft Blue
    onTertiary = Color.Black,
    tertiaryContainer = Color(0xFF001F3D),
    onTertiaryContainer = Color(0xFFB0D0FF),
    
    background = Color(0xFF050508),        // Deep space
    onBackground = Color(0xFFE0E0E0),
    
    surface = Color(0xFF0A0A0F),           // Slightly lighter
    onSurface = Color(0xFFE0E0E0),
    surfaceVariant = Color(0xFF1A1A2E),
    onSurfaceVariant = Color(0xFFB0B0C0),
    
    error = Color(0xFFFF4444),
    onError = Color.Black,
    errorContainer = Color(0xFF3D0000),
    onErrorContainer = Color(0xFFFF8888),
    
    outline = Color(0xFF4A4A5A),
    outlineVariant = Color(0xFF2A2A3A),
    
    scrim = Color.Black.copy(alpha = 0.8f),
    
    inverseSurface = Color(0xFFE0E0E0),
    inverseOnSurface = Color(0xFF050508),
    inversePrimary = Color(0xFFB08D00),
    
    surfaceTint = Color(0xFFFFD700)
)

@Composable
fun GlyfCathedralTheme(
    darkTheme: Boolean = true, // Always dark
    content: @Composable () -> Unit
) {
    val colorScheme = DarkColorScheme
    val view = LocalView.current
    
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as Activity).window
            window.statusBarColor = colorScheme.background.toArgb()
            window.navigationBarColor = colorScheme.background.toArgb()
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = false
            WindowCompat.getInsetsController(window, view).isAppearanceLightNavigationBars = false
        }
    }
    
    MaterialTheme(
        colorScheme = colorScheme,
        typography = CathedralTypography,
        content = content
    )
}

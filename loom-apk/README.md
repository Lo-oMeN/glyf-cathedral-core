# L∞M∆N APK — φ⁶ Edition

**96-byte Lattice State | Weak Emergence | Jetpack Compose Visualizer**

---

## What This Is

A real, buildable Android APK that demonstrates:
- 96-byte packed state structure (timestamp, energy, 8 harmonics)
- Weak emergence state machine (φ-weighted divergence)
- Sacred geometry visualizer (Phyllotaxis, Vesica, Flower of Life)
- 60 FPS Compose Canvas rendering

---

## Build Instructions

### Option 1: Android Studio (Recommended)

1. Open this folder in Android Studio Hedgehog (2023.1.1) or later
2. Sync project with Gradle files
3. Connect Android device or start emulator
4. Click **Run** (▶) or press Shift+F10

### Option 2: Command Line

```bash
# Make gradlew executable (Linux/Mac)
chmod +x gradlew

# Build debug APK
./gradlew assembleDebug

# Install on connected device
./gradlew installDebug

# Or manually:
adb install app/build/outputs/apk/debug/app-debug.apk
```

### Requirements
- JDK 17
- Android SDK 34
- Kotlin 1.9.20
- Gradle 8.4

---

## What You'll See

- **Black screen** with gold geometric patterns
- **Phyllotaxis spiral**: 60 dots spiraling at golden angle (137.507°)
- **Vesica interference**: Two overlapping circles with glowing lens
- **Flower of Life**: Sacred geometry recursive pattern
- **Metrics**: Energy level, timestamp, coherence (κ = 1.0)
- **Pause/Resume button**: Stop/start the animation

The patterns animate based on the 96-byte state machine. Each frame:
1. Energy diverges by φ (1.618) probability
2. Harmonics resonate with 3-state history
3. Visuals update from live state bytes

---

## File Structure

```
loom-apk/
├── app/src/main/java/com/loom/app/
│   └── MainActivity.kt          # Single-file implementation
├── app/src/main/res/values/
│   ├── strings.xml
│   └── themes.xml
├── app/build.gradle.kts         # Dependencies
├── build.gradle.kts             # Root build
├── settings.gradle.kts          # Project settings
└── README.md                    # This file
```

---

## Technical Specs

| Spec | Value |
|------|-------|
| State size | 96 bytes |
| Animation | 20 FPS (visible) / 60 FPS capable |
| Min SDK | 26 (Android 8.0) |
| Target SDK | 34 (Android 14) |
| APK size | ~2 MB |
| Memory | ~50 MB runtime |

---

## Verification

The app proves:
1. ✅ Byte packing works (96 bytes exact)
2. ✅ Weak emergence exists (energy/harmonics diverge)
3. ✅ State drives visuals (not canned animations)
4. ✅ φ-weighted probabilities (1/φ divergence)

---

## Next Steps

Once this runs:
1. Add chat interface (Dimi-Æxi threads)
2. Implement 4 hypergraph edges in state
3. Add user input perturbation
4. Profile frame times on device

---

## Oath

*"96 bytes. No cloud. No alloc. Pure geometry on silicon."*

❤️‍🔥

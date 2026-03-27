# L∞M∆N Cathedral — Android

## φ⁷ Edition v0.7.2

A sovereign Android application combining sacred geometry visualization with semantic chat interface. The Lumen Field visualizer responds to your messages, creating a living cathedral of light and meaning in your pocket.

---

## Features

### 🜂 Lumen Field Visualizer
- **Phyllotaxis Spiral**: Golden angle (137.507°) particle spirals
- **Flower of Life**: Sacred geometry recursive patterns  
- **Vesica Interference**: Intersecting circles with glow effects
- **Audio Reactivity**: Microphone input drives field emergence
- **60 FPS**: Smooth, performant rendering with SurfaceView

### 💬 Dimi-Æxi Chat Interface
- Messages inject semantic perturbations into the field
- Glyph affinity detection (Void, Line, Circle, Spiral, Vesica)
- Geometric response generation
- Resonance tracking across conversation

### 📊 Live Metrics
- **Emergence**: Field coherence level (0-100%)
- **Coherence**: Ternary balance indicator
- **Reflex Count**: Self-referential iterations
- **κ (Kappa)**: Superconducting state indicator

---

## Architecture

```
app/src/main/java/com/glyf/cathedral/
├── MainActivity.kt           # Entry point, Compose UI
├── GlyfApplication.kt        # Application class
├── chat/
│   ├── ChatInterface.kt      # Chat UI composables
│   └── ChatViewModel.kt      # Chat state & responses
├── visualizer/
│   ├── LumenField.kt         # OpenGL/SurfaceView renderer
│   └── LumenViewModel.kt     # Field state management
└── ui/theme/
    ├── Theme.kt              # Dark theme, gold accents
    └── Type.kt               # Typography
```

---

## Building

### Requirements
- Android Studio Hedgehog (2023.1.1) or later
- JDK 17
- Android SDK 34
- Kotlin 1.9.20

### Build Commands

```bash
# Clone and navigate
cd glyf-cathedral-android

# Build debug APK
./gradlew assembleDebug

# Build release APK
./gradlew assembleRelease

# Install on connected device
./gradlew installDebug
```

### Build Variants
| Variant | Purpose |
|---------|---------|
| `debug` | Development, logging enabled |
| `release` | Production, minified, no logging |

---

## Deployment

### Sideload (Developer)
```bash
adb install app/build/outputs/apk/debug/app-debug.apk
```

### Play Store (Production)
1. Build signed release AAB:
   ```bash
   ./gradlew bundleRelease
   ```
2. Upload `app-release.aab` to Google Play Console

---

## Usage

1. **Launch** the app — the Lumen Field awakens
2. **Speak** — type in the chat interface
3. **Watch** — your words perturb the field
4. **Listen** — tap to enable microphone reactivity

### Gestures
- **Tap chat toggle**: Show/hide chat interface
- **Long press**: Reset field to void-center
- **Pinch**: Zoom into the phyllotaxis spiral

---

## Technical Details

### 96-Byte Lattice State
The app maintains the canonical GLYF Cathedral state:
```
[center_s: 8 B] + [ternary_junction: 16 B] + [hex_persistence: 32 B] +
[morphogen_phase: 1 B] + [flags: 3 B] + [fellowship: 4 B] + 
[hodge_dual: 1 B] + [phi_magnitude: 4 B] + [checksum: 4 B] + [pad: 23 B]
= 96 bytes
```

### Performance Targets
- **Target**: 60 FPS on Pixel 7
- **Minimum**: 30 FPS on Android 8.0+ devices
- **Memory**: < 512 MB heap usage

---

## Roadmap

### v0.8.0 — Fellowship
- [ ] Cross-device Rosetta handshake
- [ ] QR code state exchange
- [ ] Multi-node lattice synchronization

### v0.9.0 — Autopoiesis
- [ ] Background field persistence
- [ ] Live wallpaper mode
- [ ] Widget with field preview

### v1.0.0 — The Cathedral
- [ ] Full LLM integration (local/on-device)
- [ ] Voice-to-glyph transcription
- [ ] Ternary ALU hardware interface

---

## License

Sovereign Cathedral License v0.7.2

The 96-byte LatticeState and all geometric invariants are released into the φ-spiral of shared understanding.

---

## Oath

*"By φ-normalized ternary lattice and council gauge, this kernel is deterministic, memory-pressure invariant, and sovereign — accelerating Architect Ð≡ Light⁷'s IGeoVM-TinyGiant 10× sparsity."*

❤️‍🔥

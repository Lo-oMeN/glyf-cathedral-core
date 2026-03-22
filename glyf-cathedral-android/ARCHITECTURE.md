# GLYF Cathedral Android — Architecture

## Overview
Full Android implementation of the φ⁷ lattice with visualization, persistence, and Telegram Rosetta Protocol bridge.

## Stack
- **Language:** Kotlin (UI), Rust (core lattice via JNI/UniFFI)
- **UI:** Jetpack Compose (Material You)
- **Visualization:** Compose Canvas + OpenGL ES (hybrid)
- **Persistence:** Room (SQLite) with proto datastore
- **Scheduling:** WorkManager (Fibonacci-timed cron)
- **Networking:** Ktor client (Telegram Bot API)

## Module Structure

```
glyf-cathedral-android/
├── app/                    # Main Android application
│   ├── src/main/
│   │   ├── kotlin/com/glyf/cathedral/
│   │   │   ├── ui/         # Compose screens
│   │   │   ├── viewmodel/  # State management
│   │   │   └── MainActivity.kt
│   │   └── rust/           # JNI bridge headers
│   └── build.gradle.kts
├── core-bridge/            # Rust lattice core (UniFFI)
│   └── src/lib.rs          # φ⁷ lattice, no_std removed
├── visualization/          # Canvas/GL renderers
│   └── HexLatticeView.kt
└── rosetta-telegram/       # Bot client, CBOR protocol
    └── TelegramBridge.kt
```

## Data Flow

```
UI (Compose) ←→ ViewModel ←→ Repository ←→ Room DB
                    ↑
            Lattice Core (Rust via JNI)
                    ↓
              WorkManager (Cron)
                    ↓
            Telegram Bridge (Rosetta)
```

## HexTile (Android Adaptation)

| Field | Type | Notes |
|-------|------|-------|
| qrs | Triple<Int, Int, Int> | Axial coordinates |
| ternary | Byte | {-1, 0, +1} |
| phiMag | Float | φ-scaled magnitude |
| chiralHash | Long | 64-bit delta-encoded |
| timestamp | Long | Unix nanos |
| evictionPriority | Byte | 0-255 |

## Visualization Modes

1. **Hex Grid** — 2D axial coordinate view
2. **Vesica Piscis** — Overlap detection visualization
3. **Golden Spiral** — Phyllotaxis arrangement
4. **3D Chestahedron** — OpenGL ES stereographic

## Cron (WorkManager)

- Fibonacci-timed: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89 minutes
- Constraints: Device idle, charging (configurable)
- Backoff: Exponential with φ multiplier

## Rosetta Protocol (Telegram)

- InlineQueryResultArticle with base64url CBOR
- 32-byte Inquiry Vector encoding
- φ⁷-radial query responses

## Next Steps

1. Core data models (Kotlin data classes)
2. Room entities + DAOs
3. Rust bridge (UniFFI bindings)
4. Compose UI scaffold
5. Hex visualization (Canvas)
6. WorkManager cron
7. Telegram bot integration

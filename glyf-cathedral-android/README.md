# GLYF Cathedral Android

Full Android implementation of the φ⁷ lattice with visualization, persistence, and Telegram Rosetta Protocol bridge.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        UI Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ LatticeScreen│  │SettingsScreen│  │HexLatticeView   │   │
│  └──────┬───────┘  └──────┬───────┘  └─────────────────┘   │
└─────────┼─────────────────┼─────────────────────────────────┘
          │                 │
          ▼                 ▼
┌─────────────────────────────────────────────────────────────┐
│                     ViewModel Layer                         │
│                 LatticeViewModel                            │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
┌─────────────────┐ ┌──────────┐ ┌───────────────┐
│ Repository Layer│ │ Cron     │ │ Rosetta       │
│ LatticeRepository│ │ Workers  │ │ Telegram      │
└────────┬────────┘ └──────────┘ └───────────────┘
         │
┌────────▼──────────────────────────────────────────────┐
│                   Data Layer                          │
│  ┌──────────────┐  ┌───────────┐  ┌──────────────┐   │
│  │ Room (SQLite)│  │ DataStore │  │ 68 KiB Limit │   │
│  └──────────────┘  └───────────┘  └──────────────┘   │
└───────────────────────────────────────────────────────┘
```

## Features

### Core Lattice (φ⁷)
- **HexTile**: 64-byte conceptual model (relaxed alignment for Android)
- **AxialCoord**: Hexagonal grid coordinates (q, r, s)
- **TernarySpin**: -1, 0, +1 spin states
- **ChiralHash**: Delta-encoded 64-bit hash
- **Eviction**: Priority-based outer-first eviction

### Visualization
- **Hex Grid**: 2D pointy-topped hexagons
- **Golden Spiral**: Phyllotaxis background pattern
- **Vesica Piscis**: Overlap detection visualization
- **Interactive**: Tap to select, pinch to zoom

### Persistence
- **Room Database**: SQLite with type-safe DAOs
- **68 KiB Soft Limit**: 1024 HexTiles + 64 CronTiles
- **Outer-First Eviction**: Priority-based SDMMC simulation

### Cron (WorkManager)
- **Fibonacci Intervals**: 1, 1, 2, 3, 5, 8, 13... minutes
- **Voltage Thresholds**: φ-scaled trigger conditions
- **Boot Persistence**: Rescheduled after reboot

### Rosetta Protocol
- **CBOR Encoding**: 32-byte Inquiry Vectors
- **base64url**: Telegram-compatible encoding
- **Radial Queries**: φ⁷-radial lattice search

## Project Structure

```
glyf-cathedral-android/
├── app/src/main/kotlin/com/glyf/cathedral/
│   ├── core/                    # Data models
│   │   ├── Models.kt            # HexTile, AxialCoord, etc.
│   ├── data/                    # Persistence layer
│   │   ├── Entities.kt          # Room entities
│   │   ├── LatticeRepository.kt # Repository pattern
│   ├── ui/                      # Jetpack Compose UI
│   │   ├── LatticeScreens.kt    # Main screens
│   │   ├── LatticeViewModel.kt  # State management
│   │   └── visualization/
│   │       └── HexLatticeView.kt # Canvas rendering
│   ├── cron/                    # WorkManager workers
│   │   ├── LatticeWorkers.kt    # Cron workers
│   │   └── CronInfrastructure.kt
│   ├── rosetta/                 # Telegram bridge
│   │   └── RosettaTelegramBridge.kt
│   ├── MainActivity.kt          # Entry point
│   └── CathedralApplication.kt  # App class
└── build.gradle.kts             # Dependencies
```

## Build

```bash
# Clone and build
cd glyf-cathedral-android
./gradlew assembleDebug

# Install on device
./gradlew installDebug
```

## Usage

1. **Launch**: App opens to hex lattice visualization
2. **Tap**: Select tiles (shows coordinates)
3. **Add**: Long-press empty space to add tiles
4. **Evict**: FAB removes outermost tile
5. **Scale**: Buttons adjust φ voltage
6. **Cron**: Settings → enable Fibonacci scheduling

## Configuration

```kotlin
// Default lattice parameters
val radialRadius = 21      // φ⁷ / φ⁴ ≈ 21
val cronFibBase = 13       // Default τ = 13 minutes
val maxHotTiles = 1024     // 64 KiB limit
```

## Roadmap

- [ ] Phase 2: Geometric attention operators
- [ ] Phase 3: CBOR + Telegram full integration
- [ ] Phase 4: 72-hour stress test harness
- [ ] OpenGL ES: 3D chestahedron visualization
- [ ] Swarm sync: Multi-device lattice merge

## License

MIT — φ⁷ Sovereign Lattice Fellowship

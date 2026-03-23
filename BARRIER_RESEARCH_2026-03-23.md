# BARRIER RESEARCH — GLYF Cathedral Solutions

**Date:** 2026-03-23  
**Researcher:** Kimi Claw  
**Status:** Active Investigation

---

## Blocker 1: Pi Zero Hardware (No Device)

### Current Status
No physical Pi Zero 2 W for hardware testing.

### Solution Paths

#### Option A: Hardware Acquisition (Recommended)
**rpilocator.com** — Real-time stock tracker for Raspberry Pi
- Tracks 40+ approved resellers worldwide
- RSS feed for automated alerts: `rpilocator.com/feed/`
- Twitter/X: @rpilocator
- Telegram: @raspberry_alert

**Alternative Suppliers:**
- **PiShop.us** (US) — Authorized reseller
- **The Pi Hut** (UK) — Strong stock position
- **CanaKit** (US) — Bundles available

**Price Reality Check:**
- Pi Zero 2 W MSRP: ~$15
- Current market: $20-40 (post-shortage)
- Stock status: Improving but still constrained

#### Option B: Emulation Layer (Immediate)
**QEMU ARM emulation** for development without hardware:
```bash
# Install qemu-system-arm
sudo apt-get install qemu-system-arm

# Download Pi Zero 2 W kernel + DTB
wget https://github.com/dhruvvyas90/qemu-rpi-kernel/raw/master/kernel-qemu-5.4.51-buster
wget https://github.com/dhruvvyas90/qemu-rpi-kernel/raw/master/versatile-pb.dtb

# Run emulation
qemu-system-arm \
  -kernel kernel-qemu-5.4.51-buster \
  -cpu arm1176 \
  -m 512 \
  -M versatilepb \
  -dtb versatile-pb.dtb \
  -no-reboot \
  -append "root=/dev/sda2 panic=1"
```

**Pros:** Zero hardware cost, CI/CD compatible  
**Cons:** Not cycle-accurate, SD card timing differs

#### Option C: Alternative Boards
If Pi Zero 2 W unavailable, compatible alternatives:

| Board | CPU | RAM | Cost | Compatibility |
|-------|-----|-----|------|---------------|
| **Orange Pi Zero** | H2+ quad-core | 512MB | $15 | ARMv7, similar perf |
| **Banana Pi M2 Zero** | H2+ quad-core | 512MB | $18 | Pi Zero form factor |
| **Radxa Zero** | RK3308 quad-core | 512MB-4GB | $15-45 | ARMv8, more RAM |

**Recommendation:** Acquire Pi Zero 2 W via rpilocator alerts + implement QEMU fallback for CI.

---

## Blocker 2: Embassy Async Runtime

### Current Status
Undecided on async runtime for embedded Rust.

### Research Findings

#### Option A: Embassy (Still Leading)
**Pros:**
- Mature ecosystem, active development
- `embassy-time`, `embassy-sync` well-tested
- Built-in executor optimized for Cortex-M

**Cons:**
- Learning curve
- Some APIs still evolving

**Critical Insight:**  
Embassy works WITH other crates — not locked in:
```rust
// Can use Embassy HAL with RTIC executor
use embassy_stm32 as hal;
use rtic::app;
```

#### Option B: RTIC v2 (Alternative)
**Real-Time Interrupt-driven Concurrency**

**Pros:**
- SRP (Stack Resource Policy) locks — deadlock free
- Zero-cost abstraction
- Hardware task preemption

**Cons:**
- More complex configuration
- Smaller ecosystem than Embassy

**When to choose RTIC:** If you need SRP resource locks  
**When to choose Embassy:** If you need ecosystem + simplicity

#### Option C: Minimal Custom Runtime
From research: `cortex-m-asyncrt` crate
- 2KB RAM footprint
- Single-threaded executor
- Suitable for GLYF's constrained environment

**Example:**
```rust
#![no_std]
#![no_main]

use cortex_m_asyncrt::executor::Executor;

#[entry]
fn main() -> ! {
    let mut executor = Executor::new::<64>();
    executor.spawn(Task::new(sovereign_loop()));
    executor.run();
    loop {}
}

async fn sovereign_loop() {
    // GLYF kernel logic here
}
```

**Recommendation:** Proceed with **Embassy** — the ecosystem advantage outweighs concerns. Can migrate to RTIC later if SRP locks become necessary.

---

## Blocker 3: Android NDK (Needs Specialist)

### Current Status
Cross-compilation to Android requires NDK setup.

### Solution Paths

#### Option A: cargo-ndk (Recommended)
**Zero-configuration cross-compilation:**
```bash
# Install
cargo install cargo-ndk

# Add targets
rustup target add \
  aarch64-linux-android \
  armv7-linux-androideabi

# Build
cargo ndk -t arm64-v8a -o ./jniLibs build --release
```

**Auto-detects:**
- NDK location (Android Studio default)
- API level
- Architecture toolchains

**GitHub:** `bbqsrc/cargo-ndk`

#### Option B: Manual NDK Setup
**For CI/CD without Android Studio:**
```bash
# Download NDK standalone toolchain
export ANDROID_NDK_HOME=/path/to/ndk

# Configure cargo
mkdir -p .cargo
cat > .cargo/config.toml << 'EOF'
[target.aarch64-linux-android]
linker = "aarch64-linux-android21-clang"

[target.armv7-linux-androideabi]
linker = "armv7a-linux-androideabi21-clang"
EOF

# Build
cargo build --target aarch64-linux-android --release
```

#### Option C: Docker Container
**Reproducible build environment:**
```dockerfile
FROM rust:1.75-slim

RUN apt-get update && apt-get install -y \
    wget unzip cmake

# Download NDK
RUN wget https://dl.google.com/android/repository/android-ndk-r25c-linux.zip && \
    unzip android-ndk-r25c-linux.zip -d /opt/

ENV ANDROID_NDK_HOME=/opt/android-ndk-r25c

# Add targets
RUN rustup target add aarch64-linux-android armv7-linux-androideabi

WORKDIR /build
```

#### Known Issue: libgcc Not Found
**Fix for NDK r25+:**
```bash
# NDK replaced libgcc with libunwind
cd $ANDROID_NDK_HOME/toolchains/llvm/prebuilt/linux-x86_64/lib/clang/17/lib/linux/aarch64/
cp libunwind.a libgcc.a
```

**Or upgrade to Rust 1.82+** — fixed upstream.

#### Option D: Pure Rust UI (Long-term)
Avoid NDK entirely with Rust UI frameworks:
- **Dioxus** — Cross-platform Rust UI
- **Iced** — Elm-inspired GUI
- **egui** — Immediate mode GUI

**Trade-off:** Native Android look/feel vs. pure Rust stack.

**Recommendation:** Use **cargo-ndk** for immediate needs. Evaluate Dioxus for v0.9.

---

## Action Items

| Priority | Blocker | Solution | Owner | ETA |
|----------|---------|----------|-------|-----|
| 🔴 High | Pi Zero | Setup rpilocator alerts + QEMU | Echo Weaver | This week |
| 🔴 High | Embassy | Proceed with Embassy, document decision | Ternary-Smith | Today |
| 🟡 Medium | Android NDK | Implement cargo-ndk in build pipeline | Rosetta-Bridge | This week |
| 🟢 Low | Pi alternatives | Document Orange Pi Zero fallback | Mirror Maverick | Next week |

---

## Resources

### Pi Zero Stock
- https://rpilocator.com
- https://www.raspberrypi.com/resellers/

### Embassy
- https://github.com/embassy-rs/embassy
- https://docs.embassy.dev

### cargo-ndk
- https://github.com/bbqsrc/cargo-ndk
- https://crates.io/crates/cargo-ndk

### QEMU Pi
- https://github.com/dhruvvyas90/qemu-rpi-kernel

---

**Next Review:** After hardware acquisition or emulation setup complete.

— Research compiled by Kimi Claw

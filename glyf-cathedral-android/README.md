# GLYF Cathedral Android

Android native library for the 96-byte sovereign kernel.

## Quick Start

### 1. Setup (One-time)

Run the setup script on your laptop:

```bash
curl -sSL https://raw.githubusercontent.com/Lo-oMeN/glyf-cathedral-core/main/setup-android-ndk.sh | bash
```

Or manually:
```bash
# Install cargo-ndk
cargo install cargo-ndk

# Add Android targets
rustup target add aarch64-linux-android armv7-linux-androideabi

# Set NDK path (if not auto-detected)
export ANDROID_NDK_HOME=/path/to/android-ndk
```

### 2. Build

```bash
# Build for ARM64 (modern Android devices)
cargo ndk -t arm64-v8a -o ./jniLibs build --release

# Build for all architectures
cargo ndk -t arm64-v8a -t armeabi-v7a -t x86_64 -o ./jniLibs build --release
```

### 3. Deploy to Your Android Device

```bash
# Push library to device
adb push target/aarch64-linux-android/release/libglyf_cathedral_android.so /data/local/tmp/

# Test via adb shell
adb shell "cd /data/local/tmp && LD_LIBRARY_PATH=. ./test_runner"
```

## Project Structure

```
glyf-cathedral-android/
├── Cargo.toml          # Rust package config
├── src/
│   └── lib.rs          # JNI bridge + kernel logic
└── jniLibs/            # Output directory
    └── arm64-v8a/
        └── libglyf_cathedral_android.so
```

## JNI Interface

Java class: `com.glyf.cathedral.GLYFBridge`

```java
public class GLYFBridge {
    static {
        System.loadLibrary("glyf_cathedral_android");
    }
    
    public static native int getVersion();      // Returns 72 (v0.7.2)
    public static native boolean verifyState(); // Check Noether current
    public static native float getPhi7();       // Get φ⁷ magnitude
}
```

## Architecture Targets

| Target | ABI | Devices |
|--------|-----|---------|
| arm64-v8a | AArch64 | Most modern Android (2015+) |
| armeabi-v7a | ARMv7 | Older devices |
| x86_64 | x86_64 | Emulators, some tablets |

## Requirements

- Android NDK r25c or later
- Rust 1.75+
- cargo-ndk 3.0+

## License

Same as GLYF Cathedral core project.

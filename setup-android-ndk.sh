#!/bin/bash
# setup-android-ndk.sh - Run this on your laptop to set up Android NDK cross-compilation
# For GLYF Cathedral v0.7.2

set -e

echo "=== GLYF Cathedral Android NDK Setup ==="
echo ""

# Check for Rust
if ! command -v rustc &> /dev/null; then
    echo "❌ Rust not found. Install first:"
    echo "   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
    exit 1
fi
echo "✓ Rust found: $(rustc --version)"

# Install cargo-ndk
echo ""
echo "Installing cargo-ndk..."
cargo install cargo-ndk

# Add Android targets
echo ""
echo "Adding Android targets..."
rustup target add aarch64-linux-android      # For modern Android devices (ARM64)
rustup target add armv7-linux-androideabi    # For older Android devices (ARM32)
rustup target add x86_64-linux-android       # For Android emulators

# Check for Android NDK
echo ""
echo "Checking Android NDK..."

NDK_FOUND=false

# Check common locations
if [ -n "$ANDROID_NDK_HOME" ] && [ -d "$ANDROID_NDK_HOME" ]; then
    echo "✓ NDK found at: $ANDROID_NDK_HOME"
    NDK_FOUND=true
elif [ -n "$ANDROID_HOME" ] && [ -d "$ANDROID_HOME/ndk" ]; then
    NDK_PATH=$(find "$ANDROID_HOME/ndk" -maxdepth 1 -type d -name "*" | head -1)
    if [ -n "$NDK_PATH" ]; then
        echo "✓ NDK found at: $NDK_PATH"
        export ANDROID_NDK_HOME=$NDK_PATH
        NDK_FOUND=true
    fi
elif [ -d "$HOME/Android/Sdk/ndk" ]; then
    NDK_PATH=$(find "$HOME/Android/Sdk/ndk" -maxdepth 1 -type d -name "*" | head -1)
    if [ -n "$NDK_PATH" ]; then
        echo "✓ NDK found at: $NDK_PATH"
        export ANDROID_NDK_HOME=$NDK_PATH
        NDK_FOUND=true
    fi
fi

if [ "$NDK_FOUND" = false ]; then
    echo "⚠️  Android NDK not found in standard locations"
    echo ""
    echo "Download options:"
    echo "1. Via Android Studio: Tools → SDK Manager → SDK Tools → NDK"
    echo "2. Manual download: https://developer.android.com/ndk/downloads"
    echo ""
    echo "After installation, set environment variable:"
    echo "   export ANDROID_NDK_HOME=/path/to/android-ndk"
    exit 1
fi

# Create cargo config for NDK linking
echo ""
echo "Creating cargo configuration..."
mkdir -p ~/.cargo

cat > ~/.cargo/config.toml << 'EOF'
[target.aarch64-linux-android]
linker = "aarch64-linux-android21-clang"

[target.armv7-linux-androideabi]
linker = "armv7a-linux-androideabi21-clang"

[target.x86_64-linux-android]
linker = "x86_64-linux-android21-clang"

[env]
CC_aarch64-linux-android = "aarch64-linux-android21-clang"
CC_armv7-linux-androideabi = "armv7a-linux-androideabi21-clang"
CC_x86_64-linux-android = "x86_64-linux-android21-clang"
EOF

echo "✓ Created ~/.cargo/config.toml"

# Fix libgcc issue (NDK r25+) if needed
CLANG_DIR="$ANDROID_NDK_HOME/toolchains/llvm/prebuilt/linux-x86_64/lib/clang"
if [ -d "$CLANG_DIR" ]; then
    CLANG_VERSION=$(ls "$CLANG_DIR" | head -1)
    if [ -f "$CLANG_DIR/$CLANG_VERSION/lib/linux/aarch64/libunwind.a" ]; then
        if [ ! -f "$CLANG_DIR/$CLANG_VERSION/lib/linux/aarch64/libgcc.a" ]; then
            echo ""
            echo "Applying libgcc fix for NDK r25+..."
            cp "$CLANG_DIR/$CLANG_VERSION/lib/linux/aarch64/libunwind.a" \
               "$CLANG_DIR/$CLANG_VERSION/lib/linux/aarch64/libgcc.a"
            echo "✓ libgcc fix applied"
        fi
    fi
fi

# Test build
echo ""
echo "=== Testing Android Build ==="
echo "Building for arm64-v8a (modern Android devices)..."

# Create a minimal test project
TEST_DIR=$(mktemp -d)
cd "$TEST_DIR"

cat > Cargo.toml << 'EOF'
[package]
name = "glyf-android-test"
version = "0.1.0"
edition = "2021"
EOF

mkdir -p src
cat > src/lib.rs << 'EOF'
#[no_mangle]
pub extern "C" fn glyf_version() -> i32 {
    72  // v0.7.2
}
EOF

# Build with cargo-ndk
cargo ndk -t arm64-v8a build --release 2>&1 | tail -5

if [ -f "target/aarch64-linux-android/release/libglyf_android_test.so" ]; then
    echo ""
    echo "✅ SUCCESS! Android cross-compilation working"
    echo ""
    echo "Output: target/aarch64-linux-android/release/libglyf_android_test.so"
    file target/aarch64-linux-android/release/libglyf_android_test.so
else
    echo ""
    echo "❌ Build failed. Check errors above."
fi

# Cleanup
cd -
rm -rf "$TEST_DIR"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Add to your shell profile (~/.bashrc or ~/.zshrc):"
echo "   export ANDROID_NDK_HOME=$ANDROID_NDK_HOME"
echo ""
echo "To build GLYF Cathedral for Android:"
echo "   cargo ndk -t arm64-v8a -o ./jniLibs build --release"
echo ""
echo "Supported targets:"
echo "   arm64-v8a    (ARM64, most modern Android devices)"
echo "   armeabi-v7a  (ARM32, older devices)"
echo "   x86_64       (Android emulators)"

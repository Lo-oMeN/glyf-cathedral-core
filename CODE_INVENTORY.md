# GLYF Cathedral — Code Inventory

**Audit Date:** 2026-03-23  
**Status:** ⚠️ STRUCTURE EXISTS, NEEDS COMPILATION TEST

---

## What Exists

### Rust Code (~2000 lines)

| File | Lines | Purpose | Status |
|------|-------|---------|--------|
| `trinity-v6/src/kernel.rs` | 620 | Sovereign kernel, RS codec, SD persistence | ✅ Module structure fixed |
| `trinity-v6/src/state.rs` | 435 | LatticeState, morphogen FSM | Needs review |
| `trinity-v6/src/qr.rs` | 474 | QR transfer, Reed-Solomon | Needs review |
| `trinity-v6/src/ui.rs` | 362 | Paraclete UI vessel | Needs review |
| `trinity-v6/src/lib.rs` | 103 | Module exports, error types | ✅ Created |
| `trinity-v6/src/main.rs` | 30 | Binary entry point | ✅ Created |
| `glyf-cathedral-android/src/lib.rs` | 103 | Android JNI bridge | ✅ Created |

### Build Configuration

| File | Purpose | Status |
|------|---------|--------|
| `Cargo.toml` | Workspace root | ✅ Created |
| `trinity-v6/Cargo.toml` | Kernel crate | ✅ Created |
| `glyf-cathedral-android/Cargo.toml` | Android crate | ✅ Exists |

---

## What's Missing

### 1. Compilation Test
**Critical:** No `cargo check` has been run. Need to:
```bash
cargo check        # Verify syntax
cargo test         # Run unit tests
cargo build        # Build library
cargo build --release  # Optimized build
```

### 2. Module Dependencies
The kernel.rs has references to `SovereignState` but it should reference `crate::state::LatticeState`. Need to reconcile naming:
- `SovereignState` (in kernel.rs) vs `LatticeState` (referenced in lib.rs)

### 3. Test Infrastructure
No CI/CD pipeline configured for Rust builds.

---

## File Structure (Target)

```
glyf-cathedral-core/
├── Cargo.toml                    # Workspace root
├── README.md
├── trinity-v6/
│   ├── Cargo.toml
│   └── src/
│       ├── lib.rs               # Module exports
│       ├── main.rs              # Binary entry
│       ├── kernel.rs            # Core kernel (620 lines)
│       ├── state.rs             # Lattice state (435 lines)
│       ├── qr.rs                # QR transfer (474 lines)
│       └── ui.rs                # UI vessel (362 lines)
├── glyf-cathedral-android/
│   ├── Cargo.toml
│   └── src/
│       └── lib.rs               # JNI bridge
└── ...
```

---

## Next Steps

1. **Fix module naming** — `SovereignState` vs `LatticeState`
2. **Run cargo check** — Find and fix compilation errors
3. **Add unit tests** — Verify 96-byte layout, φ⁷ constants
4. **CI pipeline** — GitHub Actions for automated builds

---

## Verification Commands

```bash
# On your laptop with Rust installed:
cd glyf-cathedral-core

# Check compilation
cargo check

# Run tests
cargo test

# Build for host
cargo build

# Build for Pi Zero (cross-compile)
cargo build --target arm-unknown-linux-gnueabihf

# Build for Android
cd glyf-cathedral-android
cargo ndk -t arm64-v8a build --release
```

---

## Summary

| Aspect | Status |
|--------|--------|
| Code exists | ✅ ~2000 lines |
| Buildable structure | ✅ Cargo workspace configured |
| Compiles | ⚠️ Not verified |
| Tests pass | ⚠️ Not verified |
| CI/CD | ❌ Missing |

**The bones are there. They need to be wired together and tested.**

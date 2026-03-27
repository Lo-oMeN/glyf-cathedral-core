# GLYF Audio Transformer — Documentation

**Purpose:** Enable GLYF to "hear" — process audio without cloud APIs  
**Output:** 96-byte AudioGlyf structure (compatible with GlyfWord)  
**Philosophy:** Deterministic, edge-native, stepping stone

---

## Architecture

### Dual Implementation

| Layer | File | Environment | Use Case |
|-------|------|-------------|----------|
| Core | `glyf-engine/src/audio_transformer.rs` | Rust, no_std | Android tracphone, edge devices |
| Web | `glyf-viz/src/audioTransformer.js` | JavaScript | Browser, Web Audio API |

Both produce identical 96-byte structures from identical audio input.

---

## 96-Byte AudioGlyf Structure

```rust
#[repr(C, align(64))]
pub struct AudioGlyf {
    temporal_sig: u64,           // 8 bytes — perceptual hash of audio
    spectral_centroid: [f64; 3], // 24 bytes — [low, mid, high] frequency bands
    harmonic_signature: [f64; 7],// 56 bytes — fundamental + 6 overtones
    energy_rms: f64,             // 8 bytes — root mean square amplitude
} // Total: exactly 96 bytes
```

**Alignment with GlyfWord:**
- `temporal_sig` ↔ `native_sig` — unique identifier
- `spectral_centroid` ↔ `geo_centroid` — 3D spatial representation
- `harmonic_signature` ↔ `center_axis` — 7-type semantic vector
- `energy_rms` ↔ `trajectory_mag` — magnitude/strength

This symmetry enables seamless audio → text → geometry transitions.

---

## Processing Pipeline

### Step 1: Pre-emphasis

**Function:** High-pass filter emphasizing voice frequencies  
**Formula:** `y[n] = x[n] - 0.97 * x[n-1]`  
**Purpose:** Compensate for spectral tilt, enhance consonants

### Step 2: Framing

**Window:** Hann (raised cosine)  
**Size:** 512 samples (32ms @ 16kHz)  
**Hop:** 256 samples (50% overlap)  
**Purpose:** Stationary analysis segments

### Step 3: FFT Spectrum

**Implementation:** Naive DFT (Rust), native FFT (JS)  
**Output:** Magnitude spectrum (0-8kHz, 256 bins)  
**Purpose:** Frequency domain representation

### Step 4: Feature Extraction

**Spectral Centroid (3 bands):**
- Low: 0-300Hz (fundamental/pitch)
- Mid: 300-2000Hz (formants/voice)
- High: 2000-8000Hz (friction/consonants)

**Harmonic Signature (7 harmonics):**
1. Fundamental frequency (pitch)
2. 1st overtone (2× fundamental)
3. 2nd overtone (3× fundamental)
4. 3rd overtone (4× fundamental)
5. 4th overtone (5× fundamental)
6. 5th overtone (6× fundamental)
7. 6th overtone (7× fundamental)

**RMS Energy:**
- Root mean square of all samples
- Normalized 0-1 range

### Step 5: Temporal Hash

**Algorithm:** FNV-1a perceptual hash  
**Sampling:** Every 100th sample (coarse fingerprint)  
**Purpose:** Robust audio identification (tolerant of small variations)

---

## 7-Type Primitive Mapping

Harmonics map directly to the universal glyphobetic primitives:

| Harmonic | Frequency | Primitive | Symbol | Semantic Field |
|----------|-----------|-----------|--------|----------------|
| Fundamental | f₀ | Curve | ∿ | flow, return, cyclical |
| 1st | 2f₀ | Line | │ | direction, will, extension |
| 2nd | 3f₀ | Angle | ∠ | tension, decision, break |
| 3rd | 4f₀ | Vesica | ⧖ | union, intersection, birth |
| 4th | 5f₀ | Spiral | ꩜ | evolution, returning, deepening |
| 5th | 6f₀ | Node | ● | point, singularity, awareness |
| 6th | 7f₀ | Field | ▥ | container, ground, context |

**The mapping:** Sound → Harmonics → Primitives → Meaning

---

## Usage Examples

### Rust (Core Engine)

```rust
use glyf_engine::audio_transformer::{AudioGlyf, AudioDecoder};

// Decode Ogg/Opus
let ogg_data = std::fs::read("voice_message.ogg")?;
let pcm = AudioDecoder::decode_ogg_opus(&ogg_data)?;

// Transform to 96-byte structure
let audio_glyf = AudioGlyf::from_pcm(&pcm);

// Extract dominant primitive
let dominant = audio_glyf.dominant_primitive();
println!("Voice quality: {:?}", dominant); // e.g., Curve (flowing)

// Convert to GlyfWord for semantic pipeline
let word = audio_glyf.to_glyf_word();
```

### JavaScript (Web Frontend)

```javascript
import AudioTransformer from './audioTransformer.js';

// Decode and transform
const response = await fetch('voice_message.ogg');
const arrayBuffer = await response.arrayBuffer();
const audioBuffer = await AudioTransformer.decodeOggOpus(arrayBuffer);

const audioGlyf = AudioTransformer.transform(audioBuffer);

// Access features
console.log('Energy:', audioGlyf.energyRMS);
console.log('Dominant:', audioGlyf.dominantPrimitive()); // "Curve"

// Convert to GlyfWord for cathedral visualization
const word = audioGlyf.toGlyfWord();
// Now word can be processed through L1→L2→L3 pipeline
```

---

## Deterministic Guarantees

**Same audio → same 96-byte structure:**
- Fixed sample rate (16kHz)
- Fixed frame size (512 samples)
- Fixed FFT implementation (naive DFT is deterministic)
- Fixed hash algorithm (FNV-1a)

**No randomness. No ML. No cloud.**

---

## Edge-Native Constraints

| Resource | Usage | Limit |
|----------|-------|-------|
| Memory | 96 bytes per utterance | <1KB buffer |
| CPU | FFT per frame | ~1ms per second of audio |
| Storage | None | Pure computation |
| Network | None | Fully offline |

**Tracphone compatible:** Runs on minimal Android hardware without lag.

---

## Integration with GLYF Pipeline

```
Audio Input (Ogg/Opus)
        ↓
[Audio Transformer]
        ↓
AudioGlyf (96 bytes)
        ↓
toGlyfWord()
        ↓
GlyfWord (96 bytes)
        ↓
[L1→L2→L3 Pipeline]
        ↓
Navigable Cathedral Geometry
```

**Result:** Voice messages become traversable geometric structures.

---

## Testing

### Rust Tests

```bash
cd glyf-engine
cargo test audio_transformer
```

Tests verify:
- 96-byte structure size
- Synthetic sine wave harmonic detection
- Energy calculation accuracy
- Hash consistency

### JavaScript Tests

```javascript
// In browser console
const synth = AudioTransformer.generateTestTone(440, 1.0);
const result = AudioTransformer.transform(synth);
console.log(result.harmonicSignature);
// Should show peak at index 0 (fundamental)
```

---

## Future Enhancements

**Phase 2:** Speaker identification via harmonic ratios  
**Phase 3:** Emotion detection via spectral flux patterns  
**Phase 4:** Real-time streaming transformer (chunked processing)

---

## References

- Rabiner, L.R. & Schafer, R.W. *Digital Processing of Speech Signals* (1978)
- FNV-1a hash: Fowler-Noll-Vo algorithm
- Hann window: Raised cosine for spectral leakage reduction
- 16kHz sample rate: Optimal for voice (telephony standard)

---

**Status:** Operational. GLYF can hear.

❤️‍🔥

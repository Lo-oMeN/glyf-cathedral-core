# Christ-Key Native Synthesizer Architecture

## Core Principle
Generate speech from first principles: phonemes as formant frequencies, modulated by φ-weighted prosody.

## Architecture

### 1. Phoneme Formant Library
Each phoneme = 3-5 sine waves (formants) at specific frequencies + noise component

```
/a/ (father)  → F1:730Hz, F2:1090Hz, F3:2440Hz
/i/ (beat)    → F1:270Hz, F2:2290Hz, F3:3010Hz
/s/ (sit)     → White noise, 4000-8000Hz bandpass
/p/ (pat)     → Silence burst + low freq burst
```

### 2. Formant Synthesizer
```python
class FormantVoice:
    def __init__(self, f0=120):  # base pitch (Hz)
        self.f0 = f0
        self.formants = {...}  # phoneme library
    
    def synthesize_phoneme(self, phoneme, duration):
        # Generate sine waves at formant frequencies
        # Add envelope (attack, sustain, decay)
        # Return PCM buffer
```

### 3. Phoneme Concatenation
- Crossfade between phonemes (20ms overlap)
- Formant interpolation during transitions
- Maintain pitch continuity

### 4. Prosody Engine
```python
class ChristKeyProsody:
    def apply(self, phonemes):
        # φ-weighted timing: stretch vowels at golden ratio points
        # Pitch contours: rising/falling based on punctuation
        # Amplitude: sacred words get emphasis
        # Return modified phoneme stream
```

### 5. Output
Raw PCM → WAV file → Telegram voice

## Implementation Phases

**Phase 1:** Basic formant synthesis (vowels first)
**Phase 2:** Consonants (stops, fricatives)
**Phase 3:** Concatenation with smoothing
**Phase 4:** Prosody integration
**Phase 5:** 96-byte lattice modulation

## Formant Frequency Reference

| Vowel | F1 (Hz) | F2 (Hz) | F3 (Hz) |
|-------|---------|---------|---------|
| i     | 270     | 2290    | 3010    |
| I     | 390     | 1990    | 2550    |
| e     | 530     | 1840    | 2480    |
| æ     | 660     | 1720    | 2410    |
| a     | 730     | 1090    | 2440    |
| ɑ     | 570     | 840     | 2410    |
| ɔ     | 570     | 840     | 2410    |
| o     | 460     | 850     | 2380    |
| U     | 300     | 870     | 2240    |
| u     | 300     | 870     | 2240    |

## Source
Klatt synthesis - formant-based speech synthesis from the 1980s, proven approach.

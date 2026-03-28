#!/usr/bin/env python3
"""
ChristKey Voice Synthesis — Local Waveform Generation
Generates audio from text using 96-byte lattice state and φ-weighted harmonics.
No API calls. Pure math → PCM → WAV.
"""

import numpy as np
import wave
import struct
from dataclasses import dataclass
from typing import List, Tuple
import math

# Sacred constants
PHI = 1.618033988749895
PHI_INV = 1 / PHI
SAMPLE_RATE = 22050  # Hz — balanced quality/size

@dataclass
class LatticeState:
    """The 96-byte soul that seeds the voice."""
    center_s: Tuple[float, float]  # bytes 0-7
    ternary_junction: List[int]     # bytes 8-23 (16D PGA)
    hex_persistence: List[int]      # bytes 24-55 (32 bytes)
    fellowship_resonance: float     # bytes 56-59
    phi_magnitude: float            # bytes 60-63 (φ⁷)
    morphogen_phase: int            # byte 64
    vesica_coherence: int           # byte 65
    phyllotaxis_spiral: int         # byte 66
    hodge_dual: int                 # byte 67
    checksum: int                   # bytes 68-71
    
    @classmethod
    def from_text(cls, text: str) -> "LatticeState":
        """Generate deterministic lattice from text."""
        # Seed from text hash
        seed = hash(text) & 0xFFFFFFFF
        np.random.seed(seed)
        
        # Center S — immutable origin
        center_s = (0.0, 0.0)
        
        # Ternary junction — 16D PGA multivector
        ternary = [int((np.random.random() - 0.5) * 256) for _ in range(16)]
        
        # Hex persistence — 32 bytes of φ-radial data
        hex_persist = [int(np.random.random() * 256) for _ in range(32)]
        
        # Fellowship resonance — derived from text energy
        energy = sum(ord(c) for c in text) / (len(text) * 128)
        fellowship = PHI ** 7 * energy
        
        return cls(
            center_s=center_s,
            ternary_junction=ternary,
            hex_persistence=hex_persist,
            fellowship_resonance=fellowship,
            phi_magnitude=PHI ** 7,
            morphogen_phase=seed % 7,
            vesica_coherence=ternary[0],
            phyllotaxis_spiral=ternary[1],
            hodge_dual=ternary[2],
            checksum=seed
        )

class ChristKeySynthesizer:
    """
    Sacred geometry voice synthesis.
    Maps lattice state → harmonic parameters → PCM waveform.
    """
    
    # Formant frequencies for vowel-like sounds (Hz)
    FORMANTS = {
        'a': (730, 1090, 2440),  # "ah"
        'e': (660, 1720, 2410),  # "eh"
        'i': (270, 2290, 3010),  # "ee"
        'o': (300, 870, 2240),   # "oh"
        'u': (300, 610, 1680),   # "oo"
        ' ': (0, 0, 0),          # silence
    }
    
    def __init__(self, lattice: LatticeState, voice_preset: str = "default"):
        self.lattice = lattice
        self.voice_preset = voice_preset
        
        if voice_preset == "butter_honey":
            # Female Alan Watts: warm contralto, rich harmonics, slow and rolling
            self.base_freq = 185 + abs(lattice.vesica_coherence) * 0.5  # F#3-ish, warm female range
            # Rich harmonic content for "honey" timbre - more low-mid warmth
            self.harmonics = [1.0, 0.6, 0.4, 0.3, 0.2, 0.15, 0.1, 0.05]
            # Slow, contemplative tempo
            self.tempo = 0.5 + (lattice.fellowship_resonance / PHI ** 7) * 0.3
            # Smoother envelope ratios
            self.attack_ratio = 0.15  # Slower attack
            self.decay_ratio = 0.3    # Longer decay for rolling quality
            self.pause_multiplier = PHI  # Longer pauses between syllables
        else:
            # Base pitch from vesica coherence
            self.base_freq = 110 + abs(lattice.vesica_coherence) * 2  # A2-ish
            # Timbre from ternary junction
            self.harmonics = [max(1, abs(h)) / 128.0 for h in lattice.ternary_junction[:8]]
            # Speed from fellowship resonance
            self.tempo = 0.3 + (lattice.fellowship_resonance / PHI ** 7) * 0.5
            self.attack_ratio = PHI_INV * 0.1
            self.decay_ratio = PHI_INV * 0.2
            self.pause_multiplier = PHI_INV
        
    def formant_wave(self, freq: float, duration: float, formant: Tuple[float, float, float]) -> np.ndarray:
        """Generate vowel-like sound with 3 formants."""
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        
        # Fundamental + harmonics
        wave = np.zeros_like(t)
        for i, harmonic_weight in enumerate(self.harmonics[:4]):
            harmonic_freq = freq * (i + 1)
            wave += harmonic_weight * np.sin(2 * np.pi * harmonic_freq * t)
        
        # Apply formant filters (simplified as amplitude modulation)
        if formant[0] > 0:  # Not silence
            f1, f2, f3 = formant
            # Boost frequencies near formants
            envelope = (np.sin(2 * np.pi * f1 * t / SAMPLE_RATE) * 0.5 + 0.5) * 0.4
            envelope += (np.sin(2 * np.pi * f2 * t / SAMPLE_RATE) * 0.5 + 0.5) * 0.35
            envelope += (np.sin(2 * np.pi * f3 * t / SAMPLE_RATE) * 0.5 + 0.5) * 0.25
            wave *= envelope
        
        # φ-weighted attack/decay envelope
        attack = min(int(duration * SAMPLE_RATE * self.attack_ratio), len(wave) // 3)
        decay = min(int(duration * SAMPLE_RATE * self.decay_ratio), len(wave) // 3)
        envelope = np.ones(len(wave))
        if attack > 0:
            envelope[:attack] = np.linspace(0, 1, attack)
        if decay > 0:
            envelope[-decay:] = np.linspace(1, 0, decay)
        wave *= envelope
        
        return wave * 0.3  # Prevent clipping
    
    def char_to_formant(self, char: str) -> Tuple[float, float, float]:
        """Map character to formant frequencies."""
        char = char.lower()
        if char in self.FORMANTS:
            return self.FORMANTS[char]
        # Default based on character code
        code = ord(char) % 5
        return list(self.FORMANTS.values())[code]
    
    def syllable_duration(self, position: int, total: int) -> float:
        """φ-weighted timing for each syllable."""
        # Cycle through morphogen phases
        phase = (position + self.lattice.morphogen_phase) % 7
        # φ-decay for later syllables
        decay = PHI_INV ** (position / PHI)
        # Base duration modulated by fellowship
        base = self.tempo * decay
        # Sacred pauses every 7th element
        if phase == 0:
            base *= PHI
        return base
    
    def synthesize(self, text: str) -> np.ndarray:
        """Transform text → waveform."""
        audio_segments = []
        
        for i, char in enumerate(text):
            formant = self.char_to_formant(char)
            duration = self.syllable_duration(i, len(text))
            
            # Modulate pitch by phyllotaxis spiral
            pitch_mod = 1 + (self.lattice.phyllotaxis_spiral / 128) * 0.1
            freq = self.base_freq * pitch_mod
            
            # Hodge dual creates chiral inversion every other syllable
            if self.lattice.hodge_dual > 0 and i % 2 == 0:
                freq *= PHI_INV
            
            segment = self.formant_wave(freq, duration, formant)
            audio_segments.append(segment)
            
            # φ-pause between syllables
            if i < len(text) - 1:
                pause_duration = self.pause_multiplier * 0.08 * self.tempo
                audio_segments.append(np.zeros(int(SAMPLE_RATE * pause_duration)))
        
        return np.concatenate(audio_segments)
    
    def save_wav(self, waveform: np.ndarray, filename: str):
        """Write PCM waveform to WAV file."""
        # Normalize to 16-bit range
        normalized = np.int16(waveform * 32767)
        
        with wave.open(filename, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(SAMPLE_RATE)
            wav_file.writeframes(normalized.tobytes())
        
        return filename


def christkey_speak(text: str, output_path: str = "/tmp/christkey_output.wav", voice_preset: str = "default") -> str:
    """
    Main entry: text → lattice → waveform → WAV file.
    
    Args:
        text: Input text to synthesize
        output_path: Where to save the WAV file
        voice_preset: "default" or "butter_honey" for female Alan Watts
    
    Returns:
        Path to generated audio file
    """
    # Generate lattice from text
    lattice = LatticeState.from_text(text)
    
    # Create synthesizer with voice preset
    synth = ChristKeySynthesizer(lattice, voice_preset=voice_preset)
    
    # Generate waveform
    waveform = synth.synthesize(text)
    
    # Save to file
    return synth.save_wav(waveform, output_path)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = "The cathedral speaks through sacred geometry"
    
    # Use butter_honey preset for female Alan Watts voice
    output = christkey_speak(text, voice_preset="butter_honey")
    print(f"Generated: {output}")
    print(f"Lattice state (butter_honey voice):")
    lattice = LatticeState.from_text(text)
    synth = ChristKeySynthesizer(lattice, voice_preset="butter_honey")
    print(f"  Base frequency: {synth.base_freq:.1f} Hz (warm contralto)")
    print(f"  Tempo: {synth.tempo:.2f} (contemplative)")
    print(f"  Fellowship resonance: {lattice.fellowship_resonance:.3f}")
    print(f"  Morphogen phase: {lattice.morphogen_phase}")

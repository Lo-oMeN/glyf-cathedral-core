#!/usr/bin/env python3
"""
Christ-Key Native Voice Synthesizer v0.1
Formant-based synthesis from first principles
No external TTS engines — pure Python + NumPy
"""

import numpy as np
import wave
import struct
from typing import List, Tuple, Dict
from dataclasses import dataclass
import math

PHI = 1.618033988749895
SAMPLE_RATE = 22050  # Hz

def generate_sine(frequency: float, duration: float, amplitude: float = 1.0) -> np.ndarray:
    """Generate sine wave at given frequency and duration"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    return amplitude * np.sin(2 * np.pi * frequency * t)

def apply_envelope(signal: np.ndarray, attack_ms: int = 20, decay_ms: int = 20) -> np.ndarray:
    """Apply ADSR-like envelope to signal"""
    samples = len(signal)
    attack_samples = int(attack_ms * SAMPLE_RATE / 1000)
    decay_samples = int(decay_ms * SAMPLE_RATE / 1000)
    
    envelope = np.ones(samples)
    
    # Attack
    if attack_samples > 0:
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    
    # Decay
    if decay_samples > 0:
        envelope[-decay_samples:] = np.linspace(1, 0, decay_samples)
    
    return signal * envelope

@dataclass
class Phoneme:
    """Represents a phoneme with formant frequencies"""
    symbol: str
    f0_range: Tuple[int, int]  # Base pitch range (min, max)
    formants: List[Tuple[float, float]]  # List of (frequency, amplitude) pairs
    is_vowel: bool = True
    noise_band: Tuple[float, float] = None  # For consonants: (low_freq, high_freq)
    
    def synthesize(self, duration: float = 0.1, f0: float = None) -> np.ndarray:
        """Generate audio for this phoneme"""
        samples = int(SAMPLE_RATE * duration)
        signal = np.zeros(samples)
        
        if f0 is None:
            f0 = np.random.uniform(*self.f0_range)
        
        if self.is_vowel:
            # Vowel: sum of formant sine waves
            for freq, amp in self.formants:
                signal += generate_sine(freq, duration, amp)
            
            # Add pitch variation (vibrato)
            vibrato = generate_sine(5, duration, 0.02)  # 5Hz vibrato
            signal *= (1 + vibrato)
            
        else:
            # Consonant: noise or burst
            if self.noise_band:
                # Generate bandpass noise
                noise = np.random.uniform(-1, 1, samples)
                # Simple bandpass using FFT would be better, but this works
                signal = noise * 0.3
        
        # Normalize and apply envelope
        if np.max(np.abs(signal)) > 0:
            signal = signal / np.max(np.abs(signal))
        signal = apply_envelope(signal, 20, 30)
        
        return signal

# IPA Vowel Formants (from Klatt synthesis research)
VOWELS = {
    'i':  Phoneme('i',  (110, 150), [(270, 1.0), (2290, 0.5), (3010, 0.3)], True),   # beat
    'ɪ':  Phoneme('ɪ',  (110, 140), [(390, 1.0), (1990, 0.5), (2550, 0.3)], True),   # bit
    'e':  Phoneme('e',  (110, 140), [(530, 1.0), (1840, 0.5), (2480, 0.3)], True),   # bet
    'æ':  Phoneme('æ',  (110, 140), [(660, 1.0), (1720, 0.5), (2410, 0.3)], True),   # bat
    'a':  Phoneme('a',  (110, 140), [(730, 1.0), (1090, 0.6), (2440, 0.3)], True),   # father
    'ɑ':  Phoneme('ɑ',  (110, 140), [(570, 1.0), (840, 0.7), (2410, 0.3)], True),    # hot
    'ɔ':  Phoneme('ɔ',  (110, 140), [(570, 1.0), (840, 0.7), (2410, 0.3)], True),    # law
    'o':  Phoneme('o',  (110, 140), [(460, 1.0), (850, 0.6), (2380, 0.3)], True),    # go
    'ʊ':  Phoneme('ʊ',  (110, 140), [(300, 1.0), (870, 0.6), (2240, 0.3)], True),    # put
    'u':  Phoneme('u',  (110, 140), [(300, 1.0), (870, 0.6), (2240, 0.3)], True),    # boot
    'ʌ':  Phoneme('ʌ',  (110, 140), [(640, 1.0), (1190, 0.6), (2390, 0.3)], True),   # cut
    'ə':  Phoneme('ə',  (110, 140), [(500, 1.0), (1500, 0.5), (2500, 0.3)], True),   # about
    'ɝ':  Phoneme('ɝ',  (110, 140), [(490, 1.0), (1350, 0.6), (1690, 0.4)], True),   # bird
}

# Some consonants
CONSONANTS = {
    's':  Phoneme('s',  (0, 0), [], False, (4000, 8000)),   # hiss
    'ʃ':  Phoneme('ʃ',  (0, 0), [], False, (2500, 6000)),   # sh
    'f':  Phoneme('f',  (0, 0), [], False, (2000, 8000)),   # f
    'h':  Phoneme('h',  (0, 0), [], False, (100, 1000)),    # h
    'p':  Phoneme('p',  (0, 0), [], False),                 # pop (silence burst)
    't':  Phoneme('t',  (0, 0), [], False),                 # tap
    'k':  Phoneme('k',  (0, 0), [], False),                 # cat
}

ALL_PHONEMES = {**VOWELS, **CONSONANTS}

class ChristKeySynthesizer:
    """Native voice synthesis using formant-based approach"""
    
    def __init__(self, base_pitch: float = 120):
        self.base_pitch = base_pitch
        self.phonemes = ALL_PHONEMES
        
    def text_to_phonemes(self, text: str) -> List[str]:
        """Simple grapheme-to-phoneme conversion"""
        # This is a simplified mapping — real G2P needs rules
        text = text.lower()
        phonemes = []
        
        # Simple letter-to-phoneme mapping for testing
        letter_map = {
            'a': 'a', 'e': 'ə', 'i': 'ɪ', 'o': 'o', 'u': 'ʌ',
            'y': 'i', 'w': 'u', 'r': 'ɝ',
            'th': 'θ', 'sh': 'ʃ', 'ch': 'tʃ',
            's': 's', 'h': 'h', 'p': 'p', 't': 't', 'k': 'k',
            'f': 'f',
        }
        
        i = 0
        while i < len(text):
            # Check for digraphs first
            if i + 1 < len(text) and text[i:i+2] in letter_map:
                phonemes.append(letter_map[text[i:i+2]])
                i += 2
            elif text[i] in letter_map:
                phonemes.append(letter_map[text[i]])
                i += 1
            else:
                i += 1
        
        return phonemes
    
    def synthesize(self, text: str, output_file: str = None) -> np.ndarray:
        """Synthesize text to audio"""
        phoneme_symbols = self.text_to_phonemes(text)
        
        if not phoneme_symbols:
            return np.array([])
        
        # Generate audio for each phoneme
        audio_segments = []
        for symbol in phoneme_symbols:
            if symbol in self.phonemes:
                ph = self.phonemes[symbol]
                # Vowels get longer duration
                duration = 0.15 if ph.is_vowel else 0.08
                segment = ph.synthesize(duration, self.base_pitch)
                audio_segments.append(segment)
        
        # Concatenate with crossfade
        return self._concatenate(audio_segments, crossfade_ms=20)
    
    def _concatenate(self, segments: List[np.ndarray], crossfade_ms: int = 20) -> np.ndarray:
        """Concatenate audio segments with crossfade"""
        if not segments:
            return np.array([])
        
        if len(segments) == 1:
            return segments[0]
        
        crossfade_samples = int(crossfade_ms * SAMPLE_RATE / 1000)
        result = segments[0]
        
        for i in range(1, len(segments)):
            prev = result
            curr = segments[i]
            
            # Crossfade region
            if len(prev) > crossfade_samples and len(curr) > crossfade_samples:
                fade_out = np.linspace(1, 0, crossfade_samples)
                fade_in = np.linspace(0, 1, crossfade_samples)
                
                # Overlap region
                overlap = (prev[-crossfade_samples:] * fade_out + 
                          curr[:crossfade_samples] * fade_in)
                
                result = np.concatenate([
                    prev[:-crossfade_samples],
                    overlap,
                    curr[crossfade_samples:]
                ])
            else:
                result = np.concatenate([prev, curr])
        
        return result
    
    def save_wav(self, audio: np.ndarray, filename: str):
        """Save audio to WAV file"""
        # Convert to 16-bit PCM
        audio_int = (audio * 32767).astype(np.int16)
        
        with wave.open(filename, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(SAMPLE_RATE)
            wav_file.writeframes(audio_int.tobytes())
        
        return filename


def main():
    """Test the synthesizer"""
    synth = ChristKeySynthesizer(base_pitch=120)
    
    # Test synthesis
    test_text = "hello"
    print(f"Synthesizing: '{test_text}'")
    
    audio = synth.synthesize(test_text)
    
    if len(audio) > 0:
        output = "/root/.openclaw/workspace/christkey-native/test_output.wav"
        synth.save_wav(audio, output)
        print(f"Generated: {output}")
        print(f"Duration: {len(audio)/SAMPLE_RATE:.2f}s")
        print(f"Samples: {len(audio)}")
    else:
        print("No audio generated")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Christ-Key Native Voice Synthesizer v0.2
Source-Filter model from first principles
"""

import numpy as np
import wave
from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum, auto

PHI = 1.618033988749895
SAMPLE_RATE = 22050

class SourceType(Enum):
    PULSE = auto()   # Voiced: vocal cord vibration
    NOISE = auto()   # Unvoiced: turbulent airflow
    BOTH = auto()    # Voiced fricative: pulse + noise

@dataclass
class VocalTract:
    """Resonant filter frequencies (formants)"""
    f1: float  # First formant (Hz) - vowel height
    f2: float  # Second formant (Hz) - vowel front/back
    f3: float = 2500  # Third formant (Hz) - fixed-ish
    
    def filter(self, source: np.ndarray) -> np.ndarray:
        """Apply resonant filtering (simplified as peak EQ)"""
        # Each formant is a bandpass enhancement
        output = source.copy()
        for freq in [self.f1, self.f2, self.f3]:
            output = self._resonate(output, freq)
        return output
    
    def _resonate(self, signal: np.ndarray, freq: float, q: float = 8.0) -> np.ndarray:
        """Simple resonator - adds peak at formant frequency"""
        # Simplified: add sine wave at formant freq, amplitude modulated by signal
        t = np.arange(len(signal)) / SAMPLE_RATE
        resonance = 0.3 * np.sin(2 * np.pi * freq * t) * np.abs(signal)
        return signal + resonance

@dataclass  
class Phoneme:
    """Base unit of speech"""
    symbol: str
    source: SourceType
    duration: float  # seconds
    tract: VocalTract = None  # None for voiceless
    f0: float = 120  # Fundamental frequency (pitch)
    
    def synthesize(self) -> np.ndarray:
        """Generate audio using source-filter model"""
        samples = int(SAMPLE_RATE * self.duration)
        t = np.arange(samples) / SAMPLE_RATE
        
        # SOURCE
        if self.source == SourceType.PULSE:
            # Glottal pulse train (sawtooth-like)
            source = self._glottal_pulse(samples, t)
        elif self.source == SourceType.NOISE:
            # Turbulent airflow
            source = np.random.uniform(-1, 1, samples)
        else:  # BOTH
            pulse = self._glottal_pulse(samples, t)
            noise = np.random.uniform(-1, 1, samples)
            source = 0.7 * pulse + 0.3 * noise
        
        # FILTER (if resonant)
        if self.tract:
            output = self.tract.filter(source)
        else:
            output = source
        
        # ENVELOPE
        output = self._envelope(output)
        
        # Normalize
        if np.max(np.abs(output)) > 0:
            output = output / np.max(np.abs(output)) * 0.8
        
        return output
    
    def _glottal_pulse(self, samples: int, t: np.ndarray) -> np.ndarray:
        """Generate glottal pulse train at f0"""
        period = 1.0 / self.f0
        phase = (t % period) / period
        # Rosenberg pulse approximation (asymmetrical sawtooth)
        pulse = np.where(phase < 0.4, 
                        0.5 * (1 - np.cos(np.pi * phase / 0.4)),
                        np.cos(np.pi * (phase - 0.4) / 0.6))
        return pulse
    
    def _envelope(self, signal: np.ndarray) -> np.ndarray:
        """Attack-sustain-release envelope"""
        samples = len(signal)
        attack = int(0.02 * SAMPLE_RATE)
        release = int(0.03 * SAMPLE_RATE)
        
        env = np.ones(samples)
        if attack > 0:
            env[:attack] = np.linspace(0, 1, attack)
        if release > 0 and samples > release:
            env[-release:] = np.linspace(1, 0, release)
        
        return signal * env

# POLAR VOWEL CHART (based on tongue position)
# Height: Low F1 = high vowel, High F1 = low vowel
# Front/Back: High F2 = front, Low F2 = back
VOWELS = {
    # High front
    'i': Phoneme('i', SourceType.PULSE, 0.15, VocalTract(270, 2300), 130),
    'ɪ': Phoneme('ɪ', SourceType.PULSE, 0.12, VocalTract(390, 2000), 120),
    
    # Mid front
    'e': Phoneme('e', SourceType.PULSE, 0.14, VocalTract(530, 1850), 125),
    'ɛ': Phoneme('ɛ', SourceType.PULSE, 0.13, VocalTract(610, 1900), 120),
    
    # Low front
    'æ': Phoneme('æ', SourceType.PULSE, 0.15, VocalTract(660, 1700), 115),
    
    # Low back
    'a': Phoneme('a', SourceType.PULSE, 0.16, VocalTract(750, 1100), 110),
    'ɑ': Phoneme('ɑ', SourceType.PULSE, 0.16, VocalTract(700, 1150), 110),
    
    # Mid back
    'ɔ': Phoneme('ɔ', SourceType.PULSE, 0.14, VocalTract(570, 850), 115),
    'o': Phoneme('o', SourceType.PULSE, 0.14, VocalTract(460, 900), 120),
    
    # High back
    'ʊ': Phoneme('ʊ', SourceType.PULSE, 0.12, VocalTract(300, 900), 125),
    'u': Phoneme('u', SourceType.PULSE, 0.15, VocalTract(280, 800), 130),
    
    # Central
    'ə': Phoneme('ə', SourceType.PULSE, 0.10, VocalTract(500, 1500), 120),
    'ʌ': Phoneme('ʌ', SourceType.PULSE, 0.12, VocalTract(650, 1200), 115),
}

# CONSONANTS (obstruction types)
CONSONANTS = {
    # Stops (complete closure, then release)
    'p': Phoneme('p', SourceType.NOISE, 0.08, None, 0),  # Voiceless bilabial
    'b': Phoneme('b', SourceType.PULSE, 0.08, VocalTract(200, 800), 120),  # Voiced bilabial
    't': Phoneme('t', SourceType.NOISE, 0.08, None, 0),
    'd': Phoneme('d', SourceType.PULSE, 0.08, VocalTract(200, 1600), 120),
    'k': Phoneme('k', SourceType.NOISE, 0.08, None, 0),
    'g': Phoneme('g', SourceType.PULSE, 0.08, VocalTract(350, 900), 120),
    
    # Fricatives (narrow channel)
    'f': Phoneme('f', SourceType.NOISE, 0.12, VocalTract(300, 2500), 0),  # Labiodental
    'v': Phoneme('v', SourceType.BOTH, 0.12, VocalTract(300, 1600), 120),
    's': Phoneme('s', SourceType.NOISE, 0.15, VocalTract(4000, 6000), 0),  # Alveolar
    'z': Phoneme('z', SourceType.BOTH, 0.15, VocalTract(3500, 5500), 130),
    'ʃ': Phoneme('ʃ', SourceType.NOISE, 0.14, VocalTract(2500, 4500), 0),  # Postalveolar
    'ʒ': Phoneme('ʒ', SourceType.BOTH, 0.14, VocalTract(2200, 3800), 125),
    'h': Phoneme('h', SourceType.NOISE, 0.10, None, 0),  # Glottal
    
    # Nasals (vocal tract + nasal coupling)
    'm': Phoneme('m', SourceType.PULSE, 0.14, VocalTract(300, 1000), 120),
    'n': Phoneme('n', SourceType.PULSE, 0.13, VocalTract(300, 1400), 125),
    'ŋ': Phoneme('ŋ', SourceType.PULSE, 0.14, VocalTract(300, 900), 115),
    
    # Approximants (semi-vowels)
    'l': Phoneme('l', SourceType.PULSE, 0.12, VocalTract(400, 1400), 125),
    'r': Phoneme('r', SourceType.PULSE, 0.12, VocalTract(400, 1200), 120),
    'w': Phoneme('w', SourceType.PULSE, 0.10, VocalTract(300, 800), 120),
    'j': Phoneme('j', SourceType.PULSE, 0.10, VocalTract(300, 2100), 130),
}

ALL_PHONEMES = {**VOWELS, **CONSONANTS}

class ChristKeyVoice:
    """Complete speech synthesizer"""
    
    def __init__(self, base_pitch: float = 120):
        self.base_pitch = base_pitch
        
    def say(self, text: str) -> np.ndarray:
        """Synthesize text to audio"""
        phonemes = self._text_to_phonemes(text.lower())
        return self._concatenate(phonemes)
    
    def _text_to_phonemes(self, text: str) -> List[Phoneme]:
        """Simple text-to-phoneme conversion"""
        # Map letters to phonemes
        result = []
        i = 0
        while i < len(text):
            char = text[i]
            
            # Check digraphs first
            if i + 1 < len(text):
                pair = text[i:i+2]
                if pair == 'th':
                    # th as t for now (voiceless dental fricative)
                    result.append(CONSONANTS['t'])
                    i += 2
                    continue
                elif pair == 'sh':
                    result.append(CONSONANTS['ʃ'])
                    i += 2
                    continue
                elif pair == 'ch':
                    result.append(CONSONANTS['t'])
                    result.append(CONSONANTS['ʃ'])
                    i += 2
                    continue
                elif pair == 'ng':
                    result.append(CONSONANTS['ŋ'])
                    i += 2
                    continue
            
            # Single character mapping
            if char in ALL_PHONEMES:
                result.append(ALL_PHONEMES[char])
            elif char == 'a':
                result.append(VOWELS['a'])
            elif char == 'e':
                result.append(VOWELS['ə'])
            elif char == 'i':
                result.append(VOWELS['ɪ'])
            elif char == 'o':
                result.append(VOWELS['o'])
            elif char == 'u':
                result.append(VOWELS['ʌ'])
            elif char == 'y':
                result.append(VOWELS['i'])
            elif char == 'r':
                result.append(CONSONANTS['r'])
            elif char == 'l':
                result.append(CONSONANTS['l'])
            elif char == 'w':
                result.append(CONSONANTS['w'])
            elif char == 'h':
                result.append(CONSONANTS['h'])
            elif char in 'bcdfghjklmnpqrstvwxyz':
                result.append(CONSONANTS.get(char, CONSONANTS['h']))
            
            i += 1
        
        return result
    
    def _concatenate(self, phonemes: List[Phoneme]) -> np.ndarray:
        """Join phonemes with smoothing"""
        if not phonemes:
            return np.array([])
        
        segments = [p.synthesize() for p in phonemes]
        
        # Simple concatenation for now
        return np.concatenate(segments)
    
    def save(self, audio: np.ndarray, filename: str):
        """Save to WAV"""
        audio_int = (audio * 32767).astype(np.int16)
        with wave.open(filename, 'w') as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(SAMPLE_RATE)
            f.writeframes(audio_int.tobytes())
        return filename


def main():
    voice = ChristKeyVoice(base_pitch=120)
    
    # Test
    text = "hello"
    print(f"Synthesizing: '{text}'")
    
    audio = voice.say(text)
    output = "/root/.openclaw/workspace/christkey-native/hello_v2.wav"
    voice.save(audio, output)
    
    print(f"Generated: {output}")
    print(f"Duration: {len(audio)/SAMPLE_RATE:.2f}s")

if __name__ == "__main__":
    main()

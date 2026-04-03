#!/usr/bin/env python3
"""
Christ-Key Native Voice Synthesizer v0.3
Proper formant synthesis using resonant bandpass filters
"""

import numpy as np
import wave
from dataclasses import dataclass
from typing import List
from enum import Enum, auto

PHI = 1.618033988749895
SAMPLE_RATE = 22050

def bandpass_filter(signal: np.ndarray, freq: float, bandwidth: float = 100.0) -> np.ndarray:
    """Simple bandpass using FFT - keeps frequencies near 'freq'"""
    if len(signal) < 10:
        return signal
    
    # FFT
    fft = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(len(signal), 1/SAMPLE_RATE)
    
    # Create mask: 1.0 at target freq, tapering off
    mask = np.exp(-((freqs - freq) ** 2) / (2 * bandwidth ** 2))
    mask += np.exp(-((freqs + freq) ** 2) / (2 * bandwidth ** 2))  # Negative frequencies
    
    # Apply filter
    filtered_fft = fft * mask
    
    # Inverse FFT
    return np.fft.irfft(filtered_fft, n=len(signal))

def resonator(signal: np.ndarray, freq: float, bw: float = 80.0, gain: float = 1.0) -> np.ndarray:
    """Resonant peak filter - amplifies region around freq"""
    # Simple approach: bandpass + mix back with original
    bp = bandpass_filter(signal, freq, bw)
    return signal + gain * bp

class SourceType(Enum):
    PULSE = auto()
    NOISE = auto()
    BOTH = auto()

@dataclass
class Phoneme:
    symbol: str
    source: SourceType
    duration: float
    f1: float = None  # First formant
    f2: float = None  # Second formant
    f0: float = 120   # Pitch
    
    def synthesize(self) -> np.ndarray:
        samples = int(SAMPLE_RATE * self.duration)
        t = np.arange(samples) / SAMPLE_RATE
        
        # Generate source
        if self.source == SourceType.PULSE:
            source = self._glottal_pulse(samples, t)
        elif self.source == SourceType.NOISE:
            source = np.random.uniform(-0.5, 0.5, samples)
        else:  # BOTH
            pulse = self._glottal_pulse(samples, t)
            noise = np.random.uniform(-0.3, 0.3, samples)
            source = 0.6 * pulse + 0.4 * noise
        
        # Apply formant filtering (vocal tract resonance)
        if self.f1 and self.f2:
            output = resonator(source, self.f1, 90, 2.0)
            output = resonator(output, self.f2, 110, 1.5)
            output = resonator(output, 2500, 150, 0.8)  # F3
        else:
            output = source
        
        # Envelope
        output = self._envelope(output)
        
        # Normalize
        max_amp = np.max(np.abs(output))
        if max_amp > 0:
            output = output / max_amp * 0.7
        
        return output
    
    def _glottal_pulse(self, samples: int, t: np.ndarray) -> np.ndarray:
        """Liljencrants-Fant glottal pulse model"""
        period = 1.0 / self.f0
        phase = (t % period) / period
        
        # Asymmetrical pulse (more realistic than sine)
        # Rising portion (open phase)
        og = 0.6  # open quotient
        pulse = np.zeros_like(t)
        
        mask = phase < og
        # Rosenberg pulse derivative approximation
        pulse[mask] = np.sin(np.pi * phase[mask] / og) ** 2
        
        return pulse
    
    def _envelope(self, signal: np.ndarray) -> np.ndarray:
        """Attack-sustain-release"""
        n = len(signal)
        attack = min(int(0.015 * SAMPLE_RATE), n // 4)
        release = min(int(0.025 * SAMPLE_RATE), n // 4)
        
        env = np.ones(n)
        if attack > 0:
            env[:attack] = np.linspace(0, 1, attack)
        if release > 0:
            env[-release:] = np.linspace(1, 0, release)
        
        return signal * env

# VOWELS - F1 (height: low=high Hz, high=low Hz), F2 (front/back: front=high Hz, back=low Hz)
VOWELS = {
    'i':  Phoneme('i',  SourceType.PULSE, 0.18, 280,  2250, 130),  # beat - high front
    'ɪ':  Phoneme('ɪ',  SourceType.PULSE, 0.14, 400,  2000, 125),  # bit
    'e':  Phoneme('e',  SourceType.PULSE, 0.16, 550,  1850, 125),  # bait - mid front
    'ɛ':  Phoneme('ɛ',  SourceType.PULSE, 0.15, 650,  1750, 120),  # bet
    'æ':  Phoneme('æ',  SourceType.PULSE, 0.17, 750,  1650, 115),  # bat - low front
    'a':  Phoneme('a',  SourceType.PULSE, 0.18, 800,  1200, 110),  # father - low central
    'ɑ':  Phoneme('ɑ',  SourceType.PULSE, 0.18, 700,  1100, 110),  # hot - low back
    'ɔ':  Phoneme('ɔ',  SourceType.PULSE, 0.16, 600,  900,  115),  # law - mid back
    'o':  Phoneme('o',  SourceType.PULSE, 0.16, 500,  850,  120),  # go
    'ʊ':  Phoneme('ʊ',  SourceType.PULSE, 0.14, 450,  950,  125),  # put
    'u':  Phoneme('u',  SourceType.PULSE, 0.17, 320,  800,  130),  # boot - high back
    'ə':  Phoneme('ə',  SourceType.PULSE, 0.12, 500,  1400, 120),  # about - schwa
    'ʌ':  Phoneme('ʌ',  SourceType.PULSE, 0.15, 650,  1200, 115),  # cut
}

# CONSONANTS
CONSONANTS = {
    # Stops
    'p': Phoneme('p', SourceType.NOISE, 0.08),  # Silence burst
    'b': Phoneme('b', SourceType.PULSE, 0.10, 250, 800, 120),
    't': Phoneme('t', SourceType.NOISE, 0.08),
    'd': Phoneme('d', SourceType.PULSE, 0.10, 250, 1600, 125),
    'k': Phoneme('k', SourceType.NOISE, 0.08),
    'g': Phoneme('g', SourceType.PULSE, 0.10, 350, 900, 120),
    
    # Fricatives
    'f': Phoneme('f', SourceType.NOISE, 0.14, None, None, 0),  # Flat spectrum
    'v': Phoneme('v', SourceType.BOTH, 0.14, 300, 1400, 125),
    's': Phoneme('s', SourceType.NOISE, 0.16, None, None, 0),  # High freq emphasis
    'z': Phoneme('z', SourceType.BOTH, 0.16, 3500, 5000, 130),
    'ʃ': Phoneme('ʃ', SourceType.NOISE, 0.15, None, None, 0),
    'h': Phoneme('h', SourceType.NOISE, 0.12, None, None, 0),
    
    # Nasals
    'm': Phoneme('m', SourceType.PULSE, 0.16, 300, 900, 115),
    'n': Phoneme('n', SourceType.PULSE, 0.15, 300, 1300, 120),
    'ŋ': Phoneme('ŋ', SourceType.PULSE, 0.16, 300, 800, 115),
    
    # Approximants
    'l': Phoneme('l', SourceType.PULSE, 0.14, 350, 1200, 125),
    'r': Phoneme('r', SourceType.PULSE, 0.14, 350, 1100, 120),
    'w': Phoneme('w', SourceType.PULSE, 0.12, 300, 700, 120),
    'j': Phoneme('j', SourceType.PULSE, 0.12, 280, 2100, 130),
}

ALL = {**VOWELS, **CONSONANTS}

class Voice:
    def __init__(self, pitch=120):
        self.pitch = pitch
    
    def say(self, text: str) -> np.ndarray:
        phonemes = self._to_phonemes(text.lower())
        if not phonemes:
            return np.array([])
        
        # Generate and overlap
        segments = [p.synthesize() for p in phonemes]
        return self._overlap(segments, 30)  # 30ms crossfade
    
    def _to_phonemes(self, text: str) -> List[Phoneme]:
        result = []
        i = 0
        while i < len(text):
            # Digraphs
            if i + 1 < len(text):
                pair = text[i:i+2]
                if pair == 'sh':
                    result.append(CONSONANTS['ʃ'])
                    i += 2
                    continue
                elif pair == 'th':
                    result.append(CONSONANTS['t'])
                    i += 2
                    continue
                elif pair == 'ch':
                    result.extend([CONSONANTS['t'], CONSONANTS['ʃ']])
                    i += 2
                    continue
                elif pair == 'ng':
                    result.append(CONSONANTS['ŋ'])
                    i += 2
                    continue
            
            char = text[i]
            if char in ALL:
                result.append(ALL[char])
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
            elif char in 'bcdfghjklmnpqrstvwxyz':
                result.append(CONSONANTS.get(char, CONSONANTS['h']))
            
            i += 1
        return result
    
    def _overlap(self, segments: List[np.ndarray], fade_ms: int) -> np.ndarray:
        """Concatenate with crossfade"""
        if not segments:
            return np.array([])
        if len(segments) == 1:
            return segments[0]
        
        fade = int(fade_ms * SAMPLE_RATE / 1000)
        result = segments[0]
        
        for seg in segments[1:]:
            if len(result) > fade and len(seg) > fade:
                # Crossfade
                fade_out = np.linspace(1, 0, fade)
                fade_in = np.linspace(0, 1, fade)
                overlap = result[-fade:] * fade_out + seg[:fade] * fade_in
                result = np.concatenate([result[:-fade], overlap, seg[fade:]])
            else:
                result = np.concatenate([result, seg])
        
        return result
    
    def save(self, audio: np.ndarray, path: str):
        audio_int = (audio * 32767).astype(np.int16)
        with wave.open(path, 'w') as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(SAMPLE_RATE)
            f.writeframes(audio_int.tobytes())
        return path

if __name__ == "__main__":
    v = Voice(pitch=120)
    
    # Test vowels
    for vname in ['a', 'i', 'u']:
        audio = VOWELS[vname].synthesize()
        v.save(audio, f'/root/.openclaw/workspace/christkey-native/vowel_{vname}.wav')
        print(f'Vowel /{vname}/ saved')
    
    # Test word
    audio = v.say("hello")
    v.save(audio, '/root/.openclaw/workspace/christkey-native/hello_v3.wav')
    print(f'Hello saved, duration: {len(audio)/SAMPLE_RATE:.2f}s')

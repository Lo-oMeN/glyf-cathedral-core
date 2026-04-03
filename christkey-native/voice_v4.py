#!/usr/bin/env python3
"""
Christ-Key Native Voice Synthesizer v0.4
Smoother synthesis with natural jitter
"""

import numpy as np
import wave
from dataclasses import dataclass
from typing import List
from enum import Enum, auto

SAMPLE_RATE = 22050

def smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
    """Smooth Hermite interpolation"""
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)

def bandpass_resonator(signal: np.ndarray, freq: float, bw: float, gain: float = 1.0) -> np.ndarray:
    """Gentler resonator using IIR-style approach in time domain"""
    if len(signal) < 10:
        return signal
    
    # Simple damped oscillator at formant frequency
    t = np.arange(len(signal)) / SAMPLE_RATE
    envelope = np.exp(-np.pi * bw * t)  # Decay
    carrier = np.sin(2 * np.pi * freq * t)
    
    # Convolve with impulse response (simplified)
    impulse = envelope * carrier
    
    # Manual convolution (simplified, just first-order)
    output = signal.copy()
    window = int(0.005 * SAMPLE_RATE)  # 5ms impulse response
    
    for i in range(len(signal)):
        for j in range(min(window, len(signal) - i)):
            output[i] += gain * 0.1 * signal[i] * impulse[j]
    
    return signal + gain * bandpass_fft(signal, freq, bw)

def bandpass_fft(signal: np.ndarray, freq: float, bw: float) -> np.ndarray:
    """Gentler FFT bandpass with windowing"""
    if len(signal) < 256:
        return signal
    
    # Apply window to reduce artifacts
    window = np.hanning(len(signal))
    windowed = signal * window
    
    fft = np.fft.rfft(windowed)
    freqs = np.fft.rfftfreq(len(signal), 1/SAMPLE_RATE)
    
    # Softer Gaussian response (not sharp cutoff)
    response = np.exp(-((freqs - freq) ** 2) / (2 * (bw/2) ** 2))
    
    filtered_fft = fft * response
    result = np.fft.irfft(filtered_fft, n=len(signal))
    
    # Remove window effect
    return result / (window + 0.001)

class SourceType(Enum):
    PULSE = auto()
    NOISE = auto()
    BOTH = auto()

@dataclass
class Phoneme:
    symbol: str
    source: SourceType
    duration: float
    f1: float = None
    f2: float = None
    f0: float = 120
    
    def synthesize(self) -> np.ndarray:
        samples = int(SAMPLE_RATE * self.duration)
        t = np.arange(samples) / SAMPLE_RATE
        
        # SOURCE with natural jitter
        if self.source == SourceType.PULSE:
            source = self._glottal_pulse_jitter(samples, t)
        elif self.source == SourceType.NOISE:
            # Softer noise
            source = np.random.normal(0, 0.3, samples)
            source = np.convolve(source, np.ones(5)/5, mode='same')  # Smooth
        else:
            pulse = self._glottal_pulse_jitter(samples, t)
            noise = np.random.normal(0, 0.2, samples)
            noise = np.convolve(noise, np.ones(3)/3, mode='same')
            source = 0.7 * pulse + 0.3 * noise
        
        # FORMANTS - gentler filtering
        if self.f1 and self.f2:
            # Cascade of gentle resonators
            output = bandpass_fft(source, self.f1, 120)
            output = bandpass_fft(output, self.f2, 150)
            output = bandpass_fft(output, 2500, 200)
            
            # Mix with original (less filtered sound)
            output = 0.6 * output + 0.4 * source
        else:
            output = source
        
        # Gentle envelope
        output = self._soft_envelope(output)
        
        # Normalize gently
        max_amp = np.max(np.abs(output))
        if max_amp > 0:
            output = output / max_amp * 0.6
        
        return output
    
    def _glottal_pulse_jitter(self, samples: int, t: np.ndarray) -> np.ndarray:
        """Glottal pulse with natural pitch variation"""
        period = 1.0 / self.f0
        
        # Add jitter (1-2% pitch variation)
        jitter = 1 + np.random.normal(0, 0.015, samples)
        
        phase = np.zeros(samples)
        current_phase = 0
        for i in range(samples):
            current_period = period * jitter[i]
            current_phase += 1.0 / SAMPLE_RATE / current_period
            if current_phase >= 1:
                current_phase -= 1
            phase[i] = current_phase
        
        # Smoother glottal pulse (Liljencrants-Fant)
        og = 0.7  # open quotient
        pulse = np.zeros(samples)
        
        mask = phase < og
        # Smoother opening
        theta = np.pi * phase[mask] / og
        pulse[mask] = 0.5 * (1 - np.cos(theta))
        
        # Gentler closing (exponential decay instead of cutoff)
        closing = phase >= og
        decay_pos = (phase[closing] - og) / (1 - og)
        pulse[closing] = np.exp(-3 * decay_pos)
        
        return pulse
    
    def _soft_envelope(self, signal: np.ndarray) -> np.ndarray:
        """Smoother attack/release"""
        n = len(signal)
        attack = min(int(0.025 * SAMPLE_RATE), n // 3)
        release = min(int(0.035 * SAMPLE_RATE), n // 3)
        
        env = np.ones(n)
        if attack > 0:
            env[:attack] = smoothstep(0, 1, np.linspace(0, 1, attack))
        if release > 0:
            env[-release:] = 1 - smoothstep(0, 1, np.linspace(0, 1, release))
        
        return signal * env

# VOWELS - adjusted for more natural sound
VOWELS = {
    'i':  Phoneme('i',  SourceType.PULSE, 0.20, 300,  2200, 125),
    'ɪ':  Phoneme('ɪ',  SourceType.PULSE, 0.16, 420,  1950, 120),
    'e':  Phoneme('e',  SourceType.PULSE, 0.18, 580,  1800, 120),
    'ɛ':  Phoneme('ɛ',  SourceType.PULSE, 0.17, 680,  1700, 115),
    'æ':  Phoneme('æ',  SourceType.PULSE, 0.20, 780,  1600, 110),
    'a':  Phoneme('a',  SourceType.PULSE, 0.22, 850,  1150, 105),
    'ɑ':  Phoneme('ɑ',  SourceType.PULSE, 0.22, 750,  1050, 105),
    'ɔ':  Phoneme('ɔ',  SourceType.PULSE, 0.18, 620,  880,  110),
    'o':  Phoneme('o',  SourceType.PULSE, 0.18, 520,  820,  115),
    'ʊ':  Phoneme('ʊ',  SourceType.PULSE, 0.16, 480,  920,  120),
    'u':  Phoneme('u',  SourceType.PULSE, 0.20, 350,  780,  125),
    'ə':  Phoneme('ə',  SourceType.PULSE, 0.14, 520,  1350, 115),
    'ʌ':  Phoneme('ʌ',  SourceType.PULSE, 0.17, 680,  1150, 110),
}

CONSONANTS = {
    'p': Phoneme('p', SourceType.NOISE, 0.06),
    'b': Phoneme('b', SourceType.PULSE, 0.10, 280, 750, 115),
    't': Phoneme('t', SourceType.NOISE, 0.06),
    'd': Phoneme('d', SourceType.PULSE, 0.10, 280, 1500, 120),
    'k': Phoneme('k', SourceType.NOISE, 0.06),
    'g': Phoneme('g', SourceType.PULSE, 0.10, 380, 850, 115),
    'f': Phoneme('f', SourceType.NOISE, 0.12),
    'v': Phoneme('v', SourceType.BOTH, 0.14, 320, 1300, 120),
    's': Phoneme('s', SourceType.NOISE, 0.16),
    'z': Phoneme('z', SourceType.BOTH, 0.16, 3600, 4800, 125),
    'ʃ': Phoneme('ʃ', SourceType.NOISE, 0.14),
    'h': Phoneme('h', SourceType.NOISE, 0.10),
    'm': Phoneme('m', SourceType.PULSE, 0.18, 320, 850, 110),
    'n': Phoneme('n', SourceType.PULSE, 0.17, 320, 1250, 115),
    'ŋ': Phoneme('ŋ', SourceType.PULSE, 0.18, 320, 750, 110),
    'l': Phoneme('l', SourceType.PULSE, 0.16, 380, 1150, 120),
    'r': Phoneme('r', SourceType.PULSE, 0.16, 380, 1050, 115),
    'w': Phoneme('w', SourceType.PULSE, 0.14, 320, 680, 115),
    'j': Phoneme('j', SourceType.PULSE, 0.14, 300, 2000, 125),
}

ALL = {**VOWELS, **CONSONANTS}

class Voice:
    def __init__(self, pitch=115):
        self.pitch = pitch
    
    def say(self, text: str) -> np.ndarray:
        phonemes = self._to_phonemes(text.lower())
        if not phonemes:
            return np.array([])
        
        segments = [p.synthesize() for p in phonemes]
        return self._blend(segments, 40)  # 40ms blend
    
    def _to_phonemes(self, text: str) -> List[Phoneme]:
        result = []
        i = 0
        while i < len(text):
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
    
    def _blend(self, segments: List[np.ndarray], fade_ms: int) -> np.ndarray:
        if not segments:
            return np.array([])
        if len(segments) == 1:
            return segments[0]
        
        fade = int(fade_ms * SAMPLE_RATE / 1000)
        result = segments[0]
        
        for seg in segments[1:]:
            if len(result) > fade and len(seg) > fade:
                # Smooth crossfade
                fade_out = np.cos(np.linspace(0, np.pi/2, fade)) ** 2
                fade_in = np.sin(np.linspace(0, np.pi/2, fade)) ** 2
                overlap = result[-fade:] * fade_out + seg[:fade] * fade_in
                result = np.concatenate([result[:-fade], overlap, seg[fade:]])
            else:
                result = np.concatenate([result, seg])
        
        return result
    
    def save(self, audio: np.ndarray, path: str):
        audio_int = np.clip(audio * 32767, -32768, 32767).astype(np.int16)
        with wave.open(path, 'w') as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(SAMPLE_RATE)
            f.writeframes(audio_int.tobytes())
        return path

if __name__ == "__main__":
    v = Voice(pitch=115)
    
    # Test
    audio = v.say("hello")
    v.save(audio, '/root/.openclaw/workspace/christkey-native/hello_v4.wav')
    print(f'Hello v4: {len(audio)/SAMPLE_RATE:.2f}s')
    
    # Vowels
    for vname in ['a', 'i', 'u']:
        audio = VOWELS[vname].synthesize()
        v.save(audio, f'/root/.openclaw/workspace/christkey-native/v4_{vname}.wav')

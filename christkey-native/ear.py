#!/usr/bin/env python3
"""
Christ-Key Voice Ear — Automated feedback loop for synthesis
Compares output against target, suggests corrections
"""

import numpy as np
import wave
import struct
from dataclasses import dataclass
from typing import Dict, Tuple, List
import json

SAMPLE_RATE = 22050

@dataclass
class TargetProfile:
    """Target acoustic profile for a phoneme"""
    f1: float  # First formant (Hz)
    f2: float  # Second formant (Hz)
    f3: float = 2500  # Third formant (Hz)
    f0: float = 120  # Pitch (Hz)
    bandwidth_f1: float = 90
    bandwidth_f2: float = 110
    aspiration: float = 0.1  # Amount of breathiness
    
@dataclass
class MeasuredProfile:
    """What we actually got"""
    f1: float
    f2: float
    f3: float
    f0: float
    centroid: float
    high_freq_ratio: float

def load_audio(wav_path: str) -> np.ndarray:
    """Load WAV file as normalized float array"""
    with wave.open(wav_path, 'rb') as f:
        n_channels = f.getnchannels()
        sample_width = f.getsampwidth()
        n_frames = f.getnframes()
        frames = f.readframes(n_frames)
        
        if sample_width == 2:
            audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
        else:
            audio = np.frombuffer(frames, dtype=np.uint8).astype(np.float32) / 128.0 - 1.0
        
        if n_channels == 2:
            audio = audio[::2]
        
        # Remove DC offset
        audio = audio - np.mean(audio)
        
        return audio

def measure_formants(audio: np.ndarray, sr: int) -> Tuple[float, float, float]:
    """Measure F1, F2, F3 from spectrum using peak picking"""
    # Windowed FFT for cleaner spectrum
    window = np.hanning(len(audio))
    fft = np.fft.rfft(audio * window)
    freqs = np.fft.rfftfreq(len(audio), 1/sr)
    magnitude = np.abs(fft)
    
    # Smooth spectrum
    kernel = np.ones(5) / 5
    smoothed = np.convolve(magnitude, kernel, mode='same')
    
    def find_peak_in_range(low, high):
        mask = (freqs >= low) & (freqs <= high)
        if not np.any(mask):
            return None
        region = smoothed.copy()
        region[~mask] = 0
        peak_idx = np.argmax(region)
        return float(freqs[peak_idx])
    
    f1 = find_peak_in_range(150, 1000) or 500
    f2 = find_peak_in_range(600, 3000) or 1500
    f3 = find_peak_in_range(1500, 4000) or 2500
    
    return f1, f2, f3

def measure_f0(audio: np.ndarray, sr: int) -> float:
    """Estimate fundamental frequency using autocorrelation"""
    # Simple autocorrelation
    corr = np.correlate(audio, audio, mode='full')
    corr = corr[len(corr)//2:]
    
    # Find first peak (excluding zero lag)
    # Search in reasonable F0 range (80-300 Hz)
    min_lag = int(sr / 300)
    max_lag = int(sr / 80)
    
    if max_lag >= len(corr):
        max_lag = len(corr) - 1
    
    search_region = corr[min_lag:max_lag]
    if len(search_region) == 0:
        return 120.0
    
    peak_idx = np.argmax(search_region) + min_lag
    f0 = sr / peak_idx
    
    return float(f0)

def analyze_audio(audio: np.ndarray, sr: int) -> MeasuredProfile:
    """Full analysis of audio"""
    f1, f2, f3 = measure_formants(audio, sr)
    f0 = measure_f0(audio, sr)
    
    # Spectral centroid
    fft = np.fft.rfft(audio)
    freqs = np.fft.rfftfreq(len(audio), 1/sr)
    magnitude = np.abs(fft)
    centroid = np.sum(freqs * magnitude) / np.sum(magnitude)
    
    # High frequency ratio
    high_mask = freqs > 4000
    high_energy = np.sum(magnitude[high_mask])
    total_energy = np.sum(magnitude)
    high_ratio = high_energy / total_energy if total_energy > 0 else 0
    
    return MeasuredProfile(f1, f2, f3, f0, float(centroid), float(high_ratio))

def calculate_errors(measured: MeasuredProfile, target: TargetProfile) -> Dict:
    """Calculate how far off we are"""
    errors = {
        'f1_error_hz': measured.f1 - target.f1,
        'f1_error_pct': ((measured.f1 - target.f1) / target.f1) * 100,
        'f2_error_hz': measured.f2 - target.f2,
        'f2_error_pct': ((measured.f2 - target.f2) / target.f2) * 100,
        'f3_error_hz': measured.f3 - target.f3,
        'f0_error_hz': measured.f0 - target.f0,
        'brightness': measured.centroid,  # Higher = brighter
        'high_freq': measured.high_freq_ratio * 100,  # Percentage
    }
    return errors

def suggest_fixes(errors: Dict, target: TargetProfile) -> List[str]:
    """Generate suggestions based on errors"""
    fixes = []
    
    # F1 issues (vowel height)
    if abs(errors['f1_error_pct']) > 20:
        if errors['f1_error_hz'] < 0:
            fixes.append(f"F1 too LOW by {-errors['f1_error_hz']:.0f}Hz → Increase F1 resonance gain or lower bandwidth")
        else:
            fixes.append(f"F1 too HIGH by {errors['f1_error_hz']:.0f}Hz → Decrease F1 resonance gain")
    
    # F2 issues (front/back)
    if abs(errors['f2_error_pct']) > 20:
        if errors['f2_error_hz'] < 0:
            fixes.append(f"F2 too LOW by {-errors['f2_error_hz']:.0f}Hz → Increase F2 gain (critical for vowel identity)")
        else:
            fixes.append(f"F2 too HIGH by {errors['f2_error_hz']:.0f}Hz → Decrease F2 gain")
    
    # Brightness issues
    if errors['brightness'] < 800:
        fixes.append(f"Too DARK (centroid {errors['brightness']:.0f}Hz) → Add high-freq aspiration noise")
    
    if errors['high_freq'] < 10:
        fixes.append(f"Too MUFFLED ({errors['high_freq']:.1f}% high freq) → Increase frication/aspiration")
    
    if not fixes:
        fixes.append("Formants within tolerance ✓")
    
    return fixes

def analyze_phoneme(wav_path: str, target: TargetProfile, name: str = "phoneme"):
    """Complete analysis with feedback"""
    audio = load_audio(wav_path)
    measured = analyze_audio(audio, SAMPLE_RATE)
    errors = calculate_errors(measured, target)
    fixes = suggest_fixes(errors, target)
    
    print(f"\n{'='*60}")
    print(f"ANALYSIS: {name}")
    print(f"{'='*60}")
    
    print(f"\n[TARGET vs MEASURED]")
    print(f"  F1: {target.f1:.0f}Hz target → {measured.f1:.0f}Hz measured " +
          f"({errors['f1_error_pct']:+.1f}%)")
    print(f"  F2: {target.f2:.0f}Hz target → {measured.f2:.0f}Hz measured " +
          f"({errors['f2_error_pct']:+.1f}%)")
    print(f"  F3: {target.f3:.0f}Hz target → {measured.f3:.0f}Hz measured")
    print(f"  F0: {target.f0:.0f}Hz target → {measured.f0:.0f}Hz measured")
    
    print(f"\n[SPECTRAL QUALITY]")
    print(f"  Centroid: {measured.centroid:.0f}Hz (brightness)")
    print(f"  High Freq: {measured.high_freq_ratio*100:.1f}%")
    
    print(f"\n[SUGGESTED FIXES]")
    for fix in fixes:
        print(f"  → {fix}")
    
    print(f"{'='*60}\n")
    
    return {
        'target': target,
        'measured': measured,
        'errors': errors,
        'fixes': fixes
    }

# Target profiles for common vowels
VOWEL_TARGETS = {
    'a': TargetProfile(f1=850, f2=1150, f3=2500, f0=105, bandwidth_f1=80, bandwidth_f2=100, aspiration=0.15),
    'i': TargetProfile(f1=300, f2=2250, f3=2900, f0=125, bandwidth_f1=60, bandwidth_f2=120, aspiration=0.1),
    'u': TargetProfile(f1=320, f2=800, f3=2200, f0=125, bandwidth_f1=70, bandwidth_f2=90, aspiration=0.08),
    'e': TargetProfile(f1=550, f2=1850, f3=2600, f0=120, bandwidth_f1=75, bandwidth_f2=110, aspiration=0.12),
    'o': TargetProfile(f1=500, f2=850, f3=2400, f0=115, bandwidth_f1=80, bandwidth_f2=95, aspiration=0.1),
}

if __name__ == "__main__":
    import sys
    
    # Analyze our test vowels
    test_files = [
        ("/root/.openclaw/workspace/christkey-native/v4_a.wav", VOWEL_TARGETS['a'], "/a/ (father)"),
        ("/root/.openclaw/workspace/christkey-native/v4_i.wav", VOWEL_TARGETS['i'], "/i/ (beat)"),
        ("/root/.openclaw/workspace/christkey-native/v4_u.wav", VOWEL_TARGETS['u'], "/u/ (boot)"),
    ]
    
    for path, target, name in test_files:
        try:
            analyze_phoneme(path, target, name)
        except Exception as e:
            print(f"Error analyzing {name}: {e}")

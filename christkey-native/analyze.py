#!/usr/bin/env python3
"""
Christ-Key Audio Analyzer
Visual waveform analysis for voice synthesis debugging
"""

import numpy as np
import wave
import struct
from pathlib import Path

SAMPLE_RATE = 22050

def analyze_audio(wav_path: str):
    """Full audio analysis - returns dict of measurements"""
    
    # Load audio
    with wave.open(wav_path, 'rb') as f:
        n_channels = f.getnchannels()
        sample_width = f.getsampwidth()
        framerate = f.getframerate()
        n_frames = f.getnframes()
        
        frames = f.readframes(n_frames)
        
        # Convert to numpy
        if sample_width == 2:
            audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
        else:
            audio = np.frombuffer(frames, dtype=np.uint8).astype(np.float32) / 128.0 - 1.0
        
        # Convert to mono
        if n_channels == 2:
            audio = audio[::2]  # Left channel only
    
    # Analysis
    results = {
        "duration": len(audio) / framerate,
        "sample_rate": framerate,
        "peak_amplitude": float(np.max(np.abs(audio))),
        "rms_energy": float(np.sqrt(np.mean(audio**2))),
        "zero_crossings": int(np.sum(np.diff(np.sign(audio)) != 0)),
        "spectral_features": analyze_spectrum(audio, framerate),
        "formant_estimate": estimate_formants(audio, framerate),
        "issues": identify_issues(audio, framerate)
    }
    
    return results

def analyze_spectrum(audio: np.ndarray, sr: int) -> dict:
    """Extract spectral features"""
    # FFT
    fft = np.fft.rfft(audio)
    freqs = np.fft.rfftfreq(len(audio), 1/sr)
    magnitude = np.abs(fft)
    
    # Spectral centroid (brightness)
    centroid = np.sum(freqs * magnitude) / np.sum(magnitude)
    
    # Spectral rolloff (where 85% of energy is below)
    cumulative = np.cumsum(magnitude)
    rolloff_idx = np.where(cumulative >= 0.85 * cumulative[-1])[0][0]
    rolloff = freqs[rolloff_idx]
    
    # Find peaks (harmonics)
    peaks = []
    for i in range(1, len(magnitude)-1):
        if magnitude[i] > magnitude[i-1] and magnitude[i] > magnitude[i+1]:
            if magnitude[i] > np.max(magnitude) * 0.1:  # Significant peak
                peaks.append((float(freqs[i]), float(magnitude[i])))
    
    # Top 5 peaks
    peaks.sort(key=lambda x: x[1], reverse=True)
    top_peaks = peaks[:5]
    
    return {
        "centroid_hz": float(centroid),
        "rolloff_hz": float(rolloff),
        "top_peaks": [(f, float(m/np.max(magnitude))) for f, m in top_peaks],
        "high_freq_ratio": float(np.sum(magnitude[freqs > 4000]) / np.sum(magnitude))
    }

def estimate_formants(audio: np.ndarray, sr: int) -> dict:
    """Estimate F1, F2, F3 from spectrum"""
    # Use LPC-like approach (simplified)
    window = np.hanning(len(audio))
    fft = np.fft.rfft(audio * window)
    freqs = np.fft.rfftfreq(len(audio), 1/sr)
    magnitude = np.abs(fft)
    
    # Look for peaks in formant regions
    f1_region = (200, 900)    # Vowel height
    f2_region = (700, 2500)   # Front/back
    f3_region = (2000, 3500)  # Rounding
    
    def find_peak(freq_range):
        mask = (freqs >= freq_range[0]) & (freqs <= freq_range[1])
        if not np.any(mask):
            return None
        region_mag = magnitude.copy()
        region_mag[~mask] = 0
        peak_idx = np.argmax(region_mag)
        return float(freqs[peak_idx])
    
    return {
        "f1_estimate": find_peak(f1_region),
        "f2_estimate": find_peak(f2_region),
        "f3_estimate": find_peak(f3_region)
    }

def identify_issues(audio: np.ndarray, sr: int) -> list:
    """Identify synthesis problems"""
    issues = []
    
    # Check for clipping
    if np.max(np.abs(audio)) > 0.95:
        issues.append("clipping")
    
    # Check for DC offset
    if abs(np.mean(audio)) > 0.01:
        issues.append("dc_offset")
    
    # Check for excessive silence at start/end
    start_nonzero = np.where(np.abs(audio) > 0.001)[0]
    if len(start_nonzero) > 0:
        silence_start = start_nonzero[0] / sr
        silence_end = (len(audio) - start_nonzero[-1]) / sr
        if silence_start > 0.1:
            issues.append(f"leading_silence_{silence_start:.3f}s")
        if silence_end > 0.1:
            issues.append(f"trailing_silence_{silence_end:.3f}s")
    
    # Check for spectral issues
    fft = np.fft.rfft(audio)
    freqs = np.fft.rfftfreq(len(audio), 1/sr)
    magnitude = np.abs(fft)
    
    # Too much high freq = harsh
    high_energy = np.sum(magnitude[freqs > 6000])
    total_energy = np.sum(magnitude)
    if high_energy / total_energy > 0.3:
        issues.append("excessive_high_freq")
    
    # Too little high freq = muffled
    if high_energy / total_energy < 0.05:
        issues.append("muffled")
    
    return issues

def print_report(wav_path: str):
    """Print formatted analysis"""
    results = analyze_audio(wav_path)
    
    print(f"\n{'='*50}")
    print(f"AUDIO ANALYSIS: {Path(wav_path).name}")
    print(f"{'='*50}")
    
    print(f"\n[Basic Info]")
    print(f"  Duration: {results['duration']:.3f}s")
    print(f"  Sample Rate: {results['sample_rate']} Hz")
    print(f"  Peak Amplitude: {results['peak_amplitude']:.3f}")
    print(f"  RMS Energy: {results['rms_energy']:.3f}")
    
    print(f"\n[Spectral Features]")
    spec = results['spectral_features']
    print(f"  Spectral Centroid: {spec['centroid_hz']:.0f} Hz (brightness)")
    print(f"  Spectral Rolloff: {spec['rolloff_hz']:.0f} Hz")
    print(f"  High Freq Ratio: {spec['high_freq_ratio']:.2%}")
    print(f"  Top Peaks:")
    for freq, mag in spec['top_peaks'][:3]:
        print(f"    {freq:.0f} Hz: {mag:.2f}")
    
    print(f"\n[Formant Estimates]")
    formants = results['formant_estimate']
    for name, value in formants.items():
        if value:
            print(f"  {name.upper()}: {value:.0f} Hz")
        else:
            print(f"  {name.upper()}: not detected")
    
    print(f"\n[Issues Detected]")
    if results['issues']:
        for issue in results['issues']:
            print(f"  ⚠️  {issue}")
    else:
        print(f"  ✅ No major issues")
    
    print(f"\n{'='*50}\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        # Analyze our test files
        files = [
            "/root/.openclaw/workspace/christkey-native/hello_v4.wav",
            "/root/.openclaw/workspace/christkey-native/v4_a.wav",
            "/root/.openclaw/workspace/christkey-native/v4_i.wav"
        ]
        for f in files:
            if Path(f).exists():
                print_report(f)
    else:
        print_report(sys.argv[1])

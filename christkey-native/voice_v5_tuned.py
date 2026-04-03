#!/usr/bin/env python3
"""
Christ-Key Self-Correcting Voice v0.5
Iterative tuning using the Ear feedback loop
"""

import numpy as np
import wave
from dataclasses import dataclass
from typing import Tuple
from ear import analyze_phoneme, TargetProfile, VOWEL_TARGETS, load_audio
import tempfile
import os

SAMPLE_RATE = 22050

@dataclass
class ResonatorParams:
    """Tunable parameters for formant synthesis"""
    f1_gain: float = 2.0
    f2_gain: float = 1.5
    f3_gain: float = 0.8
    f1_bw: float = 80.0  # Bandwidth (Hz)
    f2_bw: float = 100.0
    f3_bw: float = 150.0
    aspiration: float = 0.15  # High-freq noise mix
    source_mix: float = 0.4   # How much unfiltered source to keep

def true_formant_filter(signal: np.ndarray, freq: float, bw: float, gain: float) -> np.ndarray:
    """
    True resonant filter - amplifies harmonics near formant frequency
    Using time-domain damped oscillator approach
    """
    if len(signal) < 10:
        return signal
    
    # Create resonant impulse response
    duration = 0.005  # 5ms decay
    t = np.arange(int(SAMPLE_RATE * duration)) / SAMPLE_RATE
    decay = np.exp(-np.pi * bw * t)
    carrier = np.sin(2 * np.pi * freq * t)
    impulse = decay * carrier
    
    # Convolve (simplified manual implementation)
    output = np.zeros_like(signal)
    for i in range(len(signal)):
        for j, imp in enumerate(impulse):
            if i - j >= 0:
                output[i] += signal[i - j] * imp * gain * 0.01
    
    return signal + output

def generate_vowel(symbol: str, target: TargetProfile, params: ResonatorParams, 
                   duration: float = 0.25) -> np.ndarray:
    """Generate vowel with tunable parameters"""
    
    samples = int(SAMPLE_RATE * duration)
    t = np.arange(samples) / SAMPLE_RATE
    
    # SOURCE: Glottal pulse with jitter
    period = 1.0 / target.f0
    phase = (t % period) / period
    
    # Smoosen pulse (raised cosine)
    og = 0.7
    source = np.zeros(samples)
    mask = phase < og
    source[mask] = 0.5 * (1 - np.cos(np.pi * phase[mask] / og))
    # Exponential decay for closing
    closing = phase >= og
    decay_pos = (phase[closing] - og) / (1 - og)
    source[closing] = np.exp(-3 * decay_pos)
    
    # ASPIRATION: High-freq noise for brightness
    noise = np.random.normal(0, 0.3, samples)
    # High-pass the noise (simplified: difference filter)
    high_freq_noise = np.diff(noise, prepend=noise[0])
    high_freq_noise = np.convolve(high_freq_noise, np.ones(3)/3, mode='same')
    
    mixed_source = (1 - params.aspiration) * source + params.aspiration * high_freq_noise
    
    # FORMANT FILTERING: Cascade of resonators
    output = mixed_source
    output = true_formant_filter(output, target.f1, params.f1_bw, params.f1_gain)
    output = true_formant_filter(output, target.f2, params.f2_bw, params.f2_gain)
    output = true_formant_filter(output, target.f3, params.f3_bw, params.f3_gain)
    
    # Mix with source (less filtered sound)
    output = params.source_mix * mixed_source + (1 - params.source_mix) * output
    
    # Soft envelope
    attack = int(0.02 * SAMPLE_RATE)
    release = int(0.03 * SAMPLE_RATE)
    env = np.ones(samples)
    env[:attack] = np.linspace(0, 1, attack)
    env[-release:] = np.linspace(1, 0, release)
    output = output * env
    
    # Normalize
    max_amp = np.max(np.abs(output))
    if max_amp > 0:
        output = output / max_amp * 0.6
    
    return output

def save_audio(audio: np.ndarray, path: str):
    """Save to WAV"""
    audio_int = np.clip(audio * 32767, -32768, 32767).astype(np.int16)
    with wave.open(path, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(audio_int.tobytes())
    return path

def iterative_tune(vowel_name: str, target: TargetProfile, max_iterations: int = 10):
    """
    Self-correcting synthesis:
    1. Generate with current params
    2. Analyze with ear
    3. Adjust params based on errors
    4. Repeat until convergence
    """
    
    params = ResonatorParams()
    
    print(f"\n{'='*70}")
    print(f"ITERATIVE TUNING: /{vowel_name}/")
    print(f"Target: F1={target.f1}Hz, F2={target.f2}Hz, F3={target.f3}Hz")
    print(f"{'='*70}\n")
    
    for iteration in range(max_iterations):
        # Generate
        audio = generate_vowel(vowel_name, target, params)
        
        # Save to temp file for analysis
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            temp_path = f.name
        save_audio(audio, temp_path)
        
        # Analyze
        audio_loaded = load_audio(temp_path)
        from ear import analyze_audio, calculate_errors
        measured = analyze_audio(audio_loaded, SAMPLE_RATE)
        errors = calculate_errors(measured, target)
        
        print(f"Iteration {iteration + 1}:")
        print(f"  F1: {measured.f1:.0f}Hz ({errors['f1_error_pct']:+.1f}%)  "
              f"F2: {measured.f2:.0f}Hz ({errors['f2_error_pct']:+.1f}%)")
        print(f"  Params: F1_gain={params.f1_gain:.2f}, F2_gain={params.f2_gain:.2f}, "
              f"asp={params.aspiration:.2f}")
        
        # Check convergence
        if abs(errors['f1_error_pct']) < 15 and abs(errors['f2_error_pct']) < 15:
            print(f"  ✓ CONVERGED!")
            os.remove(temp_path)
            break
        
        # ADJUST parameters based on errors
        # F1 too low -> increase gain or decrease bandwidth
        if errors['f1_error_pct'] < -15:
            params.f1_gain = min(params.f1_gain * 1.2, 5.0)
            params.f1_bw = max(params.f1_bw * 0.9, 40)
        elif errors['f1_error_pct'] > 15:
            params.f1_gain = max(params.f1_gain * 0.9, 0.5)
        
        # F2 too low -> increase gain
        if errors['f2_error_pct'] < -15:
            params.f2_gain = min(params.f2_gain * 1.3, 6.0)
            params.f2_bw = max(params.f2_bw * 0.85, 50)
        elif errors['f2_error_pct'] > 15:
            params.f2_gain = max(params.f2_gain * 0.9, 0.5)
        
        # Brightness issues
        if measured.high_freq_ratio < 0.10:
            params.aspiration = min(params.aspiration * 1.2, 0.4)
        
        os.remove(temp_path)
        print()
    
    # Generate final version
    final_audio = generate_vowel(vowel_name, target, params, duration=0.25)
    output_path = f'/root/.openclaw/workspace/christkey-native/tuned_{vowel_name}.wav'
    save_audio(final_audio, output_path)
    
    print(f"\nFinal saved: {output_path}")
    print(f"Final params: F1_gain={params.f1_gain:.2f}, F2_gain={params.f2_gain:.2f}, "
          f"asp={params.aspiration:.2f}")
    print(f"{'='*70}\n")
    
    return output_path

if __name__ == "__main__":
    # Tune the three cardinal vowels
    for vowel, target in [('a', VOWEL_TARGETS['a']), 
                          ('i', VOWEL_TARGETS['i']), 
                          ('u', VOWEL_TARGETS['u'])]:
        iterative_tune(vowel, target, max_iterations=8)

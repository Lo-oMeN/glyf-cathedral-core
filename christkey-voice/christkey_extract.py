#!/usr/bin/env python3
"""
Christ-Key Voice Extractor
Extract voice characteristics from audio samples for training
Simplified version using basic audio analysis
"""

import json
import wave
import struct
import math
from pathlib import Path
from typing import Dict, List, Tuple
import tempfile

PHI = 1.618033988749895

class SimpleVoiceExtractor:
    """Extract voice characteristics without heavy dependencies"""
    
    def __init__(self):
        self.characteristics = {
            "pitch_profile": [],
            "energy_profile": [],
            "pause_pattern": [],
            "speech_rate": 0,
            "voice_quality": "neutral"
        }
    
    def extract_from_wav(self, wav_path: str) -> Dict:
        """Extract characteristics from WAV file"""
        try:
            with wave.open(wav_path, 'rb') as wav:
                n_channels = wav.getnchannels()
                sample_width = wav.getsampwidth()
                framerate = wav.getframerate()
                n_frames = wav.getnframes()
                
                # Read audio data
                frames = wav.readframes(n_frames)
                
                # Convert to samples
                if sample_width == 2:
                    fmt = f"{n_frames * n_channels}h"
                    samples = struct.unpack(fmt, frames)
                else:
                    # Convert other formats to 16-bit
                    samples = struct.unpack(f"{len(frames)}B", frames)
                    samples = [(s - 128) * 256 for s in samples]
                
                # Convert to mono if stereo
                if n_channels == 2:
                    samples = [(samples[i] + samples[i+1]) // 2 
                              for i in range(0, len(samples), 2)]
                
                # Extract characteristics
                self._extract_energy_profile(samples, framerate)
                self._extract_pause_pattern(samples, framerate)
                self._estimate_speech_rate(samples, framerate)
                
                return self.characteristics
                
        except Exception as e:
            print(f"Error extracting from {wav_path}: {e}")
            return self.characteristics
    
    def _extract_energy_profile(self, samples: List[int], framerate: int):
        """Extract energy (volume) over time"""
        window_size = framerate // 10  # 100ms windows
        energies = []
        
        for i in range(0, len(samples), window_size):
            window = samples[i:i + window_size]
            if window:
                # RMS energy
                energy = math.sqrt(sum(s**2 for s in window) / len(window))
                energies.append(energy)
        
        # Normalize
        if energies:
            max_energy = max(energies)
            self.characteristics["energy_profile"] = [
                e / max_energy for e in energies[:100]  # First 100 windows
            ]
    
    def _extract_pause_pattern(self, samples: List[int], framerate: int):
        """Detect pauses (low energy regions)"""
        threshold = 500  # Silence threshold
        window_size = framerate // 20  # 50ms windows
        
        pauses = []
        in_pause = False
        pause_start = 0
        
        for i in range(0, len(samples), window_size):
            window = samples[i:i + window_size]
            if not window:
                continue
            
            avg_energy = sum(abs(s) for s in window) / len(window)
            
            if avg_energy < threshold and not in_pause:
                in_pause = True
                pause_start = i / framerate
            elif avg_energy >= threshold and in_pause:
                in_pause = False
                pause_duration = (i / framerate) - pause_start
                if pause_duration > 0.1:  # Only significant pauses
                    pauses.append({
                        "start": pause_start,
                        "duration": pause_duration
                    })
        
        self.characteristics["pause_pattern"] = pauses[:20]  # First 20 pauses
    
    def _estimate_speech_rate(self, samples: List[int], framerate: int):
        """Estimate words per minute"""
        # Count zero crossings as proxy for syllables
        zero_crossings = sum(
            1 for i in range(1, len(samples))
            if samples[i-1] < 0 and samples[i] >= 0
        )
        
        duration_minutes = len(samples) / framerate / 60
        # Rough estimate: ~5 zero crossings per syllable, ~1.5 syllables per word
        estimated_words = zero_crossings / 5 / 1.5
        
        self.characteristics["speech_rate"] = estimated_words / duration_minutes if duration_minutes > 0 else 0
    
    def save_characteristics(self, output_path: str):
        """Save extracted characteristics to JSON"""
        with open(output_path, 'w') as f:
            json.dump(self.characteristics, f, indent=2)
        print(f"Saved characteristics to: {output_path}")

def convert_mp3_to_wav(mp3_path: str, output_path: str = None) -> str:
    """Convert MP3 to WAV using available tools"""
    if output_path is None:
        output_path = mp3_path.replace('.mp3', '.wav')
    
    # Try pydub if available
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_mp3(mp3_path)
        audio = audio.set_frame_rate(22050).set_channels(1)
        audio.export(output_path, format='wav')
        return output_path
    except ImportError:
        pass
    
    # Try ffmpeg
    import subprocess
    try:
        subprocess.run([
            'ffmpeg', '-i', mp3_path, '-ar', '22050', '-ac', '1', 
            '-y', output_path
        ], check=True, capture_output=True)
        return output_path
    except:
        pass
    
    print(f"Cannot convert {mp3_path}. Install pydub or ffmpeg.")
    return None

def main():
    """CLI"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract voice characteristics")
    parser.add_argument("audio", help="Audio file (WAV or MP3)")
    parser.add_argument("-o", "--output", help="Output JSON file")
    
    args = parser.parse_args()
    
    audio_path = args.audio
    
    # Convert MP3 to WAV if needed
    if audio_path.endswith('.mp3'):
        wav_path = audio_path.replace('.mp3', '.wav')
        converted = convert_mp3_to_wav(audio_path, wav_path)
        if converted:
            audio_path = converted
        else:
            sys.exit(1)
    
    # Extract characteristics
    extractor = SimpleVoiceExtractor()
    chars = extractor.extract_from_wav(audio_path)
    
    # Print summary
    print(f"Voice Characteristics:")
    print(f"  Speech rate: {chars['speech_rate']:.1f} WPM")
    print(f"  Energy profile: {len(chars['energy_profile'])} samples")
    print(f"  Pauses detected: {len(chars['pause_pattern'])}")
    
    # Save
    output = args.output or audio_path.replace('.wav', '_voice.json')
    extractor.save_characteristics(output)

if __name__ == "__main__":
    main()

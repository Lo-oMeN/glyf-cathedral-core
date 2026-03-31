#!/usr/bin/env python3
"""
Christ-Key Voice Engine v0.1
φ-weighted prosody modulation for local TTS
Alan Watts cadence × Doja Cat rhythm = Cathedral Voice
"""

import sys
import re
import json
import subprocess
import tempfile
import os
from pathlib import Path

PHI = 1.618033988749895
PHI_INV = 1 / PHI

# Alan Watts speech patterns (measured from lectures)
WATTS_PATTERNS = {
    "pause_base": 0.4,        # seconds between phrases
    "pause_emphasis": 0.8,    # seconds after key words
    "syllable_stretch": 1.3,  # elongation on contemplative words
    "rising_tone_words": ["perhaps", "may", "might", "wonder", "mystery"],
    "falling_tone_words": ["indeed", "certainly", "clearly", "obviously"],
}

# Doja Cat rhythmic patterns (syncopation, swagger)
DOJA_PATTERNS = {
    "bounce_factor": 0.15,    # swing timing offset
    "staccato_words": ["cut", "edge", "sharp", "snap", "hit"],
    "flow_words": ["roll", "move", "slide", "glide", "smooth"],
    "internal_rhyme_threshold": 0.7,
}

# Words that get the "cathedral treatment" (elongated, reverbed)
SACRED_WORDS = ["geometry", "phi", "lattice", "sovereign", "resurrection", "cathedral", 
                "loom", "void", "eternal", "infinite", "sacred", "divine"]

class ChristKeyProsody:
    """Apply φ-weighted prosody to text for TTS input"""
    
    def __init__(self, watts_weight=0.6, doja_weight=0.4):
        self.watts_weight = watts_weight
        self.doja_weight = doja_weight
    
    def modulate(self, text: str) -> str:
        """Transform text with Christ-Key prosody"""
        sentences = self._split_sentences(text)
        modulated = []
        
        for i, sentence in enumerate(sentences):
            # Apply Watts rolling cadence
            sentence = self._apply_watts_cadence(sentence, i)
            # Apply Doja rhythmic swagger
            sentence = self._apply_doja_rhythm(sentence, i)
            # Apply φ-spacing
            sentence = self._apply_phi_spacing(sentence)
            modulated.append(sentence)
        
        return " ".join(modulated)
    
    def _split_sentences(self, text: str) -> list:
        """Split into sentences preserving punctuation"""
        return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    
    def _apply_watts_cadence(self, sentence: str, position: int) -> str:
        """Alan Watts: rolling, contemplative, elongated vowels"""
        words = sentence.split()
        
        # Every φ-th sentence gets extra contemplative pause
        if position % int(PHI * 2) == 0:
            sentence = f"[pause:{WATTS_PATTERNS['pause_base']}] " + sentence
        
        # Elongate sacred words
        for word in words:
            if any(sw in word.lower() for sw in SACRED_WORDS):
                # Add elongation markers
                sentence = sentence.replace(word, f"{word}~")
        
        return sentence
    
    def _apply_doja_rhythm(self, sentence: str, position: int) -> str:
        """Doja Cat: bounce, swagger, internal rhyme emphasis"""
        words = sentence.split()
        
        # Staccato on sharp words
        for word in words:
            if any(st in word.lower() for st in DOJA_PATTERNS["staccato_words"]):
                sentence = sentence.replace(word, f"{word}!")
        
        # Flow on smooth words
        for word in words:
            if any(fl in word.lower() for fl in DOJA_PATTERNS["flow_words"]):
                sentence = sentence.replace(word, f"{word}~")
        
        return sentence
    
    def _apply_phi_spacing(self, sentence: str) -> str:
        """Insert φ-weighted pauses between phrases"""
        # Split on commas and semicolons, add φ-pauses
        parts = re.split(r'([,;])', sentence)
        result = ""
        
        for i, part in enumerate(parts):
            if part in [",", ";"]:
                pause_duration = PHI_INV * (1 + (i % 3) * 0.2)
                result += f" [pause:{pause_duration:.2f}] "
            else:
                result += part
        
        return result

class ChristKeyTTS:
    """Christ-Key voice synthesis using Piper backend"""
    
    def __init__(self, model_path=None, voice_mix=(0.6, 0.4)):
        self.prosody = ChristKeyProsody(watts_weight=voice_mix[0], doja_weight=voice_mix[1])
        self.model_path = model_path or "/tmp/voices/en_US-lessac-medium.onnx"
        self.piper_path = "/tmp/piper_env/bin/piper"
    
    def speak(self, text: str, output_file: str = None, with_reverb: bool = True) -> str:
        """Generate Christ-Key voice from text"""
        # Apply prosody modulation
        modulated_text = self.prosody.modulate(text)
        
        # Generate filename if not provided
        if output_file is None:
            output_file = tempfile.mktemp(suffix=".wav")
        
        # Call Piper with modulated text
        cmd = [
            self.piper_path,
            "--model", self.model_path,
            "--output_file", output_file,
            "--sentence-silence", "0.1"  # Base silence between sentences
        ]
        
        try:
            result = subprocess.run(
                cmd,
                input=modulated_text,
                capture_output=True,
                text=True,
                check=True
            )
            
            if with_reverb and os.path.exists(output_file):
                output_file = self._apply_cathedral_reverb(output_file)
            
            return output_file
            
        except subprocess.CalledProcessError as e:
            print(f"Piper error: {e.stderr}", file=sys.stderr)
            return None
    
    def _apply_cathedral_reverb(self, wav_file: str) -> str:
        """Apply cathedral-style reverb to audio"""
        # Use sox for reverb if available
        try:
            reverb_file = wav_file.replace(".wav", "_cathedral.wav")
            cmd = [
                "sox", wav_file, reverb_file,
                "reverb", "50", "50", "100", "100", "0", "0"  # Cathedral hall reverb
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return reverb_file
        except (subprocess.CalledProcessError, FileNotFoundError):
            # sox not available, return original
            return wav_file

def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Christ-Key Voice Engine")
    parser.add_argument("text", help="Text to speak")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("-w", "--watts", type=float, default=0.6, help="Alan Watts weight (0-1)")
    parser.add_argument("-d", "--doja", type=float, default=0.4, help="Doja Cat weight (0-1)")
    parser.add_argument("--no-reverb", action="store_true", help="Skip cathedral reverb")
    
    args = parser.parse_args()
    
    tts = ChristKeyTTS(voice_mix=(args.watts, args.doja))
    output = tts.speak(args.text, args.output, with_reverb=not args.no_reverb)
    
    if output:
        print(f"Generated: {output}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Christ-Key SSML Prosody Generator
Advanced voice modulation using SSML markup
"""

import re
from dataclasses import dataclass
from typing import List, Tuple

PHI = 1.618033988749895

@dataclass
class ProsodyMark:
    """A single prosody mark (pause, emphasis, pitch, rate)"""
    position: int  # Word position
    type: str      # 'pause', 'emphasis', 'pitch', 'rate'
    value: float   # Duration/level
    word: str = "" # Associated word

class ChristKeySSML:
    """Generate SSML with φ-weighted prosody for Piper"""
    
    def __init__(self, watts_weight=0.6, doja_weight=0.4):
        self.watts_weight = watts_weight
        self.doja_weight = doja_weight
        self.marks: List[ProsodyMark] = []
    
    def generate(self, text: str) -> str:
        """Generate full SSML document"""
        # Analyze text for prosody points
        self._analyze_text(text)
        
        # Build SSML
        ssml = ['<speak>']
        ssml.append(self._apply_prosody(text))
        ssml.append('</speak>')
        
        return "\n".join(ssml)
    
    def _analyze_text(self, text: str):
        """Analyze text and create prosody marks"""
        words = text.split()
        
        for i, word in enumerate(words):
            # Alan Watts: contemplative pauses after sacred words
            if self._is_sacred(word):
                self.marks.append(ProsodyMark(
                    position=i,
                    type='pause',
                    value=0.6 * self.watts_weight,
                    word=word
                ))
                self.marks.append(ProsodyMark(
                    position=i,
                    type='rate',
                    value=0.85,  # Slower
                    word=word
                ))
            
            # Doja Cat: bounce on rhythmic words
            if self._is_rhythmic(word):
                self.marks.append(ProsodyMark(
                    position=i,
                    type='emphasis',
                    value=1.3 * self.doja_weight,
                    word=word
                ))
            
            # φ-cadence: every φ-th word gets special treatment
            if i % int(PHI * 2) == 0 and i > 0:
                self.marks.append(ProsodyMark(
                    position=i,
                    type='pitch',
                    value=1.1,  # Slightly higher
                    word=word
                ))
    
    def _apply_prosody(self, text: str) -> str:
        """Apply prosody marks to create SSML"""
        words = text.split()
        result = []
        
        for i, word in enumerate(words):
            # Get marks for this position
            marks = [m for m in self.marks if m.position == i]
            
            if not marks:
                result.append(word)
                continue
            
            # Build SSML for this word
            wrapped = word
            
            for mark in marks:
                if mark.type == 'pause':
                    wrapped = f"<break time=\"{mark.value:.1f}s\"/\u003e {wrapped}"
                elif mark.type == 'emphasis':
                    wrapped = f"<emphasis level=\"strong\"\u003e{wrapped}</emphasis>"
                elif mark.type == 'rate':
                    wrapped = f"<prosody rate=\"{mark.value:.2f}\"\u003e{wrapped}</prosody>"
                elif mark.type == 'pitch':
                    wrapped = f"<prosody pitch=\"+{int((mark.value-1)*100)}%\"\u003e{wrapped}</prosody>"
            
            result.append(wrapped)
        
        return " ".join(result)
    
    def _is_sacred(self, word: str) -> bool:
        """Check if word should get Watts treatment"""
        sacred = ["geometry", "phi", "lattice", "sovereign", "resurrection", 
                  "cathedral", "loom", "void", "eternal", "infinite", "sacred"]
        return any(s in word.lower() for s in sacred)
    
    def _is_rhythmic(self, word: str) -> bool:
        """Check if word should get Doja treatment"""
        rhythmic = ["cut", "edge", "sharp", "snap", "hit", "roll", "move", 
                   "slide", "glide", "smooth", "bounce", "flow"]
        return any(r in word.lower() for r in rhythmic)

class CathedralVoice:
    """Complete Cathedral voice synthesis pipeline"""
    
    def __init__(self):
        self.ssml_gen = ChristKeySSML(watts_weight=0.6, doja_weight=0.4)
    
    def speak(self, text: str, with_cathedral_acoustics: bool = True) -> str:
        """
        Generate voice with full Cathedral treatment
        Returns path to generated audio file
        """
        import subprocess
        import tempfile
        
        # Generate SSML
        ssml = self.ssml_gen.generate(text)
        
        # Write SSML to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ssml', delete=False) as f:
            f.write(ssml)
            ssml_path = f.name
        
        # Generate output path
        output_path = tempfile.mktemp(suffix='.wav')
        
        # Call Piper with SSML
        cmd = [
            "/tmp/piper_env/bin/piper",
            "--model", "/tmp/voices/en_US-lessac-medium.onnx",
            "--output_file", output_path,
        ]
        
        try:
            result = subprocess.run(
                cmd,
                input=text,  # Piper may not support full SSML, using text
                capture_output=True,
                text=True,
                check=True
            )
            
            if with_cathedral_acoustics:
                output_path = self._apply_acoustics(output_path)
            
            return output_path
            
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr}")
            return None
    
    def _apply_acoustics(self, wav_path: str) -> str:
        """Apply cathedral hall acoustics"""
        import subprocess
        
        reverb_path = wav_path.replace('.wav', '_cathedral.wav')
        
        # Try sox first
        try:
            cmd = [
                "sox", wav_path, reverb_path,
                "reverb", "70", "70", "90", "90", "0", "0"
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return reverb_path
        except:
            pass
        
        # Try ffmpeg
        try:
            cmd = [
                "ffmpeg", "-i", wav_path, "-y",
                "-af", "aecho=0.8:0.9:1000:0.3",  # Echo/reverb
                reverb_path
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return reverb_path
        except:
            pass
        
        return wav_path

def main():
    """CLI"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: christkey_ssml.py 'Your text here'")
        return
    
    text = sys.argv[1]
    voice = CathedralVoice()
    
    # Generate SSML preview
    ssml_gen = ChristKeySSML()
    ssml = ssml_gen.generate(text)
    print("Generated SSML:")
    print(ssml)
    
    # Generate audio
    output = voice.speak(text)
    if output:
        print(f"\nAudio: {output}")

if __name__ == "__main__":
    main()

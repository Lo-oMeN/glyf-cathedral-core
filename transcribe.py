#!/usr/bin/env python3
"""
GLYF Audio Transcription Tool
Lightweight transcription using OpenAI Whisper API or local fallback.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

class AudioTranscriber:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.audio_dir = Path("/root/.openclaw/workspace")
        
    def transcribe_file(self, audio_path: str) -> str:
        """Transcribe an audio file using available methods."""
        
        # Method 1: OpenAI API (best quality)
        if self.api_key:
            return self._transcribe_openai(audio_path)
        
        # Method 2: Check for local whisper
        if self._check_whisper():
            return self._transcribe_local(audio_path)
        
        # Method 3: Manual fallback
        return "Error: No transcription method available. Set OPENAI_API_KEY or install whisper."
    
    def _check_whisper(self) -> bool:
        """Check if whisper is available locally."""
        try:
            result = subprocess.run(
                ["python3", "-c", "import whisper"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def _transcribe_openai(self, audio_path: str) -> str:
        """Transcribe using OpenAI Whisper API."""
        import urllib.request
        import urllib.parse
        
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        
        # Build multipart form data
        with open(audio_path, 'rb') as f:
            audio_data = f.read()
        
        body = []
        body.append(f'--{boundary}'.encode())
        body.append(b'Content-Disposition: form-data; name="file"; filename="audio.ogg"')
        body.append(b'Content-Type: audio/ogg')
        body.append(b'')
        body.append(audio_data)
        body.append(f'--{boundary}'.encode())
        body.append(b'Content-Disposition: form-data; name="model"')
        body.append(b'')
        body.append(b'whisper-1')
        body.append(f'--{boundary}--'.encode())
        
        body = b'\r\n'.join(body)
        
        req = urllib.request.Request(
            'https://api.openai.com/v1/audio/transcriptions',
            data=body,
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': f'multipart/form-data; boundary={boundary}'
            },
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode())
                return result.get('text', 'No transcription available')
        except Exception as e:
            return f"Transcription error: {e}"
    
    def _transcribe_local(self, audio_path: str) -> str:
        """Transcribe using local whisper."""
        try:
            result = subprocess.run(
                ["python3", "-m", "whisper", audio_path, "--model", "tiny", "--output_format", "txt"],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # Read output file
            output_path = Path(audio_path).with_suffix('.txt')
            if output_path.exists():
                return output_path.read_text().strip()
            return result.stdout.strip() or "Transcription failed"
        except Exception as e:
            return f"Local transcription error: {e}"

if __name__ == "__main__":
    transcriber = AudioTranscriber()
    
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        # Default to most recent voice file
        voice_files = sorted(
            Path("/root/.openclaw/workspace").glob("voice_*.ogg"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        audio_file = str(voice_files[0]) if voice_files else None
    
    if audio_file and os.path.exists(audio_file):
        print(f"Transcribing: {audio_file}")
        print("-" * 50)
        result = transcriber.transcribe_file(audio_file)
        print(result)
    else:
        print("Usage: python3 transcribe.py <audio_file.ogg>")
        print("Or set OPENAI_API_KEY for API-based transcription")

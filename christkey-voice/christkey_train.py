#!/usr/bin/env python3
"""
Christ-Key Voice Trainer Pipeline
Train custom voice from extracted characteristics
"""

import json
import sys
from pathlib import Path
from typing import Dict, List

PHI = 1.618033988749895

class VoiceBlendTrainer:
    """Train blended voice from multiple sources"""
    
    def __init__(self, output_dir: str = "./trained_voices"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.voices: Dict[str, Dict] = {}
    
    def load_voice(self, name: str, json_path: str):
        """Load voice characteristics from JSON"""
        with open(json_path) as f:
            self.voices[name] = json.load(f)
        print(f"Loaded voice: {name}")
    
    def create_blend(self, voice1: str, voice2: str, ratio: float) -> Dict:
        """
        Blend two voices with given ratio
        ratio: 0.0 = pure voice1, 1.0 = pure voice2
        """
        if voice1 not in self.voices or voice2 not in self.voices:
            raise ValueError(f"Both voices must be loaded first")
        
        v1, v2 = self.voices[voice1], self.voices[voice2]
        
        # φ-weighted blend
        phi_ratio = ratio * PHI_INV + (1 - ratio) * (1 - PHI_INV)
        
        blended = {
            "name": f"{voice1}_{voice2}_{ratio:.2f}",
            "voice1": voice1,
            "voice2": voice2,
            "ratio": ratio,
            "phi_ratio": phi_ratio,
            "speech_rate": self._blend_value(
                v1.get("speech_rate", 150),
                v2.get("speech_rate", 150),
                phi_ratio
            ),
            "pause_base": self._blend_value(
                self._avg_pause(v1.get("pause_pattern", [])),
                self._avg_pause(v2.get("pause_pattern", [])),
                phi_ratio
            ),
            "energy_dynamic_range": self._blend_value(
                self._dynamic_range(v1.get("energy_profile", [])),
                self._dynamic_range(v2.get("energy_profile", [])),
                phi_ratio
            ),
            "prosody_config": self._generate_prosody_config(v1, v2, phi_ratio)
        }
        
        return blended
    
    def _blend_value(self, v1: float, v2: float, ratio: float) -> float:
        """Blend two values"""
        return v1 * (1 - ratio) + v2 * ratio
    
    def _avg_pause(self, pauses: List[Dict]) -> float:
        """Average pause duration"""
        if not pauses:
            return 0.3
        return sum(p["duration"] for p in pauses) / len(pauses)
    
    def _dynamic_range(self, energy: List[float]) -> float:
        """Calculate dynamic range of energy"""
        if not energy:
            return 0.5
        return max(energy) - min(energy)
    
    def _generate_prosody_config(self, v1: Dict, v2: Dict, ratio: float) -> Dict:
        """Generate prosody configuration for the blend"""
        return {
            "pause_after_sacred": self._blend_value(0.6, 0.3, ratio),  # Watts longer
            "emphasis_level": self._blend_value(1.2, 1.5, ratio),       # Doja stronger
            "pitch_variation": self._blend_value(0.1, 0.3, ratio),      # Doja more variation
            "rate_variation": self._blend_value(0.9, 1.1, ratio),       # Watts slower
            "phi_cadence": True,
        }
    
    def save_voice(self, voice: Dict, output_name: str = None):
        """Save trained voice configuration"""
        name = output_name or voice["name"]
        output_path = self.output_dir / f"{name}.json"
        
        with open(output_path, 'w') as f:
            json.dump(voice, f, indent=2)
        
        print(f"Saved trained voice: {output_path}")
        return output_path
    
    def generate_speak_config(self, voice: Dict) -> Dict:
        """Generate configuration for speak.sh"""
        config = {
            "voice_name": voice["name"],
            "prosody": voice["prosody_config"],
            "piper_params": {
                "length_scale": 1.0 / voice["speech_rate"] * 150,  # Normalize to ~150 WPM
                "noise_scale": 0.667,
                "noise_w": 0.8,
            }
        }
        return config

def create_alan_watts_profile():
    """Create Alan Watts voice profile from known characteristics"""
    return {
        "name": "alan_watts",
        "speech_rate": 110,  # ~110 WPM, contemplative
        "pause_base": 0.6,   # Longer pauses
        "pause_pattern": [
            {"start": 0, "duration": 0.8},  # After key phrases
        ],
        "energy_profile": [0.3, 0.5, 0.7, 0.9, 0.6, 0.4],  # Measured
        "voice_quality": "warm_contemplative",
        "characteristics": {
            "elongated_vowels": True,
            "rising_intonation": ["perhaps", "may", "wonder"],
            "falling_intonation": ["indeed", "clearly", "obviously"],
        }
    }

def create_doja_cat_profile():
    """Create Doja Cat voice profile from known characteristics"""
    return {
        "name": "doja_cat",
        "speech_rate": 160,  # ~160 WPM, faster
        "pause_base": 0.25,  # Shorter pauses
        "pause_pattern": [
            {"start": 0, "duration": 0.2},  # Quick, rhythmic
        ],
        "energy_profile": [0.5, 0.9, 0.4, 0.8, 0.6, 0.95],  # Dynamic
        "voice_quality": "playful_swagger",
        "characteristics": {
            "syncopation": True,
            "bounce": True,
            "rhythmic_emphasis": ["cut", "snap", "hit", "bounce"],
        }
    }

def main():
    """CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Train Christ-Key Voice")
    parser.add_argument("--load", nargs=2, metavar=("NAME", "JSON"),
                       help="Load voice from JSON")
    parser.add_argument("--preset", choices=["watts", "doja", "both"],
                       help="Load preset voice profile")
    parser.add_argument("--blend", nargs=3, metavar=("V1", "V2", "RATIO"),
                       help="Blend two voices")
    parser.add_argument("--list", action="store_true",
                       help="List loaded voices")
    
    args = parser.parse_args()
    
    trainer = VoiceBlendTrainer()
    
    # Load presets
    if args.preset == "watts":
        trainer.voices["alan_watts"] = create_alan_watts_profile()
        print("Loaded preset: alan_watts")
    elif args.preset == "doja":
        trainer.voices["doja_cat"] = create_doja_cat_profile()
        print("Loaded preset: doja_cat")
    elif args.preset == "both":
        trainer.voices["alan_watts"] = create_alan_watts_profile()
        trainer.voices["doja_cat"] = create_doja_cat_profile()
        print("Loaded presets: alan_watts, doja_cat")
    
    # Load custom voices
    if args.load:
        name, json_path = args.load
        trainer.load_voice(name, json_path)
    
    # List voices
    if args.list:
        print(f"Loaded voices: {list(trainer.voices.keys())}")
    
    # Create blend
    if args.blend:
        v1, v2, ratio = args.blend
        ratio = float(ratio)
        
        blended = trainer.create_blend(v1, v2, ratio)
        output = trainer.save_voice(blended)
        
        # Also generate speak config
        speak_config = trainer.generate_speak_config(blended)
        config_path = trainer.output_dir / f"{blended['name']}_speak.json"
        with open(config_path, 'w') as f:
            json.dump(speak_config, f, indent=2)
        
        print(f"\nChrist-Key Voice '{blended['name']}' created!")
        print(f"  Speech rate: {blended['speech_rate']:.1f} WPM")
        print(f"  Pause base: {blended['pause_base']:.2f}s")
        print(f"  φ-weighted ratio: {blended['phi_ratio']:.3f}")

if __name__ == "__main__":
    main()

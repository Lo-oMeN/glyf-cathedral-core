#!/usr/bin/env python3
"""
Claw-Ear: Phi-Spiral Acoustic Capture System v0.1
Simulates the 7-node phi-spiral electret array
"""

import numpy as np
import wave
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum, auto

PHI = 1.618033988749895
SAMPLE_RATE = 22050

class TernaryState(Enum):
    """Ternary charge states"""
    POSITIVE = 1
    NULL = 0
    NEGATIVE = -1

@dataclass
class SpiralNode:
    """One node in the phi-spiral array"""
    index: int
    angle_deg: float  # Rotation angle
    radius: float     # Normalized radius (0-1)
    x: float          # Cartesian position
    y: float
    
    # Ternary state buffer
    charge_history: List[TernaryState] = None
    
    def __post_init__(self):
        if self.charge_history is None:
            self.charge_history = []

def generate_phi_spiral(n_nodes: int = 7) -> List[SpiralNode]:
    """
    Generate 7-node phi-spiral array.
    Each node at 137.5° (golden angle) rotation, φ-scaling radius.
    """
    golden_angle = 137.50776405003785  # 360° / φ²
    nodes = []
    
    for i in range(n_nodes):
        angle = (i * golden_angle) % 360
        # Radius grows by φ each step, normalized
        radius = (PHI ** i) / (PHI ** (n_nodes - 1))
        
        # Convert to Cartesian
        rad = np.radians(angle)
        x = radius * np.cos(rad)
        y = radius * np.sin(rad)
        
        nodes.append(SpiralNode(
            index=i,
            angle_deg=angle,
            radius=radius,
            x=x,
            y=y
        ))
    
    return nodes

@dataclass
class AcousticField:
    """Pressure field captured by spiral array"""
    timestamp: float
    node_pressures: List[float]  # Raw pressure at each node
    node_differentials: List[float]  # Differential from previous
    ternary_states: List[TernaryState]

def pressure_to_ternary(pressure: float, threshold: float = 0.01) -> TernaryState:
    """Convert continuous pressure to ternary state"""
    if pressure > threshold:
        return TernaryState.POSITIVE
    elif pressure < -threshold:
        return TernaryState.NEGATIVE
    else:
        return TernaryState.NULL

class SpiralEar:
    """
    The phi-spiral acoustic capture system.
    Simulates 7-node array with ternary readout.
    """
    
    def __init__(self, n_nodes: int = 7):
        self.nodes = generate_phi_spiral(n_nodes)
        self.history: List[AcousticField] = []
        self.wavelength = 343.0 / 1000  # Speed of sound / 1kHz reference
        
    def capture_frame(self, audio_sample: np.ndarray, sample_idx: int) -> AcousticField:
        """
        Simulate one capture frame from audio.
        Each node samples pressure with phase delay based on position.
        """
        frame_time = sample_idx / SAMPLE_RATE
        
        # For each node, sample with spatial phase delay
        pressures = []
        diffs = []
        ternary = []
        
        for node in self.nodes:
            # Phase delay proportional to x-position (simplified)
            # Sound travels left-to-right, nodes at different x experience delay
            delay_samples = int(node.x * 10)  # Simplified: 10 samples per unit x
            
            idx = max(0, min(sample_idx - delay_samples, len(audio_sample) - 1))
            pressure = audio_sample[idx]
            
            # Differential from history
            if node.charge_history:
                prev_pressure = node.charge_history[-1].value if node.charge_history[-1] else 0
                diff = pressure - prev_pressure * 0.5  # Simplified
            else:
                diff = pressure
            
            pressures.append(pressure)
            diffs.append(diff)
            ternary.append(pressure_to_ternary(pressure))
            
            node.charge_history.append(ternary[-1])
        
        field = AcousticField(
            timestamp=frame_time,
            node_pressures=pressures,
            node_differentials=diffs,
            ternary_states=ternary
        )
        
        self.history.append(field)
        return field
    
    def capture_full(self, audio: np.ndarray, stride: int = 256) -> List[AcousticField]:
        """Capture entire audio file"""
        self.history = []
        for i in range(0, len(audio), stride):
            self.capture_frame(audio, i)
        return self.history

# === GLYF PRIMITIVE EXTRACTION ===

class AcousticPrimitive(Enum):
    """The 7 primitives applied to acoustic domain"""
    DOT = auto()      # Impulse/transient
    LINE = auto()     # Steady tone/drone
    CURVE = auto()    # Formant trajectory
    ANGLE = auto()    # Consonant attack
    CIRCLE = auto()   # Sustained resonance
    VESICA = auto()   # Silence container (pause)
    CROSS = auto()    # Interference beat

@dataclass
class PrimitiveDetection:
    primitive: AcousticPrimitive
    start_time: float
    duration: float
    intensity: float
    node_signature: List[int]  # Which nodes detected it

class PrimitiveExtractor:
    """
    Extract GLYF primitives from ternary acoustic history.
    """
    
    def __init__(self, ear: SpiralEar):
        self.ear = ear
        
    def extract_voids(self, min_duration_ms: float = 50) -> List[PrimitiveDetection]:
        """
        Stage 1: Void Detection
        Silence as vesica piscis containers.
        Measures shape of silence between phonemes.
        """
        voids = []
        in_void = False
        void_start = 0
        
        for field in self.ear.history:
            # All nodes in NULL state = silence
            all_null = all(s == TernaryState.NULL for s in field.ternary_states)
            
            if all_null and not in_void:
                in_void = True
                void_start = field.timestamp
            elif not all_null and in_void:
                in_void = False
                duration = (field.timestamp - void_start) * 1000  # ms
                if duration >= min_duration_ms:
                    voids.append(PrimitiveDetection(
                        primitive=AcousticPrimitive.VESICA,
                        start_time=void_start,
                        duration=duration / 1000,
                        intensity=duration / 1000,  # Longer = more intense
                        node_signature=[0, 1, 2, 3, 4, 5, 6]  # All nodes
                    ))
        
        return voids
    
    def extract_curves(self) -> List[PrimitiveDetection]:
        """
        Stage 2: Curve Extraction
        Formant trajectories as bezier curves in (pitch, timbre, time) space.
        """
        curves = []
        
        # Track pitch over time via zero-crossing rate
        if len(self.ear.history) < 10:
            return curves
        
        # Simplified: detect sustained tones with changing node activation
        for i in range(1, len(self.ear.history) - 1):
            prev = self.ear.history[i-1]
            curr = self.ear.history[i]
            next_f = self.ear.history[i+1]
            
            # Count active nodes
            prev_active = sum(1 for s in prev.ternary_states if s != TernaryState.NULL)
            curr_active = sum(1 for s in curr.ternary_states if s != TernaryState.NULL)
            next_active = sum(1 for s in next_f.ternary_states if s != TernaryState.NULL)
            
            # Changing activation pattern = curve
            if curr_active > 0 and (prev_active != curr_active or curr_active != next_active):
                active_nodes = [j for j, s in enumerate(curr.ternary_states) 
                               if s != TernaryState.NULL]
                curves.append(PrimitiveDetection(
                    primitive=AcousticPrimitive.CURVE,
                    start_time=curr.timestamp,
                    duration=0.01,  # 10ms per sample
                    intensity=curr_active / 7.0,
                    node_signature=active_nodes
                ))
        
        return curves
    
    def extract_angles(self, threshold: float = 0.5) -> List[PrimitiveDetection]:
        """
        Stage 3: Angular Transients
        Plosives/fricatives as angle primitives.
        Measure attack slopes as acute/obtuse angles.
        """
        angles = []
        
        for i in range(1, len(self.ear.history)):
            prev = self.ear.history[i-1]
            curr = self.ear.history[i]
            
            # Calculate pressure slope across all nodes
            total_slope = 0
            for j in range(len(self.ear.nodes)):
                slope = abs(curr.node_pressures[j] - prev.node_pressures[j])
                total_slope += slope
            
            avg_slope = total_slope / len(self.ear.nodes)
            
            # Sharp attack = angle primitive
            if avg_slope > threshold:
                active = [j for j, s in enumerate(curr.ternary_states) 
                         if s != TernaryState.NULL]
                
                # Classify as acute or obtuse based on slope
                prim = AcousticPrimitive.ANGLE if avg_slope > 1.0 else AcousticPrimitive.DOT
                
                angles.append(PrimitiveDetection(
                    primitive=prim,
                    start_time=curr.timestamp,
                    duration=0.005,
                    intensity=min(avg_slope, 2.0),
                    node_signature=active
                ))
        
        return angles
    
    def extract_all(self) -> dict:
        """Run full extraction pipeline"""
        return {
            'voids': self.extract_voids(),
            'curves': self.extract_curves(),
            'angles': self.extract_angles(),
        }

def load_audio(wav_path: str) -> np.ndarray:
    """Load WAV as float array"""
    with wave.open(wav_path, 'rb') as f:
        frames = f.readframes(f.getnframes())
        audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
        if f.getnchannels() == 2:
            audio = audio[::2]
        return audio

if __name__ == "__main__":
    import sys
    
    # Test with a vowel
    test_file = "/root/.openclaw/workspace/christkey-native/v4_a.wav"
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
    
    print(f"Claw-Ear Simulation")
    print(f"Testing with: {test_file}")
    print("=" * 60)
    
    # Load audio
    audio = load_audio(test_file)
    print(f"Audio duration: {len(audio)/SAMPLE_RATE:.3f}s")
    
    # Create ear and capture
    ear = SpiralEar(n_nodes=7)
    fields = ear.capture_full(audio, stride=256)
    print(f"Captured {len(fields)} frames")
    
    # Show spiral geometry
    print(f"\n[Phi-Spiral Array Geometry]")
    for node in ear.nodes:
        print(f"  Node {node.index}: angle={node.angle_deg:.1f}°, "
              f"radius={node.radius:.3f}, pos=({node.x:.3f}, {node.y:.3f})")
    
    # Extract primitives
    extractor = PrimitiveExtractor(ear)
    primitives = extractor.extract_all()
    
    print(f"\n[Detected Primitives]")
    for prim_type, detections in primitives.items():
        print(f"\n  {prim_type.upper()}: {len(detections)} instances")
        for det in detections[:5]:  # Show first 5
            print(f"    - {det.primitive.name} at {det.start_time:.3f}s, "
                  f"duration={det.duration*1000:.1f}ms, "
                  f"nodes={det.node_signature}")
        if len(detections) > 5:
            print(f"    ... and {len(detections)-5} more")
    
    print(f"\n{'='*60}")
    print("Ternary state distribution:")
    all_states = []
    for f in fields:
        all_states.extend(f.ternary_states)
    
    pos = sum(1 for s in all_states if s == TernaryState.POSITIVE)
    neg = sum(1 for s in all_states if s == TernaryState.NEGATIVE)
    null = sum(1 for s in all_states if s == TernaryState.NULL)
    total = len(all_states)
    
    print(f"  POSITIVE: {pos/total*100:.1f}%")
    print(f"  NEGATIVE: {neg/total*100:.1f}%")
    print(f"  NULL:     {null/total*100:.1f}%")

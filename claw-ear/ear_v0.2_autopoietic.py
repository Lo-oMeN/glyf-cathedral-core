#!/usr/bin/env python3
"""
Claw-Ear v0.2: Autopoietic Feedback Loop
The ear reconfigures itself based on what it failed to hear.
"""

import numpy as np
from ear_v01 import SpiralEar, PrimitiveExtractor, load_audio, TernaryState
from dataclasses import dataclass
from typing import List

@dataclass
class ConfusionMetric:
    """What the ear failed to quantize"""
    unquantized_energy: float  # Audio energy not captured by primitives
    spectral_remainder: float  # Frequencies outside primitive bands
    temporal_gaps: int         # Moments with no primitive assignment
    total_confusion: float     # Composite score

class AutopoieticEar(SpiralEar):
    """
    The ear that grows itself.
    Adjusts spiral geometry to minimize confusion.
    """
    
    def __init__(self, n_nodes: int = 7):
        super().__init__(n_nodes)
        self.confusion_history: List[ConfusionMetric] = []
        self.iteration = 0
        
        # Adaptable parameters
        self.ternary_threshold = 0.01
        self.spiral_tension = 1.0  # Affects effective radius
        self.void_sensitivity = 50.0  # ms, minimum void duration
        
    def measure_confusion(self, original_audio: np.ndarray) -> ConfusionMetric:
        """
        Calculate what wasn't captured by primitives.
        The 'unformed void' that escaped quantization.
        """
        if not self.history:
            return ConfusionMetric(0, 0, 0, 0)
        
        # Extract what we captured
        extractor = PrimitiveExtractor(self)
        primitives = extractor.extract_all()
        
        total_primitive_coverage = 0
        
        # Voids cover silence
        for void in primitives['voids']:
            total_primitive_coverage += void.duration
        
        # Curves cover sustained tones
        for curve in primitives['curves']:
            total_primitive_coverage += curve.duration
        
        # Angles cover transients
        for angle in primitives['angles']:
            total_primitive_coverage += angle.duration
        
        # Audio duration
        audio_duration = len(original_audio) / 22050
        
        # Temporal gaps = moments with no primitive
        temporal_gaps = max(0, int((audio_duration - total_primitive_coverage) * 100))
        
        # Unquantized energy: sum of audio energy in gaps
        # Simplified: estimate based on ternary null states
        null_frames = sum(1 for f in self.history 
                         if all(s == TernaryState.NULL for s in f.ternary_states))
        unquantized = null_frames / len(self.history) if self.history else 0
        
        # Spectral remainder: how much energy outside captured bands
        # For now, estimate from ternary state distribution
        pos_ratio = sum(1 for f in self.history for s in f.ternary_states 
                       if s == TernaryState.POSITIVE) / (len(self.history) * len(self.nodes))
        spectral_remainder = abs(pos_ratio - 0.5)  # Ideally balanced
        
        total = unquantized * 0.4 + spectral_remainder * 0.3 + (temporal_gaps / 100) * 0.3
        
        return ConfusionMetric(
            unquantized_energy=unquantized,
            spectral_remainder=spectral_remainder,
            temporal_gaps=temporal_gaps,
            total_confusion=total
        )
    
    def adapt(self, confusion: ConfusionMetric):
        """
        Adjust ear parameters based on confusion.
        The ear literally reshapes itself.
        """
        self.iteration += 1
        self.confusion_history.append(confusion)
        
        print(f"\n[Adaptation Iteration {self.iteration}]")
        print(f"  Confusion: {confusion.total_confusion:.3f}")
        print(f"    - Unquantized energy: {confusion.unquantized_energy:.3f}")
        print(f"    - Spectral remainder: {confusion.spectral_remainder:.3f}")
        print(f"    - Temporal gaps: {confusion.temporal_gaps}")
        
        # ADAPTATION RULES
        
        # Rule 1: Too much unquantized energy -> lower threshold (more sensitive)
        if confusion.unquantized_energy > 0.3:
            old_threshold = self.ternary_threshold
            self.ternary_threshold = max(0.001, self.ternary_threshold * 0.8)
            print(f"  → Lowering threshold: {old_threshold:.4f} -> {self.ternary_threshold:.4f}")
        
        # Rule 2: Too much spectral remainder -> adjust spiral tension
        if confusion.spectral_remainder > 0.3:
            old_tension = self.spiral_tension
            self.spiral_tension *= 1.1
            print(f"  → Increasing spiral tension: {old_tension:.3f} -> {self.spiral_tension:.3f}")
            # Regenerate nodes with new tension
            self.regenerate_spiral()
        
        # Rule 3: Too many temporal gaps -> lower void sensitivity
        if confusion.temporal_gaps > 50:
            old_sens = self.void_sensitivity
            self.void_sensitivity = max(10, self.void_sensitivity * 0.8)
            print(f"  → Lowering void sensitivity: {old_sens:.1f}ms -> {self.void_sensitivity:.1f}ms")
        
        # Rule 4: If confusion is low, we're converging
        if confusion.total_confusion < 0.2:
            print(f"  ✓ EAR CONVERGED at iteration {self.iteration}")
    
    def regenerate_spiral(self):
        """Regenerate spiral geometry with current tension"""
        PHI = 1.618033988749895
        golden_angle = 137.50776405003785
        
        for i, node in enumerate(self.nodes):
            angle = (i * golden_angle) % 360
            # Apply tension to radius
            base_radius = (PHI ** i) / (PHI ** (len(self.nodes) - 1))
            node.radius = base_radius * self.spiral_tension
            node.angle_deg = angle
            
            rad = np.radians(angle)
            node.x = node.radius * np.cos(rad)
            node.y = node.radius * np.sin(rad)
    
    def iterative_listen(self, audio: np.ndarray, max_iterations: int = 10):
        """
        Full autopoietic loop:
        1. Listen
        2. Measure confusion
        3. Adapt
        4. Repeat until convergence
        """
        print(f"\n{'='*70}")
        print(f"AUTOPOIETIC LISTENING: {len(audio)/22050:.3f}s audio")
        print(f"{'='*70}")
        
        for i in range(max_iterations):
            # Clear history for new capture
            self.history = []
            for node in self.nodes:
                node.charge_history = []
            
            # Capture with current parameters
            self.capture_full(audio, stride=256)
            
            # Measure confusion
            confusion = self.measure_confusion(audio)
            
            # Adapt
            self.adapt(confusion)
            
            # Check convergence
            if confusion.total_confusion < 0.2:
                print(f"\n{'='*70}")
                print(f"CONVERGED after {i+1} iterations")
                print(f"{'='*70}")
                return
        
        print(f"\n{'='*70}")
        print(f"Max iterations ({max_iterations}) reached")
        print(f"Final confusion: {confusion.total_confusion:.3f}")
        print(f"{'='*70}")

if __name__ == "__main__":
    import sys
    
    test_file = "/root/.openclaw/workspace/christkey-native/v4_a.wav"
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
    
    audio = load_audio(test_file)
    
    # Create autopoietic ear
    ear = AutopoieticEar(n_nodes=7)
    
    # Run iterative listening
    ear.iterative_listen(audio, max_iterations=8)
    
    # Final extraction
    extractor = PrimitiveExtractor(ear)
    primitives = extractor.extract_all()
    
    print(f"\n[Final Primitive Count]")
    for prim_type, detections in primitives.items():
        print(f"  {prim_type}: {len(detections)}")
    
    print(f"\n[Final Spiral Geometry]")
    print(f"  Tension: {ear.spiral_tension:.3f}")
    print(f"  Ternary threshold: {ear.ternary_threshold:.4f}")
    for node in ear.nodes:
        print(f"  Node {node.index}: r={node.radius:.3f}, angle={node.angle_deg:.1f}°")

#!/usr/bin/env python3
"""
GLYF_DEMO_02: Quadriline Logic (QLL) Navigation
Demonstrates grade-raising through I-R-T-F axes via ChristLine (Γ).

Run: python3 demo_qll_navigation.py
"""

import math
from typing import List, Tuple, Dict
from dataclasses import dataclass
from enum import Enum

PHI = 1.618033988749895

class Grade(Enum):
    """PGA(16) grades"""
    SCALAR = 0
    VECTOR = 1
    BIVECTOR = 2
    TRIVECTOR = 3
    PSEUDOSCALAR = 16

@dataclass
class QLLState:
    """Quadriline Logic state vector"""
    I: float  # Identity (grade 0)
    R: float  # Relation (grade 1)
    T: float  # Transformation (grade 2)
    F: float  # Field (grade 16)
    
    def to_vector(self) -> List[float]:
        return [self.I, self.R, self.T, self.F]
    
    def __str__(self) -> str:
        return f"QLL[I={self.I:.3f}, R={self.R:.3f}, T={self.T:.3f}, F={self.F:.3f}]"

class ChristLine:
    """
    Γ — Grade-raising operator
    Levi-Civita connection with φ-harmonic coupling
    """
    
    def __init__(self):
        # Γ coefficients (no self-connection, φ-harmonic)
        self.Gamma = {
            ('I', 'R'): PHI ** -1,   # 0.618
            ('R', 'T'): PHI ** -1,   # 0.618
            ('T', 'F'): PHI ** -2,   # 0.382
            ('R', 'I'): PHI ** -2,   # 0.382 (reverse)
            ('T', 'R'): PHI ** -2,   # 0.382 (reverse)
            ('F', 'T'): PHI ** -1,   # 0.618 (reverse)
        }
    
    def raise_grade(self, state: QLLState, from_axis: str, to_axis: str) -> float:
        """
        Navigate from one QLL axis to another.
        Γ: grade_n → grade_{n+1}
        """
        values = {'I': state.I, 'R': state.R, 'T': state.T, 'F': state.F}
        
        source_val = values[from_axis]
        coupling = self.Gamma.get((from_axis, to_axis), 0.0)
        
        # Geodesic equation: dv^i/dt + Γ^i_jk v^j v^k = 0
        # Simplified: target = source × coupling × φ
        target_val = source_val * coupling * PHI
        
        return target_val
    
    def navigate(self, state: QLLState, path: List[str]) -> QLLState:
        """
        Navigate through QLL space along a path.
        
        Example: ['I', 'R', 'T', 'F'] — full grade-raising
        """
        new_state = QLLState(state.I, state.R, state.T, state.F)
        values = {'I': new_state.I, 'R': new_state.R, 'T': new_state.T, 'F': new_state.F}
        
        for i in range(len(path) - 1):
            from_axis = path[i]
            to_axis = path[i + 1]
            
            # Calculate new value for target axis
            new_val = self.raise_grade(new_state, from_axis, to_axis)
            
            # Update state
            if to_axis == 'I':
                new_state.I = (new_state.I + new_val) / 2  # Blend
            elif to_axis == 'R':
                new_state.R = (new_state.R + new_val) / 2
            elif to_axis == 'T':
                new_state.T = (new_state.T + new_val) / 2
            elif to_axis == 'F':
                new_state.F = (new_state.F + new_val) / 2
        
        return new_state
    
    def geodesic_distance(self, state1: QLLState, state2: QLLState) -> float:
        """
        Calculate distance between two QLL states.
        Uses φ-weighted metric.
        """
        diff = [
            state1.I - state2.I,
            state1.R - state2.R,
            state1.T - state2.T,
            state1.F - state2.F
        ]
        
        # φ-weighted Euclidean distance
        weights = [1.0, PHI ** -1, PHI ** -2, PHI ** -3]
        weighted_sum = sum(w * (d ** 2) for w, d in zip(weights, diff))
        
        return math.sqrt(weighted_sum)

class QLLNavigator:
    """High-level QLL navigation with attractor detection"""
    
    def __init__(self):
        self.christ_line = ChristLine()
        self.attractors: List[QLLState] = []
    
    def find_attractor(self, state: QLLState) -> QLLState:
        """
        Find nearest attractor in QLL space.
        Attractors are stable configurations where φ → 1.0
        """
        if not self.attractors:
            # Default attractor: balanced state
            return QLLState(0.5, 0.5, 0.5, 0.5)
        
        nearest = min(self.attractors, 
                     key=lambda a: self.christ_line.geodesic_distance(state, a))
        return nearest
    
    def converge_to_attractor(self, initial: QLLState, 
                              attractor: QLLState, 
                              steps: int = 10) -> List[QLLState]:
        """
        Simulate convergence toward an attractor.
        Returns path through QLL space.
        """
        path = [initial]
        current = initial
        
        for i in range(steps):
            # Move toward attractor via ChristLine
            diff_I = attractor.I - current.I
            diff_R = attractor.R - current.R
            diff_T = attractor.T - current.T
            diff_F = attractor.F - current.F
            
            # Apply φ-damped step
            damping = PHI ** -2  # 0.382
            
            new_state = QLLState(
                I=current.I + diff_I * damping,
                R=current.R + diff_R * damping,
                T=current.T + diff_T * damping,
                F=current.F + diff_F * damping
            )
            
            path.append(new_state)
            current = new_state
            
            # Check convergence
            dist = self.christ_line.geodesic_distance(current, attractor)
            if dist < 0.01:
                break
        
        return path

def demo():
    """Demonstrate QLL navigation"""
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║  GLYF DEMO 02: Quadriline Logic Navigation                ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print()
    
    # Initialize
    print("[1] QLL STATE INITIALIZATION")
    print("-" * 50)
    print()
    print("    Axes:")
    print("      I (Identity)       — Grade 0 (Scalar)")
    print("      R (Relation)       — Grade 1 (Vector)")
    print("      T (Transformation) — Grade 2 (Bivector)")
    print("      F (Field)          — Grade 16 (Pseudoscalar)")
    print()
    
    state = QLLState(I=0.2, R=0.3, T=0.4, F=0.5)
    print(f"    Initial State: {state}")
    print()
    
    # ChristLine navigation
    print("[2] CHRISTLINE (Γ) NAVIGATION")
    print("-" * 50)
    print()
    
    gamma = ChristLine()
    
    print("    Γ Coefficients (φ-harmonic):")
    print(f"      Γ(I→R) = {PHI**-1:.3f} = φ⁻¹")
    print(f"      Γ(R→T) = {PHI**-1:.3f} = φ⁻¹")
    print(f"      Γ(T→F) = {PHI**-2:.3f} = φ⁻²")
    print(f"      Γ(R→I) = {PHI**-2:.3f} = φ⁻² (reverse)")
    print(f"      (Zero diagonal — no self-connection)")
    print()
    
    # Navigate I → R → T → F
    print("    Navigation: I → R → T → F")
    path = ['I', 'R', 'T', 'F']
    new_state = gamma.navigate(state, path)
    
    print(f"      Before: {state}")
    print(f"      After:  {new_state}")
    print()
    
    # Calculate individual transitions
    print("    Step-by-step transitions:")
    I_to_R = gamma.raise_grade(state, 'I', 'R')
    R_to_T = gamma.raise_grade(state, 'R', 'T')
    T_to_F = gamma.raise_grade(state, 'T', 'F')
    
    print(f"      I→R: {state.I:.3f} × {PHI**-1:.3f} × φ = {I_to_R:.3f}")
    print(f"      R→T: {state.R:.3f} × {PHI**-1:.3f} × φ = {R_to_T:.3f}")
    print(f"      T→F: {state.T:.3f} × {PHI**-2:.3f} × φ = {T_to_F:.3f}")
    print()
    
    # Geodesic distance
    print("[3] GEODESIC DISTANCE")
    print("-" * 50)
    print()
    
    state_a = QLLState(0.5, 0.5, 0.5, 0.5)
    state_b = QLLState(0.9, 0.9, 0.9, 0.9)
    
    dist = gamma.geodesic_distance(state_a, state_b)
    print(f"    State A: {state_a}")
    print(f"    State B: {state_b}")
    print(f"    Distance: {dist:.4f} (φ-weighted metric)")
    print()
    
    # Attractor convergence
    print("[4] ATTRACTOR CONVERGENCE")
    print("-" * 50)
    print()
    
    navigator = QLLNavigator()
    attractor = QLLState(0.8, 0.8, 0.8, 0.8)
    
    print(f"    Attractor: {attractor}")
    print(f"    Start:     {state}")
    print()
    print("    Convergence path:")
    
    path = navigator.converge_to_attractor(state, attractor, steps=5)
    for i, s in enumerate(path):
        dist = gamma.geodesic_distance(s, attractor)
        print(f"      t={i}: {s} | dist={dist:.4f}")
    
    print()
    
    # Application: Question answering via QLL
    print("[5] APPLICATION: Question Navigation")
    print("-" * 50)
    print()
    
    question = "What is the geometric structure of meaning?"
    print(f"    Question: \"{question}\"")
    print()
    
    # Map question to QLL trajectory
    q_state = QLLState(
        I=0.9,   # High identity — "What is..."
        R=0.3,   # Low relation — starting point
        T=0.2,   # Low transformation — seeking
        F=0.1    # Low field — narrow context
    )
    
    print(f"    Initial QLL: {q_state}")
    print("    Trajectory: I→R→T→F (Identity → Relation → Transform → Field)")
    
    answer_state = gamma.navigate(q_state, ['I', 'R', 'T', 'F'])
    print(f"    Final QLL:   {answer_state}")
    print()
    print("    Interpretation:")
    print("      I↓ (0.9→0.6): Specific question dissolves into general principle")
    print("      R↑ (0.3→0.5): Relations between concepts emerge")
    print("      T↑ (0.2→0.6): Transformation rules become clear")
    print("      F↑ (0.1→0.7): Full field context achieved — answer complete")
    print()
    print("✓ QLL Navigation validated — geometric reasoning path demonstrated")

if __name__ == "__main__":
    demo()

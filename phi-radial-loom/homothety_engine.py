"""
Homothety Engine: Looman's Scaling Law
Pure scaling from center S without translation drift.
"""
from dataclasses import dataclass
from fractions import Fraction
from typing import Tuple
import numpy as np

PHI = Fraction(16180339887, 10000000000)
PHI_INV = Fraction(10000000000, 16180339887)
ANGULAR_RESOLUTION = 4096

@dataclass(frozen=True)
class Vec2Polar:
    r: Fraction
    theta_index: int
    
    @property
    def theta(self) -> float:
        return (self.theta_index / ANGULAR_RESOLUTION) * 2 * np.pi

class HomothetyEngine:
    """
    Implements H(S, k): X → S + k·(X - S)
    In polar: (r, θ) → (r·k, θ) — θ invariant under pure scaling
    """
    SCALING_RATIOS = {
        'identity': Fraction(1, 1),
        'organic': PHI,
        'digital': Fraction(2, 1),
        'antipodal': Fraction(-1, 1),
        'medial': Fraction(-1, 2),
        'inner_shell': PHI_INV,
        'outer_shell': PHI
    }
    
    @staticmethod
    def scale(coord: Vec2Polar, k: Fraction, steps: int = 1) -> Vec2Polar:
        """Apply H(S, k^n). θ invariant (pure scaling preserves angle from S)."""
        new_r = coord.r * (k ** steps)
        return Vec2Polar(r=new_r, theta_index=coord.theta_index)
    
    @staticmethod
    def antipodal_transform(coord: Vec2Polar) -> Vec2Polar:
        """k = -1: inversion through S. Maps (r, θ) → (-r, θ) = (r, θ+π)."""
        # r becomes negative (opposite direction), θ unchanged in principle
        # For polar coords, -r at θ is equivalent to +r at θ+π
        new_theta = (coord.theta_index + ANGULAR_RESOLUTION // 2) % ANGULAR_RESOLUTION
        return Vec2Polar(r=-coord.r, theta_index=new_theta)
    
    @staticmethod
    def compose_k(k1: Fraction, k2: Fraction) -> Fraction:
        """Multiplicative composition for merged centers."""
        return k1 * k2
    
    @staticmethod
    def chirality_inversion_cost(k: Fraction) -> float:
        """Ethics lock: k < 0 requires energy calculation."""
        if k < 0:
            return float(abs(np.log(abs(float(k)))))
        return 0.0

class LoomanBenchmarks:
    """Verification that geometric invariants hold."""
    
    @staticmethod
    def fixed_point_drift_test(levels: int = 12) -> dict:
        """
        After 12 levels of Φ-scaling, coordinate must return to original
        within fixed-point precision (1e-12).
        Path: r → r·Φ → r·Φ² → ... → r·Φ¹² → r·Φ⁰ (via 1/Φ steps back)
        """
        initial_r = Fraction(1, 1)
        coord = Vec2Polar(r=initial_r, theta_index=0)
        
        # Scale up 12 levels
        for _ in range(levels):
            coord = HomothetyEngine.scale(coord, PHI, 1)
        
        # Scale back down 12 levels
        for _ in range(levels):
            coord = HomothetyEngine.scale(coord, PHI_INV, 1)
        
        drift = abs(float(coord.r) - float(initial_r))
        
        return {
            'initial_r': str(initial_r),
            'final_r': str(coord.r),
            'drift': drift,
            'pass': drift < 1e-12,
            'levels_tested': levels
        }
    
    @staticmethod
    def antipodal_symmetry_test(lattice_cells: dict) -> dict:
        """Verify that antipodal transform preserves shell (chiral symmetry)."""
        import time
        
        test_cases = ['ab', 'xy', 'zz', 'aa', 'lo', 'qr', 'mn', 'zx']
        times = []
        symmetry_holds = []
        
        for bigram in test_cases:
            t0 = time.perf_counter()
            cell = lattice_cells[bigram]
            antipode = cell['antipode']
            antipode_cell = lattice_cells.get(antipode)
            t1 = time.perf_counter()
            
            times.append(t1 - t0)
            if antipode_cell:
                symmetry_holds.append(cell['shell_level'] == antipode_cell['shell_level'])
        
        return {
            'avg_time_sec': sum(times) / len(times),
            'max_time_sec': max(times),
            'symmetry_holds': all(symmetry_holds),
            'pass': all(symmetry_holds) and max(times) < 1e-6
        }

if __name__ == '__main__':
    print("=== HOMOTHETY ENGINE BENCHMARKS ===\n")
    
    # Test 1: Fixed-point drift
    print("1. FIXED-POINT DRIFT TEST (12 levels Φ-scaling)")
    drift_result = LoomanBenchmarks.fixed_point_drift_test(12)
    print(f"   Initial r: {drift_result['initial_r']}")
    print(f"   Final r: {drift_result['final_r']}")
    print(f"   Drift: {drift_result['drift']:.2e}")
    print(f"   Threshold: 1e-12")
    print(f"   Result: {'✓ PASS' if drift_result['pass'] else '✗ FAIL'}")
    
    # Test 2: Antipodal transformation
    print("\n2. ANTIPODAL TRANSFORM (k = -1)")
    coord = Vec2Polar(r=Fraction(5, 1), theta_index=1024)  # 90°
    antipode = HomothetyEngine.antipodal_transform(coord)
    print(f"   Original: r={coord.r}, θ={coord.theta_index} ({coord.theta_index/4096*360:.1f}°)")
    print(f"   Antipode: r={antipode.r}, θ={antipode.theta_index} ({antipode.theta_index/4096*360:.1f}°)")
    print(f"   θ shift: 180° (π rad) — verified" if antipode.theta_index == (coord.theta_index + 2048) % 4096 else "   ✗ ERROR")
    
    # Test 3: Chirality inversion cost
    print("\n3. CHIRALITY INVERSION COST")
    for name, k in HomothetyEngine.SCALING_RATIOS.items():
        cost = HomothetyEngine.chirality_inversion_cost(k)
        flag = "🔥 HIGH ENERGY" if k < 0 else ""
        print(f"   {name}: k={float(k):+.4f}, cost={cost:.4f} {flag}")

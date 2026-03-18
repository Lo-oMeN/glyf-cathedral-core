"""
Φ-Radial Mind Loom: Coordinate Crystallization
Generates fixed-point coordinates for all 676 bigrams.
"""
from dataclasses import dataclass
from typing import Dict, Tuple
from fractions import Fraction
import json
import numpy as np

FIXED_PRECISION = 10**12
PHI = Fraction(16180339887, 10000000000)  # Φ ≈ 1.6180339887
PHI_INV = Fraction(10000000000, 16180339887)  # 1/Φ ≈ 0.618
GOLDEN_ANGLE_DEG = 137.507764  # degrees
ANGULAR_RESOLUTION = 4096  # 12-bit

@dataclass(frozen=True)
class Vec2Polar:
    r: Fraction
    theta_index: int  # 0-4095
    
    @property
    def theta(self) -> float:
        return (self.theta_index / ANGULAR_RESOLUTION) * 2 * np.pi
    
    def to_cartesian(self) -> Tuple[Fraction, Fraction]:
        x = self.r * Fraction(np.cos(self.theta)).limit_denominator(1000)
        y = self.r * Fraction(np.sin(self.theta)).limit_denominator(1000)
        return (x, y)

@dataclass
class BigramCell:
    bigram: str
    shell_level: int  # 0-6
    base_coordinate: Vec2Polar
    semantic_density: Fraction
    children: list
    antipode: str

def crystallize_lattice() -> Dict:
    """
    Forge the 676 seeds. Each bigram assigned:
    - Shell via (i+j) mod 7 → maps to 7 glyphs
    - Theta via golden angle distribution (prevents clustering)
    - Radius via r = Φ^shell (organic growth from S)
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    cells = {}
    radial_index = {n: [] for n in range(7)}
    
    # Golden angle in 12-bit steps
    golden_angle_steps = int((GOLDEN_ANGLE_DEG / 360) * ANGULAR_RESOLUTION)
    
    for i, char1 in enumerate(alphabet):
        for j, char2 in enumerate(alphabet):
            bigram = char1 + char2
            
            # Shell assignment: (i+j) mod 7
            shell = (i + j) % 7
            
            # Theta: golden angle distribution
            # Index in 0-675 sequence
            linear_idx = i * 26 + j
            theta_idx = (linear_idx * golden_angle_steps) % ANGULAR_RESOLUTION
            
            # Radius: r = Φ^shell × r_0, r_0 = 1
            r = PHI ** shell
            
            # Semantic density: inner shells denser (1/(shell+1))
            density = Fraction(1, shell + 1)
            
            # Antipode: reversed bigram
            antipode = bigram[::-1]
            
            coord = Vec2Polar(r=r, theta_index=theta_idx)
            
            cells[bigram] = {
                'bigram': bigram,
                'shell_level': shell,
                'r': str(r),  # Fraction as exact string
                'theta_index': theta_idx,
                'theta_degrees': round(theta_idx * 360 / ANGULAR_RESOLUTION, 4),
                'semantic_density': str(density),
                'antipode': antipode,
                'cartesian_approx': {
                    'x': float(coord.to_cartesian()[0]),
                    'y': float(coord.to_cartesian()[1])
                }
            }
            
            radial_index[shell].append(bigram)
    
    return {
        'metadata': {
            'total_cells': 676,
            'angular_resolution_bits': 12,
            'phi_numerator': 16180339887,
            'phi_denominator': 10000000000,
            'golden_angle_degrees': GOLDEN_ANGLE_DEG,
            'center_S': {'r': '0', 'theta_index': 0}
        },
        'cells': cells,
        'radial_index': radial_index,
        'shell_stats': {
            shell: {
                'count': len(bigrams),
                'radius_factor': str(PHI ** shell),
                'sample_bigrams': bigrams[:5]
            }
            for shell, bigrams in radial_index.items()
        }
    }

if __name__ == '__main__':
    lattice = crystallize_lattice()
    
    # Output crystallized lattice
    output_path = '/root/.openclaw/workspace/phi-radial-loom/lattice_crystallized.json'
    with open(output_path, 'w') as f:
        json.dump(lattice, f, indent=2)
    
    print(f"✓ Lattice crystallized: {lattice['metadata']['total_cells']} cells")
    print(f"✓ Shell distribution:")
    for shell, stats in lattice['shell_stats'].items():
        print(f"  Shell {shell}: {stats['count']} cells @ r=Φ^{shell}")
    print(f"✓ Output: {output_path}")
    
    # Sample verification
    sample = lattice['cells']['ab']
    print(f"\n✓ Sample cell 'ab':")
    print(f"  Shell: {sample['shell_level']}")
    print(f"  r: {sample['r']}")
    print(f"  θ: {sample['theta_degrees']}° (index {sample['theta_index']})")
    print(f"  Antipode: {sample['antipode']}")

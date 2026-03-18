#!/usr/bin/env python3
"""
Φ-Radial Mind Loom - Black Edge Alpha
Top 50 English Bigram Lattice Placement System

Uses polar coordinates: (r = k^n, θ = m · 0.088°) where k = Φ ≈ 1.618
Implements continuous homothety scaling with Φ/1/1/Φ pattern
"""

import math
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
import json

# Golden Ratio
PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.618033988749895

# Angular step (degrees) - fine resolution for 676-slot lattice
# 0.088° ≈ 360°/4096, gives precise angular positioning
DELTA_THETA = 0.088

# Base radius unit
R0 = 1.0


@dataclass
class Bigram:
    """Represents a bigram with its frequency and lattice coordinates"""
    pair: str                    # The bigram (e.g., "TH")
    frequency: float             # Relative frequency (0-1)
    rank: int                    # Frequency rank (1 = most common)
    
    # Polar coordinates (calculated)
    n: int = 0                   # Radial exponent
    m: int = 0                   # Angular multiplier
    r: float = 0.0               # Radius = R0 * PHI^n
    theta: float = 0.0           # Angle in degrees
    theta_rad: float = 0.0       # Angle in radians
    
    # Cartesian coordinates (derived)
    x: float = 0.0
    y: float = 0.0
    
    # Homothety scaling factor
    scale: float = 1.0
    
    def __post_init__(self):
        self.pair = self.pair.upper()


@dataclass
class HomothetyRing:
    """Defines a homothety scaling ring with Φ-based pattern"""
    ring_id: int
    base_scale: float
    pattern: List[float]  # [Φ, 1, 1, 1/Φ] repeating pattern
    
    def get_scale(self, position: int) -> float:
        """Get scale factor at a specific position in the ring"""
        return self.pattern[position % len(self.pattern)]


class PhiRadialMindLoom:
    """
    Φ-Radial Mind Loom - Places bigrams on a polar lattice
    
    Architecture:
    - 676 slots (26x26 letter pairs) mapped to polar coordinates
    - Radius grows exponentially: r = R0 * PHI^n
    - Angle increments by DELTA_THETA per slot
    - Homothety scaling creates visual hierarchy
    """
    
    def __init__(self, r0: float = R0, delta_theta: float = DELTA_THETA):
        self.PHI = PHI
        self.r0 = r0
        self.delta_theta = delta_theta
        self.bigrams: List[Bigram] = []
        self.total_slots = 676  # 26 x 26
        
        # Homothety ring configuration (Φ/1/1/Φ pattern)
        self.homothety_pattern = [PHI, 1.0, 1.0, 1.0/PHI]
        
        # Top 50 English bigrams by frequency (from Cornell/Norvig data)
        self.top_50_data = [
            ("TH", 0.0352), ("HE", 0.0305), ("IN", 0.0243), ("ER", 0.0205),
            ("AN", 0.0194), ("RE", 0.0173), ("ND", 0.0168), ("AT", 0.0159),
            ("ON", 0.0157), ("NT", 0.0156), ("HA", 0.0156), ("ES", 0.0156),
            ("ST", 0.0155), ("EN", 0.0155), ("ED", 0.0153), ("TO", 0.0152),
            ("IT", 0.0150), ("OU", 0.0150), ("EA", 0.0147), ("HI", 0.0146),
            ("IS", 0.0146), ("OR", 0.0143), ("TI", 0.0134), ("AS", 0.0133),
            ("TE", 0.0127), ("ET", 0.0119), ("NG", 0.0118), ("OF", 0.0116),
            ("AL", 0.0109), ("DE", 0.0109), ("SE", 0.0108), ("LE", 0.0108),
            ("SA", 0.0106), ("SI", 0.0105), ("AR", 0.0104), ("VE", 0.0104),
            ("RA", 0.0104), ("LD", 0.0102), ("UR", 0.0102), ("BE", 0.0098),
            ("ME", 0.0095), ("CO", 0.0092), ("RO", 0.0089), ("CA", 0.0087),
            ("NE", 0.0085), ("CH", 0.0084), ("LL", 0.0083), ("SS", 0.0082),
            ("EE", 0.0081), ("TT", 0.0080), ("FF", 0.0079), ("RR", 0.0078)
        ]
    
    def letter_to_index(self, letter: str) -> int:
        """Convert A-Z to 0-25"""
        return ord(letter.upper()) - ord('A')
    
    def bigram_to_slot(self, bigram: str) -> int:
        """
        Map bigram to slot number (0-675)
        AA=0, AB=1, ..., AZ=25, BA=26, ..., ZZ=675
        """
        b = bigram.upper()
        if len(b) != 2 or not b.isalpha():
            raise ValueError(f"Invalid bigram: {bigram}")
        return self.letter_to_index(b[0]) * 26 + self.letter_to_index(b[1])
    
    def slot_to_bigram(self, slot: int) -> str:
        """Convert slot number back to bigram"""
        if not (0 <= slot < 676):
            raise ValueError(f"Slot must be 0-675, got {slot}")
        first = chr(ord('A') + slot // 26)
        second = chr(ord('A') + slot % 26)
        return first + second
    
    def calculate_radial_distribution(self, num_bigrams: int = 50) -> Tuple[int, int]:
        """
        Determine optimal radial rings and angular spacing
        Returns (rings, slots_per_ring)
        """
        # Distribute 50 bigrams across radial rings
        # Using fibonacci-like distribution for aesthetic balance
        rings = 5
        slots_per_ring = (num_bigrams + rings - 1) // rings  # ceil division
        return rings, slots_per_ring
    
    def assign_coordinates(self, bigram: Bigram, ring: int, position: int) -> Bigram:
        """
        Assign polar coordinates to a bigram
        
        Formula:
        - r = r0 * PHI^n where n is the radial ring
        - θ = m * delta_theta where m is the angular position
        """
        # Radial exponent based on ring (center = higher frequency)
        bigram.n = ring
        bigram.r = self.r0 * (self.PHI ** ring)
        
        # Angular position (spiral outward)
        bigram.m = position
        bigram.theta = position * self.delta_theta
        bigram.theta_rad = math.radians(bigram.theta)
        
        # Convert to Cartesian
        bigram.x = bigram.r * math.cos(bigram.theta_rad)
        bigram.y = bigram.r * math.sin(bigram.theta_rad)
        
        # Apply homothety scaling
        bigram.scale = self.homothety_pattern[position % len(self.homothety_pattern)]
        
        return bigram
    
    def build_lattice(self) -> List[Bigram]:
        """
        Build the complete Φ-Radial lattice for top 50 bigrams
        Places bigrams in concentric rings with optimal spacing
        """
        self.bigrams = []
        rings, slots_per_ring = self.calculate_radial_distribution(50)
        
        # Sort by frequency (already sorted, but ensure)
        sorted_data = sorted(self.top_50_data, key=lambda x: x[1], reverse=True)
        
        idx = 0
        for ring in range(rings):
            # Inner rings get higher frequency bigrams
            slots_in_this_ring = min(slots_per_ring, 50 - idx)
            
            # Angular offset per ring (golden angle for optimal packing)
            golden_angle = 137.5077640500378  # degrees
            ring_offset = ring * golden_angle / self.delta_theta
            
            for pos in range(slots_in_this_ring):
                pair, freq = sorted_data[idx]
                bigram = Bigram(
                    pair=pair,
                    frequency=freq,
                    rank=idx + 1
                )
                
                # Calculate angular position with golden angle offset
                angular_pos = int(ring_offset + pos * (360 / slots_in_this_ring) / self.delta_theta)
                
                self.assign_coordinates(bigram, ring, angular_pos)
                self.bigrams.append(bigram)
                idx += 1
                
                if idx >= 50:
                    break
            
            if idx >= 50:
                break
        
        return self.bigrams
    
    def detect_overlaps(self, min_distance: float = None) -> List[Tuple[Bigram, Bigram, float]]:
        """
        Detect overlapping bigrams based on Cartesian distance
        Returns list of (bigram1, bigram2, distance) tuples
        """
        if min_distance is None:
            # Default: minimum distance based on average frequency
            min_distance = self.r0 * 0.5
        
        overlaps = []
        n = len(self.bigrams)
        
        for i in range(n):
            for j in range(i + 1, n):
                b1, b2 = self.bigrams[i], self.bigrams[j]
                dist = math.sqrt((b1.x - b2.x)**2 + (b1.y - b2.y)**2)
                
                if dist < min_distance:
                    overlaps.append((b1, b2, dist))
        
        return overlaps
    
    def get_adjacent_bigrams(self, bigram: Bigram) -> List[Bigram]:
        """Find spatially adjacent bigrams (neighbors in lattice)"""
        neighbors = []
        for b in self.bigrams:
            if b.pair == bigram.pair:
                continue
            # Adjacent if within one ring and close angle
            if abs(b.n - bigram.n) <= 1:
                angle_diff = abs(b.theta - bigram.theta)
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff
                if angle_diff < 5.0:  # Within 5 degrees
                    neighbors.append(b)
        return neighbors
    
    def export_coordinates(self) -> Dict:
        """Export all bigram coordinates as structured data"""
        return {
            "metadata": {
                "phi": self.PHI,
                "delta_theta": self.delta_theta,
                "r0": self.r0,
                "total_bigrams": len(self.bigrams),
                "homothety_pattern": self.homothety_pattern
            },
            "bigrams": [
                {
                    "pair": b.pair,
                    "frequency": b.frequency,
                    "rank": b.rank,
                    "polar": {
                        "r": round(b.r, 6),
                        "theta": round(b.theta, 4),
                        "n": b.n,
                        "m": b.m
                    },
                    "cartesian": {
                        "x": round(b.x, 6),
                        "y": round(b.y, 6)
                    },
                    "scale": round(b.scale, 4)
                }
                for b in self.bigrams
            ]
        }
    
    def print_lattice_table(self):
        """Print formatted lattice placement table"""
        print("=" * 100)
        print("Φ-RADIAL MIND LOOM - BLACK EDGE ALPHA")
        print(f"Golden Ratio Φ = {self.PHI:.10f}")
        print(f"Angular Step = {self.delta_theta}° = 360°/{360/self.delta_theta:.0f}")
        print("=" * 100)
        print(f"{'Rank':>4} │ {'Bigram':>6} │ {'Freq%':>6} │ {'Ring':>4} │ {'n':>3} │ {'m':>6} │ {'r = Φⁿ':>10} │ {'θ°':>8} │ {'Scale':>6} │ {'x':>10} │ {'y':>10}")
        print("-" * 100)
        
        for b in sorted(self.bigrams, key=lambda x: x.rank):
            print(f"{b.rank:>4} │ {b.pair:>6} │ {b.frequency*100:>6.2f} │ {b.n:>4} │ {b.n:>3} │ {b.m:>6} │ {b.r:>10.4f} │ {b.theta:>8.2f} │ {b.scale:>6.3f} │ {b.x:>10.4f} │ {b.y:>10.4f}")
        
        print("-" * 100)
    
    def print_overlap_report(self):
        """Print overlap detection report"""
        overlaps = self.detect_overlaps()
        
        print("\n" + "=" * 80)
        print("OVERLAP DETECTION REPORT")
        print("=" * 80)
        
        if not overlaps:
            print("✓ No overlaps detected with current spacing")
        else:
            print(f"⚠ Detected {len(overlaps)} potential overlaps:\n")
            print(f"{'Bigram 1':>8} │ {'Bigram 2':>8} │ {'Distance':>10} │ {'Status'}")
            print("-" * 50)
            for b1, b2, dist in overlaps:
                status = "CRITICAL" if dist < self.r0 * 0.3 else "WARNING"
                print(f"{b1.pair:>8} │ {b2.pair:>8} │ {dist:>10.4f} │ {status}")
        
        # Check adjacent bigrams
        print("\n" + "-" * 80)
        print("ADJACENCY ANALYSIS (nearest neighbors)")
        print("-" * 80)
        
        for b in self.bigrams[:10]:  # Show top 10
            neighbors = self.get_adjacent_bigrams(b)
            if neighbors:
                neighbor_str = ", ".join([n.pair for n in neighbors[:3]])
                print(f"{b.pair}: adjacent to [{neighbor_str}]")


def main():
    """Main execution - build and analyze the Φ-Radial Mind Loom"""
    print("\n🔮 Initializing Φ-Radial Mind Loom...\n")
    
    # Create the loom
    loom = PhiRadialMindLoom()
    
    # Build lattice
    loom.build_lattice()
    
    # Print coordinate table
    loom.print_lattice_table()
    
    # Print overlap report
    loom.print_overlap_report()
    
    # Export to JSON
    data = loom.export_coordinates()
    with open('/root/.openclaw/workspace/black_edge_alpha_bigrams.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("\n" + "=" * 80)
    print(f"📁 Exported coordinates to: black_edge_alpha_bigrams.json")
    print("=" * 80)
    
    # Summary statistics
    print("\n📊 LATTICE STATISTICS")
    print("-" * 40)
    print(f"Total bigrams placed: {len(loom.bigrams)}")
    print(f"Radial rings used: {max(b.n for b in loom.bigrams) + 1}")
    print(f"Angular range: {min(b.theta for b in loom.bigrams):.2f}° to {max(b.theta for b in loom.bigrams):.2f}°")
    print(f"Radius range: {min(b.r for b in loom.bigrams):.4f} to {max(b.r for b in loom.bigrams):.4f}")
    print(f"Homothety pattern: Φ/{1}/{1}/1/Φ = {PHI:.3f}/1.0/1.0/{1/PHI:.3f}")
    
    return loom


if __name__ == "__main__":
    loom = main()

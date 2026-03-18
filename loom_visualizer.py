#!/usr/bin/env python3
"""
Φ-Radial Mind Loom Visualizer
Generates ASCII art and coordinate visualization
"""

import math
from phi_radial_mind_loom import PhiRadialMindLoom, PHI

def generate_ascii_loom():
    """Generate ASCII art representation of the loom"""
    loom = PhiRadialMindLoom()
    loom.build_lattice()
    
    # Create canvas
    width, height = 80, 40
    canvas = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Center point
    cx, cy = width // 2, height // 2
    
    # Scale factor for visualization
    scale = 5.5
    
    # Draw concentric rings (radial levels)
    for ring in range(5):
        r = (PHI ** ring) * scale
        # Draw approximate circle
        for angle in range(0, 360, 10):
            rad = math.radians(angle)
            x = int(cx + r * math.cos(rad))
            y = int(cy + r * math.sin(rad) * 0.5)  # 0.5 for aspect ratio
            if 0 <= x < width and 0 <= y < height:
                canvas[y][x] = '·'
    
    # Place bigrams
    for b in loom.bigrams:
        x = int(cx + b.x * scale)
        y = int(cy + b.y * scale * 0.5)  # Aspect ratio correction
        if 0 <= x < width and 0 <= y < height:
            # Use different symbols based on ring
            symbols = ['●', '○', '◐', '◑', '◒']
            symbol = symbols[b.n % len(symbols)]
            canvas[y][x] = symbol
    
    # Center marker
    canvas[cy][cx] = '⊕'
    
    return '\n'.join(''.join(row) for row in canvas)


def generate_ring_diagram():
    """Generate ring-based placement diagram"""
    loom = PhiRadialMindLoom()
    loom.build_lattice()
    
    lines = []
    lines.append("\n" + "=" * 70)
    lines.append("RADIAL RING PLACEMENT DIAGRAM")
    lines.append("=" * 70)
    lines.append("")
    lines.append("Ring │ Radius (Φⁿ) │ Bigrams Placed")
    lines.append("-" * 70)
    
    rings = {}
    for b in loom.bigrams:
        if b.n not in rings:
            rings[b.n] = []
        rings[b.n].append(b)
    
    for ring in sorted(rings.keys()):
        bigrams = rings[ring]
        radius = PHI ** ring
        names = ', '.join([b.pair for b in bigrams])
        lines.append(f"  {ring}  │   {radius:>8.4f}    │ {names}")
    
    lines.append("-" * 70)
    return '\n'.join(lines)


def generate_frequency_heatmap():
    """Generate text-based frequency heatmap"""
    loom = PhiRadialMindLoom()
    loom.build_lattice()
    
    lines = []
    lines.append("\n" + "=" * 70)
    lines.append("FREQUENCY-BASED HEATMAP (█ = highest frequency)")
    lines.append("=" * 70)
    
    for b in sorted(loom.bigrams, key=lambda x: x.frequency, reverse=True):
        bar_len = int(b.frequency * 100)
        bar = '█' * bar_len + '░' * (10 - bar_len)
        lines.append(f"{b.pair}: {bar} {b.frequency*100:.2f}% [Ring {b.n}, θ={b.theta:.1f}°]")
    
    return '\n'.join(lines)


def generate_semantic_clusters():
    """Group bigrams by semantic similarity"""
    clusters = {
        "Articles/Determiners": ["TH", "AT", "AN"],
        "Prepositions": ["IN", "ON", "OF", "TO"],
        "Verb Endings": ["ED", "ES", "EN", "NG"],
        "Pronouns/References": ["HE", "HI", "ME", "IT", "IS"],
        "Common Roots": ["ER", "RE", "OR", "AR", "UR"],
        "Comparatives/Superlatives": ["ER", "ST"],
        "Possessives": ["ES", "SS"],
        "Negation/Dual": ["ND", "NT", "NE"],
        "Past Tense": ["ED", "ET", "AT"],
        "Doubles": ["LL", "SS", "EE", "TT", "FF", "RR"]
    }
    
    lines = []
    lines.append("\n" + "=" * 70)
    lines.append("SEMANTIC CLUSTERS (Potential Activation Groups)")
    lines.append("=" * 70)
    
    for cluster, bigrams in clusters.items():
        found = [b for b in bigrams]
        lines.append(f"\n{cluster}:")
        lines.append(f"  Bigrams: {', '.join(found)}")
    
    return '\n'.join(lines)


if __name__ == "__main__":
    print("\n" + "🔮" * 35)
    print("           Φ-RADIAL MIND LOOM VISUALIZATION")
    print("🔮" * 35)
    
    print(generate_ring_diagram())
    print(generate_frequency_heatmap())
    print(generate_semantic_clusters())
    
    print("\n" + "=" * 70)
    print("ASCII VISUALIZATION (● = Ring 0, ○ = Ring 1, ◐ = Ring 2, etc.)")
    print("=" * 70)
    print(generate_ascii_loom())

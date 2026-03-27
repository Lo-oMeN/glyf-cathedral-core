#!/usr/bin/env python3
"""
Test and demonstration of the Glyphobetic Decomposer - 7-Segment Edition.

Shows how to use the decomposer to analyze words as 7-segment displays.
"""

import json
import sys
sys.path.insert(0, '/root/.openclaw/workspace')

from glyf.core.decomposer import (
    GlyphobeticDecomposer,
    decompose_word,
    create_simple_ast,
    compute_trajectory,
    SegmentGrid,
    SegmentType,
)


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def demo_basic_decomposition():
    """Demonstrate basic word decomposition."""
    print_section("BASIC WORD DECOMPOSITION")
    
    word = "HELLO"
    features = decompose_word(word)
    
    print(f"\nWord: {word}")
    print(f"\nSegment Bitmaps (7-bit per position):")
    for i, (bm, bin_str) in enumerate(zip(
        features.bitmaps, 
        [format(b, '07b') for b in features.bitmaps]
    )):
        print(f"  Position {i}: {bin_str} = {bm}")
    
    print(f"\n7D Feature Vector (normalized):")
    fv = features.feature_vector
    vector = fv.normalized.to_array()
    segments = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    for seg, val in zip(segments, vector):
        bar = "█" * int(val * 30)
        print(f"  Segment {seg}: {val:.4f} {bar}")
    
    print(f"\nDominant Segment: {fv.dominant_segment}")
    print(f"Segment Balance: {fv.segment_balance:.4f}")
    print(f"Horizontal/Vertical Ratio: {fv.horizontal_vertical_ratio:.4f}")
    print(f"Enclosure Score: {fv.enclosure_score:.4f}")


def demo_segment_patterns():
    """Show segment activation pattern analysis."""
    print_section("SEGMENT ACTIVATION PATTERNS")
    
    words = ["HELLO", "WORLD", "TEST", "888"]
    
    for word in words:
        features = decompose_word(word)
        pattern = features.segment_patterns
        
        print(f"\n  Word: '{word}'")
        print(f"    Bitmaps: {[format(b, '07b') for b in features.bitmaps]}")
        print(f"    Most Common: {format(pattern.most_common_bitmap, '07b')}")
        print(f"    Pattern Entropy: {pattern.pattern_entropy:.4f}")
        print(f"    Pattern Transitions: {pattern.pattern_transitions}")
        print(f"    Fill Ratio: {features.fill_ratio:.4f}")
        print(f"    Symmetry Score: {features.symmetry_score:.4f}")


def demo_geometric_analysis():
    """Show geometric calculations."""
    print_section("GEOMETRIC ANALYSIS")
    
    word = "CAT"
    features = decompose_word(word, letter_spacing=1.5)
    
    print(f"\nWord: {word}")
    
    print(f"\nBounding Box:")
    bb = features.bounding_box
    print(f"  Dimensions: {bb.width:.2f} x {bb.height:.2f}")
    print(f"  Center: ({bb.center.x:.2f}, {bb.center.y:.2f})")
    
    print(f"\nCentroid:")
    cent = features.centroid
    print(f"  Position: ({cent.position.x:.2f}, {cent.position.y:.2f})")
    print(f"  Mass (active segments): {cent.mass}")
    print(f"  Spread: {cent.spread:.4f}")
    
    print(f"\nComposition Mode: {features.composition_mode.name}")
    print(f"Density: {features.density:.4f} segments/unit²")


def demo_trajectory():
    """Show trajectory calculation between words."""
    print_section("TRAJECTORY CALCULATION")
    
    word_pairs = [
        ("HELLO", "WORLD"),
        ("CAT", "DOG"),
        ("SOS", "HELP"),
        ("888", "000"),
    ]
    
    for w1, w2 in word_pairs:
        result = compute_trajectory(w1, w2)
        traj = result['trajectory']
        
        print(f"\n  {w1} → {w2}")
        print(f"    Source Bitmap: {[format(b, '07b') for b in result['source_bitmap']]}")
        print(f"    Target Bitmap: {[format(b, '07b') for b in result['target_bitmap']]}")
        print(f"    Distance: {traj['distance']:.4f}")
        print(f"    Similarity: {traj['similarity']:.4f}")
        print(f"    Dominant Change: Segment {traj['dominant_change']}")


def demo_individual_grids():
    """Show individual letter grid representation."""
    print_section("INDIVIDUAL LETTER GRIDS")
    
    letters = ['A', 'B', 'C', 'D', 'E', 'F', '0', '1', '8']
    
    for letter in letters:
        grid = SegmentGrid.from_letter(letter)
        
        print(f"\n  Letter '{letter}':")
        print(f"    Bitmap: {format(grid.bitmap, '07b')} = {grid.bitmap}")
        print(f"    Active: {grid.active_count}/7")
        print(f"    Segments: {[s.name for s in grid.active_segments]}")
        
        # Visual representation
        visual = grid_to_visual(grid)
        for line in visual:
            print(f"    {line}")


def grid_to_visual(grid: SegmentGrid) -> list:
    """Create ASCII art representation of segment grid."""
    seg = lambda s: "█" if grid.segments[s].active else " "
    
    return [
        f" {seg(SegmentType.A)*3} ",
        f"{seg(SegmentType.F)}   {seg(SegmentType.B)}",
        f"{seg(SegmentType.F)}   {seg(SegmentType.B)}",
        f" {seg(SegmentType.G)*3} ",
        f"{seg(SegmentType.E)}   {seg(SegmentType.C)}",
        f"{seg(SegmentType.E)}   {seg(SegmentType.C)}",
        f" {seg(SegmentType.D)*3} ",
    ]


def demo_full_output():
    """Show full JSON output."""
    print_section("FULL JSON OUTPUT")
    
    word = "ABC"
    features = decompose_word(word)
    
    output = {
        "word": word,
        "analysis": features.to_dict()
    }
    
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  GLYPHOBETIC DECOMPOSER - 7-SEGMENT EDITION")
    print("  Canonical Display Grid Analysis System")
    print("="*60)
    
    demo_basic_decomposition()
    demo_segment_patterns()
    demo_geometric_analysis()
    demo_trajectory()
    demo_individual_grids()
    demo_full_output()
    
    print("\n" + "="*60)
    print("  DEMO COMPLETE")
    print("="*60 + "\n")

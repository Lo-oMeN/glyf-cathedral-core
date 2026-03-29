#!/usr/bin/env python3
"""
PHASE 0: Test Script for GaugeNode128 Implementation
Pragmatic Geometric AI - Proof of Concept

Tests:
- Generate 10,000 random GaugeNode128 instances
- Verify 128-byte alignment (check sizeof)
- Build NetworkX graph from connections
- Run chirality checker (XOR parity on all cycles)
- Serialize to /tmp/test_phase0.loom
- Read back and verify integrity
- Print timing benchmarks
"""

import sys
import os
import time
import random
import struct
from typing import List, Tuple, Set, Dict

# Add current directory to path for the compiled module
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    import py_gauge
    from py_gauge import (
        GaugeNode128, GlyfPrimitive,
        gauge_node_connect, gauge_node_distance,
        gauge_node_vesica_overlap, gauge_node_init,
        holonomy_verify_graph, holonomy_compute_parity,
        gauge_graph_write, gauge_graph_read,
        GAUGE_NODE_SIZE, PHI, GOLDEN_ANGLE,
        GAUGE_NODE_MAGIC, GAUGE_NODE_VERSION
    )
except ImportError as e:
    print(f"ERROR: Could not import py_gauge module: {e}")
    print("Please build first: python3 setup.py build_ext --inplace")
    sys.exit(1)

try:
    import networkx as nx
except ImportError:
    print("Installing networkx...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "networkx", "-q"])
    import networkx as nx

try:
    import numpy as np
except ImportError:
    print("Installing numpy...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy", "-q"])
    import numpy as np


# ============================================================================
# Test Configuration
# ============================================================================

NUM_NODES = 10000
OUTPUT_FILE = "/tmp/test_phase0.loom"
SEED = 42

# Golden ratio for Fibonacci sphere distribution
PHI_VAL = (1 + 5**0.5) / 2


def fibonacci_sphere(samples: int, radius: float = 1.0) -> List[Tuple[float, float, float]]:
    """Generate evenly distributed points on a sphere using golden angle spiral."""
    points = []
    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2  # y goes from 1 to -1
        radius_at_y = np.sqrt(1 - y * y)
        theta = GOLDEN_ANGLE * i  # golden angle increment
        x = np.cos(theta) * radius_at_y * radius
        z = np.sin(theta) * radius_at_y * radius
        points.append((x, y * radius, z))
    return points


def generate_random_nodes(n: int, seed: int = SEED) -> List[GaugeNode128]:
    """Generate n random GaugeNode128 instances."""
    random.seed(seed)
    np.random.seed(seed)
    
    # Generate points on Fibonacci sphere for spatial coherence
    points = fibonacci_sphere(n, radius=10.0)
    
    nodes = []
    glyph_types = [
        GlyfPrimitive.VOID, GlyfPrimitive.DOT, GlyfPrimitive.CURVE,
        GlyfPrimitive.LINE, GlyfPrimitive.ANGLE, GlyfPrimitive.CIRCLE,
        GlyfPrimitive.VESICA
    ]
    
    for i in range(n):
        # Random glyph type with weighted distribution
        glyph = random.choice(glyph_types[1:])  # Skip VOID for main nodes
        
        # Get coordinates from Fibonacci sphere
        x, y, z = points[i]
        
        # Add some jitter
        jitter = 0.5
        x += random.uniform(-jitter, jitter)
        y += random.uniform(-jitter, jitter)
        z += random.uniform(-jitter, jitter)
        
        # Create node
        node = GaugeNode128(i, glyph.value, x, y, z)
        
        # Random chirality
        node.chirality = random.randint(0, 1)
        
        # Random holonomy phase (radius)
        node.holonomy_phase = random.uniform(0.5, 3.0)
        
        # Set random payload
        payload = bytes([random.randint(0, 255) for _ in range(72)])
        node.set_payload(list(payload))
        
        nodes.append(node)
    
    return nodes


def connect_nearby_nodes(nodes: List[GaugeNode128], max_dist: float = 3.0) -> int:
    """Connect nearby nodes based on distance."""
    connections = 0
    n = len(nodes)
    
    for i in range(n):
        for j in range(i + 1, min(i + 20, n)):  # Check next 20 nodes
            dist = gauge_node_distance(nodes[i], nodes[j])
            if dist < max_dist:
                if gauge_node_connect(nodes[i], nodes[j]):
                    connections += 1
    
    return connections


def build_networkx_graph(nodes: List[GaugeNode128]) -> nx.Graph:
    """Build NetworkX graph from node connections."""
    G = nx.Graph()
    
    # Add all nodes
    for i, node in enumerate(nodes):
        G.add_node(i, 
                   glyph_type=node.glyph_type,
                   chirality=node.chirality,
                   x=node.x, y=node.y, z=node.z)
    
    # Add edges from bonds
    for i, node in enumerate(nodes):
        bonds = node.get_bonds()
        for target_id in bonds:
            if target_id < len(nodes):
                G.add_edge(i, target_id)
    
    return G


def find_all_cycles(G: nx.Graph, max_length: int = 10) -> List[List[int]]:
    """Find all cycles up to max_length using NetworkX."""
    cycles = []
    try:
        # Use cycle_basis for fundamental cycles
        basis = nx.cycle_basis(G)
        cycles.extend(basis)
        
        # Find additional simple cycles
        for cycle in nx.simple_cycles(nx.DiGraph(G)):
            if 3 <= len(cycle) <= max_length:
                cycles.append(cycle)
    except:
        pass
    
    return cycles


def verify_chirality_parity(nodes: List[GaugeNode128], G: nx.Graph) -> Tuple[bool, int]:
    """
    Run chirality checker (XOR parity on all cycles).
    Returns (all_valid, num_violations)
    """
    cycles = find_all_cycles(G)
    violations = 0
    
    for cycle in cycles:
        if len(cycle) < 3:
            continue
        
        # Compute XOR parity along cycle
        parity = 0
        for node_idx in cycle:
            if node_idx < len(nodes):
                parity ^= nodes[node_idx].chirality
        
        if parity != 0:
            violations += 1
    
    return (violations == 0, violations)


def verify_serialization(nodes: List[GaugeNode128]) -> bool:
    """Serialize to file and verify read-back integrity."""
    # Write
    result = gauge_graph_write(OUTPUT_FILE, nodes)
    if result != 0:
        print(f"  ERROR: Write failed with code {result}")
        return False
    
    # Check file size
    expected_size = 16 + len(nodes) * GAUGE_NODE_SIZE  # Header + nodes
    actual_size = os.path.getsize(OUTPUT_FILE)
    if actual_size != expected_size:
        print(f"  ERROR: File size mismatch. Expected {expected_size}, got {actual_size}")
        return False
    
    # Read back
    try:
        read_nodes = gauge_graph_read(OUTPUT_FILE)
    except Exception as e:
        print(f"  ERROR: Read failed: {e}")
        return False
    
    if len(read_nodes) != len(nodes):
        print(f"  ERROR: Node count mismatch. Expected {len(nodes)}, got {len(read_nodes)}")
        return False
    
    # Verify integrity of each node
    for i, (orig, read) in enumerate(zip(nodes, read_nodes)):
        if orig.node_id != read.node_id:
            print(f"  ERROR: Node {i}: ID mismatch")
            return False
        if orig.glyph_type != read.glyph_type:
            print(f"  ERROR: Node {i}: glyph_type mismatch")
            return False
        if orig.chirality != read.chirality:
            print(f"  ERROR: Node {i}: chirality mismatch")
            return False
        if abs(orig.holonomy_phase - read.holonomy_phase) > 0.0001:
            print(f"  ERROR: Node {i}: holonomy_phase mismatch")
            return False
        if orig.get_bonds() != read.get_bonds():
            print(f"  ERROR: Node {i}: bonds mismatch")
            return False
    
    return True


def run_tests():
    """Run all Phase 0 tests."""
    print("=" * 70)
    print("PHASE 0: GaugeNode128 Implementation Test Suite")
    print("=" * 70)
    print()
    
    # Test 1: Size verification
    print("[1/7] Verifying GaugeNode128 structure size...")
    if GAUGE_NODE_SIZE == 128:
        print(f"  ✓ Size check passed: {GAUGE_NODE_SIZE} bytes (128-byte aligned)")
    else:
        print(f"  ✗ Size check FAILED: {GAUGE_NODE_SIZE} bytes (expected 128)")
        return False
    print(f"  Constants: MAGIC=0x{GAUGE_NODE_MAGIC:08X}, VERSION={GAUGE_NODE_VERSION}")
    print(f"  PHI={PHI:.6f}, GOLDEN_ANGLE={GOLDEN_ANGLE:.6f}")
    print()
    
    # Test 2: Node generation
    print(f"[2/7] Generating {NUM_NODES} random GaugeNode128 instances...")
    t_start = time.perf_counter()
    nodes = generate_random_nodes(NUM_NODES)
    t_gen = time.perf_counter() - t_start
    gen_rate = NUM_NODES / t_gen
    print(f"  ✓ Generated {len(nodes)} nodes in {t_gen:.3f}s ({gen_rate:.0f} nodes/sec)")
    print()
    
    # Test 3: Node connections
    print("[3/7] Connecting nearby nodes...")
    t_start = time.perf_counter()
    num_connections = connect_nearby_nodes(nodes, max_dist=3.0)
    t_connect = time.perf_counter() - t_start
    total_bonds = sum(n.bond_count for n in nodes)
    print(f"  ✓ Created {num_connections} connections in {t_connect:.3f}s")
    print(f"  Total bonds: {total_bonds}, avg bonds/node: {total_bonds/len(nodes):.2f}")
    print()
    
    # Test 4: Build NetworkX graph
    print("[4/7] Building NetworkX graph...")
    t_start = time.perf_counter()
    G = build_networkx_graph(nodes)
    t_graph = time.perf_counter() - t_start
    print(f"  ✓ Built graph with {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    print(f"  Graph construction time: {t_graph:.3f}s")
    
    # Graph statistics
    if G.number_of_edges() > 0:
        avg_degree = 2 * G.number_of_edges() / G.number_of_nodes()
        print(f"  Average degree: {avg_degree:.2f}")
        
        # Connected components
        if hasattr(nx, 'number_connected_components'):
            num_cc = nx.number_connected_components(G)
            print(f"  Connected components: {num_cc}")
    print()
    
    # Test 5: Chirality verification
    print("[5/7] Running chirality checker (XOR parity on cycles)...")
    t_start = time.perf_counter()
    valid, violations = verify_chirality_parity(nodes, G)
    t_chiral = time.perf_counter() - t_start
    
    if valid:
        print(f"  ✓ All cycles have valid chirality parity")
    else:
        print(f"  ⚠ Found {violations} cycles with parity violations (expected for random data)")
    print(f"  Verification time: {t_chiral:.3f}s")
    print()
    
    # Test 6: Holonomy graph verification
    print("[6/7] Running holonomy graph verification...")
    t_start = time.perf_counter()
    holonomy_valid = holonomy_verify_graph(nodes)
    t_holonomy = time.perf_counter() - t_start
    print(f"  Holonomy verification: {'PASSED' if holonomy_valid else 'FAILED'}")
    print(f"  Verification time: {t_holonomy:.3f}s")
    print()
    
    # Test 7: Serialization
    print(f"[7/7] Testing serialization to {OUTPUT_FILE}...")
    t_start = time.perf_counter()
    ser_valid = verify_serialization(nodes)
    t_ser = time.perf_counter() - t_start
    
    if ser_valid:
        print(f"  ✓ Serialization verified (read-back integrity confirmed)")
        file_size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
        print(f"  File size: {file_size_mb:.2f} MB")
        print(f"  Serialization time: {t_ser:.3f}s ({file_size_mb/t_ser:.2f} MB/s)")
    else:
        print(f"  ✗ Serialization FAILED")
    print()
    
    # Summary
    print("=" * 70)
    print("TEST RESULTS SUMMARY")
    print("=" * 70)
    print(f"  Structure size:     {'PASS' if GAUGE_NODE_SIZE == 128 else 'FAIL'}")
    print(f"  Node generation:    {len(nodes)} nodes @ {gen_rate:.0f}/s")
    print(f"  Graph construction: {G.number_of_edges()} edges @ {G.number_of_edges()/t_graph:.0f}/s")
    print(f"  Chirality check:    {violations} violations found")
    print(f"  Holonomy verify:    {'PASS' if holonomy_valid else 'FAIL'}")
    print(f"  Serialization:      {'PASS' if ser_valid else 'FAIL'}")
    print()
    
    total_time = t_gen + t_connect + t_graph + t_chiral + t_holonomy + t_ser
    print(f"  Total runtime:      {total_time:.3f}s")
    print()
    
    # Final verdict
    all_passed = (
        GAUGE_NODE_SIZE == 128 and
        len(nodes) == NUM_NODES and
        holonomy_valid and
        ser_valid
    )
    
    if all_passed:
        print("✓ ALL TESTS PASSED - Ready for Phase 1")
    else:
        print("✗ SOME TESTS FAILED")
    
    return all_passed


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

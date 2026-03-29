#!/usr/bin/env python3
"""
Unit tests for graph_builder.py
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../phase0'))
sys.path.insert(0, os.path.dirname(__file__))

from graph_builder import (
    build_nodes, connect_sequential, connect_by_distance,
    build_faiss_index, search_neighbors,
    save_loom, load_loom, get_loom_file_size, estimate_loom_size,
    get_node_coordinates, get_node_vectors,
    benchmark_faiss_build, benchmark_serialization
)
from py_gauge import GlyfPrimitive

import faiss

def test_build_nodes():
    """Test node creation from tokens and coordinates."""
    tokens = [0, 1, 2, 3, 4, 5, 6]
    coords = np.random.randn(7, 3)
    
    nodes = build_nodes(tokens, coords)
    
    assert len(nodes) == 7
    for i, node in enumerate(nodes):
        assert node.node_id == i
        assert node.glyph_type == tokens[i]
        assert abs(node.x - coords[i][0]) < 1e-6
        assert abs(node.y - coords[i][1]) < 1e-6
        assert abs(node.z - coords[i][2]) < 1e-6
    
    print("✓ build_nodes passed")

def test_build_nodes_clamping():
    """Test that glyph types are clamped to valid range."""
    tokens = [-5, 10, 3]  # Out of range values
    coords = np.random.randn(3, 3)
    
    nodes = build_nodes(tokens, coords)
    
    assert nodes[0].glyph_type == 0  # Clamped to minimum
    assert nodes[1].glyph_type == 6  # Clamped to maximum
    assert nodes[2].glyph_type == 3  # Within range
    
    print("✓ build_nodes_clamping passed")

def test_connect_sequential():
    """Test bidirectional sequential bonding."""
    tokens = [1, 2, 3, 4]
    coords = np.random.randn(4, 3)
    nodes = build_nodes(tokens, coords)
    
    bonds = connect_sequential(nodes)
    
    assert bonds == 3  # 4 nodes = 3 bonds
    
    # Check bidirectional connections
    assert nodes[0].get_bonds() == [1]
    assert nodes[1].get_bonds() == [0, 2]
    assert nodes[2].get_bonds() == [1, 3]
    assert nodes[3].get_bonds() == [2]
    
    print("✓ connect_sequential passed")

def test_faiss_index():
    """Test FAISS index building and search."""
    np.random.seed(42)
    tokens = [1, 1, 1, 1, 1]
    coords = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [10.0, 10.0, 10.0],  # Far away
    ])
    
    nodes = build_nodes(tokens, coords)
    index = build_faiss_index(nodes)
    
    assert index.ntotal == 5
    
    # Search from origin
    D, I = search_neighbors(index, np.array([[0.0, 0.0, 0.0]]), k=3)
    
    assert len(I[0]) == 3
    assert I[0][0] == 0  # Closest should be node 0 (at origin)
    assert D[0][0] == 0.0  # Distance to self is 0
    
    print("✓ faiss_index passed")

def test_serialization():
    """Test .loom save/load roundtrip."""
    np.random.seed(42)
    tokens = [1, 2, 3, 4, 5]
    coords = np.random.randn(5, 3)
    
    nodes = build_nodes(tokens, coords)
    connect_sequential(nodes)
    
    filename = "/tmp/test_serialization.loom"
    
    # Save
    result = save_loom(nodes, filename)
    assert result == 0
    assert os.path.exists(filename)
    
    # Load
    loaded = load_loom(filename)
    assert len(loaded) == 5
    
    # Verify data
    for i, (orig, load) in enumerate(zip(nodes, loaded)):
        assert load.node_id == orig.node_id
        assert load.glyph_type == orig.glyph_type
        # Bonds should be preserved
        assert load.get_bonds() == orig.get_bonds()
    
    # Cleanup
    os.remove(filename)
    
    print("✓ serialization passed")

def test_file_size_estimation():
    """Test file size estimation accuracy."""
    np.random.seed(42)
    
    for num_nodes in [10, 100, 500]:
        tokens = list(range(num_nodes))
        coords = np.random.randn(num_nodes, 3)
        nodes = build_nodes(tokens, coords)
        
        filename = f"/tmp/test_size_{num_nodes}.loom"
        save_loom(nodes, filename)
        
        actual_size = get_loom_file_size(filename)
        estimated_size = estimate_loom_size(num_nodes)
        
        # Allow small margin for padding
        assert abs(actual_size - estimated_size) <= 4
        
        os.remove(filename)
    
    print("✓ file_size_estimation passed")

def test_connect_by_distance():
    """Test distance-based connectivity."""
    tokens = [1, 1, 1, 1]
    coords = np.array([
        [0.0, 0.0, 0.0],
        [0.5, 0.0, 0.0],  # Distance 0.5 from node 0
        [2.0, 0.0, 0.0],  # Distance 2.0 from node 0
        [2.5, 0.0, 0.0],  # Distance 0.5 from node 2
    ])
    
    nodes = build_nodes(tokens, coords)
    bonds = connect_by_distance(nodes, max_distance=1.0)
    
    # Should connect: 0-1 and 2-3
    assert bonds == 2
    assert nodes[0].get_bonds() == [1]
    assert nodes[1].get_bonds() == [0]
    assert nodes[2].get_bonds() == [3]
    assert nodes[3].get_bonds() == [2]
    
    print("✓ connect_by_distance passed")

def test_node_coordinate_helpers():
    """Test coordinate extraction helpers."""
    tokens = [1, 2]
    coords = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    nodes = build_nodes(tokens, coords)
    
    # Test single node
    c = get_node_coordinates(nodes[0])
    assert np.allclose(c, [1.0, 2.0, 3.0])
    
    # Test all nodes
    vectors = get_node_vectors(nodes)
    assert vectors.shape == (2, 3)
    assert np.allclose(vectors, coords)
    
    print("✓ node_coordinate_helpers passed")

def test_benchmark_functions():
    """Test that benchmark functions run without error."""
    result = benchmark_faiss_build(100)
    assert "faiss_build_time_ms" in result
    
    result = benchmark_serialization(100)
    assert "file_size_bytes" in result
    assert result["load_verified"] is True
    
    print("✓ benchmark_functions passed")

def run_all_tests():
    """Run all unit tests."""
    print("=" * 50)
    print("Running graph_builder unit tests")
    print("=" * 50)
    
    test_build_nodes()
    test_build_nodes_clamping()
    test_connect_sequential()
    test_faiss_index()
    test_serialization()
    test_file_size_estimation()
    test_connect_by_distance()
    test_node_coordinate_helpers()
    test_benchmark_functions()
    
    print("=" * 50)
    print("All tests passed!")
    print("=" * 50)

if __name__ == "__main__":
    run_all_tests()

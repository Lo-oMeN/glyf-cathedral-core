#!/usr/bin/env python3
"""
PHASE 1C: Graph Builder + FAISS Integration
Pragmatic Geometric AI - Graph Construction Layer

Builds GaugeNode128 graphs with FAISS vector indexing for semantic search.
"""

import sys
import os
import numpy as np
from typing import List, Tuple, Optional
import time

# Add phase0 to path for py_gauge
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../phase0'))

from py_gauge import (
    GaugeNode128, 
    GlyfPrimitive, 
    gauge_node_connect,
    gauge_graph_write,
    gauge_graph_read
)

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("Warning: faiss-cpu not installed. Vector search disabled.")


# ============================================================================
# Node Construction
# ============================================================================

def build_nodes(tokens: List[int], coords: np.ndarray) -> List[GaugeNode128]:
    """
    Create GaugeNode128 instances from tokens and coordinates.
    
    Args:
        tokens: List of glyph type indices (0-6 for GlyfPrimitive)
        coords: Nx3 array of spatial coordinates
        
    Returns:
        List of initialized GaugeNode128 instances
        
    Raises:
        ValueError: If tokens and coords length mismatch
    """
    if len(tokens) != len(coords):
        raise ValueError(f"Token count ({len(tokens)}) != coordinate count ({len(coords)})")
    
    if coords.shape[1] != 3:
        raise ValueError(f"Coordinates must be Nx3, got {coords.shape}")
    
    nodes = []
    for i, (t, coord) in enumerate(zip(tokens, coords)):
        # Clamp glyph type to valid range (0-6)
        glyph_type = max(0, min(6, int(t)))
        
        node = GaugeNode128()
        node.init(i, glyph_type, float(coord[0]), float(coord[1]), float(coord[2]))
        nodes.append(node)
    
    return nodes


def get_node_coordinates(node: GaugeNode128) -> np.ndarray:
    """Extract coordinates from a GaugeNode128 as numpy array."""
    return np.array([node.x, node.y, node.z], dtype=np.float32)


def get_node_vectors(nodes: List[GaugeNode128]) -> np.ndarray:
    """Extract coordinates from all nodes as Nx3 numpy array."""
    return np.array([get_node_coordinates(n) for n in nodes], dtype=np.float32)


# ============================================================================
# Graph Connectivity
# ============================================================================

def connect_sequential(nodes: List[GaugeNode128]) -> int:
    """
    Create bidirectional bonds between sequential nodes (i <-> i+1).
    
    Args:
        nodes: List of GaugeNode128 instances
        
    Returns:
        Number of bonds created
    """
    bonds_created = 0
    
    for i in range(len(nodes) - 1):
        # Use the gauge_node_connect function from py_gauge
        # This creates a bidirectional bond automatically
        success = gauge_node_connect(nodes[i], nodes[i + 1])
        if success:
            bonds_created += 1
    
    return bonds_created


def connect_by_distance(nodes: List[GaugeNode128], max_distance: float) -> int:
    """
    Connect nodes within max_distance of each other.
    
    Args:
        nodes: List of GaugeNode128 instances
        max_distance: Maximum distance for connection
        
    Returns:
        Number of bonds created
    """
    bonds_created = 0
    
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            coord_i = get_node_coordinates(nodes[i])
            coord_j = get_node_coordinates(nodes[j])
            distance = np.linalg.norm(coord_i - coord_j)
            
            if distance <= max_distance:
                success = gauge_node_connect(nodes[i], nodes[j])
                if success:
                    bonds_created += 1
    
    return bonds_created


# ============================================================================
# FAISS Vector Index
# ============================================================================

def build_faiss_index(nodes: List[GaugeNode128]) -> Optional["faiss.Index"]:
    """
    Build a searchable FAISS index from node coordinates.
    
    Args:
        nodes: List of GaugeNode128 instances
        
    Returns:
        FAISS IndexFlatL2 instance or None if faiss not available
    """
    if not FAISS_AVAILABLE:
        raise RuntimeError("FAISS not available. Install with: pip install faiss-cpu")
    
    if not nodes:
        raise ValueError("Cannot build index from empty node list")
    
    # Extract coordinates from all nodes
    vectors = get_node_vectors(nodes)
    
    # Create L2 distance index (exact search, not approximate)
    # IndexFlatL2 is the simplest exact search index
    dimension = 3  # 3D coordinates
    index = faiss.IndexFlatL2(dimension)
    
    # Add vectors to index
    index.add(vectors)
    
    return index


def search_neighbors(
    index: "faiss.Index", 
    query_point: np.ndarray, 
    k: int = 5
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Search for k nearest neighbors to query point.
    
    Args:
        index: FAISS index
        query_point: 3D coordinate or Nx3 array
        k: Number of neighbors to return
        
    Returns:
        (distances, indices) arrays where indices are node IDs
    """
    if not FAISS_AVAILABLE:
        raise RuntimeError("FAISS not available")
    
    # Ensure query is 2D array (n_queries x dimension)
    if query_point.ndim == 1:
        query_point = query_point.reshape(1, -1)
    
    # Search
    distances, indices = index.search(query_point.astype(np.float32), k)
    
    return distances, indices


# ============================================================================
# Serialization (.loom format)
# ============================================================================

LOOM_MAGIC = 0x474C5946  # "GLYF" in ASCII as uint32
LOOM_VERSION = 1

def save_loom(nodes: List[GaugeNode128], filename: str) -> int:
    """
    Serialize graph to binary .loom format.
    
    Args:
        nodes: List of GaugeNode128 instances
        filename: Output file path (.loom extension recommended)
        
    Returns:
        0 on success, -1 on failure
    """
    if not nodes:
        raise ValueError("Cannot save empty graph")
    
    # Ensure .loom extension
    if not filename.endswith('.loom'):
        filename += '.loom'
    
    # Use the C-level serialization from py_gauge
    return gauge_graph_write(filename, nodes)


def load_loom(filename: str) -> List[GaugeNode128]:
    """
    Load graph from binary .loom format.
    
    Args:
        filename: Input file path
        
    Returns:
        List of GaugeNode128 instances
    """
    return gauge_graph_read(filename)


def get_loom_file_size(filename: str) -> int:
    """Get size of .loom file in bytes."""
    return os.path.getsize(filename)


def estimate_loom_size(num_nodes: int) -> int:
    """
    Estimate the file size for a given number of nodes.
    Each node is exactly 128 bytes (cache-line aligned).
    
    Args:
        num_nodes: Number of nodes in graph
        
    Returns:
        Estimated file size in bytes
    """
    # Header: magic (4) + version (4) + count (4) = 12 bytes
    # Nodes: 128 bytes each
    return 12 + (num_nodes * 128)


# ============================================================================
# Benchmark / Testing
# ============================================================================

def benchmark_faiss_build(num_nodes: int = 1000, seed: int = 42) -> dict:
    """
    Benchmark FAISS index building for a given number of nodes.
    
    Args:
        num_nodes: Number of nodes to generate
        seed: Random seed for reproducibility
        
    Returns:
        Dictionary with benchmark results
    """
    if not FAISS_AVAILABLE:
        return {"error": "FAISS not available"}
    
    np.random.seed(seed)
    
    # Generate random tokens and coordinates
    tokens = np.random.randint(0, 7, size=num_nodes)
    coords = np.random.randn(num_nodes, 3).astype(np.float32)
    
    # Build nodes
    nodes = build_nodes(tokens.tolist(), coords)
    
    # Benchmark FAISS index build
    start_time = time.perf_counter()
    index = build_faiss_index(nodes)
    build_time = time.perf_counter() - start_time
    
    # Test search
    query = np.array([[1.0, 0.0, 0.0]], dtype=np.float32)
    start_time = time.perf_counter()
    D, I = search_neighbors(index, query, k=min(3, num_nodes))
    search_time = time.perf_counter() - start_time
    
    return {
        "num_nodes": num_nodes,
        "faiss_build_time_ms": round(build_time * 1000, 3),
        "faiss_search_time_ms": round(search_time * 1000, 3),
        "index_is_trained": index.is_trained,
        "index_ntotal": index.ntotal,
    }


def benchmark_serialization(num_nodes: int = 1000, seed: int = 42) -> dict:
    """
    Benchmark serialization performance and file size.
    
    Args:
        num_nodes: Number of nodes to generate
        seed: Random seed for reproducibility
        
    Returns:
        Dictionary with benchmark results
    """
    np.random.seed(seed)
    
    # Generate random tokens and coordinates
    tokens = np.random.randint(0, 7, size=num_nodes)
    coords = np.random.randn(num_nodes, 3).astype(np.float32)
    
    # Build and connect nodes
    nodes = build_nodes(tokens.tolist(), coords)
    connect_sequential(nodes)
    
    # Benchmark save
    filename = f"/tmp/benchmark_{num_nodes}.loom"
    start_time = time.perf_counter()
    result = save_loom(nodes, filename)
    save_time = time.perf_counter() - start_time
    
    file_size = get_loom_file_size(filename)
    estimated_size = estimate_loom_size(num_nodes)
    
    # Benchmark load
    start_time = time.perf_counter()
    loaded_nodes = load_loom(filename)
    load_time = time.perf_counter() - start_time
    
    # Cleanup
    os.remove(filename)
    
    return {
        "num_nodes": num_nodes,
        "save_time_ms": round(save_time * 1000, 3),
        "load_time_ms": round(load_time * 1000, 3),
        "file_size_bytes": file_size,
        "estimated_size_bytes": estimated_size,
        "size_per_node_bytes": file_size / num_nodes,
        "load_verified": len(loaded_nodes) == num_nodes,
    }


# ============================================================================
# Main / Test
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("PHASE 1C: Graph Builder + FAISS Integration")
    print("=" * 60)
    
    # Basic test from specification
    print("\n[TEST] Basic node creation and FAISS indexing...")
    
    np.random.seed(42)
    nodes = build_nodes([4, 2, 0, 4, 2], np.random.randn(5, 3))
    
    print(f"  Created {len(nodes)} nodes")
    for n in nodes:
        print(f"    Node {n.node_id}: glyph={n.glyph_type}, pos=({n.x:.3f}, {n.y:.3f}, {n.z:.3f})")
    
    # Connect sequential nodes
    bonds = connect_sequential(nodes)
    print(f"  Created {bonds} sequential bonds")
    
    # Check bonds
    for n in nodes:
        if n.get_bonds():
            print(f"    Node {n.node_id} bonds: {n.get_bonds()}")
    
    # Build FAISS index
    if FAISS_AVAILABLE:
        index = build_faiss_index(nodes)
        print(f"  FAISS index built: ntotal={index.ntotal}, trained={index.is_trained}")
        
        # Query nearest neighbors
        D, I = search_neighbors(index, np.array([[1.0, 0.0, 0.0]]), k=3)
        print(f"  Query [1.0, 0.0, 0.0] nearest 3 neighbors:")
        print(f"    Indices: {I[0]}")
        print(f"    Distances: {D[0]}")
        
        assert len(I[0]) == 3, "Expected 3 neighbors"
        print("  ✓ FAISS test passed")
    
    # Test serialization
    print("\n[TEST] Serialization to .loom format...")
    filename = "/tmp/test_graph.loom"
    result = save_loom(nodes, filename)
    file_size = get_loom_file_size(filename)
    print(f"  Saved to {filename}: {file_size} bytes")
    
    loaded = load_loom(filename)
    print(f"  Loaded {len(loaded)} nodes")
    assert len(loaded) == len(nodes), "Node count mismatch"
    print("  ✓ Serialization test passed")
    
    os.remove(filename)
    
    # Benchmarks
    print("\n" + "=" * 60)
    print("BENCHMARKS")
    print("=" * 60)
    
    if FAISS_AVAILABLE:
        print("\n[FAISS] 1000 nodes:")
        result = benchmark_faiss_build(1000)
        for k, v in result.items():
            print(f"  {k}: {v}")
    
    print("\n[Serialization] 1000 nodes:")
    result = benchmark_serialization(1000)
    for k, v in result.items():
        print(f"  {k}: {v}")
    
    print("\n" + "=" * 60)
    print("PHASE 1C: All tests passed!")
    print("=" * 60)

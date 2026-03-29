"""
graph_builder.py - FAISS-based knowledge graph construction

Creates GaugeNode128 structures from tokens and coordinates,
builds FAISS index for similarity search, and serializes to .loom format.
"""
import numpy as np
import struct
from typing import List, Tuple, Optional, BinaryIO
from dataclasses import dataclass
from enum import IntEnum

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    # Mock faiss for testing
    class MockIndex:
        def __init__(self, dim):
            self.dim = dim
            self.vectors = []
        def add(self, x):
            self.vectors.append(x)
        def search(self, x, k):
            return None, None
    class MockFaiss:
        IndexFlatL2 = lambda self, dim: MockIndex(dim)
        IndexIVFFlat = lambda self, *args: MockIndex(args[0])
    faiss = MockFaiss()

class GlyfPrimitive(IntEnum):
    """Geometric primitive types."""
    GLYPH_VOID = 0
    GLYPH_DOT = 1
    GLYPH_CURVE = 2
    GLYPH_LINE = 3
    GLYPH_ANGLE = 4
    GLYPH_SIBILANT = 5
    GLYPH_RESERVED = 6

MAX_BONDS = 8  # Maximum bonds per node
NODE_SIZE_BYTES = 128  # Fixed-size node structure

@dataclass
class GaugeNode128:
    """
    128-byte fixed-size node structure for geometric knowledge graph.
    
    Layout:
    - node_id (4 bytes): uint32
    - glyph_type (1 byte): uint8 (0-6)
    - chirality (1 byte): uint8 (0-1)
    - bond_count (1 byte): uint8 (0-8)
    - reserved (1 byte): padding
    - coordinates (12 bytes): 3 x float32 (x, y, z)
    - bonds (32 bytes): 8 x uint32 (connected node IDs)
    - bond_weights (32 bytes): 8 x float32 (connection strengths)
    - metadata (16 bytes): user-defined data
    - vector (32 bytes): 8 x float32 (embedding slice for FAISS)
    """
    node_id: int
    glyph_type: int
    chirality: int
    coordinates: np.ndarray  # shape (3,), float32
    bonds: List[int] = None  # List of connected node IDs
    bond_weights: List[float] = None
    metadata: bytes = None   # 16 bytes
    vector: np.ndarray = None  # shape (8,), float32 - for FAISS
    
    def __post_init__(self):
        if self.bonds is None:
            self.bonds = []
        if self.bond_weights is None:
            self.bond_weights = [1.0] * len(self.bonds)
        if self.metadata is None:
            self.metadata = bytes(16)
        if self.vector is None:
            self.vector = np.zeros(8, dtype=np.float32)
    
    @property
    def bond_count(self) -> int:
        return len(self.bonds)
    
    def to_bytes(self) -> bytes:
        """Serialize to 128-byte binary structure."""
        # Pack bonds (pad to MAX_BONDS)
        bonds_padded = (self.bonds + [0] * MAX_BONDS)[:MAX_BONDS]
        weights_padded = (self.bond_weights + [0.0] * MAX_BONDS)[:MAX_BONDS]
        
        # Ensure vector is right size
        vector_padded = np.zeros(8, dtype=np.float32)
        if self.vector is not None:
            vector_padded[:min(len(self.vector), 8)] = self.vector[:8]
        
        # Pack structure
        data = struct.pack(
            '<I B B B B 3f 8I 8f 16s 8f',
            self.node_id,
            self.glyph_type,
            self.chirality,
            self.bond_count,
            0,  # reserved
            self.coordinates[0],
            self.coordinates[1],
            self.coordinates[2],
            *bonds_padded,
            *weights_padded,
            self.metadata[:16].ljust(16, b'\x00'),
            *vector_padded
        )
        
        return data
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'GaugeNode128':
        """Deserialize from 128-byte binary structure."""
        if len(data) != NODE_SIZE_BYTES:
            raise ValueError(f"Expected {NODE_SIZE_BYTES} bytes, got {len(data)}")
        
        unpacked = struct.unpack('<I B B B B 3f 8I 8f 16s 8f', data)
        
        node_id = unpacked[0]
        glyph_type = unpacked[1]
        chirality = unpacked[2]
        bond_count = unpacked[3]
        coords = np.array(unpacked[5:8], dtype=np.float32)
        bonds = list(unpacked[8:16])
        weights = list(unpacked[16:24])
        metadata = unpacked[24]
        vector = np.array(unpacked[25:33], dtype=np.float32)
        
        # Trim bonds to actual count
        bonds = bonds[:bond_count]
        weights = weights[:bond_count]
        
        return cls(
            node_id=node_id,
            glyph_type=glyph_type,
            chirality=chirality,
            coordinates=coords,
            bonds=bonds,
            bond_weights=weights,
            metadata=metadata,
            vector=vector
        )

def build_nodes(
    tokens: List[int],
    chirality: List[int],
    coordinates: np.ndarray,
    generate_vectors: bool = True
) -> List[GaugeNode128]:
    """
    Build GaugeNode128 list from token sequence and coordinates.
    
    Args:
        tokens: List of glyph type integers (0-6)
        chirality: List of chirality bits (0-1) per token
        coordinates: Nx3 array of 3D coordinates
        generate_vectors: Whether to populate FAISS vector field
        
    Returns:
        List of GaugeNode128 nodes
    """
    nodes = []
    n = len(tokens)
    
    for i in range(n):
        # Create node
        node = GaugeNode128(
            node_id=i,
            glyph_type=tokens[i],
            chirality=chirality[i] if i < len(chirality) else 0,
            coordinates=coordinates[i],
        )
        
        # Generate 8D vector from coordinates + glyph info
        if generate_vectors:
            vec = np.zeros(8, dtype=np.float32)
            vec[0:3] = coordinates[i]  # xyz
            vec[3] = float(tokens[i]) / 6.0  # normalized glyph type
            vec[4] = float(chirality[i]) if i < len(chirality) else 0.0
            # Add small hash of position for distinctiveness
            vec[5] = np.sin(i * 0.1)
            vec[6] = np.cos(i * 0.1)
            vec[7] = float(i) / max(n, 1)
            node.vector = vec
        
        nodes.append(node)
    
    # Second pass: connect sequential tokens
    for i in range(n - 1):
        nodes[i].bonds.append(i + 1)
        nodes[i].bond_weights.append(1.0)
        
        # Add reverse bond for bidirectional graph
        nodes[i + 1].bonds.append(i)
        nodes[i + 1].bond_weights.append(1.0)
    
    return nodes

def build_faiss_index(nodes: List[GaugeNode128], use_ivf: bool = False) -> Optional:
    """
    Build FAISS index from node vectors.
    
    Args:
        nodes: List of GaugeNode128 nodes
        use_ivf: Use IVF index for large datasets (1000+ nodes)
        
    Returns:
        FAISS index object or None if faiss unavailable
    """
    if not nodes:
        return None
    
    if not FAISS_AVAILABLE:
        print("Warning: FAISS not available, returning mock index")
        return faiss.IndexFlatL2(8)
    
    # Extract vectors
    vectors = np.array([node.vector for node in nodes], dtype=np.float32)
    dim = vectors.shape[1]
    
    if use_ivf and len(nodes) > 1000:
        # Use IVF for large datasets
        quantizer = faiss.IndexFlatL2(dim)
        nlist = min(int(np.sqrt(len(nodes))), 256)
        index = faiss.IndexIVFFlat(quantizer, dim, nlist)
        index.train(vectors)
    else:
        # Use flat index for small datasets
        index = faiss.IndexFlatL2(dim)
    
    index.add(vectors)
    
    return index

def search_similar(index, query_vector: np.ndarray, k: int = 5) -> Tuple[np.ndarray, np.ndarray]:
    """
    Search for similar nodes in FAISS index.
    
    Args:
        index: FAISS index
        query_vector: 8D query vector
        k: Number of neighbors
        
    Returns:
        (distances, indices) arrays
    """
    if index is None:
        return np.array([]), np.array([])
    
    query = query_vector.reshape(1, -1).astype(np.float32)
    distances, indices = index.search(query, k)
    
    return distances[0], indices[0]

def serialize_to_loom(nodes: List[GaugeNode128], filepath: str):
    """
    Serialize nodes to .loom file format.
    
    Format:
    - Header (64 bytes):
      - Magic: "LOOM" (4 bytes)
      - Version: uint32
      - Node count: uint32
      - Node size: uint32
      - Reserved: 52 bytes
    - Node data: node_count * 128 bytes
    
    Args:
        nodes: List of GaugeNode128 nodes
        filepath: Output file path
    """
    with open(filepath, 'wb') as f:
        # Write header
        header = struct.pack(
            '<4s I I I 52s',
            b'LOOM',
            1,  # version
            len(nodes),
            NODE_SIZE_BYTES,
            b'\x00' * 52
        )
        f.write(header)
        
        # Write nodes
        for node in nodes:
            f.write(node.to_bytes())

def deserialize_from_loom(filepath: str) -> List[GaugeNode128]:
    """
    Deserialize nodes from .loom file.
    
    Args:
        filepath: Path to .loom file
        
    Returns:
        List of GaugeNode128 nodes
    """
    nodes = []
    
    with open(filepath, 'rb') as f:
        # Read header
        header_data = f.read(64)
        magic, version, node_count, node_size, _ = struct.unpack('<4s I I I 52s', header_data)
        
        if magic != b'LOOM':
            raise ValueError(f"Invalid .loom file: wrong magic bytes {magic}")
        
        if node_size != NODE_SIZE_BYTES:
            raise ValueError(f"Node size mismatch: expected {NODE_SIZE_BYTES}, got {node_size}")
        
        # Read nodes
        for _ in range(node_count):
            node_data = f.read(NODE_SIZE_BYTES)
            node = GaugeNode128.from_bytes(node_data)
            nodes.append(node)
    
    return nodes


def get_graph_stats(nodes: List[GaugeNode128]) -> dict:
    """
    Compute statistics about the knowledge graph.
    
    Args:
        nodes: List of GaugeNode128 nodes
        
    Returns:
        Dictionary with graph statistics
    """
    if not nodes:
        return {"node_count": 0, "edge_count": 0}
    
    edge_count = sum(len(node.bonds) for node in nodes) // 2  # Divide by 2 for undirected
    
    glyph_counts = {}
    for node in nodes:
        glyph_counts[node.glyph_type] = glyph_counts.get(node.glyph_type, 0) + 1
    
    return {
        "node_count": len(nodes),
        "edge_count": edge_count,
        "avg_degree": sum(len(node.bonds) for node in nodes) / len(nodes),
        "glyph_distribution": glyph_counts
    }


if __name__ == "__main__":
    # Test node creation
    coords = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.5, 1.0, 0.0],
    ], dtype=np.float32)
    
    tokens = [4, 2, 3]  # ANGLE, CURVE, LINE
    chirality = [1, 0, 0]  # T, h, e
    
    print("Building nodes...")
    nodes = build_nodes(tokens, chirality, coords)
    
    for node in nodes:
        print(f"Node {node.node_id}: glyph={node.glyph_type}, bonds={node.bonds}")
    
    print(f"\nGraph stats: {get_graph_stats(nodes)}")
    
    # Test serialization
    print("\nTesting .loom serialization...")
    test_path = "/tmp/test.loom"
    serialize_to_loom(nodes, test_path)
    loaded = deserialize_from_loom(test_path)
    
    print(f"Original count: {len(nodes)}, Loaded count: {len(loaded)}")
    print(f"Match: {all(n1.to_bytes() == n2.to_bytes() for n1, n2 in zip(nodes, loaded))}")
    
    # Test FAISS index
    if FAISS_AVAILABLE:
        print("\nTesting FAISS index...")
        index = build_faiss_index(nodes)
        print(f"Index size: {index.ntotal}")
        
        # Search for similar nodes
        query = nodes[0].vector
        distances, indices = search_similar(index, query, k=2)
        print(f"Query node 0, nearest neighbors: {indices}, distances: {distances}")

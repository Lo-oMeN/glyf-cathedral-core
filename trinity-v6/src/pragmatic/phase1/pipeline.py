"""
pipeline.py - End-to-end text-to-graph pipeline

Integrates tokenizer, SVD embedding, and graph builder to transform
text into searchable geometric knowledge graphs.
"""
import numpy as np
from typing import List, Tuple, Optional
import os
import time

# Import local modules
from glyph_tokenizer import (
    glyph_tokenize, 
    tokenize_to_integers, 
    Token,
    GlyfPrimitive
)
from embedding_svd import (
    compute_embeddings,
    embed_sequence,
    get_default_embeddings,
    save_embeddings,
    load_embeddings,
    VOCAB_SIZE
)
from graph_builder import (
    GaugeNode128,
    build_nodes,
    build_faiss_index,
    serialize_to_loom,
    deserialize_from_loom,
    search_similar,
    get_graph_stats,
    NODE_SIZE_BYTES
)

# Default cache paths
DEFAULT_EMBEDDING_CACHE = os.path.expanduser("~/.trinity/phase1_embeddings.npy")
DEFAULT_LOOM_PATH = "output.loom"

def ensure_cache_dir():
    """Ensure cache directory exists."""
    cache_dir = os.path.dirname(DEFAULT_EMBEDDING_CACHE)
    if cache_dir and not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)

def text_to_graph(
    text: str,
    embeddings: Optional[np.ndarray] = None,
    use_default_embeddings: bool = False,
    build_index: bool = True
) -> Tuple[List[GaugeNode128], Optional[any]]:
    """
    Convert text to geometric knowledge graph.
    
    Pipeline:
    1. Tokenize text → glyph primitives
    2. Map tokens to 3D coordinates via embeddings
    3. Build GaugeNode128 nodes with bonds
    4. Create FAISS index for similarity search
    
    Args:
        text: Input text (UTF-8)
        embeddings: Pre-computed Vx3 embedding array, or None to use defaults
        use_default_embeddings: Force use of default geometric embeddings
        build_index: Whether to build FAISS index
        
    Returns:
        (nodes, index): List of GaugeNode128 nodes and FAISS index
    """
    # Step 1: Tokenize
    tokens_obj = glyph_tokenize(text)
    tokens = [t.glyph_type for t in tokens_obj]
    chirality = [t.chirality for t in tokens_obj]
    
    # Step 2: Get embeddings
    if use_default_embeddings or embeddings is None:
        embeddings = get_default_embeddings()
    
    # Step 3: Map tokens to coordinates
    coordinates = embed_sequence(tokens, embeddings)
    
    # Step 4: Build nodes
    nodes = build_nodes(tokens, chirality, coordinates)
    
    # Step 5: Build FAISS index
    index = None
    if build_index:
        index = build_faiss_index(nodes)
    
    return nodes, index

def text_to_loom(
    text: str,
    output_path: str = DEFAULT_LOOM_PATH,
    embeddings: Optional[np.ndarray] = None
) -> str:
    """
    Convert text directly to .loom file.
    
    Args:
        text: Input text
        output_path: Output .loom file path
        embeddings: Optional pre-computed embeddings
        
    Returns:
        Path to created .loom file
    """
    nodes, _ = text_to_graph(text, embeddings, build_index=False)
    serialize_to_loom(nodes, output_path)
    return output_path

def batch_text_to_graph(
    texts: List[str],
    embeddings: Optional[np.ndarray] = None,
    use_corpus_embeddings: bool = False
) -> Tuple[List[GaugeNode128], Optional[any], List[Tuple[int, int]]]:
    """
    Process multiple texts into a single combined graph.
    
    Args:
        texts: List of input texts
        embeddings: Pre-computed embeddings
        use_corpus_embeddings: Compute embeddings from corpus
        
    Returns:
        (nodes, index, text_ranges): Combined graph with text boundaries
    """
    if use_corpus_embeddings:
        # Compute embeddings from corpus
        all_token_sequences = [tokenize_to_integers(t) for t in texts]
        embeddings = compute_embeddings(all_token_sequences, window_size=5)
    elif embeddings is None:
        embeddings = get_default_embeddings()
    
    all_nodes = []
    text_ranges = []
    offset = 0
    
    for text in texts:
        nodes, _ = text_to_graph(text, embeddings, build_index=False)
        
        # Adjust node IDs and bonds for combined graph
        for i, node in enumerate(nodes):
            node.node_id = offset + i
            node.bonds = [offset + b if b < len(nodes) else b for b in node.bonds]
        
        text_ranges.append((offset, offset + len(nodes)))
        all_nodes.extend(nodes)
        offset += len(nodes)
    
    # Build combined index
    index = build_faiss_index(all_nodes)
    
    return all_nodes, index, text_ranges

def search_text_nodes(
    index,
    query_text: str,
    embeddings: np.ndarray,
    k: int = 5
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Search for nodes similar to a query text.
    
    Args:
        index: FAISS index
        query_text: Text to search for
        embeddings: Glyph embeddings
        k: Number of results
        
    Returns:
        (distances, indices) from FAISS search
    """
    # Get query vector from first token
    query_tokens = tokenize_to_integers(query_text)
    if not query_tokens:
        return np.array([]), np.array([])
    
    query_coords = embed_sequence([query_tokens[0]], embeddings)
    
    # Build 8D query vector (same as graph_builder)
    vec = np.zeros(8, dtype=np.float32)
    vec[0:3] = query_coords[0]
    vec[3] = float(query_tokens[0]) / 6.0
    vec[4] = 0.0
    vec[5:8] = [0.0, 1.0, 0.0]  # Default position indicators
    
    return search_similar(index, vec, k)

def get_pipeline_info() -> dict:
    """Get information about the pipeline configuration."""
    return {
        "vocab_size": VOCAB_SIZE,
        "node_size_bytes": NODE_SIZE_BYTES,
        "embedding_dimensions": 3,
        "faiss_vector_dimensions": 8,
        "max_bonds_per_node": 8,
        "glyph_types": [g.name for g in GlyfPrimitive]
    }

class TextGraphPipeline:
    """
    Stateful pipeline for repeated text-to-graph conversions.
    
    Maintains cached embeddings and index for efficiency.
    """
    
    def __init__(self, embeddings: Optional[np.ndarray] = None):
        """
        Initialize pipeline with optional pre-computed embeddings.
        
        Args:
            embeddings: Vx3 embedding array or None for defaults
        """
        self.embeddings = embeddings or get_default_embeddings()
        self.corpus_embeddings = None
        self.index = None
        self.nodes = []
        
    def load_corpus_embeddings(self, filepath: str = DEFAULT_EMBEDDING_CACHE):
        """Load embeddings from cache file."""
        cached = load_embeddings(filepath)
        if cached is not None:
            self.corpus_embeddings = cached
            return True
        return False
    
    def save_corpus_embeddings(self, filepath: str = DEFAULT_EMBEDDING_CACHE):
        """Save current embeddings to cache."""
        ensure_cache_dir()
        save_embeddings(self.embeddings, filepath)
    
    def train_on_corpus(self, texts: List[str], window_size: int = 5):
        """
        Compute SVD embeddings from text corpus.
        
        Args:
            texts: Training corpus
            window_size: Co-occurrence window size
        """
        token_sequences = [tokenize_to_integers(t) for t in texts]
        self.corpus_embeddings = compute_embeddings(token_sequences, window_size)
        self.embeddings = self.corpus_embeddings
    
    def process(self, text: str, build_index: bool = True) -> Tuple[List[GaugeNode128], Optional[any]]:
        """
        Process text through pipeline.
        
        Args:
            text: Input text
            build_index: Whether to build FAISS index
            
        Returns:
            (nodes, index)
        """
        return text_to_graph(text, self.embeddings, build_index=build_index)
    
    def search(self, query: str, k: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """
        Search current index for query.
        
        Args:
            query: Query text
            k: Number of results
            
        Returns:
            (distances, indices)
        """
        if self.index is None:
            raise ValueError("No index available. Process text first.")
        return search_text_nodes(self.index, query, self.embeddings, k)


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 1: Geometric Tokenizer Pipeline")
    print("=" * 60)
    
    # Pipeline info
    info = get_pipeline_info()
    print(f"\nPipeline Configuration:")
    for k, v in info.items():
        print(f"  {k}: {v}")
    
    # Test single text processing
    test_text = "The quick brown fox jumps over the lazy dog"
    print(f"\n{'='*60}")
    print(f"Test: {test_text!r}")
    print(f"{'='*60}")
    
    start = time.time()
    nodes, index = text_to_graph(test_text)
    elapsed = time.time() - start
    
    print(f"\nTokenization + Graph Build: {elapsed*1000:.2f}ms")
    print(f"Nodes created: {len(nodes)}")
    print(f"FAISS index size: {index.ntotal if index else 0}")
    
    # Show first few nodes
    print(f"\nFirst 5 nodes:")
    for node in nodes[:5]:
        glyph_name = GlyfPrimitive(node.glyph_type).name
        print(f"  Node {node.node_id:2d}: {glyph_name:12s} @ [{node.coordinates[0]:6.3f}, {node.coordinates[1]:6.3f}, {node.coordinates[2]:6.3f}]")
    
    # Graph stats
    stats = get_graph_stats(nodes)
    print(f"\nGraph Statistics:")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    
    # Test .loom serialization
    print(f"\n{'='*60}")
    print("Testing .loom serialization")
    print(f"{'='*60}")
    
    loom_path = "/tmp/test_output.loom"
    text_to_loom(test_text, loom_path)
    
    file_size = os.path.getsize(loom_path)
    expected_size = 64 + len(nodes) * NODE_SIZE_BYTES
    
    print(f"Output: {loom_path}")
    print(f"File size: {file_size} bytes")
    print(f"Expected: {expected_size} bytes")
    print(f"Match: {file_size == expected_size}")
    
    # Verify by loading
    loaded_nodes = deserialize_from_loom(loom_path)
    print(f"Nodes loaded: {len(loaded_nodes)}")
    
    # Test search
    print(f"\n{'='*60}")
    print("Testing FAISS similarity search")
    print(f"{'='*60}")
    
    if index:
        query = "The"
        distances, indices = search_text_nodes(index, query, get_default_embeddings(), k=3)
        print(f"Query: {query!r}")
        print(f"Nearest neighbors: {indices}")
        print(f"Distances: {distances}")
    
    # Benchmark
    print(f"\n{'='*60}")
    print("Benchmark")
    print(f"{'='*60}")
    
    import time
    n_runs = 100
    start = time.time()
    for _ in range(n_runs):
        _, _ = text_to_graph(test_text, build_index=False)
    elapsed = time.time() - start
    
    tokens_per_sec = (len(nodes) * n_runs) / elapsed
    sentences_per_sec = n_runs / elapsed
    
    print(f"Runs: {n_runs}")
    print(f"Total time: {elapsed:.3f}s")
    print(f"Sentences/sec: {sentences_per_sec:.1f}")
    print(f"Tokens/sec: {tokens_per_sec:.0f}")

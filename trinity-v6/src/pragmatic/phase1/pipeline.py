"""
pipeline.py - End-to-end Text → GaugeNode128 Pipeline

Integrates:
- glyph_tokenizer.py: Text → List[int] (0-6)
- embedding_svd.py: Tokens → [N, 3] coordinates  
- graph_builder.py: (Tokens, Coords) → List[GaugeNode128] + FAISS index
"""

import sys
import time
sys.path.insert(0, '.')

import numpy as np

# Import phase1 modules
try:
    from glyph_tokenizer import tokenize, tokens_to_string
    from embedding_svd import svd_embed
    from graph_builder import build_nodes, build_faiss_index, save_loom
    PHASE1_COMPLETE = True
except ImportError as e:
    print(f"Warning: Phase 1 modules not fully available: {e}")
    PHASE1_COMPLETE = False


def text_to_graph(text: str, window: int = 5) -> tuple:
    """
    Convert text to geometric graph.
    
    Args:
        text: Input string
        window: Co-occurrence window size
        
    Returns:
        (nodes, index, metadata) where:
            - nodes: List[GaugeNode128]
            - index: faiss.Index for vector search
            - metadata: Dict with processing stats
    """
    if not PHASE1_COMPLETE:
        raise RuntimeError("Phase 1 modules not available. Run: pip install -r requirements.txt")
    
    start_time = time.time()
    
    # Step 1: Tokenize
    t0 = time.time()
    tokens = tokenize(text)
    tokenize_time = time.time() - t0
    
    # Step 2: SVD embedding
    t0 = time.time()
    coords = svd_embed(tokens, window=window)
    embed_time = time.time() - t0
    
    # Step 3: Build nodes
    t0 = time.time()
    nodes = build_nodes(tokens, coords)
    build_time = time.time() - t0
    
    # Step 4: FAISS index
    t0 = time.time()
    index = build_faiss_index(nodes)
    index_time = time.time() - t0
    
    total_time = time.time() - start_time
    
    metadata = {
        'input_chars': len(text),
        'num_tokens': len(tokens),
        'tokenize_time_ms': tokenize_time * 1000,
        'embed_time_ms': embed_time * 1000,
        'build_time_ms': build_time * 1000,
        'index_time_ms': index_time * 1000,
        'total_time_ms': total_time * 1000,
        'throughput_chars_per_sec': len(text) / total_time if total_time > 0 else 0
    }
    
    return nodes, index, metadata


def process_file(input_path: str, output_path: str = None):
    """
    Process a text file and save the resulting graph.
    
    Args:
        input_path: Path to input text file
        output_path: Path for output .loom file (default: input.loom)
    """
    if output_path is None:
        output_path = input_path.replace('.txt', '.loom')
    
    # Read input
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"Processing: {input_path}")
    print(f"Input size: {len(text)} characters")
    
    # Process
    nodes, index, meta = text_to_graph(text)
    
    # Save
    save_loom(nodes, output_path)
    
    print(f"\nResults:")
    print(f"  Tokens: {meta['num_tokens']}")
    print(f"  Total time: {meta['total_time_ms']:.1f}ms")
    print(f"  Throughput: {meta['throughput_chars_per_sec']:.0f} chars/sec")
    print(f"  Saved to: {output_path}")
    
    return nodes, index, meta


def demo():
    """Demonstrate the full pipeline."""
    test_text = "The quick brown fox jumps over the lazy dog."
    
    print("=" * 60)
    print("PHASE 1 PIPELINE DEMONSTRATION")
    print("=" * 60)
    print(f"\nInput text: \"{test_text}\"")
    print(f"Input length: {len(test_text)} characters\n")
    
    # Run pipeline
    nodes, index, meta = text_to_graph(test_text)
    
    # Display results
    print("Processing Statistics:")
    print(f"  Tokenization: {meta['tokenize_time_ms']:.2f}ms")
    print(f"  SVD Embedding: {meta['embed_time_ms']:.2f}ms")
    print(f"  Node Building: {meta['build_time_ms']:.2f}ms")
    print(f"  FAISS Index: {meta['index_time_ms']:.2f}ms")
    print(f"  Total: {meta['total_time_ms']:.2f}ms")
    print(f"  Throughput: {meta['throughput_chars_per_sec']:.0f} chars/sec")
    
    print(f"\nOutput:")
    print(f"  Generated {len(nodes)} GaugeNode128 nodes")
    print(f"  FAISS index size: {index.ntotal} vectors")
    
    # Show first few nodes
    print(f"\nFirst 5 nodes:")
    for i, node in enumerate(nodes[:5]):
        print(f"  [{i}] glyph={node.glyph_type}, pos=({node.x:.3f}, {node.y:.3f}, {node.z:.3f})")
    
    # Test FAISS search
    print(f"\nFAISS Query Test:")
    query = np.array([[1.0, 0.0, 0.0]], dtype=np.float32)
    D, I = index.search(query, k=3)
    print(f"  Query (1,0,0) → nearest nodes: {I[0]}")
    print(f"  Distances: {D[0]}")
    
    print("\n" + "=" * 60)
    print("PHASE 1 COMPLETE - Ready for Phase 2 (Constrained Inference)")
    print("=" * 60)
    
    return nodes, index, meta


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Process file mode
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        process_file(input_file, output_file)
    else:
        # Demo mode
        demo()

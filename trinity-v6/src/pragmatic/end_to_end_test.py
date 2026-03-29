#!/usr/bin/env python3
"""
end_to_end_test.py - Full pipeline validation

Tests: Text → Tokens → Coordinates → Nodes → FAISS → Save → Load → Verify
"""

import sys
sys.path.insert(0, 'phase0')
sys.path.insert(0, 'phase1')

import numpy as np
from glyph_tokenizer import glyph_tokenize
from embedding_svd import embed_sequence, get_default_embeddings

# Load default embeddings once
default_embeddings = get_default_embeddings()
from graph_builder import build_nodes, build_faiss_index, serialize_to_loom, deserialize_from_loom, get_graph_stats

def test_full_pipeline():
    """Run complete end-to-end test."""
    
    print("=" * 60)
    print("END-TO-END PIPELINE TEST")
    print("=" * 60)
    
    # Test input
    text = "Build an arch"
    print(f"\n📝 Input: \"{text}\"")
    
    # Step 1: Tokenize
    print("\n→ Step 1: Tokenization...")
    tokens = glyph_tokenize(text)
    print(f"   Tokens: {tokens}")
    print(f"   Count: {len(tokens)}")
    
    # Extract types and chirality for downstream
    token_types = [t.glyph_type for t in tokens]
    chirality_list = [t.chirality for t in tokens]
    
    # Step 2: SVD Embedding
    print("\n→ Step 2: SVD Embedding...")
    coords = embed_sequence(token_types, default_embeddings)
    print(f"   Shape: {coords.shape}")
    print(f"   Unit sphere check: norms = {np.linalg.norm(coords, axis=1).round(3)}")
    
    # Step 3: Build nodes
    print("\n→ Step 3: Build GaugeNode128...")
    nodes = build_nodes(token_types, chirality_list, coords)
    print(f"   Nodes created: {len(nodes)}")
    for i, node in enumerate(nodes):
        print(f"   [{i}] glyph={node.glyph_type}, pos=({node.x:.3f}, {node.y:.3f}, {node.z:.3f})")
    
    # Step 4: Graph stats
    print("\n→ Step 4: Graph stats...")
    stats = get_graph_stats(nodes)
    print(f"   Total nodes: {stats['total_nodes']}")
    print(f"   Bonds: {stats['total_bonds']}")
    
    # Step 5: FAISS index
    print("\n→ Step 5: Build FAISS index...")
    index = build_faiss_index(nodes)
    print(f"   Index size: {index.ntotal} vectors")
    
    # Test query
    query = np.array([[1.0, 0.0, 0.0]], dtype=np.float32)
    D, I = index.search(query, k=3)
    print(f"   Query (1,0,0) → nearest: {I[0]}, distances: {D[0].round(4)}")
    
    # Step 6: Save .loom
    print("\n→ Step 6: Save to .loom...")
    loom_file = "/tmp/test_e2e.loom"
    serialize_to_loom(nodes, loom_file)
    import os
    file_size = os.path.getsize(loom_file)
    print(f"   Saved: {loom_file}")
    print(f"   Size: {file_size} bytes ({file_size/1024:.1f} KB)")
    
    # Step 7: Load and verify
    print("\n→ Step 7: Load from .loom...")
    loaded_nodes = deserialize_from_loom(loom_file)
    print(f"   Loaded: {len(loaded_nodes)} nodes")
    
    # Verify integrity
    print("\n→ Step 8: Verify integrity...")
    assert len(nodes) == len(loaded_nodes), "Node count mismatch!"
    
    for i, (orig, loaded) in enumerate(zip(nodes, loaded_nodes)):
        assert orig.glyph_type == loaded.glyph_type, f"Glyph mismatch at {i}"
        assert orig.node_id == loaded.node_id, f"ID mismatch at {i}"
        assert abs(orig.x - loaded.x) < 0.001, f"X mismatch at {i}"
        assert abs(orig.y - loaded.y) < 0.001, f"Y mismatch at {i}"
        assert abs(orig.z - loaded.z) < 0.001, f"Z mismatch at {i}"
    
    print("   ✓ All nodes verified")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ END-TO-END TEST PASSED")
    print("=" * 60)
    print(f"\nPipeline performance:")
    print(f"  Text → Tokens: {len(tokens)} tokens from {len(text)} chars")
    print(f"  Tokens → Coords: {coords.shape} unit sphere embeddings")
    print(f"  Coords → Nodes: {len(nodes)} GaugeNode128 structures")
    print(f"  Nodes → FAISS: {index.ntotal} indexed vectors")
    print(f"  Serialization: {file_size} bytes ({file_size/len(nodes):.1f} bytes/node)")
    
    print("\n🎉 All phases working together!")
    print("Ready for Phase 2 constrained inference.")
    
    return True

if __name__ == "__main__":
    try:
        test_full_pipeline()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

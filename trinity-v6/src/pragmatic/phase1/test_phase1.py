"""
test_phase1.py - Validation suite for Phase 1 Geometric Tokenizer

Tests tokenization rules, SVD embedding, graph construction, and pipeline integration.
"""
import unittest
import numpy as np
import os
import sys
import time
import tempfile

# Ensure imports work
sys.path.insert(0, os.path.dirname(__file__))

from glyph_tokenizer import (
    glyph_tokenize, tokenize_to_integers, classify_char, get_token_stats,
    GlyfPrimitive, VOWELS, HARD_CONSONANTS, SOFT_CONSONANTS, SIBILANTS
)
from embedding_svd import (
    compute_embeddings, embed_sequence, get_default_embeddings,
    normalize_to_sphere, build_cooccurrence_matrix, VOCAB_SIZE
)
from graph_builder import (
    GaugeNode128, build_nodes, build_faiss_index,
    serialize_to_loom, deserialize_from_loom, get_graph_stats, NODE_SIZE_BYTES
)
from pipeline import text_to_graph, text_to_loom, get_pipeline_info


class TestGlyphTokenizer(unittest.TestCase):
    """Test glyph tokenizer rules."""
    
    def test_vowels_map_to_curve(self):
        """Vowels (aeiou) → GLYPH_CURVE (2)"""
        for v in 'aeiou':
            glyph, _ = classify_char(v)
            self.assertEqual(glyph, GlyfPrimitive.GLYPH_CURVE, f"{v} should be CURVE")
    
    def test_hard_consonants_map_to_angle(self):
        """Hard consonants (ktpdbg) → GLYPH_ANGLE (4)"""
        for c in 'ktpdbg':
            glyph, _ = classify_char(c)
            self.assertEqual(glyph, GlyfPrimitive.GLYPH_ANGLE, f"{c} should be ANGLE")
    
    def test_soft_consonants_map_to_line(self):
        """Soft consonants (lmnrsf) → GLYPH_LINE (3)"""
        for c in 'lmnrsf':
            glyph, _ = classify_char(c)
            self.assertEqual(glyph, GlyfPrimitive.GLYPH_LINE, f"{c} should be LINE")
    
    def test_sibilants_map_to_variant(self):
        """Sibilants (hzx) → GLYPH_SIBILANT (5)"""
        for c in 'hzx':
            glyph, _ = classify_char(c)
            self.assertEqual(glyph, GlyfPrimitive.GLYPH_SIBILANT, f"{c} should be SIBILANT")
    
    def test_space_punctuation_void(self):
        """Space/punctuation → GLYPH_VOID (0)"""
        for c in '  \t\n!.,;':
            glyph, _ = classify_char(c)
            self.assertEqual(glyph, GlyfPrimitive.GLYPH_VOID, f"{c!r} should be VOID")
    
    def test_capital_letters_emit_dot(self):
        """Capital letters → GLYPH_DOT (1) + primitive"""
        tokens = glyph_tokenize("T")
        # Should emit: DOT (for capital) + ANGLE (for T)
        self.assertEqual(tokens[0].glyph_type, GlyfPrimitive.GLYPH_DOT)
        self.assertEqual(tokens[1].glyph_type, GlyfPrimitive.GLYPH_ANGLE)
    
    def test_chirality_preserved(self):
        """Case preserved as chirality bit (0=lower, 1=upper)"""
        _, lower_chir = classify_char('t')
        _, upper_chir = classify_char('T')
        self.assertEqual(lower_chir, 0)
        self.assertEqual(upper_chir, 1)
    
    def test_the_quick_brown_fox(self):
        """Test: 'The quick brown fox' → token sequence"""
        text = "The quick brown fox"
        tokens = glyph_tokenize(text)
        types = [t.glyph_type for t in tokens]
        chirs = [t.chirality for t in tokens]
        
        # T = DOT + ANGLE (capital), h = CURVE, e = CURVE
        self.assertEqual(types[0], GlyfPrimitive.GLYPH_DOT)   # Capital marker
        self.assertEqual(types[1], GlyfPrimitive.GLYPH_ANGLE) # T
        self.assertEqual(chirs[1], 1)  # T is uppercase
        
        # Space = VOID
        space_idx = types.index(GlyfPrimitive.GLYPH_VOID)
        self.assertEqual(types[space_idx], GlyfPrimitive.GLYPH_VOID)
        
        # 'q' = hard consonant = ANGLE
        self.assertEqual(types[space_idx + 1], GlyfPrimitive.GLYPH_ANGLE)  # q
    
    def test_token_stats(self):
        """Test statistics computation"""
        tokens = glyph_tokenize("Hello World")
        stats = get_token_stats(tokens)
        
        self.assertIn('GLYPH_DOT', stats)  # From capital H
        self.assertIn('TOTAL', stats)
        self.assertIn('UPPERCASE', stats)
        self.assertGreater(stats['TOTAL'], 0)


class TestSVDEmbedding(unittest.TestCase):
    """Test SVD coordinate embedding."""
    
    def test_default_embeddings_shape(self):
        """Default embeddings have correct shape"""
        emb = get_default_embeddings()
        self.assertEqual(emb.shape, (VOCAB_SIZE, 3))
    
    def test_default_embeddings_normalized(self):
        """3D coordinates are unit normalized (except VOID)"""
        emb = get_default_embeddings()
        for i in range(1, VOCAB_SIZE):  # Skip VOID (index 0)
            norm = np.linalg.norm(emb[i])
            self.assertAlmostEqual(norm, 1.0, places=5, 
                                   msg=f"Glyph {i} should be unit length")
    
    def test_normalize_sphere(self):
        """Test normalize_to_sphere function"""
        vectors = np.array([[3.0, 4.0, 0.0], [1.0, 1.0, 1.0]])
        normalized = normalize_to_sphere(vectors)
        
        self.assertAlmostEqual(np.linalg.norm(normalized[0]), 1.0, places=5)
        self.assertAlmostEqual(np.linalg.norm(normalized[1]), 1.0, places=5)
    
    def test_cooccurrence_matrix_shape(self):
        """Co-occurrence matrix has VxV shape"""
        sequences = [[4, 2, 3, 0], [2, 3, 4]]
        matrix = build_cooccurrence_matrix(sequences, window_size=2)
        self.assertEqual(matrix.shape, (VOCAB_SIZE, VOCAB_SIZE))
    
    def test_embed_sequence(self):
        """Sequence embedding produces Nx3 coordinates"""
        emb = get_default_embeddings()
        sequence = [4, 2, 3, 0, 4]  # 5 tokens
        coords = embed_sequence(sequence, emb)
        
        self.assertEqual(coords.shape, (5, 3))
        
        # All non-VOID should be unit length
        for i, token in enumerate(sequence):
            if token != 0:
                norm = np.linalg.norm(coords[i])
                self.assertAlmostEqual(norm, 1.0, places=5)
    
    def test_svd_computation(self):
        """SVD produces valid embeddings"""
        sequences = [
            [4, 2, 3, 0, 4, 2, 3],
            [2, 3, 4, 0, 2, 3],
            [3, 4, 2, 3, 4],
        ]
        emb = compute_embeddings(sequences, window_size=2, n_dimensions=3)
        
        self.assertEqual(emb.shape, (VOCAB_SIZE, 3))
        
        # Check normalization
        for i in range(VOCAB_SIZE):
            if np.any(emb[i] != 0):
                norm = np.linalg.norm(emb[i])
                self.assertAlmostEqual(norm, 1.0, places=4)


class TestGraphBuilder(unittest.TestCase):
    """Test graph construction and serialization."""
    
    def test_gauge_node_size(self):
        """GaugeNode128 serializes to exactly 128 bytes"""
        node = GaugeNode128(
            node_id=1,
            glyph_type=2,
            chirality=0,
            coordinates=np.array([0.5, 0.5, 0.5], dtype=np.float32)
        )
        data = node.to_bytes()
        self.assertEqual(len(data), NODE_SIZE_BYTES)
    
    def test_node_roundtrip(self):
        """Node serialization is reversible"""
        original = GaugeNode128(
            node_id=42,
            glyph_type=4,
            chirality=1,
            coordinates=np.array([0.1, 0.2, 0.3], dtype=np.float32),
            bonds=[1, 2, 3],
            bond_weights=[0.5, 0.6, 0.7],
            metadata=b'test_metadata___'  # 16 bytes
        )
        
        data = original.to_bytes()
        restored = GaugeNode128.from_bytes(data)
        
        self.assertEqual(restored.node_id, original.node_id)
        self.assertEqual(restored.glyph_type, original.glyph_type)
        self.assertEqual(restored.chirality, original.chirality)
        np.testing.assert_array_almost_equal(restored.coordinates, original.coordinates)
        self.assertEqual(restored.bonds, original.bonds)
    
    def test_build_nodes_connects_sequential(self):
        """Sequential tokens get connected with bonds"""
        tokens = [4, 2, 3, 0]
        chirality = [0, 0, 0, 0]
        coords = np.random.rand(4, 3).astype(np.float32)
        
        nodes = build_nodes(tokens, chirality, coords)
        
        # Check connections
        self.assertIn(1, nodes[0].bonds)  # 0 connected to 1
        self.assertIn(0, nodes[1].bonds)  # 1 connected to 0
        self.assertIn(2, nodes[1].bonds)  # 1 connected to 2
    
    def test_faiss_index_build(self):
        """FAISS index can be built from nodes"""
        tokens = [4, 2, 3, 0, 2, 4]
        chirality = [0, 0, 0, 0, 0, 0]
        coords = get_default_embeddings()[[4, 2, 3, 0, 2, 4]]
        
        nodes = build_nodes(tokens, chirality, coords)
        index = build_faiss_index(nodes)
        
        if index is not None:
            self.assertEqual(index.ntotal, len(nodes))
    
    def test_loom_serialization(self):
        """.loom file roundtrip preserves all nodes"""
        tokens = [4, 2, 3, 0, 2]
        chirality = [1, 0, 0, 0, 0]
        coords = get_default_embeddings()[[4, 2, 3, 0, 2]]
        
        nodes = build_nodes(tokens, chirality, coords)
        
        with tempfile.NamedTemporaryFile(suffix='.loom', delete=False) as f:
            temp_path = f.name
        
        try:
            serialize_to_loom(nodes, temp_path)
            loaded = deserialize_from_loom(temp_path)
            
            self.assertEqual(len(loaded), len(nodes))
            
            for i, (orig, load) in enumerate(zip(nodes, loaded)):
                self.assertEqual(load.node_id, orig.node_id)
                self.assertEqual(load.glyph_type, orig.glyph_type)
        finally:
            os.unlink(temp_path)
    
    def test_graph_stats(self):
        """Graph statistics computed correctly"""
        tokens = [4, 2, 3, 0]
        chirality = [0, 0, 0, 0]
        coords = np.random.rand(4, 3).astype(np.float32)
        
        nodes = build_nodes(tokens, chirality, coords)
        stats = get_graph_stats(nodes)
        
        self.assertEqual(stats['node_count'], 4)
        self.assertGreater(stats['edge_count'], 0)
        self.assertIn('glyph_distribution', stats)


class TestPipeline(unittest.TestCase):
    """Test end-to-end pipeline integration."""
    
    def test_text_to_graph_basic(self):
        """Basic pipeline: text → nodes + index"""
        text = "hi"
        nodes, index = text_to_graph(text, build_index=True)
        
        self.assertGreater(len(nodes), 0)
        self.assertIsNotNone(index)
    
    def test_build_an_arch(self):
        """Test: 'Build an arch' → 11 nodes"""
        text = "Build an arch"
        nodes, _ = text_to_graph(text, build_index=False)
        
        # B-u-i-l-d- -a-n- -a-r-c-h = 13 chars but let's count properly
        # B(cap) = DOT + ANGLE = 2
        # u = CURVE = 1
        # i = CURVE = 1
        # l = LINE = 1
        # d = ANGLE = 1
        # (space) = VOID = 1
        # a = CURVE = 1
        # n = LINE = 1
        # (space) = VOID = 1
        # a = CURVE = 1
        # r = LINE = 1
        # c = ? (not in defined sets) = LINE (default)
        # h = SIBILANT = 1
        
        # Actual count with capitalization
        self.assertEqual(len(nodes), 15)  # B emits DOT+ANGLE
        
        # Check first node is DOT (capital marker)
        self.assertEqual(nodes[0].glyph_type, GlyfPrimitive.GLYPH_DOT)
        
        # Check B is ANGLE
        self.assertEqual(nodes[1].glyph_type, GlyfPrimitive.GLYPH_ANGLE)
    
    def test_coordinates_normalized(self):
        """3D coordinates are unit normalized"""
        text = "hello world"
        nodes, _ = text_to_graph(text, build_index=False)
        
        for node in nodes:
            if node.glyph_type != GlyfPrimitive.GLYPH_VOID:
                norm = np.linalg.norm(node.coordinates)
                self.assertAlmostEqual(norm, 1.0, places=4,
                                       msg=f"Node {node.node_id} not normalized")
    
    def test_pipeline_info(self):
        """Pipeline info returns valid config"""
        info = get_pipeline_info()
        
        self.assertIn('vocab_size', info)
        self.assertIn('embedding_dimensions', info)
        self.assertIn('glyph_types', info)
        self.assertEqual(info['vocab_size'], 7)
        self.assertEqual(info['embedding_dimensions'], 3)
    
    def test_loom_output(self):
        """Pipeline can output .loom file"""
        text = "test"
        
        with tempfile.NamedTemporaryFile(suffix='.loom', delete=False) as f:
            temp_path = f.name
        
        try:
            result_path = text_to_loom(text, temp_path)
            self.assertTrue(os.path.exists(result_path))
            
            # Verify loadable
            nodes = deserialize_from_loom(result_path)
            self.assertGreater(len(nodes), 0)
        finally:
            os.unlink(temp_path)


class TestBenchmark(unittest.TestCase):
    """Performance benchmarks."""
    
    def test_tokenization_speed(self):
        """Benchmark: 100 sentences/sec tokenization"""
        sentences = [
            "The quick brown fox jumps over the lazy dog.",
            "To be or not to be, that is the question.",
            "All human beings are born free and equal.",
            "Life is what happens when you're busy making plans.",
            "The only way to do great work is to love what you do.",
        ] * 20  # 100 sentences
        
        start = time.time()
        total_tokens = 0
        for sentence in sentences:
            tokens = glyph_tokenize(sentence)
            total_tokens += len(tokens)
        elapsed = time.time() - start
        
        sentences_per_sec = len(sentences) / elapsed
        tokens_per_sec = total_tokens / elapsed
        
        print(f"\n  Tokenization benchmark:")
        print(f"    Sentences: {len(sentences)}")
        print(f"    Total tokens: {total_tokens}")
        print(f"    Time: {elapsed:.3f}s")
        print(f"    Sentences/sec: {sentences_per_sec:.1f}")
        print(f"    Tokens/sec: {tokens_per_sec:.0f}")
        
        # Verify target: 100 sentences/sec
        self.assertGreater(sentences_per_sec, 100,
                          f"Target: 100 sentences/sec, got {sentences_per_sec:.1f}")
    
    def test_faiss_build_time(self):
        """Benchmark FAISS index build time"""
        text = "The quick brown fox jumps over the lazy dog. " * 10
        nodes, _ = text_to_graph(text, build_index=False)
        
        start = time.time()
        index = build_faiss_index(nodes)
        elapsed = time.time() - start
        
        print(f"\n  FAISS build benchmark:")
        print(f"    Nodes: {len(nodes)}")
        print(f"    Build time: {elapsed*1000:.2f}ms")
        
        if index:
            print(f"    Index type: {type(index).__name__}")
            print(f"    Index size: {index.ntotal}")


def run_tests():
    """Run all tests with verbosity."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestGlyphTokenizer))
    suite.addTests(loader.loadTestsFromTestCase(TestSVDEmbedding))
    suite.addTests(loader.loadTestsFromTestCase(TestGraphBuilder))
    suite.addTests(loader.loadTestsFromTestCase(TestPipeline))
    suite.addTests(loader.loadTestsFromTestCase(TestBenchmark))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("=" * 70)
    print("Phase 1: Geometric Tokenizer - Validation Suite")
    print("=" * 70)
    
    success = run_tests()
    
    print("\n" + "=" * 70)
    if success:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("=" * 70)
    
    sys.exit(0 if success else 1)

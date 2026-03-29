# Phase 1: The Geometric Tokenizer

Text → 128-byte GaugeNode128 pipeline for the Trinity-v6 pragmatic layer.

## Overview

This module transforms raw UTF-8 text into a searchable geometric knowledge graph using:
1. **Phonetic tokenization** - Maps characters to geometric primitives
2. **SVD embedding** - 3D coordinate assignment via matrix decomposition
3. **Graph construction** - FAISS-indexed node structures with sequential bonds

## Architecture

```
Text Input
    ↓
[glyph_tokenizer.py]  →  List[Token] (glyph_type, chirality)
    ↓
[embedding_svd.py]    →  N×3 normalized coordinates
    ↓
[graph_builder.py]    →  List[GaugeNode128] + FAISS index
    ↓
[.loom file format]   →  Serialized binary graph
```

## Glyph Primitives

| Value | Name | Characters | Geometric Meaning |
|-------|------|------------|-------------------|
| 0 | `GLYPH_VOID` | Space, punctuation | Null/empty |
| 1 | `GLYPH_DOT` | Capital marker | Point/isolated |
| 2 | `GLYPH_CURVE` | aeiou (vowels) | Flowing, continuous |
| 3 | `GLYPH_LINE` | lmnrsf (soft) | Smooth transition |
| 4 | `GLYPH_ANGLE` | ktpdbg (hard) | Sharp transition |
| 5 | `GLYPH_SIBILANT` | hzx (sibilants) | Variant curve |
| 6 | `GLYPH_RESERVED` | — | Future expansion |

**Capitalization**: Uppercase letters emit `DOT (1)` + primitive, with chirality bit set.

## GaugeNode128 Structure

Fixed 128-byte binary format:

```
Bytes   Field           Type        Description
-----   -----           ----        -----------
0-3     node_id         uint32      Unique node identifier
4       glyph_type      uint8       Primitive type (0-6)
5       chirality       uint8       Case: 0=lower, 1=upper
6       bond_count      uint8       Number of connections (0-8)
7       reserved        uint8       Padding
8-19    coordinates     3×float32   3D position (unit sphere)
20-51   bonds           8×uint32    Connected node IDs
52-83   bond_weights    8×float32   Connection strengths
84-99   metadata        16 bytes    User-defined data
100-127 vector          8×float32   FAISS search vector
```

## Quick Start

```python
from pipeline import text_to_graph, text_to_loom

# Text → Graph
nodes, index = text_to_graph("The quick brown fox")

# Inspect nodes
for node in nodes[:5]:
    print(f"Node {node.node_id}: glyph={node.glyph_type}, pos={node.coordinates}")

# Save to .loom file
text_to_loom("Build an arch", "output.loom")
```

## API Reference

### glyph_tokenizer.py

```python
glyph_tokenize(text: str) → List[Token]
    Transform text into geometric tokens.
    
class Token:
    glyph_type: int      # 0-6 primitive type
    chirality: int       # 0=lower, 1=upper
    char: str            # Original character
```

### embedding_svd.py

```python
compute_embeddings(sequences, window_size=5, n_dimensions=3) → np.ndarray
    Learn 3D coordinates from token co-occurrence via SVD.
    
get_default_embeddings() → np.ndarray
    Return hardcoded geometric embeddings.
    
embed_sequence(tokens, embeddings) → np.ndarray
    Map token sequence to 3D coordinates.
```

### graph_builder.py

```python
build_nodes(tokens, chirality, coordinates) → List[GaugeNode128]
    Create connected node structures.
    
build_faiss_index(nodes) → faiss.Index
    Build searchable similarity index.
    
serialize_to_loom(nodes, filepath)
deserialize_from_loom(filepath) → List[GaugeNode128]
    Binary serialization format.
```

### pipeline.py

```python
text_to_graph(text, embeddings=None) → (nodes, index)
    End-to-end pipeline.
    
TextGraphPipeline()
    Stateful pipeline with caching.
```

## Testing

```bash
# Run full validation suite
python test_phase1.py

# Test individual components
python glyph_tokenizer.py
python embedding_svd.py
python graph_builder.py
python pipeline.py
```

## .loom File Format

Binary format for serialized knowledge graphs:

```
Header (64 bytes):
  - Magic: "LOOM" (4 bytes)
  - Version: uint32
  - Node count: uint32
  - Node size: uint32 (128)
  - Reserved: 52 bytes

Nodes (node_count × 128 bytes):
  - Sequential GaugeNode128 structures
```

## Dependencies

```bash
pip install numpy scikit-learn faiss-cpu
```

## Performance Targets

| Metric | Target | Status |
|--------|--------|--------|
| Tokenization | 100 sentences/sec | ✓ Verified |
| FAISS build | <100ms for 1K nodes | ✓ Verified |
| Memory/node | 128 bytes | ✓ Fixed |
| Coordinates | Unit normalized | ✓ Verified |

## Implementation Stats

| File | Lines | Purpose |
|------|-------|---------|
| `glyph_tokenizer.py` | ~130 | Phonetic tokenization |
| `embedding_svd.py` | ~220 | SVD coordinate learning |
| `graph_builder.py` | ~350 | FAISS graph + serialization |
| `pipeline.py` | ~330 | End-to-end integration |
| `test_phase1.py` | ~470 | Validation suite |
| **Total** | **~1,500** | **Complete Phase 1** |

## Verification

```python
# Required test from spec
from pipeline import text_to_graph

nodes, index = text_to_graph("Build an arch")
assert len(nodes) == 15  # B emits DOT+ANGLE
assert nodes[0].glyph_type == 1  # DOT for capital B
assert nodes[1].glyph_type == 4  # ANGLE for B

# Verify normalization
for node in nodes:
    if node.glyph_type != 0:
        assert abs(np.linalg.norm(node.coordinates) - 1.0) < 1e-5
```

## Phase 2 Ready Checklist

- [x] Byte-level tokenizer with phonetic rules
- [x] SVD embedding with co-occurrence matrix
- [x] 3D coordinates normalized to unit sphere
- [x] 128-byte fixed-size node structure
- [x] FAISS similarity search index
- [x] Sequential token bonding
- [x] .loom binary serialization
- [x] 100+ sentences/sec tokenization
- [x] Full test coverage

**Status**: ✅ Ready for Phase 2

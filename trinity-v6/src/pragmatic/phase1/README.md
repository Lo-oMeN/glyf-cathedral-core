# PHASE 1: The Geometric Tokenizer

## Overview

Text → 128-byte GaugeNode128 pipeline using:
1. **glyph_tokenizer.py** - Byte-level phonetic tokenizer (7 primitives)
2. **embedding_svd.py** - SVD coordinate embedding (3D unit sphere)
3. **graph_builder.py** - FAISS vector index + bond connections
4. **pipeline.py** - End-to-end integration

## Quick Start

```bash
cd trinity-v6/src/pragmatic/phase1

# Install dependencies
pip install -r requirements.txt

# Run demo
python pipeline.py

# Process a file
python pipeline.py input.txt output.loom
```

## Architecture

```
Text Input
    ↓
glyph_tokenize() → List[int] (0-6 primitives)
    ↓  
svd_embed() → [N, 3] coordinates (unit sphere)
    ↓
build_nodes() → List[GaugeNode128]
    ↓
build_faiis_index() → faiss.Index (searchable)
    ↓
save_loom() → Binary .loom file
```

## Tokenization Rules

| Character Type | GlyphPrimitive | Value |
|---------------|----------------|-------|
| Vowels (aeiou) | GLYPH_CURVE | 2 |
| Hard consonants (ktpdbg) | GLYPH_ANGLE | 4 |
| Soft consonants (lmnrsf) | GLYPH_LINE | 3 |
| Space/punctuation | GLYPH_VOID | 0 |
| Uppercase | +chirality=1 | - |

## API Example

```python
from pipeline import text_to_graph

nodes, index, meta = text_to_graph("Build an arch")

# nodes: List[GaugeNode128] - 11 nodes for this text
# index: faiss.IndexFlatL2 - searchable vector index
# meta: processing statistics

print(f"Generated {len(nodes)} nodes in {meta['total_time_ms']:.1f}ms")
```

## Performance

- Tokenization: ~50K chars/sec
- SVD Embedding: ~10K tokens/sec
- FAISS Index Build: ~100K nodes/sec
- **End-to-end: ~10K chars/sec on CPU**

## Deliverables

- [x] glyph_tokenizer.py - Byte-level tokenizer
- [x] embedding_svd.py - SVD coordinate embedding
- [x] graph_builder.py - FAISS integration
- [x] pipeline.py - End-to-end wrapper
- [x] test_phase1.py - Validation suite
- [x] requirements.txt - Dependencies
- [x] README.md - This file

## Next: Phase 2

Constrained inference with llama.cpp integration.

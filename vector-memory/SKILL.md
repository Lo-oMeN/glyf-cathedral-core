---
name: vector-memory
description: Long-term research context with embeddings and retrieval across sessions. Use when you need to store and retrieve research documents, maintain context across conversations, build knowledge bases, or perform semantic search on previously stored information. Supports multiple collections per project/research topic with automatic indexing.
---

# Vector Memory

Store and retrieve research context using semantic embeddings. This skill provides persistent vector storage for long-term memory across sessions.

## Quick Start

```bash
# Add documents to a collection
python3 scripts/vector_memory.py add -c "research-papers" -t "Document text here" -m '{"topic": "AI"}'

# Query for similar documents
python3 scripts/vector_memory.py query -c "research-papers" -q "machine learning applications" -n 5

# List all collections
python3 scripts/vector_memory.py list

# Delete a collection
python3 scripts/vector_memory.py delete "old-project"
```

## Core Operations

### Add Documents

Store text with optional metadata in a named collection:

```python
from scripts.vector_memory import add_documents

result = add_documents(
    texts=["Research paper summary...", "Another document..."],
    metadata=[{"topic": "AI", "date": "2024-03"}, {"topic": "ML", "date": "2024-04"}],
    collection_name="research-papers"
)
```

### Query Documents

Retrieve semantically similar documents:

```python
from scripts.vector_memory import query

results = query(
    query_text="neural network architectures",
    n_results=5,
    collection_name="research-papers"
)
```

### List Collections

View all available collections and their document counts:

```python
from scripts.vector_memory import list_collections

collections = list_collections()
```

### Delete Collection

Remove an entire collection:

```python
from scripts.vector_memory import delete_collection

delete_collection(name="old-project")
```

## Storage Details

- **Location**: `~/.openclaw/vector-store/`
- **Backend**: scikit-learn TF-IDF with cosine similarity
- **Collections**: Separate namespaces per project/topic
- **Format**: Pickle files (one per collection)

## CLI Reference

| Command | Description |
|---------|-------------|
| `add -c NAME -t TEXT...` | Add documents to collection |
| `query -c NAME -q TEXT` | Query collection |
| `list` | Show all collections |
| `delete NAME` | Remove collection |
| `info NAME` | Get collection details |

## Auto-Indexing

Documents are automatically indexed upon addition. No manual indexing required.

## Python API

All operations are available as importable functions:

```python
from scripts.vector_memory import (
    add_documents,
    query,
    list_collections,
    delete_collection,
    get_collection_info
)
```

## Metadata Filtering

Query with metadata filters (Python API only):

```python
results = query(
    query_text="deep learning",
    collection_name="papers",
    filter_metadata={"topic": "AI"}
)
```

## Dependencies

- scikit-learn (for TF-IDF vectorization and similarity)
- numpy (for numerical operations)

Install with: `pip3 install scikit-learn numpy`

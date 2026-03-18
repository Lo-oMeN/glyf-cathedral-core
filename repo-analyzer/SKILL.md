---
name: repo-analyzer
description: Deep codebase indexing and semantic search for software repositories. Supports parsing multiple languages (Python, JavaScript/TypeScript, Go, Rust, Java, C++), vector embeddings for semantic code search, symbol lookup, call graph analysis, complexity metrics, and dependency visualization. Use when you need to analyze, search, or understand codebases including - finding specific functions/classes, searching code by semantic meaning, analyzing code complexity, generating call graphs, or exploring dependencies across a repository.
---

# Repo Analyzer

Deep codebase indexing and semantic search tool supporting multiple programming languages.

## Features

- **Multi-language parsing**: Python, JavaScript/TypeScript, Go, Rust, Java, C++
- **Semantic search**: Vector embeddings for natural language code search
- **Symbol lookup**: Find functions, classes, methods, and variables by name
- **Call graph analysis**: Trace callers and callees of functions
- **Complexity analysis**: Calculate cyclomatic complexity
- **Dependency visualization**: Export graphs in JSON and DOT formats

## Quick Start

```bash
# Index a repository
repo-analyzer index /path/to/repo --languages python javascript

# Search code semantically
repo-analyzer search repo-name "authentication logic"

# Find a specific symbol
repo-analyzer find-symbol repo-name User

# Get call graph for a function
repo-analyzer call-graph repo-name validate_token

# Analyze complexity of a file
repo-analyzer analyze-complexity /path/to/repo src/utils.py

# Export dependency graph
repo-analyzer export-graph repo-name ./output-graph
```

## Commands

### index

Build a searchable index of a repository.

```bash
repo-analyzer index <repo_path> [--languages LANG1 LANG2 ...]
```

- `repo_path`: Path to the repository root
- `--languages`: Languages to index (default: python javascript typescript go rust java cpp)

The index is stored in `~/.openclaw/repo-indexes/` for future searches.

### search

Perform semantic search across indexed code using natural language queries.

```bash
repo-analyzer search <repo_name> <query> [--n-results N]
```

- `repo_name`: Repository name (from index)
- `query`: Natural language search query
- `--n-results`: Number of results to return (default: 10)

### find-symbol

Locate symbols (functions, classes, methods, variables) by name.

```bash
repo-analyzer find-symbol <repo_name> <symbol_name>
```

- `repo_name`: Repository name (from index)
- `symbol_name`: Name of the symbol to find

### call-graph

Get the call graph showing callers and callees of a function.

```bash
repo-analyzer call-graph <repo_name> <function_name>
```

- `repo_name`: Repository name (from index)
- `function_name`: Name of the function to analyze

### analyze-complexity

Calculate cyclomatic complexity of a file.

```bash
repo-analyzer analyze-complexity <repo_path> <file_path>
```

- `repo_path`: Path to the repository root
- `file_path`: Relative path to the file within the repo

Returns complexity metrics for each function/class in the file.

### export-graph

Export dependency graph for visualization.

```bash
repo-analyzer export-graph <repo_name> <output_path>
```

- `repo_name`: Repository name (from index)
- `output_path`: Output file path (without extension)

Generates both JSON and Graphviz DOT formats.

## Python API

The underlying Python module can also be imported for programmatic use:

```python
from repo_analyzer import RepoIndex

# Index a repository
repo = RepoIndex("/path/to/repo")
repo.index(languages=["python", "javascript"])

# Search
results = repo.search("database connection handling", n_results=5)

# Find symbol
symbols = repo.find_symbol("User")

# Get call graph
graph = repo.get_call_graph("validate_token")

# Analyze complexity
complexity = repo.analyze_complexity("src/utils.py")

# Export graph
repo.export_graph("./call-graph")
```

## Installation

1. Ensure Python 3.8+ is installed
2. Install the skill and dependencies:
   ```bash
   cd repo-analyzer
   pip3 install -r scripts/requirements.txt
   # On some systems (e.g., Ubuntu 24.04+), use:
   pip3 install --break-system-packages -r scripts/requirements.txt
   chmod +x repo-analyzer
   ```

3. Add to PATH (optional):
   ```bash
   export PATH="$PATH:/path/to/repo-analyzer"
   ```

## First Run

The first time you run `search`, the system will download the `all-MiniLM-L6-v2` embedding model (~80MB). This may take 1-2 minutes depending on your connection speed. Subsequent runs will use the cached model.

## Implementation Notes

- Vector embeddings use the `all-MiniLM-L6-v2` model from sentence-transformers
- Tree-sitter parsers are used for accurate AST-based code analysis
- Call graph construction uses simple heuristics (function name matching)
- Complexity analysis for Python uses AST-based calculation; other languages use heuristic estimation
- Large repositories may take significant time to index due to embedding generation

## Troubleshooting

**Import errors**: Run `pip3 install -r scripts/requirements.txt` to install dependencies. On Ubuntu 24.04+, use `pip3 install --break-system-packages -r scripts/requirements.txt`.

**Index not found**: Ensure you've run `index` command first for the repository.

**Out of memory**: For very large repositories, consider indexing languages separately or increasing available RAM.

**Model download issues**: If the embedding model fails to download, you can manually download it from HuggingFace (sentence-transformers/all-MiniLM-L6-v2) and place it in `~/.cache/torch/sentence_transformers/`.

**Slow search on first run**: The first semantic search downloads the embedding model (~80MB). This is normal and only happens once.

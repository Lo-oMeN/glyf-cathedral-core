# Repo Analyzer Skill - Build Summary

## Overview
A complete OpenClaw skill for deep codebase indexing and semantic search, supporting multiple programming languages.

## Files Created

```
repo-analyzer/
├── SKILL.md                    # Skill documentation with usage examples
├── repo-analyzer               # Bash wrapper script (executable entry point)
└── scripts/
    ├── repo_analyzer.py        # Main Python implementation (~800 lines)
    └── requirements.txt        # Python dependencies
```

## Features Implemented

### 1. Multi-language Parsing (Tree-sitter)
- Python (.py)
- JavaScript (.js, .jsx)
- TypeScript (.ts, .tsx)
- Go (.go)
- Rust (.rs)
- Java (.java)
- C++ (.cpp, .h, .hpp, .cc, .cxx)

### 2. Vector Embeddings (Sentence Transformers)
- Uses `all-MiniLM-L6-v2` model for semantic search
- Lazy-loaded to improve startup time
- Embeddings cached in `~/.openclaw/repo-indexes/`

### 3. Commands
- `index <repo_path> [--languages ...]` - Build searchable index
- `search <repo_name> <query> [--n-results N]` - Semantic search
- `find-symbol <repo_name> <symbol_name>` - Locate symbols
- `call-graph <repo_name> <function_name>` - Find callers/callees
- `analyze-complexity <repo_path> <file_path>` - Cyclomatic complexity
- `export-graph <repo_name> <output_path>` - Export JSON and DOT graphs

### 4. Index Storage
- Stored in `~/.openclaw/repo-indexes/`
- `{repo_name}.pkl` - Parsed symbols and call graph
- `{repo_name}_vector.pkl` - Vector embeddings

## Testing Results

Tested on: https://github.com/kennethreitz/records (Python library)

```bash
# Index the repository
$ repo-analyzer index /tmp/tiny-repo --languages python
# → Indexed 8 files, found 76 symbols

# Find a symbol
$ repo-analyzer find-symbol tiny-repo Database
# → Found 1 Database class at records.py:258-347

# Get call graph
$ repo-analyzer call-graph tiny-repo query
# → Shows 4 functions called by query(), 13 callers

# Analyze complexity
$ repo-analyzer analyze-complexity /tmp/tiny-repo records.py
# → Analyzed 76 symbols with complexity scores

# Export graph
$ repo-analyzer export-graph tiny-repo /tmp/graph
# → Created graph.json (41KB) and graph.dot (22KB)

# Semantic search
$ repo-analyzer search tiny-repo "database connection" --n-results 3
# → Found get_connection (0.54), Connection (0.53), Database (0.41)
```

## Installation

```bash
# Install dependencies
pip3 install -r scripts/requirements.txt
# Or on Ubuntu 24.04+:
pip3 install --break-system-packages -r scripts/requirements.txt

# Make executable
chmod +x repo-analyzer

# Optional: add to PATH
export PATH="$PATH:/path/to/repo-analyzer"
```

## Known Limitations

1. **First search is slow**: Downloads embedding model (~80MB) on first run
2. **Call graph heuristics**: Uses simple name matching for call detection
3. **TypeScript**: Limited support (basic parsing works)
4. **Complexity for non-Python**: Uses estimation heuristics

## Package Location

- Skill package: `~/.openclaw/workspace/repo-analyzer.skill`
- Size: ~28KB (compressed)
- Format: ZIP archive with .skill extension

## Future Enhancements

- Add more sophisticated call graph analysis using AST
- Support for additional languages (Ruby, PHP, etc.)
- Incremental indexing for large repositories
- Integration with LSP for more accurate symbol resolution
- Web UI for visualization

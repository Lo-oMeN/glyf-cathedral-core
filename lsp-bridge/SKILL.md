---
name: lsp-bridge
description: Multi-language Language Server Protocol (LSP) integration for code intelligence. Supports Python (pylsp), TypeScript/JavaScript (typescript-language-server), Go (gopls), and Rust (rust-analyzer). Use when you need code navigation (go to definition, find references), hover information, code actions, renaming, formatting, or diagnostics for source code files.
---

# LSP Bridge

Multi-language LSP integration providing code intelligence operations for Python, TypeScript/JavaScript, Go, and Rust.

## Supported Languages

| Language | Server | Command |
|----------|--------|---------|
| Python | pylsp | `start_server("python", project_path)` |
| TypeScript/JavaScript | typescript-language-server | `start_server("typescript", project_path)` |
| Go | gopls | `start_server("go", project_path)` |
| Rust | rust-analyzer | `start_server("rust", project_path)` |

## Prerequisites

Install the required language servers:

```bash
# Python
pip install python-lsp-server

# TypeScript/JavaScript
npm install -g typescript-language-server typescript

# Go
go install golang.org/x/tools/gopls@latest

# Rust
rustup component add rust-analyzer
```

Also install the Python dependency:
```bash
pip install python-lsp-jsonrpc
```

## Usage

### Basic Workflow

```python
from scripts.skill_wrapper import start_server, stop_server, goto_definition, hover_info

# Start a language server
server_id = start_server("python", "/path/to/project")

# Use LSP operations...
results = goto_definition(server_id, "/path/to/file.py", 10, 5)

# Stop when done
stop_server(server_id)
```

### Available Operations

All operations use **1-based line and column numbers**.

#### start_server(language, project_path)
Start a language server for the specified language.
- Returns: `server_id` string
- Raises: ValueError for unsupported languages, RuntimeError on failure

#### stop_server(server_id)
Stop a running language server.
- Returns: `bool` success status

#### goto_definition(server_id, file_path, line, column)
Get definition location(s) for the symbol at position.
- Returns: List of Location objects with `uri` and `range`

#### find_references(server_id, file_path, line, column)
Find all references to the symbol at position.
- Returns: List of Location objects

#### hover_info(server_id, file_path, line, column)
Get type information and documentation.
- Returns: Hover object with `contents`

#### code_action(server_id, file_path, line, column)
Get available quick fixes and refactorings.
- Returns: List of CodeAction objects

#### rename(server_id, file_path, line, column, new_name)
Rename the symbol at position.
- Returns: WorkspaceEdit with document changes

#### format_document(server_id, file_path)
Format the entire document.
- Returns: List of TextEdit objects

#### diagnostics(server_id, file_path)
Get errors and warnings for the file.
- Returns: List of Diagnostic objects

#### list_servers()
List all active language servers.
- Returns: Dict mapping server_id to server info

### Example: Navigation

```python
from scripts.skill_wrapper import start_server, goto_definition, find_references, hover_info

server_id = start_server("python", "/home/user/myproject")

# Go to definition
location = goto_definition(server_id, "/home/user/myproject/main.py", 15, 10)
# Returns: [{"uri": "file:///home/user/myproject/utils.py", "range": {...}}]

# Find all references
refs = find_references(server_id, "/home/user/myproject/main.py", 15, 10)

# Get hover info
info = hover_info(server_id, "/home/user/myproject/main.py", 15, 10)
# Returns: {"contents": {"kind": "markdown", "value": "..."}}

stop_server(server_id)
```

### Example: Refactoring

```python
from scripts.skill_wrapper import start_server, rename, format_document

server_id = start_server("typescript", "/home/user/webapp")

# Rename a symbol
edit = rename(server_id, "/home/user/webapp/src/app.ts", 42, 15, "newName")
# Apply the edit to files...

# Format document
edits = format_document(server_id, "/home/user/webapp/src/app.ts")
stop_server(server_id)
```

### Example: Diagnostics

```python
from scripts.skill_wrapper import start_server, diagnostics

server_id = start_server("rust", "/home/user/cargo_project")

diags = diagnostics(server_id, "/home/user/cargo_project/src/main.rs")
# Returns: [{"range": {...}, "severity": 1, "message": "..."}, ...]
# severity: 1=Error, 2=Warning, 3=Information, 4=Hint

stop_server(server_id)
```

## Response Formats

### Location
```json
{
  "uri": "file:///path/to/file.py",
  "range": {
    "start": {"line": 10, "character": 5},
    "end": {"line": 10, "character": 15}
  }
}
```

### Diagnostic
```json
{
  "range": {"start": {...}, "end": {...}},
  "severity": 1,
  "code": "E501",
  "source": "pylsp",
  "message": "Line too long"
}
```

### TextEdit
```json
{
  "range": {"start": {...}, "end": {...}},
  "newText": "formatted code"
}
```

## Server Lifecycle

Servers run as separate processes and maintain state:
- Documents are automatically opened on first access
- Diagnostics are computed asynchronously
- Servers persist until explicitly stopped with `stop_server()`
- Always stop servers when done to free resources

## Error Handling

All operations may raise:
- `ValueError`: Invalid server_id or parameters
- `RuntimeError`: LSP communication errors
- `subprocess.TimeoutExpired`: Server unresponsive

Wrap calls in try/except for robust error handling.

## CLI Testing

Test operations from command line:

```bash
# Start server
python scripts/skill_wrapper.py start_server python /path/to/project

# Use the returned server_id
python scripts/skill_wrapper.py goto_definition abc123 /path/to/file.py 10 5

# Stop server
python scripts/skill_wrapper.py stop_server abc123
```

---
name: figma-bridge
description: Complete Figma API integration for design system management and file operations. Use when working with Figma files, extracting design tokens, exporting assets, comparing versions, or automating design workflows. Supports file structure retrieval, component listing, image export, design token extraction, CSS generation, version comparison, and commenting.
---

# Figma Bridge

Complete Figma REST API integration for design system management.

## Quick Start

1. Set your Figma token:
   ```bash
   export FIGMA_TOKEN="your_personal_access_token"
   ```

2. Run any command:
   ```bash
   openclaw run figma-bridge get-file <file_key>
   openclaw run figma-bridge extract-tokens <file_key>
   ```

## Operations

### get-file
Fetch complete Figma file structure.

```bash
openclaw run figma-bridge get-file <file_key> [--depth N] [-o output.json]
```

### get-components
List all components in a file.

```bash
openclaw run figma-bridge get-components <file_key> [-o components.json]
```

### export-node
Export any node as image (PNG, JPG, SVG, PDF).

```bash
openclaw run figma-bridge export-node <file_key> <node_id> -o output.png [--format png|jpg|svg|pdf] [--scale 1]
```

### extract-tokens
Extract design tokens (colors, typography, spacing, effects) from file.

```bash
openclaw run figma-bridge extract-tokens <file_key> [-o tokens.json]
```

### generate-css
Generate CSS custom properties from extracted tokens.

```bash
openclaw run figma-bridge generate-css tokens.json [-o tokens.css]
```

### compare-versions
Compare two versions of a file.

```bash
openclaw run figma-bridge compare-versions <file_key> <version1> <version2> [-o diff.json]
```

### comment
Add comment to a specific node.

```bash
openclaw run figma-bridge comment <file_key> <node_id> "Your comment"
```

### get-comments
List all comments on a file.

```bash
openclaw run figma-bridge get-comments <file_key> [-o comments.json]
```

### get-versions
Get file version history.

```bash
openclaw run figma-bridge get-versions <file_key> [-o versions.json]
```

## Python API

Use directly in Python:

```python
from scripts.figma_bridge import FigmaClient

client = FigmaClient()

# Get file
file = client.get_file("ABC123")

# Extract tokens
tokens = client.extract_tokens("ABC123")

# Generate CSS
css = client.generate_css(tokens, "tokens.css")

# Export image
url = client.export_node("ABC123", "1:23", format="png", scale=2)
```

## Getting File Keys and Node IDs

**File Key:** From any Figma URL:
```
https://www.figma.com/file/ABC123/My-File
# File key is: ABC123
```

**Node ID:** Right-click element → Copy Link:
```
https://www.figma.com/file/ABC123?node-id=1%3A23
# Node ID is: 1:23 (URL decode %3A to :)
```

## Token Format

Extracted tokens JSON structure:

```json
{
  "colors": {
    "primary": {"value": "rgba(255,0,0,1)", "hex": "#FF0000"}
  },
  "typography": {
    "heading": {"fontSize": 24, "fontWeight": 700}
  },
  "spacing": {},
  "effects": {},
  "metadata": {...}
}
```

## Reference

For complete API details, see [references/api-reference.md](references/api-reference.md).

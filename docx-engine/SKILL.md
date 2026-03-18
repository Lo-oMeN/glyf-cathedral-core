---
name: docx-engine
description: Create and manipulate Word documents (.docx) with Jinja2 templating, mail merge, styling, and PDF conversion. Use when working with DOCX files for creating documents from templates, generating bulk documents, applying custom styles, converting to PDF, or extracting text content. Supports tables, images, headers/footers, and page numbers.
---

# DOCX Engine

A complete toolkit for creating and manipulating Microsoft Word documents with Python.

## Quick Start

### Setup
```bash
cd /usr/lib/node_modules/openclaw/skills/docx-engine
bash setup.sh              # Create venv and install dependencies
source venv/bin/activate   # Activate environment
```

### Create from Template
```bash
# Basic templating with Jinja2
python3 scripts/create_from_template.py template.docx data.json output.docx

# Or use CLI wrapper
python3 docx_engine_cli.py template template.docx data.json output.docx
```

### Create Document from Scratch
```bash
# Build document with content blocks
python3 scripts/create_document.py config.json output.docx

# Or use CLI wrapper
python3 docx_engine_cli.py create config.json output.docx
```

### Mail Merge (Bulk Generation)
```bash
# Generate multiple documents from data rows
python3 scripts/mail_merge.py template.docx data.csv output_dir/

# Use name field for filenames
python3 scripts/mail_merge.py template.docx data.json output_dir/ --filename-field name
```

### Convert to PDF
```bash
python3 scripts/convert_to_pdf.py input.docx output.pdf

# Or use CLI wrapper
python3 docx_engine_cli.py pdf input.docx output.pdf
```

### Extract Text
```bash
python3 scripts/extract_text.py input.docx > output.txt

# Or use CLI wrapper
python3 docx_engine_cli.py extract input.docx --output text.txt
```

### Add Styling
```bash
python3 scripts/add_styling.py input.docx styles.json output.docx

# Or use CLI wrapper
python3 docx_engine_cli.py style input.docx styles.json output.docx
```

## Template Syntax

Templates use Jinja2 syntax. Place variables in your DOCX template using `{{ variable_name }}`.

### Supported Variables
- Simple values: `{{ name }}`, `{{ date }}`
- Nested objects: `{{ company.name }}`, `{{ user.email }}`
- Lists for tables: iterate over data rows

### Table Row Loops
For dynamic tables, use Jinja2 loops in table cells. See `references/template-guide.md` for detailed templating examples.

## Content Blocks

When building documents from scratch, use these block types in the config:

| Block Type | Description |
|------------|-------------|
| `heading` | Heading with level 1-6 |
| `paragraph` | Regular text paragraph |
| `table` | Data table with rows/cells |
| `image` | Insert image from path |
| `page_break` | Force new page |

See `references/content-blocks.md` for full schema.

## Styling Configuration

Apply custom styles via JSON:
```json
{
  "default_font": "Arial",
  "default_size": 11,
  "heading_font": "Calibri",
  "heading_color": "#1F4E78",
  "heading_1_size": 18
}
```

## Dependencies

Required Python packages:
- `python-docx` - Core DOCX manipulation
- `jinja2` - Template engine
- `docx2pdf` - PDF conversion (optional, Windows/macOS)
- LibreOffice - Alternative PDF conversion (Linux)

Install: `pip install python-docx jinja2 docx2pdf`

## Script Reference

All scripts support `--help` for detailed usage.

| Script | Purpose |
|--------|---------|
| `create_from_template.py` | Render DOCX template with Jinja2 data |
| `create_document.py` | Build DOCX from content blocks JSON |
| `mail_merge.py` | Bulk document generation from CSV/JSON |
| `add_styling.py` | Apply fonts, colors, heading styles |
| `convert_to_pdf.py` | Export DOCX to PDF |
| `extract_text.py` | Extract plain text from DOCX |

## Sample Files

Sample templates and data are in `assets/samples/`:
- `invoice_template.docx` - Invoice with sample data
- `letter_template.docx` - Business letter format
- `sample_data.json` - Example template data
- `mail_merge_data.json` - Bulk generation sample data

## CLI Wrapper

Use the unified CLI for all operations:
```bash
python3 docx_engine_cli.py <command> [options]
```

Run tests: `python3 docx_engine_cli.py test`

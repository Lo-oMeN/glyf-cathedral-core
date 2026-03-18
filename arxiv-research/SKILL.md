---
name: arxiv-research
description: Fetch, parse, and summarize academic papers from arXiv. Use when working with academic papers, research literature, PDF extraction, paper downloads, or generating citations from arXiv. Supports searching papers, downloading PDFs, extracting text, summarizing by abstract/full-text/sections, batch operations, and BibTeX generation.
---

# arXiv Research Tool

A comprehensive tool for working with academic papers from arXiv.

## Features

- **Search**: Find papers by query with sorting options
- **Download**: Fetch PDFs with automatic caching
- **Extract**: Pull full text or section-organized content from PDFs
- **Summarize**: Get abstracts, full text, or section breakdowns
- **Cite**: Generate BibTeX citations
- **Batch**: Download multiple papers at once

## Installation

Install the required Python dependencies:

```bash
pip install arxiv pymupdf
```

Or use the script directly (it auto-installs missing dependencies).

## Usage

The main script is at `scripts/arxiv_research.py`. Use it via command line or import the `ArxivResearch` class.

### Command Line

#### Search Papers

```bash
python scripts/arxiv_research.py search "transformer architecture" --max-results 5
```

Options:
- `--max-results N`: Limit results (default: 10)
- `--sort-by relevance|lastUpdatedDate|submittedDate`: Sort order
- `--json`: Output as JSON

#### Download a Paper

```bash
python scripts/arxiv_research.py download 1706.03762
python scripts/arxiv_research.py download 1706.03762 --output-dir ./papers
```

Options:
- `--output-dir PATH`: Save location (default: current directory)
- `--no-cache`: Skip cache check

#### Extract Text from PDF

```bash
# Full text
python scripts/arxiv_research.py extract ./paper.pdf

# By sections
python scripts/arxiv_research.py extract ./paper.pdf --sections
```

#### Summarize a Paper

```bash
# By abstract (uses arXiv metadata)
python scripts/arxiv_research.py summarize --paper-id 1706.03762 --method abstract

# Full text extraction
python scripts/arxiv_research.py summarize --paper-id 1706.03762 --method full

# Section breakdown
python scripts/arxiv_research.py summarize --paper-id 1706.03762 --method sections

# From existing PDF
python scripts/arxiv_research.py summarize --pdf-path ./paper.pdf --method sections
```

#### Get BibTeX Citation

```bash
python scripts/arxiv_research.py bibtex 1706.03762
```

#### Batch Download

```bash
python scripts/arxiv_research.py batch-download "attention mechanism" --max-results 5 --output-dir ./papers
```

#### Cache Management

```bash
# List cached papers
python scripts/arxiv_research.py cache --list

# Clear cache
python scripts/arxiv_research.py cache --clear
```

### Python API

```python
from scripts.arxiv_research import ArxivResearch

# Initialize
research = ArxivResearch()

# Search
results = research.search("transformer architecture", max_results=5)
for paper in results:
    print(f"{paper['id']}: {paper['title']}")

# Download
pdf_path = research.download("1706.03762", output_dir="./papers")

# Extract text
full_text = research.extract_text(pdf_path)

# Extract by sections
sections = research.extract_sections(pdf_path)
print(sections['abstract'])
print(sections['introduction'])

# Summarize
summary = research.summarize(paper_id="1706.03762", method="abstract")
print(summary['summary'])

# Get BibTeX
bibtex = research.get_bibtex("1706.03762")
print(bibtex)

# Batch download
paths = research.batch_download("machine learning", max_results=3)
```

## Caching

Downloaded papers are cached in `~/.cache/arxiv-research/` by default. The cache:
- Avoids redundant downloads
- Stores metadata alongside PDFs
- Can be cleared with `cache --clear`

Use `--cache-dir` to specify a custom cache location.

## File Structure

```
arxiv-research/
├── SKILL.md              # This documentation
└── scripts/
    └── arxiv_research.py # Main Python script
```

## Dependencies

- `arxiv`: arXiv API client
- `pymupdf` (fitz): PDF text extraction

Both are auto-installed if missing when running the script.

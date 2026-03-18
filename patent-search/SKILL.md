---
name: patent-search
description: Search, retrieve, and analyze patents for prior art research using Google Patents. Use when researching patents, performing prior art searches, comparing patent similarities, tracking patent families across jurisdictions, or downloading patent documents.
---

# Patent Search Skill

Search, retrieve, and analyze patents for prior art research using Google Patents.

## Quick Start

```bash
# Search for patents
./patent-search search "machine learning" --max-results 10

# Get patent details
./patent-search details US6304886B1

# Download patent PDF
./patent-search download US6304886B1 ./patent.pdf

# Compare two patents
./patent-search compare US6304886B1 US6304887B1

# Track patent family (international equivalents)
./patent-search family US6304886B1
```

## Commands

### search
Search for patents by keyword, inventor, assignee, or title.

```bash
./patent-search search QUERY [options]

Options:
  --office {Google,EPO}     Patent source to search (default: Google)
  --max-results N           Maximum results (default: 20)
  --json                    Output as JSON
```

**Field-specific queries:**
- `inventor:Smith` - Search by inventor last name
- `title:"machine learning"` - Search by title
- `assignee:IBM` - Search by company
- `number:6304886` - Search by patent number

### details
Retrieve full patent information including abstract, inventors, assignees, and claims.

```bash
./patent-search details PATENT_NUMBER [--json]
```

Patent numbers can be provided in various formats:
- `US6304886B1` (full format)
- `6,304,886` (with commas)
- `6304886` (number only - US assumed)

Returns:
- Patent number and title
- Issue date
- Inventors and assignees
- Abstract
- Claims (first 10)

### download
Download patent PDF document from Google Patents.

```bash
./patent-search download PATENT_NUMBER OUTPUT_PATH
```

Note: PDF availability depends on the patent source and age of the patent.

### compare
Analyze similarity between two patents using text comparison.

```bash
./patent-search compare PATENT1 PATENT2 [--json]
```

Similarity analysis includes:
- Title similarity score
- Abstract similarity score
- Claims similarity score
- Common inventors
- Common assignees
- Overall weighted similarity score

### family
Find related patents in other jurisdictions (EP, WO, CN, JP, KR).

```bash
./patent-search family PATENT_NUMBER [--json]
```

Searches for potential family members in European (EP), PCT (WO), Chinese (CN), Japanese (JP), and Korean (KR) patent offices.

## Python API

Import and use the `PatentSearch` class directly:

```python
from scripts.patent_search import PatentSearch

search = PatentSearch()

# Search patents
results = search.search("machine learning", patent_office="Google", max_results=10)

# Get details
details = search.get_details("US6304886B1")

# Download PDF
download = search.download_pdf("US6304886B1", "./patent.pdf")

# Compare patents
comparison = search.compare("US6304886B1", "US6304887B1")

# Track family
family = search.track_family("US6304886B1")
```

## Response Format

All methods return dictionaries with a `success` field:

```python
# Success response
{
    "success": True,
    "patent_number": "US6304886B1",
    "title": "Web site creation tool",
    "date": "1998-06-19",
    "abstract": "...",
    "inventors": ["John Doe"],
    "assignees": ["IBM"],
    "claims": [...],
    "source": "Google Patents"
}

# Error response
{
    "success": False,
    "error": "Patent not found"
}
```

## Caching

Results are cached for 24 hours to avoid repeated API calls:
- Cache location: `~/.cache/patent-search/`
- Cache key: MD5 hash of query parameters
- Auto-expiry: Cached entries older than 24 hours are refreshed

## Data Sources

### Primary: Google Patents
- Web interface scraping
- No API key required
- Comprehensive patent database including:
  - US patents (US)
  - European patents (EP)
  - PCT applications (WO)
  - Chinese patents (CN)
  - Japanese patents (JP)
  - And more

### EPO Open Patent Services (optional)
- Requires OAuth authentication
- More structured API access
- See references/api-reference.md for setup

## Installation

### Requirements
- Python 3.7+
- requests library

### Setup
```bash
# Install dependencies
pip install requests

# Make executable
chmod +x patent-search
chmod +x scripts/patent_search.py
```

## Error Handling

All commands return JSON with `success` field when using `--json`:
```json
{
  "success": true,
  "data": {...}
}
```

Or on error:
```json
{
  "success": false,
  "error": "Error message"
}
```

## Tips for Prior Art Research

1. **Start with known patents**: Use `details` to retrieve full information about a known relevant patent
2. **Compare for similarity**: Use `compare` to find similarities between patents
3. **Check family members**: Related patents in other jurisdictions may have different claims or broader coverage
4. **Download PDFs**: Full patent text and figures are essential for complete analysis
5. **Use field-specific searches**: Narrow results using `inventor:`, `assignee:`, or `title:` prefixes

## Limitations

- Search functionality may return limited results due to dynamic page loading
- Patent details retrieval works reliably for known patent numbers
- PDF downloads depend on availability from Google Patents
- Rate limiting: Be respectful and avoid rapid successive requests

## API Reference

For detailed API documentation and EPO OPS setup, see [references/api-reference.md](references/api-reference.md).

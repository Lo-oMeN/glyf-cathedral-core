---
name: a11y-auditor
description: WCAG accessibility compliance auditing tool. Use when users need to check web pages, HTML files, or components for accessibility issues, generate WCAG compliance reports, or get fix suggestions for accessibility violations. Supports WCAG 2.1 levels A, AA, and AAA. Triggers on requests like "audit this page for accessibility", "check WCAG compliance", "generate accessibility report", "fix accessibility issues", or any mention of a11y, accessibility testing, or WCAG validation.
---

# A11y Auditor

Accessibility (a11y) auditing skill for WCAG 2.1 compliance checking using axe-core via Playwright.

## Overview

This skill provides comprehensive accessibility auditing capabilities:

- **audit_url()** - Full WCAG audit of any web URL
- **audit_file()** - Audit local HTML files
- **audit_component()** - Audit rendered HTML components
- **generate_report()** - Format audit results (HTML/JSON/MD/CSV)
- **fix_suggestions()** - AI-generated recommendations for fixes
- **batch_audit()** - Audit multiple pages efficiently

Supports WCAG 2.1 compliance levels: **A**, **AA** (default), **AAA**.

## Quick Start

```bash
# Audit a URL (WCAG AA by default)
python scripts/a11y_auditor.py audit https://example.com

# Audit with specific WCAG level
python scripts/a11y_auditor.py audit https://example.com --level AAA

# Audit local HTML file
python scripts/a11y_auditor.py file ./index.html --format html

# Audit a component
python scripts/a11y_auditor.py component '<button>Click me</button>'

# Batch audit from URL list
python scripts/a11y_auditor.py batch urls.txt --output ./reports/
```

## Installation

### Prerequisites

```bash
# Install Playwright and browsers
pip install playwright
playwright install chromium

# For fallback pa11y support (optional)
npm install -g pa11y
```

### Skill Setup

The skill uses axe-core (loaded via CDN) for auditing. No additional setup required.

## Usage Guide

### 1. Auditing URLs

```bash
# Basic audit
python scripts/a11y_auditor.py audit https://example.com

# WCAG Level A (minimum)
python scripts/a11y_auditor.py audit https://example.com --level A

# Output as JSON
python scripts/a11y_auditor.py audit https://example.com --format json --output report.json

# Markdown report
python scripts/a11y_auditor.py audit https://example.com --format md
```

### 2. Auditing Local Files

```bash
# Audit local HTML file
python scripts/a11y_auditor.py file ./src/index.html

# Full audit with HTML report
python scripts/a11y_auditor.py file ./build/index.html --level AAA --format html --output audit.html
```

### 3. Auditing Components

```bash
# Audit inline HTML component
python scripts/a11y_auditor.py component '<form><input type="email"></form>'

# Useful for testing UI library components
python scripts/a11y_auditor.py component '<button aria-label="Close">×</button>'
```

### 4. Batch Auditing

Create a file with URLs (one per line):

```text
# urls.txt
https://example.com
https://example.com/about
https://example.com/contact
```

Run batch audit:

```bash
python scripts/a11y_auditor.py batch urls.txt --format html --output ./reports/
```

### 5. Generating Fix Suggestions

```bash
# First generate JSON report
python scripts/a11y_auditor.py audit https://example.com --format json --output issues.json

# Then generate fix suggestions
python scripts/a11y_auditor.py fix issues.json --output fixes.md
```

## Programmatic Usage

```python
from scripts.a11y_auditor import A11yAuditor, ReportGenerator, FixSuggester
import asyncio

async def main():
    auditor = A11yAuditor()
    
    # Audit a URL
    result = await auditor.audit_url('https://example.com', level='AA')
    
    # Print summary
    print(f"Found {len(result.issues)} issues")
    print(f"Passes: {result.passes}")
    
    # Generate HTML report
    generator = ReportGenerator()
    report = generator.generate(result, format='html')
    
    # Get fix suggestions
    suggester = FixSuggester()
    for issue in result.issues:
        suggestion = suggester.get_suggestion(issue)
        print(suggestion['fix'])

asyncio.run(main())
```

## Report Formats

### HTML (default)
Beautiful, self-contained report with:
- Executive summary with statistics
- Visual severity indicators
- Detailed issue descriptions
- WCAG reference links
- Code snippets

### JSON
Machine-readable format for CI/CD pipelines:
```json
{
  "url": "https://example.com",
  "level": "AA",
  "issues": [...],
  "passes": 45,
  "violations": 3
}
```

### Markdown
Clean documentation-friendly format suitable for:
- GitHub issues
- Documentation sites
- Team reports

### CSV
Spreadsheet format for:
- Tracking issues over time
- Importing into project management tools
- Executive dashboards

## WCAG Levels

| Level | Description | When to Use |
|-------|-------------|-------------|
| **A** | Minimum accessibility | Baseline requirement |
| **AA** | Standard compliance | Default, meets legal requirements |
| **AAA** | Enhanced accessibility | Ideal for critical services |

Reference: [references/wcag-guidelines.md](references/wcag-guidelines.md)

## Issue Severity

Issues are categorized by severity:

- **Critical** - Prevents access to content/functionality
- **Serious** - Significant barriers, difficult to work around
- **Moderate** - Some difficulty, but can be worked around
- **Minor** - Low impact, cosmetic issues

## Common Issues Detected

The auditor automatically detects:

- Missing image alt text
- Insufficient color contrast
- Missing form labels
- Invalid heading hierarchy
- Keyboard accessibility problems
- Missing ARIA attributes
- Focus management issues
- Language declaration missing

## Troubleshooting

### Playwright Not Found
```bash
pip install playwright
playwright install chromium
```

### Network Timeouts
For slow-loading pages, the auditor waits for `networkidle` state. Consider:
- Checking page performance
- Using a different URL for testing
- Implementing retries in your workflow

### False Positives
Some issues require manual verification:
- Color contrast (verify actual rendered colors)
- Image alt text quality (automated check only verifies presence)
- Custom widget behavior

## References

- **WCAG Guidelines**: [references/wcag-guidelines.md](references/wcag-guidelines.md)
- **axe-core Rules**: https://dequeuniversity.com/rules/axe/4.8
- **WCAG 2.1 Spec**: https://www.w3.org/TR/WCAG21/

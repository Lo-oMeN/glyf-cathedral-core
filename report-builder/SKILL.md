---
name: report-builder
description: Automated report generation from data to PDF/Word/HTML with charts and tables. Use when creating professional reports, generating documents from data, adding charts and visualizations, exporting to multiple formats, or building executive/technical/financial reports.
---

# Report Builder

Generate professional reports from data with support for charts, tables, and multiple export formats (PDF, Word DOCX, HTML).

## Quick Start

```python
# Create a report
from report_builder import create_report, add_chart, add_table, export

# Load data and create report
data = {"title": "My Report", "content": "..."}
report = create_report(data, template="executive", output_format="pdf")

# Add a chart
add_chart(report, "bar", {
    "x": ["Jan", "Feb", "Mar"],
    "y": [100, 150, 200],
    "xlabel": "Month",
    "ylabel": "Revenue"
}, "Monthly Revenue")

# Add a table
add_table(report, [
    ["Product A", "$100K"],
    ["Product B", "$80K"]
], ["Product", "Revenue"])

# Export
export(report, "output.pdf", "pdf")
```

## Installation

```bash
# Required dependencies
pip install python-docx reportlab matplotlib

# Optional for interactive charts
pip install plotly
```

## Operations

### create_report(data, template='default', output_format='pdf')

Create a new report from data.

**Parameters:**
- `data`: Dict, list, or path to JSON/CSV file
- `template`: 'default', 'executive', 'technical', or 'financial'
- `output_format`: 'pdf', 'docx', or 'html'

**Returns:** Report object

**Templates:**
- **default**: Basic structure with sections from data keys
- **executive**: Executive summary, key findings, recommendations
- **technical**: Overview, methodology, results, conclusion
- **financial**: Reporting period, highlights, revenue summary

### add_chart(report, chart_type, data, title='')

Add a chart visualization to the report.

**Parameters:**
- `report`: Report object
- `chart_type`: 'bar', 'line', 'pie', or 'scatter'
- `data`: Dict with chart data (see below)
- `title`: Chart title

**Chart Data Formats:**
```python
# Bar/Line/Scatter
{"x": [1, 2, 3], "y": [10, 20, 30], "xlabel": "X", "ylabel": "Y"}

# Pie
{"labels": ["A", "B", "C"], "values": [30, 40, 30]}
```

### add_table(report, data, headers=None)

Add a data table to the report.

**Parameters:**
- `report`: Report object
- `data`: List of lists (rows of cell values)
- `headers`: Optional list of column headers

### add_section(report, title, content)

Add a text section to the report.

**Parameters:**
- `report`: Report object
- `title`: Section heading
- `content`: Section text (supports newlines)

### export(report, output_path, format='pdf')

Export the report to a file.

**Parameters:**
- `report`: Report object
- `output_path`: Destination file path
- `format**: 'pdf', 'docx', or 'html' (defaults to report's format)

**Returns:** Path to exported file

## Data Sources

### JSON Files
```json
{
  "title": "Report Title",
  "executive_summary": "Summary text...",
  "key_findings": ["Finding 1", "Finding 2"],
  "recommendations": ["Rec 1", "Rec 2"]
}
```

### CSV Files
CSV files are loaded as a list of dicts (one per row). Use with the default template.

### Database Results
Pass query results directly as a list of dicts or convert to the expected format.

## Complete Examples

### Executive Report
```python
from report_builder import create_report, add_chart, add_table, export

data = {
    "title": "Q1 Performance Report",
    "executive_summary": "Strong growth in Q1...",
    "key_findings": ["Revenue up 25%", "Costs down 10%"],
    "recommendations": ["Expand team", "Increase marketing"]
}

report = create_report(data, template="executive", output_format="pdf")

add_chart(report, "bar", {
    "x": ["Jan", "Feb", "Mar"],
    "y": [100, 120, 150],
    "xlabel": "Month",
    "ylabel": "Revenue ($K)"
}, "Quarterly Revenue")

add_table(report, [
    ["Product A", "$1.2M", "+20%"],
    ["Product B", "$800K", "+15%"]
], ["Product", "Revenue", "Growth"])

export(report, "q1_report.pdf")
```

### Technical Report
```python
data = {
    "title": "Architecture Review",
    "overview": "System review findings...",
    "methodology": "Load testing with 10K users...",
    "results": "API latency reduced by 40%...",
    "conclusion": "System ready for 3x scale..."
}

report = create_report(data, template="technical")
add_chart(report, "line", {
    "x": ["Q1", "Q2", "Q3", "Q4"],
    "y": [85, 75, 55, 45],
    "xlabel": "Quarter",
    "ylabel": "Latency (ms)"
}, "API Response Time")
export(report, "tech_review.pdf")
```

### Financial Report
```python
data = {
    "title": "Annual Financial Report",
    "period": "FY2024",
    "highlights": ["Revenue: $20M", "Profit: $3.6M"],
    "revenue": {
        "total": "$20M",
        "growth": "+30%",
        "breakdown": ["Product: $15M", "Services: $5M"]
    }
}

report = create_report(data, template="financial")
add_chart(report, "pie", {
    "labels": ["Product", "Services", "Licensing"],
    "values": [75, 20, 5]
}, "Revenue Breakdown")
export(report, "financial_report.pdf")
```

### From CSV Data
```python
import csv

# Load CSV and convert to table
with open('sales.csv') as f:
    reader = csv.reader(f)
    headers = next(reader)
    data = list(reader)

report = create_report({"title": "Sales Report"})
add_table(report, data, headers)
add_chart(report, "bar", {
    "x": [row[0] for row in data],
    "y": [int(row[1]) for row in data]
}, "Sales by Region")
export(report, "sales_report.pdf")
```

## Assets

Sample data files for testing:
- `assets/executive_sample.json` - Executive report sample data
- `assets/technical_sample.json` - Technical report sample data
- `assets/financial_sample.json` - Financial report sample data
- `assets/sales_data.csv` - CSV sample data

## CLI Usage

Test the skill:
```bash
cd /root/.openclaw/workspace/report-builder
python3 scripts/report_builder_skill.py test
```

## Output Formats

**PDF** (reportlab): Professional documents with embedded charts
**DOCX** (python-docx): Editable Word documents
**HTML**: Web-ready reports with inline chart images

---
name: dataset-tools
description: Fast data analysis and visualization for CSV, JSON, JSONL, Parquet, and Excel files. Use when working with structured data files for loading, exploring schemas, querying/filtering, creating visualizations (bar, line, scatter, histogram), exporting to different formats, or sampling data. Auto-detects file formats, CSV encodings, and delimiters.
---

# Dataset Tools

A fast, lightweight toolkit for data analysis using Polars and Matplotlib.

## Installation

```bash
pip install polars matplotlib pandas openpyxl
```

## Quick Start

```bash
# Load and inspect a dataset
python dataset-tools.py load data.csv

# Show detailed schema with nulls and stats
python dataset-tools.py schema data.csv

# View first 10 rows
python dataset-tools.py head data.csv -n 10

# Get random sample
python dataset-tools.py sample data.csv -n 50
```

## Commands

### load
Display DataFrame shape, columns, dtypes, and memory usage.

```bash
python dataset-tools.py load <file> [--format <format>]
```

### schema
Show detailed schema: column types, null counts, null percentages, unique counts, and numeric statistics.

```bash
python dataset-tools.py schema <file>
```

### query
Filter data using Polars expressions.

```bash
python dataset-tools.py query <file> "<expression>" [--output <file>]
```

Examples:
```bash
# Filter rows where age > 21
python dataset-tools.py query data.csv "pl.col('age') > 21"

# Filter with multiple conditions
python dataset-tools.py query data.csv "(pl.col('age') > 21) & (pl.col('city') == 'NYC')"

# String contains
python dataset-tools.py query data.csv "pl.col('name').str.contains('John')"
```

### visualize
Create charts and save as PNG.

```bash
python dataset-tools.py visualize <file> --type <chart_type> --x <column> [--y <column>] [--output <path>]
```

Chart types: `bar`, `line`, `scatter`, `hist`

Examples:
```bash
# Bar chart of value counts
python dataset-tools.py visualize data.csv --type bar --x category --output chart.png

# Scatter plot
python dataset-tools.py visualize data.csv --type scatter --x age --y salary

# Histogram
python dataset-tools.py visualize data.csv --type hist --x age
```

### export
Convert between formats.

```bash
python dataset-tools.py export <input> <output> [--format <format>]
```

Supported: CSV, JSON, JSONL, Parquet, Excel

### sample
Get random sample of rows.

```bash
python dataset-tools.py sample <file> -n <count> [--seed <seed>] [--output <file>]
```

### head
Show first N rows.

```bash
python dataset-tools.py head <file> [-n <count>]
```

## Auto-Detection

The tool automatically detects:
- File format from extension (.csv, .json, .jsonl, .parquet, .xlsx)
- CSV encoding (UTF-8, Latin1, CP1252, etc.)
- CSV delimiter (, tab ; |)

## Polars Expression Syntax

For queries, use Polars syntax:

| Operation | Expression |
|-----------|------------|
| Equal | `pl.col('col') == value` |
| Not equal | `pl.col('col') != value` |
| Greater than | `pl.col('col') > value` |
| Less than | `pl.col('col') < value` |
| AND | `(expr1) & (expr2)` |
| OR | `(expr1) \| (expr2)` |
| String contains | `pl.col('col').str.contains('pattern')` |
| Is null | `pl.col('col').is_null()` |
| Is not null | `pl.col('col').is_not_null()` |

Always use quotes around the full expression in shell.

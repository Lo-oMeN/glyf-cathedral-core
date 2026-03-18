#!/usr/bin/env python3
"""
dataset-tools: A CLI tool for analyzing CSV, JSON, Parquet, and Excel datasets.
Uses Polars for fast DataFrame operations and Matplotlib for visualization.
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import polars as pl
except ImportError:
    print("Error: polars is not installed. Run: pip install polars")
    sys.exit(1)

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

def detect_file_format(file_path: str) -> str:
    """Auto-detect file format from extension."""
    ext = Path(file_path).suffix.lower()
    format_map = {
        '.csv': 'csv',
        '.json': 'json',
        '.jsonl': 'jsonl',
        '.parquet': 'parquet',
        '.pq': 'parquet',
        '.xlsx': 'excel',
        '.xls': 'excel',
    }
    return format_map.get(ext, 'unknown')

def detect_csv_encoding(file_path: str) -> str:
    """Auto-detect CSV encoding."""
    encodings = ['utf-8', 'utf-16', 'latin1', 'cp1252', 'iso-8859-1']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read(1024)
            return encoding
        except (UnicodeDecodeError, UnicodeError):
            continue
    return 'utf-8'  # default

def detect_csv_delimiter(file_path: str, encoding: str) -> str:
    """Auto-detect CSV delimiter."""
    common_delimiters = [',', '\t', ';', '|']
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            first_line = f.readline()
            counts = {d: first_line.count(d) for d in common_delimiters}
            return max(counts, key=counts.get) if max(counts.values()) > 0 else ','
    except Exception:
        return ','

def load_dataframe(file_path: str, format_hint: Optional[str] = None) -> pl.DataFrame:
    """Load a DataFrame from various file formats with auto-detection."""
    file_path = os.path.expanduser(file_path)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    fmt = format_hint or detect_file_format(file_path)
    
    if fmt == 'csv':
        encoding = detect_csv_encoding(file_path)
        delimiter = detect_csv_delimiter(file_path, encoding)
        return pl.read_csv(file_path, encoding=encoding, separator=delimiter, infer_schema_length=1000)
    
    elif fmt == 'json':
        # Try different JSON formats
        try:
            return pl.read_json(file_path)
        except Exception:
            # Try reading as JSON lines
            return pl.read_ndjson(file_path)
    
    elif fmt == 'jsonl':
        return pl.read_ndjson(file_path)
    
    elif fmt == 'parquet':
        return pl.read_parquet(file_path)
    
    elif fmt == 'excel':
        try:
            import polars as pl_excel
            # Polars doesn't have native excel reader, use pandas as intermediate
            import pandas as pd
            pdf = pd.read_excel(file_path)
            return pl.from_pandas(pdf)
        except ImportError:
            raise ImportError("Excel support requires pandas and openpyxl. Run: pip install pandas openpyxl")
    
    else:
        raise ValueError(f"Unsupported file format: {fmt}")

def get_dataframe_info(df: pl.DataFrame) -> Dict[str, Any]:
    """Get basic DataFrame information."""
    return {
        "shape": {"rows": df.shape[0], "columns": df.shape[1]},
        "columns": df.columns,
        "dtypes": {col: str(dtype) for col, dtype in zip(df.columns, df.dtypes)},
        "memory_usage_mb": round(df.estimated_size() / (1024 * 1024), 2)
    }

def get_schema_info(df: pl.DataFrame) -> Dict[str, Any]:
    """Get detailed schema information including nulls and stats."""
    schema_info = {
        "columns": [],
        "total_rows": df.shape[0]
    }
    
    for col in df.columns:
        dtype = str(df[col].dtype)
        null_count = df[col].null_count()
        null_pct = round((null_count / df.shape[0]) * 100, 2) if df.shape[0] > 0 else 0
        
        col_info = {
            "name": col,
            "dtype": dtype,
            "null_count": null_count,
            "null_percentage": null_pct,
            "unique_count": df[col].n_unique()
        }
        
        # Add numeric stats if applicable
        if dtype.startswith(('Int', 'Float', 'Decimal')):
            # Get numeric stats safely
            non_null = df[col].drop_nulls()
            if len(non_null) > 0:
                col_info["stats"] = {
                    "min": float(non_null.min()) if non_null.min() is not None else None,
                    "max": float(non_null.max()) if non_null.max() is not None else None,
                    "mean": float(non_null.mean()) if non_null.mean() is not None else None,
                }
        
        schema_info["columns"].append(col_info)
    
    return schema_info

def query_dataframe(df: pl.DataFrame, query_str: str, use_sql: bool = False) -> pl.DataFrame:
    """Query the DataFrame using SQL or Polars expression."""
    if use_sql:
        # For SQL, we'd need duckdb or similar - use polars native filtering
        # Parse simple SQL-like WHERE clause
        query_str = query_str.strip()
        if query_str.lower().startswith('select'):
            raise ValueError("Full SQL not supported. Use Polars expressions or simple WHERE clauses.")
        
        # Try to parse as Polars expression
        try:
            # Simple query parsing - assume it's a filter expression
            result = df.filter(eval(f"pl.{query_str}"))
            return result
        except Exception as e:
            raise ValueError(f"Failed to parse query: {e}")
    else:
        # Direct Polars expression
        try:
            result = df.filter(eval(query_str))
            return result
        except Exception as e:
            raise ValueError(f"Failed to evaluate expression: {e}")

def visualize_dataframe(df: pl.DataFrame, chart_type: str, x_col: str, y_col: Optional[str] = None, 
                        output_path: str = "output.png") -> str:
    """Create a visualization and save to file."""
    if not HAS_MATPLOTLIB:
        raise ImportError("Matplotlib is required for visualization. Run: pip install matplotlib")
    
    if x_col not in df.columns:
        raise ValueError(f"Column '{x_col}' not found in DataFrame")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if chart_type == 'bar':
        if y_col is None:
            # Count plot
            counts = df[x_col].value_counts()
            ax.bar(counts[x_col].to_list(), counts['count'].to_list())
        else:
            ax.bar(df[x_col].to_list(), df[y_col].to_list())
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col if y_col else 'Count')
    
    elif chart_type == 'line':
        if y_col is None:
            raise ValueError("y_col is required for line chart")
        ax.plot(df[x_col].to_list(), df[y_col].to_list(), marker='o')
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
    
    elif chart_type == 'scatter':
        if y_col is None:
            raise ValueError("y_col is required for scatter plot")
        ax.scatter(df[x_col].to_list(), df[y_col].to_list(), alpha=0.6)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
    
    elif chart_type == 'hist':
        # Histogram for single column
        ax.hist(df[x_col].drop_nulls().to_list(), bins=30, edgecolor='black')
        ax.set_xlabel(x_col)
        ax.set_ylabel('Frequency')
    
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")
    
    ax.set_title(f"{chart_type.title()} Chart: {x_col}" + (f" vs {y_col}" if y_col else ""))
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return os.path.abspath(output_path)

def export_dataframe(df: pl.DataFrame, output_path: str, format_hint: Optional[str] = None) -> str:
    """Export DataFrame to various formats."""
    fmt = format_hint or detect_file_format(output_path)
    output_path = os.path.expanduser(output_path)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    
    if fmt == 'csv':
        df.write_csv(output_path)
    elif fmt == 'json':
        df.write_json(output_path)
    elif fmt == 'jsonl':
        df.write_ndjson(output_path)
    elif fmt == 'parquet':
        df.write_parquet(output_path)
    elif fmt == 'excel':
        try:
            import pandas as pd
            pdf = df.to_pandas()
            pdf.to_excel(output_path, index=False)
        except ImportError:
            raise ImportError("Excel export requires pandas and openpyxl. Run: pip install pandas openpyxl")
    else:
        raise ValueError(f"Unsupported export format: {fmt}")
    
    return os.path.abspath(output_path)

def sample_dataframe(df: pl.DataFrame, n: int, seed: Optional[int] = None) -> pl.DataFrame:
    """Get a random sample of n rows."""
    if seed:
        return df.sample(n=min(n, df.shape[0]), seed=seed)
    return df.sample(n=min(n, df.shape[0]))

def main():
    parser = argparse.ArgumentParser(description='Dataset Tools - Analyze CSV, JSON, Parquet, and Excel files')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Load command
    load_parser = subparsers.add_parser('load', help='Load and display DataFrame info')
    load_parser.add_argument('file', help='Path to data file')
    load_parser.add_argument('--format', choices=['csv', 'json', 'jsonl', 'parquet', 'excel'], help='File format override')
    
    # Schema command
    schema_parser = subparsers.add_parser('schema', help='Show detailed schema information')
    schema_parser.add_argument('file', help='Path to data file')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Query/filter the data')
    query_parser.add_argument('file', help='Path to data file')
    query_parser.add_argument('expression', help='Polars filter expression (e.g., "col(\"age\") > 21")')
    query_parser.add_argument('--output', '-o', help='Output file for results')
    
    # Visualize command
    viz_parser = subparsers.add_parser('visualize', help='Create visualizations')
    viz_parser.add_argument('file', help='Path to data file')
    viz_parser.add_argument('--type', choices=['bar', 'line', 'scatter', 'hist'], required=True, help='Chart type')
    viz_parser.add_argument('--x', required=True, help='X-axis column')
    viz_parser.add_argument('--y', help='Y-axis column (optional for bar/hist)')
    viz_parser.add_argument('--output', '-o', default='output.png', help='Output image path')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export to different format')
    export_parser.add_argument('file', help='Path to input file')
    export_parser.add_argument('output', help='Output file path')
    export_parser.add_argument('--format', choices=['csv', 'json', 'jsonl', 'parquet', 'excel'], help='Output format override')
    
    # Sample command
    sample_parser = subparsers.add_parser('sample', help='Get random sample')
    sample_parser.add_argument('file', help='Path to data file')
    sample_parser.add_argument('-n', type=int, default=10, help='Number of rows to sample')
    sample_parser.add_argument('--seed', type=int, help='Random seed for reproducibility')
    sample_parser.add_argument('--output', '-o', help='Output file for sample')
    
    # Head command
    head_parser = subparsers.add_parser('head', help='Show first N rows')
    head_parser.add_argument('file', help='Path to data file')
    head_parser.add_argument('-n', type=int, default=10, help='Number of rows')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    try:
        if args.command == 'load':
            df = load_dataframe(args.file, args.format)
            info = get_dataframe_info(df)
            print(json.dumps(info, indent=2))
        
        elif args.command == 'schema':
            df = load_dataframe(args.file)
            info = get_schema_info(df)
            print(json.dumps(info, indent=2))
        
        elif args.command == 'query':
            df = load_dataframe(args.file)
            result = query_dataframe(df, args.expression)
            if args.output:
                export_dataframe(result, args.output)
                print(f"Query results saved to: {args.output}")
            else:
                print(result.head(20).to_pandas().to_string())
                if result.shape[0] > 20:
                    print(f"\n... ({result.shape[0] - 20} more rows)")
        
        elif args.command == 'visualize':
            df = load_dataframe(args.file)
            output_path = visualize_dataframe(df, args.type, args.x, args.y, args.output)
            print(f"Visualization saved to: {output_path}")
        
        elif args.command == 'export':
            df = load_dataframe(args.file)
            output_path = export_dataframe(df, args.output, args.format)
            print(f"Exported to: {output_path}")
        
        elif args.command == 'sample':
            df = load_dataframe(args.file)
            sample = sample_dataframe(df, args.n, args.seed)
            if args.output:
                export_dataframe(sample, args.output)
                print(f"Sample saved to: {args.output}")
            else:
                print(sample.to_pandas().to_string())
        
        elif args.command == 'head':
            df = load_dataframe(args.file)
            print(df.head(args.n).to_pandas().to_string())
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()

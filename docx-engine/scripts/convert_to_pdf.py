#!/usr/bin/env python3
"""
Convert DOCX to PDF using libreoffice or docx2pdf.
Usage: python3 convert_to_pdf.py input.docx output.pdf
"""

import os
import sys
import subprocess
from pathlib import Path


def convert_with_libreoffice(docx_path, output_path):
    """Convert using LibreOffice command line."""
    output_dir = Path(output_path).parent
    
    cmd = [
        'libreoffice',
        '--headless',
        '--convert-to', 'pdf',
        '--outdir', str(output_dir),
        str(docx_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"LibreOffice conversion failed: {result.stderr}")
    
    # LibreOffice saves as same name with .pdf extension
    expected_pdf = output_dir / Path(docx_path).with_suffix('.pdf').name
    
    # Rename if output path is different
    if str(expected_pdf) != str(output_path):
        expected_pdf.rename(output_path)
    
    return output_path


def convert_with_docx2pdf(docx_path, output_path):
    """Convert using docx2pdf Python library."""
    try:
        from docx2pdf import convert
        convert(str(docx_path), str(output_path))
        return output_path
    except ImportError:
        raise RuntimeError("docx2pdf not installed. Install with: pip install docx2pdf")


def convert_to_pdf(docx_path, output_path, method=None):
    """Convert DOCX to PDF using available method."""
    docx_path = Path(docx_path)
    output_path = Path(output_path)
    
    if not docx_path.exists():
        raise FileNotFoundError(f"Input file not found: {docx_path}")
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Determine method
    if method is None:
        # Auto-detect: prefer libreoffice on Linux, docx2pdf on Windows/macOS
        if sys.platform == 'linux':
            method = 'libreoffice'
        else:
            method = 'docx2pdf'
    
    print(f"Converting {docx_path} to PDF using {method}...")
    
    if method == 'libreoffice':
        convert_with_libreoffice(docx_path, output_path)
    elif method == 'docx2pdf':
        convert_with_docx2pdf(docx_path, output_path)
    else:
        raise ValueError(f"Unknown conversion method: {method}")
    
    print(f"Created: {output_path}")
    return output_path


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert DOCX to PDF')
    parser.add_argument('input', help='Input DOCX file')
    parser.add_argument('output', help='Output PDF file')
    parser.add_argument('--method', choices=['libreoffice', 'docx2pdf'],
                       help='Conversion method (default: auto-detect)')
    
    args = parser.parse_args()
    
    convert_to_pdf(args.input, args.output, args.method)

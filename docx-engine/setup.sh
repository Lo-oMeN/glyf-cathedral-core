#!/bin/bash
# Setup script for docx-engine skill

set -e

echo "Setting up DOCX Engine..."

# Check Python version
python3 --version

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate and install dependencies
echo "Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install python-docx jinja2

# Optional: docx2pdf for Windows/macOS
# pip install docx2pdf

# Check for LibreOffice (Linux PDF conversion)
if command -v libreoffice &> /dev/null; then
    echo "LibreOffice found - PDF conversion available"
else
    echo "LibreOffice not found - install with: sudo apt install libreoffice"
    echo "Or on macOS/Windows: pip install docx2pdf"
fi

echo ""
echo "Setup complete! Activate with: source venv/bin/activate"

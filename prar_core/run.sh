#!/bin/bash
# run.sh — One-command PRAR deployment
# Usage: ./run.sh

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  PRAR — Persistent Reflective Agent Runtime              ║"
echo "║  Deploying self-modifying agent...                        ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[!] Python 3 not found${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "[✓] Python $PYTHON_VERSION found"

# Create virtual environment if needed
VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "[+] Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Install dependencies
echo "[+] Installing dependencies..."
pip install -q -r requirements.txt

# Check for Ollama
echo ""
echo "[+] Checking Ollama..."
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}[✓] Ollama found${NC}"
    
    # Check if llama3.2 is available
    if ollama list | grep -q "llama3.2"; then
        echo -e "${GREEN}[✓] Model llama3.2 available${NC}"
    else
        echo -e "${YELLOW}[!] Model llama3.2 not found${NC}"
        echo "    Pulling llama3.2 (this may take a few minutes)..."
        ollama pull llama3.2
    fi
else
    echo -e "${YELLOW}[!] Ollama not found${NC}"
    echo "    PRAR will attempt to connect to http://localhost:11434"
    echo "    Install Ollama from: https://ollama.com"
fi

# Create PRAR data directory
PRAR_DIR="$HOME/.prar"
mkdir -p "$PRAR_DIR/memory"
mkdir -p "$PRAR_DIR/tools"

echo ""
echo "[+] PRAR directories:"
echo "    Data: $PRAR_DIR"
echo "    Source: $(pwd)"
echo ""

# Check if already running
PID_FILE="$PRAR_DIR/prar.pid"
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}[!] PRAR already running (PID: $PID)${NC}"
        echo "    Options:"
        echo "      ./run.sh --status    # Check status"
        echo "      ./run.sh --shutdown  # Stop current instance"
        echo ""
        exit 0
    else
        rm "$PID_FILE"
    fi
fi

# Start PRAR
echo -e "${GREEN}[+] Starting PRAR...${NC}"
echo ""
echo "═══════════════════════════════════════════════════════════"
python3 prar.py

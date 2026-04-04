#!/bin/bash
# install_sovereign_api.sh — Install and configure universal inference proxy

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   Sovereign API Proxy — Installation                     ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
python3 --version || { echo "Python 3 not found"; exit 1; }

# Create virtual environment
echo "[1/5] Creating virtual environment..."
cd "$(dirname "$0")"
python3 -m venv venv || { echo "venv creation failed"; exit 1; }

# Activate and install
echo "[2/5] Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Check for API keys
echo ""
echo "[3/5] Checking API keys..."
if [ -z "$KIMI_API_KEY" ]; then
    echo "⚠️  KIMI_API_KEY not set"
    echo "   Get from: https://platform.moonshot.cn/"
    echo "   Set with: export KIMI_API_KEY=sk-..."
fi

if [ -z "$OPENAI_API_KEY" ]; then
    echo "ℹ️  OPENAI_API_KEY not set (optional)"
fi

if [ -z "$GROQ_API_KEY" ]; then
    echo "ℹ️  GROQ_API_KEY not set (optional, fast inference)"
fi

# Create systemd service file (optional)
echo ""
echo "[4/5] Creating systemd service template..."
cat > sovereign-api.service << EOF
[Unit]
Description=Sovereign API Proxy
After=network.target

[Service]
Type=simple
User=%I
WorkingDirectory=$(pwd)
Environment=KIMI_API_KEY=$KIMI_API_KEY
Environment=OPENAI_API_KEY=$OPENAI_API_KEY
Environment=GROQ_API_KEY=$GROQ_API_KEY
Environment=PROXY_PORT=3000
ExecStart=$(pwd)/venv/bin/python $(pwd)/proxy_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo "   Service file: sovereign-api.service"
echo "   Install with: sudo cp sovereign-api.service /etc/systemd/system/"
echo "   Start with:   sudo systemctl start sovereign-api"

# Test configuration
echo ""
echo "[5/5] Testing configuration..."
source venv/bin/activate
python3 -c "import fastapi, uvicorn, httpx; print('✓ All dependencies installed')"

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   Installation Complete!                                  ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo ""
echo "1. Set API keys:"
echo "   export KIMI_API_KEY=sk-..."
echo "   export OPENAI_API_KEY=sk-...  # optional"
echo ""
echo "2. Start the proxy:"
echo "   cd sovereign_api"
echo "   source venv/bin/activate"
echo "   python3 proxy_server.py"
echo ""
echo "3. Test the proxy:"
echo "   curl http://localhost:3000/health"
echo ""
echo "4. Update OpenClaw config (see SOVEREIGN_API_CONFIG.md)"
echo ""
echo "5. (Optional) Install Ollama for local inference:"
echo "   curl -fsSL https://ollama.com/install.sh | sh"
echo "   ollama pull llama3.2"
echo ""

#!/bin/bash
# Run GCE TGM + Visualizer Integration

echo "🜁 GCE Tiny Giant Model — Launcher"
echo "=================================="
echo ""

cd /root/.openclaw/workspace

# Check if bridge is already running
if lsof -i :8080 > /dev/null 2>&1; then
    echo "✓ Bridge already running on port 8080"
else
    echo "[1/3] Starting GCE Bridge..."
    cd gce_tgm
    python3 bridge.py --mode http --port 8080 &
    BRIDGE_PID=$!
    sleep 2
    echo "  ✓ Bridge started (PID: $BRIDGE_PID)"
    cd ..
fi

echo ""
echo "[2/3] Testing inference..."
curl -s -X POST http://localhost:8080/infer \
    -H "Content-Type: application/json" \
    -d '{"text":"Phi spirals encode meaning"}' | python3 -m json.tool 2>/dev/null || echo "  ⚠ Bridge not responding"

echo ""
echo "[3/3] Visualizer ready"
echo "  URL: http://localhost:8080/synesthesia.html"
echo ""
echo "Usage:"
echo "  1. Open browser to the URL above"
echo "  2. Upload audio or use microphone"
echo "  3. Enter text, click 'Run Inference'"
echo "  4. Watch phi-spirals dance"
echo ""
echo "Press Ctrl+C to stop bridge"
echo ""

# Keep running
wait

# GCE Synesthesia Visualizer

WebGL-based audio-reactive geometric visualization.

## Files
- `synesthesia.html` — Main visualizer
- `shaders/` — GLSL phi-spiral shaders (coming)
- `assets/` — Audio samples (coming)

## Usage

1. Open `synesthesia.html` in browser
2. Upload audio file or use microphone
3. Enter text and click "Run Inference"
4. Watch phi-spiral geometry react to audio + GCE state

## Integration with TGM

```bash
# Terminal 1: Start bridge
cd ../gce_tgm
python3 bridge.py --mode http --port 8080

# Browser: Open visualizer
http://localhost:8080/synesthesia.html
```

## Features
- Real-time frequency analysis
- Phi-harmonic spiral rendering
- GCE state visualization
- Audio-reactive particle system
- 60fps WebGL rendering

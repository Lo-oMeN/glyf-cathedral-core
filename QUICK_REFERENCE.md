# Geo-AI Engineering — Quick Reference

## 🚀 Launch TGM + Visualizer
```bash
./run-gce-tgm.sh
# Open http://localhost:8080/synesthesia.html
```

## 🧪 Test TGM
```bash
cd gce_tgm
python3 test_tgm.py        # Run all tests
python3 core.py "text"     # Single inference
```

## 📤 Push to GitHub
```bash
./push-all-repos.sh <token>
```

## 📊 Check Status
```bash
cd memory
python3 memory_manager.py
```

## 🎬 Record Demo
1. `./run-gce-tgm.sh`
2. Open browser to `localhost:8080/synesthesia.html`
3. Upload audio / use mic
4. Enter text, run inference
5. Screen record at 1080p60

## 📁 Key Paths
| File | Path |
|------|------|
| JSON Memory | `memory/comprehensive_state.json` |
| Full Docs | `COMPREHENSIVE_DOCUMENTATION.md` |
| Focus Doc | `GEO_AI_FOCUS.md` |
| TGM Core | `gce_tgm/core.py` |
| Visualizer | `visualizer/synesthesia.html` |

## 🔢 Invariants
- **Phi:** 1.618033988749895
- **PGA:** 16D
- **Manifold:** SO(3,1)
- **Deterministic:** True

## ✅ Done
- TGM: 640 lines, 5/5 tests ✅
- Visualizer: WebGL 60fps ✅
- Bridge: HTTP/WebSocket ✅

## ⏳ Next
1. Record demo video
2. Push repos
3. Resume chronicler

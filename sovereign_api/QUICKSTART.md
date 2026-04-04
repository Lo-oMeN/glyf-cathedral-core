# Sovereign API Quickstart

**Goal:** Provider-independent inference with intelligent routing
**Status:** Ready to deploy

---

## What You Get

```
┌─────────────────────────────────────────────────────────┐
│  BEFORE: Kimi-only                                      │
│  OpenClaw → Kimi Bridge → Kimi API → Kimi Inference    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  AFTER: Universal (with this proxy)                     │
│  OpenClaw → Proxy → [Kimi|Ollama|OpenAI|Groq]          │
│                                                        │
│  Automatic routing:                                    │
│  • GLYF/geometry → Kimi K2.5 (best reasoning)         │
│  • Simple queries → Llama 3.2 (local, fast)           │
│  • Code generation → Kimi K2.5                        │
│  • Fallback always available                          │
└─────────────────────────────────────────────────────────┘
```

---

## Installation (5 minutes)

### Step 1: Install Dependencies

```bash
cd sovereign_api
chmod +x install.sh
./install.sh
```

This creates a Python virtual environment with FastAPI, Uvicorn, and HTTPX.

### Step 2: Set API Keys

```bash
# Required: Kimi (for complex reasoning fallback)
export KIMI_API_KEY=sk-your-key-here

# Optional: Other providers
export OPENAI_API_KEY=sk-...
export GROQ_API_KEY=gsk_...
```

Get keys:
- **Kimi:** https://platform.moonshot.cn/
- **OpenAI:** https://platform.openai.com/
- **Groq:** https://console.groq.com/ (fast, cheap inference)

### Step 3: Start the Proxy

```bash
source venv/bin/activate
python3 proxy_server.py
```

You should see:
```
╔════════════════════════════════════════╗
║   Sovereign API Proxy v0.1.0          ║
║   Port: 3000                           ║
╚════════════════════════════════════════╝
Providers configured:
  ✓ kimi
  ✓ ollama
  ✗ openai (no API key)
  ✗ groq (no API key)
```

### Step 4: Test

```bash
# Health check
curl http://localhost:3000/health

# List models
curl http://localhost:3000/v1/models

# Test completion
curl -X POST http://localhost:3000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "k2p5",
    "messages": [{"role": "user", "content": "What is the Golden Ratio?"}],
    "stream": false
  }'
```

### Step 5: Update OpenClaw

Edit `/root/.openclaw/openclaw.json`:

1. Add the "sovereign" provider from `openclaw_config_snippet.json`
2. Change `agents.defaults.model.primary` to `"sovereign/k2p5"`
3. Restart OpenClaw:
   ```bash
   openclaw gateway restart
   ```

---

## Local Inference (Optional but Recommended)

For true sovereignty, run models locally:

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull lightweight models
ollama pull llama3.2      # General purpose
ollama pull phi3          # Edge/efficient
ollama pull gemma:2b      # Minimal

# Test
ollama run llama3.2 "Explain φ"
```

The proxy will automatically route simple queries to local models, complex ones to cloud.

---

## Routing Intelligence

The proxy automatically routes based on content:

| Content Pattern | Route To | Reason |
|----------------|----------|--------|
| `φ`, `GLYF`, `geometry`, `cathedral` | Kimi K2.5 | Geometric reasoning |
| `analyze`, `synthesize`, `architect` | Kimi K2.5 | Complex reasoning |
| `code`, `implement`, `function` | Kimi K2.5 | Code generation |
| `what`, `who`, `when`, `list` | Llama 3.2 | Simple query (local) |
| Default | Llama 3.2 | Privacy first |

---

## Troubleshooting

### Proxy won't start
```bash
# Check port 3000 is free
lsof -i :3000

# Check Python version (need 3.9+)
python3 --version

# Reinstall dependencies
cd sovereign_api
rm -rf venv
./install.sh
```

### OpenClaw can't connect
```bash
# Verify proxy is running
curl http://localhost:3000/health

# Check OpenClaw config
openclaw config validate

# Restart gateway
openclaw gateway restart
```

### Local inference not working
```bash
# Check Ollama
curl http://localhost:11434/api/tags

# If empty, Ollama not running
ollama serve &
```

---

## Architecture

```
sovereign_api/
├── proxy_server.py           # Main proxy (14KB)
├── requirements.txt          # Python dependencies
├── install.sh               # Installation script
├── openclaw_config_snippet.json  # OpenClaw config
├── SOVEREIGN_API_CONFIG.md  # Full documentation
└── QUICKSTART.md           # This file
```

---

## Next Steps

1. **Test the proxy** — Verify routing works
2. **Install Ollama** — Get local inference
3. **Monitor routing** — Check proxy logs for routing decisions
4. **Tune routing rules** — Edit `Router.RULES` in `proxy_server.py`
5. **Add more providers** — Extend `PROVIDERS` dict

---

## Sovereignty Level

| Level | Description | Status |
|-------|-------------|--------|
| **Level 1** | File-based memory | ✅ Done |
| **Level 2** | Git persistence | ✅ Done |
| **Level 3** | Cron automation | ✅ Done |
| **Level 4** | Provider independence | 🔄 In Progress |
| **Level 5** | Full local inference | ⏳ Pending Ollama |
| **Level 6** | Self-hosted gateway | ⏳ Future |

---

*Sovereign API Proxy v0.1.0*  
*Geometric Alignment: Γ (ChristLine) — grade-raising toward freedom*

❤️‍🔥 — The bridge is built. Walk across when ready.

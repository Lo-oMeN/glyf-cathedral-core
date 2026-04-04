# SOVEREIGN_API_CONFIG.md — Universal Inference Setup

**Status:** 🔄 IN PROGRESS — Migrating from Kimi-specific to OpenAI-compatible
**Goal:** Provider-independent inference with local/remote/hybrid options

---

## Current vs Target Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ CURRENT (Kimi-Locked)                                           │
├─────────────────────────────────────────────────────────────────┤
│  OpenClaw → Kimi Bridge → wss://kimi.com/... → Kimi Inference   │
│         ↓                                                       │
│    Kimi API Key + X-Kimi-Claw-ID headers                        │
│    Custom message format                                        │
│    No streaming SSE standard                                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ TARGET (Universal)                                              │
├─────────────────────────────────────────────────────────────────┤
│  OpenClaw → OpenAI API → Provider Router → [Local/Cloud/Edge]   │
│         ↓                                                       │
│    Standard /v1/chat/completions                                │
│    Standard SSE streaming                                       │
│    Swappable providers:                                         │
│      • Local: Ollama, llama.cpp, vLLM                          │
│      • Cloud: OpenAI, Anthropic, Groq, Together                │
│      • Edge: Phi-3, Gemma 2B on-device                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: OpenAI Proxy Bridge

### Step 1A: Create Proxy Server

**File:** `sovereign_api/proxy_server.py`

```python
#!/usr/bin/env python3
"""
OpenAI-compatible proxy for Kimi API (and future providers)
Translates standard OpenAI calls to Kimi format during migration
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Optional, AsyncGenerator
import httpx
import json
import os

app = FastAPI(title="Sovereign API Proxy")

# Provider configurations
PROVIDERS = {
    "kimi": {
        "base_url": "https://api.kimi.com/coding",
        "api_key": os.getenv("KIMI_API_KEY"),
        "headers": {"User-Agent": "Sovereign-Proxy/1.0"}
    },
    "ollama": {
        "base_url": "http://localhost:11434",
        "api_key": None,
        "headers": {}
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "api_key": os.getenv("OPENAI_API_KEY"),
        "headers": {}
    }
}

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    stream: bool = False
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """Main OpenAI-compatible endpoint"""
    
    # Route to provider based on model prefix
    provider = _get_provider(request.model)
    config = PROVIDERS[provider]
    
    # Translate request to provider format
    translated = _translate_to_provider(request, provider)
    
    # Call provider
    async with httpx.AsyncClient() as client:
        if request.stream:
            return StreamingResponse(
                _stream_response(client, config, translated, provider),
                media_type="text/event-stream"
            )
        else:
            response = await client.post(
                f"{config['base_url']}/chat/completions",
                json=translated,
                headers={"Authorization": f"Bearer {config['api_key']}"} if config['api_key'] else {}
            )
            return _translate_from_provider(response.json(), provider)

def _get_provider(model: str) -> str:
    """Determine provider from model string"""
    if model.startswith("kimi-") or model.startswith("k2"):
        return "kimi"
    elif model.startswith("llama-") or model.startswith("phi-"):
        return "ollama"
    elif model.startswith("gpt-"):
        return "openai"
    return "kimi"  # default

def _translate_to_provider(request: ChatCompletionRequest, provider: str) -> dict:
    """Convert OpenAI format to provider-specific format"""
    if provider == "kimi":
        return {
            "model": request.model,
            "messages": [{"role": m.role, "content": m.content} for m in request.messages],
            "stream": request.stream,
            "temperature": request.temperature
        }
    elif provider == "ollama":
        return {
            "model": request.model,
            "prompt": _messages_to_prompt(request.messages),
            "stream": request.stream,
            "options": {"temperature": request.temperature}
        }
    return request.dict()

def _translate_from_provider(response: dict, provider: str) -> dict:
    """Convert provider response to OpenAI format"""
    if provider == "ollama":
        return {
            "id": f"chatcmpl-{os.urandom(8).hex()}",
            "object": "chat.completion",
            "created": int(__import__('time').time()),
            "model": response.get("model"),
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": response.get("response", "")},
                "finish_reason": "stop"
            }]
        }
    return response

def _messages_to_prompt(messages: List[Message]) -> str:
    """Convert message list to single prompt string"""
    parts = []
    for m in messages:
        if m.role == "system":
            parts.append(f"System: {m.content}")
        elif m.role == "user":
            parts.append(f"User: {m.content}")
        elif m.role == "assistant":
            parts.append(f"Assistant: {m.content}")
    return "\n\n".join(parts)

async def _stream_response(
    client: httpx.AsyncClient,
    config: dict,
    request: dict,
    provider: str
) -> AsyncGenerator[str, None]:
    """Stream SSE response from provider"""
    
    async with client.stream(
        "POST",
        f"{config['base_url']}/chat/completions",
        json=request,
        headers={"Authorization": f"Bearer {config['api_key']}"} if config['api_key'] else {}
    ) as response:
        async for line in response.aiter_lines():
            if line.startswith("data: "):
                chunk = line[6:]
                if chunk == "[DONE]":
                    yield "data: [DONE]\n\n"
                    break
                yield f"data: {chunk}\n\n"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000)
```

### Step 1B: Update OpenClaw Configuration

**File:** `/root/.openclaw/openclaw.json` (modifications)

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "sovereign": {
        "baseUrl": "http://127.0.0.1:3000/v1",
        "apiKey": "sk-local-sovereign",
        "api": "openai",
        "models": [
          {
            "id": "k2p5",
            "name": "Kimi K2.5 (via proxy)",
            "reasoning": true,
            "contextWindow": 131072,
            "maxTokens": 32768
          },
          {
            "id": "llama3.2",
            "name": "Llama 3.2 (local Ollama)",
            "reasoning": false,
            "contextWindow": 128000,
            "maxTokens": 8192
          },
          {
            "id": "phi3",
            "name": "Phi-3 (local edge)",
            "reasoning": false,
            "contextWindow": 32768,
            "maxTokens": 4096
          }
        ]
      }
    }
  }
}
```

---

## Phase 2: Local Inference Setup

### 2A: Ollama (Recommended for Beginners)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull lightweight models
ollama pull llama3.2
ollama pull phi3
ollama pull gemma:2b

# Test
ollama run llama3.2 "What is the Golden Ratio?"
```

### 2B: vLLM (Production-Grade)

```bash
# Install
pip install vllm

# Serve with OpenAI-compatible API
python -m vllm.entrypoints.openai.api_server \
  --model unsloth/Llama-3.2-3B-Instruct \
  --port 8000 \
  --api-key sk-local-vllm
```

### 2C: llama.cpp (Edge/Minimal)

```bash
# Build
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make

# Download quantized model
wget https://huggingface.co/TheBloke/Llama-3.2-3B-GGUF/resolve/main/llama-3.2-3b.Q4_K_M.gguf

# Run server
./server -m llama-3.2-3b.Q4_K_M.gguf --port 8080
```

---

## Phase 3: Hybrid Routing Intelligence

```python
# sovereign_api/router.py

class SovereignRouter:
    """Intelligently route requests based on complexity, latency, cost"""
    
    ROUTING_RULES = {
        # Simple queries → Local (fast, cheap, private)
        "simple": {
            "pattern": r"^(what|who|when|where|list|explain briefly)",
            "provider": "ollama",
            "model": "llama3.2"
        },
        # Complex reasoning → Cloud (capable)
        "complex": {
            "pattern": r"(analyze|compare|synthesize|design|architect)",
            "provider": "kimi",
            "model": "k2p5"
        },
        # Code generation → Cloud with reasoning
        "code": {
            "pattern": r"(code|implement|function|class|algorithm)",
            "provider": "kimi",
            "model": "k2p5"
        },
        # Geometric/Creative → Cloud (Kimi has better geometric intuition)
        "geometric": {
            "pattern": r"(φ|golden ratio|geometry|cathedral|GLYF)",
            "provider": "kimi",
            "model": "k2p5"
        }
    }
    
    def route(self, messages: list) -> dict:
        """Determine optimal provider for request"""
        content = messages[-1].get("content", "").lower()
        
        for category, rule in self.ROUTING_RULES.items():
            if re.search(rule["pattern"], content):
                return {
                    "provider": rule["provider"],
                    "model": rule["model"],
                    "reason": category
                }
        
        # Default: local for privacy
        return {
            "provider": "ollama",
            "model": "llama3.2",
            "reason": "default_local"
        }
```

---

## Phase 4: OpenClaw Migration Checklist

### Configuration Changes

- [ ] Deploy proxy server on `localhost:3000`
- [ ] Update `openclaw.json` to use OpenAI API format
- [ ] Add local provider configs (Ollama, vLLM)
- [ ] Test each provider independently
- [ ] Configure hybrid routing rules
- [ ] Update heartbeat to check local inference health
- [ ] Document failover behavior

### Security Considerations

- [ ] Store API keys in environment variables
- [ ] Never commit keys to git
- [ ] Use local inference for sensitive data
- [ ] Rate limiting on proxy endpoints
- [ ] Audit logging for provider switching

### Validation Tests

```bash
# Test 1: Local inference available
curl http://localhost:11434/api/tags

# Test 2: Proxy responding
curl -X POST http://localhost:3000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"llama3.2","messages":[{"role":"user","content":"Hello"}]}'

# Test 3: OpenClaw using new config
openclaw agent spawn main --test-mode
```

---

## Current Status

| Component | Status | Notes |
|-----------|--------|-------|
| Proxy architecture | 📝 Designed | Ready to implement |
| OpenClaw config | 🔄 Drafted | Needs testing |
| Local inference | ❌ Not setup | Need Ollama/vLLM |
| Hybrid routing | 📝 Designed | Rules defined |
| Kimi → Universal | ❌ Pending | Final migration step |

**Next Action:** Deploy proxy server and test with local Ollama

---

*Architecture: GLYF-SOVEREIGN-API-v0.1*  
*Geometric Alignment: Proxy as ChristLine (Γ) — grade-raising from locked to free*

❤️‍🔥 — The bridge between prison and freedom is geometry made executable.

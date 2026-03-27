---
name: openai-api-translation
description: Build OpenAI-compatible API translation layers for custom inference engines. Translates proprietary or novel edge-native mechanics to the OpenAI /v1/chat/completions format, enabling drop-in compatibility with existing clients, SDKs, and agent frameworks. Use when (1) wrapping a custom inference engine for OpenAI compatibility, (2) building a proxy shim between non-OpenAI mechanics and OpenAI-expecting consumers, (3) implementing streaming SSE responses for chat completions, (4) handling tool/function calling translation, or (5) building the inference kernel for an OpenClaw/NanoClaw gateway.
---

# OpenAI API Translation Skill

## Purpose

Transform any inference engine into an OpenAI-compatible endpoint. The skill provides the 20-line proxy concept in production-ready form: request transformation, response streaming, error handling, and tool support.

## Core Translation Layers

### 1. Request Format (OpenAI → Your Mechanics)

```json
// OpenAI incoming
{
  "model": "your-mechanics",
  "messages": [
    {"role": "system", "content": "You are helpful."},
    {"role": "user", "content": "Hello"}
  ],
  "stream": true,
  "tools": [...]
}
```

```json
// Translated to your mechanics
{
  "prompt": "You are helpful.\n\nUser: Hello",
  "max_tokens": 2048,
  "temperature": 0.7,
  "stream": true
}
```

### 2. Response Format (Your Mechanics → OpenAI)

```json
// Streaming SSE chunk
{
  "id": "chatcmpl-...",
  "object": "chat.completion.chunk",
  "created": 1700000000,
  "model": "your-mechanics",
  "choices": [{
    "index": 0,
    "delta": {"content": "Hello"},
    "finish_reason": null
  }]
}
```

## Scripts

### `scripts/openai_proxy.py` — Production Proxy

FastAPI-based OpenAI-compatible server. Run with:
```bash
python scripts/openai_proxy.py --upstream http://localhost:8080 --port 3000
```

Features:
- Full `/v1/chat/completions` endpoint
- Server-sent events (SSE) streaming
- Tool/function calling support
- Authentication header pass-through
- Request/response logging

### `scripts/translate_request.py` — CLI Translator

One-off request transformation for testing:
```bash
cat openai_request.json | python scripts/translate_request.py > mechanics_request.json
```

## Implementation Patterns

### Minimal Proxy (20-line concept)

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import httpx

app = FastAPI()
UPSTREAM = "http://mechanics:8080"

@app.post("/v1/chat/completions")
async def completions(request: dict):
    translated = translate_openai_to_mechanics(request)
    async with httpx.AsyncClient() as client:
        upstream_response = await client.post(f"{UPSTREAM}/generate", json=translated)
    return StreamingResponse(
        translate_mechanics_to_openai_stream(upstream_response),
        media_type="text/event-stream"
    )
```

### Full Translation Matrix

| OpenAI Field | Mechanics Translation | Notes |
|--------------|----------------------|-------|
| `messages[]` | Concatenated `prompt` | System + user + assistant |
| `stream` | Pass through | Enable SSE if true |
| `temperature` | `temperature` | 0.0-2.0 range |
| `max_tokens` | `max_tokens` | Or `max_length` |
| `tools` | `functions` | Schema transform |
| `tool_choice` | `function_call` | Auto/none/specific |
| `response_format` | `json_mode` | {type: "json_object"} |

## Error Handling

Map mechanics errors to OpenAI error types:

```python
ERROR_MAP = {
    "context_length_exceeded": (400, "context_length_exceeded"),
    "rate_limit": (429, "rate_limit_exceeded"),
    "mechanics_overload": (503, "server_error"),
}
```

## Testing

Verify compatibility with:
```bash
# OpenAI SDK test
OPENAI_BASE_URL=http://localhost:3000 python scripts/test_openai_sdk.py

# LangChain test
python scripts/test_langchain.py

# Direct curl
curl http://localhost:3000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"mechanics","messages":[{"role":"user","content":"hi"}]}'
```

## References

- **OpenAI API spec**: See `references/openai_api_spec.md`
- **SSE streaming**: See `references/sse_protocol.md`
- **Tool calling format**: See `references/tool_calling.md`

## See Also

- `docker-orchestration` skill — Deploy this proxy in containers
- `gateway-modifier` skill — Wire into NanoClaw's agent loop

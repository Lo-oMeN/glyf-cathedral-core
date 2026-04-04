#!/usr/bin/env python3
"""
Sovereign API Proxy v0.1.0
OpenAI-compatible proxy for multi-provider inference

Usage:
    python proxy_server.py
    
Environment:
    KIMI_API_KEY    - Kimi API key
    OPENAI_API_KEY  - OpenAI API key (optional)
    PROXY_PORT      - Port to run proxy (default: 3000)
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional, AsyncGenerator, Union
import httpx
import json
import os
import sys
import re
import asyncio
from datetime import datetime

app = FastAPI(title="Sovereign API Proxy", version="0.1.0")

# Provider configurations
PROVIDERS = {
    "kimi": {
        "base_url": "https://api.kimi.com/coding",
        "api_key": os.getenv("KIMI_API_KEY", ""),
        "headers": {"User-Agent": "Sovereign-Proxy/1.0"},
        "format": "kimi"  # Custom format
    },
    "ollama": {
        "base_url": os.getenv("OLLAMA_URL", "http://localhost:11434"),
        "api_key": None,
        "headers": {},
        "format": "ollama"
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "headers": {},
        "format": "openai"
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "api_key": os.getenv("GROQ_API_KEY", ""),
        "headers": {},
        "format": "openai"
    }
}

# Model → Provider mapping
MODEL_MAP = {
    # Kimi models
    "k2p5": ("kimi", "k2p5"),
    "kimi-k2p5": ("kimi", "k2p5"),
    
    # Ollama models (local)
    "llama3.2": ("ollama", "llama3.2"),
    "llama3.1": ("ollama", "llama3.1"),
    "phi3": ("ollama", "phi3"),
    "gemma:2b": ("ollama", "gemma:2b"),
    "qwen2.5": ("ollama", "qwen2.5"),
    
    # OpenAI models
    "gpt-4o": ("openai", "gpt-4o"),
    "gpt-4o-mini": ("openai", "gpt-4o-mini"),
    
    # Groq models (fast inference)
    "llama-3.2-90b": ("groq", "llama-3.2-90b-vision-preview"),
    "llama-3.1-70b": ("groq", "llama-3.1-70b-versatile"),
    "mixtral-8x7b": ("groq", "mixtral-8x7b-32768"),
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
    top_p: Optional[float] = 1.0
    frequency_penalty: Optional[float] = 0.0
    presence_penalty: Optional[float] = 0.0

class Router:
    """Intelligent request routing based on content analysis"""
    
    RULES = [
        # (pattern, provider, model, reason)
        (r"\b(φ|phi|golden ratio|geometry|cathedral|GLYF|∿|│|∠|⧖|꩜|●|▥)\b", "kimi", "k2p5", "geometric_reasoning"),
        (r"\b(analyze|synthesize|architect|design pattern|formal proof)\b", "kimi", "k2p5", "complex_reasoning"),
        (r"\b(code|implement|function|class|algorithm|refactor|debug)\b", "kimi", "k2p5", "code_generation"),
        (r"\b(what|who|when|where|list|briefly|quick)\b", "ollama", "llama3.2", "simple_query"),
    ]
    
    @classmethod
    def route(cls, messages: List[Message], requested_model: str) -> tuple:
        """Determine optimal provider and model"""
        
        # If specific model requested, use it
        if requested_model in MODEL_MAP:
            provider, model = MODEL_MAP[requested_model]
            return provider, model, "explicit"
        
        # Analyze content for routing
        content = " ".join([m.content for m in messages[-3:]]).lower()  # Last 3 messages
        
        for pattern, provider, model, reason in cls.RULES:
            if re.search(pattern, content):
                return provider, model, reason
        
        # Default: try local first, fallback to cloud
        return "ollama", "llama3.2", "default_local"

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "providers": {
            name: {
                "available": bool(config["api_key"]) if name != "ollama" else True,
                "format": config["format"]
            }
            for name, config in PROVIDERS.items()
        }
    }

@app.get("/v1/models")
async def list_models():
    """List available models"""
    models = []
    for model_id, (provider, actual_name) in MODEL_MAP.items():
        models.append({
            "id": model_id,
            "object": "model",
            "created": int(datetime.now().timestamp()),
            "owned_by": provider
        })
    return {"object": "list", "data": models}

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """Main OpenAI-compatible chat completion endpoint"""
    
    # Route to provider
    provider, model, reason = Router.route(request.messages, request.model)
    config = PROVIDERS.get(provider)
    
    if not config:
        raise HTTPException(status_code=400, detail=f"Unknown provider: {provider}")
    
    if provider != "ollama" and not config["api_key"]:
        raise HTTPException(
            status_code=503, 
            detail=f"Provider {provider} not configured (missing API key)"
        )
    
    print(f"[Router] {request.model} → {provider}/{model} (reason: {reason})")
    
    # Translate request
    translated = translate_to_provider(request, provider, model)
    
    # Call provider
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            if request.stream:
                return StreamingResponse(
                    stream_response(client, config, translated, provider, model),
                    media_type="text/event-stream",
                    headers={"X-Routing-Reason": reason}
                )
            else:
                response = await call_provider(client, config, translated, provider)
                translated_response = translate_from_provider(response, provider, model)
                translated_response["routing"] = {"provider": provider, "model": model, "reason": reason}
                return translated_response
    
    except httpx.ConnectError as e:
        if provider == "ollama":
            # Fallback to Kimi if local unavailable
            print(f"[Fallback] Ollama unavailable, routing to Kimi")
            return await fallback_to_kimi(request, reason="local_unavailable")
        raise HTTPException(status_code=503, detail=f"Provider connection failed: {e}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {e}")

def translate_to_provider(request: ChatCompletionRequest, provider: str, model: str) -> dict:
    """Convert OpenAI format to provider-specific format"""
    
    if provider == "kimi":
        return {
            "model": model,
            "messages": [{"role": m.role, "content": m.content} for m in request.messages],
            "stream": request.stream,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens
        }
    
    elif provider == "ollama":
        # Ollama uses different format
        prompt = messages_to_prompt(request.messages)
        return {
            "model": model,
            "prompt": prompt,
            "stream": request.stream,
            "options": {
                "temperature": request.temperature,
                "num_predict": request.max_tokens or 2048
            }
        }
    
    elif provider in ["openai", "groq"]:
        # These are already OpenAI-compatible
        return {
            "model": model,
            "messages": [{"role": m.role, "content": m.content} for m in request.messages],
            "stream": request.stream,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "top_p": request.top_p
        }
    
    return request.dict()

def translate_from_provider(response: dict, provider: str, model: str) -> dict:
    """Convert provider response to OpenAI format"""
    
    if provider == "ollama":
        # Ollama returns different format
        return {
            "id": f"chatcmpl-{os.urandom(8).hex()}",
            "object": "chat.completion",
            "created": int(datetime.now().timestamp()),
            "model": model,
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": response.get("response", "")},
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": response.get("prompt_eval_count", 0),
                "completion_tokens": response.get("eval_count", 0),
                "total_tokens": response.get("prompt_eval_count", 0) + response.get("eval_count", 0)
            }
        }
    
    # Kimi, OpenAI, Groq already return OpenAI format
    return response

async def call_provider(client: httpx.AsyncClient, config: dict, request: dict, provider: str) -> dict:
    """Make non-streaming request to provider"""
    
    headers = dict(config["headers"])
    if config["api_key"]:
        headers["Authorization"] = f"Bearer {config['api_key']}"
    
    if provider == "ollama":
        url = f"{config['base_url']}/api/generate"
    else:
        url = f"{config['base_url']}/chat/completions"
    
    response = await client.post(url, json=request, headers=headers)
    response.raise_for_status()
    return response.json()

async def stream_response(
    client: httpx.AsyncClient,
    config: dict,
    request: dict,
    provider: str,
    model: str
) -> AsyncGenerator[str, None]:
    """Stream SSE response from provider"""
    
    headers = dict(config["headers"])
    if config["api_key"]:
        headers["Authorization"] = f"Bearer {config['api_key']}"
    
    if provider == "ollama":
        url = f"{config['base_url']}/api/generate"
    else:
        url = f"{config['base_url']}/chat/completions"
    
    async with client.stream("POST", url, json=request, headers=headers) as response:
        response.raise_for_status()
        
        if provider == "ollama":
            # Ollama streaming format
            async for line in response.aiter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        chunk = data.get("response", "")
                        if chunk:
                            openai_chunk = {
                                "id": f"chatcmpl-{os.urandom(8).hex()}",
                                "object": "chat.completion.chunk",
                                "created": int(datetime.now().timestamp()),
                                "model": model,
                                "choices": [{
                                    "index": 0,
                                    "delta": {"content": chunk},
                                    "finish_reason": None
                                }]
                            }
                            yield f"data: {json.dumps(openai_chunk)}\n\n"
                        
                        if data.get("done"):
                            yield "data: [DONE]\n\n"
                            break
                    except json.JSONDecodeError:
                        continue
        else:
            # Standard SSE format
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    chunk = line[6:]
                    if chunk == "[DONE]":
                        yield "data: [DONE]\n\n"
                        break
                    yield f"data: {chunk}\n\n"

async def fallback_to_kimi(request: ChatCompletionRequest, reason: str):
    """Fallback to Kimi when local inference unavailable"""
    config = PROVIDERS["kimi"]
    
    if not config["api_key"]:
        raise HTTPException(status_code=503, detail="Fallback failed: Kimi not configured")
    
    translated = translate_to_provider(request, "kimi", "k2p5")
    
    async with httpx.AsyncClient(timeout=300.0) as client:
        if request.stream:
            return StreamingResponse(
                stream_response(client, config, translated, "kimi", "k2p5"),
                media_type="text/event-stream",
                headers={"X-Routing-Reason": f"fallback:{reason}"}
            )
        else:
            response = await call_provider(client, config, translated, "kimi")
            translated_response = translate_from_provider(response, "kimi", "k2p5")
            translated_response["routing"] = {"provider": "kimi", "model": "k2p5", "reason": f"fallback:{reason}"}
            return translated_response

def messages_to_prompt(messages: List[Message]) -> str:
    """Convert message list to single prompt string for Ollama"""
    parts = []
    for m in messages:
        if m.role == "system":
            parts.append(f"System: {m.content}")
        elif m.role == "user":
            parts.append(f"User: {m.content}")
        elif m.role == "assistant":
            parts.append(f"Assistant: {m.content}")
    return "\n\n".join(parts)

@app.get("/")
async def root():
    """Root endpoint with usage info"""
    return {
        "name": "Sovereign API Proxy",
        "version": "0.1.0",
        "endpoints": {
            "/health": "Health check",
            "/v1/models": "List available models",
            "/v1/chat/completions": "Chat completions (OpenAI-compatible)"
        },
        "providers": list(PROVIDERS.keys()),
        "models": list(MODEL_MAP.keys()),
        "routing": "Automatic based on content analysis"
    }

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PROXY_PORT", "3000"))
    
    print(f"╔════════════════════════════════════════╗")
    print(f"║   Sovereign API Proxy v0.1.0          ║")
    print(f"║   Port: {port}                          ║")
    print(f"╚════════════════════════════════════════╝")
    print(f"")
    print(f"Providers configured:")
    for name, config in PROVIDERS.items():
        status = "✓" if (name == "ollama" or config["api_key"]) else "✗"
        print(f"  {status} {name}")
    print(f"")
    print(f"Ready for OpenAI-compatible requests")
    
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")

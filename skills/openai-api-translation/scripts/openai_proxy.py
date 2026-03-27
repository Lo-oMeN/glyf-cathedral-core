#!/usr/bin/env python3
"""
OpenAI-compatible API proxy for custom inference engines.
Translates OpenAI /v1/chat/completions to your mechanics' native format.

Usage:
    python openai_proxy.py --upstream http://localhost:8080 --port 3000

Environment variables:
    UPSTREAM_URL: URL of your mechanics inference server
    PROXY_PORT: Port to run the proxy on (default: 3000)
    LOG_LEVEL: DEBUG/INFO/WARNING/ERROR (default: INFO)
"""

import json
import time
import uuid
import argparse
import os
from typing import AsyncGenerator, Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
import httpx
import uvicorn

app = FastAPI(title="OpenAI API Translation Proxy")

# Configuration
UPSTREAM_URL: str = ""

def generate_id() -> str:
    """Generate OpenAI-style completion ID."""
    return f"chatcmpl-{uuid.uuid4().hex[:24]}"

def translate_openai_to_mechanics(request: dict) -> dict:
    """
    Transform OpenAI request format to mechanics-native format.
    
    Handles:
    - Message concatenation into prompt
    - Temperature/max_tokens passthrough
    - Tool conversion to function format
    - Streaming flag preservation
    """
    messages = request.get("messages", [])
    
    # Concatenate messages into prompt
    prompt_parts = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role == "system":
            prompt_parts.append(f"System: {content}")
        elif role == "user":
            prompt_parts.append(f"User: {content}")
        elif role == "assistant":
            prompt_parts.append(f"Assistant: {content}")
    
    prompt = "\n\n".join(prompt_parts)
    
    mechanics_request = {
        "prompt": prompt,
        "max_tokens": request.get("max_tokens", 2048),
        "temperature": request.get("temperature", 0.7),
        "stream": request.get("stream", False),
    }
    
    # Handle tools -> functions translation
    tools = request.get("tools")
    if tools:
        mechanics_request["functions"] = [
            {
                "name": tool["function"]["name"],
                "description": tool["function"].get("description", ""),
                "parameters": tool["function"].get("parameters", {})
            }
            for tool in tools
        ]
    
    # Handle tool_choice
    tool_choice = request.get("tool_choice")
    if tool_choice:
        if tool_choice == "auto":
            mechanics_request["function_call"] = "auto"
        elif tool_choice == "none":
            mechanics_request["function_call"] = "none"
        elif isinstance(tool_choice, dict):
            mechanics_request["function_call"] = tool_choice.get("function", {}).get("name")
    
    return mechanics_request

async def translate_mechanics_to_openai_stream(
    response: httpx.Response,
    model: str,
    completion_id: str
) -> AsyncGenerator[str, None]:
    """
    Stream mechanics response as OpenAI SSE format.
    
    Yields: data: {...}\n\n formatted chunks
    """
    created = int(time.time())
    
    async for line in response.aiter_lines():
        if not line:
            continue
            
        try:
            # Parse mechanics response chunk
            chunk = json.loads(line)
            
            # Extract content from various mechanics formats
            delta_content = ""
            if "text" in chunk:
                delta_content = chunk["text"]
            elif "content" in chunk:
                delta_content = chunk["content"]
            elif "token" in chunk:
                delta_content = chunk["token"]
            elif "delta" in chunk:
                delta_content = chunk["delta"]
            
            # Check for finish
            finish_reason = None
            if chunk.get("finish_reason") or chunk.get("done"):
                finish_reason = "stop"
            
            # Build OpenAI chunk
            openai_chunk = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": created,
                "model": model,
                "choices": [{
                    "index": 0,
                    "delta": {"content": delta_content} if delta_content else {},
                    "finish_reason": finish_reason
                }]
            }
            
            yield f"data: {json.dumps(openai_chunk)}\n\n"
            
            if finish_reason:
                yield "data: [DONE]\n\n"
                
        except json.JSONDecodeError:
            # Skip non-JSON lines
            continue

async def translate_mechanics_to_openai_response(
    mechanics_response: dict,
    model: str,
    completion_id: str
) -> dict:
    """
    Convert mechanics non-streaming response to OpenAI format.
    """
    created = int(time.time())
    
    # Extract content
    content = ""
    if "text" in mechanics_response:
        content = mechanics_response["text"]
    elif "content" in mechanics_response:
        content = mechanics_response["content"]
    elif "response" in mechanics_response:
        content = mechanics_response["response"]
    elif "output" in mechanics_response:
        content = mechanics_response["output"]
    elif "generated_text" in mechanics_response:
        content = mechanics_response["generated_text"]
    
    return {
        "id": completion_id,
        "object": "chat.completion",
        "created": created,
        "model": model,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": content
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": mechanics_response.get("prompt_tokens", -1),
            "completion_tokens": mechanics_response.get("completion_tokens", -1),
            "total_tokens": mechanics_response.get("total_tokens", -1)
        }
    }

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    """Main OpenAI-compatible completions endpoint."""
    try:
        body = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    model = body.get("model", "unknown")
    stream = body.get("stream", False)
    completion_id = generate_id()
    
    # Translate request
    mechanics_request = translate_openai_to_mechanics(body)
    
    # Forward to upstream
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            if stream:
                # Streaming response
                upstream_response = await client.post(
                    f"{UPSTREAM_URL}/generate",
                    json=mechanics_request,
                    headers={"Accept": "text/event-stream"}
                )
                upstream_response.raise_for_status()
                
                return StreamingResponse(
                    translate_mechanics_to_openai_stream(upstream_response, model, completion_id),
                    media_type="text/event-stream",
                    headers={
                        "Cache-Control": "no-cache",
                        "Connection": "keep-alive",
                    }
                )
            else:
                # Non-streaming response
                upstream_response = await client.post(
                    f"{UPSTREAM_URL}/generate",
                    json=mechanics_request
                )
                upstream_response.raise_for_status()
                mechanics_response = upstream_response.json()
                
                openai_response = await translate_mechanics_to_openai_response(
                    mechanics_response, model, completion_id
                )
                return JSONResponse(content=openai_response)
                
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Mechanics server unavailable")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Mechanics request timeout")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Mechanics error: {e.response.text}")

@app.get("/v1/models")
async def list_models():
    """List available models (OpenAI-compatible)."""
    return {
        "object": "list",
        "data": [
            {
                "id": "your-mechanics",
                "object": "model",
                "created": 1700000000,
                "owned_by": "local"
            }
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{UPSTREAM_URL}/health")
            mechanics_healthy = response.status_code == 200
    except:
        mechanics_healthy = False
    
    return {
        "status": "healthy" if mechanics_healthy else "degraded",
        "proxy": "healthy",
        "mechanics": "healthy" if mechanics_healthy else "unavailable",
        "upstream": UPSTREAM_URL
    }

def main():
    parser = argparse.ArgumentParser(description="OpenAI API Translation Proxy")
    parser.add_argument("--upstream", default=os.getenv("UPSTREAM_URL", "http://localhost:8080"),
                        help="URL of mechanics inference server")
    parser.add_argument("--port", type=int, default=int(os.getenv("PROXY_PORT", "3000")),
                        help="Port to run proxy on")
    parser.add_argument("--host", default="0.0.0.0",
                        help="Host to bind to")
    
    args = parser.parse_args()
    
    global UPSTREAM_URL
    UPSTREAM_URL = args.upstream
    
    print(f"Starting OpenAI API Proxy")
    print(f"  Upstream: {UPSTREAM_URL}")
    print(f"  Listening: {args.host}:{args.port}")
    print(f"  OpenAI endpoint: http://{args.host}:{args.port}/v1/chat/completions")
    
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")

if __name__ == "__main__":
    main()

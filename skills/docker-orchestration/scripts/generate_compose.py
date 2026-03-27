#!/usr/bin/env python3
"""
Generate production-ready docker-compose.yml for the cathedral stack.

Usage:
    python generate_compose.py --env-file .env --output docker-compose.yml
    
Environment variables (from .env):
    MECHANICS_URL: Upstream mechanics endpoint
    INFERENCE_PROVIDER: local-mechanics | ollama | anthropic
    GATEWAY_PORT: Port for gateway HTTP
    OPENAI_API_PORT: Port for OpenAI-compatible API
    WEBUI_PORT: Port for dashboard
    ENABLE_WEBUI: true | false
"""

import argparse
import os
import sys
from typing import Dict, Any

COMPOSE_TEMPLATE = '''version: '3.8'

services:
  # Layer 1: Inference Kernel
  mechanics:
    image: {{{MECHANICS_IMAGE}}}
    container_name: cathedral-mechanics
    networks:
      - cathedral-net
    volumes:
      - mechanics-data:/data
      - mechanics-models:/models
    environment:
      - MODEL_PATH=/models
      - MAX_BATCH_SIZE=1
      - DEVICE={{{MECHANICS_DEVICE}}}
    deploy:
      resources:
        limits:
          cpus: '{{{MECHANICS_CPU_LIMIT}}}'
          memory: {{{MECHANICS_MEM_LIMIT}}}
        reservations:
          cpus: '{{{MECHANICS_CPU_RESERVE}}}'
          memory: {{{MECHANICS_MEM_RESERVE}}}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true

  # Layer 2: Agent Gateway
  gateway:
    image: {{{GATEWAY_IMAGE}}}
    container_name: cathedral-gateway
    networks:
      - cathedral-net
    ports:
      - "{{{OPENAI_API_PORT}}}:3000"
      - "{{{GATEWAY_PORT}}}:8080"
    volumes:
      - gateway-memory:/app/memory
      - gateway-config:/app/config
      - ./.env:/app/.env:ro
    environment:
      - NODE_ENV=production
      - MECHANICS_URL={{{MECHANICS_URL}}}
      - INFERENCE_PROVIDER={{{INFERENCE_PROVIDER}}}
      - MEMORY_PATH=/app/memory
      - GATEWAY_PORT=8080
      - OPENAI_API_PORT=3000
    depends_on:
      mechanics:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true

  # Layer 3: Web UI (optional)
  {{{WEBUI_SERVICE}}}

networks:
  cathedral-net:
    driver: bridge
    internal: false

volumes:
  mechanics-data:
    driver: local
  mechanics-models:
    driver: local
  gateway-memory:
    driver: local
  gateway-config:
    driver: local
  {{{WEBUI_VOLUME}}}
'''

WEBUI_SERVICE_TEMPLATE = '''webui:
    image: {{{WEBUI_IMAGE}}}
    container_name: cathedral-ui
    networks:
      - cathedral-net
    ports:
      - "{{{WEBUI_PORT}}}:3000"
    environment:
      - GATEWAY_URL=http://gateway:8080
      - API_KEY={{{DASHBOARD_API_KEY}}}
      - NODE_ENV=production
    depends_on:
      - gateway
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
'''

def load_env(env_file: str) -> Dict[str, str]:
    """Load environment variables from .env file."""
    env = {}
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env[key] = value
    return env

def generate_compose(args) -> str:
    """Generate docker-compose.yml content."""
    env = load_env(args.env_file)
    
    # Default values
    config = {
        'MECHANICS_IMAGE': args.mechanics_image or env.get('MECHANICS_IMAGE', 'your-mechanics:latest'),
        'GATEWAY_IMAGE': args.gateway_image or env.get('GATEWAY_IMAGE', 'nanoclaw:latest'),
        'WEBUI_IMAGE': args.webui_image or env.get('WEBUI_IMAGE', 'cathedral-ui:latest'),
        'MECHANICS_URL': args.mechanics_url or env.get('MECHANICS_URL', 'http://mechanics:8080'),
        'INFERENCE_PROVIDER': env.get('INFERENCE_PROVIDER', 'local-mechanics'),
        'GATEWAY_PORT': env.get('GATEWAY_PORT', '8080'),
        'OPENAI_API_PORT': env.get('OPENAI_API_PORT', '3000'),
        'WEBUI_PORT': env.get('WEBUI_PORT', '80'),
        'DASHBOARD_API_KEY': env.get('DASHBOARD_API_KEY', 'change-me-in-production'),
        'MECHANICS_DEVICE': env.get('MECHANICS_DEVICE', 'cpu'),
        'MECHANICS_CPU_LIMIT': env.get('MECHANICS_CPU_LIMIT', '2.0'),
        'MECHANICS_MEM_LIMIT': env.get('MECHANICS_MEM_LIMIT', '4G'),
        'MECHANICS_CPU_RESERVE': env.get('MECHANICS_CPU_RESERVE', '1.0'),
        'MECHANICS_MEM_RESERVE': env.get('MECHANICS_MEM_RESERVE', '2G'),
    }
    
    # Handle webui option
    enable_webui = args.with_webui if args.with_webui is not None else env.get('ENABLE_WEBUI', 'true').lower() == 'true'
    
    if enable_webui:
        config['WEBUI_SERVICE'] = WEBUI_SERVICE_TEMPLATE
        config['WEBUI_VOLUME'] = 'webui-assets:\n    driver: local'
        for key in ['WEBUI_IMAGE', 'WEBUI_PORT', 'DASHBOARD_API_KEY']:
            config['WEBUI_SERVICE'] = config['WEBUI_SERVICE'].replace(f'{{{{{key}}}}}', config[key])
    else:
        config['WEBUI_SERVICE'] = '# Web UI disabled'
        config['WEBUI_VOLUME'] = ''
    
    # Replace all placeholders
    compose = COMPOSE_TEMPLATE
    for key, value in config.items():
        compose = compose.replace(f'{{{{{key}}}}}', value)
    
    return compose

def main():
    parser = argparse.ArgumentParser(description='Generate cathedral docker-compose.yml')
    parser.add_argument('--env-file', default='.env', help='Path to .env file')
    parser.add_argument('--output', '-o', default='docker-compose.yml', help='Output file')
    parser.add_argument('--mechanics-image', help='Mechanics Docker image')
    parser.add_argument('--gateway-image', help='Gateway Docker image')
    parser.add_argument('--webui-image', help='WebUI Docker image')
    parser.add_argument('--mechanics-url', help='Mechanics URL')
    parser.add_argument('--with-webui', action='store_true', dest='with_webui', help='Enable WebUI')
    parser.add_argument('--without-webui', action='store_false', dest='with_webui', help='Disable WebUI')
    
    args = parser.parse_args()
    
    compose = generate_compose(args)
    
    with open(args.output, 'w') as f:
        f.write(compose)
    
    print(f"✓ Generated {args.output}")
    print(f"  Mechanics: {args.mechanics_image or 'from env'}")
    print(f"  Gateway: {args.gateway_image or 'from env'}")
    print(f"  WebUI: {'enabled' if args.with_webui else 'disabled'}")

if __name__ == '__main__':
    main()

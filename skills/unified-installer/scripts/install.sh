#!/bin/bash
#
# Cathedral Unified Installer
# One-command setup for the complete sovereign agent stack
# Usage: curl -fsSL https://cathedral.ai/install.sh | bash

set -e

VERSION="0.1.0"
WORKDIR="${HOME}/.cathedral"
REPOS_DIR="$WORKDIR/repos"
COMPOSE_FILE="$WORKDIR/docker-compose.yml"
ENV_FILE="$WORKDIR/.env"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}ℹ${NC} $1"; }
log_success() { echo -e "${GREEN}✓${NC} $1"; }
log_warn() { echo -e "${YELLOW}⚠${NC} $1"; }
log_error() { echo -e "${RED}❌${NC} $1"; }

print_banner() {
  echo ""
  echo "╔════════════════════════════════════════╗"
  echo "║      🏛️  CATHEDRAL INSTALLER v$VERSION     ║"
  echo "║   Sovereign Agent Stack - Edge Native  ║"
  echo "╚════════════════════════════════════════╝"
  echo ""
}

detect_os() {
  if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
  else
    log_error "Unsupported OS: $OSTYPE"
    exit 1
  fi
  
  ARCH=$(uname -m)
  log_info "Detected: $OS ($ARCH)"
}

check_prerequisites() {
  log_info "Checking prerequisites..."
  
  # Docker
  if ! command -v docker &> /dev/null; then
    log_error "Docker is required but not installed"
    echo "   Install: https://docs.docker.com/get-docker/"
    exit 1
  fi
  log_success "Docker found"
  
  # Docker Compose
  if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
  elif docker-compose version &> /dev/null; then
    COMPOSE_CMD="docker-compose"
  else
    log_error "Docker Compose is required"
    exit 1
  fi
  log_success "Docker Compose found ($COMPOSE_CMD)"
  
  # Git
  if ! command -v git &> /dev/null; then
    log_warn "Git not found — will use curl for downloads"
    HAS_GIT=false
  else
    HAS_GIT=true
    log_success "Git found"
  fi
  
  # curl
  if ! command -v curl &> /dev/null; then
    log_error "curl is required"
    exit 1
  fi
}

detect_mechanics() {
  log_info "Detecting inference mechanics..."
  
  # Check for local mechanics
  if curl -s http://localhost:8080/health &> /dev/null; then
    log_success "Edge-native mechanics detected at :8080"
    MECHANICS_URL="http://mechanics:8080"
    INFERENCE_PROVIDER="local-mechanics"
    EDGE_NATIVE=true
    return
  fi
  
  # Check for Ollama
  if curl -s http://localhost:11434/api/tags &> /dev/null; then
    log_success "Ollama detected at :11434"
    MECHANICS_URL="http://ollama:11434"
    INFERENCE_PROVIDER="ollama"
    EDGE_NATIVE=false
    return
  fi
  
  # Default to Ollama container
  log_warn "No local mechanics detected — will deploy Ollama"
  MECHANICS_URL="http://ollama:11434"
  INFERENCE_PROVIDER="ollama"
  EDGE_NATIVE=false
}

setup_directories() {
  log_info "Setting up directories..."
  
  mkdir -p "$WORKDIR"/{memory,models,config}
  cd "$WORKDIR"
  
  log_success "Working directory: $WORKDIR"
}

generate_env() {
  log_info "Generating configuration..."
  
  # Generate secrets
  DASHBOARD_API_KEY=$(openssl rand -hex 32 2>/dev/null || head -c 64 /dev/urandom | xxd -p | tr -d '\n')
  JWT_SECRET=$(openssl rand -hex 32 2>/dev/null || head -c 64 /dev/urandom | xxd -p | tr -d '\n')
  
  cat > "$ENV_FILE" << EOF
# Cathedral Configuration
# Generated: $(date)

# Environment
NODE_ENV=production
COMPOSE_PROJECT_NAME=cathedral

# Inference Configuration
MECHANICS_URL=${MECHANICS_URL}
INFERENCE_PROVIDER=${INFERENCE_PROVIDER}
OLLAMA_URL=http://ollama:11434

# Gateway Configuration
GATEWAY_PORT=8080
OPENAI_API_PORT=3000
WEBUI_PORT=80

# Security
DASHBOARD_API_KEY=${DASHBOARD_API_KEY}
JWT_SECRET=${JWT_SECRET}

# Persistence
MEMORY_PATH=/app/memory
MODELS_PATH=/models

# Feature Flags
ENABLE_WEBUI=true
ENABLE_TELEGRAM=false
ENABLE_DISCORD=false

# Edge Native
EDGE_NATIVE=${EDGE_NATIVE}
EOF

  log_success "Configuration saved to .env"
}

generate_compose() {
  log_info "Generating docker-compose.yml..."
  
  # Download or generate compose file
  if [ "$EDGE_NATIVE" = true ]; then
    # Edge-native: mechanics is external, only gateway + ui
    cat > "$COMPOSE_FILE" << 'EOF'
version: '3.8'

services:
  gateway:
    image: ghcr.io/cathedral-ai/gateway:latest
    container_name: cathedral-gateway
    networks:
      - cathedral-net
    ports:
      - "${OPENAI_API_PORT:-3000}:3000"
      - "${GATEWAY_PORT:-8080}:8080"
    volumes:
      - ./memory:/app/memory
      - ./.env:/app/.env:ro
    environment:
      - NODE_ENV=production
      - MECHANICS_URL=${MECHANICS_URL}
      - INFERENCE_PROVIDER=${INFERENCE_PROVIDER}
    extra_hosts:
      - "host.docker.internal:host-gateway"
    restart: unless-stopped

  webui:
    image: ghcr.io/cathedral-ai/webui:latest
    container_name: cathedral-ui
    networks:
      - cathedral-net
    ports:
      - "${WEBUI_PORT:-80}:3000"
    environment:
      - GATEWAY_URL=http://gateway:8080
      - API_KEY=${DASHBOARD_API_KEY}
    depends_on:
      - gateway
    restart: unless-stopped

networks:
  cathedral-net:
    driver: bridge
EOF
  else
    # With Ollama: full stack
    cat > "$COMPOSE_FILE" << 'EOF'
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: cathedral-ollama
    networks:
      - cathedral-net
    volumes:
      - ./models:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
    restart: unless-stopped

  gateway:
    image: ghcr.io/cathedral-ai/gateway:latest
    container_name: cathedral-gateway
    networks:
      - cathedral-net
    ports:
      - "${OPENAI_API_PORT:-3000}:3000"
      - "${GATEWAY_PORT:-8080}:8080"
    volumes:
      - ./memory:/app/memory
      - ./.env:/app/.env:ro
    environment:
      - NODE_ENV=production
      - MECHANICS_URL=${MECHANICS_URL}
      - INFERENCE_PROVIDER=${INFERENCE_PROVIDER}
    depends_on:
      - ollama
    restart: unless-stopped

  webui:
    image: ghcr.io/cathedral-ai/webui:latest
    container_name: cathedral-ui
    networks:
      - cathedral-net
    ports:
      - "${WEBUI_PORT:-80}:3000"
    environment:
      - GATEWAY_URL=http://gateway:8080
      - API_KEY=${DASHBOARD_API_KEY}
    depends_on:
      - gateway
    restart: unless-stopped

networks:
  cathedral-net:
    driver: bridge
EOF
  fi

  log_success "Docker Compose configuration created"
}

deploy() {
  log_info "Deploying cathedral..."
  
  cd "$WORKDIR"
  
  # Pull images
  $COMPOSE_CMD pull
  
  # Start stack
  $COMPOSE_CMD up -d
  
  # Wait for startup
  log_info "Waiting for services to start..."
  sleep 10
  
  # Health check
  log_info "Checking service health..."
  
  GATEWAY_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:${GATEWAY_PORT:-8080}/health 2>/dev/null || echo "000")
  
  if [ "$GATEWAY_HEALTH" = "200" ]; then
    log_success "Gateway is healthy"
  else
    log_warn "Gateway not responding yet (HTTP $GATEWAY_HEALTH)"
    log_info "It may still be starting — check logs with: docker compose logs -f"
  fi
}

print_summary() {
  source "$ENV_FILE"
  
  echo ""
  echo "╔════════════════════════════════════════╗"
  echo "║       🎉 INSTALLATION COMPLETE         ║"
  echo "╚════════════════════════════════════════╝"
  echo ""
  echo "📊 Access Points:"
  echo "   Gateway:    http://localhost:${GATEWAY_PORT:-8080}"
  echo "   OpenAI API: http://localhost:${OPENAI_API_PORT:-3000}/v1"
  echo "   Dashboard:  http://localhost:${WEBUI_PORT:-80}"
  echo ""
  echo "🔑 Credentials:"
  echo "   Dashboard API Key: ${DASHBOARD_API_KEY:0:16}..."
  echo "   (Full key in: $ENV_FILE)"
  echo ""
  echo "📁 Installation Directory: $WORKDIR"
  echo ""
  echo "🛠️  Useful Commands:"
  echo "   cd $WORKDIR"
  echo "   docker compose logs -f    # View logs"
  echo "   docker compose down       # Stop stack"
  echo "   docker compose restart    # Restart"
  echo ""
  echo "🌐 Edge Native: ${EDGE_NATIVE}"
  echo "   Inference: ${INFERENCE_PROVIDER}"
  echo ""
  
  if [ "$EDGE_NATIVE" = true ]; then
    echo "⚡ Your local mechanics are being used as the inference engine."
    echo "   All agents route to your edge-native implementation."
  else
    echo "🦙 Ollama is providing inference."
    echo "   Pull a model: docker exec -it cathedral-ollama ollama pull llama2"
  fi
  
  echo ""
  log_success "Cathedral is ready."
}

main() {
  print_banner
  detect_os
  check_prerequisites
  detect_mechanics
  setup_directories
  generate_env
  generate_compose
  deploy
  print_summary
}

# Run main function
main "$@"

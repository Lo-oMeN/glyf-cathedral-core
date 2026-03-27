#!/bin/bash
#
# Deploy the cathedral stack
# Usage: ./deploy_stack.sh [--env production|development] [--build]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="docker-compose.yml"
ENV="development"
BUILD=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --env)
      ENV="$2"
      shift 2
      ;;
    --build)
      BUILD=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

echo "🏗️  Cathedral Stack Deployment"
echo "================================"
echo "Environment: $ENV"
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command -v docker &> /dev/null; then
  echo "❌ Docker not installed"
  exit 1
fi

if docker compose version &> /dev/null; then
  COMPOSE_CMD="docker compose"
elif docker-compose version &> /dev/null; then
  COMPOSE_CMD="docker-compose"
else
  echo "❌ Docker Compose not found"
  exit 1
fi

echo "✓ Docker found"
echo "✓ Compose command: $COMPOSE_CMD"

# Check for .env
if [ ! -f ".env" ]; then
  echo "⚠ .env file not found, creating from template..."
  if [ -f ".env.example" ]; then
    cp .env.example .env
    echo "✓ Created .env from template"
  else
    echo "❌ No .env or .env.example found"
    exit 1
  fi
fi

# Generate compose if needed
if [ ! -f "$COMPOSE_FILE" ] || [ ".env" -nt "$COMPOSE_FILE" ]; then
  echo "📝 Generating docker-compose.yml..."
  python3 "$SCRIPT_DIR/generate_compose.py" --env-file .env --output "$COMPOSE_FILE"
fi

# Build if requested or if images don't exist
if [ "$BUILD" = true ]; then
  echo "🔨 Building images..."
  $COMPOSE_CMD -f "$COMPOSE_FILE" build
fi

# Deploy
echo "🚀 Starting stack..."
$COMPOSE_CMD -f "$COMPOSE_FILE" up -d

# Wait for health checks
echo "⏳ Waiting for services..."
sleep 5

# Check health
echo "🏥 Health check..."
MECHANICS_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health || echo "000")
GATEWAY_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health || echo "000")

if [ "$MECHANICS_HEALTH" = "200" ]; then
  echo "✓ Mechanics: healthy"
else
  echo "⚠ Mechanics: not responding (HTTP $MECHANICS_HEALTH)"
fi

if [ "$GATEWAY_HEALTH" = "200" ]; then
  echo "✓ Gateway: healthy"
else
  echo "⚠ Gateway: not responding (HTTP $GATEWAY_HEALTH)"
fi

echo ""
echo "📊 Stack Status"
echo "==============="
$COMPOSE_CMD -f "$COMPOSE_FILE" ps

echo ""
echo "🌐 Access Points"
echo "================"
source .env 2>/dev/null || true
echo "Gateway:    http://localhost:${GATEWAY_PORT:-8080}"
echo "OpenAI API: http://localhost:${OPENAI_API_PORT:-3000}/v1"
if [ "${ENABLE_WEBUI:-true}" = "true" ]; then
  echo "Dashboard:  http://localhost:${WEBUI_PORT:-80}"
fi

echo ""
echo "📋 Useful Commands"
echo "=================="
echo "View logs:     $COMPOSE_CMD -f $COMPOSE_FILE logs -f"
echo "Stop stack:    $COMPOSE_CMD -f $COMPOSE_FILE down"
echo "Restart:       $COMPOSE_CMD -f $COMPOSE_FILE restart"

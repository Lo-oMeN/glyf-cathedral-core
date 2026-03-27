---
name: unified-installer
description: One-command installer for the complete sovereign agent stack. Clones repositories, configures .env, builds containers, and launches the unified cathedral. Use when (1) providing the curl | bash installation experience, (2) automating setup of mechanics + gateway + UI stack, (3) detecting edge-native mode and auto-configuring local inference, (4) provisioning web UI tokens and credentials, (5) running air-gapped installations with pre-downloaded assets.
---

# Unified Installer Skill

## Purpose

Transform complex multi-step setup into a single command. The installer detects environment, fetches dependencies, configures the stack, and launches everything — all with rollback capability.

## The One-Liner

```bash
curl -fsSL https://yourdomain.ai/install.sh | bash
```

Or for air-gapped:
```bash
./install.sh --offline --bundle ./cathedral-bundle.tar.gz
```

## Scripts

### `scripts/install.sh` — Bash Installer

Main installer supporting multiple modes:

```bash
# Standard install
curl -fsSL https://cathedral.ai/install.sh | bash

# With options
curl -fsSL https://cathedral.ai/install.sh | bash -s -- \
  --branch main \
  --mechanics-url http://localhost:8080 \
  --with-webui

# Offline/air-gapped
./install.sh --offline --bundle ./bundle.tar.gz
```

### `scripts/install.go` — Go Binary (Advanced)

Cross-platform binary with embedded assets:

```bash
# Build
make build-installer

# Run
./cathedral-install --help
```

## Installation Phases

### Phase 1: Environment Detection

```bash
#!/bin/bash

detect_environment() {
  echo "🔍 Detecting environment..."
  
  # OS detection
  if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
  else
    echo "❌ Unsupported OS: $OSTYPE"
    exit 1
  fi
  
  # Architecture
  ARCH=$(uname -m)
  
  # Docker check
  if ! command -v docker &> /dev/null; then
    echo "❌ Docker required but not installed"
    exit 1
  fi
  
  # Docker Compose check
  if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
  elif docker-compose version &> /dev/null; then
    COMPOSE_CMD="docker-compose"
  else
    echo "❌ Docker Compose required"
    exit 1
  fi
  
  # Edge-native detection
  if curl -s http://localhost:8080/health &> /dev/null; then
    echo "✓ Edge-native mode detected — routing all agents to local mechanics"
    EDGE_NATIVE=true
  else
    echo "⚠ No local mechanics detected — will use Ollama fallback"
    EDGE_NATIVE=false
  fi
}
```

### Phase 2: Repository Clone

```bash
clone_repositories() {
  echo "📦 Cloning cathedral repositories..."
  
  WORKDIR="${WORKDIR:-$HOME/.cathedral}"
  mkdir -p "$WORKDIR"
  cd "$WORKDIR"
  
  # Fork NanoClaw if not exists
  if [ ! -d "nanoclaw" ]; then
    git clone --depth 1 https://github.com/qwibitai/nanoclaw.git
    cd nanoclaw
    # Apply patches
    bash scripts/patch_for_mechanics.sh
    cd ..
  fi
  
  # Get mechanics image
  if [ "$EDGE_NATIVE" = true ]; then
    echo "Using local mechanics at http://localhost:8080"
  else
    docker pull ollama/ollama:latest
  fi
}
```

### Phase 3: Configuration Generation

```bash
generate_config() {
  echo "⚙️  Generating configuration..."
  
  # Generate random API key for dashboard
  DASHBOARD_API_KEY=$(openssl rand -hex 32)
  
  # Create .env file
  cat > .env <<EOF
# Cathedral Configuration
COMPOSE_PROJECT_NAME=cathedral

# Inference Configuration
MECHANICS_URL=${MECHANICS_URL:-http://mechanics:8080}
INFERENCE_PROVIDER=${INFERENCE_PROVIDER:-local-mechanics}
OLLAMA_URL=http://ollama:11434

# Gateway Configuration
GATEWAY_PORT=8080
OPENAI_API_PORT=3000
WEBUI_PORT=80

# Security
DASHBOARD_API_KEY=$DASHBOARD_API_KEY
JWT_SECRET=$(openssl rand -hex 32)

# Persistence
MEMORY_PATH=./memory
MODELS_PATH=./models

# Feature Flags
ENABLE_WEBUI=${WITH_WEBUI:-true}
ENABLE_TELEGRAM=${WITH_TELEGRAM:-false}
ENABLE_DISCORD=${WITH_DISCORD:-false}
EOF

  echo "✓ Configuration written to .env"
}
```

### Phase 4: Build & Launch

```bash
build_and_launch() {
  echo "🏗️  Building cathedral..."
  
  # Generate docker-compose from template
  python3 scripts/generate_compose.py \
    --env-file .env \
    --output docker-compose.yml
  
  # Build containers
  $COMPOSE_CMD build
  
  # Start stack
  $COMPOSE_CMD up -d
  
  # Wait for health checks
  echo "⏳ Waiting for services to be ready..."
  sleep 5
  
  # Verify
  if curl -s http://localhost:8080/health &> /dev/null; then
    echo "✓ Cathedral is running!"
    echo ""
    echo "🌐 Access points:"
    echo "   Gateway:    http://localhost:8080"
    echo "   OpenAI API: http://localhost:3000/v1"
    [ "$WITH_WEBUI" = "true" ] && echo "   Dashboard:  http://localhost"
    echo ""
    echo "🔑 Dashboard API Key: $DASHBOARD_API_KEY"
  else
    echo "❌ Something went wrong. Check logs:"
    echo "   docker compose logs -f"
    exit 1
  fi
}
```

## Wizard Integration

The installer includes an interactive mode:

```bash
curl -fsSL https://cathedral.ai/install.sh | bash -s -- --wizard
```

Wizard flow:
```
Welcome to Cathedral Installer
==============================

1. Detected OS: Linux (x86_64)
2. Docker: ✓ Installed
3. Edge-native mode: ✓ Detected (mechanics at :8080)

Configuration:
- Gateway port [8080]: 
- Enable Web UI? [Y/n]: Y
- Enable Telegram bot? [y/N]: N
- Enable Discord? [y/N]: N

Ready to install. Proceed? [Y/n]: Y

Installing...
[████████████] 100%

✓ Cathedral installed!
Access: http://localhost:8080
```

## Air-Gapped Installation

For offline/air-gapped environments:

```bash
# On connected machine
./scripts/create_bundle.sh --output cathedral-bundle.tar.gz

# Transfer to air-gapped machine
scp cathedral-bundle.tar.gz airgap:/tmp/

# On air-gapped machine
cd /tmp
tar xzf cathedral-bundle.tar.gz
./install.sh --offline --bundle ./bundle
```

## Uninstall

```bash
./scripts/uninstall.sh
```

Removes:
- Docker containers and volumes
- Configuration files
- Preserves: Memory files (ask user)

## Testing

```bash
# Test installer in clean environment
docker run --rm -it ubuntu:22.04 bash -c "
  apt-get update && apt-get install -y curl docker.io
  curl -fsSL https://cathedral.ai/install.sh | bash
"

# Test offline bundle
./scripts/test_offline.sh --bundle ./test-bundle.tar.gz
```

## References

- **Docker Compose spec**: See `references/compose_spec.md`
- **Cross-platform bash**: See `references/portable_bash.md`
- **Go embed package**: See `references/go_embed.md`

## See Also

- `docker-orchestration` skill — The compose files this installs
- `gateway-modifier` skill — The NanoClaw fork this clones

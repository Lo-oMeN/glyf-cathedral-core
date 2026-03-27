---
name: docker-orchestration
description: Container orchestration for multi-service agent deployments. Build Docker Compose stacks with proper networking, volume persistence, cgroup isolation, and health checks. Specifically designed for OpenClaw/NanoClaw gateways with inference kernels, agent loops, and web UIs. Use when (1) creating the three-layer unified stack (inference + gateway + UI), (2) configuring inter-container networking for mechanics↔gateway communication, (3) setting up volume mounts for persistent memory and state, (4) implementing cgroup resource limits for edge devices, (5) building production docker-compose.yml with zero external dependencies.
---

# Docker Orchestration Skill

## Purpose

Deploy the unified agent stack as isolated, reproducible containers. This skill creates the three-layer architecture with proper networking, persistence, and resource constraints.

## The Three-Layer Stack

```yaml
# docker-compose.yml structure
services:
  mechanics:      # Layer 1: Inference kernel
  gateway:        # Layer 2: NanoClaw agent gateway
  webui:          # Layer 3: Control plane dashboard
```

## Scripts

### `scripts/generate_compose.py` — Compose Generator

Creates production-ready docker-compose.yml with your specific configuration:

```bash
python scripts/generate_compose.py \
  --mechanics-image my-mechanics:latest \
  --gateway-image nanoclaw:latest \
  --with-webui \
  --output docker-compose.yml
```

### `scripts/deploy_stack.sh` — One-Command Deploy

Builds and starts the entire stack:

```bash
./scripts/deploy_stack.sh --env production
```

## Architecture Patterns

### Layer 1: Inference Kernel (Mechanics)

```yaml
services:
  mechanics:
    image: your-mechanics:latest
    container_name: cathedral-mechanics
    networks:
      - cathedral-net
    volumes:
      - mechanics-data:/data
    environment:
      - MODEL_PATH=/data/models
      - MAX_BATCH_SIZE=1
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

**Key configurations:**
- **Cgroup limits**: Hard caps on CPU/memory for edge devices
- **Volume persistence**: Model weights and state survive container restarts
- **Health checks**: Automatic restart on inference failure
- **Network isolation**: Only gateway can reach mechanics

### Layer 2: Agent Gateway (NanoClaw)

```yaml
services:
  gateway:
    image: nanoclaw:latest
    container_name: cathedral-gateway
    networks:
      - cathedral-net
    ports:
      - "3000:3000"    # OpenAI API proxy
      - "8080:8080"    # Gateway HTTP
    volumes:
      - gateway-memory:/app/memory
      - ./config:/app/config:ro
    environment:
      - OPENAI_BASE_URL=http://mechanics:8080
      - MECHANICS_PROXY=http://mechanics:8080
      - MEMORY_PATH=/app/memory
    depends_on:
      mechanics:
        condition: service_healthy
```

**Key configurations:**
- **Upstream pointing**: Gateway → Mechanics via internal DNS
- **Memory persistence**: Long-term state in named volume
- **Config mounting**: Read-only config injection
- **Dependency health**: Waits for mechanics to be ready

### Layer 3: Web UI (Control Plane)

```yaml
services:
  webui:
    image: cathedral-dashboard:latest
    container_name: cathedral-ui
    networks:
      - cathedral-net
    ports:
      - "80:3000"
    environment:
      - GATEWAY_URL=http://gateway:8080
      - API_KEY=${DASHBOARD_API_KEY}
    depends_on:
      - gateway
```

## Networking Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Network                        │
│              (cathedral-net, isolated)                   │
│                                                          │
│  ┌──────────────┐      ┌──────────────┐                │
│  │  Mechanics   │◄────►│   Gateway    │◄──External    │
│  │  :8080       │      │   :3000      │   API access   │
│  └──────────────┘      └──────┬───────┘                │
│                               │                         │
│                        ┌──────┴───────┐                │
│                        │    WebUI     │                │
│                        │    :3000     │                │
│                        └──────────────┘                │
└─────────────────────────────────────────────────────────┘
```

**Security properties:**
- Mechanics has no external ports — only gateway can reach it
- Gateway exposes OpenAI-compatible API (port 3000) and admin (port 8080)
- Web UI is optional — can be disabled for headless deployments

## Volume Persistence

```yaml
volumes:
  # Mechanics state (models, cache)
  mechanics-data:
    driver: local
    
  # Gateway long-term memory
  gateway-memory:
    driver: local
    
  # Web UI uploads/assets
  webui-assets:
    driver: local
```

**Backup strategy:**
```bash
# Create archive
docker run --rm -v cathedral_gateway-memory:/data -v $(pwd):/backup alpine tar czf /backup/memory-backup.tar.gz -C /data .

# Restore
docker run --rm -v cathedral_gateway-memory:/data -v $(pwd):/backup alpine tar xzf /backup/memory-backup.tar.gz -C /data
```

## Resource Constraints for Edge Devices

### Raspberry Pi 4 (4GB RAM)

```yaml
deploy:
  resources:
    limits:
      cpus: '3.0'
      memory: 3.2G
    reservations:
      cpus: '2.0'
      memory: 2G
```

### Raspberry Pi Zero 2 W (512MB RAM)

```yaml
deploy:
  resources:
    limits:
      cpus: '0.9'
      memory: 480M
    reservations:
      cpus: '0.5'
      memory: 256M
```

## Health Check Patterns

```yaml
healthcheck:
  test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:8080/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## Production Hardening

```yaml
# Security options
security_opt:
  - no-new-privileges:true
  
# Read-only root filesystem
read_only: true

# Tmpfs for temporary files
tmpfs:
  - /tmp:noexec,nosuid,size=100m
  
# Capabilities drop
cap_drop:
  - ALL
cap_add:
  - NET_BIND_SERVICE
```

## References

- **Multi-arch builds**: See `references/multiarch_builds.md` for ARM64/AMD64
- **Swarm mode**: See `references/swarm_deployment.md` for clustering
- **GPU passthrough**: See `references/nvidia_runtime.md` for CUDA support

## See Also

- `openai-api-translation` skill — The proxy layer inside the gateway
- `unified-installer` skill — One-command script that uses this compose

---
name: container-ops
description: Docker and Kubernetes container operations including build, run, manage containers, view logs, execute commands, docker compose, and kubectl operations. Use when working with containerized applications, managing Docker containers or Kubernetes clusters, deploying apps, checking container status, viewing logs, or executing commands in containers.
---

# Container Operations

This skill provides comprehensive Docker and Kubernetes operations for managing containerized applications.

## Auto-Detection

The skill automatically detects Docker and Kubernetes availability on startup:
- **Docker**: Checks for docker-py library and Docker daemon connection
- **Kubernetes**: Checks for kubernetes client library and cluster connectivity

Run the check command to verify availability:
```bash
python3 scripts/container_ops.py check
```

## Installation Requirements

### Required Python Packages

```bash
pip install docker kubernetes
```

### Docker Access

Ensure the user has permissions to access Docker:
```bash
sudo usermod -aG docker $USER
# Log out and back in for changes to take effect
```

### Kubernetes Access

Ensure kubectl is configured with a valid kubeconfig:
```bash
kubectl config current-context
```

## Docker Operations

### Build Image

Build a Docker image from a Dockerfile:

```bash
python3 scripts/container_ops.py build /path/to/Dockerfile --tag myimage:1.0 --context .
```

Parameters:
- `dockerfile_path`: Path to Dockerfile
- `--tag, -t`: Image tag (required)
- `--context, -c`: Build context directory (default: current directory)

### Run Container

Start a new container from an image:

```bash
# Basic run
python3 scripts/container_ops.py run nginx:latest

# With port mappings
python3 scripts/container_ops.py run nginx:latest --ports '{"8080": "80"}'

# With environment variables
python3 scripts/container_ops.py run myapp --env '{"NODE_ENV": "production", "PORT": "3000"}'

# With volumes
python3 scripts/container_ops.py run myapp --volumes '{"/host/data": {"bind": "/app/data", "mode": "rw"}}'

# Combined
python3 scripts/container_ops.py run myapp:1.0 \
  --ports '{"8080": "80", "8443": "443"}' \
  --env '{"NODE_ENV": "production"}' \
  --volumes '{"/host/data": "/app/data"}'
```

Parameters:
- `image`: Image name (required)
- `--ports, -p`: Port mappings as JSON (host port -> container port)
- `--env, -e`: Environment variables as JSON
- `--volumes, -v`: Volume mappings as JSON

### List Containers

List running or all containers:

```bash
# Running containers only
python3 scripts/container_ops.py ps

# All containers including stopped
python3 scripts/container_ops.py ps --all
```

Returns: Container ID, name, image, status, ports, creation time

### Get Logs

Fetch container logs:

```bash
python3 scripts/container_ops.py logs CONTAINER_ID --tail 100
```

Parameters:
- `container_id`: Container ID or name
- `--tail, -n`: Number of lines to show (default: 100)

### Execute Command

Run a command inside a running container:

```bash
python3 scripts/container_ops.py exec CONTAINER_ID ls -la
python3 scripts/container_ops.py exec CONTAINER_ID sh -c "echo hello"
```

Parameters:
- `container_id`: Container ID or name
- `command`: Command and arguments to execute

### Docker Compose

Start services defined in a compose file:

```bash
# Default docker-compose.yml
python3 scripts/container_ops.py compose-up

# Custom compose file
python3 scripts/container_ops.py compose-up --file docker-compose.prod.yml
```

Parameters:
- `--file, -f`: Compose file path (default: docker-compose.yml)

## Kubernetes Operations

### Apply Manifest

Apply Kubernetes YAML manifests:

```bash
# Apply to default namespace
python3 scripts/container_ops.py k8s-apply deployment.yaml

# Apply to specific namespace
python3 scripts/container_ops.py k8s-apply deployment.yaml --namespace production
```

Parameters:
- `manifest_path`: Path to YAML manifest file
- `--namespace, -n`: Target namespace (default: default)

### Get Resources

List Kubernetes resources:

```bash
# List pods
python3 scripts/container_ops.py k8s-get pods

# List services
python3 scripts/container_ops.py k8s-get services

# List deployments
python3 scripts/container_ops.py k8s-get deployments

# List configmaps
python3 scripts/container_ops.py k8s-get configmaps

# List secrets
python3 scripts/container_ops.py k8s-get secrets

# In specific namespace
python3 scripts/container_ops.py k8s-get pods --namespace kube-system
```

Supported resource types: pods, services, deployments, configmaps, secrets

Parameters:
- `resource_type`: Type of resource to list
- `--namespace, -n`: Namespace to query (default: default)

### Get Pod Logs

Fetch logs from Kubernetes pods:

```bash
# Get last 100 lines
python3 scripts/container_ops.py k8s-logs my-pod

# Get specific number of lines
python3 scripts/container_ops.py k8s-logs my-pod --tail 500

# From specific namespace
python3 scripts/container_ops.py k8s-logs my-pod --namespace production --tail 50
```

Parameters:
- `pod_name`: Pod name
- `--namespace, -n`: Pod namespace (default: default)
- `--tail`: Number of lines (default: 100)

## Output Format

All commands output JSON with the following structure:

```json
{
  "success": true|false,
  "...": "...",
  "error": "error message if failed"
}
```

Check the `success` field to determine if the operation succeeded.

## Error Handling

Common errors and solutions:

### Docker Connection Error
```
Cannot connect to Docker daemon
```
Solution: Ensure Docker is running and user has permissions

### Image Not Found
```
Image not found: myimage:tag
```
Solution: Build the image first or pull it from a registry

### K8s Connection Error
```
Cannot connect to Kubernetes cluster
```
Solution: Check kubeconfig and cluster availability with `kubectl config current-context`

### Resource Not Found
```
API error: Not Found
```
Solution: Verify the resource name and namespace are correct

## Common Workflows

### Build and Deploy to Docker

```bash
# Build image
python3 scripts/container_ops.py build ./Dockerfile --tag myapp:1.0

# Run container
python3 scripts/container_ops.py run myapp:1.0 --ports '{"8080": "80"}'

# Check status
python3 scripts/container_ops.py ps

# View logs
python3 scripts/container_ops.py logs CONTAINER_ID --tail 50
```

### Deploy to Kubernetes

```bash
# Apply deployment
python3 scripts/container_ops.py k8s-apply deployment.yaml --namespace production

# Check pods
python3 scripts/container_ops.py k8s-get pods --namespace production

# View logs
python3 scripts/container_ops.py k8s-logs my-pod --namespace production --tail 100
```

### Debug Container Issues

```bash
# Check container status
python3 scripts/container_ops.py ps --all

# View recent logs
python3 scripts/container_ops.py logs CONTAINER_ID --tail 50

# Execute debug command
python3 scripts/container_ops.py exec CONTAINER_ID sh
```

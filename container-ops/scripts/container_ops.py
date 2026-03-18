#!/usr/bin/env python3
"""
Container Operations Script for Docker and Kubernetes
Supports: build, run, ps, logs, exec, compose_up, k8s_apply, k8s_get, k8s_logs
"""

import argparse
import json
import os
import sys
import subprocess
from typing import Optional, Dict, List, Any

# Docker availability flag
DOCKER_AVAILABLE = False
K8S_AVAILABLE = False

# Try importing docker
try:
    import docker
    from docker.errors import DockerException, ImageNotFound, ContainerError
    DOCKER_AVAILABLE = True
except ImportError:
    pass

# Try importing kubernetes
try:
    from kubernetes import client, config, utils
    from kubernetes.client.rest import ApiException
    K8S_AVAILABLE = True
except ImportError:
    pass


def get_docker_client():
    """Get Docker client with auto-detection."""
    if not DOCKER_AVAILABLE:
        raise RuntimeError("docker-py not installed. Run: pip install docker")
    try:
        return docker.from_env()
    except DockerException as e:
        raise RuntimeError(f"Cannot connect to Docker daemon: {e}")


def get_k8s_client():
    """Get Kubernetes client with auto-detection."""
    if not K8S_AVAILABLE:
        raise RuntimeError("kubernetes client not installed. Run: pip install kubernetes")
    try:
        config.load_kube_config()
        return client.ApiClient()
    except Exception as e:
        # Try in-cluster config
        try:
            config.load_incluster_config()
            return client.ApiClient()
        except Exception:
            raise RuntimeError(f"Cannot connect to Kubernetes cluster: {e}")


def build_image(dockerfile_path: str, tag: str, context: str = ".") -> Dict[str, Any]:
    """Build Docker image from Dockerfile."""
    client = get_docker_client()
    
    # Resolve paths
    context_path = os.path.abspath(context)
    dockerfile_abs = os.path.abspath(dockerfile_path)
    
    if not os.path.exists(dockerfile_abs):
        return {"success": False, "error": f"Dockerfile not found: {dockerfile_path}"}
    
    try:
        # Build image
        image, build_logs = client.images.build(
            path=context_path,
            dockerfile=dockerfile_abs,
            tag=tag,
            rm=True
        )
        
        logs = []
        for log in build_logs:
            if 'stream' in log:
                logs.append(log['stream'].strip())
            elif 'error' in log:
                return {"success": False, "error": log['error']}
        
        return {
            "success": True,
            "image_id": image.id,
            "tags": image.tags,
            "logs": logs
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def run_container(image: str, ports: Optional[Dict] = None, 
                  env: Optional[Dict] = None, 
                  volumes: Optional[Dict] = None) -> Dict[str, Any]:
    """Run a Docker container."""
    client = get_docker_client()
    
    try:
        # Parse ports format {"host:container": ...} or {"container": host_port}
        port_bindings = {}
        if ports:
            for key, value in ports.items():
                if ':' in key:
                    host_port, container_port = key.split(':')
                    port_bindings[f"{container_port}/tcp"] = ("0.0.0.0", int(host_port))
                else:
                    port_bindings[f"{key}/tcp"] = ("0.0.0.0", int(value))
        
        # Parse volumes format {"host": {"bind": "container", "mode": "rw"}}
        volume_bindings = {}
        if volumes:
            for host_path, vol_config in volumes.items():
                if isinstance(vol_config, dict):
                    bind_path = vol_config.get('bind', '')
                    mode = vol_config.get('mode', 'rw')
                    volume_bindings[host_path] = {'bind': bind_path, 'mode': mode}
                else:
                    volume_bindings[host_path] = {'bind': vol_config, 'mode': 'rw'}
        
        container = client.containers.run(
            image,
            detach=True,
            ports=port_bindings,
            environment=env or {},
            volumes=volume_bindings
        )
        
        return {
            "success": True,
            "container_id": container.id,
            "short_id": container.short_id,
            "name": container.name,
            "status": container.status
        }
    except ImageNotFound:
        return {"success": False, "error": f"Image not found: {image}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_containers(all_containers: bool = False) -> Dict[str, Any]:
    """List Docker containers."""
    client = get_docker_client()
    
    try:
        containers = client.containers.list(all=all_containers)
        result = []
        for c in containers:
            result.append({
                "id": c.short_id,
                "name": c.name,
                "image": c.image.tags[0] if c.image.tags else c.image.id[:12],
                "status": c.status,
                "ports": c.ports,
                "created": c.attrs.get('Created', '')
            })
        return {"success": True, "containers": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_logs(container_id: str, tail: int = 100) -> Dict[str, Any]:
    """Get container logs."""
    client = get_docker_client()
    
    try:
        container = client.containers.get(container_id)
        logs = container.logs(tail=tail, timestamps=True).decode('utf-8')
        return {"success": True, "logs": logs}
    except Exception as e:
        return {"success": False, "error": str(e)}


def exec_command(container_id: str, command: List[str]) -> Dict[str, Any]:
    """Execute command in container."""
    client = get_docker_client()
    
    try:
        container = client.containers.get(container_id)
        result = container.exec_run(command, tty=True)
        return {
            "success": True,
            "exit_code": result.exit_code,
            "output": result.output.decode('utf-8') if result.output else ""
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def compose_up(file_path: str = 'docker-compose.yml') -> Dict[str, Any]:
    """Run docker compose up."""
    if not os.path.exists(file_path):
        return {"success": False, "error": f"Compose file not found: {file_path}"}
    
    try:
        # Use docker compose command
        result = subprocess.run(
            ['docker', 'compose', '-f', file_path, 'up', '-d'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return {"success": True, "output": result.stdout}
        else:
            # Try legacy docker-compose
            result = subprocess.run(
                ['docker-compose', '-f', file_path, 'up', '-d'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return {"success": True, "output": result.stdout}
            return {"success": False, "error": result.stderr}
    except Exception as e:
        return {"success": False, "error": str(e)}


def k8s_apply(manifest_path: str, namespace: str = 'default') -> Dict[str, Any]:
    """Apply Kubernetes manifest."""
    if not os.path.exists(manifest_path):
        return {"success": False, "error": f"Manifest file not found: {manifest_path}"}
    
    try:
        api_client = get_k8s_client()
        
        # Use kubectl if available, otherwise use client
        result = subprocess.run(
            ['kubectl', 'apply', '-f', manifest_path, '-n', namespace],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return {"success": True, "output": result.stdout}
        else:
            return {"success": False, "error": result.stderr}
    except Exception as e:
        return {"success": False, "error": str(e)}


def k8s_get(resource_type: str, namespace: str = 'default') -> Dict[str, Any]:
    """Get Kubernetes resources."""
    try:
        config.load_kube_config()
        
        v1 = client.CoreV1Api()
        apps_v1 = client.AppsV1Api()
        
        result = []
        
        resource_type = resource_type.lower()
        
        if resource_type in ['pods', 'pod', 'po']:
            items = v1.list_namespaced_pod(namespace=namespace).items
            for item in items:
                result.append({
                    "name": item.metadata.name,
                    "status": item.status.phase,
                    "ready": f"{sum(1 for c in (item.status.container_statuses or []) if c.ready)}/{len(item.spec.containers)}",
                    "restarts": sum((c.restart_count or 0) for c in (item.status.container_statuses or [])),
                    "age": str(item.metadata.creation_timestamp)
                })
        
        elif resource_type in ['services', 'service', 'svc']:
            items = v1.list_namespaced_service(namespace=namespace).items
            for item in items:
                result.append({
                    "name": item.metadata.name,
                    "type": item.spec.type,
                    "cluster_ip": item.spec.cluster_ip,
                    "ports": [f"{p.port}/{p.protocol}" for p in item.spec.ports] if item.spec.ports else [],
                    "age": str(item.metadata.creation_timestamp)
                })
        
        elif resource_type in ['deployments', 'deployment', 'deploy']:
            items = apps_v1.list_namespaced_deployment(namespace=namespace).items
            for item in items:
                result.append({
                    "name": item.metadata.name,
                    "ready": f"{item.status.ready_replicas or 0}/{item.spec.replicas}",
                    "available": item.status.available_replicas or 0,
                    "age": str(item.metadata.creation_timestamp)
                })
        
        elif resource_type in ['configmaps', 'configmap', 'cm']:
            items = v1.list_namespaced_config_map(namespace=namespace).items
            for item in items:
                result.append({
                    "name": item.metadata.name,
                    "keys": list(item.data.keys()) if item.data else [],
                    "age": str(item.metadata.creation_timestamp)
                })
        
        elif resource_type in ['secrets', 'secret']:
            items = v1.list_namespaced_secret(namespace=namespace).items
            for item in items:
                result.append({
                    "name": item.metadata.name,
                    "type": item.type,
                    "keys": list(item.data.keys()) if item.data else [],
                    "age": str(item.metadata.creation_timestamp)
                })
        
        else:
            return {"success": False, "error": f"Unsupported resource type: {resource_type}"}
        
        return {"success": True, "resources": result}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def k8s_logs(pod_name: str, namespace: str = 'default', tail: int = 100) -> Dict[str, Any]:
    """Get Kubernetes pod logs."""
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        
        logs = v1.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            tail_lines=tail
        )
        
        return {"success": True, "logs": logs}
    except ApiException as e:
        return {"success": False, "error": f"API error: {e.reason}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def check_availability() -> Dict[str, Any]:
    """Check Docker and Kubernetes availability."""
    result = {
        "docker": {"available": False, "version": None, "error": None},
        "kubernetes": {"available": False, "version": None, "error": None}
    }
    
    # Check Docker
    if DOCKER_AVAILABLE:
        try:
            client = docker.from_env()
            version = client.version()
            result["docker"]["available"] = True
            result["docker"]["version"] = version.get('Version', 'unknown')
        except Exception as e:
            result["docker"]["error"] = str(e)
    else:
        result["docker"]["error"] = "docker-py not installed"
    
    # Check Kubernetes
    if K8S_AVAILABLE:
        try:
            config.load_kube_config()
            v1 = client.VersionApi()
            version = v1.get_code()
            result["kubernetes"]["available"] = True
            result["kubernetes"]["version"] = version.git_version
        except Exception as e:
            result["kubernetes"]["error"] = str(e)
    else:
        result["kubernetes"]["error"] = "kubernetes client not installed"
    
    return result


def main():
    parser = argparse.ArgumentParser(description='Container Operations')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Check command
    subparsers.add_parser('check', help='Check Docker/K8s availability')
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Build Docker image')
    build_parser.add_argument('dockerfile_path', help='Path to Dockerfile')
    build_parser.add_argument('--tag', '-t', required=True, help='Image tag')
    build_parser.add_argument('--context', '-c', default='.', help='Build context')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run container')
    run_parser.add_argument('image', help='Image name')
    run_parser.add_argument('--ports', '-p', help='Port mappings (JSON)')
    run_parser.add_argument('--env', '-e', help='Environment variables (JSON)')
    run_parser.add_argument('--volumes', '-v', help='Volume mappings (JSON)')
    
    # PS command
    ps_parser = subparsers.add_parser('ps', help='List containers')
    ps_parser.add_argument('--all', '-a', action='store_true', help='Show all containers')
    
    # Logs command
    logs_parser = subparsers.add_parser('logs', help='Get container logs')
    logs_parser.add_argument('container_id', help='Container ID')
    logs_parser.add_argument('--tail', '-n', type=int, default=100, help='Number of lines')
    
    # Exec command
    exec_parser = subparsers.add_parser('exec', help='Execute command in container')
    exec_parser.add_argument('container_id', help='Container ID')
    exec_parser.add_argument('command', nargs='+', help='Command to execute')
    
    # Compose up command
    compose_parser = subparsers.add_parser('compose-up', help='Docker compose up')
    compose_parser.add_argument('--file', '-f', default='docker-compose.yml', help='Compose file')
    
    # K8s apply command
    k8s_apply_parser = subparsers.add_parser('k8s-apply', help='Apply K8s manifest')
    k8s_apply_parser.add_argument('manifest_path', help='Path to manifest')
    k8s_apply_parser.add_argument('--namespace', '-n', default='default', help='Namespace')
    
    # K8s get command
    k8s_get_parser = subparsers.add_parser('k8s-get', help='Get K8s resources')
    k8s_get_parser.add_argument('resource_type', help='Resource type (pods, services, deployments, etc.)')
    k8s_get_parser.add_argument('--namespace', '-n', default='default', help='Namespace')
    
    # K8s logs command
    k8s_logs_parser = subparsers.add_parser('k8s-logs', help='Get K8s pod logs')
    k8s_logs_parser.add_argument('pod_name', help='Pod name')
    k8s_logs_parser.add_argument('--namespace', '-n', default='default', help='Namespace')
    k8s_logs_parser.add_argument('--tail', type=int, default=100, help='Number of lines')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    result = None
    
    try:
        if args.command == 'check':
            result = check_availability()
        
        elif args.command == 'build':
            result = build_image(args.dockerfile_path, args.tag, args.context)
        
        elif args.command == 'run':
            ports = json.loads(args.ports) if args.ports else None
            env = json.loads(args.env) if args.env else None
            volumes = json.loads(args.volumes) if args.volumes else None
            result = run_container(args.image, ports, env, volumes)
        
        elif args.command == 'ps':
            result = list_containers(args.all)
        
        elif args.command == 'logs':
            result = get_logs(args.container_id, args.tail)
        
        elif args.command == 'exec':
            result = exec_command(args.container_id, args.command)
        
        elif args.command == 'compose-up':
            result = compose_up(args.file)
        
        elif args.command == 'k8s-apply':
            result = k8s_apply(args.manifest_path, args.namespace)
        
        elif args.command == 'k8s-get':
            result = k8s_get(args.resource_type, args.namespace)
        
        elif args.command == 'k8s-logs':
            result = k8s_logs(args.pod_name, args.namespace, args.tail)
    
    except Exception as e:
        result = {"success": False, "error": str(e)}
    
    print(json.dumps(result, indent=2, default=str))
    sys.exit(0 if result and result.get('success') else 1)


if __name__ == '__main__':
    main()

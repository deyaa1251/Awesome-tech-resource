import docker
from typing import Dict, List, Optional
from pathlib import Path


class DockerManager:
    """Wrapper around Docker SDK for managing LLMObs services."""
    
    def __init__(self):
        try:
            self.client = docker.from_env()
        except Exception as e:
            raise Exception(f"Failed to connect to Docker: {e}")
        
        self.project_name = "llmobs-core"
    
    def start_service(self, service_name: str) -> bool:
        """Start a specific service using docker-compose."""
        try:
            # This is a simplified version. In production, you'd use docker-compose Python library
            # or subprocess to call docker-compose commands
            import subprocess
            result = subprocess.run(
                ["docker-compose", "up", "-d", service_name],
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Error starting service {service_name}: {e}")
            return False
    
    def stop_services(self) -> bool:
        """Stop all LLMObs services."""
        try:
            import subprocess
            result = subprocess.run(
                ["docker-compose", "down"],
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Error stopping services: {e}")
            return False
    
    def get_status(self) -> Dict[str, bool]:
        """Get status of all services."""
        services = ["postgres", "redis", "backend", "frontend"]
        status = {}
        
        for service in services:
            try:
                container_name = f"{self.project_name}-{service}-1"
                container = self.client.containers.get(container_name)
                status[service] = container.status == "running"
            except docker.errors.NotFound:
                status[service] = False
            except Exception:
                status[service] = False
        
        return status
    
    def pull_image(self, image: str) -> bool:
        """Pull a Docker image."""
        try:
            self.client.images.pull(image)
            return True
        except Exception as e:
            print(f"Error pulling image {image}: {e}")
            return False
    
    def is_plugin_installed(self, plugin_name: str) -> bool:
        """Check if a plugin is installed."""
        try:
            container_name = f"{self.project_name}-plugin-{plugin_name}"
            self.client.containers.get(container_name)
            return True
        except docker.errors.NotFound:
            return False
        except Exception:
            return False
    
    def register_plugin(self, plugin_name: str, image: str) -> bool:
        """Register and start a plugin container."""
        try:
            container = self.client.containers.run(
                image,
                name=f"{self.project_name}-plugin-{plugin_name}",
                detach=True,
                network=f"{self.project_name}_default",
                labels={
                    "llmobs.plugin": plugin_name,
                    "llmobs.type": "plugin",
                },
            )
            return container is not None
        except Exception as e:
            print(f"Error registering plugin {plugin_name}: {e}")
            return False
    
    def list_plugins(self, include_inactive: bool = False) -> List[Dict]:
        """List all registered plugins."""
        try:
            filters = {"label": "llmobs.type=plugin"}
            containers = self.client.containers.list(all=include_inactive, filters=filters)
            
            plugins = []
            for container in containers:
                plugins.append({
                    "name": container.labels.get("llmobs.plugin", "unknown"),
                    "active": container.status == "running",
                    "image": container.image.tags[0] if container.image.tags else "unknown",
                    "version": "latest",
                })
            
            return plugins
        except Exception as e:
            print(f"Error listing plugins: {e}")
            return []
    
    def follow_logs(self):
        """Follow logs from all services."""
        try:
            import subprocess
            subprocess.run(["docker-compose", "logs", "-f"])
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Error following logs: {e}")

import redis
from typing import Dict, List
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


class PluginManager:
    """Manages plugin registration and heartbeats."""
    
    PLUGIN_REGISTRY_KEY = "plugins:registry"
    PLUGIN_HEARTBEAT_KEY = "plugins:heartbeat:{plugin_id}"
    HEARTBEAT_TTL = 60  # seconds
    
    @classmethod
    def register_plugin(cls, plugin_id: str, metadata: Dict) -> bool:
        """Register a plugin in the registry."""
        try:
            redis_client.hset(
                cls.PLUGIN_REGISTRY_KEY,
                plugin_id,
                str(metadata),
            )
            return True
        except Exception as e:
            print(f"Error registering plugin: {e}")
            return False
    
    @classmethod
    def unregister_plugin(cls, plugin_id: str) -> bool:
        """Remove a plugin from the registry."""
        try:
            redis_client.hdel(cls.PLUGIN_REGISTRY_KEY, plugin_id)
            redis_client.delete(cls.PLUGIN_HEARTBEAT_KEY.format(plugin_id=plugin_id))
            return True
        except Exception as e:
            print(f"Error unregistering plugin: {e}")
            return False
    
    @classmethod
    def heartbeat(cls, plugin_id: str) -> bool:
        """Record a heartbeat for a plugin."""
        try:
            key = cls.PLUGIN_HEARTBEAT_KEY.format(plugin_id=plugin_id)
            redis_client.setex(key, cls.HEARTBEAT_TTL, "alive")
            return True
        except Exception as e:
            print(f"Error recording heartbeat: {e}")
            return False
    
    @classmethod
    def is_plugin_alive(cls, plugin_id: str) -> bool:
        """Check if a plugin is alive based on heartbeat."""
        try:
            key = cls.PLUGIN_HEARTBEAT_KEY.format(plugin_id=plugin_id)
            return redis_client.exists(key) > 0
        except Exception as e:
            print(f"Error checking plugin status: {e}")
            return False
    
    @classmethod
    def get_all_plugins(cls) -> Dict:
        """Get all registered plugins."""
        try:
            return redis_client.hgetall(cls.PLUGIN_REGISTRY_KEY)
        except Exception as e:
            print(f"Error getting plugins: {e}")
            return {}
    
    @classmethod
    def get_active_plugins(cls) -> List[str]:
        """Get list of plugin IDs that are currently active (with heartbeat)."""
        try:
            all_plugins = cls.get_all_plugins()
            return [
                plugin_id
                for plugin_id in all_plugins.keys()
                if cls.is_plugin_alive(plugin_id)
            ]
        except Exception as e:
            print(f"Error getting active plugins: {e}")
            return []

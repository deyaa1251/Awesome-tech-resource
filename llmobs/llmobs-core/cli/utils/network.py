import requests
from typing import Optional


def check_plugin_availability(url: str, timeout: int = 5) -> bool:
    """Check if a plugin service is available."""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except Exception:
        return False


def get_plugin_metadata(url: str) -> Optional[dict]:
    """Fetch plugin metadata from its endpoint."""
    try:
        response = requests.get(f"{url}/metadata", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error fetching plugin metadata: {e}")
        return None


def validate_plugin_url(url: str) -> bool:
    """Validate that a URL is properly formatted."""
    from urllib.parse import urlparse
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

import requests
from typing import Dict, Any


class BaseAPIClient:
    """Base class for API clients."""
    def __init__(self, token: str, base_url: str):
        self.token = token
        self.base_url = base_url

    def _make_request(self, endpoint: str = "", params: Dict[str, Any] = None, method: str = "POST"):
        """Make an API request."""
        headers = {
            "accept": "application/json",
            "token": self.token,
        }
        url = f"{self.base_url}{endpoint}"
        
        # Perform the request
        if method == "POST":
            response = requests.post(url, headers=headers, params=params)
        elif method == "GET":
            response = requests.get(url, headers=headers, params=params)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        # Check for response status
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def fetch_hosts(self, skip: int = 5, limit: int = 2):
        """Fetch hosts from Qualys and CrowdStrike API."""
        params = {"skip": skip, "limit": limit}
        return self._make_request(params=params)
    
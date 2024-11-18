import requests
from typing import Dict, Any


class BaseAPIClient:
    """
    Base class for API clients to interact with Qualys and CrowdStrike APIs.
    """

    def __init__(self, token: str, base_url: str):
        """
        Initialize the API client.

        :param token: API token for authentication.
        :param base_url: Base URL of the API.
        """
        self.token = token
        self.base_url = base_url

    def _make_request(self, endpoint: str = "", params: Dict[str, Any] = None, method: str = "POST"):
        """
        Make an API request.

        :param endpoint: API endpoint (optional).
        :param params: Query parameters for the request (optional).
        :param method: HTTP method ('POST').
        :return: Parsed JSON response from the API.
        :raises: HTTPError if the request fails.
        """
        headers = {
            "accept": "application/json",
            "token": self.token,
        }
        url = f"{self.base_url}{endpoint}"

        # Perform the request
        if method == "POST":
            response = requests.post(url, headers=headers, params=params)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        # Check response status
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def fetch_hosts(self, skip: int = 0, limit: int = 10):
        """
        Fetch host data from the API.

        :param skip: Number of hosts to skip.
        :param limit: Number of hosts to fetch.
        :return: List of host data.
        """
        params = {"skip": skip, "limit": limit}
        return self._make_request(params=params)
import requests




class QualysClient:
    def __init__(self, TOKEN: str, QUALYS_API: str):
        self.token = TOKEN
        self.base_url = QUALYS_API

    def fetch_hosts(self, skip: int = 5, limit: int = 2):
        headers = {
            "accept": "application/json",
            "token": self.token,
        }
        params = {"skip": skip, "limit": limit}
        response = requests.post(self.base_url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()  # Parse JSON response
        else:
            response.raise_for_status()  # Raise an error for bad responses
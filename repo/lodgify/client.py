import requests
from typing import Dict, List, Optional


class LodgifyClient:
    """Client for Lodgify API - Vacation Rental Platform"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.lodgify.com"
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}
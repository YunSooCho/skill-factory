import requests
from typing import Dict, Optional


class ProductFruitsClient:
    """Client for ProductFruits API - User Onboarding Platform"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.productfruits.io"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}

    def create_or_update_user(self, user_data: Dict) -> Dict:
        """Create or update a user in ProductFruits"""
        return self._request('POST', '/v1/users', json=user_data)
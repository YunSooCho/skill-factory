import requests
import time
from typing import Dict, Optional


class DlvrItAPIError(Exception):
    pass


class DlvrItClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.dlvr.it/api/v1",
        timeout: int = 30,
        max_retries: int = 3
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries

    def _make_request(self, method: str, endpoint: str, json_data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}

        for attempt in range(self.max_retries):
            try:
                response = requests.request(method, url, json=json_data, params=params, headers=headers, timeout=self.timeout)
                if response.status_code == 429:
                    time.sleep(1)
                    continue
                if not response.ok:
                    raise DlvrItAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise DlvrItAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise DlvrItAPIError("Max retries exceeded")

    def create_post_to_account(self, account_id: str, content: str, platforms: list, scheduled_at: Optional[str] = None) -> Dict:
        return self._make_request('POST', '/accounts/posts', json_data={
            'account_id': account_id, 'content': content, 'platforms': platforms, 'scheduled_at': scheduled_at
        })

    def create_post_to_route(self, route_id: str, content: str, scheduled_at: Optional[str] = None) -> Dict:
        return self._make_request('POST', '/routes/posts', json_data={
            'route_id': route_id, 'content': content, 'scheduled_at': scheduled_at
        })

    def list_accounts(self, limit: int = 100, offset: int = 0) -> Dict:
        return self._make_request('GET', '/accounts', params={'limit': limit, 'offset': offset})

    def list_routes(self, limit: int = 100, offset: int = 0) -> Dict:
        return self._make_request('GET', '/routes', params={'limit': limit, 'offset': offset})

    def close(self):
        self.session = None
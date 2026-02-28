import requests
import time
from typing import Dict

class GoogleBusinessProfileAPIError(Exception):
    pass

class GoogleBusinessProfileClient:
    def __init__(self, access_token: str, base_url: str = "https://mybusinessbusinessinformation.googleapis.com/v1", timeout: int = 30, max_retries: int = 3):
        self.access_token = access_token
        self.base_url = base_url.rstrip('/')
        self.timeout, self.max_retries = timeout, max_retries
        self._last_request = 0
        self._min_interval = 0.1

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        headers = {'Authorization': f'Bearer {self.access_token}'}

        for attempt in range(self.max_retries):
            try:
                time.sleep(max(0, self._min_interval - (time.time() - self._last_request)))
                response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
                self._last_request = time.time()
                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        time.sleep(1); continue
                if not response.ok:
                    raise GoogleBusinessProfileAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise GoogleBusinessProfileAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise GoogleBusinessProfileAPIError("Max retries exceeded")

    def get_locations(self, account_id: str, page_size: int = 100) -> Dict:
        return self._make_request(f'/accounts/{account_id}/locations', params={'pageSize': page_size})

    def get_location(self, location_id: str) -> Dict:
        return self._make_request(f'/{location_id}')

    def close(self):
        self.session = None
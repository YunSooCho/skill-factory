import requests
import time
from typing import Dict, Optional

class GoogleSearchConsoleAPIError(Exception):
    pass

class GoogleSearchConsoleClient:
    def __init__(self, access_token: str, base_url: str = "https://searchconsole.googleapis.com/v1", timeout: int = 30, max_retries: int = 3):
        self.access_token = access_token
        self.base_url = base_url.rstrip('/')
        self.timeout, self.max_retries = timeout, max_retries
        self._last_request = 0
        self._min_interval = 0.1

    def _make_request(self, endpoint: str, json_data: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        headers = {'Authorization': f'Bearer {self.access_token}', 'Content-Type': 'application/json'}

        for attempt in range(self.max_retries):
            try:
                time.sleep(max(0, self._min_interval - (time.time() - self._last_request)))
                response = requests.post(url, json=json_data, headers=headers, timeout=self.timeout)
                self._last_request = time.time()
                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        time.sleep(1); continue
                if not response.ok:
                    raise GoogleSearchConsoleAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise GoogleSearchConsoleAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise GoogleSearchConsoleAPIError("Max retries exceeded")

    def get_search_analytics(self, site_url: str, data: Dict) -> Dict:
        return self._make_request(f'/urlInspection/index:inspect', json_data={'inspectionUrl': site_url, ...})

    def close(self):
        self.session = None
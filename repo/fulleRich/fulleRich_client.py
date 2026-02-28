import requests
import time
from typing import Dict

class FullEnrichAPIError(Exception):
    pass

class FullEnrichClient:
    def __init__(self, api_key: str, base_url: str = "https://api.fullenrich.com/v1", timeout: int = 30, max_retries: int = 3):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout, self.max_retries = timeout, max_retries
        self._last_request = 0
        self._min_interval = 0.1

    def _make_request(self, endpoint: str, json_data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        for attempt in range(self.max_retries):
            try:
                time.sleep(max(0, self._min_interval - (time.time() - self._last_request)))
                response = requests.post(url, json=json_data, params=params, headers=headers, timeout=self.timeout)
                self._last_request = time.time()
                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        time.sleep(1); continue
                if not response.ok:
                    raise FullEnrichAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise FullEnrichAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise FullEnrichAPIError("Max retries exceeded")

    def enrich_contact(self, data: Dict) -> Dict:
        return self._make_request('/enrich', json_data=data)

    def get_enrichment_result(self, enrichment_id: str) -> Dict:
        return self._make_request('/enrich/result', params={'enrichment_id': enrichment_id})

    def close(self):
        self.session = None
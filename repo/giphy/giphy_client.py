import requests
import time
from typing import Dict, Optional

class GiphyAPIError(Exception):
    pass

class GiphyClient:
    def __init__(self, api_key: str, base_url: str = "https://api.giphy.com/v1/gifs", timeout: int = 30, max_retries: int = 3):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout, self.max_retries = timeout, max_retries
        self._last_request = 0
        self._min_interval = 0.1

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        if not params: params = {}
        params['api_key'] = self.api_key
        for attempt in range(self.max_retries):
            try:
                time.sleep(max(0, self._min_interval - (time.time() - self._last_request)))
                response = requests.get(url, params=params, timeout=self.timeout)
                self._last_request = time.time()
                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        time.sleep(1); continue
                if not response.ok:
                    raise GiphyAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise GiphyAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise GiphyAPIError("Max retries exceeded")

    def search_gifs(self, query: str, limit: int = 25, offset: int = 0) -> Dict:
        return self._make_request('/search', params={'q': query, 'limit': limit, 'offset': offset})

    def get_gif_by_id(self, gif_id: str) -> Dict:
        return self._make_request(f'/{gif_id}')

    def close(self):
        self.session = None
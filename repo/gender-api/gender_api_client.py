import requests
import time
from typing import Dict

class GenderAPIError(Exception):
    pass

class GenderAPIClient:
    def __init__(self, api_key: str, base_url: str = "https://api.gender-api.com/v2", timeout: int = 30, max_retries: int = 3):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout, self.max_retries = timeout, max_retries
        self._last_request = 0
        self._min_interval = 0.1

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        if not params: params = {}
        params['key'] = self.api_key
        for attempt in range(self.max_retries):
            try:
                time.sleep(max(0, self._min_interval - (time.time() - self._last_request)))
                response = requests.get(url, params=params, timeout=self.timeout)
                self._last_request = time.time()
                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        time.sleep(1); continue
                if not response.ok:
                    raise GenderAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise GenderAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise GenderAPIError("Max retries exceeded")

    def get_account_stats(self) -> Dict:
        return self._make_request('/account/stats')

    def get_country_of_origin(self, name: str, country: Optional[str] = None) -> Dict:
        params = {'name': name}
        if country: params['country'] = country
        return self._make_request('/country-of-origin', params=params)

    def query_gender_by_first_name(self, first_name: str, country: Optional[str] = None) -> Dict:
        params = {'firstName': first_name}
        if country: params['country'] = country
        return self._make_request('/gender', params=params)

    def close(self):
        self.session = None
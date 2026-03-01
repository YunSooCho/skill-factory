import requests
import time
from typing import Dict, List, Optional


class EmeliaAPIError(Exception):
    pass


class EmeliaRateLimitError(EmeliaAPIError):
    pass


class EmeliaClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.emelia.fr/v1",
        timeout: int = 30,
        max_retries: int = 3
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        self._last_request = 0
        self._min_interval = 0.1

    def _make_request(self, method: str, endpoint: str, json_data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        for attempt in range(self.max_retries):
            try:
                time.sleep(max(0, self._min_interval - (time.time() - self._last_request)))
                response = requests.request(method, url, json=json_data, params=params, headers=headers, timeout=self.timeout)
                self._last_request = time.time()

                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 1))
                    if attempt < self.max_retries - 1:
                        time.sleep(retry_after)
                        continue
                    raise EmeliaRateLimitError("Rate limit exceeded")

                if not response.ok:
                    raise EmeliaAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise EmeliaAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise EmeliaAPIError("Max retries exceeded")

    def add_contact_to_campaign(self, campaign_id: str, email: str, first_name: Optional[str] = None, last_name: Optional[str] = None) -> Dict:
        data = {'email': email}
        if first_name: data['first_name'] = first_name
        if last_name: data['last_name'] = last_name
        return self._make_request('POST', f'/campaigns/{campaign_id}/contacts', json_data=data)

    def list_contacts(self, campaign_id: str, limit: int = 100, offset: int = 0) -> Dict:
        return self._make_request('GET', f'/campaigns/{campaign_id}/contacts', params={'limit': limit, 'offset': offset})

    def delete_contact_from_campaign(self, campaign_id: str, contact_id: str) -> Dict:
        return self._make_request('DELETE', f'/campaigns/{campaign_id}/contacts/{contact_id}')

    def close(self):
        self.session = None
import requests
import time
from typing import Dict, Optional

class GetResponseAPIError(Exception):
    pass

class GetResponseClient:
    def __init__(self, api_key: str, base_url: str = "https://api.getresponse.com/v3", timeout: int = 30, max_retries: int = 3):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout, self.max_retries = timeout, max_retries
        self._last_request = 0
        self._min_interval = 0.1

    def _make_request(self, method: str, endpoint: str, json_data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        headers = {'X-Auth-Token': f'api-key {self.api_key}', 'Content-Type': 'application/json'}
        for attempt in range(self.max_retries):
            try:
                time.sleep(max(0, self._min_interval - (time.time() - self._last_request)))
                response = requests.request(method, url, json=json_data, params=params, headers=headers, timeout=self.timeout)
                self._last_request = time.time()
                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        time.sleep(1); continue
                if not response.ok:
                    raise GetResponseAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise GetResponseAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise GetResponseAPIError("Max retries exceeded")

    def get_contacts(self, limit: int = 100, offset: int = 0, list_id: Optional[str] = None) -> Dict:
        params = {'perPage': limit, 'page': offset // limit + 1}
        if list_id: params['query[campaignId]'] = list_id
        return self._make_request('GET', '/contacts', params=params)

    def get_contact_by_id(self, contact_id: str) -> Dict:
        return self._make_request('GET', f'/contacts/{contact_id}')

    def create_contact(self, email: str, campaign_id: Optional[str] = None, name: Optional[str] = None) -> Dict:
        data = {'email': email}
        if campaign_id: data['campaign'] = {'campaignId': campaign_id}
        if name: data['name'] = name
        return self._make_request('POST', '/contacts', json_data=data)

    def update_contact(self, contact_id: str, data: Dict) -> Dict:
        return self._make_request('POST', f'/contacts/{contact_id}', json_data=data)

    def delete_contact(self, contact_id: str) -> Dict:
        return self._make_request('DELETE', f'/contacts/{contact_id}')

    def get_newsletters(self, limit: int = 100, offset: int = 0) -> Dict:
        return self._make_request('GET', '/newsletters', params={'perPage': limit, 'page': offset // limit + 1})

    def create_newsletter(self, data: Dict) -> Dict:
        return self._make_request('POST', '/newsletters', json_data=data)

    def close(self):
        self.session = None
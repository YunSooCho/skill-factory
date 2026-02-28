import requests
import time
from typing import Dict, Optional

class HubSpotAPIError(Exception):
    pass

class HubSpotClient:
    def __init__(self, api_key: str, base_url: str = "https://api.hubapi.com", timeout: int = 30, max_retries: int = 3):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout, self.max_retries = timeout, max_retries
        self._last_request = 0
        self._min_interval = 0.1

    def _make_request(self, method: str, endpoint: str, json_data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}

        for attempt in range(self.max_retries):
            try:
                time.sleep(max(0, self._min_interval - (time.time() - self._last_request)))
                response = requests.request(method, url, json=json_data, params=params, headers=headers, timeout=self.timeout)
                self._last_request = time.time()
                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        time.sleep(1); continue
                if not response.ok:
                    raise HubSpotAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise HubSpotAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise HubSpotAPIError("Max retries exceeded")

    def get_contacts(self, limit: int = 100, after: Optional[str] = None) -> Dict:
        params = {'limit': limit}
        if after: params['after'] = after
        return self._make_request('GET', '/crm/v3/objects/contacts', params=params)

    def get_contact(self, contact_id: str) -> Dict:
        return self._make_request('GET', f'/crm/v3/objects/contacts/{contact_id}')

    def create_contact(self, email: str, first_name: Optional[str] = None, last_name: Optional[str] = None) -> Dict:
        properties = {'email': email}
        if first_name: properties['firstname'] = first_name
        if last_name: properties['lastname'] = last_name
        return self._make_request('POST', '/crm/v3/objects/contacts', json_data={'properties': properties})

    def update_contact(self, contact_id: str, properties: Dict) -> Dict:
        return self._make_request('PATCH', f'/crm/v3/objects/contacts/{contact_id}', json_data={'properties': properties})

    def delete_contact(self, contact_id: str) -> Dict:
        return self._make_request('DELETE', f'/crm/v3/objects/contacts/{contact_id}')

    def get_companies(self, limit: int = 100, after: Optional[str] = None) -> Dict:
        params = {'limit': limit}
        if after: params['after'] = after
        return self._make_request('GET', '/crm/v3/objects/companies', params=params)

    def close(self):
        self.session = None
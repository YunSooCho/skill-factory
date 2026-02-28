import requests
import time
from typing import Dict, List, Optional


class ElasticEmailAPIError(Exception):
    pass


class ElasticEmailRateLimitError(ElasticEmailAPIError):
    pass


class ElasticEmailClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.elasticemail.com/v4",
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
            'X-ElasticEmail-ApiKey': self.api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
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
                    raise ElasticEmailRateLimitError("Rate limit exceeded")

                if not response.ok:
                    raise ElasticEmailAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise ElasticEmailAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise ElasticEmailAPIError("Max retries exceeded")

    def add_contact(self, email: str, list_name: Optional[str] = None, first_name: Optional[str] = None, last_name: Optional[str] = None, fields: Optional[Dict] = None) -> Dict:
        data = {'email': email}
        if list_name: data['list_name'] = list_name
        if first_name: data['first_name'] = first_name
        if last_name: data['last_name'] = last_name
        if fields: data['fields'] = fields
        return self._make_request('POST', '/contacts', json_data=data)

    def add_list(self, name: str, description: Optional[str] = None) -> Dict:
        data = {'name': name}
        if description: data['description'] = description
        return self._make_request('POST', '/lists', json_data=data)

    def list_contacts(self, limit: int = 100, offset: int = 0, list_id: Optional[str] = None) -> Dict:
        params = {'limit': min(limit, 1000), 'offset': offset}
        if list_id: params['list_id'] = list_id
        return self._make_request('GET', '/contacts', params=params)

    def update_list(self, list_id: str, name: Optional[str] = None, description: Optional[str] = None) -> Dict:
        data = {}
        if name: data['name'] = name
        if description: data['description'] = description
        return self._make_request('PUT', f'/lists/{list_id}', json_data=data)

    def delete_contact(self, email: str) -> Dict:
        return self._make_request('DELETE', f'/contacts/{email}')

    def get_lists(self, limit: int = 100, offset: int = 0) -> Dict:
        return self._make_request('GET', '/lists', params={'limit': limit, 'offset': offset})

    def get_list(self, list_id: str) -> Dict:
        return self._make_request('GET', f'/lists/{list_id}')

    def update_contact(self, email: str, first_name: Optional[str] = None, last_name: Optional[str] = None, fields: Optional[Dict] = None) -> Dict:
        data = {}
        if first_name: data['first_name'] = first_name
        if last_name: data['last_name'] = last_name
        if fields: data['fields'] = fields
        return self._make_request('PUT', f'/contacts/{email}', json_data=data)

    def get_contact(self, email: str) -> Dict:
        return self._make_request('GET', f'/contacts/{email}')

    def close(self):
        self.session = None
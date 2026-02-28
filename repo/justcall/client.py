import requests
from typing import Dict, List, Optional


class JustcallClient:
    """Client for JustCall API - Cloud Phone System"""

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.justcall.io"
        self.session = requests.Session()

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        url = f"{self.base_url}{endpoint}"
        kwargs['auth'] = (self.api_key, self.api_secret)
        if method != 'GET':
            kwargs.setdefault('headers', {})['Content-Type'] = 'application/json'
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}

    def search_phone_number(self, query: str) -> List[Dict]:
        result = self._request('GET', '/phonebook/contacts/search', params={'query': query})
        return result if isinstance(result, list) else []

    def delete_contact(self, contact_id: str) -> Dict:
        return self._request('DELETE', f'/phonebook/contacts/{contact_id}')

    def create_contact(self, contact_data: Dict) -> Dict:
        return self._request('POST', '/phonebook/contacts', json=contact_data)

    def search_contact(self, query: str) -> Dict:
        return self._request('GET', '/phonebook/contacts/search', params={'query': query})

    def get_call_sales_dialer(self, call_id: str) -> Dict:
        return self._request('GET', f'/calls/{call_id}', params={'source': 'sales_dialer'})

    def update_contact(self, contact_id: str, data: Dict) -> Dict:
        return self._request('PUT', f'/phonebook/contacts/{contact_id}', json=data)

    def download_call_recording(self, call_id: str) -> str:
        response = self._request('GET', f'/calls/{call_id}/recording')
        return response.get('download_url', '')

    def search_sms(self, query: str) -> List[Dict]:
        result = self._request('GET', '/sms/search', params={'query': query})
        return result.get('results', [])

    def search_call(self, query: str) -> List[Dict]:
        result = self._request('GET', '/calls/search', params={'query': query})
        return result.get('results', [])

    def search_call_sales_dialer(self, query: str) -> List[Dict]:
        result = self._request('GET', '/calls/search', params={'query': query, 'source': 'sales_dialer'})
        return result.get('results', [])

    def get_contact(self, contact_id: str) -> Dict:
        return self._request('GET', f'/phonebook/contacts/{contact_id}')
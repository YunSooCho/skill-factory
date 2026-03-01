import requests
import time
import hmac
import hashlib
from typing import Dict, Optional

class EndorsalAPIError(Exception):
    pass

class EndorsalClient:
    def __init__(self, api_key: str, webhook_secret: Optional[str] = None, base_url: str = "https://api.endorsal.io/v1", timeout: int = 30, max_retries: int = 3):
        self.api_key = api_key
        self.webhook_secret = webhook_secret
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
                    raise EndorsalAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise EndorsalAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise EndorsalAPIError("Max retries exceeded")

    def create_contact(self, email: str, name: Optional[str] = None) -> Dict:
        data = {'email': email}
        if name: data['name'] = name
        return self._make_request('POST', '/contacts', json_data=data)

    def search_contacts(self, query: str, limit: int = 100, offset: int = 0) -> Dict:
        return self._make_request('GET', '/contacts', params={'q': query, 'limit': limit, 'offset': offset})

    def list_contacts(self, limit: int = 100, offset: int = 0) -> Dict:
        return self._make_request('GET', '/contacts', params={'limit': limit, 'offset': offset})

    def get_contact(self, contact_id: str) -> Dict:
        return self._make_request('GET', f'/contacts/{contact_id}')

    def update_contact(self, contact_id: str, data: Dict) -> Dict:
        return self._make_request('PUT', f'/contacts/{contact_id}', json_data=data)

    def create_testimonial(self, contact_id: str, content: str, rating: Optional[int] = None) -> Dict:
        data = {'contact_id': contact_id, 'content': content}
        if rating: data['rating'] = rating
        return self._make_request('POST', '/testimonials', json_data=data)

    def list_testimonials(self, limit: int = 100, offset: int = 0) -> Dict:
        return self._make_request('GET', '/testimonials', params={'limit': limit, 'offset': offset})

    def get_testimonial(self, testimonial_id: str) -> Dict:
        return self._make_request('GET', f'/testimonials/{testimonial_id}')

    def update_testimonial(self, testimonial_id: str, data: Dict) -> Dict:
        return self._make_request('PUT', f'/testimonials/{testimonial_id}', json_data=data)

    def search_testimonials(self, query: str, limit: int = 100, offset: int = 0) -> Dict:
        return self._make_request('GET', '/testimonials', params={'q': query, 'limit': limit, 'offset': offset})

    def list_campaigns(self, limit: int = 100, offset: int = 0) -> Dict:
        return self._make_request('GET', '/campaigns', params={'limit': limit, 'offset': offset})

    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        if not self.webhook_secret: return True
        expected = hmac.new(self.webhook_secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature.lstrip('sha256='))

    def handle_webhook(self, payload: Dict, signature: Optional[str] = None) -> Dict:
        if signature and self.webhook_secret and not self.verify_webhook_signature(str(payload), signature):
            raise EndorsalAPIError("Invalid webhook signature")
        return {'event_type': payload.get('type'), 'data': payload.get('data'), 'timestamp': payload.get('timestamp')}

    def close(self):
        self.session = None
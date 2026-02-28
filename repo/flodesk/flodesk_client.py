import requests
import time
import hmac
import hashlib
from typing import Dict, Optional

class FlodeskAPIError(Exception):
    pass

class FlodeskClient:
    def __init__(self, api_key: str, webhook_secret: Optional[str] = None, base_url: str = "https://api.flodesk.com/v1", timeout: int = 30, max_retries: int = 3):
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
                    raise FlodeskAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise FlodeskAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise FlodeskAPIError("Max retries exceeded")

    def create_or_update_subscriber(self, email: str, first_name: Optional[str] = None, last_name: Optional[str] = None) -> Dict:
        data = {'email': email}
        if first_name: data['first_name'] = first_name
        if last_name: data['last_name'] = last_name
        return self._make_request('POST', '/subscribers', json_data=data)

    def get_subscriber(self, subscriber_id: str) -> Dict:
        return self._make_request('GET', f'/subscribers/{subscriber_id}')

    def search_subscriber(self, email: str) -> Dict:
        return self._make_request('GET', '/subscribers', params={'email': email})

    def unsubscribe_subscriber(self, subscriber_id: str) -> Dict:
        return self._make_request('POST', f'/subscribers/{subscriber_id}/unsubscribe')

    def add_subscriber_to_segment(self, subscriber_id: str, segment_id: str) -> Dict:
        return self._make_request('POST', f'/segments/{segment_id}/subscribers', json_data={'subscriber_id': subscriber_id})

    def delete_subscriber_from_segment(self, subscriber_id: str, segment_id: str) -> Dict:
        return self._make_request('DELETE', f'/segments/{segment_id}/subscribers/{subscriber_id}')

    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        if not self.webhook_secret: return True
        expected = hmac.new(self.webhook_secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature.lstrip('sha256='))

    def handle_webhook(self, payload: Dict, signature: Optional[str] = None) -> Dict:
        if signature and self.webhook_secret and not self.verify_webhook_signature(str(payload), signature):
            raise FlodeskAPIError("Invalid webhook signature")
        return {'event': payload.get('event'), 'data': payload.get('data')}

    def close(self):
        self.session = None
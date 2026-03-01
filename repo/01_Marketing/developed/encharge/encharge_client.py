import requests
import time
import hmac
import hashlib
from typing import Dict, List, Optional


class EnchargeAPIError(Exception):
    pass


class EnchargeRateLimitError(EnchargeAPIError):
    pass


class EnchargeClient:
    def __init__(
        self,
        api_key: str,
        webhook_secret: Optional[str] = None,
        base_url: str = "https://api.encharge.io/v1",
        timeout: int = 30,
        max_retries: int = 3
    ):
        self.api_key = api_key
        self.webhook_secret = webhook_secret
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
                    raise EnchargeRateLimitError("Rate limit exceeded")

                if not response.ok:
                    raise EnchargeAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise EnchargeAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise EnchargeAPIError("Max retries exceeded")

    def get_all_people(self, limit: int = 100, offset: int = 0) -> Dict:
        return self._make_request('GET', '/people', params={'limit': limit, 'offset': offset})

    def delete_tag(self, tag_id: str) -> Dict:
        return self._make_request('DELETE', f'/tags/{tag_id}')

    def get_people_in_segment(self, segment_id: str, limit: int = 100, offset: int = 0) -> Dict:
        return self._make_request('GET', f'/segments/{segment_id}/people', params={'limit': limit, 'offset': offset})

    def get_segments(self, limit: int = 100, offset: int = 0) -> Dict:
        return self._make_request('GET', '/segments', params={'limit': limit, 'offset': offset})

    def create_and_update_people(self, email: str, fields: Optional[Dict] = None) -> Dict:
        data = {'email': email}
        if fields: data['fields'] = fields
        return self._make_request('POST', '/people', json_data=data)

    def get_specific_people(self, person_id: str) -> Dict:
        return self._make_request('GET', f'/people/{person_id}')

    def unsubscribe_people(self, email: str) -> Dict:
        return self._make_request('POST', '/people/unsubscribe', json_data={'email': email})

    def add_tag(self, email: str, tag_id: str) -> Dict:
        return self._make_request('POST', '/people/tags', json_data={'email': email, 'tag_id': tag_id})

    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        if not self.webhook_secret:
            return True
        expected = hmac.new(self.webhook_secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature.lstrip('sha256='))

    def handle_webhook(self, payload: Dict, signature: Optional[str] = None) -> Dict:
        if signature and self.webhook_secret:
            payload_str = str(payload)
            if not self.verify_webhook_signature(payload_str, signature):
                raise EnchargeAPIError("Invalid webhook signature")
        event_type = payload.get('type')
        result = {
            'event_type': event_type,
            'data': payload.get('data', {}),
            'timestamp': payload.get('timestamp')
        }
        return result

    def close(self):
        self.session = None
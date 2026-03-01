import requests
import time
import hmac
import hashlib
from typing import Dict, Optional

class EventbriteAPIError(Exception):
    pass

class EventbriteRateLimitError(EventbriteAPIError):
    pass

class EventbriteClient:
    def __init__(self, oauth_token: str, webhook_secret: Optional[str] = None, base_url: str = "https://www.eventbriteapi.com/v3", timeout: int = 30, max_retries: int = 3):
        self.oauth_token = oauth_token
        self.webhook_secret = webhook_secret
        self.base_url = base_url.rstrip('/')
        self.timeout, self.max_retries = timeout, max_retries
        self._last_request = 0
        self._min_interval = 0.1

    def _make_request(self, method: str, endpoint: str, json_data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        headers = {'Authorization': f'Bearer {self.oauth_token}', 'Content-Type': 'application/json'}
        for attempt in range(self.max_retries):
            try:
                time.sleep(max(0, self._min_interval - (time.time() - self._last_request)))
                response = requests.request(method, url, json=json_data, params=params, headers=headers, timeout=self.timeout)
                self._last_request = time.time()
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 1))
                    if attempt < self.max_retries - 1:
                        time.sleep(retry_after); continue
                    raise EventbriteRateLimitError("Rate limit exceeded")
                if not response.ok:
                    raise EventbriteAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise EventbriteAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise EventbriteAPIError("Max retries exceeded")

    def publish_event(self, event_id: str) -> Dict:
        return self._make_request('POST', f'/events/{event_id}/publish/')

    def unpublish_event(self, event_id: str) -> Dict:
        return self._make_request('POST', f'/events/{event_id}/unpublish/')

    def get_order_details(self, order_id: str) -> Dict:
        return self._make_request('GET', f'/orders/{order_id}')

    def get_event_ticket_classes(self, event_id: str) -> Dict:
        return self._make_request('GET', f'/events/{event_id}/ticket_classes')

    def update_event(self, event_id: str, data: Dict) -> Dict:
        return self._make_request('POST', f'/events/{event_id}', json_data=data)

    def get_event_details(self, event_id: str) -> Dict:
        return self._make_request('GET', f'/events/{event_id}')

    def get_event_attendees(self, event_id: str, limit: int = 50, offset: int = 0) -> Dict:
        return self._make_request('GET', f'/events/{event_id}/attendees', params={'page': offset // 50 + 1})

    def get_ticket_class_details(self, ticket_class_id: str) -> Dict:
        return self._make_request('GET', f'/ticket_classes/{ticket_class_id}')

    def create_event(self, data: Dict) -> Dict:
        return self._make_request('POST', '/events', json_data=data)

    def get_attendee_details(self, attendee_id: str) -> Dict:
        return self._make_request('GET', f'/attendees/{attendee_id}')

    def get_event_orders(self, event_id: str, limit: int = 50, offset: int = 0) -> Dict:
        return self._make_request('GET', f'/events/{event_id}/orders', params={'page': offset // 50 + 1})

    def get_organization_attendees(self, organization_id: str, limit: int = 50, offset: int = 0) -> Dict:
        return self._make_request('GET', f'/organizations/{organization_id}/attendees', params={'page': offset // 50 + 1})

    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        if not self.webhook_secret: return True
        expected = hmac.new(self.webhook_secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature.lstrip('sha256='))

    def handle_webhook(self, payload: Dict, signature: Optional[str] = None) -> Dict:
        if signature and self.webhook_secret and not self.verify_webhook_signature(str(payload), signature):
            raise EventbriteAPIError("Invalid webhook signature")
        return {'event_type': payload.get('api_url'), 'data': payload.get('data'), 'config': payload.get('config')}

    def close(self):
        self.session = None
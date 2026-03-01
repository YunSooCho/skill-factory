import requests
import time
import hmac
import hashlib
from typing import Dict, Optional, List

class FindymailAPIError(Exception):
    pass

class FindymailClient:
    def __init__(self, api_key: str, webhook_secret: Optional[str] = None, base_url: str = "https://app.findymail.com/api", timeout: int = 30, max_retries: int = 3):
        self.api_key = api_key
        self.webhook_secret = webhook_secret
        self.base_url = base_url.rstrip('/')
        self.timeout, self.max_retries = timeout, max_retries
        self._last_request = 0
        self._min_interval = 0.1

    def _make_request(self, endpoint: str, json_data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        for attempt in range(self.max_retries):
            try:
                time.sleep(max(0, self._min_interval - (time.time() - self._last_request)))
                response = requests.post(url, json=json_data, params=params, headers=headers, timeout=self.timeout)
                self._last_request = time.time()
                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        time.sleep(1); continue
                if not response.ok:
                    raise FindymailAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise FindymailAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise FindymailAPIError("Max retries exceeded")

    def search_email_by_domain(self, domain: str, first_name: Optional[str] = None, last_name: Optional[str] = None) -> Dict:
        data = {'domain': domain}
        if first_name: data['first_name'] = first_name
        if last_name: data['last_name'] = last_name
        return self._make_request('/search/email/domain', json_data=data)

    def search_email_by_linkedin(self, linkedin_url: str) -> Dict:
        return self._make_request('/search/email/linkedin', json_data={'linkedin_url': linkedin_url})

    def verify_email(self, email: str) -> Dict:
        return self._make_request('/verify/email', json_data={'email': email})

    def search_phone_by_linkedin(self, linkedin_url: str) -> Dict:
        return self._make_request('/search/phone/linkedin', json_data={'linkedin_url': linkedin_url})

    def search_email_by_name(self, first_name: str, last_name: str, domain: str) -> Dict:
        return self._make_request('/search/email/name', json_data={'first_name': first_name, 'last_name': last_name, 'domain': domain})

    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        if not self.webhook_secret: return True
        expected = hmac.new(self.webhook_secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature.lstrip('sha256='))

    def handle_webhook(self, payload: Dict, signature: Optional[str] = None) -> Dict:
        if signature and self.webhook_secret and not self.verify_webhook_signature(str(payload), signature):
            raise FindymailAPIError("Invalid webhook signature")
        return {'event_type': payload.get('type'), 'data': payload.get('data'), 'timestamp': payload.get('timestamp')}

    def close(self):
        self.session = None
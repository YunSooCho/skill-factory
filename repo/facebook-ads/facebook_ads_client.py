import requests
import time
import hmac
import hashlib
from typing import Dict, Optional

class FacebookAdsAPIError(Exception):
    pass

class FacebookAdsClient:
    def __init__(self, access_token: str, webhook_secret: Optional[str] = None, base_url: str = "https://graph.facebook.com/v18.0", timeout: int = 30, max_retries: int = 3):
        self.access_token = access_token
        self.webhook_secret = webhook_secret
        self.base_url = base_url.rstrip('/')
        self.timeout, self.max_retries = timeout, max_retries
        self._last_request = 0
        self._min_interval = 0.1

    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        if not params: params = {}
        params['access_token'] = self.access_token
        for attempt in range(self.max_retries):
            try:
                time.sleep(max(0, self._min_interval - (time.time() - self._last_request)))
                response = requests.get(url, params=params, timeout=self.timeout)
                self._last_request = time.time()
                if not response.ok:
                    raise FacebookAdsAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise FacebookAdsAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise FacebookAdsAPIError("Max retries exceeded")

    def create_account_report(self, account_id: str, fields: list, date_preset: str = 'last_28d') -> Dict:
        return self._make_request('GET', f'/act_{account_id}/insights', params={'fields': ','.join(fields), 'date_preset': date_preset})

    def get_account_report(self, account_id: str, fields: list, date_preset: str = 'last_28d') -> Dict:
        return self.create_account_report(account_id, fields, date_preset)

    def create_campaign_report(self, account_id: str, fields: list, date_preset: str = 'last_28d') -> Dict:
        return self._make_request('GET', f'/act_{account_id}/campaigns', params={'fields': ','.join(fields), 'date_preset': date_preset})

    def get_campaign_report(self, account_id: str, fields: list, date_preset: str = 'last_28d') -> Dict:
        return self.create_campaign_report(account_id, fields, date_preset)

    def create_adset_report(self, account_id: str, fields: list, date_preset: str = 'last_28d') -> Dict:
        return self._make_request('GET', f'/act_{account_id}/adsets', params={'fields': ','.join(fields), 'date_preset': date_preset})

    def get_adset_report(self, account_id: str, fields: list, date_preset: str = 'last_28d') -> Dict:
        return self.create_adset_report(account_id, fields, date_preset)

    def create_ad_report(self, account_id: str, fields: list, date_preset: str = 'last_28d') -> Dict:
        return self._make_request('GET', f'/act_{account_id}/ads', params={'fields': ','.join(fields), 'date_preset': date_preset})

    def get_ad_report(self, account_id: str, fields: list, date_preset: str = 'last_28d') -> Dict:
        return self.create_ad_report(account_id, fields, date_preset)

    def verify_webhook_signature(self, payload: str, signature: str, x_hub_signature: str) -> bool:
        if not self.webhook_secret: return True
        expected = hmac.new(self.webhook_secret.encode(), payload.encode(), hashlib.sha1).hexdigest()
        return hmac.compare_digest(f"sha1={expected}", x_hub_signature)

    def handle_webhook(self, payload: Dict, signature: Optional[str] = None, x_hub_signature: Optional[str] = None) -> Dict:
        if x_hub_signature and self.webhook_secret and not self.verify_webhook_signature(str(payload), signature, x_hub_signature):
            raise FacebookAdsAPIError("Invalid webhook signature")
        return {'entry': payload.get('entry'), 'object': payload.get('object')}

    def close(self):
        self.session = None
import requests
import time
import hmac
import hashlib
from typing import Dict

class FirstpromoterAPIError(Exception):
    pass

class FirstpromoterClient:
    def __init__(self, api_key: str, webhook_secret: Optional[str] = None, base_url: str = "https://firstpromoter.com/api/v1", timeout: int = 30, max_retries: int = 3):
        self.api_key = api_key
        self.webhook_secret = webhook_secret
        self.base_url = base_url.rstrip('/')
        self.timeout, self.max_retries = timeout, max_retries
        self._last_request = 0
        self._min_interval = 0.1

    def _make_request(self, endpoint: str, json_data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        headers = {'X-API-KEY': self.api_key, 'Content-Type': 'application/json'}
        for attempt in range(self.max_retries):
            try:
                time.sleep(max(0, self._min_interval - (time.time() - self._last_request)))
                response = requests.post(url, json=json_data, params=params, headers=headers, timeout=self.timeout)
                self._last_request = time.time()
                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        time.sleep(1); continue
                if not response.ok:
                    raise FirstpromoterAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise FirstpromoterAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise FirstpromoterAPIError("Max retries exceeded")

    def get_promoter_report(self, promoter_id: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict:
        params = {'promoter_id': promoter_id}
        if start_date: params['start_date'] = start_date
        if end_date: params['end_date'] = end_date
        return self._make_request('/promoters/report', params=params)

    def get_overview_report(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict:
        params = {}
        if start_date: params['start_date'] = start_date
        if end_date: params['end_date'] = end_date
        return self._make_request('/overview/report', params=params)

    def get_campaign_report(self, campaign_id: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict:
        params = {'campaign_id': campaign_id}
        if start_date: params['start_date'] = start_date
        if end_date: params['end_date'] = end_date
        return self._make_request('/campaigns/report', params=params)

    def search_promoter(self, email: str) -> Dict:
        return self._make_request('/promoters/search', json_data={'email': email})

    def track_sale(self, email: str, amount: float, currency: str = 'USD', promoter_code: Optional[str] = None) -> Dict:
        data = {'email': email, 'amount': amount, 'currency': currency}
        if promoter_code: data['promoter_code'] = promoter_code
        return self._make_request('/sales/track', json_data=data)

    def archive_promoters(self, promoter_ids: list) -> Dict:
        return self._make_request('/promoters/archive', json_data={'promoter_ids': promoter_ids})

    def get_promoter(self, promoter_id: str) -> Dict:
        return self._make_request('/promoters/get', params={'promoter_id': promoter_id})

    def create_promoter(self, email: str, name: Optional[str] = None) -> Dict:
        data = {'email': email}
        if name: data['name'] = name
        return self._make_request('/promoters/create', json_data=data)

    def update_promoter(self, promoter_id: str, data: Dict) -> Dict:
        return self._make_request('/promoters/update', json_data={'promoter_id': promoter_id, **data})

    def track_lead_signup(self, email: str, promoter_code: Optional[str] = None) -> Dict:
        data = {'email': email}
        if promoter_code: data['promoter_code'] = promoter_code
        return self._make_request('/leads/track', json_data=data)

    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        if not self.webhook_secret: return True
        expected = hmac.new(self.webhook_secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature.lstrip('sha256='))

    def handle_webhook(self, payload: Dict, signature: Optional[str] = None) -> Dict:
        if signature and self.webhook_secret and not self.verify_webhook_signature(str(payload), signature):
            raise FirstpromoterAPIError("Invalid webhook signature")
        return {'event_type': payload.get('event_type'), 'data': payload.get('data')}

    def close(self):
        self.session = None
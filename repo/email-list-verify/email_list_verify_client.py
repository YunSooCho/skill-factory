import requests
import time
from typing import Dict, Optional, List


class EmailListVerifyAPIError(Exception):
    pass


class EmailListVerifyRateLimitError(EmailListVerifyAPIError):
    pass


class EmailListVerifyClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.emaillistverify.com/v2",
        timeout: int = 30,
        max_retries: int = 3
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        self._last_request = 0
        self._min_interval = 0.1

    def _make_request(self, endpoint: str, params: Optional[Dict] = None, json_data: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        for attempt in range(self.max_retries):
            try:
                time.sleep(max(0, self._min_interval - (time.time() - self._last_request)))
                response = requests.post(url, params=params, json=json_data, headers=headers, timeout=self.timeout)
                self._last_request = time.time()

                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 1))
                    if attempt < self.max_retries - 1:
                        time.sleep(retry_after)
                        continue
                    raise EmailListVerifyRateLimitError("Rate limit exceeded")

                if not response.ok:
                    raise EmailListVerifyAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise EmailListVerifyAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise EmailListVerifyAPIError("Max retries exceeded")

    def find_business_email_address(self, domain: str, name: Optional[str] = None) -> Dict:
        return self._make_request('/find-email', json_data={'domain': domain, 'name': name})

    def email_address_verification(self, email: str) -> Dict:
        return self._make_request('/verify', json_data={'email': email})

    def email_deliverability_evaluation(self, email: str) -> Dict:
        return self._make_request('/deliverability', json_data={'email': email})

    def check_disposable_email_domain(self, domain: str) -> Dict:
        return self._make_request('/check-disposable', json_data={'domain': domain})

    def close(self):
        self.session = None
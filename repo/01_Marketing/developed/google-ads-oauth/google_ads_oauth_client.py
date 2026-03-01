import requests
import time
from typing import Dict, Optional

class GoogleAdsOAuthAPIError(Exception):
    pass

class GoogleAdsOAuthClient:
    def __init__(self, access_token: str, base_url: str = "https://googleads.googleapis.com/v15", timeout: int = 30, max_retries: int = 3):
        self.access_token = access_token
        self.base_url = base_url.rstrip('/')
        self.timeout, self.max_retries = timeout, max_retries
        self._last_request = 0
        self._min_interval = 0.1

    def _make_request(self, customer_id: str, query: str) -> Dict:
        url = f"{self.base_url}/customers/{customer_id}/googleAds:search"
        headers = {'Authorization': f'Bearer {self.access_token}', 'Content-Type': 'application/json'}

        for attempt in range(self.max_retries):
            try:
                time.sleep(max(0, self._min_interval - (time.time() - self._last_request)))
                response = requests.post(url, json={'query': query}, headers=headers, timeout=self.timeout)
                self._last_request = time.time()
                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        time.sleep(1); continue
                if not response.ok:
                    raise GoogleAdsOAuthAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise GoogleAdsOAuthAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise GoogleAdsOAuthAPIError("Max retries exceeded")

    def get_campaigns(self, customer_id: str) -> Dict:
        query = "SELECT campaign.id, campaign.name, campaign.status FROM campaign"
        return self._make_request(customer_id, query)

    def get_ad_groups(self, customer_id: str) -> Dict:
        query = "SELECT ad_group.id, ad_group.name FROM ad_group"
        return self._make_request(customer_id, query)

    def close(self):
        self.session = None
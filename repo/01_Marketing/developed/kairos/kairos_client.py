import requests
import time
from typing import Dict, Optional, List

class KairosAPIError(Exception):
    pass

class KairosClient:
    def __init__(self, app_id: str, app_key: str, base_url: str = "https://api.kairos.com", timeout: int = 30, max_retries: int = 3):
        self.app_id = app_id
        self.app_key = app_key
        self.base_url = base_url.rstrip('/')
        self.timeout, self.max_retries = timeout, max_retries
        self._last_request = 0
        self._min_interval = 0.1

    def _make_request(self, endpoint: str, json_data: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json', 'app_id': self.app_id, 'app_key': self.app_key}

        for attempt in range(self.max_retries):
            try:
                time.sleep(max(0, self._min_interval - (time.time() - self._last_request)))
                response = requests.post(url, json=json_data, headers=headers, timeout=self.timeout)
                self._last_request = time.time()
                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        time.sleep(1); continue
                if not response.ok:
                    raise KairosAPIError(f"API error {response.status_code}: {response.text}")
                return response.json()
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise KairosAPIError(f"Request failed: {str(e)}")
                time.sleep(1)
        raise KairosAPIError("Max retries exceeded")

    def detect_face(self, image: str) -> Dict:
        return self._make_request('/detect', json_data={'image': image})

    def enroll_face(self, image: str, subject_id: str, gallery_name: str) -> Dict:
        return self._make_request('/enroll', json_data={'image': image, 'subject_id': subject_id, 'gallery_name': gallery_name})

    def recognize_face(self, image: str, gallery_name: str) -> Dict:
        return self._make_request('/recognize', json_data={'image': image, 'gallery_name': gallery_name})

    def close(self):
        self.session = None
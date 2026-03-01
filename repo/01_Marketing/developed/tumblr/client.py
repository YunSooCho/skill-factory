"""
Tumblr Client - Social media
"""

import requests

class TumblrError(Exception): pass
class APIError(TumblrError): pass

class TumblrClient:
    BASE_URL = "https://api.tumblr.com/v2"

    def __init__(self, api_key: str, timeout: int = 30):
        self.session = requests.Session()
        self.timeout = timeout
        self.api_key = api_key

    def _request(self, endpoint: str, params: dict = None) -> dict:
        try:
            if params is None: params = {}
            params["api_key"] = self.api_key
            r = requests.get(f"{self.BASE_URL}{endpoint}", params=params, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise APIError(str(e))

    def get_blog(self, blog_name: str) -> dict:
        return self._request(f"/blog/{blog_name}/info")

    def get_page(self, blog_name: str, page_id: str) -> dict:
        return self._request(f"/blog/{blog_name}/pages/{page_id}")

    def get_post(self, blog_name: str, post_id: int) -> dict:
        return self._request(f"/blog/{blog_name}/posts/{post_id}")

    def close(self): self.session.close()
    def __enter__(self): return self
    def __exit__(self, *args): self.close()
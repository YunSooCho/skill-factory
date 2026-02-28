"""
Twitch Client - Streaming platform
"""

import requests

class TwitchError(Exception): pass
class APIError(TwitchError): pass

class TwitchClient:
    BASE_URL = "https://api.twitch.tv/helix"

    def __init__(self, client_id: str, access_token: str, timeout: int = 30):
        self.session = requests.Session()
        self.timeout = timeout
        self.session.headers.update({"Client-Id": client_id, "Authorization": f"Bearer {access_token}", "Content-Type": "application/json"})

    def _request(self, endpoint: str, params: dict = None) -> dict:
        try:
            r = requests.get(f"{self.BASE_URL}{endpoint}", params=params, timeout=self.timeout, headers=self.session.headers)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise APIError(str(e))

    def get_user(self, user_id: str = None, login: str = None) -> dict:
        params = {}
        if user_id: params["id"] = user_id
        if login: params["login"] = login
        return self._request("/users", params)

    def search_streams(self, query: str) -> dict:
        return self._request("/search/channels", {"query": query})

    def get_channel_followers(self, broadcaster_id: str, first: int = 100) -> dict:
        return self._request("/channels/followers", {"broadcaster_id": broadcaster_id, "first": first})

    def close(self): self.session.close()
    def __enter__(self): return self
    def __exit__(self, *args): self.close()
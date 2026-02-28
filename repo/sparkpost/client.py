"""
SparkPost Client - Email service
"""

import requests

class SparkpostError(Exception): pass
class APIError(SparkpostError): pass

class SparkpostClient:
    BASE_URL = "https://api.sparkpost.com/api/v1"

    def __init__(self, api_key: str, timeout: int = 30):
        self.session = requests.Session()
        self.timeout = timeout
        self.session.headers.update({"Authorization": api_key, "Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, data: dict = None, params: dict = None) -> dict:
        try:
            r = requests.request(method, f"{self.BASE_URL}{endpoint}", json=data, params=params, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise APIError(str(e))

    def schedule_transmission(self, template_id: str, recipients: dict, options: dict = None) -> dict:
        data = {"campaign_id": template_id, "recipients": recipients}
        if options: data["options"] = options
        return self._request("POST", "/transmissions", data)

    def delete_recipient_list(self, list_id: str) -> dict:
        return self._request("DELETE", f"/recipient-lists/{list_id}")

    def search_message_events(self, from_: str, to_: str, events: str = "bounce") -> dict:
        return self._request("GET", "/metrics/deliverability/message-events", params={"from": from_, "to": to_, "events": events})

    def close(self): self.session.close()
    def __enter__(self): return self
    def __exit__(self, *args): self.close()
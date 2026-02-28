"""
Google Forms API Client

Supports:
- Get form responses
- Get form details
- Create forms
"""

import requests
from typing import Optional, Dict, Any, List


class GoogleFormClient:
    """
    Google Forms client.

    Authentication: OAuth2 Access Token
    Base URL: https://forms.googleapis.com/v1
    """

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://forms.googleapis.com/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}/{endpoint}"
        try:
            resp = getattr(self.session, method.lower())(url, params=params, json=data if method != "GET" else None)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def get_form(self, form_id: str) -> Dict[str, Any]:
        """Get form details."""
        return self._request("GET", f"forms/{form_id}")

    def get_responses(self, form_id: str, page_token: Optional[str] = None) -> Dict[str, Any]:
        """Get form responses."""
        params = {}
        if page_token:
            params["pageToken"] = page_token
        return self._request("GET", f"forms/{form_id}/responses", params=params)

    def get_response(self, form_id: str, response_id: str) -> Dict[str, Any]:
        """Get single response."""
        return self._request("GET", f"forms/{form_id}/responses/{response_id}")

    def create_form(self, title: str) -> Dict[str, Any]:
        """Create a new form."""
        return self._request("POST", "forms", data={"info": {"title": title}})

    def batch_update(self, form_id: str, requests_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Batch update form with multiple requests."""
        return self._request("POST", f"forms/{form_id}:batchUpdate", data={"requests": requests_list})

    def create_watch(self, form_id: str, event_type: str, topic_name: str) -> Dict[str, Any]:
        """Create a watch on form for push notifications."""
        data = {
            "watch": {
                "target": {"topic": {"topicName": topic_name}},
                "eventType": event_type
            }
        }
        return self._request("POST", f"forms/{form_id}/watches", data=data)

    def close(self):
        self.session.close()


def main():
    client = GoogleFormClient(access_token="your_oauth_token")
    try:
        form = client.get_form("form_id_here")
        print(f"Form: {form}")
        responses = client.get_responses("form_id_here")
        print(f"Responses: {responses}")
        new_form = client.create_form("My New Form")
        print(f"Created: {new_form}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    main()

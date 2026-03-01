"""
Tally API Client

Supports:
- Get form responses
- List forms
- Delete responses
"""

import requests
from typing import Optional, Dict, Any, List


class TallyClient:
    """
    Tally client for form management.

    Authentication: API Key (Bearer token)
    Base URL: https://api.tally.so
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.tally.so"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
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

    def list_forms(self, page: int = 1, limit: int = 50) -> Dict[str, Any]:
        """List all forms."""
        return self._request("GET", "forms", params={"page": page, "limit": limit})

    def get_form(self, form_id: str) -> Dict[str, Any]:
        """Get form details."""
        return self._request("GET", f"forms/{form_id}")

    def get_responses(self, form_id: str, page: int = 1, limit: int = 50) -> Dict[str, Any]:
        """Get form responses."""
        return self._request("GET", f"forms/{form_id}/responses", params={"page": page, "limit": limit})

    def delete_response(self, response_id: str) -> Dict[str, Any]:
        """Delete a response."""
        return self._request("DELETE", f"responses/{response_id}")

    def close(self):
        self.session.close()


def main():
    client = TallyClient(api_key="your_key")
    try:
        forms = client.list_forms()
        print(f"Forms: {forms}")
        if forms.get("data"):
            responses = client.get_responses(forms["data"][0]["id"])
            print(f"Responses: {responses}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()

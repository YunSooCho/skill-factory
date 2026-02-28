"""
Formcrafts API Client

Supports:
- Get form submissions
- List forms
- Get form analytics
"""

import requests
from typing import Optional, Dict, Any, List


class FormcraftsClient:
    """
    Formcrafts client for form management.

    Authentication: API Key
    Base URL: https://api.formcrafts.com/v1
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.formcrafts.com/v1"
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

    def list_forms(self) -> List[Dict[str, Any]]:
        """List all forms."""
        result = self._request("GET", "forms")
        return result.get("forms", [])

    def get_form(self, form_id: str) -> Dict[str, Any]:
        """Get form details."""
        return self._request("GET", f"forms/{form_id}")

    def get_submissions(self, form_id: str, limit: int = 50, page: int = 1) -> List[Dict[str, Any]]:
        """Get form submissions."""
        result = self._request("GET", f"forms/{form_id}/submissions", params={"limit": limit, "page": page})
        return result.get("submissions", [])

    def get_submission(self, form_id: str, submission_id: str) -> Dict[str, Any]:
        """Get submission details."""
        return self._request("GET", f"forms/{form_id}/submissions/{submission_id}")

    def get_analytics(self, form_id: str) -> Dict[str, Any]:
        """Get form analytics."""
        return self._request("GET", f"forms/{form_id}/analytics")

    def export_submissions(self, form_id: str, format: str = "csv") -> Dict[str, Any]:
        """Export submissions."""
        return self._request("GET", f"forms/{form_id}/export", params={"format": format})

    def close(self):
        self.session.close()


def main():
    client = FormcraftsClient(api_key="your_key")
    try:
        forms = client.list_forms()
        print(f"Forms: {forms}")
        if forms:
            analytics = client.get_analytics(forms[0]["id"])
            print(f"Analytics: {analytics}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    main()

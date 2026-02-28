"""
Getform API Client

Supports:
- Get form submissions
- List forms
- Delete submissions
"""

import requests
from typing import Optional, Dict, Any, List


class GetformClient:
    """
    Getform client for form backend.

    Authentication: API Token
    Base URL: https://api.getform.io/v1
    """

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.getform.io/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_token}",
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
        return result.get("forms", []) if isinstance(result, dict) else result

    def get_form(self, form_id: str) -> Dict[str, Any]:
        """Get form details."""
        return self._request("GET", f"forms/{form_id}")

    def get_submissions(self, form_id: str, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Get form submissions."""
        result = self._request("GET", f"forms/{form_id}/submissions", params={"limit": limit, "offset": offset})
        return result.get("submissions", []) if isinstance(result, dict) else result

    def delete_submission(self, form_id: str, submission_id: str) -> Dict[str, Any]:
        """Delete a submission."""
        return self._request("DELETE", f"forms/{form_id}/submissions/{submission_id}")

    def export_submissions(self, form_id: str, format: str = "json") -> Any:
        """Export submissions."""
        return self._request("GET", f"forms/{form_id}/export", params={"format": format})

    def close(self):
        self.session.close()


def main():
    client = GetformClient(api_token="your_token")
    try:
        forms = client.list_forms()
        print(f"Forms: {forms}")
        if forms:
            subs = client.get_submissions(forms[0]["id"])
            print(f"Submissions: {subs}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    main()

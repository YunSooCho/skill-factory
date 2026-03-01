"""
Formrun API Client

Supports:
- Get form submissions
- List forms
- Update submission status
"""

import requests
from typing import Optional, Dict, Any, List


class FormrunClient:
    """
    Formrun client for form management (Japanese service).

    Authentication: API Key
    Base URL: https://api.form.run/api/v1
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.form.run/api/v1"
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

    def update_submission_status(self, form_id: str, submission_id: str, status: str) -> Dict[str, Any]:
        """Update submission status (e.g., unread, read, processing, done)."""
        return self._request("PUT", f"forms/{form_id}/submissions/{submission_id}", data={"status": status})

    def close(self):
        self.session.close()


def main():
    client = FormrunClient(api_key="your_key")
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

"""
Paperform API Client

Supports:
- Get form submissions
- List forms
- Get partial submissions
"""

import requests
from typing import Optional, Dict, Any, List


class PaperformClient:
    """
    Paperform client for form management.

    Authentication: API Key (Bearer token)
    Base URL: https://api.paperform.co/v1
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.paperform.co/v1"
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

    def list_forms(self, limit: int = 50) -> List[Dict[str, Any]]:
        """List all forms."""
        result = self._request("GET", "forms", params={"limit": limit})
        return result.get("results", [])

    def get_form(self, form_slug: str) -> Dict[str, Any]:
        """Get form details by slug."""
        return self._request("GET", f"forms/{form_slug}")

    def get_submissions(self, form_slug: str, limit: int = 50, before: Optional[str] = None) -> Dict[str, Any]:
        """Get form submissions."""
        params = {"limit": limit}
        if before:
            params["before"] = before
        return self._request("GET", f"forms/{form_slug}/submissions", params=params)

    def get_submission(self, submission_id: str) -> Dict[str, Any]:
        """Get submission details."""
        return self._request("GET", f"submissions/{submission_id}")

    def get_partial_submissions(self, form_slug: str, limit: int = 50) -> Dict[str, Any]:
        """Get partial (incomplete) submissions."""
        return self._request("GET", f"forms/{form_slug}/partial-submissions", params={"limit": limit})

    def close(self):
        self.session.close()


def main():
    client = PaperformClient(api_key="your_key")
    try:
        forms = client.list_forms()
        print(f"Forms: {forms}")
        if forms:
            subs = client.get_submissions(forms[0]["slug"])
            print(f"Submissions: {subs}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()

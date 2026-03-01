"""
MoreApp Forms API Client

Supports:
- Get form submissions
- List forms
- Export submissions
"""

import requests
from typing import Optional, Dict, Any, List


class MoreAppFormsClient:
    """
    MoreApp Forms client for mobile form management.

    Authentication: API Key
    Base URL: https://api.moreapp.com/api/v1.0
    """

    def __init__(self, api_key: str, customer_id: str):
        self.api_key = api_key
        self.customer_id = customer_id
        self.base_url = "https://api.moreapp.com/api/v1.0"
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key,
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
        """List all forms for the customer."""
        result = self._request("GET", f"customers/{self.customer_id}/forms")
        return result if isinstance(result, list) else result.get("forms", [])

    def get_form(self, form_id: str) -> Dict[str, Any]:
        """Get form details."""
        return self._request("GET", f"customers/{self.customer_id}/forms/{form_id}")

    def get_submissions(self, form_id: str, page: int = 0, size: int = 20) -> List[Dict[str, Any]]:
        """Get form submissions."""
        result = self._request("GET", f"customers/{self.customer_id}/forms/{form_id}/submissions",
                               params={"page": page, "size": size})
        return result.get("content", []) if isinstance(result, dict) else result

    def get_submission(self, submission_id: str) -> Dict[str, Any]:
        """Get submission details."""
        return self._request("GET", f"customers/{self.customer_id}/submissions/{submission_id}")

    def export_submissions(self, form_id: str, format: str = "json") -> Any:
        """Export form submissions."""
        return self._request("GET", f"customers/{self.customer_id}/forms/{form_id}/export",
                             params={"format": format})

    def close(self):
        self.session.close()


def main():
    client = MoreAppFormsClient(api_key="your_key", customer_id="your_customer_id")
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

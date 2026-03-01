"""
Formsite API Client

Supports:
- Get form results
- List forms
- Export results
"""

import requests
from typing import Optional, Dict, Any, List
import base64


class FormsiteClient:
    """
    Formsite client for form management.

    Authentication: API Token
    Base URL: https://{server}.formsite.com/api/v2/{user_dir}
    """

    def __init__(self, api_token: str, server: str = "fs1", user_dir: str = ""):
        self.api_token = api_token
        self.server = server
        self.user_dir = user_dir
        self.base_url = f"https://{server}.formsite.com/api/v2/{user_dir}"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"bearer {api_token}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}/{endpoint}"
        try:
            resp = getattr(self.session, method.lower())(url, params=params)
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

    def get_results(self, form_id: str, page: int = 1, per_page: int = 25,
                    after_date: Optional[str] = None, before_date: Optional[str] = None) -> Dict[str, Any]:
        """Get form results with pagination."""
        params = {"page": page, "per_page": per_page}
        if after_date:
            params["after_date"] = after_date
        if before_date:
            params["before_date"] = before_date
        return self._request("GET", f"forms/{form_id}/results", params=params)

    def get_result(self, form_id: str, result_id: str) -> Dict[str, Any]:
        """Get single result."""
        return self._request("GET", f"forms/{form_id}/results/{result_id}")

    def get_form_items(self, form_id: str) -> List[Dict[str, Any]]:
        """Get form items (fields)."""
        result = self._request("GET", f"forms/{form_id}/items")
        return result.get("items", [])

    def close(self):
        self.session.close()


def main():
    client = FormsiteClient(api_token="your_token", server="fs1", user_dir="your_dir")
    try:
        forms = client.list_forms()
        print(f"Forms: {forms}")
        if forms:
            results = client.get_results(forms[0]["id"])
            print(f"Results: {results}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    main()

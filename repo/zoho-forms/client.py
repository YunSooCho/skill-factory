"""
Zoho Forms API Client

Supports:
- Get form entries
- List forms
- Get form fields
"""

import requests
from typing import Optional, Dict, Any, List


class ZohoFormsClient:
    """
    Zoho Forms client for form management.

    Authentication: OAuth Token
    Base URL: https://forms.zoho.com/api/v1
    """

    def __init__(self, oauth_token: str):
        self.oauth_token = oauth_token
        self.base_url = "https://forms.zoho.com/api/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Zoho-oauthtoken {oauth_token}",
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

    def list_forms(self, limit: int = 50, start: int = 0) -> List[Dict[str, Any]]:
        """List all forms."""
        result = self._request("GET", "forms", params={"limit": limit, "start": start})
        return result.get("forms", [])

    def get_form(self, form_link_name: str) -> Dict[str, Any]:
        """Get form details."""
        return self._request("GET", f"forms/{form_link_name}")

    def get_entries(self, form_link_name: str, limit: int = 50, start: int = 0,
                    sort_by: Optional[str] = None, sort_order: str = "desc") -> List[Dict[str, Any]]:
        """Get form entries."""
        params = {"limit": limit, "start": start, "sort_order": sort_order}
        if sort_by:
            params["sort_by"] = sort_by
        result = self._request("GET", f"forms/{form_link_name}/entries", params=params)
        return result.get("entries", [])

    def get_entry(self, form_link_name: str, entry_id: str) -> Dict[str, Any]:
        """Get single entry."""
        return self._request("GET", f"forms/{form_link_name}/entries/{entry_id}")

    def get_fields(self, form_link_name: str) -> List[Dict[str, Any]]:
        """Get form fields."""
        result = self._request("GET", f"forms/{form_link_name}/fields")
        return result.get("fields", [])

    def create_entry(self, form_link_name: str, entry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new entry."""
        return self._request("POST", f"forms/{form_link_name}/entries", data=entry_data)

    def close(self):
        self.session.close()


def main():
    client = ZohoFormsClient(oauth_token="your_oauth_token")
    try:
        forms = client.list_forms()
        print(f"Forms: {forms}")
        if forms:
            form_link = forms[0]["formLinkName"]
            entries = client.get_entries(form_link)
            print(f"Entries: {entries}")
            fields = client.get_fields(form_link)
            print(f"Fields: {fields}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()

"""
Wufoo API Client

Supports:
- Get form entries
- List forms
- Get form fields
"""

import requests
from typing import Optional, Dict, Any, List
import base64


class WufooClient:
    """
    Wufoo client for form management.

    Authentication: API Key (HTTP Basic Auth)
    Base URL: https://{subdomain}.wufoo.com/api/v3
    """

    def __init__(self, api_key: str, subdomain: str):
        self.api_key = api_key
        self.subdomain = subdomain
        self.base_url = f"https://{subdomain}.wufoo.com/api/v3"
        self.session = requests.Session()
        # Wufoo uses HTTP Basic Auth with API key as username and any password
        self.session.auth = (api_key, "footastic")
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}/{endpoint}.json"
        try:
            resp = getattr(self.session, method.lower())(url, params=params, json=data if method != "GET" else None)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def list_forms(self) -> List[Dict[str, Any]]:
        """List all forms."""
        result = self._request("GET", "forms")
        return result.get("Forms", [])

    def get_form(self, form_hash: str) -> Dict[str, Any]:
        """Get form details by hash."""
        result = self._request("GET", f"forms/{form_hash}")
        forms = result.get("Forms", [])
        return forms[0] if forms else {}

    def get_entries(self, form_hash: str, page_start: int = 0, page_size: int = 25,
                    sort_id: Optional[str] = None, sort_direction: str = "ASC") -> List[Dict[str, Any]]:
        """Get form entries."""
        params = {"pageStart": page_start, "pageSize": page_size, "sortDirection": sort_direction}
        if sort_id:
            params["sort"] = sort_id
        result = self._request("GET", f"forms/{form_hash}/entries", params=params)
        return result.get("Entries", [])

    def get_entry_count(self, form_hash: str) -> int:
        """Get entry count for a form."""
        result = self._request("GET", f"forms/{form_hash}/entries/count")
        return result.get("EntryCount", 0)

    def get_fields(self, form_hash: str) -> List[Dict[str, Any]]:
        """Get form fields."""
        result = self._request("GET", f"forms/{form_hash}/fields")
        return result.get("Fields", [])

    def submit_entry(self, form_hash: str, entry_data: Dict[str, str]) -> Dict[str, Any]:
        """Submit an entry to a form."""
        return self._request("POST", f"forms/{form_hash}/entries", data=entry_data)

    def get_comments(self, form_hash: str, entry_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get form comments."""
        endpoint = f"forms/{form_hash}/comments"
        if entry_id:
            endpoint += f"/{entry_id}"
        result = self._request("GET", endpoint)
        return result.get("Comments", [])

    def close(self):
        self.session.close()


def main():
    client = WufooClient(api_key="your_key", subdomain="yoursubdomain")
    try:
        forms = client.list_forms()
        print(f"Forms: {forms}")
        if forms:
            form_hash = forms[0]["Hash"]
            fields = client.get_fields(form_hash)
            print(f"Fields: {fields}")
            entries = client.get_entries(form_hash)
            print(f"Entries: {entries}")
            count = client.get_entry_count(form_hash)
            print(f"Entry count: {count}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()

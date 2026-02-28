"""
Typeform API Client

Supports:
- Get form responses
- List forms
- Create forms
- Webhooks
"""

import requests
from typing import Optional, Dict, Any, List


class TypeformClient:
    """
    Typeform client for form management.

    Authentication: Personal Access Token
    Base URL: https://api.typeform.com
    """

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.typeform.com"
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

    def list_forms(self, page: int = 1, page_size: int = 10, workspace_id: Optional[str] = None) -> Dict[str, Any]:
        """List forms."""
        params = {"page": page, "page_size": page_size}
        if workspace_id:
            params["workspace_id"] = workspace_id
        return self._request("GET", "forms", params=params)

    def get_form(self, form_id: str) -> Dict[str, Any]:
        """Get form details."""
        return self._request("GET", f"forms/{form_id}")

    def create_form(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a form."""
        return self._request("POST", "forms", data=form_data)

    def update_form(self, form_id: str, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a form."""
        return self._request("PUT", f"forms/{form_id}", data=form_data)

    def delete_form(self, form_id: str) -> Dict[str, Any]:
        """Delete a form."""
        return self._request("DELETE", f"forms/{form_id}")

    def get_responses(self, form_id: str, page_size: int = 25, since: Optional[str] = None,
                      until: Optional[str] = None, after: Optional[str] = None) -> Dict[str, Any]:
        """Get form responses."""
        params = {"page_size": page_size}
        if since:
            params["since"] = since
        if until:
            params["until"] = until
        if after:
            params["after"] = after
        return self._request("GET", f"forms/{form_id}/responses", params=params)

    def delete_responses(self, form_id: str, included_tokens: List[str]) -> Dict[str, Any]:
        """Delete specific responses."""
        params = {"included_tokens": ",".join(included_tokens)}
        return self._request("DELETE", f"forms/{form_id}/responses", params=params)

    def create_webhook(self, form_id: str, tag: str, url: str, enabled: bool = True) -> Dict[str, Any]:
        """Create or update a webhook."""
        return self._request("PUT", f"forms/{form_id}/webhooks/{tag}", data={"url": url, "enabled": enabled})

    def get_webhooks(self, form_id: str) -> Dict[str, Any]:
        """Get webhooks for a form."""
        return self._request("GET", f"forms/{form_id}/webhooks")

    def close(self):
        self.session.close()


def main():
    client = TypeformClient(access_token="your_token")
    try:
        forms = client.list_forms()
        print(f"Forms: {forms}")
        if forms.get("items"):
            form_id = forms["items"][0]["id"]
            responses = client.get_responses(form_id)
            print(f"Responses: {responses}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()

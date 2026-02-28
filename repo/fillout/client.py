"""
Fillout API Client

Supports:
- Get form submissions
- List forms
- Create forms
- Webhook management
"""

import requests
from typing import Optional, Dict, Any, List


class FilloutClient:
    """
    Fillout client for form management.

    Authentication: API Key
    Base URL: https://api.fillout.com/v1/api
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.fillout.com/v1/api"
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
        return result if isinstance(result, list) else result.get("forms", [])

    def get_form(self, form_id: str) -> Dict[str, Any]:
        """Get form details."""
        return self._request("GET", f"forms/{form_id}")

    def get_submissions(self, form_id: str, limit: int = 50, offset: int = 0, after_date: Optional[str] = None) -> Dict[str, Any]:
        """Get form submissions with pagination."""
        params = {"limit": limit, "offset": offset}
        if after_date:
            params["afterDate"] = after_date
        return self._request("GET", f"forms/{form_id}/submissions", params=params)

    def create_webhook(self, form_id: str, url: str) -> Dict[str, Any]:
        """Create a webhook for a form."""
        return self._request("POST", f"forms/{form_id}/webhooks", data={"url": url})

    def delete_webhook(self, form_id: str, webhook_id: str) -> Dict[str, Any]:
        """Delete a webhook."""
        return self._request("DELETE", f"forms/{form_id}/webhooks/{webhook_id}")

    def close(self):
        self.session.close()


def main():
    client = FilloutClient(api_key="your_key")
    try:
        forms = client.list_forms()
        print(f"Forms: {forms}")
        if forms:
            form_id = forms[0]["formId"]
            subs = client.get_submissions(form_id)
            print(f"Submissions: {subs}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    main()

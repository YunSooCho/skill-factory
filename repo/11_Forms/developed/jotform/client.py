"""
JotForm API Client

Supports:
- Get form submissions
- List forms
- Get form questions
"""

import requests
from typing import Optional, Dict, Any, List


class JotFormClient:
    """
    JotForm client for form management.

    Authentication: API Key
    Base URL: https://api.jotform.com
    """

    def __init__(self, api_key: str, use_eu: bool = False):
        self.api_key = api_key
        host = "eu-api.jotform.com" if use_eu else "api.jotform.com"
        self.base_url = f"https://{host}"
        self.session = requests.Session()
        self.session.headers.update({
            "APIKEY": api_key,
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}/{endpoint}"
        try:
            resp = getattr(self.session, method.lower())(url, params=params, json=data if method != "GET" else None)
            resp.raise_for_status()
            result = resp.json()
            return result.get("content", result)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def list_forms(self, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """List user's forms."""
        result = self._request("GET", "user/forms", params={"limit": limit, "offset": offset})
        return result if isinstance(result, list) else []

    def get_form(self, form_id: str) -> Dict[str, Any]:
        """Get form details."""
        return self._request("GET", f"form/{form_id}")

    def get_submissions(self, form_id: str, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """Get form submissions."""
        result = self._request("GET", f"form/{form_id}/submissions", params={"limit": limit, "offset": offset})
        return result if isinstance(result, list) else []

    def get_submission(self, submission_id: str) -> Dict[str, Any]:
        """Get submission details."""
        return self._request("GET", f"submission/{submission_id}")

    def get_questions(self, form_id: str) -> Dict[str, Any]:
        """Get form questions."""
        return self._request("GET", f"form/{form_id}/questions")

    def create_submission(self, form_id: str, submission_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a submission."""
        return self._request("POST", f"form/{form_id}/submissions", data=submission_data)

    def delete_submission(self, submission_id: str) -> Dict[str, Any]:
        """Delete a submission."""
        return self._request("DELETE", f"submission/{submission_id}")

    def get_form_properties(self, form_id: str) -> Dict[str, Any]:
        """Get form properties."""
        return self._request("GET", f"form/{form_id}/properties")

    def close(self):
        self.session.close()


def main():
    client = JotFormClient(api_key="your_key")
    try:
        forms = client.list_forms()
        print(f"Forms: {forms}")
        if forms:
            form_id = forms[0]["id"]
            questions = client.get_questions(form_id)
            print(f"Questions: {questions}")
            subs = client.get_submissions(form_id)
            print(f"Submissions: {subs}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    main()

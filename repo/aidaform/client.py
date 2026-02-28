"""
AidaForm API Client

Supports:
- Get form submissions
- Get form details
- List forms
"""

import requests
from typing import Optional, Dict, Any, List


class AidaFormClient:
    """
    AidaForm client for form management.

    Authentication: API Token
    Base URL: https://api.aidaform.com/v1
    """

    def __init__(self, api_token: str):
        """
        Initialize AidaForm client.

        Args:
            api_token: AidaForm API Token
        """
        self.api_token = api_token
        self.base_url = "https://api.aidaform.com/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make API request with error handling"""
        url = f"{self.base_url}/{endpoint}"

        try:
            if method == "GET":
                response = self.session.get(url, params=params)
            elif method == "POST":
                response = self.session.post(url, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def list_forms(self) -> List[Dict[str, Any]]:
        """
        List all forms.

        Returns:
            List of forms
        """
        result = self._request("GET", "forms")
        return result.get("forms", [])

    def get_form_details(self, form_id: str) -> Dict[str, Any]:
        """
        Get form details.

        Args:
            form_id: Form ID

        Returns:
            Dict with form information
        """
        return self._request("GET", f"forms/{form_id}")

    def get_submissions(
        self,
        form_id: str,
        limit: int = 50,
        offset: int = 0,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get form submissions.

        Args:
            form_id: Form ID
            limit: Maximum number of submissions
            offset: Pagination offset
            status: Filter by status

        Returns:
            List of submissions
        """
        params = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status

        result = self._request("GET", f"forms/{form_id}/submissions", params=params)
        return result.get("submissions", [])

    def get_submission_detail(self, form_id: str, submission_id: str) -> Dict[str, Any]:
        """
        Get submission details.

        Args:
            form_id: Form ID
            submission_id: Submission ID

        Returns:
            Dict with submission information
        """
        return self._request("GET", f"forms/{form_id}/submissions/{submission_id}")

    def get_submission_count(self, form_id: str) -> Dict[str, Any]:
        """
        Get submission count for a form.

        Args:
            form_id: Form ID

        Returns:
            Dict with count information
        """
        return self._request("GET", f"forms/{form_id}/submissions/count")

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_token = "your_aidaform_token"

    client = AidaFormClient(api_token=api_token)

    try:
        # List forms
        forms = client.list_forms()
        print(f"Forms: {forms}")

        # Get form details
        if forms:
            form_id = forms[0]["id"]
            form = client.get_form_details(form_id)
            print(f"Form details: {form}")

            # Get submissions
            submissions = client.get_submissions(form_id, limit=10)
            print(f"Submissions: {submissions}")

            # Get submission count
            count = client.get_submission_count(form_id)
            print(f"Count: {count}")

            # Get submission detail
            if submissions:
                submission_id = submissions[0]["id"]
                detail = client.get_submission_detail(form_id, submission_id)
                print(f"Submission detail: {detail}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()
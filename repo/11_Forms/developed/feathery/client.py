"""
Feathery API Client

Supports:
- Get submissions
- Get form details
- List forms
- Create submission
"""

import requests
from typing import Optional, Dict, Any, List


class FeatheryClient:
    """
    Feathery client for form management.

    Authentication: API Key
    Base URL: https://api.feathery.io
    """

    def __init__(self, api_key: str):
        """
        Initialize Feathery client.

        Args:
            api_key: Feathery API Key
        """
        self.api_key = api_key
        self.base_url = "https://api.feathery.io"
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key,
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
            elif method == "PUT":
                response = self.session.put(url, json=data)
            elif method == "DELETE":
                response = self.session.delete(url, json=data)
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

    def get_form(self, form_id: str) -> Dict[str, Any]:
        """
        Get form details.

        Args:
            form_id: Form ID

        Returns:
            Dict with form information
        """
        return self._request("GET", f"forms/{form_id}")

    def create_submission(self, form_id: str, submission_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a submission.

        Args:
            form_id: Form ID
            submission_data: Submission data

        Returns:
            Dict with created submission
        """
        return self._request("POST", f"forms/{form_id}/submissions", data=submission_data)

    def get_submissions(
        self,
        form_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get form submissions.

        Args:
            form_id: Form ID
            limit: Maximum number of submissions
            offset: Pagination offset

        Returns:
            List of submissions
        """
        params = {"limit": limit, "offset": offset}
        result = self._request("GET", f"forms/{form_id}/submissions", params=params)
        return result.get("submissions", [])

    def get_submission(self, form_id: str, submission_id: str) -> Dict[str, Any]:
        """
        Get submission details.

        Args:
            form_id: Form ID
            submission_id: Submission ID

        Returns:
            Dict with submission information
        """
        return self._request("GET", f"forms/{form_id}/submissions/{submission_id}")

    def update_submission(
        self,
        form_id: str,
        submission_id: str,
        update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a submission.

        Args:
            form_id: Form ID
            submission_id: Submission ID
            update_data: Update data

        Returns:
            Dict with updated submission
        """
        return self._request("PUT", f"forms/{form_id}/submissions/{submission_id}", data=update_data)

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_feathery_key"

    client = FeatheryClient(api_key=api_key)

    try:
        # List forms
        forms = client.list_forms()
        print(f"Forms: {forms}")

        # Get form
        if forms:
            form_id = forms[0]["id"]
            form = client.get_form(form_id)
            print(f"Form: {form}")

            # Create submission
            submission = client.create_submission(
                form_id,
                {"name": "John Doe", "email": "john@example.com"}
            )
            print(f"Created: {submission}")

            # Get submissions
            submissions = client.get_submissions(form_id, limit=10)
            print(f"Submissions: {submissions}")

            # Get submission
            if submissions:
                submission_id = submissions[0]["id"]
                detail = client.get_submission(form_id, submission_id)
                print(f"Submission: {detail}")

                # Update submission
                updated = client.update_submission(form_id, submission_id, {"status": "reviewed"})
                print(f"Updated: {updated}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()
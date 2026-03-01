"""
Cognito Forms API Client

Supports:
- Get entries
- Get form information
- List forms
"""

import requests
from typing import Optional, Dict, Any, List


class CognitoFormsClient:
    """
    Cognito Forms client for form management.

    Authentication: API Key
    Base URL: https://www.cognitoforms.com/api
    """

    def __init__(self, api_key: str):
        """
        Initialize Cognito Forms client.

        Args:
            api_key: Cognito Forms API Key
        """
        self.api_key = api_key
        self.base_url = "https://www.cognitoforms.com/api"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
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
        return result if isinstance(result, list) else result.get("forms", [])

    def get_form(self, form_id: str) -> Dict[str, Any]:
        """
        Get form information.

        Args:
            form_id: Form ID

        Returns:
            Dict with form information
        """
        return self._request("GET", f"forms/{form_id}")

    def get_entries(
        self,
        form_id: str,
        limit: int = 100,
        offset: int = 0,
        filter_query: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get form entries.

        Args:
            form_id: Form ID
            limit: Maximum number of entries
            offset: Pagination offset
            filter_query: OData filter query

        Returns:
            List of entries
        """
        params = {
            "$top": limit,
            "$skip": offset
        }
        if filter_query:
            params["$filter"] = filter_query

        result = self._request("GET", f"forms/{form_id}/entries", params=params)
        return result if isinstance(result, list) else result.get("entries", [])

    def get_entry(self, form_id: str, entry_id: str) -> Dict[str, Any]:
        """
        Get specific entry.

        Args:
            form_id: Form ID
            entry_id: Entry ID

        Returns:
            Dict with entry information
        """
        return self._request("GET", f"forms/{form_id}/entries/{entry_id}")

    def create_entry(self, form_id: str, entry_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new entry.

        Args:
            form_id: Form ID
            entry_data: Entry data

        Returns:
            Dict with created entry
        """
        return self._request("POST", f"forms/{form_id}/entries", data=entry_data)

    def update_entry(self, form_id: str, entry_id: str, entry_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an entry.

        Args:
            form_id: Form ID
            entry_id: Entry ID
            entry_data: Updated entry data

        Returns:
            Dict with updated entry
        """
        return self._request("PUT", f"forms/{form_id}/entries/{entry_id}", data=entry_data)

    def delete_entry(self, form_id: str, entry_id: str) -> Dict[str, Any]:
        """
        Delete an entry.

        Args:
            form_id: Form ID
            entry_id: Entry ID

        Returns:
            Dict with result
        """
        return self._request("DELETE", f"forms/{form_id}/entries/{entry_id}")

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_cognito_forms_key"

    client = CognitoFormsClient(api_key=api_key)

    try:
        # List forms
        forms = client.list_forms()
        print(f"Forms: {forms}")

        # Get form
        if forms:
            form_id = forms[0].get("Id") if isinstance(forms[0], dict) else forms[0]
            form = client.get_form(form_id)
            print(f"Form: {form}")

            # Get entries
            entries = client.get_entries(form_id, limit=10)
            print(f"Entries: {entries}")

            # Get entry
            if entries:
                entry_id = entries[0].get("Id") if isinstance(entries[0], dict) else entries[0]
                entry = client.get_entry(form_id, entry_id)
                print(f"Entry: {entry}")

            # Create entry
            new_entry = client.create_entry(form_id, {"Name": "John Doe", "Email": "john@example.com"})
            print(f"Created: {new_entry}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()
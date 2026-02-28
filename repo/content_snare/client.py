"""
Content Snare API Client

Supports:
- Get requests
- Get request details
- List requests
"""

import requests
from typing import Optional, Dict, Any, List


class ContentSnareClient:
    """
    Content Snare client for content collection.

    Authentication: API Key
    Base URL: https://api.contentsnare.com
    """

    def __init__(self, api_key: str):
        """
        Initialize Content Snare client.

        Args:
            api_key: Content Snare API Key
        """
        self.api_key = api_key
        self.base_url = "https://api.contentsnare.com"
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
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def list_requests(
        self,
        status: Optional[str] = None,
        limit: int = 50,
        page: int = 1
    ) -> List[Dict[str, Any]]:
        """
        List content requests.

        Args:
            status: Filter by status
            limit: Maximum number of requests
            page: Page number

        Returns:
            List of requests
        """
        params = {"limit": limit, "page": page}
        if status:
            params["status"] = status

        result = self._request("GET", "requests", params=params)
        return result.get("requests", [])

    def get_request(self, request_id: str) -> Dict[str, Any]:
        """
        Get request details.

        Args:
            request_id: Request ID

        Returns:
            Dict with request information
        """
        return self._request("GET", f"requests/{request_id}")

    def get_request_documents(self, request_id: str) -> List[Dict[str, Any]]:
        """
        Get request documents.

        Args:
            request_id: Request ID

        Returns:
            List of documents
        """
        result = self._request("GET", f"requests/{request_id}/documents")
        return result.get("documents", [])

    def create_request(self, client_email: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new request.

        Args:
            client_email: Client email address
            request_data: Request data

        Returns:
            Dict with created request
        """
        data = {
            "client_email": client_email,
            "request": request_data
        }
        return self._request("POST", "requests", data=data)

    def update_request(self, request_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a request.

        Args:
            request_id: Request ID
            update_data: Update data

        Returns:
            Dict with updated request
        """
        return self._request("PUT", f"requests/{request_id}", data=update_data)

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_content_snare_key"

    client = ContentSnareClient(api_key=api_key)

    try:
        # List requests
        requests = client.list_requests(limit=10)
        print(f"Requests: {requests}")

        # Get request details
        if requests:
            request_id = requests[0]["id"]
            request = client.get_request(request_id)
            print(f"Request: {request}")

            # Get documents
            documents = client.get_request_documents(request_id)
            print(f"Documents: {documents}")

        # Create request
        new_request = client.create_request(
            client_email="client@example.com",
            request_data={"title": "New Request", "description": "Request details"}
        )
        print(f"Created: {new_request}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()
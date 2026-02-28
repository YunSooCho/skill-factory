import requests
import json
from typing import Dict, List, Optional, Any


class SignableClient:
    """Client for Signable e-signature API."""

    BASE_URL = "https://api.signable.co.uk/v1"

    def __init__(self, api_key: str, api_version: str = "v1"):
        """
        Initialize Signable client.

        Args:
            api_key: Your Signable API key
            api_version: API version (default: v1)
        """
        self.api_key = api_key
        self.base_url = f"https://api.signable.co.uk/{api_version}"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                 files: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to Signable API."""
        url = f"{self.base_url}{endpoint}"
        try:
            if files:
                response = self.session.request(method, url, files=files, data=data)
            else:
                response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def list_documents(self, limit: int = 50) -> Dict[str, Any]:
        """List all documents."""
        return self._request("GET", f"/documents?limit={limit}")

    def create_document(self, title: str, file_path: str) -> Dict[str, Any]:
        """Create a new document from file."""
        with open(file_path, 'rb') as f:
            files = {'file': (title, f, 'application/pdf')}
            data = {'title': title}
            return self._request("POST", "/documents", data=data, files=files)

    def get_document(self, doc_id: int) -> Dict[str, Any]:
        """Get document details."""
        return self._request("GET", f"/documents/{doc_id}")

    def delete_document(self, doc_id: int) -> Dict[str, Any]:
        """Delete a document."""
        return self._request("DELETE", f"/documents/{doc_id}")

    def get_document_url(self, doc_id: int) -> Dict[str, Any]:
        """Get document signing URL."""
        return self._request("GET", f"/documents/{doc_id}/url")

    def list_signers(self, doc_id: int) -> Dict[str, Any]:
        """List associated signers for a document."""
        return self._request("GET", f"/documents/{doc_id}/signers")

    def create_signer(self, doc_id: int, name: str, email: str) -> Dict[str, Any]:
        """Add a signer to a document."""
        data = {
            "signer": {
                "name": name,
                "email": email
            }
        }
        return self._request("POST", f"/documents/{doc_id}/signers", data=data)

    def send_document(self, doc_id: int) -> Dict[str, Any]:
        """Send document for signature."""
        return self._request("POST", f"/documents/{doc_id}/send")
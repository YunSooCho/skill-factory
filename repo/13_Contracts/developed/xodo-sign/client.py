import requests
from typing import Dict, List, Optional, Any


class XodoSignClient:
    """Client for Xodo Sign electronic signature API."""

    BASE_URL = "https://api.xodo.com/sign/v1"

    def __init__(self, api_key: str):
        """
        Initialize Xodo Sign client.

        Args:
            api_key: Your Xodo Sign API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                 files: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to Xodo Sign API."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            if files:
                response = self.session.request(method, url, files=files, data=data)
            else:
                response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def send_for_signature(self, file_path: str, recipient_email: str,
                          recipient_name: str = None, subject: str = "Please sign",
                          message: str = "") -> Dict[str, Any]:
        """Send document for signature."""
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.split('/')[-1], f, 'application/pdf')}
            data = {
                'recipient_email': recipient_email,
                'recipient_name': recipient_name,
                'subject': subject,
                'message': message
            }
            return self._request("POST", "/documents/send", data=data, files=files)

    def get_document(self, doc_id: str) -> Dict[str, Any]:
        """Get document details."""
        return self._request("GET", f"/documents/{doc_id}")

    def get_document_status(self, doc_id: str) -> Dict[str, Any]:
        """Get document signing status."""
        return self._request("GET", f"/documents/{doc_id}/status")

    def get_documents(self, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """List all documents."""
        return self._request("GET", f"/documents?limit={limit}&offset={offset}")

    def download_document(self, doc_id: str, output_path: str) -> bool:
        """Download signed document."""
        url = f"{self.BASE_URL}/documents/{doc_id}/download"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        except requests.RequestException:
            return False

    def cancel_signing(self, doc_id: str) -> Dict[str, Any]:
        """Cancel a signing request."""
        return self._request("POST", f"/documents/{doc_id}/cancel")

    def delete_document(self, doc_id: str) -> Dict[str, Any]:
        """Delete a document."""
        return self._request("DELETE", f"/documents/{doc_id}")

    def create_template(self, name: str, file_path: str) -> Dict[str, Any]:
        """Create a template from document."""
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.split('/')[-1], f, 'application/pdf')}
            data = {'name': name}
            return self._request("POST", "/templates", data=data, files=files)

    def get_templates(self) -> Dict[str, Any]:
        """List all templates."""
        return self._request("GET", "/templates")

    def send_template(self, template_id: str, recipient_email: str,
                     fields: Optional[Dict] = None) -> Dict[str, Any]:
        """Send template for signing."""
        data = {
            "recipient_email": recipient_email,
            "fields": fields or {}
        }
        return self._request("POST", f"/templates/{template_id}/send", data=data)

    def get_audit_trail(self, doc_id: str) -> Dict[str, Any]:
        """Get document audit trail."""
        return self._request("GET", f"/documents/{doc_id}/audit")
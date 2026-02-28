import requests
from typing import Dict, List, Optional, Any


class WanSignClient:
    """Client for Wan-Sign digital signature API."""

    BASE_URL = "https://api.wansign.com/api"

    def __init__(self, api_key: str):
        """
        Initialize Wan-Sign client.

        Args:
            api_key: Your Wan-Sign API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"ApiKey {api_key}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                 files: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to Wan-Sign API."""
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

    def upload_and_sign(self, document_path: str, signers: List[Dict],
                       title: str = "") -> Dict[str, Any]:
        """Upload document and setup signers."""
        with open(document_path, 'rb') as f:
            files = {'document': (document_path.split('/')[-1], f, 'application/pdf')}
            data = {
                'signers': signers,
                'title': title or document_path.split('/')[-1]
            }
            return self._request("POST", "/signing/upload", data=data, files=files)

    def get_document_status(self, doc_id: str) -> Dict[str, Any]:
        """Get signing status of a document."""
        return self._request("GET", f"/signing/{doc_id}/status")

    def get_document(self, doc_id: str) -> Dict[str, Any]:
        """Get document details."""
        return self._request("GET", f"/signing/{doc_id}")

    def cancel_document(self, doc_id: str) -> Dict[str, Any]:
        """Cancel a signing request."""
        return self._request("POST", f"/signing/{doc_id}/cancel")

    def send_reminder(self, doc_id: str, signer_id: str) -> Dict[str, Any]:
        """Send reminder to signer."""
        return self._request("POST", f"/signing/{doc_id}/remind", data={"signer_id": signer_id})

    def download_signed(self, doc_id: str, output_path: str) -> bool:
        """Download signed document."""
        url = f"{self.BASE_URL}/signing/{doc_id}/download"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        except requests.RequestException:
            return False

    def list_documents(self, page: int = 1, per_page: int = 50) -> Dict[str, Any]:
        """List all documents."""
        return self._request("GET", f"/signing?page={page}&per_page={per_page}")

    def create_template(self, name: str, document_path: str) -> Dict[str, Any]:
        """Create a document template."""
        with open(document_path, 'rb') as f:
            files = {'document': (document_path.split('/')[-1], f, 'application/pdf')}
            data = {'name': name}
            return self._request("POST", "/templates", data=data, files=files)

    def use_template(self, template_id: str, signers: List[Dict], fields: Optional[Dict] = None) -> Dict[str, Any]:
        """Create signing request from template."""
        data = {
            "signers": signers,
            "fields": fields or {}
        }
        return self._request("POST", f"/templates/{template_id}/use", data=data)

    def get_webhook_events(self) -> Dict[str, Any]:
        """Get recent webhook events."""
        return self._request("GET", "/webhooks/events")
import requests
import json
from typing import Dict, List, Optional, Any


class SignTimeClient:
    """Client for SignTime electronic signature API."""

    BASE_URL = "https://api.signtime.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize SignTime client.

        Args:
            api_key: Your SignTime API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                 files: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to SignTime API."""
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

    def create_signing_request(self, document_path: str, recipients: List[str],
                              subject: str = "Please sign this document",
                              message: str = "") -> Dict[str, Any]:
        """Create a new signing request."""
        with open(document_path, 'rb') as f:
            files = {'document': (document_path.split('/')[-1], f, 'application/pdf')}
            data = {
                'recipients': json.dumps(recipients),
                'subject': subject,
                'message': message
            }
            return self._request("POST", "/signatures", data=data, files=files)

    def get_status(self, request_id: str) -> Dict[str, Any]:
        """Get status of a signing request."""
        return self._request("GET", f"/signatures/{request_id}")

    def get_signers(self, request_id: str) -> Dict[str, Any]:
        """Get signer information for a request."""
        return self._request("GET", f"/signatures/{request_id}/signers")

    def resend_email(self, request_id: str, email: str) -> Dict[str, Any]:
        """Resend signing email to a recipient."""
        data = {"email": email}
        return self._request("POST", f"/signatures/{request_id}/resend", data=data)

    def cancel_request(self, request_id: str) -> Dict[str, Any]:
        """Cancel a signing request."""
        return self._request("DELETE", f"/signatures/{request_id}")

    def download_document(self, request_id: str, output_path: str) -> bool:
        """Download signed document."""
        url = f"{self.BASE_URL}/signatures/{request_id}/download"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        except requests.RequestException:
            return False

    def list_requests(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """List all signing requests."""
        return self._request("GET", f"/signatures?limit={limit}&offset={offset}")

    def get_template(self, template_id: str) -> Dict[str, Any]:
        """Get template details."""
        return self._request("GET", f"/templates/{template_id}")

    def create_from_template(self, template_id: str, recipients: List[str],
                            fields: Optional[Dict] = None) -> Dict[str, Any]:
        """Create signing request from template."""
        data = {
            "recipients": recipients,
            "fields": fields or {}
        }
        return self._request("POST", f"/templates/{template_id}/sign", data=data)
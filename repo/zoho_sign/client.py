import requests
from typing import Dict, List, Optional, Any


class ZohoSignClient:
    """Client for Zoho Sign electronic signature API."""

    BASE_URL = "https://sign.zoho.com/api/v1"

    def __init__(self, authtoken: str, email: str):
        """
        Initialize Zoho Sign client.

        Args:
            authtoken: Your Zoho Sign authtoken
            email: Your Zoho account email
        """
        self.authtoken = authtoken
        self.email = email
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Zoho-oauthtoken {authtoken}"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                 files: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to Zoho Sign API."""
        url = f"{self.BASE_URL}{endpoint}"
        if params is None:
            params = {}
        try:
            if files:
                response = self.session.request(method, url, files=files, data=data, params=params)
            else:
                response = self.session.request(method, url, json=data, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def create_document(self, file_path: str, recipient: str, recipient_name: str = None,
                       template_id: str = None) -> Dict[str, Any]:
        """Create document and send for signature."""
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.split('/')[-1], f, 'application/pdf')}
            data = {
                "action": "createandandsign",
                "request_name": file_path.split('/')[-1]
            }
            if recipient:
                data["recipients"] = {
                    "0": {
                        "recipient_name": recipient_name or recipient,
                        "recipient_email": recipient,
                        "action_type": "sign"
                    }
                }
            if template_id:
                data["template_id"] = template_id
            return self._request("POST", "/requests", data=data, files=files)

    def get_request(self, request_id: str) -> Dict[str, Any]:
        """Get request details."""
        return self._request("GET", f"/requests/{request_id}")

    def list_requests(self, status: str = None, limit: int = 100) -> Dict[str, Any]:
        """List all requests."""
        params = {"limit": limit}
        if status:
            params["status"] = status
        return self._request("GET", "/requests", params=params)

    def get_status(self, request_id: str) -> Dict[str, Any]:
        """Get request status."""
        return self._request("GET", f"/requests/{request_id}/status")

    def send_reminder(self, request_id: str, recipient_id: str = None) -> Dict[str, Any]:
        """Send reminder for signing."""
        data = {"recipient_id": recipient_id} if recipient_id else {}
        return self._request("POST", f"/requests/{request_id}/reminder", data=data)

    def download_document(self, request_id: str, output_path: str, pdf_type: str = "completed") -> bool:
        """Download signed document."""
        url = f"{self.BASE_URL}/requests/{request_id}/pdflink"
        params = {"pdf_type": pdf_type}
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            result = response.json()
            if "pdflink" in result:
                pdf_response = self.session.get(result["pdflink"])
                with open(output_path, 'wb') as f:
                    f.write(pdf_response.content)
                return True
            return False
        except requests.RequestException:
            return False

    def cancel_request(self, request_id: str) -> Dict[str, Any]:
        """Cancel a signature request."""
        return self._request("DELETE", f"/requests/{request_id}")

    def get_templates(self) -> Dict[str, Any]:
        """List all templates."""
        return self._request("GET", "/templates")

    def get_template(self, template_id: str) -> Dict[str, Any]:
        """Get template details."""
        return self._request("GET", f"/templates/{template_id}")

    def create_from_template(self, template_id: str, recipients: List[Dict]) -> Dict[str, Any]:
        """Create request from template."""
        data = {
            "template_ids": [template_id],
            "recipients": recipients
        }
        return self._request("POST", "/templates", data=data)
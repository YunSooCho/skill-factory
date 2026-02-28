import requests
from typing import Dict, List, Optional, Any


class YouSignClient:
    """Client for YouSign electronic signature API."""

    BASE_URL_SANDBOX = "https://api-sandbox.yousign.com"
    BASE_URL_PROD = "https://api.yousign.com"
    VERSION = "v3"

    def __init__(self, api_key: str, mode: str = "prod"):
        """
        Initialize YouSign client.

        Args:
            api_key: Your YouSign API key
            mode: 'prod' or 'sandbox' (default: 'prod')
        """
        self.api_key = api_key
        self.base_url = f"{self.BASE_URL_PROD if mode == 'prod' else self.BASE_URL_SANDBOX}/{self.VERSION}"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                 files: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to YouSign API."""
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

    def create_procedure(self, name: str, workflow: List[Dict],
                        description: str = "") -> Dict[str, Any]:
        """Create a signature procedure."""
        data = {
            "name": name,
            "description": description,
            "workflow": workflow
        }
        return self._request("POST", "/signature_procedures", data=data)

    def get_procedure(self, procedure_id: str) -> Dict[str, Any]:
        """Get procedure details."""
        return self._request("GET", f"/signature_procedures/{procedure_id}")

    def list_procedures(self, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """List all signature procedures."""
        return self._request("GET", f"/signature_procedures?limit={limit}&offset={offset}")

    def add_document(self, procedure_id: str, file_path: str) -> Dict[str, Any]:
        """Add document to procedure."""
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.split('/')[-1], f, 'application/pdf')}
            data = {
                "procedure": procedure_id,
                'name': file_path.split('/')[-1]
            }
            return self._request("POST", "/signature_procedures/documents", data=data, files=files)

    def start_procedure(self, procedure_id: str) -> Dict[str, Any]:
        """Start a signature procedure."""
        endpoints = self._request("POST", f"/signature_procedures/{procedure_id}/start")
        return endpoints

    def cancel_procedure(self, procedure_id: str) -> Dict[str, Any]:
        """Cancel a signature procedure."""
        return self._request("DELETE", f"/signature_procedures/{procedure_id}")

    def download_document(self, file_id: str, output_path: str) -> bool:
        """Download document."""
        url = f"{self.base_url}/signature_procedures/documents/{file_id}/download"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        except requests.RequestException:
            return False

    def download_coe(self, procedure_id: str, output_path: str) -> bool:
        """Download Certificate of Electronic Signature."""
        url = f"{self.base_url}/signature_procedures/{procedure_id}/certificates/download"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        except requests.RequestException:
            return False

    def get_audit_trail(self, procedure_id: str) -> Dict[str, Any]:
        """Get procedure audit trail."""
        return self._request("GET", f"/signature_procedures/{procedure_id}/audit_trails")

    def check_status(self, procedure_id: str) -> Dict[str, Any]:
        """Check procedure status."""
        return self._request("GET", f"/signature_procedures/{procedure_id}/status")
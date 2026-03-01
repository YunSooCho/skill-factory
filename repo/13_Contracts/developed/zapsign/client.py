import requests
from typing import Dict, List, Optional, Any


class ZapSignClient:
    """Client for ZapSign electronic signature API."""

    BASE_URL = "https://app.zapsign.com.br/api/v1"

    def __init__(self, api_token: str):
        """
        Initialize ZapSign client.

        Args:
            api_token: Your ZapSign API token
        """
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "multipart/form-data; charset=utf-8; boundary=__X_PAW_BOUNDARY__"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                 files: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to ZapSign API."""
        url = f"{self.BASE_URL}{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_token}"}
        try:
            if files:
                headers["Content-Type"] = None
                response = requests.request(method, url, headers=headers, files=files, data=data)
            else:
                headers["Content-Type"] = "application/json"
                response = requests.request(method, url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def upload_pdf(self, pdf_path: str, signers: List[Dict],
                  name: str = None, months_until_deletion: int = 1,
                  signed_file_only_once: bool = False) -> Dict[str, Any]:
        """Upload PDF document for signature."""
        with open(pdf_path, 'rb') as f:
            files = {'file': (pdf_path.split('/')[-1], f, 'application/pdf')}
            data = {
                'signers': str(signers),
                'name': name or pdf_path.split('/')[-1],
                'months_until_deletion': months_until_deletion,
                'signed_file_only_once': str(signed_file_only_once).lower()
            }
            return self._request("POST", "/docs", data=data, files=files)

    def get_doc(self, doc_id: str) -> Dict[str, Any]:
        """Get document details."""
        return self._request("GET", f"/docs/{doc_id}")

    def list_docs(self, page_number: int = 1) -> Dict[str, Any]:
        """List all documents."""
        return self._request("GET", f"/docs?page={page_number}")

    def sign(self, doc_id: str) -> Dict[str, Any]:
        """Trigger signing process."""
        return self._request("POST", f"/docs/{doc_id}/upload_pdf_base64")

    def cancel_signature(self, doc_id: str) -> Dict[str, Any]:
        """Cancel document signature."""
        return self._request("DELETE", f"/docs/{doc_id}/cancel_signature")

    def download_signed(self, doc_id: str, output_path: str) -> bool:
        """Download signed document."""
        url = f"{self.BASE_URL}/docs/{doc_id}/blob"
        headers = {"Authorization": f"Bearer {self.api_token}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        except requests.RequestException:
            return False

    def add_signer(self, doc_id: str, signer: Dict) -> Dict[str, Any]:
        """Add signer to document."""
        data = {"signer": signer}
        return self._request("POST", f"/docs/{doc_id}/add_signer", data=data)

    def remove_signer(self, doc_id: str, signer_key: str) -> Dict[str, Any]:
        """Remove signer from document."""
        return self._request("DELETE", f"/docs/{doc_id}/remove_signer/{signer_key}")
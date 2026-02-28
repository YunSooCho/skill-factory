"""
ZeroCodeKit API Client - Utility Tools Service
"""

import requests
import time
import base64
from typing import Optional, Dict, Any, List, Union


class ZeroCodeKitError(Exception):
    """Base exception for ZeroCodeKit errors"""
    pass


class ZeroCodeKitRateLimitError(ZeroCodeKitError):
    """Rate limit exceeded"""
    pass


class ZeroCodeKitAuthenticationError(ZeroCodeKitError):
    """Authentication failed"""
    pass


class ZeroCodeKitClient:
    """Client for ZeroCodeKit Utility API"""

    BASE_URL = "https://api.zerocodekit.com/v1"

    def __init__(self, api_key: str, timeout: int = 60):
        """
        Initialize ZeroCodeKit client

        Args:
            api_key: ZeroCodeKit API key
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
        self.min_delay = 0.1
        self.last_request_time = 0

    def _enforce_rate_limit(self):
        """Enforce rate limiting between requests"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request < self.min_delay:
            time.sleep(self.min_delay - time_since_last_request)

        self.last_request_time = time.time()

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        if response.status_code == 429:
            raise ZeroCodeKitRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise ZeroCodeKitAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', or error_data.get('error', ''))
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise ZeroCodeKitError(f"API error ({response.status_code}): {error_msg}")

        return response.json()

    def convert_docx_to_pdf(self, docx_data: Union[str, bytes]) -> Dict[str, Any]:
        """Convert DOCX to PDF"""
        self._enforce_rate_limit()

        if isinstance(docx_data, str):
            with open(docx_data, 'rb') as f:
                docx_b64 = base64.b64encode(f.read()).decode('utf-8')
        else:
            docx_b64 = base64.b64encode(docx_data).decode('utf-8')

        payload = {"docx": f"data:application/docx;base64,{docx_b64}"}

        try:
            response = self.session.post(
                f"{self.BASE_URL}/convert/docx-to-pdf",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")

    def generate_random_string(self, length: int = 10,
                                 include_numbers: bool = True,
                                 include_symbols: bool = False) -> Dict[str, Any]:
        """Generate random string"""
        self._enforce_rate_limit()

        payload = {
            "length": length,
            "include_numbers": include_numbers,
            "include_symbols": include_symbols
        }

        try:
            response = self.session.post(
                f"{self.BASE_URL}/generate/random-string",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")

    def check_free_email(self, email: str) -> Dict[str, Any]:
        """Check if email is from free email provider"""
        self._enforce_rate_limit()

        payload = {"email": email}

        try:
            response = self.session.post(
                f"{self.BASE_URL}/check/free-email",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")

    def split_pdf(self, pdf_data: Union[str, bytes], pages: List[int]) -> Dict[str, Any]:
        """Split PDF by pages"""
        self._enforce_rate_limit()

        if isinstance(pdf_data, str):
            with open(pdf_data, 'rb') as f:
                pdf_b64 = base64.b64encode(f.read()).decode('utf-8')
        else:
            pdf_b64 = base64.b64encode(pdf_data).decode('utf-8')

        payload = {
            "pdf": f"data:application/pdf;base64,{pdf_b64}",
            "pages": pages
        }

        try:
            response = self.session.post(
                f"{self.BASE_URL}/pdf/split",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")

    def generate_barcode(self, data: str, barcode_type: str = "QR") -> Dict[str, Any]:
        """Generate barcode"""
        self._enforce_rate_limit()

        payload = {"data": data, "type": barcode_type}

        try:
            response = self.session.post(
                f"{self.BASE_URL}/generate/barcode",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")

    def convert_timezone(self, datetime_str: str,
                         from_timezone: str, to_timezone: str) -> Dict[str, Any]:
        """Convert timezone"""
        self._enforce_rate_limit()

        payload = {
            "datetime": datetime_str,
            "from_timezone": from_timezone,
            "to_timezone": to_timezone
        }

        try:
            response = self.session.post(
                f"{self.BASE_URL}/convert/timezone",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")

    def generate_image(self, prompt: str, size: str = "1024x1024") -> Dict[str, Any]:
        """Generate image from prompt"""
        self._enforce_rate_limit()

        payload = {"prompt": prompt, "size": size}

        try:
            response = self.session.post(
                f"{self.BASE_URL}/generate/image",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")

    def pdf_to_base64(self, pdf_data: Union[str, bytes]) -> Dict[str, Any]:
        """Convert PDF to base64"""
        self._enforce_rate_limit()

        if isinstance(pdf_data, str):
            with open(pdf_data, 'rb') as f:
                pdf_b64 = base64.b64encode(f.read()).decode('utf-8')
        else:
            pdf_b64 = base64.b64encode(pdf_data).decode('utf-8')

        payload = {"pdf": f"data:application/pdf;base64,{pdf_b64}"}

        try:
            response = self.session.post(
                f"{self.BASE_URL}/convert/pdf-to-base64",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")

    def html_to_pdf(self, html_content: str, url: Optional[str] = None) -> Dict[str, Any]:
        """Convert HTML/URL to PDF"""
        self._enforce_rate_limit()

        payload = {"html": html_content}

        if url:
            payload["url"] = url

        try:
            response = self.session.post(
                f"{self.BASE_URL}/convert/html-to-pdf",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")

    def split_name(self, full_name: str) -> Dict[str, Any]:
        """Split full name into components"""
        self._enforce_rate_limit()

        payload = {"name": full_name}

        try:
            response = self.session.post(
                f"{self.BASE_URL}/parse/name",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")

    def generate_number(self, min_val: int = 0, max_val: int = 100) -> Dict[str, Any]:
        """Generate random number"""
        self._enforce_rate_limit()

        payload = {"min": min_val, "max": max_val}

        try:
            response = self.session.post(
                f"{self.BASE_URL}/generate/number",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")

    def upload_temp_file(self, file_data: Union[str, bytes],
                          filename: str,
                          content_type: str) -> Dict[str, Any]:
        """Upload file to temporary storage"""
        self._enforce_rate_limit()

        if isinstance(file_data, str):
            with open(file_data, 'rb') as f:
                file_b64 = base64.b64encode(f.read()).decode('utf-8')
        else:
            file_b64 = base64.b64encode(file_data).decode('utf-8')

        payload = {
            "file": f"data:{content_type};base64,{file_b64}",
            "filename": filename
        }

        try:
            response = self.session.post(
                f"{self.BASE_URL}/storage/upload",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")

    def hash_text(self, text: str, algorithm: str = "sha256") -> Dict[str, Any]:
        """Generate hash from text"""
        self._enforce_rate_limit()

        payload = {"text": text, "algorithm": algorithm}

        try:
            response = self.session.post(
                f"{self.BASE_URL}/hash/text",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")

    def get_logo_url(self, domain: str) -> Dict[str, Any]:
        """Get logo URL for domain"""
        self._enforce_rate_limit()

        payload = {"domain": domain}

        try:
            response = self.session.post(
                f"{self.BASE_URL}/get/logo-url",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")

    def pdf_to_image(self, pdf_data: Union[str, bytes], page: int = 1) -> Dict[str, Any]:
        """Convert PDF to image"""
        self._enforce_rate_limit()

        if isinstance(pdf_data, str):
            with open(pdf_data, 'rb') as f:
                pdf_b64 = base64.b64encode(f.read()).decode('utf-8')
        else:
            pdf_b64 = base64.b64encode(pdf_data).decode('utf-8')

        payload = {"pdf": f"data:application/pdf;base64,{pdf_b64}", "page": page}

        try:
            response = self.session.post(
                f"{self.BASE_URL}/convert/pdf-to-image",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")

    def generate_python_code(self, prompt: str) -> Dict[str, Any]:
        """Generate Python code from prompt"""
        self._enforce_rate_limit()

        payload = {"prompt": prompt, "language": "python"}

        try:
            response = self.session.post(
                f"{self.BASE_URL}/generate/code",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")

    def ip_to_geolocation(self, ip_address: str) -> Dict[str, Any]:
        """Convert IP address to geolocation data"""
        self._enforce_rate_limit()

        payload = {"ip": ip_address}

        try:
            response = self.session.post(
                f"{self.BASE_URL}/lookup/ip",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")

    def generate_javascript_code(self, prompt: str) -> Dict[str, Any]:
        """Generate JavaScript code from prompt"""
        self._enforce_rate_limit()

        payload = {"prompt": prompt, "language": "javascript"}

        try:
            response = self.session.post(
                f"{self.BASE_URL}/generate/code",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")

    def generate_qrcode(self, data: str, size: int = 200) -> Dict[str, Any]:
        """Generate QR code"""
        self._enforce_rate_limit()

        payload = {"data": data, "size": size}

        try:
            response = self.session.post(
                f"{self.BASE_URL}/generate/qrcode",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")

    def get_thumbnail(self, url: str, width: int = 200, height: int = 200) -> Dict[str, Any]:
        """Get thumbnail for URL"""
        self._enforce_rate_limit()

        payload = {"url": url, "width": width, "height": height}

        try:
            response = self.session.post(
                f"{self.BASE_URL}/get/thumbnail",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")

    def html_to_image(self, html_content: str, url: Optional[str] = None) -> Dict[str, Any]:
        """Convert HTML/URL to image"""
        self._enforce_rate_limit()

        payload = {"html": html_content}

        if url:
            payload["url"] = url

        try:
            response = self.session.post(
                f"{self.BASE_URL}/convert/html-to-image",
                json=payload,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            raise ZeroCodeKitError(f"Request failed: {str(e)}")
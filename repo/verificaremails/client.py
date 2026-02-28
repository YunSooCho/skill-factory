"""
Verificaremails Client - Email validation
"""

import requests

class VerificaremailsError(Exception): pass
class APIError(VerificaremailsError): pass

class VerificaremailsClient:
    BASE_URL = "https://api.verificaremails.com/v"

    def __init__(self, api_key: str, timeout: int = 30):
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()

    def validate_single_email(self, email: str) -> dict:
        try:
            r = requests.get(f"{self.BASE_URL}/1/check?apikey={self.api_key}&email={email}", timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise APIError(str(e))

    def close(self): self.session.close()
    def __enter__(self): return self
    def __exit__(self, *args): self.close()
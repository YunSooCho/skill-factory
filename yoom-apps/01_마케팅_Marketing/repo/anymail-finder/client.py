"""
Anymail Finder API Client
"""

import logging
import requests
from typing import List, Optional, Dict, Any
from .models import Person, EmailResult, EmailValidation

logger = logging.getLogger(__name__)


class AnymailFinderClient:
    """
    Anymail Finder Client for Yoom Integration

    API Actions:
    - Search for Person's Email
    - Search for Company's Email
    - Validate Email
    """

    BASE_URL = "https://api.anymailfind.com/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"AnymailFinder Error: {e}")
            raise

    def search_person_email(
        self,
        first_name: str,
        last_name: str,
        company: Optional[str] = None,
        domain: Optional[str] = None
    ) -> EmailResult:
        data = {'first_name': first_name, 'last_name': last_name}
        if company:
            data['company'] = company
        if domain:
            data['domain'] = domain
        result = self._request('POST', 'find/person', json=data)
        return EmailResult(
            email=result['email'],
            confidence=result['confidence'],
            source=result.get('source')
        )

    def search_company_email(
        self,
        company: str,
        position: Optional[str] = None
    ) -> List[EmailResult]:
        data = {'company': company}
        if position:
            data['position'] = position
        result = self._request('POST', 'find/company', json=data)
        return [
            EmailResult(email=e['email'], confidence=e['confidence'], source=e.get('source'))
            for e in result.get('emails', [])
        ]

    def validate_email(self, email: str) -> EmailValidation:
        result = self._request('GET', f'validate/{email}')
        return EmailValidation(
            email=result['email'],
            is_deliverable=result['is_deliverable'],
            is_valid_format=result['is_valid_format'],
            score=result['score'],
            description=result.get('description')
        )

    def test_connection(self) -> bool:
        try:
            self.validate_email('test@example.com')
            return True
        except Exception:
            return False
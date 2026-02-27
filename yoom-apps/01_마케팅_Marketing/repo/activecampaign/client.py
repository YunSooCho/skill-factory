"""
ActiveCampaign API Client
Documentation: https://developers.activecampaign.com/
"""

import logging
import requests
from typing import List, Optional, Dict, Any
from .models import (
    Account, Contact, Deal, Automation, List as ACList,
    Note, ContactScore, AccountContact, ContactField
)

logger = logging.getLogger(__name__)


class ActiveCampaignClient:
    """
    ActiveCampaign API Client for Yoom Integration

    API Actions:
    - Update Account
    - Delete Contact
    - Add Contact to List
    - Delete Account
    - Associate Contact with Account
    - Search Contact
    - List/Get Contacts
    - Create Deal
    - Create Contact
    - Get Contact
    - Add Contact to Automation
    - Remove Contact from List
    - Create Account
    - Add Note
    - Get Contact Score
    - Get Account
    """

    def __init__(self, api_key: str, api_url: str):
        """
        Initialize ActiveCampaign Client

        Args:
            api_key: ActiveCampaign API Key
            api_url: ActiveCampaign API URL (e.g., https://youraccount.api-us1.com)
        """
        self.api_key = api_key
        self.api_url = api_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Api-Token': api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make HTTP request to ActiveCampaign API

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional arguments for requests

        Returns:
            JSON response data

        Raises:
            requests.RequestException: If request fails
        """
        url = f"{self.api_url}/api/3/{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"ActiveCampaign API Error: {e}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response: {e.response.text}")
            raise

    # ========== ACCOUNT OPERATIONS ==========

    def update_account(self, account_id: str, name: Optional[str] = None) -> Account:
        """
        Update Account

        Args:
            account_id: Account ID
            name: New account name (optional)

        Returns:
            Updated Account object
        """
        data = {'account': {}}
        if name:
            data['account']['name'] = name

        result = self._request('PUT', f'accounts/{account_id}', json=data)
        return Account(
            id=result['account']['id'],
            name=result['account']['name'],
            account_url=result['account'].get('account_url'),
            created_timestamp=result['account'].get('created_timestamp'),
            updated_timestamp=result['account'].get('updated_timestamp')
        )

    def delete_account(self, account_id: str) -> Dict[str, Any]:
        """
        Delete Account

        Args:
            account_id: Account ID

        Returns:
            Deletion response
        """
        return self._request('DELETE', f'accounts/{account_id}')

    def create_account(self, name: str, account_url: Optional[str] = None) -> Account:
        """
        Create Account

        Args:
            name: Account name
            account_url: Account URL (optional)

        Returns:
            Created Account object
        """
        data = {'account': {'name': name}}
        if account_url:
            data['account']['account_url'] = account_url

        result = self._request('POST', 'accounts', json=data)
        return Account(
            id=result['account']['id'],
            name=result['account']['name'],
            account_url=result['account'].get('account_url'),
            created_timestamp=result['account'].get('created_timestamp')
        )

    def get_account(self, account_id: str) -> Account:
        """
        Get Account

        Args:
            account_id: Account ID

        Returns:
            Account object
        """
        result = self._request('GET', f'accounts/{account_id}')
        return Account(
            id=result['account']['id'],
            name=result['account']['name'],
            account_url=result['account'].get('account_url'),
            created_timestamp=result['account'].get('created_timestamp'),
            updated_timestamp=result['account'].get('updated_timestamp')
        )

    # ========== CONTACT OPERATIONS ==========

    def create_contact(
        self,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        field_values: Optional[Dict[str, str]] = None
    ) -> Contact:
        """
        Create Contact

        Args:
            email: Contact email
            first_name: First name (optional)
            last_name: Last name (optional)
            phone: Phone number (optional)
            field_values: Custom field values (optional)

        Returns:
            Created Contact object
        """
        data = {'contact': {'email': email}}
        if first_name:
            data['contact']['firstName'] = first_name
        if last_name:
            data['contact']['lastName'] = last_name
        if phone:
            data['contact']['phone'] = phone

        if field_values:
            data['fieldValues'] = [
                {'field': k, 'value': v} for k, v in field_values.items()
            ]

        result = self._request('POST', 'contacts', json=data)
        return Contact(
            id=result['contact']['id'],
            email=result['contact']['email'],
            first_name=result['contact'].get('firstName'),
            last_name=result['contact'].get('lastName'),
            phone=result['contact'].get('phone'),
            created_timestamp=result['contact'].get('createdTimestamp')
        )

    def get_contact(self, contact_id: str) -> Contact:
        """
        Get Contact

        Args:
            contact_id: Contact ID

        Returns:
            Contact object
        """
        result = self._request('GET', f'contacts/{contact_id}')
        return Contact(
            id=result['contact']['id'],
            email=result['contact']['email'],
            first_name=result['contact'].get('firstName'),
            last_name=result['contact'].get('lastName'),
            phone=result['contact'].get('phone'),
            created_timestamp=result['contact'].get('createdTimestamp'),
            updated_timestamp=result['contact'].get('updatedTimestamp')
        )

    def search_contact(self, email: str) -> Optional[Contact]:
        """
        Search Contact by Email

        Args:
            email: Contact email

        Returns:
            Contact object if found, None otherwise
        """
        result = self._request('GET', 'contacts', params={'email': email})
        contacts = result.get('contacts', [])
        if contacts:
            c = contacts[0]
            return Contact(
                id=c['id'],
                email=c['email'],
                first_name=c.get('firstName'),
                last_name=c.get('lastName'),
                phone=c.get('phone'),
                created_timestamp=c.get('createdTimestamp'),
                updated_timestamp=c.get('updatedTimestamp')
            )
        return None

    def list_contacts(
        self,
        limit: int = 20,
        offset: int = 0
    ) -> List[Contact]:
        """
        List Contacts

        Args:
            limit: Number of contacts to return
            offset: Pagination offset

        Returns:
            List of Contact objects
        """
        result = self._request('GET', 'contacts', params={'limit': limit, 'offset': offset})
        contacts = []
        for c in result.get('contacts', []):
            contacts.append(Contact(
                id=c['id'],
                email=c['email'],
                first_name=c.get('firstName'),
                last_name=c.get('lastName'),
                phone=c.get('phone'),
                created_timestamp=c.get('createdTimestamp'),
                updated_timestamp=c.get('updatedTimestamp')
            ))
        return contacts

    def delete_contact(self, contact_id: str) -> Dict[str, Any]:
        """
        Delete Contact

        Args:
            contact_id: Contact ID

        Returns:
            Deletion response
        """
        return self._request('DELETE', f'contacts/{contact_id}')

    # ========== LIST OPERATIONS ==========

    def add_contact_to_list(self, contact_id: str, list_id: str) -> Dict[str, Any]:
        """
        Add Contact to List

        Args:
            contact_id: Contact ID
            list_id: List ID

        Returns:
            Response dictionary
        """
        data = {'contactList': {'list': list_id, 'contact': contact_id, 'status': 1}}
        return self._request('POST', 'contactLists', json=data)

    def remove_contact_from_list(self, contact_id: str, list_id: str) -> Dict[str, Any]:
        """
        Remove Contact from List

        Args:
            contact_id: Contact ID
            list_id: List ID

        Returns:
            Response dictionary
        """
        data = {'contactList': {'list': list_id, 'contact': contact_id, 'status': 2}}
        return self._request('POST', 'contactLists', json=data)

    # ========== AUTOMATION OPERATIONS ==========

    def add_contact_to_automation(self, contact_id: str, automation_id: str) -> Dict[str, Any]:
        """
        Add Contact to Automation

        Args:
            contact_id: Contact ID
            automation_id: Automation ID

        Returns:
            Response dictionary
        """
        data = {'contactAutomation': {'contact': contact_id, 'automation': automation_id}}
        return self._request('POST', 'contactAutomations', json=data)

    # ========== DEAL OPERATIONS ==========

    def create_deal(
        self,
        contact_id: str,
        value: float,
        currency: str,
        title: str,
        stage: int = 1,
        account_id: Optional[str] = None
    ) -> Deal:
        """
        Create Deal

        Args:
            contact_id: Contact ID
            value: Deal value
            currency: Currency code (e.g., USD, EUR)
            title: Deal title
            stage: Deal stage ID (default: 1)
            account_id: Account ID (optional)

        Returns:
            Created Deal object
        """
        data = {
            'deal': {
                'contact': contact_id,
                'value': value,
                'currency': currency,
                'title': title,
                'stage': stage
            }
        }
        if account_id:
            data['deal']['account'] = account_id

        result = self._request('POST', 'deals', json=data)
        return Deal(
            id=result['deal']['id'],
            contact=result['deal']['contact'],
            value=result['deal']['value'],
            currency=result['deal']['currency'],
            title=result['deal']['title'],
            status=result['deal'].get('status', 'open'),
            stage=result['deal'].get('stage'),
            created_timestamp=result['deal'].get('createdTimestamp')
        )

    # ========== ACCOUNT-CONTACT RELATIONSHIPS ==========

    def associate_account_contact(
        self,
        account_id: str,
        contact_id: str,
        job_title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Associate Contact with Account

        Args:
            account_id: Account ID
            contact_id: Contact ID
            job_title: Job title (optional)

        Returns:
            Response dictionary
        """
        data = {
            'accountContact': {
                'account': account_id,
                'contact': contact_id
            }
        }
        if job_title:
            data['accountContact']['jobTitle'] = job_title

        return self._request('POST', 'accountContacts', json=data)

    # ========== NOTE OPERATIONS ==========

    def add_note(self, contact_id: str, note_text: str) -> Note:
        """
        Add Note to Contact

        Args:
            contact_id: Contact ID
            note_text: Note text

        Returns:
            Created Note object
        """
        data = {'note': {'note': note_text, 'relid': contact_id}}
        result = self._request('POST', 'notes', json=data)
        return Note(
            id=result['note']['id'],
            note=result['note']['note'],
            relid=result['note']['relid'],
            created_timestamp=result['note']['createdTimestamp']
        )

    # ========== SCORE OPERATIONS ==========

    def get_contact_score(self, contact_id: str) -> int:
        """
        Get Contact Score

        Args:
            contact_id: Contact ID

        Returns:
            Contact score
        """
        result = self._request('GET', f'contactScores?contact={contact_id}')
        scores = result.get('contactScores', [])
        if scores:
            return int(scores[0]['score'])
        return 0

    # ========== UTILITY ==========

    def test_connection(self) -> bool:
        """
        Test API connection

        Returns:
            True if connection successful
        """
        try:
            self._request('GET', 'account')
            return True
        except Exception:
            return False
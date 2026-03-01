"""
Insightly CRM API Client
CRM platform for managing contacts, leads, organizations, projects, and tasks

API Documentation: https://developers.insightly.com/
"""

import requests
import time
from typing import Dict, List, Optional, Any
from requests.exceptions import RequestException


class InsightlyAPIError(Exception):
    """Custom exception for Insightly API errors"""
    pass


class InsightlyRateLimitError(InsightlyAPIError):
    """Rate limit exceeded error"""
    pass


class InsightlyClient:
    """
    Insightly REST API Client
    Supports comprehensive CRM operations including:
    - Contacts
    - Leads
    - Organizations
    - Projects
    - Tasks
    - Project Pipelines
    """

    def __init__(self, api_key: str, api_url: str = "https://api.insight.ly", timeout: int = 30):
        """
        Initialize Insightly API client

        Args:
            api_key: Insightly API key
            api_url: Base URL of Insightly API
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.api_url = api_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        })
        self.session.params = {'api_key': api_key}
        self.last_request_time = 0
        self.min_request_interval = 0.2  # 200ms between requests
        self.rate_limit_remaining = None

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None,
                     params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make an authenticated API request with error handling and rate limiting

        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request body data
            params: Query parameters

        Returns:
            Response data as dictionary
        """
        # Rate limiting
        current_time = time.time()

        if self.rate_limit_remaining is not None and self.rate_limit_remaining <= 0:
            time.sleep(1)

        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)

        url = f"{self.api_url}{endpoint}"

        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params, timeout=self.timeout)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, params=params, timeout=self.timeout)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, params=params, timeout=self.timeout)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, params=params, timeout=self.timeout)
            else:
                raise InsightlyAPIError(f"Unsupported HTTP method: {method}")

            self.last_request_time = time.time()

            # Update rate limit info
            rate_limit_info = response.headers.get('X-RateLimit')
            if rate_limit_info:
                parts = rate_limit_info.split('/')
                if len(parts) >= 2:
                    self.rate_limit_remaining = int(parts[1]) - int(parts[0])

            # Handle rate limiting (HTTP 429)
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 5))
                time.sleep(retry_after)
                return self._make_request(method, endpoint, data, params)

            # Handle errors
            if response.status_code >= 400:
                try:
                    error_data = response.json()
                except:
                    error_data = {}
                error_msg = error_data.get('message', error_data.get('error', response.text))
                raise InsightlyAPIError(f"API error {response.status_code}: {error_msg}")

            return response.json() if response.content else {}

        except RequestException as e:
            raise InsightlyAPIError(f"Request failed: {str(e)}")

    # ========== CONTACT METHODS ==========

    def create_contact(self, first_name: Optional[str] = None, last_name: Optional[str] = None,
                      contactinfos: Optional[List[Dict]] = None, **kwargs) -> Dict[str, Any]:
        """
        Create a new contact

        Args:
            first_name: First name
            last_name: Last name
            contactinfos: List of contact info objects (email, phone, etc.)
            **kwargs: Additional contact fields

        Returns:
            Created contact data
        """
        data = {}
        if first_name:
            data['FIRST_NAME'] = first_name
        if last_name:
            data['LAST_NAME'] = last_name
        if contactinfos:
            data['CONTACTINFOS'] = contactinfos
        data.update(kwargs)

        return self._make_request('POST', '/v3.1/Contacts', data=data)

    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """Get contact by ID"""
        return self._make_request('GET', f'/v3.1/Contacts/{contact_id}')

    def update_contact(self, contact_id: str, **kwargs) -> Dict[str, Any]:
        """Update contact"""
        kwargs['CONTACT_ID'] = int(contact_id)
        return self._make_request('PUT', f'/v3.1/Contacts', data=kwargs)

    def list_contacts(self, skip: int = 0, top: int = 100, **filters) -> Dict[str, Any]:
        """List contacts with filtering"""
        params = {'skip': skip, 'top': top}
        params.update(filters)
        return self._make_request('GET', '/v3.1/Contacts', params=params)

    # ========== LEAD METHODS ==========

    def create_lead(self, first_name: Optional[str] = None, last_name: Optional[str] = None,
                   contactinfos: Optional[List[Dict]] = None, **kwargs) -> Dict[str, Any]:
        """Create a new lead"""
        data = {}
        if first_name:
            data['FIRST_NAME'] = first_name
        if last_name:
            data['LAST_NAME'] = last_name
        if contactinfos:
            data['CONTACTINFOS'] = contactinfos
        data.update(kwargs)

        return self._make_request('POST', '/v3.1/Leads', data=data)

    def get_lead(self, lead_id: str) -> Dict[str, Any]:
        """Get lead by ID"""
        return self._make_request('GET', f'/v3.1/Leads/{lead_id}')

    def update_lead(self, lead_id: str, **kwargs) -> Dict[str, Any]:
        """Update lead"""
        kwargs['LEAD_ID'] = int(lead_id)
        return self._make_request('PUT', f'/v3.1/Leads', data=kwargs)

    def list_leads(self, skip: int = 0, top: int = 100, **filters) -> Dict[str, Any]:
        """List leads with filtering"""
        params = {'skip': skip, 'top': top}
        params.update(filters)
        return self._make_request('GET', '/v3.1/Leads', params=params)

    # ========== ORGANIZATION METHODS ==========

    def create_organisation(self, name: str, **kwargs) -> Dict[str, Any]:
        """Create a new organization"""
        data = {'ORGANISATION_NAME': name, **kwargs}
        return self._make_request('POST', '/v3.1/Organisations', data=data)

    def get_organisation(self, organisation_id: str) -> Dict[str, Any]:
        """Get organisation by ID"""
        return self._make_request('GET', f'/v3.1/Organisations/{organisation_id}')

    def update_organisation(self, organisation_id: str, **kwargs) -> Dict[str, Any]:
        """Update organisation"""
        kwargs['ORGANISATION_ID'] = int(organisation_id)
        return self._make_request('PUT', f'/v3.1/Organisations', data=kwargs)

    def list_organisations(self, skip: int = 0, top: int = 100, **filters) -> Dict[str, Any]:
        """List organisations with filtering"""
        params = {'skip': skip, 'top': top}
        params.update(filters)
        return self._make_request('GET', '/v3.1/Organisations', params=params)

    # ========== PROJECT METHODS ==========

    def create_project(self, name: str, project_stage_id: Optional[str] = None,
                      **kwargs) -> Dict[str, Any]:
        """Create a new project"""
        data = {'PROJECT_NAME': name, **kwargs}
        if project_stage_id:
            data['PROJECT_STAGE_ID'] = project_stage_id
        return self._make_request('POST', '/v3.1/Projects', data=data)

    def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get project by ID"""
        return self._make_request('GET', f'/v3.1/Projects/{project_id}')

    def update_project(self, project_id: str, **kwargs) -> Dict[str, Any]:
        """Update project"""
        kwargs['PROJECT_ID'] = int(project_id)
        return self._make_request('PUT', f'/v3.1/Projects', data=kwargs)

    def list_projects(self, skip: int = 0, top: int = 100, **filters) -> Dict[str, Any]:
        """List projects with filtering"""
        params = {'skip': skip, 'top': top}
        params.update(filters)
        return self._make_request('GET', '/v3.1/Projects', params=params)

    def update_project_pipeline(self, project_id: str, pipeline_stage_id: str) -> Dict[str, Any]:
        """Update project pipeline stage"""
        data = {
            'PROJECT_ID': int(project_id),
            'PIPELINE_STAGE_ID': pipeline_stage_id
        }
        return self._make_request('PUT', '/v3.1/Projects', data=data)

    # ========== TASK METHODS ==========

    def create_task(self, subject: str, **kwargs) -> Dict[str, Any]:
        """Create a new task"""
        data = {'SUBJECT': subject, **kwargs}
        return self._make_request('POST', '/v3.1/Tasks', data=data)

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get task by ID"""
        return self._make_request('GET', f'/v3.1/Tasks/{task_id}')

    def update_task(self, task_id: str, **kwargs) -> Dict[str, Any]:
        """Update task"""
        kwargs['TASK_ID'] = int(task_id)
        return self._make_request('PUT', f'/v3.1/Tasks', data=kwargs)

    def list_tasks(self, skip: int = 0, top: int = 100, **filters) -> Dict[str, Any]:
        """List tasks with filtering"""
        params = {'skip': skip, 'top': top}
        params.update(filters)
        return self._make_request('GET', '/v3.1/Tasks', params=params)


if __name__ == '__main__':
    import os

    API_KEY = os.getenv('INSIGHTLY_API_KEY', 'your_api_key')

    client = InsightlyClient(api_key=API_KEY)

    try:
        # Example: Create a contact
        contact = client.create_contact(
            first_name='Jane',
            last_name='Doe',
            contactinfos=[
                {
                    'TYPE': 'EMAIL',
                    'LABEL': 'WORK',
                    'DETAIL': 'jane.doe@example.com'
                }
            ]
        )
        print(f"Created contact: {contact}")

        # Example: Create an organization
        org = client.create_organisation(
            name='Acme Corporation',
            website='https://acme.com'
        )
        print(f"Created organization: {org}")

        # Example: Create a project
        project = client.create_project(
            name='Website Redesign',
            status='In Progress'
        )
        print(f"Created project: {project}")

        # Example: Create a task
        task = client.create_task(
            subject='Complete initial design',
            due_date='2025-03-15'
        )
        print(f"Created task: {task}")

        # Example: Create a lead
        lead = client.create_lead(
            first_name='John',
            last_name='Smith',
            contactinfos=[
                {
                    'TYPE': 'EMAIL',
                    'LABEL': 'WORK',
                    'DETAIL': 'john.smith@example.com'
                }
            ]
        )
        print(f"Created lead: {lead}")

        # Example: List contacts
        contacts = client.list_contacts(top=10)
        print(f"Contacts: {contacts}")

    except InsightlyAPIError as e:
        print(f"Error: {e}")
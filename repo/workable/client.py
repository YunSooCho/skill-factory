"""
Workable Recruiting API Client

This module provides a Python client for interacting with the Workable
recruiting platform API.
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime


class WorkableClient:
    """
    Client for Workable Recruiting Platform API.

    Workable provides:
    - Job posting and management
    - Applicant tracking
    - Candidate management
    - Interview scheduling
    - Offer management
    """

    def __init__(
        self,
        api_key: str,
        subdomain: str,
        base_url: str = "https://www.workable.com/spi/v3",
        timeout: int = 30
    ):
        """
        Initialize the Workable client.

        Args:
            api_key: Your Workable API key
            subdomain: Your Workable account subdomain
            base_url: API base URL (default: https://www.workable.com/spi/v3)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.subdomain = subdomain
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
        self.session.params = {'account': subdomain}

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an authenticated request to the Workable API.

        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            data: Request body data

        Returns:
            Response JSON
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(
            method,
            url,
            params=params,
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def get_jobs(
        self,
        state: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List jobs.

        Args:
            state: Filter by job state (published, draft, closed)
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of jobs
        """
        params = {
            'limit': limit,
            'offset': offset
        }
        if state:
            params['state'] = state

        result = self._request('GET', '/jobs', params=params)
        return result.get('jobs', [])

    def get_job(self, job_id: str) -> Dict[str, Any]:
        """
        Get job details.

        Args:
            job_id: Job ID

        Returns:
            Job details
        """
        return self._request('GET', f'/jobs/{job_id}')

    def create_job(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new job.

        Args:
            data: Job data including title, department, location, description, etc.

        Returns:
            Created job details
        """
        return self._request('POST', '/jobs', data=data)

    def update_job(self, job_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a job.

        Args:
            job_id: Job ID
            data: Fields to update

        Returns:
            Updated job details
        """
        return self._request('PUT', f'/jobs/{job_id}', data=data)

    def get_candidates(
        self,
        job_id: Optional[str] = None,
        stage: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List candidates.

        Args:
            job_id: Filter by job (optional)
            stage: Filter by hiring stage (optional)
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of candidates
        """
        params = {
            'limit': limit,
            'offset': offset
        }
        if job_id:
            params['job_id'] = job_id
        if stage:
            params['stage'] = stage

        result = self._request('GET', '/candidates', params=params)
        return result.get('candidates', [])

    def get_candidate(self, candidate_id: str) -> Dict[str, Any]:
        """
        Get candidate details.

        Args:
            candidate_id: Candidate ID

        Returns:
            Candidate details
        """
        return self._request('GET', f'/candidates/{candidate_id}')

    def create_candidate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new candidate.

        Args:
            data: Candidate data including name, email, phone, etc.

        Returns:
            Created candidate details
        """
        return self._request('POST', '/candidates', data=data)

    def update_candidate(self, candidate_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update candidate information.

        Args:
            candidate_id: Candidate ID
            data: Fields to update

        Returns:
            Updated candidate details
        """
        return self._request('PUT', f'/candidates/{candidate_id}', data=data)

    def get_candidate_activities(
        self,
        candidate_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get candidate activity history.

        Args:
            candidate_id: Candidate ID
            limit: Maximum number of activities

        Returns:
            List of activities
        """
        params = {'limit': limit}
        result = self._request('GET', f'/candidates/{candidate_id}/activities', params=params)
        return result.get('activities', [])

    def add_candidate_to_job(
        self,
        candidate_id: str,
        job_id: str
    ) -> Dict[str, Any]:
        """
        Add a candidate to a job.

        Args:
            candidate_id: Candidate ID
            job_id: Job ID

        Returns:
            Application details
        """
        return self._request(
            'POST',
            f'/candidates/{candidate_id}/jobs',
            data={'job': job_id}
        )

    def get_interviews(
        self,
        job_id: Optional[str] = None,
        candidate_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List interviews.

        Args:
            job_id: Filter by job (optional)
            candidate_id: Filter by candidate (optional)
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of interviews
        """
        params = {
            'limit': limit,
            'offset': offset
        }
        if job_id:
            params['job_id'] = job_id
        if candidate_id:
            params['candidate_id'] = candidate_id

        result = self._request('GET', '/interviews', params=params)
        return result.get('interviews', [])

    def create_interview(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new interview.

        Args:
            data: Interview data including candidate_id, job_id, date, time, interviewers

        Returns:
            Created interview details
        """
        return self._request('POST', '/interviews', data=data)

    def update_interview(self, interview_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an interview.

        Args:
            interview_id: Interview ID
            data: Fields to update

        Returns:
            Updated interview details
        """
        return self._request('PUT', f'/interviews/{interview_id}', data=data)

    def delete_interview(self, interview_id: str) -> Dict[str, Any]:
        """
        Delete an interview.

        Args:
            interview_id: Interview ID

        Returns:
            Deletion result
        """
        return self._request('DELETE', f'/interviews/{interview_id}')

    def get_offers(
        self,
        job_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        List offers.

        Args:
            job_id: Filter by job (optional)
            status: Filter by status (draft, sent, accepted, rejected, expired)
            limit: Maximum number of results

        Returns:
            List of offers
        """
        params = {'limit': limit}
        if job_id:
            params['job_id'] = job_id
        if status:
            params['status'] = status

        result = self._request('GET', '/offers', params=params)
        return result.get('offers', [])

    def create_offer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new offer.

        Args:
            data: Offer data including candidate_id, job_id, salary, etc.

        Returns:
            Created offer details
        """
        return self._request('POST', '/offers', data=data)

    def get_offer(self, offer_id: str) -> Dict[str, Any]:
        """
        Get offer details.

        Args:
            offer_id: Offer ID

        Returns:
            Offer details
        """
        return self._request('GET', f'/offers/{offer_id}')

    def update_offer(self, offer_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an offer.

        Args:
            offer_id: Offer ID
            data: Fields to update

        Returns:
            Updated offer details
        """
        return self._request('PUT', f'/offers/{offer_id}', data=data)

    def send_offer(self, offer_id: str) -> Dict[str, Any]:
        """
        Send an offer to a candidate.

        Args:
            offer_id: Offer ID

        Returns:
            Sent offer details
        """
        return self._request('POST', f'/offers/{offer_id}/send')

    def get_users(self) -> List[Dict[str, Any]]:
        """
        List users (recruiters and hiring managers).

        Returns:
            List of users
        """
        result = self._request('GET', '/users')
        return result.get('users', [])

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Get user details.

        Args:
            user_id: User ID

        Returns:
            User details
        """
        return self._request('GET', f'/users/{user_id}')

    def get_recruiters(self) -> List[Dict[str, Any]]:
        """
        List recruiters.

        Returns:
            List of recruiters
        """
        result = self._request('GET', '/recruiters')
        return result.get('recruiters', [])

    def get_departments(self) -> List[Dict[str, Any]]:
        """
        List departments.

        Returns:
            List of departments
        """
        result = self._request('GET', '/departments')
        return result.get('departments', [])

    def get_stages(self, job_id: str) -> List[Dict[str, Any]]:
        """
        Get hiring stages for a job.

        Args:
            job_id: Job ID

        Returns:
            List of hiring stages
        """
        result = self._request('GET', f'/jobs/{job_id}/pipeline')
        return result.get('stages', [])

    def move_candidate(
        self,
        candidate_id: str,
        job_id: str,
        stage_id: str
    ) -> Dict[str, Any]:
        """
        Move a candidate to a different stage.

        Args:
            candidate_id: Candidate ID
            job_id: Job ID
            stage_id: New stage ID

        Returns:
            Updated candidate details
        """
        return self._request(
            'POST',
            f'/candidates/{candidate_id}/jobs/{job_id}/move',
            data={'stage_id': stage_id}
        )
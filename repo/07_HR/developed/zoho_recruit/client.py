"""
Zoho Recruit ATS API Client

This module provides a Python client for interacting with the Zoho Recruit
applicant tracking system API.
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime


class ZohoRecruitClient:
    """
    Client for Zoho Recruit Applicant Tracking System API.

    Zoho Recruit provides:
    - Job posting management
    - Candidate management
    - Interview scheduling
    - Application tracking
    - Offer management
    - Recruitment analytics
    """

    def __init__(
        self,
        auth_token: str,
        organization_id: str,
        base_url: str = "https://recruit.zoho.com/recruit/v2",
        timeout: int = 30
    ):
        """
        Initialize the Zoho Recruit client.

        Args:
            auth_token: Zoho authentication token
            organization_id: Your organization ID
            base_url: API base URL (default: https://recruit.zoho.com/recruit/v2)
            timeout: Request timeout in seconds
        """
        self.auth_token = auth_token
        self.organization_id = organization_id
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Zoho-oauthtoken {auth_token}',
            'Content-Type': 'application/json'
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an authenticated request to the Zoho Recruit API.

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
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get list of job openings.

        Args:
            status: Filter by job status (optional)
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of job openings
        """
        params = {
            'limit': limit,
            'offset': offset
        }
        if status:
            params['status'] = status

        result = self._request('GET', '/JobOpenings', params=params)
        return result.get('data', [])

    def get_job(self, job_id: str) -> Dict[str, Any]:
        """
        Get job details.

        Args:
            job_id: Job opening ID

        Returns:
            Job details
        """
        result = self._request('GET', f'/JobOpenings/{job_id}')
        return result.get('data', [{}])[0]

    def create_job(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new job opening.

        Args:
            data: Job data including title, department, description, etc.

        Returns:
            Created job details
        """
        result = self._request('POST', '/JobOpenings', data={'data': [data]})
        return result.get('data', [{}])[0]

    def update_job(self, job_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a job opening.

        Args:
            job_id: Job opening ID
            data: Fields to update

        Returns:
            Updated job details
        """
        result = self._request('PUT', f'/JobOpenings/{job_id}', data={'data': [data]})
        return result.get('data', [{}])[0]

    def delete_job(self, job_id: str) -> Dict[str, Any]:
        """
        Delete a job opening.

        Args:
            job_id: Job opening ID

        Returns:
            Deletion result
        """
        return self._request('DELETE', f'/JobOpenings/{job_id}')

    def get_candidates(
        self,
        job_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get list of candidates.

        Args:
            job_id: Filter by job (optional)
            status: Filter by candidate status (optional)
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
        if status:
            params['status'] = status

        result = self._request('GET', '/Candidates', params=params)
        return result.get('data', [])

    def get_candidate(self, candidate_id: str) -> Dict[str, Any]:
        """
        Get candidate details.

        Args:
            candidate_id: Candidate ID

        Returns:
            Candidate details
        """
        result = self._request('GET', f'/Candidates/{candidate_id}')
        return result.get('data', [{}])[0]

    def create_candidate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new candidate.

        Args:
            data: Candidate data including name, email, phone, etc.

        Returns:
            Created candidate details
        """
        result = self._request('POST', '/Candidates', data={'data': [data]})
        return result.get('data', [{}])[0]

    def update_candidate(self, candidate_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update candidate information.

        Args:
            candidate_id: Candidate ID
            data: Fields to update

        Returns:
            Updated candidate details
        """
        result = self._request('PUT', f'/Candidates/{candidate_id}', data={'data': [data]})
        return result.get('data', [{}])[0]

    def delete_candidate(self, candidate_id: str) -> Dict[str, Any]:
        """
        Delete a candidate.

        Args:
            candidate_id: Candidate ID

        Returns:
            Deletion result
        """
        return self._request('DELETE', f'/Candidates/{candidate_id}')

    def get_applications(
        self,
        job_id: Optional[str] = None,
        candidate_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get list of job applications.

        Args:
            job_id: Filter by job (optional)
            candidate_id: Filter by candidate (optional)
            status: Filter by application status (optional)
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of applications
        """
        params = {
            'limit': limit,
            'offset': offset
        }
        if job_id:
            params['job_id'] = job_id
        if candidate_id:
            params['candidate_id'] = candidate_id
        if status:
            params['status'] = status

        result = self._request('GET', '/JobApplications', params=params)
        return result.get('data', [])

    def get_application(self, application_id: str) -> Dict[str, Any]:
        """
        Get application details.

        Args:
            application_id: Application ID

        Returns:
            Application details
        """
        result = self._request('GET', f'/JobApplications/{application_id}')
        return result.get('data', [{}])[0]

    def create_application(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new job application.

        Args:
            data: Application data including job_id, candidate_id, etc.

        Returns:
            Created application details
        """
        result = self._request('POST', '/JobApplications', data={'data': [data]})
        return result.get('data', [{}])[0]

    def update_application(self, application_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update application status.

        Args:
            application_id: Application ID
            data: Fields to update

        Returns:
            Updated application details
        """
        result = self._request('PUT', f'/JobApplications/{application_id}', data={'data': [data]})
        return result.get('data', [{}])[0]

    def get_interviews(
        self,
        job_id: Optional[str] = None,
        candidate_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get list of interviews.

        Args:
            job_id: Filter by job (optional)
            candidate_id: Filter by candidate (optional)
            status: Filter by interview status (optional)
            limit: Maximum number of results

        Returns:
            List of interviews
        """
        params = {'limit': limit}
        if job_id:
            params['job_id'] = job_id
        if candidate_id:
            params['candidate_id'] = candidate_id
        if status:
            params['status'] = status

        result = self._request('GET', '/Interviews', params=params)
        return result.get('data', [])

    def create_interview(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new interview.

        Args:
            data: Interview data including candidate_id, job_id, schedule, etc.

        Returns:
            Created interview details
        """
        result = self._request('POST', '/Interviews', data={'data': [data]})
        return result.get('data', [{}])[0]

    def update_interview(self, interview_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update interview details.

        Args:
            interview_id: Interview ID
            data: Fields to update

        Returns:
            Updated interview details
        """
        result = self._request('PUT', f'/Interviews/{interview_id}', data={'data': [data]})
        return result.get('data', [{}])[0]

    def delete_interview(self, interview_id: str) -> Dict[str, Any]:
        """
        Delete an interview.

        Args:
            interview_id: Interview ID

        Returns:
            Deletion result
        """
        return self._request('DELETE', f'/Interviews/{interview_id}')

    def get_offers(
        self,
        job_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get list of offers.

        Args:
            job_id: Filter by job (optional)
            status: Filter by offer status (optional)
            limit: Maximum number of results

        Returns:
            List of offers
        """
        params = {'limit': limit}
        if job_id:
            params['job_id'] = job_id
        if status:
            params['status'] = status

        result = self._request('GET', '/Offers', params=params)
        return result.get('data', [])

    def create_offer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new offer.

        Args:
            data: Offer data including candidate_id, job_id, salary, etc.

        Returns:
            Created offer details
        """
        result = self._request('POST', '/Offers', data={'data': [data]})
        return result.get('data', [{}])[0]

    def get_offer(self, offer_id: str) -> Dict[str, Any]:
        """
        Get offer details.

        Args:
            offer_id: Offer ID

        Returns:
            Offer details
        """
        result = self._request('GET', f'/Offers/{offer_id}')
        return result.get('data', [{}])[0]

    def update_offer(self, offer_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update offer details.

        Args:
            offer_id: Offer ID
            data: Fields to update

        Returns:
            Updated offer details
        """
        result = self._request('PUT', f'/Offers/{offer_id}', data={'data': [data]})
        return result.get('data', [{}])[0]

    def get_pipeline(self, job_id: str) -> Dict[str, Any]:
        """
        Get recruitment pipeline for a job.

        Args:
            job_id: Job opening ID

        Returns:
            Pipeline stages and candidates in each stage
        """
        return self._request('GET', f'/JobOpenings/{job_id}/Pipeline')

    def move_application(
        self,
        application_id: str,
        stage_id: str
    ) -> Dict[str, Any]:
        """
        Move application to a different stage.

        Args:
            application_id: Application ID
            stage_id: Target stage ID

        Returns:
            Updated application
        """
        return self._request(
            'POST',
            f'/JobApplications/{application_id}/Stages',
            data={'stage_id': stage_id}
        )

    def get_activities(
        self,
        record_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get activity history for a record.

        Args:
            record_id: Record ID (candidate, application, etc.)
            limit: Maximum number of activities

        Returns:
            List of activities
        """
        params = {'limit': limit}
        result = self._request('GET', f'/Activities', params=params)
        return result.get('data', [])

    def create_note(
        self,
        record_id: str,
        note_text: str,
        module: str = "Candidates"
    ) -> Dict[str, Any]:
        """
        Create a note on a record.

        Args:
            record_id: Record ID
            note_text: Note content
            module: Module name (Candidates, JobApplications, etc.)

        Returns:
            Created note details
        """
        data = {
            'Note_Title': 'Note',
            'Note_Content': note_text,
            'Parent_Id': record_id,
            'se_module': module
        }
        result = self._request('POST', '/Notes', data={'data': [data]})
        return result.get('data', [{}])[0]

    def upload_file(
        self,
        record_id: str,
        file_url: str,
        module: str = "Candidates"
    ) -> Dict[str, Any]:
        """
        Upload a file attachment.

        Args:
            record_id: Record ID
            file_url: URL of the file
            module: Module name (Candidates, JobApplications, etc.)

        Returns:
            Uploaded file details
        """
        data = {
            'Parent_Id': record_id,
            'File_Url': file_url,
            'se_module': module
        }
        result = self._request('POST', '/File', data={'data': [data]})
        return result.get('data', [{}])[0]

    def search_candidates(
        self,
        query: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Search candidates.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of matching candidates
        """
        params = {
            'criteria': query,
            'limit': limit
        }
        result = self._request('GET', '/Cv/search', params=params)
        return result.get('data', [])

    def get_clients(self) -> List[Dict[str, Any]]:
        """
        Get list of clients (for recruiting agencies).

        Returns:
            List of clients
        """
        result = self._request('GET', '/Clients')
        return result.get('data', [])

    def get_client_Contacts(self, client_id: str) -> List[Dict[str, Any]]:
        """
        Get contacts at a client.

        Args:
            client_id: Client ID

        Returns:
            List of contacts
        """
        params = {'client_id': client_id}
        result = self._request('GET', '/Contacts', params=params)
        return result.get('data', [])
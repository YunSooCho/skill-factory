"""
Talentio API Client - Recruitment & Talent Management System
"""

import requests
import time
from typing import Optional, Dict, Any, List


class TalentioError(Exception):
    """Base exception for Talentio"""


class TalentioClient:
    BASE_URL = "https://api.talentio.com/v1"

    def __init__(self, api_key: str, account_id: str, timeout: int = 30):
        """
        Initialize Talentio client

        Args:
            api_key: Talentio API key
            account_id: Account ID
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.account_id = account_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'X-Account-ID': account_id
        })

        self.last_request_time = 0
        self.min_delay = 0.3

    def _enforce_rate_limit(self):
        """Enforce rate limiting"""
        current = time.time()
        elapsed = current - self.last_request_time
        if elapsed < self.min_delay:
            time.sleep(self.min_delay - elapsed)
        self.last_request_time = time.time()

    def _handle_response(self, resp: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise TalentioError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise TalentioError(f"Error ({resp.status_code}): {resp.text}")

        if resp.status_code == 204:
            return {}
        return resp.json()

    def _get_params(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Add account_id to params"""
        if params is None:
            params = {}
        params['account_id'] = self.account_id
        return params

    # Candidates
    def get_candidates(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of candidates"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/candidates",
                                params=self._get_params(params), timeout=self.timeout)
        return self._handle_response(resp)

    def get_candidate(self, candidate_id: str) -> Dict[str, Any]:
        """Get candidate details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/candidates/{candidate_id}",
                                params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    def create_candidate(self, candidate_data: Dict) -> Dict[str, Any]:
        """Create a candidate"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/candidates",
                                params=self._get_params(), json=candidate_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_candidate(self, candidate_id: str, candidate_data: Dict) -> Dict[str, Any]:
        """Update candidate"""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/candidates/{candidate_id}",
                                params=self._get_params(), json=candidate_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Jobs
    def get_jobs(self, status: Optional[str] = None) -> Dict[str, Any]:
        """Get list of job openings"""
        self._enforce_rate_limit()
        params = self._get_params()
        if status:
            params['status'] = status

        resp = self.session.get(f"{self.BASE_URL}/jobs",
                                params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_job(self, job_id: str) -> Dict[str, Any]:
        """Get job details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/jobs/{job_id}",
                                params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)

    # Applications
    def get_applications(self, candidate_id: Optional[str] = None,
                        job_id: Optional[str] = None,
                        status: Optional[str] = None) -> Dict[str, Any]:
        """Get applications"""
        self._enforce_rate_limit()
        params = self._get_params()
        if candidate_id:
            params['candidate_id'] = candidate_id
        if job_id:
            params['job_id'] = job_id
        if status:
            params['status'] = status

        resp = self.session.get(f"{self.BASE_URL}/applications",
                                params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_application(self, application_data: Dict) -> Dict[str, Any]:
        """Create an application"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/applications",
                                params=self._get_params(), json=application_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_application(self, application_id: str, data: Dict) -> Dict[str, Any]:
        """Update application"""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/applications/{application_id}",
                                params=self._get_params(), json=data, timeout=self.timeout)
        return self._handle_response(resp)

    # Interviews
    def get_interviews(self, candidate_id: Optional[str] = None) -> Dict[str, Any]:
        """Get interviews"""
        self._enforce_rate_limit()
        params = self._get_params()
        if candidate_id:
            params['candidate_id'] = candidate_id

        resp = self.session.get(f"{self.BASE_URL}/interviews",
                                params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_interview(self, interview_data: Dict) -> Dict[str, Any]:
        """Create an interview"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/interviews",
                                params=self._get_params(), json=interview_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_interview(self, interview_id: str, data: Dict) -> Dict[str, Any]:
        """Update interview"""
        self._enforce_rate_limit()
        resp = self.session.put(f"{self.BASE_URL}/interviews/{interview_id}",
                                params=self._get_params(), json=data, timeout=self.timeout)
        return self._handle_response(resp)

    # Offer
    def create_offer(self, offer_data: Dict) -> Dict[str, Any]:
        """Create an offer"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/offers",
                                params=self._get_params(), json=offer_data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_offer(self, offer_id: str) -> Dict[str, Any]:
        """Get offer details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/offers/{offer_id}",
                                params=self._get_params(), timeout=self.timeout)
        return self._handle_response(resp)
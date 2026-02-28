"""
CATS API Client - Applicant Tracking System (ATS)
"""

import requests
import time
from typing import Optional, Dict, Any, List


class CATSError(Exception):
    """Base exception for CATS"""

class CATSRateLimitError(CATSError):
    """Rate limit exceeded"""

class CATSAuthenticationError(CATSError):
    """Authentication failed"""

class CATSClient:
    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize CATS client

        Args:
            api_key: CATS API key
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

        self.last_request_time = 0
        self.min_delay = 0.5

    def _enforce_rate_limit(self):
        """Enforce rate limiting"""
        current = time.time()
        elapsed = current - self.last_request_time
        if elapsed < self.min_delay:
            time.sleep(self.min_delay - elapsed)
        self.last_request_time = time.time()

    def _handle_response(self, resp: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        if resp.status_code == 429:
            raise CATSRateLimitError("Rate limit exceeded")
        if resp.status_code == 401 or resp.status_code == 403:
            raise CATSAuthenticationError("Authentication failed")
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise CATSError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise CATSError(f"Error ({resp.status_code}): {resp.text}")

        if resp.status_code == 204:
            return {}

        return resp.json()

    # Candidates
    def get_candidates(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of candidates"""
        self._enforce_rate_limit()
        resp = self.session.get("https://api.catsone.com/v3/candidates", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_candidate(self, candidate_id: str) -> Dict[str, Any]:
        """Get candidate details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"https://api.catsone.com/v3/candidates/{candidate_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def create_candidate(self, candidate_data: Dict) -> Dict[str, Any]:
        """Create a candidate"""
        self._enforce_rate_limit()
        resp = self.session.post("https://api.catsone.com/v3/candidates", json=candidate_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_candidate(self, candidate_id: str, candidate_data: Dict) -> Dict[str, Any]:
        """Update candidate"""
        self._enforce_rate_limit()
        resp = self.session.put(f"https://api.catsone.com/v3/candidates/{candidate_id}", json=candidate_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Jobs
    def get_jobs(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of jobs"""
        self._enforce_rate_limit()
        resp = self.session.get("https://api.catsone.com/v3/jobs", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_job(self, job_id: str) -> Dict[str, Any]:
        """Get job details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"https://api.catsone.com/v3/jobs/{job_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def create_job(self, job_data: Dict) -> Dict[str, Any]:
        """Create a job posting"""
        self._enforce_rate_limit()
        resp = self.session.post("https://api.catsone.com/v3/jobs", json=job_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Pipelines
    def get_pipelines(self) -> Dict[str, Any]:
        """Get pipelines"""
        self._enforce_rate_limit()
        resp = self.session.get("https://api.catsone.com/v3/pipelines", timeout=self.timeout)
        return self._handle_response(resp)

    def get_pipeline(self, pipeline_id: str) -> Dict[str, Any]:
        """Get pipeline details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"https://api.catsone.com/v3/pipelines/{pipeline_id}", timeout=self.timeout)
        return self._handle_response(resp)

    # Activities
    def get_activities(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get activities"""
        self._enforce_rate_limit()
        resp = self.session.get("https://api.catsone.com/v3/activities", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_activity(self, activity_data: Dict) -> Dict[str, Any]:
        """Create an activity"""
        self._enforce_rate_limit()
        resp = self.session.post("https://api.catsone.com/v3/activities", json=activity_data, timeout=self.timeout)
        return self._handle_response(resp)

    # Companies
    def get_companies(self) -> Dict[str, Any]:
        """Get companies"""
        self._enforce_rate_limit()
        resp = self.session.get("https://api.catsone.com/v3/companies", timeout=self.timeout)
        return self._handle_response(resp)

    def create_company(self, company_data: Dict) -> Dict[str, Any]:
        """Create a company"""
        self._enforce_rate_limit()
        resp = self.session.post("https://api.catsone.com/v3/companies", json=company_data, timeout=self.timeout)
        return self._handle_response(resp)
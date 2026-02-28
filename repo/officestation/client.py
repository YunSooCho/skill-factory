"""
OfficeStation API Client - Japanese Document Workflow Management
"""

import requests
import time
from typing import Optional, Dict, Any


class OfficeStationError(Exception):
    """Base exception for OfficeStation"""


class OfficeStationClient:
    BASE_URL = "https://api.officestation.com/v1"

    def __init__(self, api_key: str, workspace_id: str, timeout: int = 30):
        """
        Initialize OfficeStation client

        Args:
            api_key: OfficeStation API key
            workspace_id: Workspace ID
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.workspace_id = workspace_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'X-Workspace-ID': workspace_id
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
                raise OfficeStationError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise OfficeStationError(f"Error ({resp.status_code}): {resp.text}")

        if resp.status_code == 204:
            return {}
        return resp.json()

    # Documents
    def get_documents(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of documents"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/documents", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_document(self, document_id: str) -> Dict[str, Any]:
        """Get document details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/documents/{document_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def create_document(self, document_data: Dict) -> Dict[str, Any]:
        """Create document"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/documents", json=document_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_document(self, document_id: str, document_data: Dict) -> Dict[str, Any]:
        """Update document"""
        self._enforce_rate_limit()
        resp = self.session.put(
            f"{self.BASE_URL}/documents/{document_id}",
            json=document_data,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    def delete_document(self, document_id: str) -> Dict[str, Any]:
        """Delete document"""
        self._enforce_rate_limit()
        resp = self.session.delete(f"{self.BASE_URL}/documents/{document_id}", timeout=self.timeout)
        return self._handle_response(resp)

    # Workflows
    def get_workflows(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get workflows"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/workflows", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/workflows/{workflow_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def create_workflow(self, workflow_data: Dict) -> Dict[str, Any]:
        """Create workflow"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/workflows", json=workflow_data, timeout=self.timeout)
        return self._handle_response(resp)

    def start_workflow(self, workflow_id: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Start workflow"""
        self._enforce_rate_limit()
        payload = data if data else {}
        resp = self.session.post(
            f"{self.BASE_URL}/workflows/{workflow_id}/start",
            json=payload,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Form Templates
    def get_form_templates(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get form templates"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/form-templates", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_form_template(self, template_id: str) -> Dict[str, Any]:
        """Get form template details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/form-templates/{template_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def create_form_template(self, template_data: Dict) -> Dict[str, Any]:
        """Create form template"""
        self._enforce_rate_limit()
        resp = self.session.post(
            f"{self.BASE_URL}/form-templates",
            json=template_data,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Requests
    def get_requests(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get requests"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/requests", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_request(self, request_id: str) -> Dict[str, Any]:
        """Get request details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/requests/{request_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def create_request(self, request_data: Dict) -> Dict[str, Any]:
        """Create request"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/requests", json=request_data, timeout=self.timeout)
        return self._handle_response(resp)

    def approve_request(self, request_id: str, comment: Optional[str] = None) -> Dict[str, Any]:
        """Approve request"""
        self._enforce_rate_limit()
        data = {'decision': 'approve'}
        if comment:
            data['comment'] = comment
        resp = self.session.put(
            f"{self.BASE_URL}/requests/{request_id}/decision",
            json=data,
            timeout=self.timeout
        )
        return self._handle_response(resp)

    def reject_request(self, request_id: str, reason: str) -> Dict[str, Any]:
        """Reject request"""
        self._enforce_rate_limit()
        resp = self.session.put(
            f"{self.BASE_URL}/requests/{request_id}/decision",
            json={'decision': 'reject', 'comment': reason},
            timeout=self.timeout
        )
        return self._handle_response(resp)

    # Users & Departments
    def get_users(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get users"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/users", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_departments(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get departments"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/departments", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    # Notifications
    def get_notifications(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get notifications"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/notifications", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def mark_notification_read(self, notification_id: str) -> Dict[str, Any]:
        """Mark notification as read"""
        self._enforce_rate_limit()
        resp = self.session.put(
            f"{self.BASE_URL}/notifications/{notification_id}/read",
            timeout=self.timeout
        )
        return self._handle_response(resp)
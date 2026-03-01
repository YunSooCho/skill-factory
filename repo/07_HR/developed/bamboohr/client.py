"""
BambooHR API Client - HR Management Platform
"""

import requests
import time
import base64
from typing import Optional, Dict, Any, List


class BambooHRError(Exception):
    """Base exception for BambooHR"""

class BambooHRRateLimitError(BambooHRError):
    """Rate limit exceeded"""

class BambooHRAuthenticationError(BambooHRError):
    """Authentication failed"""

class BambooHRClient:
    def __init__(self, subdomain: str, api_key: str, timeout: int = 30):
        """
        Initialize BambooHR client

        Args:
            subdomain: Your BambooHR subdomain (e.g., 'company' from 'company.bamboohr.com')
            api_key: BambooHR API key
            timeout: Request timeout in seconds
        """
        self.subdomain = subdomain
        self.base_url = f"https://api.bamboohr.com/api/gateway.php/{subdomain}"
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()

        # Basic authentication
        auth_string = base64.b64encode(f"{api_key}:x".encode()).decode()
        self.session.headers.update({
            'Authorization': f'Basic {auth_string}',
            'Accept': 'application/json'
        })

        # Rate limiting
        self.last_request_time = 0
        self.min_delay = 0.5  # Conservative rate limiting

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
            raise BambooHRRateLimitError("Rate limit exceeded")
        if resp.status_code == 401 or resp.status_code == 403:
            raise BambooHRAuthenticationError("Authentication failed")
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise BambooHRError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise BambooHRError(f"Error ({resp.status_code}): {resp.text}")

        # Some endpoints return 204 with no content
        if resp.status_code == 204:
            return {}

        return resp.json()

    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, data: Optional[Dict] = None, files: Optional[Dict] = None) -> Dict[str, Any]:
        """Make API request"""
        self._enforce_rate_limit()

        url = f"{self.base_url}/{endpoint}"

        headers = {'Content-Type': 'application/json'} if data else {}

        kwargs = {
            'url': url,
            'method': method,
            'headers': headers,
            'timeout': self.timeout
        }

        if params:
            kwargs['params'] = params
        if data:
            kwargs['json'] = data
        if files:
            kwargs['files'] = files

        resp = self.session.request(**kwargs)
        return self._handle_response(resp)

    # Employees
    def get_employees(self, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get list of all employees

        Args:
            fields: List of fields to return (default: all)
        """
        params = {}
        if fields:
            params['fields'] = ','.join(fields)

        return self._request('GET', 'v1/employees/directory', params=params)

    def get_employee(self, employee_id: str, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get specific employee details

        Args:
            employee_id: Employee ID
            fields: List of fields to return
        """
        params = {}
        if fields:
            params['fields'] = ','.join(fields)

        return self._request('GET', f'v1/employees/{employee_id}', params=params)

    def add_employee(self, employee_data: Dict) -> Dict[str, Any]:
        """
        Add a new employee

        Args:
            employee_data: Employee information
        """
        return self._request('POST', 'v1/employees', data=employee_data)

    def update_employee(self, employee_id: str, employee_data: Dict) -> Dict[str, Any]:
        """
        Update employee information

        Args:
            employee_id: Employee ID
            employee_data: Updated employee information
        """
        return self._request('POST', f'v1/employees/{employee_id}', data=employee_data)

    def get_updated_employees(self, since: str) -> Dict[str, Any]:
        """
        Get list of employees updated since a certain date

        Args:
            since: Date in format YYYY-MM-DD
        """
        params = {'since': since}
        return self._request('GET', 'v1/employees/updated', params=params)

    # Time Off
    def get_time_off_requests(self, employee_id: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
        """
        Get time off requests

        Args:
            employee_id: Filter by employee ID (optional)
            status: Filter by status (e.g., 'approved', 'denied', 'requested')
        """
        params = {}
        if employee_id:
            params['employeeId'] = employee_id
        if status:
            params['status'] = status

        return self._request('GET', 'v1/time_off/requests', params=params)

    def get_time_off_request(self, request_id: str) -> Dict[str, Any]:
        """Get specific time off request details"""
        return self._request('GET', f'v1/time_off/requests/{request_id}')

    def add_time_off_request(self, request_data: Dict) -> Dict[str, Any]:
        """
        Add a time off request

        Args:
            request_data: Time off request information
        """
        return self._request('POST', 'v1/time_off/requests', data=request_data)

    def change_time_off_status(self, request_id: str, status: str) -> Dict[str, Any]:
        """
        Change time off request status

        Args:
            request_id: Time off request ID
            status: New status ('approved' or 'denied')
        """
        return self._request('PUT', f'v1/time_off/requests/{request_id}', data={'status': status})

    # Who's Out
    def get_whos_out(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get list of employees who are out (time off)

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        """
        params = {}
        if start_date:
            params['start'] = start_date
        if end_date:
            params['end'] = end_date

        return self._request('GET', 'v1/time_off/whos_out', params=params)

    # Files
    def get_employee_files(self, employee_id: str, category_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get list of files for an employee

        Args:
            employee_id: Employee ID
            category_id: Filter by category ID (optional)
        """
        params = {}
        if category_id:
            params['categoryId'] = category_id

        return self._request('GET', f'v1/employees/{employee_id}/files', params=params)

    def get_employee_files_categories(self, employee_id: str) -> Dict[str, Any]:
        """Get file categories for an employee"""
        return self._request('GET', f'v1/employees/{employee_id}/files/categories')

    def upload_employee_file(self, employee_id: str, category_id: str, file: Any, file_name: str, share: bool = False) -> Dict[str, Any]:
        """
        Upload a file for an employee

        Args:
            employee_id: Employee ID
            category_id: Category ID
            file: File object
            file_name: File name
            share: Whether to share with employee
        """
        return self._request('POST', f'v1/employees/{employee_id}/files',
                           data={'category': category_id, 'fileName': file_name, 'share': 'yes' if share else 'no'},
                           files={'file': file})

    def download_employee_file(self, employee_id: str, file_id: str) -> requests.Response:
        """
        Download an employee file

        Args:
            employee_id: Employee ID
            file_id: File ID

        Returns:
            Response object with file content
        """
        self._enforce_rate_limit()
        url = f"{self.base_url}/v1/employees/{employee_id}/files/{file_id}"
        resp = self.session.get(url, timeout=self.timeout, stream=True)
        self._handle_response(resp)
        return resp

    # Reports
    def get_reports_list(self) -> Dict[str, Any]:
        """Get list of available reports"""
        return self._request('GET', 'v1/reports')

    def run_report(self, report_id: str, format: str = 'JSON') -> Dict[str, Any]:
        """
        Run a specific report

        Args:
            report_id: Report ID
            format: Output format ('JSON', 'PDF', 'XLS', 'CSV')
        """
        params = {'format': format}
        return self._request('GET', f'v1/reports/{report_id}', params=params)

    # Custom Data (Tabs)
    def get_tabs(self) -> Dict[str, Any]:
        """Get list of custom tabs"""
        return self._request('GET', 'v1/tabs')

    def get_tab_data(self, employee_id: str) -> Dict[str, Any]:
        """Get custom tab data for an employee"""
        return self._request('GET', f'v1/employees/{employee_id}/tables')

    # Company Information
    def get_company_directory(self) -> Dict[str, Any]:
        """Get company directory (all employees with basic info)"""
        return self._request('GET', 'v1/employees/directory')

    def get_meta_data(self) -> Dict[str, Any]:
        """Get metadata (fields, lists, options)"""
        return self._request('GET', 'v1/meta/fields')

    # Tracking Fields
    def get_tracking_categories(self) -> Dict[str, Any]:
        """Get tracking categories"""
        return self._request('GET', 'v1/tracking_categories')

    # Job Info
    def get_job_info(self, employee_id: str) -> Dict[str, Any]:
        """Get job info for an employee"""
        return self._request('GET', f'v1/employees/{employee_id}/job_info')

    def update_job_info(self, employee_id: str, job_data: Dict) -> Dict[str, Any]:
        """Update job info for an employee"""
        return self._request('PUT', f'v1/employees/{employee_id}/job_info', data=job_data)

    # Time Tracking
    def get_time_off_balance(self, employee_id: str) -> Dict[str, Any]:
        """Get time off balance for an employee"""
        return self._request('GET', f'v1/employees/{employee_id}/time_off/balance')

    # Benefits
    def get_benefits_enrollments(self, employee_id: str) -> Dict[str, Any]:
        """Get benefits enrollments for an employee"""
        return self._request('GET', f'v1/employees/{employee_id}/benefits')
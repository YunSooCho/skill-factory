"""
Asana OAuth API Client - Project Management
"""

import requests
import time
from typing import Optional, Dict, Any, List


class AsanaOAuthError(Exception):
    """Base exception for Asana OAuth errors"""
    pass


class AsanaOAuthRateLimitError(AsanaOAuthError):
    """Rate limit exceeded"""
    pass


class AsanaOAuthAuthenticationError(AsanaOAuthError):
    """Authentication failed"""
    pass


class AsanaOAuthClient:
    """Client for Asana OAuth API"""

    BASE_URL = "https://app.asana.com/api/1.0"

    def __init__(self, access_token: str, timeout: int = 30):
        """
        Initialize Asana OAuth client

        Args:
            access_token: Asana OAuth access token
            timeout: Request timeout in seconds
        """
        self.access_token = access_token
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        })
        self.min_delay = 0.1
        self.last_request_time = 0

    def _enforce_rate_limit(self):
        """Enforce rate limiting between requests"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request < self.min_delay:
            time.sleep(self.min_delay - time_since_last_request)

        self.last_request_time = time.time()

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        if response.status_code == 429:
            raise AsanaOAuthRateLimitError("Rate limit exceeded")

        if response.status_code == 401:
            raise AsanaOAuthAuthenticationError("Authentication failed")

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('errors', [{}])[0].get('message', 'Unknown error')
            except:
                error_msg = response.text or response.reason or "Unknown error"
            raise AsanaOAuthError(f"API error ({response.status_code}): {error_msg}")

        return response.json()

    def get_workspaces(self) -> Dict[str, Any]:
        """Get all workspaces"""
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f"{self.BASE_URL}/workspaces",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AsanaOAuthError(f"Request failed: {str(e)}")

    def get_teams(self, workspace_id: str) -> Dict[str, Any]:
        """Get teams in a workspace"""
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f"{self.BASE_URL}/organizations/{workspace_id}/teams",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AsanaOAuthError(f"Request failed: {str(e)}")

    def get_projects(self, workspace: Optional[str] = None, team: Optional[str] = None) -> Dict[str, Any]:
        """Get projects"""
        self._enforce_rate_limit()

        params = {}
        if workspace:
            params['workspace'] = workspace
        if team:
            params['team'] = team

        try:
            response = self.session.get(
                f"{self.BASE_URL}/projects",
                params=params,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AsanaOAuthError(f"Request failed: {str(e)}")

    def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get project details"""
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f"{self.BASE_URL}/projects/{project_id}",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AsanaOAuthError(f"Request failed: {str(e)}")

    def create_project(self, workspace: str, name: str, team: Optional[str] = None) -> Dict[str, Any]:
        """Create project"""
        self._enforce_rate_limit()

        payload = {'workspace': workspace, 'name': name}
        if team:
            payload['team'] = team

        try:
            response = self.session.post(
                f"{self.BASE_URL}/projects",
                json={'data': payload},
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AsanaOAuthError(f"Request failed: {str(e)}")

    def update_project(self, project_id: str, **kwargs) -> Dict[str, Any]:
        """Update project"""
        self._enforce_rate_limit()

        try:
            response = self.session.put(
                f"{self.BASE_URL}/projects/{project_id}",
                json={'data': kwargs},
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AsanaOAuthError(f"Request failed: {str(e)}")

    def get_tasks(self, project: Optional[str] = None,
                  assignee: Optional[str] = None,
                  completed: bool = False) -> Dict[str, Any]:
        """Get tasks"""
        self._enforce_rate_limit()

        params = {'completed': str(completed).lower()}
        if project:
            params['project'] = project
        if assignee:
            params['assignee'] = assignee

        try:
            response = self.session.get(
                f"{self.BASE_URL}/tasks",
                params=params,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AsanaOAuthError(f"Request failed: {str(e)}")

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get task details"""
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f"{self.BASE_URL}/tasks/{task_id}",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AsanaOAuthError(f"Request failed: {str(e)}")

    def create_task(self, workspace: str, name: str,
                    project: Optional[str] = None,
                    assignee: Optional[str] = None,
                    due_on: Optional[str] = None) -> Dict[str, Any]:
        """Create task"""
        self._enforce_rate_limit()

        payload = {'workspace': workspace, 'name': name}
        if project:
            payload['projects'] = [project]
        if assignee:
            payload['assignee'] = assignee
        if due_on:
            payload['due_on'] = due_on

        try:
            response = self.session.post(
                f"{self.BASE_URL}/tasks",
                json={'data': payload},
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AsanaOAuthError(f"Request failed: {str(e)}")

    def update_task(self, task_id: str, **kwargs) -> Dict[str, Any]:
        """Update task"""
        self._enforce_rate_limit()

        try:
            response = self.session.put(
                f"{self.BASE_URL}/tasks/{task_id}",
                json={'data': kwargs},
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AsanaOAuthError(f"Request failed: {str(e)}")

    def complete_task(self, task_id: str) -> Dict[str, Any]:
        """Complete task"""
        return self.update_task(task_id, completed=True)

    def delete_task(self, task_id: str) -> Dict[str, Any]:
        """Delete task"""
        self._enforce_rate_limit()

        try:
            response = self.session.delete(
                f"{self.BASE_URL}/tasks/{task_id}",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AsanaOAuthError(f"Request failed: {str(e)}")

    def get_sections(self, project_id: str) -> Dict[str, Any]:
        """Get project sections"""
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f"{self.BASE_URL}/projects/{project_id}/sections",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AsanaOAuthError(f"Request failed: {str(e)}")

    def create_section(self, project_id: str, name: str) -> Dict[str, Any]:
        """Create section"""
        self._enforce_rate_limit()

        try:
            response = self.session.post(
                f"{self.BASE_URL}/projects/{project_id}/sections",
                json={'data': {'name': name}},
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AsanaOAuthError(f"Request failed: {str(e)}")

    def add_task_to_section(self, section_id: str, task_id: str) -> Dict[str, Any]:
        """Add task to section"""
        self._enforce_rate_limit()

        try:
            response = self.session.post(
                f"{self.BASE_URL}/sections/{section_id}/addTask",
                json={'data': {'task': task_id}},
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AsanaOAuthError(f"Request failed: {str(e)}")

    def get_users(self, workspace: str) -> Dict[str, Any]:
        """Get users in workspace"""
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f"{self.BASE_URL}/workspaces/{workspace}/users",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AsanaOAuthError(f"Request failed: {str(e)}")

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user details"""
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f"{self.BASE_URL}/users/{user_id}",
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AsanaOAuthError(f"Request failed: {str(e)}")

    def add_comment_to_task(self, task_id: str, text: str) -> Dict[str, Any]:
        """Add comment to task"""
        self._enforce_rate_limit()

        try:
            response = self.session.post(
                f"{self.BASE_URL}/tasks/{task_id}/stories",
                json={'data': {'text': text}},
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AsanaOAuthError(f"Request failed: {str(e)}")

    def search_tasks(self, query: str, workspace: Optional[str] = None) -> Dict[str, Any]:
        """Search tasks"""
        self._enforce_rate_limit()

        params = {'query': query}
        if workspace:
            params['workspace'] = workspace

        try:
            response = self.session.get(
                f"{self.BASE_URL}/tasks/search",
                params=params,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AsanaOAuthError(f"Request failed: {str(e)}")

    def get_portfolios(self, workspace: str) -> Dict[str, Any]:
        """Get portfolios"""
        self._enforce_rate_limit()

        try:
            response = self.session.get(
                f"{self.BASE_URL}/portfolios",
                params={'workspace': workspace},
                timeout=self.timeout
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            raise AsanaOAuthError(f"Request failed: {str(e)}")

    def attach_file_to_task(self, task_id: str, file_path: str) -> Dict[str, Any]:
        """Attach file to task"""
        self._enforce_rate_limit()

        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = self.session.post(
                    f"{self.BASE_URL}/tasks/{task_id}/attachments",
                    files=files,
                    timeout=self.timeout
                )
            return self._handle_response(response)
        except Exception as e:
            raise AsanaOAuthError(f"Request failed: {str(e)}")
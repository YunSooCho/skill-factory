import requests
from typing import Dict, List, Optional, Any


class TookanClient:
    """Client for Tookan field workforce API."""

    BASE_URL = "https://api.tookanapp.com/api"

    def __init__(self, api_key: str):
        """
        Initialize Tookan client.

        Args:
            api_key: Your Tookan API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to Tookan API."""
        url = f"{self.BASE_URL}{endpoint}"
        request_data = {"api_key": self.api_key}
        if data:
            request_data.update(data)
        try:
            response = self.session.request(method, url, json=request_data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def create_task(self, job_type: str, job_description: str,
                   customer_email: str, customer_address: str,
                   fleet_id: str = None, has_pickup: bool = False) -> Dict[str, Any]:
        """Create a new task/job."""
        data = {
            "job_type": job_type,
            "job_description": job_description,
            "customer_email": customer_email,
            "customer_address": customer_address
        }
        if fleet_id:
            data["fleet_id"] = fleet_id
        if has_pickup:
            data["has_pickup"] = 1
        return self._request("POST", "/add_task", data)

    def get_task(self, job_id: str) -> Dict[str, Any]:
        """Get task details."""
        return self._request("GET", "/get_job_details", {"job_id": job_id})

    def list_tasks(self, page: int = 1, limit: int = 100, status: str = None) -> Dict[str, Any]:
        """List all tasks."""
        data = {
            "page": page,
            "limit": limit
        }
        if status:
            data["status"] = status
        return self._request("GET", "/fetch_job", data)

    def update_task(self, job_id: str, data: Dict) -> Dict[str, Any]:
        """Update task."""
        data["job_id"] = job_id
        return self._request("POST", "/edit_task", data)

    def delete_task(self, job_id: str) -> Dict[str, Any]:
        """Delete task."""
        return self._request("POST", "/delete_job", {"job_id": job_id})

    def get_fleets(self) -> Dict[str, Any]:
        """Get all fleets."""
        return self._request("GET", "/view_all_fleets")

    def get_agents(self) -> Dict[str, Any]:
        """Get all agents."""
        return self._request("GET", "/view_all_agents")

    def get_agent(self, agent_id: str) -> Dict[str, Any]:
        """Get agent details."""
        return self._request("GET", "/view_agent_details", {"agent_id": agent_id})

    def assign_task(self, job_id: str, agent_id: str) -> Dict[str, Any]:
        """Assign task to agent."""
        return self._request("POST", "/assign_job", {"job_id": job_id, "agent_id": agent_id})

    def unassign_task(self, job_id: str) -> Dict[str, Any]:
        """Unassign task."""
        return self._request("POST", "/delete_agent_from_job", {"job_id": job_id})

    def get_templates(self) -> Dict[str, Any]:
        """Get job templates."""
        return self._request("GET", "/all_templates")

    def get_customers(self) -> Dict[str, Any]:
        """Get all customers."""
        return self._request("GET", "/view_all_customers")

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """Get customer details."""
        return self._request("GET", "/view_customer_details", {"customer_id": customer_id})

    def get_jobs_by_date(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get jobs by date range."""
        return self._request("GET", "/list_jobs_by_date", {
            "start_date": start_date,
            "end_date": end_date
        })

    def create_team(self, team_name: str, admin_id: str) -> Dict[str, Any]:
        """Create a team."""
        return self._request("POST", "/create_team", {
            "team_name": team_name,
            "admin_id": admin_id
        })

    def get_teams(self) -> Dict[str, Any]:
        """Get all teams."""
        return self._request("GET", "/list_team")
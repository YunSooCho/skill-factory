"""
Senses API Client
API Documentation: https://docs.senses.co.jp/
"""

import requests
from typing import Optional, Dict, List, Any


class SensesAPIError(Exception):
    """Custom exception for Senses API errors."""
    pass


class SensesClient:
    """Client for Senses API - Marketing automation platform."""

    def __init__(self, api_key: str, base_url: str = "https://api.senses.co.jp"):
        """
        Initialize Senses API client.

        Args:
            api_key: Your Senses API key
            base_url: API base URL (default: https://api.senses.co.jp)
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make API request with error handling.

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional request arguments

        Returns:
            Response data
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()

            data = response.json()
            return {
                "status": "success",
                "data": data,
                "status_code": response.status_code
            }

        except requests.exceptions.HTTPError as e:
            error_data = self._parse_error(response)
            raise SensesAPIError(
                f"HTTP {response.status_code}: {error_data.get('message', str(e))}"
            )
        except requests.exceptions.RequestException as e:
            raise SensesAPIError(f"Request failed: {str(e)}")

    def _parse_error(self, response: requests.Response) -> Dict[str, Any]:
        """Parse error response."""
        try:
            return response.json() if response.content else {"message": response.text}
        except Exception:
            return {"message": response.text}

    def create_form(
        self,
        name: str,
        fields: List[Dict[str, Any]],
        success_message: Optional[str] = None,
        thank_you_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a form (Create Form).

        API Reference: Forms endpoint

        Args:
            name: Form name
            fields: List of field definitions with type, name, label, required
            success_message: Success message to display
            thank_you_url: Thank you page URL

        Returns:
            Created form information with ID
        """
        endpoint = "/forms"

        data = {
            "name": name,
            "fields": fields
        }

        if success_message:
            data["success_message"] = success_message
        if thank_you_url:
            data["thank_you_url"] = thank_you_url

        return self._make_request("POST", endpoint, json=data)

    def get_form(self, form_id: int) -> Dict[str, Any]:
        """
        Get form details (Get Form).

        Args:
            form_id: Form ID

        Returns:
            Form details
        """
        endpoint = f"/forms/{form_id}"
        return self._make_request("GET", endpoint)

    def update_form(
        self,
        form_id: int,
        name: Optional[str] = None,
        fields: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Update a form (Update Form).

        Args:
            form_id: Form ID
            name: Form name
            fields: Field definitions

        Returns:
            Updated form information
        """
        endpoint = f"/forms/{form_id}"

        data = {}
        if name:
            data["name"] = name
        if fields:
            data["fields"] = fields

        return self._make_request("PUT", endpoint, json=data)

    def delete_form(self, form_id: int) -> Dict[str, Any]:
        """
        Delete a form (Delete Form).

        Args:
            form_id: Form ID

        Returns:
            Deletion confirmation
        """
        endpoint = f"/forms/{form_id}"
        return self._make_request("DELETE", endpoint)

    def create_landing_page(
        self,
        name: str,
        content: str,
        domain: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a landing page (Create Landing Page).

        Args:
            name: Landing page name
            content: HTML content
            domain: Custom domain

        Returns:
            Created landing page information with ID
        """
        endpoint = "/landing-pages"

        data = {
            "name": name,
            "content": content
        }

        if domain:
            data["domain"] = domain

        return self._make_request("POST", endpoint, json=data)

    def get_landing_page(self, page_id: int) -> Dict[str, Any]:
        """
        Get landing page details (Get Landing Page).

        Args:
            page_id: Landing page ID

        Returns:
            Landing page details
        """
        endpoint = f"/landing-pages/{page_id}"
        return self._make_request("GET", endpoint)

    def update_landing_page(
        self,
        page_id: int,
        name: Optional[str] = None,
        content: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update a landing page (Update Landing Page).

        Args:
            page_id: Landing page ID
            name: Landing page name
            content: HTML content

        Returns:
            Updated landing page information
        """
        endpoint = f"/landing-pages/{page_id}"

        data = {}
        if name:
            data["name"] = name
        if content:
            data["content"] = content

        return self._make_request("PUT", endpoint, json=data)

    def delete_landing_page(self, page_id: int) -> Dict[str, Any]:
        """
        Delete a landing page (Delete Landing Page).

        Args:
            page_id: Landing page ID

        Returns:
            Deletion confirmation
        """
        endpoint = f"/landing-pages/{page_id}"
        return self._make_request("DELETE", endpoint)

    def create_campaign(
        self,
        name: str,
        type: str,
        status: str = "draft"
    ) -> Dict[str, Any]:
        """
        Create a campaign (Create Campaign).

        Args:
            name: Campaign name
            type: Campaign type (email, sms, push)
            status: Status (draft, active, paused)

        Returns:
            Created campaign information with ID
        """
        endpoint = "/campaigns"

        data = {
            "name": name,
            "type": type,
            "status": status
        }

        return self._make_request("POST", endpoint, json=data)

    def get_campaign(self, campaign_id: int) -> Dict[str, Any]:
        """
        Get campaign details (Get Campaign).

        Args:
            campaign_id: Campaign ID

        Returns:
            Campaign details
        """
        endpoint = f"/campaigns/{campaign_id}"
        return self._make_request("GET", endpoint)

    def update_campaign(
        self,
        campaign_id: int,
        name: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update a campaign (Update Campaign).

        Args:
            campaign_id: Campaign ID
            name: Campaign name
            status: Status

        Returns:
            Updated campaign information
        """
        endpoint = f"/campaigns/{campaign_id}"

        data = {}
        if name:
            data["name"] = name
        if status:
            data["status"] = status

        return self._make_request("PUT", endpoint, json=data)

    def delete_campaign(self, campaign_id: int) -> Dict[str, Any]:
        """
        Delete a campaign (Delete Campaign).

        Args:
            campaign_id: Campaign ID

        Returns:
            Deletion confirmation
        """
        endpoint = f"/campaigns/{campaign_id}"
        return self._make_request("DELETE", endpoint)

    def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        phone: Optional[str] = None,
        custom_attributes: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a user (Create User).

        Args:
            email: User email
            first_name: First name
            last_name: Last name
            phone: Phone number
            custom_attributes: Custom attributes

        Returns:
            Created user information with ID
        """
        endpoint = "/users"

        data = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name
        }

        if phone:
            data["phone"] = phone
        if custom_attributes:
            data["custom_attributes"] = custom_attributes

        return self._make_request("POST", endpoint, json=data)

    def get_user(self, user_id: int) -> Dict[str, Any]:
        """
        Get user details (Get User).

        Args:
            user_id: User ID

        Returns:
            User details
        """
        endpoint = f"/users/{user_id}"
        return self._make_request("GET", endpoint)

    def update_user(
        self,
        user_id: int,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update a user (Update User).

        Args:
            user_id: User ID
            email: Email address
            first_name: First name
            last_name: Last name
            phone: Phone number

        Returns:
            Updated user information
        """
        endpoint = f"/users/{user_id}"

        data = {}
        if email:
            data["email"] = email
        if first_name:
            data["first_name"] = first_name
        if last_name:
            data["last_name"] = last_name
        if phone:
            data["phone"] = phone

        return self._make_request("PUT", endpoint, json=data)

    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """
        Delete a user (Delete User).

        Args:
            user_id: User ID

        Returns:
            Deletion confirmation
        """
        endpoint = f"/users/{user_id}"
        return self._make_request("DELETE", endpoint)

    def create_email_template(
        self,
        name: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create an email template (Create Email Template).

        Args:
            name: Template name
            subject: Email subject
            html_content: HTML body content
            text_content: Plain text content

        Returns:
            Created email template information with ID
        """
        endpoint = "/email-templates"

        data = {
            "name": name,
            "subject": subject,
            "html_content": html_content
        }

        if text_content:
            data["text_content"] = text_content

        return self._make_request("POST", endpoint, json=data)

    def send_email(
        self,
        to: str,
        subject: str,
        html_content: str,
        template_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Send an email (Send Email).

        Args:
            to: Recipient email
            subject: Email subject
            html_content: HTML content
            template_id: Template ID (if using template)

        Returns:
            Sent email information with ID
        """
        endpoint = "/emails/send"

        data = {
            "to": to,
            "subject": subject,
            "html_content": html_content
        }

        if template_id:
            data["template_id"] = template_id

        return self._make_request("POST", endpoint, json=data)

    def create_segment(
        self,
        name: str,
        criteria: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a segment (Create Segment).

        Args:
            name: Segment name
            criteria: Segment criteria (filters)

        Returns:
            Created segment information with ID
        """
        endpoint = "/segments"

        data = {
            "name": name,
            "criteria": criteria
        }

        return self._make_request("POST", endpoint, json=data)

    def get_segment(self, segment_id: int) -> Dict[str, Any]:
        """
        Get segment details (Get Segment).

        Args:
            segment_id: Segment ID

        Returns:
            Segment details
        """
        endpoint = f"/segments/{segment_id}"
        return self._make_request("GET", endpoint)

    def update_segment(
        self,
        segment_id: int,
        name: Optional[str] = None,
        criteria: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Update a segment (Update Segment).

        Args:
            segment_id: Segment ID
            name: Segment name
            criteria: Segment criteria

        Returns:
            Updated segment information
        """
        endpoint = f"/segments/{segment_id}"

        data = {}
        if name:
            data["name"] = name
        if criteria:
            data["criteria"] = criteria

        return self._make_request("PUT", endpoint, json=data)

    def delete_segment(self, segment_id: int) -> Dict[str, Any]:
        """
        Delete a segment (Delete Segment).

        Args:
            segment_id: Segment ID

        Returns:
            Deletion confirmation
        """
        endpoint = f"/segments/{segment_id}"
        return self._make_request("DELETE", endpoint)

    def create_workflow(
        self,
        name: str,
        trigger: Dict[str, Any],
        actions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create a workflow (Create Workflow).

        Args:
            name: Workflow name
            trigger: Trigger configuration
            actions: List of actions to execute

        Returns:
            Created workflow information with ID
        """
        endpoint = "/workflows"

        data = {
            "name": name,
            "trigger": trigger,
            "actions": actions
        }

        return self._make_request("POST", endpoint, json=data)

    def get_workflow(self, workflow_id: int) -> Dict[str, Any]:
        """
        Get workflow details (Get Workflow).

        Args:
            workflow_id: Workflow ID

        Returns:
            Workflow details
        """
        endpoint = f"/workflows/{workflow_id}"
        return self._make_request("GET", endpoint)

    def update_workflow(
        self,
        workflow_id: int,
        name: Optional[str] = None,
        active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Update a workflow (Update Workflow).

        Args:
            workflow_id: Workflow ID
            name: Workflow name
            active: Active status

        Returns:
            Updated workflow information
        """
        endpoint = f"/workflows/{workflow_id}"

        data = {}
        if name:
            data["name"] = name
        if active is not None:
            data["active"] = active

        return self._make_request("PUT", endpoint, json=data)

    def delete_workflow(self, workflow_id: int) -> Dict[str, Any]:
        """
        Delete a workflow (Delete Workflow).

        Args:
            workflow_id: Workflow ID

        Returns:
            Deletion confirmation
        """
        endpoint = f"/workflows/{workflow_id}"
        return self._make_request("DELETE", endpoint)

    def trigger_workflow(self, workflow_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Trigger a workflow manually (Trigger Workflow).

        Args:
            workflow_id: Workflow ID
            data: Workflow trigger data

        Returns:
            Trigger result
        """
        endpoint = f"/workflows/{workflow_id}/trigger"
        return self._make_request("POST", endpoint, json=data)

    def get_analytics(
        self,
        type: str,
        start_date: str,
        end_date: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get analytics (Get Analytics).

        Args:
            type: Analytics type (email, form, landing_page, campaign)
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            filters: Additional filters

        Returns:
            Analytics data
        """
        endpoint = f"/analytics/{type}"

        params = {
            "start_date": start_date,
            "end_date": end_date
        }

        if filters:
            params.update(filters)

        return self._make_request("GET", endpoint, params=params)
"""
Brevo API Client

Supports:
- Get Contact
- Create Contact
- Update Contact
- Add Contact to List
- Send Transactional Email
- Create SMS Campaign
- Send SMS Campaign
- Create WhatsApp Campaign
- Get Email Campaign Report
- Send Campaign Report
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class Contact:
    """Brevo contact representation"""
    id: Optional[int] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
    list_ids: List[int] = None
    attributes_blacklisted: bool = False
    email_blacklisted: bool = False
    sms_blacklisted: bool = False
    created_at: Optional[str] = None
    modified_at: Optional[str] = None

    def __post_init__(self):
        if self.list_ids is None:
            self.list_ids = []


@dataclass
class Campaign:
    """Brevo campaign representation"""
    id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    subject: Optional[str] = None
    created_at: Optional[str] = None
    scheduled_at: Optional[str] = None


@dataclass
class CampaignStats:
    """Campaign statistics"""
    sent: int = 0
    delivered: int = 0
    opened: int = 0
    clicked: int = 0
    bounced: int = 0
    complaints: int = 0
    unsubscribed: int = 0


class BrevoClient:
    """
    Brevo API client for email, SMS, and WhatsApp marketing.

    Authentication: API Key (Header: api-key)
    Base URL: https://api.brevo.com/v3
    """

    BASE_URL = "https://api.brevo.com/v3"

    def __init__(self, api_key: str):
        """
        Initialize Brevo client.

        Args:
            api_key: Brevo API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request with error handling"""
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)

            if response.status_code in (200, 201, 202, 204):
                if response.status_code == 204:
                    return {}
                data = response.json()
                return data
            elif response.status_code == 401:
                raise Exception("Authentication failed: Invalid API key")
            elif response.status_code == 404:
                raise Exception(f"Resource not found: {endpoint}")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded")
            elif response.status_code >= 500:
                raise Exception(f"Server error: {response.status_code}")
            else:
                error_data = response.json() if response.content else {}
                raise Exception(f"API error {response.status_code}: {error_data}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    # ==================== Contact Operations ====================

    def create_contact(
        self,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        list_ids: Optional[List[int]] = None,
        email_blacklisted: bool = False,
        sms_blacklisted: bool = False
    ) -> Contact:
        """
        Create a new contact.

        Args:
            email: Email address (required)
            first_name: First name
            last_name: Last name
            attributes: Custom attributes
            list_ids: List IDs to add contact to
            email_blacklisted: Blacklist from emails
            sms_blacklisted: Blacklist from SMS

        Returns:
            Contact object
        """
        if not email:
            raise ValueError("Email is required")

        payload: Dict[str, Any] = {"email": email, "updateEnabled": False}

        if first_name:
            payload["attributes"] = payload.get("attributes", {})
            payload["attributes"]["FIRSTNAME"] = first_name
        if last_name:
            payload["attributes"] = payload.get("attributes", {})
            payload["attributes"]["LASTNAME"] = last_name
        if attributes:
            payload["attributes"] = {**(payload.get("attributes", {})), **attributes}
        if list_ids:
            payload["listIds"] = list_ids
        if email_blacklisted:
            payload["emailBlacklisted"] = email_blacklisted
        if sms_blacklisted:
            payload["smsBlacklisted"] = sms_blacklisted

        result = self._request("POST", "/contacts", json=payload)
        return self._parse_contact(result)

    def get_contact(self, email: str) -> Contact:
        """
        Retrieve a contact by email.

        Args:
            email: Email address

        Returns:
            Contact object
        """
        if not email:
            raise ValueError("Email is required")

        result = self._request("GET", f"/contacts/{email}")
        return self._parse_contact(result)

    def update_contact(
        self,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        list_ids: Optional[List[int]] = None,
        email_blacklisted: Optional[bool] = None,
        sms_blacklisted: Optional[bool] = None
    ) -> Contact:
        """
        Update an existing contact.

        Args:
            email: Email address
            first_name: First name
            last_name: Last name
            attributes: Updated custom attributes
            list_ids: Updated list IDs
            email_blacklisted: Update email blacklist status
            sms_blacklisted: Update SMS blacklist status

        Returns:
            Updated Contact object
        """
        if not email:
            raise ValueError("Email is required")

        payload: Dict[str, Any] = {}

        if first_name:
            payload["attributes"] = payload.get("attributes", {})
            payload["attributes"]["FIRSTNAME"] = first_name
        if last_name:
            payload["attributes"] = payload.get("attributes", {})
            payload["attributes"]["LASTNAME"] = last_name
        if attributes:
            payload["attributes"] = {**(payload.get("attributes", {})), **attributes}
        if list_ids:
            payload["listIds"] = list_ids
        if email_blacklisted is not None:
            payload["emailBlacklisted"] = email_blacklisted
        if sms_blacklisted is not None:
            payload["smsBlacklisted"] = sms_blacklisted

        result = self._request("PUT", f"/contacts/{email}", json=payload)
        return self._parse_contact(result)

    def add_contact_to_list(self, email: str, list_id: int) -> Dict[str, Any]:
        """
        Add an existing contact to a list.

        Args:
            email: Email address
            list_id: List ID

        Returns:
            Response data
        """
        contact = self.get_contact(email)
        current_lists = contact.list_ids or []

        if list_id not in current_lists:
            current_lists.append(list_id)

        return self.update_contact(email, list_ids=current_lists).__dict__

    # ==================== Transactional Email ====================

    def send_transactional_email(
        self,
        to: List[Dict[str, str]],
        subject: str,
        html_content: Optional[str] = None,
        text_content: Optional[str] = None,
        sender: Optional[Dict[str, str]] = None,
        reply_to: Optional[Dict[str, str]] = None,
        cc: Optional[List[Dict[str, str]]] = None,
        bcc: Optional[List[Dict[str, str]]] = None,
        tags: Optional[List[str]] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send a transactional email.

        Args:
            to: List of recipients [{"email": "user@example.com", "name": "John"}]
            subject: Email subject
            html_content: HTML email body
            text_content: Plain text email body
            sender: Sender info {"email": "sender@example.com", "name": "Sender"}
            reply_to: Reply-to info
            cc: CC recipients
            bcc: BCC recipients
            tags: Email tags
            headers: Custom headers
            params: Template parameters

        Returns:
            Send response with message ID
        """
        if not to:
            raise ValueError("At least one recipient required")
        if not subject:
            raise ValueError("Subject is required")
        if not html_content and not text_content:
            raise ValueError("Either html_content or text_content required")

        payload: Dict[str, Any] = {
            "to": to,
            "subject": subject
        }

        if html_content:
            payload["htmlContent"] = html_content
        if text_content:
            payload["textContent"] = text_content
        if sender:
            payload["sender"] = sender
        if reply_to:
            payload["replyTo"] = reply_to
        if cc:
            payload["cc"] = cc
        if bcc:
            payload["bcc"] = bcc
        if tags:
            payload["tags"] = tags
        if headers:
            payload["headers"] = headers
        if params:
            payload["params"] = params

        return self._request("POST", "/smtp/email", json=payload)

    # ==================== SMS Operations ====================

    def create_sms_campaign(
        self,
        name: str,
        sender: str,
        content: str,
        recipients: Dict[str, Any],
        scheduled_at: Optional[str] = None
    ) -> Campaign:
        """
        Create an SMS campaign.

        Args:
            name: Campaign name
            sender: Sender name (3-11 alphanumeric characters)
            content: SMS content (max 160 characters)
            recipients: Recipients info {"listIds": [1, 2]} or {"excludedListIds": [1]}
            scheduled_at: Scheduled datetime (ISO format)

        Returns:
            Campaign object
        """
        payload = {
            "name": name,
            "sender": sender,
            "content": content,
            "recipients": recipients
        }

        if scheduled_at:
            payload["scheduledAt"] = scheduled_at

        result = self._request("POST", "/sms/campaigns", json=payload)
        return self._parse_campaign(result)

    def send_sms_now(self, campaign_id: int) -> Dict[str, Any]:
        """
        Send an SMS campaign immediately.

        Args:
            campaign_id: Campaign ID

        Returns:
            Send response
        """
        return self._request("POST", f"/sms/campaigns/{campaign_id}/sendNow")

    # ==================== WhatsApp Operations ====================

    def create_whatsapp_campaign(
        self,
        name: str,
        template_id: int,
        recipients: Dict[str, Any]
    ) -> Campaign:
        """
        Create and send a WhatsApp campaign.

        Args:
            name: Campaign name
            template_id: WhatsApp template ID
            recipients: Recipients info

        Returns:
            Campaign object
        """
        payload = {
            "name": name,
            "templateId": template_id,
            "recipients": recipients
        }

        result = self._request("POST", "/whatsapp/campaigns", json=payload)
        return self._parse_campaign(result)

    # ==================== Campaign Reports ====================

    def get_email_campaign_report(self, campaign_id: int) -> CampaignStats:
        """
        Get email campaign report statistics.

        Args:
            campaign_id: Campaign ID

        Returns:
            CampaignStats object
        """
        result = self._request("GET", f"/emailCampaigns/{campaign_id}/stats")

        return CampaignStats(
            sent=result.get("sent", 0),
            delivered=result.get("delivered", 0),
            opened=result.get("opened", 0),
            clicked=result.get("clicked", 0),
            bounced=result.get("bounced", 0),
            complaints=result.get("complaints", 0),
            unsubscribed=result.get("unsubscribed", 0)
        )

    def send_campaign_report(
        self,
        campaign_id: int,
        email: str,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Send a campaign report to an email.

        Args:
            campaign_id: Campaign ID
            email: Recipient email address
            language: Report language (en, fr, etc.)

        Returns:
            Send response
        """
        return self._request(
            "POST",
            f"/reports/{campaign_id}/email",
            params={"email": email, "language": language}
        )

    # ==================== Webhook Operations ====================

    def verify_webhook(self, signature: str, payload: bytes, webhook_key: str) -> bool:
        """
        Verify a webhook signature.

        Args:
            signature: Signature from X-Signature header
            payload: Raw webhook payload bytes
            webhook_key: Your webhook key

        Returns:
            True if signature is valid
        """
        import hmac
        import hashlib

        expected_signature = hmac.new(
            webhook_key.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected_signature)

    # ==================== Helper Methods ====================

    def _parse_contact(self, data: Dict[str, Any]) -> Contact:
        """Parse contact data from API response"""
        return Contact(
            id=data.get("id"),
            email=data.get("email"),
            first_name=data.get("attributes", {}).get("FIRSTNAME"),
            last_name=data.get("attributes", {}).get("LASTNAME"),
            attributes=data.get("attributes"),
            list_ids=data.get("listIds", []),
            email_blacklisted=data.get("emailBlacklisted", False),
            sms_blacklisted=data.get("smsBlacklisted", False),
            attributes_blacklisted=data.get("attributesBlacklisted", False),
            created_at=data.get("createdAt"),
            modified_at=data.get("modifiedAt")
        )

    def _parse_campaign(self, data: Dict[str, Any]) -> Campaign:
        """Parse campaign data from API response"""
        return Campaign(
            id=data.get("id"),
            name=data.get("name"),
            type=data.get("type"),
            status=data.get("status"),
            subject=data.get("subject"),
            created_at=data.get("createdAt"),
            scheduled_at=data.get("scheduledAt")
        )

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    api_key = "your_brevo_api_key"

    client = BrevoClient(api_key=api_key)

    try:
        # Create contact
        contact = client.create_contact(
            email="user@example.com",
            first_name="John",
            last_name="Doe",
            list_ids=[1],
            attributes={"COUNTRY": "Japan", "PLAN": "Premium"}
        )
        print(f"Contact created: {contact.email} (ID: {contact.id})")

        # Get contact
        fetched = client.get_contact("user@example.com")
        print(f"Fetched: {fetched.first_name} {fetched.last_name}")

        # Send transactional email
        client.send_transactional_email(
            to=[{"email": "recipient@example.com", "name": "Recipient"}],
            subject="Welcome!",
            html_content="<h1>Welcome to our service!</h1><p>Thank you for signing up.</p>",
            sender={"email": "noreply@example.com", "name": "Your Company"},
            tags=["welcome", "onboarding"]
        )
        print("Email sent successfully")

        # Create SMS campaign
        sms_campaign = client.create_sms_campaign(
            name="Promo SMS",
            sender="YOURBRAND",
            content="Special offer: 50% off! Visit our store today.",
            recipients={"listIds": [2]},
            scheduled_at="2024-01-20T10:00:00Z"
        )
        print(f"SMS campaign created: {sms_campaign.id}")

        # Send SMS immediately
        client.send_sms_now(sms_campaign.id)
        print("SMS sent immediately")

        # Get campaign stats
        stats = client.get_email_campaign_report(123)
        print(f"Email stats - Sent: {stats.sent}, Opened: {stats.opened}, Clicked: {stats.clicked}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()
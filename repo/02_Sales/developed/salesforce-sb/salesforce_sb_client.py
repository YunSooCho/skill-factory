"""
Salesforce Sb API Client
API Documentation: https://developer.salesforce.com/docs/api/rest/
"""

import requests
from typing import Optional, Dict, List, Any


class SalesforceSbAPIError(Exception):
    """Custom exception for Salesforce Sb API errors."""
    pass


class SalesforceSbClient:
    """Client for Salesforce S&B (Sales & Business integration) API."""

    def __init__(
        self,
        instance_url: str,
        access_token: str,
        api_version: str = "56.0"
    ):
        """
        Initialize Salesforce Sb API client.

        Args:
            instance_url: Your Salesforce instance URL (e.g., https://yourname.my.salesforce.com)
            access_token: OAuth access token
            api_version: API version (default: 56.0)
        """
        self.instance_url = instance_url
        self.access_token = access_token
        self.api_version = api_version
        self.base_url = f"{instance_url}/services/data/v{api_version}"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
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
            raise SalesforceSbAPIError(
                f"HTTP {response.status_code}: {error_data.get('message', str(e))}"
            )
        except requests.exceptions.RequestException as e:
            raise SalesforceSbAPIError(f"Request failed: {str(e)}")

    def _parse_error(self, response: requests.Response) -> Dict[str, Any]:
        """Parse error response."""
        try:
            return response.json() if response.content else {"message": response.text}
        except Exception:
            return {"message": response.text}

    def query(self, soql: str) -> Dict[str, Any]:
        """
        Execute SOQL query.

        API Reference: REST API Query endpoint

        Args:
            soql: SOQL query string

        Returns:
            Query results
        """
        endpoint = f"/query?q={soql}"
        return self._make_request("GET", endpoint)

    def query_all(self, soql: str) -> Dict[str, Any]:
        """
        Execute SOQL query including deleted records.

        Args:
            soql: SOQL query string

        Returns:
            Query results including deleted/archived records
        """
        endpoint = f"/queryAll?q={soql}"
        return self._make_request("GET", endpoint)

    def create_object(
        self,
        object_type: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a new object record.

        Args:
            object_type: Salesforce object type (Account, Contact, Opportunity, etc.)
            data: Object field data

        Returns:
            Created object with ID
        """
        endpoint = f"/sobjects/{object_type}/"
        return self._make_request("POST", endpoint, json=data)

    def get_object(
        self,
        object_type: str,
        record_id: str,
        fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get object record by ID.

        Args:
            object_type: Salesforce object type
            record_id: Record ID
            fields: List of fields to retrieve

        Returns:
            Object record
        """
        endpoint = f"/sobjects/{object_type}/{record_id}"
        return self._make_request("GET", endpoint)

    def update_object(
        self,
        object_type: str,
        record_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update object record.

        Args:
            object_type: Salesforce object type
            record_id: Record ID
            data: Fields to update

        Returns:
            Update confirmation
        """
        endpoint = f"/sobjects/{object_type}/{record_id}"
        return self._make_request("PATCH", endpoint, json=data)

    def delete_object(
        self,
        object_type: str,
        record_id: str
    ) -> Dict[str, Any]:
        """
        Delete object record.

        Args:
            object_type: Salesforce object type
            record_id: Record ID

        Returns:
            Deletion confirmation
        """
        endpoint = f"/sobjects/{object_type}/{record_id}"
        return self._make_request("DELETE", endpoint)

    def upsert_object(
        self,
        object_type: str,
        external_id_field: str,
        external_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Upsert object record.

        Args:
            object_type: Salesforce object type
            external_id_field: External ID field name
            external_id: External ID value
            data: Object field data

        Returns:
            Upserted object with ID
        """
        endpoint = f"/sobjects/{object_type}/{external_id_field}/{external_id}"
        return self._make_request("PATCH", endpoint, json=data)

    def create_account(
        self,
        name: str,
        type: str = "Customer",
        billing_city: Optional[str] = None,
        billing_country: Optional[str] = None,
        billing_postal_code: Optional[str] = None,
        billing_state: Optional[str] = None,
        billing_street: Optional[str] = None,
        billing_latitude: Optional[float] = None,
        billing_longitude: Optional[float] = None,
        shipping_city: Optional[str] = None,
        shipping_country: Optional[str] = None,
        shipping_postal_code: Optional[str] = None,
        shipping_state: Optional[str] = None,
        shipping_street: Optional[str] = None,
        phone: Optional[str] = None,
        fax: Optional[str] = None,
        website: Optional[str] = None,
        industry: Optional[str] = None,
        annual_revenue: Optional[float] = None,
        number_of_employees: Optional[int] = None,
        description: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an Account.

        Args:
            name: Account name
            type: Account type
            billing_city: Billing city
            billing_country: Billing country
            billing_postal_code: Billing postal code
            billing_state: Billing state
            billing_street: Billing street
            billing_latitude: Billing latitude
            billing_longitude: Billing longitude
            shipping_city: Shipping city
            shipping_country: Shipping country
            shipping_postal_code: Shipping postal code
            shipping_state: Shipping state
            shipping_street: Shipping street
            phone: Phone number
            fax: Fax number
            website: Website URL
            industry: Industry
            annual_revenue: Annual revenue
            number_of_employees: Number of employees
            description: Description
            custom_fields: Custom field values

        Returns:
            Created account with ID
        """
        data = {"Name": name, "Type": type}

        if billing_city:
            data["BillingCity"] = billing_city
        if billing_country:
            data["BillingCountry"] = billing_country
        if billing_postal_code:
            data["BillingPostalCode"] = billing_postal_code
        if billing_state:
            data["BillingState"] = billing_state
        if billing_street:
            data["BillingStreet"] = billing_street
        if billing_latitude is not None:
            data["BillingLatitude"] = billing_latitude
        if billing_longitude is not None:
            data["BillingLongitude"] = billing_longitude

        if shipping_city:
            data["ShippingCity"] = shipping_city
        if shipping_country:
            data["ShippingCountry"] = shipping_country
        if shipping_postal_code:
            data["ShippingPostalCode"] = shipping_postal_code
        if shipping_state:
            data["ShippingState"] = shipping_state
        if shipping_street:
            data["ShippingStreet"] = shipping_street

        if phone:
            data["Phone"] = phone
        if fax:
            data["Fax"] = fax
        if website:
            data["Website"] = website
        if industry:
            data["Industry"] = industry
        if annual_revenue is not None:
            data["AnnualRevenue"] = annual_revenue
        if number_of_employees is not None:
            data["NumberOfEmployees"] = number_of_employees
        if description:
            data["Description"] = description

        if custom_fields:
            data.update(custom_fields)

        return self.create_object("Account", data)

    def create_contact(
        self,
        first_name: str,
        last_name: str,
        account_id: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        mobile_phone: Optional[str] = None,
        title: Optional[str] = None,
        department: Optional[str] = None,
        mailing_city: Optional[str] = None,
        mailing_country: Optional[str] = None,
        mailing_postal_code: Optional[str] = None,
        mailing_state: Optional[str] = None,
        mailing_street: Optional[str] = None,
        mailing_latitude: Optional[float] = None,
        mailing_longitude: Optional[float] = None,
        lead_source: Optional[str] = None,
        description: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a Contact.

        Args:
            first_name: First name
            last_name: Last name
            account_id: Associated account ID
            email: Email address
            phone: Phone number
            mobile_phone: Mobile phone number
            title: Job title
            department: Department
            mailing_city: Mailing city
            mailing_country: Mailing country
            mailing_postal_code: Mailing postal code
            mailing_state: Mailing state
            mailing_street: Mailing street
            mailing_latitude: Mailing latitude
            mailing_longitude: Mailing longitude
            lead_source: Lead source
            description: Description
            custom_fields: Custom field values

        Returns:
            Created contact with ID
        """
        data = {"FirstName": first_name, "LastName": last_name}

        if account_id:
            data["AccountId"] = account_id
        if email:
            data["Email"] = email
        if phone:
            data["Phone"] = phone
        if mobile_phone:
            data["MobilePhone"] = mobile_phone
        if title:
            data["Title"] = title
        if department:
            data["Department"] = department

        if mailing_city:
            data["MailingCity"] = mailing_city
        if mailing_country:
            data["MailingCountry"] = mailing_country
        if mailing_postal_code:
            data["MailingPostalCode"] = mailing_postal_code
        if mailing_state:
            data["MailingState"] = mailing_state
        if mailing_street:
            data["MailingStreet"] = mailing_street
        if mailing_latitude is not None:
            data["MailingLatitude"] = mailing_latitude
        if mailing_longitude is not None:
            data["MailingLongitude"] = mailing_longitude

        if lead_source:
            data["LeadSource"] = lead_source
        if description:
            data["Description"] = description

        if custom_fields:
            data.update(custom_fields)

        return self.create_object("Contact", data)

    def create_opportunity(
        self,
        name: str,
        stage_name: str,
        account_id: Optional[str] = None,
        close_date: Optional[str] = None,
        amount: Optional[float] = None,
        type: str = "New Customer",
        probability: Optional[int] = None,
        expected_revenue: Optional[float] = None,
        lead_source: Optional[str] = None,
        next_step: Optional[str] = None,
        description: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an Opportunity.

        Args:
            name: Opportunity name
            stage_name: Opportunity stage name
            account_id: Associated account ID
            close_date: Expected close date (YYYY-MM-DD)
            amount: Opportunity amount
            type: Opportunity type
            probability: Probability percentage (0-100)
            expected_revenue: Expected revenue
            lead_source: Lead source
            next_step: Next step
            description: Description
            custom_fields: Custom field values

        Returns:
            Created opportunity with ID
        """
        data = {
            "Name": name,
            "StageName": stage_name,
            "Type": type
        }

        if account_id:
            data["AccountId"] = account_id
        if close_date:
            data["CloseDate"] = close_date
        if amount is not None:
            data["Amount"] = amount
        if probability is not None:
            data["Probability"] = probability
        if expected_revenue is not None:
            data["ExpectedRevenue"] = expected_revenue
        if lead_source:
            data["LeadSource"] = lead_source
        if next_step:
            data["NextStep"] = next_step
        if description:
            data["Description"] = description

        if custom_fields:
            data.update(custom_fields)

        return self.create_object("Opportunity", data)

    def create_lead(
        self,
        first_name: str,
        last_name: str,
        company: str,
        owner_id: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        mobile_phone: Optional[str] = None,
        title: Optional[str] = None,
        industry: Optional[str] = None,
        annual_revenue: Optional[float] = None,
        description: Optional[str] = None,
        status: str = "Open",
        lead_source: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a Lead.

        Args:
            first_name: First name
            last_name: Last name
            company: Company name
            owner_id: Owner user ID
            email: Email address
            phone: Phone number
            mobile_phone: Mobile phone number
            title: Job title
            industry: Industry
            annual_revenue: Annual revenue
            description: Description
            status: Lead status
            lead_source: Lead source
            custom_fields: Custom field values

        Returns:
            Created lead with ID
        """
        data = {
            "FirstName": first_name,
            "LastName": last_name,
            "Company": company,
            "Status": status
        }

        if owner_id:
            data["OwnerId"] = owner_id
        if email:
            data["Email"] = email
        if phone:
            data["Phone"] = phone
        if mobile_phone:
            data["MobilePhone"] = mobile_phone
        if title:
            data["Title"] = title
        if industry:
            data["Industry"] = industry
        if annual_revenue is not None:
            data["AnnualRevenue"] = annual_revenue
        if description:
            data["Description"] = description
        if lead_source:
            data["LeadSource"] = lead_source

        if custom_fields:
            data.update(custom_fields)

        return self.create_object("Lead", data)

    def convert_lead(
        self,
        lead_id: str,
        account_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        opportunity_name: Optional[str] = None,
        converted_status: str = "Converted",
        do_not_create_opportunity: bool = False
    ) -> Dict[str, Any]:
        """
        Convert a lead to an account/contact/opportunity.

        Args:
            lead_id: Lead ID to convert
            account_id: Account ID (if using existing)
            contact_id: Contact ID (if using existing)
            opportunity_name: Name for opportunity
            converted_status: Converted status
            do_not_create_opportunity: Skip opportunity creation

        Returns:
            Conversion result with new IDs
        """
        data = {
            "leadId": lead_id,
            "convertedStatus": converted_status,
            "doNotCreateOpportunity": do_not_create_opportunity
        }

        if account_id:
            data["accountId"] = account_id
        if contact_id:
            data["contactId"] = contact_id
        if opportunity_name:
            data["opportunityName"] = opportunity_name

        endpoint = f"/composite/leadConverts"
        return self._make_request("POST", endpoint, json={"leadConverts": [data]})

    def create_task(
        self,
        subject: str,
        owner_id: Optional[str] = None,
        what_id: Optional[str] = None,
        who_id: Optional[str] = None,
        status: str = "Not Started",
        priority: str = "Normal",
        activity_date: Optional[str] = None,
        description: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a Task.

        Args:
            subject: Task subject
            owner_id: Owner user ID
            what_id: Related what ID (account, opportunity, etc.)
            who_id: Related who ID (contact, lead)
            status: Task status
            priority: Task priority
            activity_date: Activity date (YYYY-MM-DD)
            description: Description
            custom_fields: Custom field values

        Returns:
            Created task with ID
        """
        data = {
            "Subject": subject,
            "Status": status,
            "Priority": priority
        }

        if owner_id:
            data["OwnerId"] = owner_id
        if what_id:
            data["WhatId"] = what_id
        if who_id:
            data["WhoId"] = who_id
        if activity_date:
            data["ActivityDate"] = activity_date
        if description:
            data["Description"] = description

        if custom_fields:
            data.update(custom_fields)

        return self.create_object("Task", data)

    def create_event(
        self,
        subject: str,
        start_datetime: str,
        end_datetime: str,
        owner_id: Optional[str] = None,
        what_id: Optional[str] = None,
        who_id: Optional[str] = None,
        location: Optional[str] = None,
        description: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an Event.

        Args:
            subject: Event subject
            start_datetime: Start datetime (ISO 8601 format)
            end_datetime: End datetime (ISO 8601 format)
            owner_id: Owner user ID
            what_id: Related what ID
            who_id: Related who ID
            location: Location
            description: Description
            custom_fields: Custom field values

        Returns:
            Created event with ID
        """
        data = {
            "Subject": subject,
            "StartDateTime": start_datetime,
            "EndDateTime": end_datetime
        }

        if owner_id:
            data["OwnerId"] = owner_id
        if what_id:
            data["WhatId"] = what_id
        if who_id:
            data["WhoId"] = who_id
        if location:
            data["Location"] = location
        if description:
            data["Description"] = description

        if custom_fields:
            data.update(custom_fields)

        return self.create_object("Event", data)

    def search(
        self,
        search_string: str
    ) -> Dict[str, Any]:
        """
        SOSL search query.

        Args:
            search_string: SOSL search string

        Returns:
            Search results
        """
        endpoint = f"/search?q={search_string}"
        return self._make_request("GET", endpoint)

    def describe_object(self, object_type: str) -> Dict[str, Any]:
        """
        Get object metadata.

        Args:
            object_type: Salesforce object type

        Returns:
            Object metadata including fields, relationships, etc.
        """
        endpoint = f"/sobjects/{object_type}/describe"
        return self._make_request("GET", endpoint)

    def get_limits(self) -> Dict[str, Any]:
        """
        Get organization limits.

        Returns:
            Current organization limits information
        """
        endpoint = "/limits"
        return self._make_request("GET", endpoint)

    def create_case(
        self,
        subject: str,
        owner_id: Optional[str] = None,
        account_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        priority: str = "Medium",
        status: str = "New",
        origin: str = "Phone",
        description: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a Case.

        Args:
            subject: Case subject
            owner_id: Owner user ID
            account_id: Account ID
            contact_id: Contact ID
            priority: Priority
            status: Status
            origin: Origin
            description: Description
            custom_fields: Custom field values

        Returns:
            Created case with ID
        """
        data = {
            "Subject": subject,
            "Priority": priority,
            "Status": status,
            "Origin": origin
        }

        if owner_id:
            data["OwnerId"] = owner_id
        if account_id:
            data["AccountId"] = account_id
        if contact_id:
            data["ContactId"] = contact_id
        if description:
            data["Description"] = description

        if custom_fields:
            data.update(custom_fields)

        return self.create_object("Case", data)

    def bulk_insert(
        self,
        object_type: str,
        records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Bulk insert records using Bulk API.

        Args:
            object_type: Salesforce object type
            records: List of record data to insert

        Returns:
            Bulk job information
        """
        endpoint = f"/jobs/ingest"
        data = {
            "object": object_type,
            "contentType": "JSON",
            "operation": "insert"
        }
        job_response = self._make_request("POST", endpoint, json=data)
        job_id = job_response.get('data', {}).get('id')

        # Upload data
        upload_endpoint = f"/jobs/ingest/{job_id}/batches"
        import json as json_module
        csv_data = "\n".join([json_module.dumps(record) for record in records])
        self._make_request("PUT", upload_endpoint, data=csv_data, headers={"Content-Type": "text/csv"})

        # Close job
        close_endpoint = f"/jobs/ingest/{job_id}"
        return self._make_request("PATCH", close_endpoint, json={"state": "UploadComplete"})

    def chatter_post(
        self,
        user_id: str,
        text: str
    ) -> Dict[str, Any]:
        """
        Post to Chatter feed.

        Args:
            user_id: User ID for feed
            text: Post text

        Returns:
            Posted feed item
        """
        endpoint = f"/chatter/feed-elements"
        data = {
            "body": {
                "messageSegments": [
                    {
                        "type": "Text",
                        "text": text
                    }
                ]
            },
            "feedElementType": "FeedItem",
            "subjectId": user_id
        }
        return self._make_request("POST", endpoint, json=data)
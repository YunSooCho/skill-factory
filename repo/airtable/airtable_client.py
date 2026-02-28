"""
Airtable API Client

Airtable is a low-code database platform for building relational databases.

API Actions (9):
1. Create Record
2. List Records
3. Create Comment
4. Search Records
5. Delete Record
6. Get Record
7. Attach File to Record
8. Update Record
9. Download Record File

Triggers (2):
- Record Updated
- Record Created

Authentication: Personal Access Token (Bearer) or OAuth
Base URL: https://api.airtable.com/v0
Documentation: https://airtable.com/developers/web/api
Rate Limiting: 5 requests per second per base
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List, BinaryIO
from dataclasses import dataclass, field


@dataclass
class AirtableRecord:
    """Airtable record model"""
    id: str
    created_time: str
    fields: Dict[str, Any]

    def __post_init__(self):
        """Ensure fields is always a dict"""
        if self.fields is None:
            self.fields = {}


@dataclass
class Attachment:
    """Attachment model"""
    url: str
    filename: Optional[str] = None
    size: Optional[int] = None
    type: Optional[str] = None
    id: Optional[str] = None


@dataclass
class Comment:
    """Comment model"""
    id: str
    text: str
    created_time: str
    last_modified_time: Optional[str] = None
    author_id: Optional[str] = None
    mentioned_ids: List[str] = field(default_factory=list)


@dataclass
class AirtableError:
    """Error response model"""
    type: str
    message: str


@dataclass
class QueryOptions:
    """Query options"""
    filter_by_formula: Optional[str] = None
    sort: Optional[List[Dict[str, Any]]] = None
    view: Optional[str] = None
    max_records: Optional[int] = None
    page_size: Optional[int] = None
    offset: Optional[str] = None
    cell_format: str = "json"
    time_zone: str = "utc"
    user_locale: str = "en"


class AirtableClient:
    """
    Airtable API client for database operations.

    Supports: Records, Comments, Attachments
    Rate limit: 5 requests/second per base
    """

    BASE_URL = "https://api.airtable.com/v0"
    RATE_LIMIT = 5  # requests per second

    def __init__(self, access_token: str, base_id: str):
        """
        Initialize Airtable client.

        Args:
            access_token: Personal access token or OAuth token
            base_id: Base ID (can be found in Airtable API documentation)
        """
        self.access_token = access_token
        self.base_id = base_id
        self.session = None
        self._last_request_time = datetime.now()
        self._headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _check_rate_limit(self):
        """Check and enforce rate limiting"""
        now = datetime.now()
        time_since_last = (now - self._last_request_time).total_seconds()

        if time_since_last < (1.0 / self.RATE_LIMIT):
            wait_time = (1.0 / self.RATE_LIMIT) - time_since_last
            await asyncio.sleep(wait_time)

        self._last_request_time = datetime.now()

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make API request with rate limiting.

        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            headers: Additional headers

        Returns:
            Response JSON

        Raises:
            Exception: If request fails
        """
        await self._check_rate_limit()

        url = f"{self.BASE_URL}{endpoint}"
        request_headers = self._headers.copy()
        if headers:
            request_headers.update(headers)

        async with self.session.request(
            method,
            url,
            headers=request_headers,
            json=data,
            params=params
        ) as response:
            try:
                result = await response.json()
            except:
                result = {}

            if response.status not in [200, 201]:
                error = result.get("error", {})
                raise Exception(
                    f"Airtable API error: {response.status} - {error.get('message', 'Unknown error')}"
                )

            return result

    # ==================== Record Operations ====================

    async def create_record(
        self,
        table_name: str,
        fields: Dict[str, Any],
        typecast: bool = False
    ) -> AirtableRecord:
        """
        Create a new record.

        Args:
            table_name: Table name or ID
            fields: Field values for the new record
            typecast: Whether to automatically convert data types

        Returns:
            Created AirtableRecord object

        Raises:
            Exception: If creation fails
        """
        data = {
            "fields": fields
        }

        if typecast:
            data["typecast"] = True

        response = await self._make_request(
            "POST",
            f"/{self.base_id}/{table_name}",
            data=data
        )

        return AirtableRecord(**response)

    async def get_record(
        self,
        table_name: str,
        record_id: str
    ) -> AirtableRecord:
        """
        Get a specific record.

        Args:
            table_name: Table name or ID
            record_id: Record ID

        Returns:
            AirtableRecord object

        Raises:
            Exception: If retrieval fails
        """
        response = await self._make_request(
            "GET",
            f"/{self.base_id}/{table_name}/{record_id}"
        )
        return AirtableRecord(**response)

    async def update_record(
        self,
        table_name: str,
        record_id: str,
        fields: Dict[str, Any],
        typecast: bool = False
    ) -> AirtableRecord:
        """
        Update a record.

        Args:
            table_name: Table name or ID
            record_id: Record ID
            fields: Fields to update
            typecast: Whether to automatically convert data types

        Returns:
            Updated AirtableRecord object

        Raises:
            Exception: If update fails
        """
        data = {
            "fields": fields
        }

        if typecast:
            data["typecast"] = True

        response = await self._make_request(
            "PATCH",
            f"/{self.base_id}/{table_name}/{record_id}",
            data=data
        )

        return AirtableRecord(**response)

    async def delete_record(
        self,
        table_name: str,
        record_id: str
    ) -> Dict[str, str]:
        """
        Delete a record.

        Args:
            table_name: Table name or ID
            record_id: Record ID

        Returns:
            Dictionary with deleted record ID

        Raises:
            Exception: If deletion fails
        """
        response = await self._make_request(
            "DELETE",
            f"/{self.base_id}/{table_name}/{record_id}"
        )
        return response

    async def list_records(
        self,
        table_name: str,
        offset: Optional[str] = None,
        limit: Optional[int] = None,
        # Additional query parameters
        filter_by_formula: Optional[str] = None,
        sort: Optional[List[Dict[str, str]]] = None,
        view: Optional[str] = None,
        fields: Optional[List[str]] = None,
        max_records: Optional[int] = None,
        page_size: Optional[int] = None,
        cell_format: str = "json",
        time_zone: str = "utc",
        user_locale: str = "en"
    ) -> List[AirtableRecord]:
        """
        List records from a table.

        Args:
            table_name: Table name or ID
            offset: Page offset for pagination
            limit: Maximum number of records to return
            filter_by_formula: Formula to filter records
            sort: Sorting specification
            view: View name or ID
            fields: Specific fields to return
            max_records: Maximum records per request
            page_size: Page size
            cell_format: Output format
            time_zone: Timezone string
            user_locale: User locale

        Returns:
            List of AirtableRecord objects

        Raises:
            Exception: If retrieval fails
        """
        params = {}

        if offset:
            params["offset"] = offset
        if filter_by_formula:
            params["filterByFormula"] = filter_by_formula
        if sort:
            params["sort"] = sort
        if view:
            params["view"] = view
        if fields:
            params["fields"] = fields
        if max_records:
            params["maxRecords"] = max_records
        if page_size:
            params["pageSize"] = page_size
        if cell_format:
            params["cellFormat"] = cell_format
        if time_zone:
            params["timeZone"] = time_zone
        if user_locale:
            params["userLocale"] = user_locale

        response = await self._make_request(
            "GET",
            f"/{self.base_id}/{table_name}",
            params=params
        )

        records = response.get("records", [])

        if limit and len(records) > limit:
            records = records[:limit]

        return [AirtableRecord(**r) for r in records]

    async def search_records(
        self,
        table_name: str,
        field_name: str,
        search_value: str,
        operator: str = "=",
        limit: int = 10
    ) -> List[AirtableRecord]:
        """
        Search records by field value.

        Args:
            table_name: Table name or ID
            field_name: Field to search in
            search_value: Value to search for
            operator: Comparison operator (=, !=, >, <, >=, <=, CONTAINS, etc.)
            limit: Maximum results

        Returns:
            List of matching AirtableRecord objects

        Raises:
            Exception: If search fails
        """
        formula = f"{{{{{{{field_name}}} {operator} '{search_value}'}}}}"

        records = await self.list_records(
            table_name=table_name,
            filter_by_formula=formula,
            limit=limit
        )

        return records[:limit]

    async def attach_file_to_record(
        self,
        table_name: str,
        record_id: str,
        field_name: str,
        file_url: str,
        filename: Optional[str] = None
    ) -> AirtableRecord:
        """
        Attach a file to a record.

        Args:
            table_name: Table name or ID
            record_id: Record ID
            field_name: Attachment field name
            file_url: URL of the file to attach
            filename: Optional filename for the attachment

        Returns:
            Updated AirtableRecord object

        Raises:
            Exception: If attachment fails
        """
        # Get current record
        record = await self.get_record(table_name, record_id)

        # Get existing attachments
        existing_attachments = record.fields.get(field_name, [])
        if not isinstance(existing_attachments, list):
            existing_attachments = []

        # Add new attachment
        new_attachment = {"url": file_url}
        if filename:
            new_attachment["filename"] = filename

        existing_attachments.append(new_attachment)

        # Update record
        return await self.update_record(
            table_name,
            record_id,
            {field_name: existing_attachments}
        )

    async def download_record_file(
        self,
        table_name: str,
        record_id: str,
        field_name: str,
        attachment_index: int = 0
    ) -> bytes:
        """
        Download a file from a record's attachment field.

        Args:
            table_name: Table name or ID
            record_id: Record ID
            field_name: Attachment field name
            attachment_index: Index of attachment if multiple

        Returns:
            File content as bytes

        Raises:
            Exception: If download fails
        """
        record = await self.get_record(table_name, record_id)
        attachments = record.fields.get(field_name, [])

        if not isinstance(attachments, list) or len(attachments) == 0:
            raise Exception(f"No attachments found in field '{field_name}'")

        if attachment_index >= len(attachments):
            raise Exception(f"Attachment index {attachment_index} out of range")

        attachment_url = attachments[attachment_index].get("url")

        if not attachment_url:
            raise Exception("Attachment URL not found")

        # Download file
        async with self.session.get(attachment_url) as response:
            if response.status != 200:
                raise Exception(f"Failed to download file: {response.status}")
            return await response.read()

    # ==================== Comment Operations ====================

    async def create_comment(
        self,
        table_name: str,
        record_id: str,
        text: str
    ) -> Comment:
        """
        Create a comment on a record.

        Args:
            table_name: Table name or ID
            record_id: Record ID
            text: Comment text

        Returns:
            Created Comment object

        Raises:
            Exception: If creation fails
        """
        data = {
            "text": text
        }

        response = await self._make_request(
            "POST",
            f"/{self.base_id}/{table_name}/{record_id}/comments",
            data=data
        )
        return Comment(**response)

    # ==================== Webhook Handling ====================

    def handle_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle webhook events from Airtable.

        Args:
            webhook_data: Webhook payload

        Returns:
            Processed event data

        Supported triggers:
        - Record Updated
        - Record Created
        """
        event_type = webhook_data.get("type", "unknown")
        base_id = webhook_data.get("base", {}).get("id")
        table_id = webhook_data.get("table", {}).get("id")
        record_id = webhook_data.get("record", {}).get("id")

        return {
            "event_type": event_type,
            "base_id": base_id,
            "table_id": table_id,
            "record_id": record_id,
            "raw_data": webhook_data
        }


# ==================== Example Usage ====================

async def main():
    """Example usage of Airtable client"""

    # Replace with your actual credentials
    access_token = "your_airtable_access_token"
    base_id = "appXXXXXXXXXXXXXX"  # Your base ID
    table_name = "Contacts"  # Your table name

    async with AirtableClient(access_token, base_id) as client:
        # Create a record
        new_record = await client.create_record(
            table_name=table_name,
            fields={
                "Name": "John Doe",
                "Email": "john.doe@example.com",
                "Status": "Active"
            }
        )
        print(f"Created record: {new_record.id}")

        # Get the record
        record = await client.get_record(table_name, new_record.id)
        print(f"Record fields: {record.fields}")

        # Search records
        results = await client.search_records(
            table_name=table_name,
            field_name="Name",
            search_value="John",
            operator="CONTAINS",
            limit=5
        )
        print(f"Found {len(results)} matching records")

        # List records
        all_records = await client.list_records(table_name=table_name, limit=10)
        print(f"Total records: {len(all_records)}")


if __name__ == "__main__":
    asyncio.run(main())
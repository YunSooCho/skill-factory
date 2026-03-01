"""
 Zoho Sheet API Client
"""

import time
import requests
from typing import Optional, Dict, List, Any, Union
from urllib.parse import urljoin

from .models import (
    Workbook,
    Worksheet,
    Cell,
    Record,
    WorkbookListResponse,
    WorksheetListResponse,
    RecordListResponse,
)
from .exceptions import (
    ZohoSheetError,
    RateLimitError,
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
)


class ZohoSheetClient:
    """Zoho Sheet API Client (V3)"""

    BASE_URL = "https://sheet.zoho.com/api/v3/"
    UPLOAD_URL = "https://sheet.zoho.com/api/v1/"

    def __init__(
        self,
        auth_token: str,
        organization_id: Optional[str] = None,
        timeout: int = 30,
    ):
        """
        Initialize Zoho Sheet client

        Args:
            auth_token: Zoho authentication token
            organization_id: Organization ID (optional, for enterprise)
            timeout: Request timeout in seconds
        """
        self.auth_token = auth_token
        self.organization_id = organization_id
        self.timeout = timeout
        self.session = requests.Session()

        # Rate limiting
        self._last_request_time = 0
        self._min_request_interval = 0.1  # 100ms between requests
        self._rate_limit_remaining = 1000
        self._rate_limit_reset = time.time() + 3600

    def _wait_for_rate_limit(self):
        """Apply rate limiting to requests"""
        now = time.time()
        time_since_last = now - self._last_request_time

        if time_since_last < self._min_request_interval:
            sleep_time = self._min_request_interval - time_since_last
            time.sleep(sleep_time)

        self._last_request_time = time.time()

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        use_upload_endpoint: bool = False,
    ) -> Union[Dict, List]:
        """
        Make API request with error handling and rate limiting

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: URL query parameters
            data: Form data
            json_data: JSON body data
            use_upload_endpoint: Use upload endpoint instead

        Returns:
            JSON response data

        Raises:
            ZohoSheetError: General API error
            RateLimitError: Rate limit exceeded
            AuthenticationError: Authentication failed
            ResourceNotFoundError: Resource not found
            ValidationError: Validation error
        """
        self._wait_for_rate_limit()

        base_url = self.UPLOAD_URL if use_upload_endpoint else self.BASE_URL
        url = urljoin(base_url, endpoint)

        # Zoho auth token in query params
        if params is None:
            params = {}
        params["authtoken"] = self.auth_token

        if self.organization_id:
            params["organization_id"] = self.organization_id

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json_data,
                timeout=self.timeout,
            )

            # Update rate limit info from headers
            self._update_rate_limit(response.headers)

            return self._handle_response(response)

        except requests.exceptions.Timeout:
            raise ZohoSheetError(f"Request timeout after {self.timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise ZohoSheetError(f"Request failed: {str(e)}")

    def _update_rate_limit(self, headers: Dict):
        """Update rate limit information from response headers"""
        if "X-RateLimit-Remaining" in headers:
            self._rate_limit_remaining = int(headers["X-RateLimit-Remaining"])
        if "X-RateLimit-Reset" in headers:
            self._rate_limit_reset = int(headers["X-RateLimit-Reset"])

    def _handle_response(self, response: requests.Response) -> Union[Dict, List]]:
        """
        Handle API response and raise appropriate exceptions

        Args:
            response: HTTP response object

        Returns:
            JSON response data

        Raises:
            ZohoSheetError: General API error
            RateLimitError: Rate limit exceeded
            AuthenticationError: Authentication failed
            ResourceNotFoundError: Resource not found
            ValidationError: Validation error
        """
        try:
            response_text = response.text
            if response_text:
                data = response.json()
            else:
                data = {}
        except ValueError:
            return {"raw": response_text}

        # Zoho API error handling
        if isinstance(data, dict):
            if "error" in data:
                error_code = data.get("error", {}).get("code", "")
                error_message = data.get("error", {}).get("message", "Unknown error")

                if error_code in ["AUTHENTICATION_FAILURE", "INVALID_TOKEN"]:
                    raise AuthenticationError(error_message, response=data)
                elif error_code == "NOT_FOUND":
                    raise ResourceNotFoundError(error_message, response=data)
                else:
                    raise ZohoSheetError(error_message, response=data)

        if response.status_code >= 200 and response.status_code < 300:
            return data
        elif response.status_code == 400:
            error_message = self._extract_error_message(data)
            raise ValidationError(error_message, response=data)
        elif response.status_code == 401:
            error_message = self._extract_error_message(data)
            raise AuthenticationError(error_message, response=data)
        elif response.status_code == 403:
            error_message = self._extract_error_message(data)
            raise AuthenticationError(error_message, response=data)
        elif response.status_code == 404:
            error_message = self._extract_error_message(data)
            raise ResourceNotFoundError(error_message, response=data)
        elif response.status_code == 422:
            error_message = self._extract_error_message(data)
            raise ValidationError(error_message, response=data)
        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            error_message = self._extract_error_message(data)
            raise RateLimitError(error_message, retry_after=retry_after, response=data)
        else:
            error_message = self._extract_error_message(data)
            raise ZohoSheetError(
                error_message or f"HTTP {response.status_code}",
                status_code=response.status_code,
                response=data,
            )

    def _extract_error_message(self, data: Union[Dict, List]) -> str:
        """Extract error message from response data"""
        if isinstance(data, dict):
            return (
                data.get("message")
                or data.get("error_message")
                or data.get("error", {}).get("message", "")
                or str(data)
            )
        return str(data)

    # ==================== WORKBOOK ACTIONS ====================

    def create_workbook(
        self,
        name: str,
        folder_id: Optional[str] = None,
        language: str = "en",
    ) -> Workbook:
        """
        Create a new workbook (3)

        Args:
            name: Workbook name (required)
            folder_id: Folder ID to create workbook in (optional)
            language: Language code (default 'en')

        Returns:
            Created Workbook

        Raises:
            ZohoSheetError: If the request fails
            ValidationError: If validation fails
        """
        if not name:
            raise ValidationError("name is required")

        params = {"workbook_name": name, "language": language}
        if folder_id:
            params["folder_id"] = folder_id

        data = self._make_request("PUT", "workbook", params=params)
        return Workbook.from_api_response(data)

    def list_workbooks(self, status: Optional[str] = None) -> WorkbookListResponse:
        """
        List all workbooks (9)

        Args:
            status: Filter by status ('active', 'trashed')

        Returns:
            WorkbookListResponse with workbook list

        Raises:
            ZohoSheetError: If the request fails
        """
        params = {}
        if status:
            params["status"] = status

        data = self._make_request("GET", "workbooks", params=params)
        return WorkbookListResponse.from_api_response(data)

    def get_workbook(self, workbook_id: str) -> Workbook:
        """
        Get a workbook by ID

        Args:
            workbook_id: Workbook ID

        Returns:
            Workbook

        Raises:
            ZohoSheetError: If the request fails
            ResourceNotFoundError: If workbook not found
        """
        if not workbook_id:
            raise ValidationError("workbook_id is required")

        data = self._make_request("GET", f"workbook/{workbook_id}")
        return Workbook.from_api_response(data)

    def delete_workbook(self, workbook_id: str) -> bool:
        """
        Delete a workbook permanently (17)

        Args:
            workbook_id: Workbook ID

        Returns:
            True if deleted

        Raises:
            ZohoSheetError: If the request fails
            ResourceNotFoundError: If workbook not found
        """
        if not workbook_id:
            raise ValidationError("workbook_id is required")

        self._make_request("DELETE", f"workbook/{workbook_id}")
        return True

    def move_to_trash(self, workbook_id: str) -> bool:
        """
        Move workbook to trash (15)

        Args:
            workbook_id: Workbook ID

        Returns:
            True if moved

        Raises:
            ZohoSheetError: If the request fails
            ResourceNotFoundError: If workbook not found
        """
        if not workbook_id:
            raise ValidationError("workbook_id is required")

        self._make_request("PUT", f"workbook/{workbook_id}/trash")
        return True

    def upload_workbook(
        self,
        file_path: str,
        name: Optional[str] = None,
        folder_id: Optional[str] = None,
    ) -> Workbook:
        """
        Upload a workbook from file (21)

        Args:
            file_path: Local file path
            name: Workbook name (optional, defaults to file name)
            folder_id: Folder ID (optional)

        Returns:
            Uploaded Workbook

        Raises:
            ZohoSheetError: If the request fails
            ValidationError: If validation fails
        """
        if not file_path:
            raise ValidationError("file_path is required")

        import os

        if not os.path.exists(file_path):
            raise ValidationError(f"File not found: {file_path}")

        files = {"content": open(file_path, "rb")}
        params = {}

        if name:
            params["workbook_name"] = name
        else:
            params["workbook_name"] = os.path.basename(file_path)

        if folder_id:
            params["folder_id"] = folder_id

        try:
            data = self._make_request("POST", "upload", params=params, use_upload_endpoint=True)
            files["content"].close()
            return Workbook.from_api_response(data)
        except Exception as e:
            files["content"].close()
            raise e

    # ==================== WORKSHEET ACTIONS ====================

    def create_worksheet(
        self,
        workbook_id: str,
        name: str,
        rows: int = 100,
        columns: int = 26,
    ) -> Worksheet:
        """
        Create a new worksheet (18)

        Args:
            workbook_id: Workbook ID
            name: Worksheet name
            rows: Initial row count
            columns: Initial column count

        Returns:
            Created Worksheet

        Raises:
            ZohoSheetError: If the request fails
            ValidationError: If validation fails
        """
        if not workbook_id:
            raise ValidationError("workbook_id is required")
        if not name:
            raise ValidationError("name is required")

        params = {
            "sheet_name": name,
            "rows": rows,
            "columns": columns,
        }

        data = self._make_request(
            "PUT", f"workbook/{workbook_id}/worksheet", params=params
        )
        return Worksheet.from_api_response(data)

    def list_worksheets(self, workbook_id: str) -> WorksheetListResponse:
        """
        List all worksheets in a workbook (12)

        Args:
            workbook_id: Workbook ID

        Returns:
            WorksheetListResponse

        Raises:
            ZohoSheetError: If the request fails
            ResourceNotFoundError: If workbook not found
        """
        if not workbook_id:
            raise ValidationError("workbook_id is required")

        data = self._make_request("GET", f"workbook/{workbook_id}/worksheets")
        return WorksheetListResponse.from_api_response(data)

    def get_worksheet(self, workbook_id: str, worksheet_id: str) -> Worksheet:
        """
        Get a worksheet

        Args:
            workbook_id: Workbook ID
            worksheet_id: Worksheet ID

        Returns:
            Worksheet

        Raises:
            ZohoSheetError: If the request fails
            ResourceNotFoundError: If worksheet not found
        """
        if not workbook_id or not worksheet_id:
            raise ValidationError("workbook_id and worksheet_id are required")

        data = self._make_request("GET", f"workbook/{workbook_id}/worksheet/{worksheet_id}")
        return Worksheet.from_api_response(data)

    def rename_worksheet(
        self,
        workbook_id: str,
        worksheet_id: str,
        new_name: str,
    ) -> Worksheet:
        """
        Rename a worksheet (13)

        Args:
            workbook_id: Workbook ID
            worksheet_id: Worksheet ID
            new_name: New name

        Returns:
            Updated Worksheet

        Raises:
            ZohoSheetError: If the request fails
            ResourceNotFoundError: If worksheet not found
        """
        if not workbook_id or not worksheet_id:
            raise ValidationError("workbook_id and worksheet_id are required")
        if not new_name:
            raise ValidationError("new_name is required")

        params = {"new_sheet_name": new_name}
        data = self._make_request(
            "PUT", f"workbook/{workbook_id}/worksheet/{worksheet_id}/rename", params=params
        )
        return Worksheet.from_api_response(data)

    def delete_worksheet(
        self,
        workbook_id: str,
        worksheet_id: str,
    ) -> bool:
        """
        Delete a worksheet (8)

        Args:
            workbook_id: Workbook ID
            worksheet_id: Worksheet ID

        Returns:
            True if deleted

        Raises:
            ZohoSheetError: If the request fails
            ResourceNotFoundError: If worksheet not found
        """
        if not workbook_id or not worksheet_id:
            raise ValidationError("workbook_id and worksheet_id are required")

        self._make_request(
            "DELETE", f"workbook/{workbook_id}/worksheet/{worksheet_id}"
        )
        return True

    # ==================== CELL ACTIONS ====================

    def get_cell(
        self,
        workbook_id: str,
        worksheet_id: str,
        row_index: int,
        column_index: int,
    ) -> Cell:
        """
        Get cell information (14)

        Args:
            workbook_id: Workbook ID
            worksheet_id: Worksheet ID
            row_index: Row index (1-based)
            column_index: Column index (1-based)

        Returns:
            Cell

        Raises:
            ZohoSheetError: If the request fails
            ValidationError: If validation fails
        """
        if row_index < 1 or column_index < 1:
            raise ValidationError("row_index and column_index must be >= 1")

        params = {
            "row": row_index,
            "column": column_index,
        }

        data = self._make_request(
            "GET", f"workbook/{workbook_id}/worksheet/{worksheet_id}/cell", params=params
        )
        return Cell.from_api_response(data)

    def get_cell_range(
        self,
        workbook_id: str,
        worksheet_id: str,
        start_row: int,
        start_column: int,
        end_row: int,
        end_column: int,
    ) -> Dict[str, Any]:
        """
        Get range of cell information (1)

        Args:
            workbook_id: Workbook ID
            worksheet_id: Worksheet ID
            start_row: Start row index (1-based)
            start_column: Start column index (1-based)
            end_row: End row index (1-based)
            end_column: End column index (1-based)

        Returns:
            Dictionary with cell range data

        Raises:
            ZohoSheetError: If the request fails
            ValidationError: If validation fails
        """
        if not all([start_row, start_column, end_row, end_column]):
            raise ValidationError("All range indices must be provided")
        if start_row < 1 or start_column < 1 or end_row < 1 or end_column < 1:
            raise ValidationError("All range indices must be >= 1")

        params = {
            "start_row": start_row,
            "start_column": start_column,
            "end_row": end_row,
            "end_column": end_column,
        }

        data = self._make_request(
            "GET",
            f"workbook/{workbook_id}/worksheet/{worksheet_id}/cell/range",
            params=params,
        )
        return data

    def update_cell(
        self,
        workbook_id: str,
        worksheet_id: str,
        row_index: int,
        column_index: int,
        value: Any,
        formula: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update a cell (19)

        Args:
            workbook_id: Workbook ID
            worksheet_id: Worksheet ID
            row_index: Row index (1-based)
            column_index: Column index (1-based)
            value: Cell value
            formula: Cell formula (optional, takes precedence over value)

        Returns:
            Updated cell data

        Raises:
            ZohoSheetError: If the request fails
            ValidationError: If validation fails
        """
        if row_index < 1 or column_index < 1:
            raise ValidationError("row_index and column_index must be >= 1")

        params = {
            "row": row_index,
            "column": column_index,
        }

        json_data = {"data": value}
        if formula:
            json_data["formula"] = formula

        data = self._make_request(
            "POST", f"workbook/{workbook_id}/worksheet/{worksheet_id}/cell", params=params, json_data=json_data
        )
        return data

    def update_cells(
        self,
        workbook_id: str,
        worksheet_id: str,
        cells: List[Dict],
    ) -> Dict[str, Any]:
        """
        Update multiple cells

        Args:
            workbook_id: Workbook ID
            worksheet_id: Worksheet ID
            cells: List of cell dicts with 'row', 'column', 'value'/'formula'

        Returns:
            Update result

        Raises:
            ZohoSheetError: If the request fails
            ValidationError: If validation fails
        """
        if not cells:
            raise ValidationError("cells list cannot be empty")

        json_data = {"updates": cells}

        data = self._make_request(
            "POST",
            f"workbook/{workbook_id}/worksheet/{worksheet_id}/cells",
            json_data=json_data,
        )
        return data

    # ==================== ROW ACTIONS ====================

    def insert_row(
        self,
        workbook_id: str,
        worksheet_id: str,
        row_index: int,
        count: int = 1,
    ) -> Dict[str, Any]:
        """
        Insert rows (4)

        Args:
            workbook_id: Workbook ID
            worksheet_id: Worksheet ID
            row_index: Row index to insert at (1-based)
            count: Number of rows to insert

        Returns:
            Result data

        Raises:
            ZohoSheetError: If the request fails
            ValidationError: If validation fails
        """
        if row_index < 1:
            raise ValidationError("row_index must be >= 1")
        if count < 1:
            raise ValidationError("count must be >= 1")

        params = {
            "row": row_index,
            "count": count,
        }

        data = self._make_request(
            "PUT",
            f"workbook/{workbook_id}/worksheet/{worksheet_id}/row",
            params=params,
        )
        return data

    def delete_row(
        self,
        workbook_id: str,
        worksheet_id: str,
        row_index: int,
        count: int = 1,
    ) -> Dict[str, Any]:
        """
        Delete rows (6)

        Args:
            workbook_id: Workbook ID
            worksheet_id: Worksheet ID
            row_index: Row index to delete from (1-based)
            count: Number of rows to delete

        Returns:
            Result data

        Raises:
            ZohoSheetError: If the request fails
            ValidationError: If validation fails
        """
        if row_index < 1:
            raise ValidationError("row_index must be >= 1")
        if count < 1:
            raise ValidationError("count must be >= 1")

        params = {
            "row": row_index,
            "count": count,
        }

        data = self._make_request(
            "DELETE",
            f"workbook/{workbook_id}/worksheet/{worksheet_id}/row",
            params=params,
        )
        return data

    # ==================== COLUMN ACTIONS ====================

    def insert_column(
        self,
        workbook_id: str,
        worksheet_id: str,
        column_index: int,
        count: int = 1,
    ) -> Dict[str, Any]:
        """
        Insert columns (22)

        Args:
            workbook_id: Workbook ID
            worksheet_id: Worksheet ID
            column_index: Column index to insert at (1-based)
            count: Number of columns to insert

        Returns:
            Result data

        Raises:
            ZohoSheetError: If the request fails
            ValidationError: If validation fails
        """
        if column_index < 1:
            raise ValidationError("column_index must be >= 1")
        if count < 1:
            raise ValidationError("count must be >= 1")

        params = {
            "column": column_index,
            "count": count,
        }

        data = self._make_request(
            "PUT",
            f"workbook/{workbook_id}/worksheet/{worksheet_id}/column",
            params=params,
        )
        return data

    def delete_column(
        self,
        workbook_id: str,
        worksheet_id: str,
        column_index: int,
        count: int = 1,
    ) -> Dict[str, Any]:
        """
        Delete columns (7)

        Args:
            workbook_id: Workbook ID
            worksheet_id: Worksheet ID
            column_index: Column index to delete from (1-based)
            count: Number of columns to delete

        Returns:
            Result data

        Raises:
            ZohoSheetError: If the request fails
            ValidationError: If validation fails
        """
        if column_index < 1:
            raise ValidationError("column_index must be >= 1")
        if count < 1:
            raise ValidationError("count must be >= 1")

        params = {
            "column": column_index,
            "count": count,
        }

        data = self._make_request(
            "DELETE",
            f"workbook/{workbook_id}/worksheet/{worksheet_id}/column",
            params=params,
        )
        return data

    def update_column(
        self,
        workbook_id: str,
        worksheet_id: str,
        column_index: int,
        values: List[Any],
    ) -> Dict[str, Any]:
        """
        Update a column (20)

        Args:
            workbook_id: Workbook ID
            worksheet_id: Worksheet ID
            column_index: Column index (1-based)
            values: List of values to set in the column

        Returns:
            Result data

        Raises:
            ZohoSheetError: If the request fails
            ValidationError: If validation fails
        """
        if column_index < 1:
            raise ValidationError("column_index must be >= 1")
        if not values:
            raise ValidationError("values cannot be empty")

        params = {"column": column_index}
        json_data = {"values": values}

        data = self._make_request(
            "POST",
            f"workbook/{workbook_id}/worksheet/{worksheet_id}/column",
            params=params,
            json_data=json_data,
        )
        return data

    # ==================== RECORD ACTIONS ====================

    def add_records(
        self,
        workbook_id: str,
        worksheet_id: str,
        records: List[Dict[str, Any]],
        append: bool = True,
    ) -> Dict[str, Any]:
        """
        Add records to worksheet (11)

        Args:
            workbook_id: Workbook ID
            worksheet_id: Worksheet ID
            records: List of record dicts (column_name: value)
            append: Append to end (true) or insert at row 1 (false)

        Returns:
            Result data

        Raises:
            ZohoSheetError: If the request fails
            ValidationError: If validation fails
        """
        if not records:
            raise ValidationError("records cannot be empty")

        json_data = {
            "records": records,
            "append": "row" if append else "column",
        }

        data = self._make_request(
            "POST",
            f"workbook/{workbook_id}/worksheet/{worksheet_id}/records",
            json_data=json_data,
        )
        return data

    def get_records(
        self,
        workbook_id: str,
        worksheet_id: str,
        row_index: Optional[int] = None,
        count: Optional[int] = None,
    ) -> RecordListResponse:
        """
        Get worksheet records (5)

        Args:
            workbook_id: Workbook ID
            worksheet_id: Worksheet ID
            row_index: Starting row index (1-based, optional)
            count: Number of records to fetch (optional)

        Returns:
            RecordListResponse

        Raises:
            ZohoSheetError: If the request fails
            ValidationError: If validation fails
        """
        params = {}

        if row_index is not None:
            if row_index < 1:
                raise ValidationError("row_index must be >= 1")
            params["row"] = row_index
        if count is not None:
            if count < 1:
                raise ValidationError("count must be >= 1")
            params["count"] = count

        data = self._make_request(
            "GET",
            f"workbook/{workbook_id}/worksheet/{worksheet_id}/records",
            params=params,
        )
        return RecordListResponse.from_api_response(data)

    def update_records(
        self,
        workbook_id: str,
        worksheet_id: str,
        updates: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Update worksheet records (16)

        Args:
            workbook_id: Workbook ID
            worksheet_id: Worksheet ID
            updates: List of update dicts with 'row_index' and field values

        Returns:
            Result data

        Raises:
            ZohoSheetError: If the request fails
            ValidationError: If validation fails
        """
        if not updates:
            raise ValidationError("updates cannot be empty")

        json_data = {"updates": updates}

        data = self._make_request(
            "POST",
            f"workbook/{workbook_id}/worksheet/{worksheet_id}/records/update",
            json_data=json_data,
        )
        return data

    def delete_records(
        self,
        workbook_id: str,
        worksheet_id: str,
        row_indices: List[int],
    ) -> Dict[str, Any]:
        """
        Delete worksheet records (10)

        Args:
            workbook_id: Workbook ID
            worksheet_id: Worksheet ID
            row_indices: List of row indices to delete

        Returns:
            Result data

        Raises:
            ZohoSheetError: If the request fails
            ValidationError: If validation fails
        """
        if not row_indices:
            raise ValidationError("row_indices cannot be empty")

        json_data = {"rows": row_indices}

        data = self._make_request(
            "POST",
            f"workbook/{workbook_id}/worksheet/{worksheet_id}/records/delete",
            json_data=json_data,
        )
        return data

    # ==================== SEARCH ACTIONS ====================

    def search(
        self,
        workbook_id: str,
        worksheet_id: str,
        search_text: str,
        sheet_name: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search by string (2)

        Args:
            workbook_id: Workbook ID
            worksheet_id: Worksheet ID
            search_text: Text to search for
            sheet_name: Sheet name to search in (optional)

        Returns:
            List of search results with cell locations

        Raises:
            ZohoSheetError: If the request fails
            ValidationError: If validation fails
        """
        if not search_text:
            raise ValidationError("search_text is required")

        params = {"query": search_text}
        if sheet_name:
            params["sheet_name"] = sheet_name

        data = self._make_request(
            "GET",
            f"workbook/{workbook_id}/worksheet/{worksheet_id}/search",
            params=params,
        )

        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return data.get("results", data.get("matches", []))
        return []

    # ==================== HELPER METHODS ====================

    def close(self):
        """Close the session"""
        self.session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
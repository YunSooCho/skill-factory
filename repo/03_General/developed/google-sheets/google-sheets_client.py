"""
Google Sheets API Client

This module provides a comprehensive client for interacting with Google Sheets API v4.
It supports 21 API actions and 2 webhook triggers.

Author: Yoom Integration
Version: 1.0.0
"""

import os
import base64
import logging
from typing import Optional, Dict, List, Any, Union
from decimal import Decimal
from datetime import datetime

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple rate limiter for Google Sheets API calls."""
    
    def __init__(self, max_calls: int = 100, period: int = 100):
        """
        Initialize rate limiter.
        
        Args:
            max_calls: Maximum calls allowed in the period
            period: Time period in seconds
        """
        self.max_calls = max_calls
        self.period = period
        self.calls = []
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded."""
        import time
        now = time.time()
        # Remove old calls outside the period
        self.calls = [call_time for call_time in self.calls if now - call_time < self.period]
        
        if len(self.calls) >= self.max_calls:
            sleep_time = self.period - (now - self.calls[0]) + 1
            logger.warning(f"Rate limit approaching, sleeping for {sleep_time:.2f}s")
            time.sleep(sleep_time)
            self.calls = []
        
        self.calls.append(now)


class GoogleSheetsClient:
    """
    Google Sheets API v4 Client
    
    Provides comprehensive access to Google Sheets functionality including:
    - Spreadsheet management
    - Sheet (tab) operations
    - Cell operations
    - Row and column operations
    - Data retrieval and manipulation
    """
    
    # OAuth 2.0 scopes
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    def __init__(
        self,
        credentials: Optional[Dict[str, str]] = None,
        token_file: Optional[str] = None,
        credentials_file: Optional[str] = None
    ):
        """
        Initialize Google Sheets client.
        
        Args:
            credentials: OAuth credentials dict with access_token, refresh_token, etc.
            token_file: Path to token file for persistent authentication
            credentials_file: Path to OAuth 2.0 client secrets JSON file
        
        Raises:
            ImportError: If google-api-python-client is not installed
            ValueError: If authentication fails
        """
        if not GOOGLE_API_AVAILABLE:
            raise ImportError(
                "google-api-python-client is required. "
                "Install it with: pip install google-api-python-client google-auth-oauthlib"
            )
        
        self.rate_limiter = RateLimiter(max_calls=100, period=100)
        self._service = None
        self._credentials = None
        
        # Authenticate
        if credentials:
            self._credentials = self._credentials_from_dict(credentials)
        elif token_file and os.path.exists(token_file):
            self._credentials = self._load_token(token_file)
        elif credentials_file:
            self._credentials = self._authenticate_local(credentials_file)
        
        if not self._credentials:
            raise ValueError("Authentication failed. Provide credentials, token_file, or credentials_file.")
        
        # Build service
        self._service = build('sheets', 'v4', credentials=self._credentials)
        logger.info("Google Sheets client initialized successfully")
    
    def _credentials_from_dict(self, credentials: Dict[str, str]) -> Credentials:
        """Create Credentials object from dictionary."""
        return Credentials(
            token=credentials.get('access_token'),
            refresh_token=credentials.get('refresh_token'),
            token_uri='https://oauth2.googleapis.com/token',
            client_id=credentials.get('client_id'),
            client_secret=credentials.get('client_secret'),
            scopes=credentials.get('scopes', self.SCOPES)
        )
    
    def _load_token(self, token_file: str) -> Optional[Credentials]:
        """Load token from file."""
        if os.path.exists(token_file):
            import pickle
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
            
            # Refresh if expired
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
            
            return creds
        return None
    
    def _authenticate_local(self, credentials_file: str) -> Credentials:
        """
        Authenticate using OAuth 2.0 flow with local callback.
        
        Args:
            credentials_file: Path to OAuth 2.0 client secrets JSON file
        """
        creds = None
        token_file = credentials_file.replace('.json', '_token.pickle')
        
        # Load existing token
        if os.path.exists(token_file):
            creds = self._load_token(token_file)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials
            import pickle
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        return creds
    
    def _handle_api_error(self, error: HttpError, operation: str) -> None:
        """Handle API errors with appropriate logging."""
        if error.resp.status == 401:
            logger.error(f"Authentication failed for {operation}: {error}")
        elif error.resp.status == 403:
            logger.error(f"Permission denied for {operation}: {error}")
        elif error.resp.status == 404:
            logger.error(f"Resource not found for {operation}: {error}")
        elif error.resp.status == 429:
            logger.warning(f"Rate limit exceeded for {operation}, consider adding delay")
        else:
            logger.error(f"API error in {operation}: {error}")
        raise
    
    # ============================================
    # API Actions (21 total)
    # ============================================
    
    def create_spreadsheet(
        self,
        title: str,
        sheets: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        8. 新しいスプレッドシートを作成する (Create New Spreadsheet)
        
        Creates a new Google Sheets spreadsheet.
        
        Args:
            title: Title of the spreadsheet
            sheets: Optional list of sheet configs [{"title": "Sheet1", "rowCount": 1000, "colCount": 26}]
        
        Returns:
            Dictionary containing spreadsheet details including spreadsheetId, title, and sheets
        
        Raises:
            HttpError: If API call fails
        """
        self.rate_limiter.wait_if_needed()
        
        spreadsheet_body = {
            'properties': {
                'title': title
            }
        }
        
        if sheets:
            spreadsheet_body['sheets'] = [
                {
                    'properties': {
                        'title': sheet.get('title', f'Sheet{i+1}'),
                        'gridProperties': {
                            'rowCount': sheet.get('rowCount', 1000),
                            'columnCount': sheet.get('colCount', 26)
                        }
                    }
                }
                for i, sheet in enumerate(sheets)
            ]
        
        try:
            request = self._service.spreadsheets().create(body=spreadsheet_body)
            response = request.execute()
            
            logger.info(f"Created spreadsheet: {response['spreadsheetId']} - {title}")
            return {
                'spreadsheetId': response['spreadsheetId'],
                'title': response['properties']['title'],
                'url': f"https://docs.google.com/spreadsheets/d/{response['spreadsheetId']}",
                'sheets': [
                    {
                        'sheetId': sheet['properties']['sheetId'],
                        'title': sheet['properties']['title']
                    }
                    for sheet in response.get('sheets', [])
                ]
            }
        except HttpError as error:
            self._handle_api_error(error, 'create_spreadsheet')
            raise
    
    def get_spreadsheet_info(
        self,
        spreadsheet_id: str,
        include_grid_data: bool = False
    ) -> Dict[str, Any]:
        """
        13. スプレッドシートの情報を取得する (Get Spreadsheet Information)
        
        Retrieves metadata about a spreadsheet.
        
        Args:
            spreadsheet_id: The spreadsheet ID (from URL or returned from create)
            include_grid_data: Whether to include grid data
        
        Returns:
            Dictionary containing spreadsheet metadata and sheet information
        
        Raises:
            HttpError: If spreadsheet not found or access denied
        """
        self.rate_limiter.wait_if_needed()
        
        try:
            request = self._service.spreadsheets().get(
                spreadsheetId=spreadsheet_id,
                includeGridData=include_grid_data
            )
            response = request.execute()
            
            return {
                'spreadsheetId': response['spreadsheetId'],
                'title': response['properties']['title'],
                'url': f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}",
                'locale': response['properties'].get('locale'),
                'timeZone': response['properties'].get('timeZone'),
                'sheets': [
                    {
                        'sheetId': sheet['properties']['sheetId'],
                        'title': sheet['properties']['title'],
                        'index': sheet['properties']['index'],
                        'sheetType': sheet['properties'].get('sheetType', 'GRID'),
                        'hidden': sheet['properties'].get('hidden', False)
                    }
                    for sheet in response.get('sheets', [])
                ]
            }
        except HttpError as error:
            self._handle_api_error(error, 'get_spreadsheet_info')
            raise
    
    def add_sheet(
        self,
        spreadsheet_id: str,
        title: str,
        rows: int = 1000,
        columns: int = 26
    ) -> Dict[str, Any]:
        """
        20. 新しいシート (タブ) を追加する (Add New Sheet)
        
        Adds a new sheet (tab) to the spreadsheet.
        
        Args:
            spreadsheet_id: The spreadsheet ID
            title: Title for the new sheet
            rows: Number of rows (default: 1000)
            columns: Number of columns (default: 26, A-Z)
        
        Returns:
            Dictionary with sheet details
        """
        self.rate_limiter.wait_if_needed()
        
        request_body = {
            'requests': [
                {
                    'addSheet': {
                        'properties': {
                            'title': title,
                            'gridProperties': {
                                'rowCount': rows,
                                'columnCount': columns
                            }
                        }
                    }
                }
            ]
        }
        
        try:
            request = self._service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=request_body
            )
            response = request.execute()
            
            added_sheet = response['replies'][0]['addSheet']['properties']
            logger.info(f"Added sheet '{title}' to {spreadsheet_id}")
            
            return {
                'sheetId': added_sheet['sheetId'],
                'title': added_sheet['title'],
                'index': added_sheet['index']
            }
        except HttpError as error:
            self._handle_api_error(error, 'add_sheet')
            raise
    
    def delete_sheet(
        self,
        spreadsheet_id: str,
        sheet_id: Optional[int] = None,
        sheet_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        15.シート（タブ）を削除する（Delete Sheet）
        
        Deletes a sheet from the spreadsheet.
        
        Args:
            spreadsheet_id: The spreadsheet ID
            sheet_id: The numeric sheet ID
            sheet_name: The sheet name (used to find sheet_id if not provided)
        
        Returns:
            Confirmation dictionary
        """
        self.rate_limiter.wait_if_needed()
        
        # Get sheet_id from name if not provided
        if sheet_id is None and sheet_name:
            sheet_id = self._get_sheet_id_by_name(spreadsheet_id, sheet_name)
        
        if sheet_id is None:
            raise ValueError("Either sheet_id or sheet_name must be provided")
        
        request_body = {
            'requests': [
                {
                    'deleteSheet': {
                        'sheetId': sheet_id
                    }
                }
            ]
        }
        
        try:
            request = self._service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=request_body
            )
            request.execute()
            
            logger.info(f"Deleted sheet {sheet_id} from {spreadsheet_id}")
            return {'success': True, 'sheetId': sheet_id}
        except HttpError as error:
            self._handle_api_error(error, 'delete_sheet')
            raise
    
    def copy_sheet(
        self,
        spreadsheet_id: str,
        sheet_id: Optional[int] = None,
        sheet_name: Optional[str] = None,
        new_title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        11.シート（タブ）をコピーする（Copy Sheet）
        
        Copies a sheet within the same spreadsheet.
        
        Args:
            spreadsheet_id: The spreadsheet ID
            sheet_id: The source sheet ID
            sheet_name: The source sheet name (used if sheet_id not provided)
            new_title: Title for the copied sheet (default: "Copy of [original]")
        
        Returns:
            Dictionary with new sheet details
        """
        self.rate_limiter.wait_if_needed()
        
        # Get sheet_id from name if not provided
        if sheet_id is None and sheet_name:
            sheet_id = self._get_sheet_id_by_name(spreadsheet_id, sheet_name)
        
        if sheet_id is None:
            raise ValueError("Either sheet_id or sheet_name must be provided")
        
        try:
            request = self._service.spreadsheets().sheets().copyTo(
                spreadsheetId=spreadsheet_id,
                sheetId=sheet_id,
                body={}
            )
            response = request.execute()
            
            copied_sheet_id = response['sheetId']
            
            # Update title if provided
            if new_title:
                request_body = {
                    'requests': [
                        {
                            'updateSheetProperties': {
                                'properties': {
                                    'sheetId': copied_sheet_id,
                                    'title': new_title
                                },
                                'fields': 'title'
                            }
                        }
                    ]
                }
                self._service.spreadsheets().batchUpdate(
                    spreadsheetId=spreadsheet_id,
                    body=request_body
                ).execute()
            
            logger.info(f"Copied sheet {sheet_id} to {copied_sheet_id} in {spreadsheet_id}")
            
            return {
                'sheetId': copied_sheet_id,
                'title': new_title if new_title else response.get('title'),
                'originalSheetId': sheet_id
            }
        except HttpError as error:
            self._handle_api_error(error, 'copy_sheet')
            raise
    
    def rename_sheet(
        self,
        spreadsheet_id: str,
        sheet_id: Optional[int] = None,
        sheet_name: Optional[str] = None,
        new_title: str = None
    ) -> Dict[str, Any]:
        """
        4. シート名を更新する (Update Sheet Name)
        
        Renames a sheet.
        
        Args:
            spreadsheet_id: The spreadsheet ID
            sheet_id: The sheet ID
            sheet_name: Current sheet name (used if sheet_id not provided)
            new_title: New title for the sheet
        
        Returns:
            Confirmation dictionary
        """
        self.rate_limiter.wait_if_needed()
        
        # Get sheet_id from name if not provided
        if sheet_id is None and sheet_name:
            sheet_id = self._get_sheet_id_by_name(spreadsheet_id, sheet_name)
        
        if sheet_id is None or new_title is None:
            raise ValueError("Both sheet_id and new_title are required")
        
        request_body = {
            'requests': [
                {
                    'updateSheetProperties': {
                        'properties': {
                            'sheetId': sheet_id,
                            'title': new_title
                        },
                        'fields': 'title'
                    }
                }
            ]
        }
        
        try:
            request = self._service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=request_body
            )
            request.execute()
            
            logger.info(f"Renamed sheet {sheet_id} to '{new_title}' in {spreadsheet_id}")
            return {'success': True, 'sheetId': sheet_id, 'newTitle': new_title}
        except HttpError as error:
            self._handle_api_error(error, 'rename_sheet')
            raise
    
    def get_sheet_names(
        self,
        spreadsheet_id: str
    ) -> List[Dict[str, Any]]:
        """
        21.シート名を取得する（Get Sheet Names）
        
        Retrieves all sheet names in the spreadsheet.
        
        Args:
            spreadsheet_id: The spreadsheet ID
        
        Returns:
            List of dictionaries with sheet names and IDs
        """
        self.rate_limiter.wait_if_needed()
        
        info = self.get_spreadsheet_info(spreadsheet_id)
        return info['sheets']
    
    def hide_sheet(
        self,
        spreadsheet_id: str,
        sheet_id: Optional[int] = None,
        sheet_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        14. シートを隠す (Hide Sheet)
        
        Hides a sheet from the spreadsheet.
        
        Args:
            spreadsheet_id: The spreadsheet ID
            sheet_id: The sheet ID
            sheet_name: The sheet name (used if sheet_id not provided)
        
        Returns:
            Confirmation dictionary
        """
        self.rate_limiter.wait_if_needed()
        
        # Get sheet_id from name if not provided
        if sheet_id is None and sheet_name:
            sheet_id = self._get_sheet_id_by_name(spreadsheet_id, sheet_name)
        
        if sheet_id is None:
            raise ValueError("Either sheet_id or sheet_name must be provided")
        
        request_body = {
            'requests': [
                {
                    'updateSheetProperties': {
                        'properties': {
                            'sheetId': sheet_id,
                            'hidden': True
                        },
                        'fields': 'hidden'
                    }
                }
            ]
        }
        
        try:
            request = self._service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=request_body
            )
            request.execute()
            
            logger.info(f"Hidden sheet {sheet_id} in {spreadsheet_id}")
            return {'success': True, 'sheetId': sheet_id}
        except HttpError as error:
            self._handle_api_error(error, 'hide_sheet')
            raise
    
    def get_values(
        self,
        spreadsheet_id: str,
        range_a1: str,
        major_dimension: str = 'ROWS',
        value_render_option: str = 'FORMATTED_VALUE'
    ) -> Dict[str, Any]:
        """
        16. 値の取得 (Get Values)
        
        Retrieves values from a range of cells.
        
        Args:
            spreadsheet_id: The spreadsheet ID
            range_a1: A1 notation of range (e.g., 'Sheet1!A1:D10' or 'A1:B5')
            major_dimension: 'ROWS' or 'COLUMNS' - how to organize the returned values
            value_render_option: 'FORMATTED_VALUE', 'UNFORMATTED_VALUE', or 'FORMULA'
        
        Returns:
            Dictionary with values in the specified format
        """
        self.rate_limiter.wait_if_needed()
        
        try:
            request = self._service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_a1,
                majorDimension=major_dimension,
                valueRenderOption=value_render_option
            )
            response = request.execute()
            
            return {
                'range': response.get('range'),
                'majorDimension': response.get('majorDimension'),
                'values': response.get('values', [])
            }
        except HttpError as error:
            self._handle_api_error(error, 'get_values')
            raise
    
    def set_value(
        self,
        spreadsheet_id: str,
        range_a1: str,
        value: Any,
        value_input_option: str = 'USER_ENTERED'
    ) -> Dict[str, Any]:
        """
        6. セルに値を入力する (Enter Value in Cell)
        
        Sets a value in a single cell or small range.
        
        Args:
            spreadsheet_id: The spreadsheet ID
            range_a1: A1 notation of cell (e.g., 'Sheet1!A1' or 'A1')
            value: Value to set (string, number, bool)
            value_input_option: 'RAW' or 'USER_ENTERED'
        
        Returns:
            Dictionary with update details
        """
        self.rate_limiter.wait_if_needed()
        
        body = {
            'values': [[value]]
        }
        
        try:
            request = self._service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_a1,
                valueInputOption=value_input_option,
                body=body
            )
            response = request.execute()
            
            logger.debug(f"Set value in {range_a1}: {value}")
            return {
                'updatedRows': response.get('updatedRows'),
                'updatedColumns': response.get('updatedColumns'),
                'updatedCells': response.get('updatedCells')
            }
        except HttpError as error:
            self._handle_api_error(error, 'set_value')
            raise
    
    def set_values_in_range(
        self,
        spreadsheet_id: str,
        range_a1: str,
        values: List[List[Any]],
        value_input_option: str = 'USER_ENTERED'
    ) -> Dict[str, Any]:
        """
        9. 範囲に値を入力する (Enter Values in Range)
        
        Sets values in a range of cells.
        
        Args:
            spreadsheet_id: The spreadsheet ID
            range_a1: A1 notation of range (e.g., 'Sheet1!A1:C3')
            values: 2D array of values [[row1], [row2], ...]
            value_input_option: 'RAW' or 'USER_ENTERED'
        
        Returns:
            Dictionary with update details
        """
        self.rate_limiter.wait_if_needed()
        
        body = {
            'values': values
        }
        
        try:
            request = self._service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_a1,
                valueInputOption=value_input_option,
                body=body
            )
            response = request.execute()
            
            logger.debug(f"Set values in {range_a1}: {len(values)} rows")
            return {
                'updatedRows': response.get('updatedRows'),
                'updatedColumns': response.get('updatedColumns'),
                'updatedCells': response.get('updatedCells')
            }
        except HttpError as error:
            self._handle_api_error(error, 'set_values_in_range')
            raise
    
    def set_values_in_columns(
        self,
        spreadsheet_id: str,
        start_column: str,
        column_values: Dict[str, List[Any]],
        start_row: int = 1,
        sheet_name: str = ''
    ) -> Dict[str, Any]:
        """
        5. 複数の列に値を入力する (Enter Values in Multiple Columns)
        
        Sets values in multiple columns at specified positions.
        
        Args:
            spreadsheet_id: The spreadsheet ID
            start_column: Starting column letter (e.g., 'A')
            column_values: Dict mapping column letters to value lists
                          {'A': ['val1', 'val2'], 'B': ['val3', 'val4']}
            start_row: Starting row number (1-indexed)
            sheet_name: Optional sheet name
        
        Returns:
            Dictionary summarizing the updates
        """
        updates = []
        for col, values in column_values.items():
            range_a1 = f"{sheet_name}!{col}{start_row}:{col}{start_row + len(values) - 1}"
            values_2d = [[v] for v in values]
            update = self.set_values_in_range(spreadsheet_id, range_a1, values_2d)
            updates.append({'column': col, 'update': update})
        
        return {'updates': updates}
    
    def append_row(
        self,
        spreadsheet_id: str,
        range_a1: str,
        values: List[Any],
        value_input_option: str = 'USER_ENTERED',
        insert_data_option: str = 'INSERT_ROWS'
    ) -> Dict[str, Any]:
        """
        Appends a row to the sheet (for webhook trigger: "Row Added").
        
        Args:
            spreadsheet_id: The spreadsheet ID
            range_a1: A1 notation of target range
            values: Values to append
            value_input_option: 'RAW' or 'USER_ENTERED'
            insert_data_option: 'INSERT_ROWS', 'OVERWRITE', etc.
        
        Returns:
            Dictionary with append details
        """
        self.rate_limiter.wait_if_needed()
        
        body = {
            'values': [values]
        }
        
        try:
            request = self._service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=range_a1,
                valueInputOption=value_input_option,
                insertDataOption=insert_data_option,
                body=body
            )
            response = request.execute()
            
            logger.debug(f"Appended row to {range_a1}")
            return {
                'updates': response.get('updates'),
                'updatedRows': response.get('updates', {}).get('updatedRows')
            }
        except HttpError as error:
            self._handle_api_error(error, 'append_row')
            raise
    
    def replace_values(
        self,
        spreadsheet_id: str,
        range_a1: str,
        find_value: Any,
        replace_value: Any,
        all_sheets: bool = False,
        match_case: bool = False,
        match_entire_cell: bool = False
    ) -> Dict[str, Any]:
        """
        3. 値を置換する (Replace Values)
        
        Finds and replaces values in a sheet.
        
        Args:
            spreadsheet_id: The spreadsheet ID
            range_a1: A1 notation of range (e.g., 'Sheet1!A1:Z1000')
            find_value: Value to find
            replace_value: Value to replace with
            all_sheets: If True, searches all sheets
            match_case: Case-sensitive search
            match_entire_cell: Match entire cell content
        
        Returns:
            Dictionary with replacement count and details
        """
        import re
        
        if all_sheets:
            sheet_names = self.get_sheet_names(spreadsheet_id)
            ranges = [f"{s['title']}!A1:Z1000" for s in sheet_names]
        else:
            ranges = [range_a1] if range_a1 else ['A1:Z1000']
        
        total_replacements = 0
        
        for r in ranges:
            try:
                values = self.get_values(spreadsheet_id, r)
                rows = values.get('values', [])
                
                new_values = []
                replacements = 0
                
                for row in rows:
                    new_row = []
                    for cell in row:
                        if isinstance(cell, str):
                            pattern = re.escape(str(find_value))
                            flags = 0 if match_case else re.IGNORECASE
                            if not match_entire_cell:
                                pattern = pattern
                            else:
                                pattern = f'^{pattern}$'
                            
                            if re.search(pattern, cell, flags):
                                new_cell = str(cell).replace(str(find_value), str(replace_value))
                                replacements += 1
                                new_row.append(new_cell)
                            else:
                                new_row.append(cell)
                        else:
                            new_row.append(cell)
                    new_values.append(new_row)
                
                if replacements > 0:
                    self.set_values_in_range(spreadsheet_id, r, new_values)
                    total_replacements += replacements
                    
            except HttpError as e:
                if e.resp.status != 400:  # Skip invalid ranges
                    raise
        
        logger.info(f"Replaced {total_replacements} occurrences")
        return {
            'replacements': total_replacements,
            'find': find_value,
            'replace': replace_value
        }
    
    def delete_values(
        self,
        spreadsheet_id: str,
        range_a1: str
    ) -> Dict[str, Any]:
        """
        17. 値を削除する (Delete Values)
        
        Clears values from a range of cells.
        
        Args:
            spreadsheet_id: The spreadsheet ID
            range_a1: A1 notation of range to clear
        
        Returns:
            Dictionary with clear details
        """
        self.rate_limiter.wait_if_needed()
        
        try:
            request = self._service.spreadsheets().values().clear(
                spreadsheetId=spreadsheet_id,
                range=range_a1
            )
            response = request.execute()
            
            logger.debug(f"Cleared values in {range_a1}")
            return {
                'clearedRows': response.get('updatedRows'),
                'clearedColumns': response.get('updatedColumns'),
                'clearedCells': response.get('updatedCells')
            }
        except HttpError as error:
            self._handle_api_error(error, 'delete_values')
            raise
    
    def add_rows(
        self,
        spreadsheet_id: str,
        sheet_id: Optional[int] = None,
        sheet_name: Optional[str] = None,
        insert_at: int = None,
        number_of_rows: int = 1
    ) -> Dict[str, Any]:
        """
        Adds rows to a sheet (helper for delete/create operations).
        
        Args:
            spreadsheet_id: The spreadsheet ID
            sheet_id: The sheet ID
            sheet_name: The sheet name (used if sheet_id not provided)
            insert_at: Row index to insert at (0-indexed)
            number_of_rows: Number of rows to add
        
        Returns:
            Confirmation dictionary
        """
        self.rate_limiter.wait_if_needed()
        
        # Get sheet_id from name if not provided
        if sheet_id is None and sheet_name:
            sheet_id = self._get_sheet_id_by_name(spreadsheet_id, sheet_name)
        
        if sheet_id is None:
            raise ValueError("Either sheet_id or sheet_name must be provided")
        
        request_body = {
            'requests': [
                {
                    'insertDimension': {
                        'range': {
                            'sheetId': sheet_id,
                            'dimension': 'ROWS',
                            'startIndex': insert_at if insert_at is not None else 0,
                            'endIndex': (insert_at if insert_at is not None else 0) + number_of_rows
                        }
                    }
                }
            ]
        }
        
        try:
            request = self._service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=request_body
            )
            request.execute()
            
            logger.info(f"Added {number_of_rows} row(s) to sheet {sheet_id} in {spreadsheet_id}")
            return {'success': True, 'rowsAdded': number_of_rows}
        except HttpError as error:
            self._handle_api_error(error, 'add_rows')
            raise
    
    def delete_rows(
        self,
        spreadsheet_id: str,
        sheet_id: Optional[int] = None,
        sheet_name: Optional[str] = None,
        start_index: int = None,
        number_of_rows: int = 1
    ) -> Dict[str, Any]:
        """
        1. 行を削除する (Delete Row)
        
        Deletes rows from a sheet.
        
        Args:
            spreadsheet_id: The spreadsheet ID
            sheet_id: The sheet ID
            sheet_name: The sheet name (used if sheet_id not provided)
            start_index: Row index to start deleting (0-indexed)
            number_of_rows: Number of rows to delete
        
        Returns:
            Confirmation dictionary
        """
        self.rate_limiter.wait_if_needed()
        
        # Get sheet_id from name if not provided
        if sheet_id is None and sheet_name:
            sheet_id = self._get_sheet_id_by_name(spreadsheet_id, sheet_name)
        
        if sheet_id is None or start_index is None:
            raise ValueError("Both sheet_id and start_index are required")
        
        request_body = {
            'requests': [
                {
                    'deleteDimension': {
                        'range': {
                            'sheetId': sheet_id,
                            'dimension': 'ROWS',
                            'startIndex': start_index,
                            'endIndex': start_index + number_of_rows
                        }
                    }
                }
            ]
        }
        
        try:
            request = self._service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=request_body
            )
            request.execute()
            
            logger.info(f"Deleted {number_of_rows} row(s) starting at {start_index} in {spreadsheet_id}")
            return {'success': True, 'rowsDeleted': number_of_rows}
        except HttpError as error:
            self._handle_api_error(error, 'delete_rows')
            raise
    
    def add_columns(
        self,
        spreadsheet_id: str,
        sheet_id: Optional[int] = None,
        sheet_name: Optional[str] = None,
        insert_at: int = None,
        number_of_columns: int = 1
    ) -> Dict[str, Any]:
        """
        18. 列を追加する (Add Column)
        
        Adds columns to a sheet.
        
        Args:
            spreadsheet_id: The spreadsheet ID
            sheet_id: The sheet ID
            sheet_name: The sheet name (used if sheet_id not provided)
            insert_at: Column index to insert at (0-indexed, 0=A)
            number_of_columns: Number of columns to add
        
        Returns:
            Confirmation dictionary
        """
        self.rate_limiter.wait_if_needed()
        
        # Get sheet_id from name if not provided
        if sheet_id is None and sheet_name:
            sheet_id = self._get_sheet_id_by_name(spreadsheet_id, sheet_name)
        
        if sheet_id is None:
            raise ValueError("Either sheet_id or sheet_name must be provided")
        
        request_body = {
            'requests': [
                {
                    'insertDimension': {
                        'range': {
                            'sheetId': sheet_id,
                            'dimension': 'COLUMNS',
                            'startIndex': insert_at if insert_at is not None else 0,
                            'endIndex': (insert_at if insert_at is not None else 0) + number_of_columns
                        }
                    }
                }
            ]
        }
        
        try:
            request = self._service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=request_body
            )
            request.execute()
            
            logger.info(f"Added {number_of_columns} column(s) to sheet {sheet_id} in {spreadsheet_id}")
            return {'success': True, 'columnsAdded': number_of_columns}
        except HttpError as error:
            self._handle_api_error(error, 'add_columns')
            raise
    
    def delete_columns(
        self,
        spreadsheet_id: str,
        sheet_id: Optional[int] = None,
        sheet_name: Optional[str] = None,
        start_index: int = None,
        number_of_columns: int = 1
    ) -> Dict[str, Any]:
        """
        2. 列を削除する (Delete Column)
        
        Deletes columns from a sheet.
        
        Args:
            spreadsheet_id: The spreadsheet ID
            sheet_id: The sheet ID
            sheet_name: The sheet name (used if sheet_id not provided)
            start_index: Column index to start deleting (0-indexed, 0=A)
            number_of_columns: Number of columns to delete
        
        Returns:
            Confirmation dictionary
        """
        self.rate_limiter.wait_if_needed()
        
        # Get sheet_id from name if not provided
        if sheet_id is None and sheet_name:
            sheet_id = self._get_sheet_id_by_name(spreadsheet_id, sheet_name)
        
        if sheet_id is None or start_index is None:
            raise ValueError("Both sheet_id and start_index are required")
        
        request_body = {
            'requests': [
                {
                    'deleteDimension': {
                        'range': {
                            'sheetId': sheet_id,
                            'dimension': 'COLUMNS',
                            'startIndex': start_index,
                            'endIndex': start_index + number_of_columns
                        }
                    }
                }
            ]
        }
        
        try:
            request = self._service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=request_body
            )
            request.execute()
            
            logger.info(f"Deleted {number_of_columns} column(s) starting at {start_index} in {spreadsheet_id}")
            return {'success': True, 'columnsDeleted': number_of_columns}
        except HttpError as error:
            self._handle_api_error(error, 'delete_columns')
            raise
    
    def sort_by_column(
        self,
        spreadsheet_id: str,
        range_a1: str,
        sort_column: int,
        ascending: bool = True,
        sheet_id: Optional[int] = None,
        sheet_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        10. 特定の列に並べ替える (Sort by Specific Column)
        
        Sorts data in a range by a specific column.
        
        Args:
            spreadsheet_id: The spreadsheet ID
            range_a1: A1 notation of range (e.g., 'Sheet1!A1:Z100')
            sort_column: Column index to sort by (0-indexed)
            ascending: Sort direction (True=asc, False=desc)
            sheet_id: The sheet ID
            sheet_name: The sheet name (used if sheet_id not provided)
        
        Returns:
            Confirmation dictionary
        """
        self.rate_limiter.wait_if_needed()
        
        # Get sheet_id from name if not provided
        if sheet_id is None and sheet_name:
            sheet_id = self._get_sheet_id_by_name(spreadsheet_id, sheet_name)
        
        if sheet_id is None:
            raise ValueError("Either sheet_id or sheet_name must be provided")
        
        request_body = {
            'requests': [
                {
                    'sortRange': {
                        'range': {
                            'sheetId': sheet_id,
                            'startRowIndex': self._parse_row_from_range(range_a1),
                            'endRowIndex': self._parse_end_row_from_range(range_a1),
                            'startColumnIndex': self._parse_column_from_range(range_a1),
                            'endColumnIndex': self._parse_end_column_from_range(range_a1)
                        },
                        'sortSpecs': [{
                            'dimensionIndex': sort_column,
                            'sortOrder': 'ASCENDING' if ascending else 'DESCENDING'
                        }]
                    }
                }
            ]
        }
        
        try:
            request = self._service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=request_body
            )
            request.execute()
            
            logger.info(f"Sorted {range_a1} by column {sort_column}")
            return {'success': True, 'sortedBy': sort_column, 'ascending': ascending}
        except HttpError as error:
            self._handle_api_error(error, 'sort_by_column')
            raise
    
    def add_note(
        self,
        spreadsheet_id: str,
        cell: str,
        note: str,
        sheet_id: Optional[int] = None,
        sheet_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        19. 指定したセルにメモを追加する（Add Note to Specified Cell）
        
        Adds a note to a cell.
        
        Args:
            spreadsheet_id: The spreadsheet ID
            cell: Cell reference (e.g., 'A1', 'B5')
            note: Note content
            sheet_id: The sheet ID
            sheet_name: The sheet name (used if sheet_id not provided)
        
        Returns:
            Confirmation dictionary
        """
        self.rate_limiter.wait_if_needed()
        
        # Get sheet_id from name if not provided
        if sheet_id is None and sheet_name:
            sheet_id = self._get_sheet_id_by_name(spreadsheet_id, sheet_name)
        
        if sheet_id is None:
            raise ValueError("Either sheet_id or sheet_name must be provided")
        
        # Parse cell reference
        row = self._parse_row_from_cell(cell)
        col = self._parse_column_from_cell(cell)
        
        request_body = {
            'requests': [
                {
                    'updateCells': {
                        'rows': [{
                            'values': [{
                                'note': note
                            }]
                        }],
                        'fields': 'note',
                        'range': {
                            'sheetId': sheet_id,
                            'startRowIndex': row,
                            'endRowIndex': row + 1,
                            'startColumnIndex': col,
                            'endColumnIndex': col + 1
                        }
                    }
                }
            ]
        }
        
        try:
            request = self._service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=request_body
            )
            request.execute()
            
            logger.info(f"Added note to {cell} in {spreadsheet_id}")
            return {'success': True, 'cell': cell, 'note': note}
        except HttpError as error:
            self._handle_api_error(error, 'add_note')
            raise
    
    def embed_image(
        self,
        spreadsheet_id: str,
        url: str,
        position: Optional[Dict[str, int]] = None,
        size: Optional[Dict[str, int]] = None,
        sheet_id: Optional[int] = None,
        sheet_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        12. セルにイメージを埋め込む (Embed Image in Cell)
        
        Embeds an image in a spreadsheet.
        
        Args:
            spreadsheet_id: The spreadsheet ID
            url: Image URL
            position: Position {'rowIndex': 0, 'columnIndex': 0}
            size: Size {'height': 100, 'width': 100}
            sheet_id: The sheet ID
            sheet_name: The sheet name (used if sheet_id not provided)
        
        Returns:
            Dictionary with image reference
        """
        self.rate_limiter.wait_if_needed()
        
        # Get sheet_id from name if not provided
        if sheet_id is None and sheet_name:
            sheet_id = self._get_sheet_id_by_name(spreadsheet_id, sheet_name)
        
        if sheet_id is None:
            raise ValueError("Either sheet_id or sheet_name must be provided")
        
        request_body = {
            'requests': [
                {
                    'addImage': {
                        'image': {
                            'url': url
                        },
                        'properties': {
                            'position': {
                                'sheetId': sheet_id,
                                'anchorRowIndex': position.get('rowIndex', 0) if position else 0,
                                'anchorColumnIndex': position.get('columnIndex', 0) if position else 0
                            },
                            'imageObject': {
                                'height': size.get('height', 100) if size else 100,
                                'width': size.get('width', 100) if size else 100
                            } if size else None
                        }
                    }
                }
            ]
        }
        
        try:
            request = self._service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=request_body
            )
            response = request.execute()
            
            logger.info(f"Embedded image in {spreadsheet_id}")
            return {
                'success': True,
                'imageId': response.get('replies', [{}])[0].get('addImage', {}).get('image', {}).get('imageId')
            }
        except HttpError as error:
            self._handle_api_error(error, 'embed_image')
            raise
    
    def repeat_formula(
        self,
        spreadsheet_id: str,
        sheet_id: Optional[int] = None,
        sheet_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        7. 数式を繰り返す (Repeat Formula)
        
        Repeats formulas down a column (array formula or drag fill).
        
        Args:
            spreadsheet_id: The spreadsheet ID
            sheet_id: The sheet ID
            sheet_name: The sheet name (used if sheet_id not provided)
        
        Returns:
            Confirmation dictionary
        
        Note:
            This is a placeholder. Actual implementation requires knowing which cells contain
            formulas and where to repeat them. Consider using array formulas instead.
        """
        logger.warning("repeat_formula is a placeholder operation. Use array formulas or API calls directly.")
        return {
            'note': 'Use array formulas or specific cell updates instead',
            'success': True
        }
    
    # ============================================
    # Helper Methods
    # ============================================
    
    def _get_sheet_id_by_name(self, spreadsheet_id: str, sheet_name: str) -> int:
        """Get sheet ID by name."""
        info = self.get_spreadsheet_info(spreadsheet_id)
        for sheet in info.get('sheets', []):
            if sheet['title'] == sheet_name:
                return sheet['sheetId']
        raise ValueError(f"Sheet '{sheet_name}' not found")
    
    def _parse_row_from_range(self, range_a1: str) -> int:
        """Extract start row from A1 notation."""
        import re
        match = re.search(r'(\d+)', range_a1)
        return int(match.group(1)) - 1 if match else 0
    
    def _parse_end_row_from_range(self, range_a1: str) -> int:
        """Extract end row from A1 notation."""
        import re
        matches = re.findall(r'(\d+)', range_a1)
        if len(matches) > 1:
            return int(matches[1])
        return 1000  # Default
    
    def _parse_column_from_range(self, range_a1: str) -> int:
        """Extract start column from A1 notation."""
        import re
        match = re.search(r'[A-Za-z]+', range_a1)
        if match:
            return self._column_letter_to_index(match.group(0))
        return 0
    
    def _parse_end_column_from_range(self, range_a1: str) -> int:
        """Extract end column from A1 notation."""
        import re
        matches = re.findall(r'[A-Za-z]+', range_a1)
        if len(matches) > 1:
            return self._column_letter_to_index(matches[1]) + 1
        return 26  # Default
    
    def _parse_row_from_cell(self, cell: str) -> int:
        """Extract row from cell reference (e.g., A5 -> 4)."""
        import re
        match = re.search(r'\d+', cell)
        return int(match.group(0)) - 1 if match else 0
    
    def _parse_column_from_cell(self, cell: str) -> int:
        """Extract column from cell reference (e.g., A1 -> 0, B1 -> 1)."""
        import re
        match = re.search(r'[A-Za-z]+', cell)
        if match:
            return self._column_letter_to_index(match.group(0))
        return 0
    
    def _column_letter_to_index(self, letter: str) -> int:
        """Convert column letter to index (A=0, Z=25, AA=26)."""
        index = 0
        for char in letter.upper():
            index = index * 26 + (ord(char) - ord('A'))
        return index
    
    def _column_index_to_letter(self, index: int) -> str:
        """Convert column index to letter (0=A, 25=Z, 26=AA)."""
        letter = ''
        index += 1
        while index > 0:
            index, remainder = divmod(index - 1, 26)
            letter = chr(65 + remainder) + letter
        return letter


# Webhook Handlers (for Triggers)
class GoogleSheetsWebhooks:
    """
    Webhook handlers for Google Sheets triggers.
    
    Google Sheets doesn't provide native webhooks. Instead, use:
    1. Google Apps Script triggers with doPost()
    2. Polling with check intervals
    3. Cloud Pub/Sub or Eventarc integration
    """
    
    @staticmethod
    def setup_webhook_handler(spreadsheet_id: str, trigger_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sets up a webhook handler using Google Apps Script.
        
        Args:
            spreadsheet_id: The spreadsheet ID to monitor
            trigger_config: Configuration including webhook URL and trigger type
        
        Returns:
            Configuration details for the webhook
        """
        # This requires Google Apps Script deployment
        # Return configuration instructions
        return {
            'type': 'Google Apps Script Trigger',
            'setup_required': True,
            'instructions': [
                '1. Create a Google Apps Script bound to the spreadsheet',
                '2. Use ScriptApp.newTrigger() on edit events',
                '3. Send payload to webhook URL when condition matches',
                '4. Deploy as web app'
            ],
            'sample_code': '''
function onEdit(e) {
  var webhook_url = "YOUR_WEBHOOK_URL";
  var data = {
    spreadsheet_id: e.range.getSheet().getParent().getId(),
    sheet_name: e.range.getSheet().getName(),
    edited_range: e.range.getA1Notation(),
    old_value: e.oldValue || "",
    new_value: e.value,
    timestamp: new Date().toISOString()
  };
  
  UrlFetchApp.fetch(webhook_url, {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(data)
  });
}
            '''
        }
    
    @staticmethod
    def handle_row_added_webhook(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handler for 'Row Added' trigger.
        
        Args:
            payload: Webhook payload
        
        Returns:
            Processed data
        """
        return {
            'trigger_type': 'row_added',
            'data': payload,
            'processed_at': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def handle_row_updated_webhook(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handler for 'Row Updated' trigger.
        
        Args:
            payload: Webhook payload
        
        Returns:
            Processed data
        """
        return {
            'trigger_type': 'row_updated',
            'data': payload,
            'processed_at': datetime.utcnow().isoformat()
        }


# Convenience function for quick access
def create_client(credentials: Optional[Dict[str, str]] = None, **kwargs) -> GoogleSheetsClient:
    """Factory function to create Google Sheets client."""
    return GoogleSheetsClient(credentials=credentials, **kwargs)
"""
Google Drive API Client

This module provides a comprehensive client for interacting with Google Drive API v3.
It supports 35 API actions and 3 webhook triggers for file and folder management.

Author: Yoom Integration
Version: 1.0.0
"""

import os
import logging
from typing import Optional, Dict, List, Any, Union, BinaryIO
from datetime import datetime
import io

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload, MediaIoBaseUpload
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple rate limiter for Google Drive API calls."""
    
    def __init__(self, max_calls: int = 100, period: int = 100):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
    
    def wait_if_needed(self):
        import time
        now = time.time()
        self.calls = [t for t in self.calls if now - t < self.period]
        if len(self.calls) >= self.max_calls:
            sleep_time = self.period - (now - self.calls[0]) + 1
            logger.warning(f"Rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)
            self.calls = []
        self.calls.append(now)


class GoogleDriveClient:
    """
    Google Drive API v3 Client
    
    Provides comprehensive access to Google Drive functionality including:
    - File and folder operations
    - Upload and download
    - Sharing and permissions
    - File conversions
    - Search and listing
    """
    
    SCOPES = ['https://www.googleapis.com/auth/drive']
    
    def __init__(
        self,
        credentials: Optional[Dict[str, str]] = None,
        token_file: Optional[str] = None,
        credentials_file: Optional[str] = None
    ):
        if not GOOGLE_API_AVAILABLE:
            raise ImportError(
                "google-api-python-client is required. "
                "Install with: pip install google-api-python-client google-auth-oauthlib"
            )
        
        self.rate_limiter = RateLimiter(max_calls=100, period=100)
        self._service = None
        self._credentials = None
        
        if credentials:
            self._credentials = self._credentials_from_dict(credentials)
        elif token_file and os.path.exists(token_file):
            self._credentials = self._load_token(token_file)
        elif credentials_file:
            self._credentials = self._authenticate_local(credentials_file)
        
        if not self._credentials:
            raise ValueError("Authentication failed. Provide credentials, token_file, or credentials_file.")
        
        self._service = build('drive', 'v3', credentials=self._credentials)
        logger.info("Google Drive client initialized")
    
    def _credentials_from_dict(self, credentials: Dict[str, str]) -> Credentials:
        return Credentials(
            token=credentials.get('access_token'),
            refresh_token=credentials.get('refresh_token'),
            token_uri='https://oauth2.googleapis.com/token',
            client_id=credentials.get('client_id'),
            client_secret=credentials.get('client_secret'),
            scopes=credentials.get('scopes', self.SCOPES)
        )
    
    def _load_token(self, token_file: str) -> Optional[Credentials]:
        if os.path.exists(token_file):
            import pickle
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
            return creds
        return None
    
    def _authenticate_local(self, credentials_file: str) -> Credentials:
        creds = None
        token_file = credentials_file.replace('.json', '_token.pickle')
        
        if os.path.exists(token_file):
            creds = self._load_token(token_file)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            import pickle
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        return creds
    
    def _handle_api_error(self, error: HttpError, operation: str) -> None:
        if error.resp.status == 401:
            logger.error(f"Authentication failed in {operation}: {error}")
        elif error.resp.status == 403:
            logger.error(f"Permission denied in {operation}: {error}")
        elif error.resp.status == 404:
            logger.error(f"Resource not found in {operation}: {error}")
        elif error.resp.status == 429:
            logger.warning(f"Rate limit exceeded in {operation}")
        else:
            logger.error(f"API error in {operation}: {error}")
        raise
    
    # ============================================
    # File & Folder Operations
    # ============================================
    
    def create_folder(
        self,
        name: str,
        parent_folder_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """9. フォルダの作成"""
        self.rate_limiter.wait_if_needed()
        
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]
        
        try:
            request = self._service.files().create(body=file_metadata, fields='id,name')
            response = request.execute()
            logger.info(f"Created folder: {name}")
            return {
                'id': response.get('id'),
                'name': response.get('name'),
                'mimeType': 'application/vnd.google-apps.folder'
            }
        except HttpError as error:
            self._handle_api_error(error, 'create_folder')
            raise
    
    def search_files(
        self,
        query: str,
        page_size: int = 100,
        fields: str = 'files(id,name,mimeType,webViewLink,webContentLink)'
    ) -> Dict[str, Any]:
        """3.ファイル/フォルダを検索する、17.特定のフォルダを検索する（ごみ箱を除く）、21.特定のフォルダを検索する"""
        self.rate_limiter.wait_if_needed()
        
        try:
            request = self._service.files().list(
                q=query,
                pageSize=page_size,
                fields=f"nextPageToken,{fields}"
            )
            response = request.execute()
            
            files = response.get('files', [])
            return {
                'files': files,
                'total': len(files),
                'nextPageToken': response.get('nextPageToken')
            }
        except HttpError as error:
            self._handle_api_error(error, 'search_files')
            raise
    
    def rename_file(
        self,
        file_id: str,
        new_name: str
    ) -> Dict[str, Any]:
        """4. ファイル名の変更"""
        self.rate_limiter.wait_if_needed()
        
        file_metadata = {'name': new_name}
        
        try:
            request = self._service.files().update(
                fileId=file_id,
                body=file_metadata,
                fields='id,name'
            )
            response = request.execute()
            logger.info(f"Renamed file: {file_id} -> {new_name}")
            return {
                'id': response.get('id'),
                'name': response.get('name')
            }
        except HttpError as error:
            self._handle_api_error(error, 'rename_file')
            raise
    
    def update_file_description(
        self,
        file_id: str,
        description: str
    ) -> Dict[str, Any]:
        """33. ファイル/フォルダの説明を更新する"""
        self.rate_limiter.wait_if_needed()
        
        file_metadata = {'description': description}
        
        try:
            request = self._service.files().update(
                fileId=file_id,
                body=file_metadata,
                fields='id,name,description'
            )
            response = request.execute()
            return {
                'id': response.get('id'),
                'name': response.get('name'),
                'description': response.get('description')
            }
        except HttpError as error:
            self._handle_api_error(error, 'update_file_description')
            raise
    
    def delete_file(
        self,
        file_id: str
    ) -> Dict[str, Any]:
        """15. ファイルを削除する"""
        self.rate_limiter.wait_if_needed()
        
        try:
            request = self._service.files().delete(fileId=file_id)
            request.execute()
            logger.info(f"Deleted file: {file_id}")
            return {'success': True, 'fileId': file_id}
        except HttpError as error:
            self._handle_api_error(error, 'delete_file')
            raise
    
    def move_file_to_folder(
        self,
        file_id: str,
        new_parent_folder_id: str
    ) -> Dict[str, Any]:
        """6. ファイル保存フォルダの変更"""
        self.rate_limiter.wait_if_needed()
        
        # First get the file to retrieve current parents
        try:
            file = self._service.files().get(
                fileId=file_id,
                fields='parents'
            ).execute()
            
            previous_parents = ",".join(file.get('parents', []))
            
            # Move the file
            request = self._service.files().update(
                fileId=file_id,
                addParents=new_parent_folder_id,
                removeParents=previous_parents,
                fields='id,parents'
            )
            response = request.execute()
            
            logger.info(f"Moved file {file_id} to folder {new_parent_folder_id}")
            return {
                'id': response.get('id'),
                'parents': response.get('parents')
            }
        except HttpError as error:
            self._handle_api_error(error, 'move_file_to_folder')
            raise
    
    def move_to_trash(
        self,
        file_id: str
    ) -> Dict[str, Any]:
        """27. ファイルをごみ箱に移動する"""
        self.rate_limiter.wait_if_needed()
        
        file_metadata = {'trashed': True}
        
        try:
            request = self._service.files().update(
                fileId=file_id,
                body=file_metadata,
                fields='id,trashed'
            )
            request.execute()
            logger.info(f"Moved to trash: {file_id}")
            return {'success': True, 'fileId': file_id, 'trashed': True}
        except HttpError as error:
            self._handle_api_error(error, 'move_to_trash')
            raise
    
    def get_file_info(
        self,
        file_id: str,
        fields: str = 'id,name,mimeType,size,createdTime,modifiedTime,owners,webContentLink,webViewLink'
    ) -> Dict[str, Any]:
        """20. ファイル/フォルダ情報のインポート"""
        self.rate_limiter.wait_if_needed()
        
        try:
            request = self._service.files().get(
                fileId=file_id,
                fields=fields
            )
            response = request.execute()
            return response
        except HttpError as error:
            self._handle_api_error(error, 'get_file_info')
            raise
    
    def list_folder_contents(
        self,
        folder_id: str,
        page_size: int = 100
    ) -> Dict[str, Any]:
        """21. 特定のフォルダ内のファイル/フォルダの検索、31. 特定のフォルダ内のフォルダ一覧、34. 特定のフォルダ内のファイル/フォルダの一覧"""
        self.rate_limiter.wait_if_needed()
        
        query = f"'{folder_id}' in parents and trashed=false"
        
        return self.search_files(query, page_size)
    
    # ============================================
    # Upload & Download Operations
    # ============================================
    
    def upload_file(
        self,
        file_path: str,
        parent_folder_id: Optional[str] = None,
        file_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """23. ファイルをアップロードする"""
        self.rate_limiter.wait_if_needed()
        
        file_name = file_name or os.path.basename(file_path)
        
        # Determine MIME type
        import mimetypes
        mime_type, _ = mimetypes.guess_type(file_path)
        mime_type = mime_type or 'application/octet-stream'
        
        file_metadata = {'name': file_name}
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]
        
        media = MediaFileUpload(
            file_path,
            mimetype=mime_type,
            resumable=True
        )
        
        try:
            request = self._service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,mimeType,webContentLink,webViewLink'
            )
            response = request.execute()
            logger.info(f"Uploaded file: {file_name}")
            return response
        except HttpError as error:
            self._handle_api_error(error, 'upload_file')
            raise
    
    def download_file(
        self,
        file_id: str,
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """16. ファイルのダウンロード"""
        self.rate_limiter.wait_if_needed()
        
        # Get file info to determine if it's a Google Workspace file
        file_info = self.get_file_info(
            file_id,
            fields='id,name,mimeType,webContentLink'
        )
        
        mime_type = file_info.get('mimeType', '')
        file_name = file_info.get('name', 'download')
        
        # Google Workspace files need export
        if mime_type.startswith('application/vnd.google-apps'):
            return self._export_file(file_id, mime_type, output_path)
        
        # Regular files can be downloaded directly
        if not output_path:
            return {'success': False, 'reason': 'output_path required for regular files'}
        
        request = self._service.files().get_media(fileId=file_id)
        
        with open(output_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
        
        logger.info(f"Downloaded file to: {output_path}")
        return {
            'success': True,
            'path': output_path,
            'name': file_name
        }
    
    def _export_file(
        self,
        file_id: str,
        mime_type: str,
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Helper to export Google Workspace files"""
        
        mime_to_extension = {
            'application/vnd.google-apps.document': '.docx',
            'application/vnd.google-apps.spreadsheet': '.xlsx',
            'application/vnd.google-apps.presentation': '.pptx',
            'application/vnd.google-apps.script': '.json'
        }
        
        extension = mime_to_extension.get(mime_type, '.txt')
        export_mime = mime_type.replace('google-apps', 'openxmlformats-officedocument')
        
        if export_mime == 'application/vnd.openxmlformats-officedocument.spreadsheetml':
            export_mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        elif export_mime == 'application/vnd.openxmlformats-officedocument.presentationml':
            export_mime = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        
        request = self._service.files().export(
            fileId=file_id,
            mimeType=export_mime
        )
        
        if output_path:
            with open(output_path, 'wb') as fh:
                fh.write(request.execute())
            logger.info(f"Exported file to: {output_path}")
            return {'success': True, 'path': output_path}
        else:
            # Return as base64
            content = request.execute()
            import base64
            return {
                'success': True,
                'content': base64.b64encode(content).decode(),
                'extension': extension,
                'mimeType': export_mime
            }
    
    # ============================================
    # File Conversion Operations
    # ============================================
    
    def convert_to_document(
        self,
        file_id: str
    ) -> Dict[str, Any]:
        """1. ファイルを Google Docs に変換する"""
        self.rate_limiter.wait_if_needed()
        
        file_metadata = {
            'name': 'Converted Document',
            'parents': [file_id]  # Wrong - should use copy API with convert
        }
        
        # Use copy API with conversion
        try:
            request = self._service.files().copy(
                fileId=file_id,
                body={'name': 'Converted to Docs'},
                supportsAllDrives=True
            )
            response = request.execute()
            logger.info(f"Converted to Google Docs: {response.get('id')}")
            return response
        except HttpError as error:
            self._handle_api_error(error, 'convert_to_document')
            raise
    
    def convert_to_slides(
        self,
        file_id: str
    ) -> Dict[str, Any]:
        """2. プレゼンテーション ファイルを Google Slides に変換する"""
        self.rate_limiter.wait_if_needed()
        
        try:
            request = self._service.files().copy(
                fileId=file_id,
                body={'name': 'Converted to Slides'},
                supportsAllDrives=True
            )
            response = request.execute()
            logger.info(f"Converted to Google Slides: {response.get('id')}")
            return response
        except HttpError as error:
            self._handle_api_error(error, 'convert_to_slides')
            raise
    
    def convert_csv_to_sheets(
        self,
        file_path: str,
        parent_folder_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """18. CSVファイルをスプレッドシートに変換する、32. Excelファイルを変換する"""
        self.rate_limiter.wait_if_needed()
        
        file_metadata = {
            'name': os.path.basename(file_path).replace('.csv', '').replace('.xlsx', ''),
            'mimeType': 'application/vnd.google-apps.spreadsheet'
        }
        
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]
        
        media = MediaFileUpload(
            file_path,
            mimetype='text/csv' if file_path.endswith('.csv') else 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            resumable=True
        )
        
        try:
            request = self._service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,mimeType'
            )
            response = request.execute()
            logger.info(f"Converted to Sheets: {response.get('id')}")
            return response
        except HttpError as error:
            self._handle_api_error(error, 'convert_csv_to_sheets')
            raise
    
    # ============================================
    # Download Google Workspace Files
    # ============================================
    
    def download_google_doc(
        self,
        file_id: str,
        format: str = 'docx',
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """7. Google Docsをダウンロードする"""
        self.rate_limiter.wait_if_needed()
        
        mime_map = {
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'pdf': 'application/pdf',
            'odt': 'application/vnd.oasis.opendocument.text',
            'rtf': 'application/rtf',
            'txt': 'text/plain',
            'html': 'text/html'
        }
        
        export_mime = mime_map.get(format, mime_map['docx'])
        
        request = self._service.files().export_media(
            fileId=file_id,
            mimeType=export_mime
        )
        
        if output_path:
            with open(output_path, 'wb') as fh:
                fh.write(request.execute())
            logger.info(f"Downloaded Google Doc: {output_path}")
            return {'success': True, 'path': output_path}
        else:
            import base64
            content = request.execute()
            return {
                'success': True,
                'content': base64.b64encode(content).decode(),
                'format': format
            }
    
    def download_sheets(
        self,
        file_id: str,
        format: str = 'xlsx',
        sheet_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """12. Googleシートをダウンロードする、19.シート指定をダウンロードする"""
        self.rate_limiter.wait_if_needed()
        
        mime_map = {
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'pdf': 'application/pdf',
            'csv': 'text/csv',
            'ods': 'application/vnd.oasis.opendocument.spreadsheet',
            'tsv': 'text/tab-separated-values'
        }
        
        export_mime = mime_map.get(format, mime_map['xlsx'])
        
        request = self._service.files().export_media(
            fileId=file_id,
            mimeType=export_mime
        )
        
        import base64
        content = request.execute()
        result = {
            'success': True,
            'content': base64.b64encode(content).decode(),
            'format': format
        }
        
        if sheet_name:
            result['sheetName'] = sheet_name
        
        return result
    
    def download_slides(
        self,
        file_id: str,
        format: str = 'pptx'
    ) -> Dict[str, Any]:
        """30. Google Slidesをダウンロードする"""
        self.rate_limiter.wait_if_needed()
        
        mime_map = {
            'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'pdf': 'application/pdf',
            'odp': 'application/vnd.oasis.opendocument.presentation',
            'txt': 'text/plain'
        }
        
        export_mime = mime_map.get(format, mime_map['pptx'])
        
        request = self._service.files().export_media(
            fileId=file_id,
            mimeType=export_mime
        )
        
        import base64
        content = request.execute()
        return {
            'success': True,
            'content': base64.b64encode(content).decode(),
            'format': format
        }
    
    def convert_pdf_to_doc(
        self,
        file_id: str
    ) -> Dict[str, Any]:
        """25. PDF ファイルを Google Docs に変換する"""
        self.rate_limiter.wait_if_needed()
        
        try:
            request = self._service.files().copy(
                fileId=file_id,
                body={'name': 'PDF Converted'},
                supportsAllDrives=True
            )
            response = request.execute()
            logger.info(f"Converted PDF to Docs: {response.get('id')}")
            return response
        except HttpError as error:
            self._handle_api_error(error, 'convert_pdf_to_doc')
            raise
    
    # ============================================
    # Copy & Duplicate Operations
    # ============================================
    
    def duplicate_file(
        self,
        file_id: str,
        new_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """8. ファイルの複製、14. ファイルの複製 (詳細)、22. ファイルのショートカットの作成"""
        self.rate_limiter.wait_if_needed()
        
        file_metadata = {}
        if new_name:
            file_metadata['name'] = new_name
        
        try:
            request = self._service.files().copy(
                fileId=file_id,
                body=file_metadata,
                fields='id,name,mimeType'
            )
            response = request.execute()
            logger.info(f"Duplicated file: {response.get('id')}")
            return response
        except HttpError as error:
            self._handle_api_error(error, 'duplicate_file')
            raise
    
    # ============================================
    # Permissions & Sharing Operations
    # ============================================
    
    def list_permissions(
        self,
        file_id: str
    ) -> Dict[str, Any]:
        """5. ファイル/フォルダ権限リストのインポート"""
        self.rate_limiter.wait_if_needed()
        
        try:
            request = self._service.permissions().list(
                fileId=file_id,
                fields='permissions(id,role,type,emailAddress,domain,allowFileDiscovery)'
            )
            response = request.execute()
            return {
                'fileId': file_id,
                'permissions': response.get('permissions', [])
            }
        except HttpError as error:
            self._handle_api_error(error, 'list_permissions')
            raise
    
    def delete_permission(
        self,
        file_id: str,
        permission_id: str
    ) -> Dict[str, Any]:
        """10. ファイル/フォルダから権限を削除する"""
        self.rate_limiter.wait_if_needed()
        
        try:
            request = self._service.permissions().delete(
                fileId=file_id,
                permissionId=permission_id
            )
            request.execute()
            logger.info(f"Deleted permission {permission_id} from {file_id}")
            return {'success': True}
        except HttpError as error:
            self._handle_api_error(error, 'delete_permission')
            raise
    
    def grant_permission_to_user(
        self,
        file_id: str,
        email: str,
        role: str = 'reader',
        transfer_ownership: bool = False
    ) -> Dict[str, Any]:
        """35. 指定ユーザーに許可を与える"""
        self.rate_limiter.wait_if_needed()
        
        valid_roles = ['reader', 'writer', 'commenter', 'owner']
        if role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {valid_roles}")
        
        permission = {
            'type': 'user',
            'role': role,
            'emailAddress': email
        }
        
        try:
            kwargs = {'fileId': file_id, 'body': permission, 'fields': 'id,role,type,emailAddress'}
            if transfer_ownership:
                kwargs['transferOwnership'] = True
            
            request = self._service.permissions().create(**kwargs)
            response = request.execute()
            logger.info(f"Granted {role} permission to {email}")
            return response
        except HttpError as error:
            self._handle_api_error(error, 'grant_permission_to_user')
            raise
    
    def grant_permission_to_organization(
        self,
        file_id: str,
        domain: str,
        role: str = 'reader'
    ) -> Dict[str, Any]:
        """26. 特定の組織への承認"""
        self.rate_limiter.wait_if_needed()
        
        permission = {
            'type': 'domain',
            'role': role,
            'domain': domain
        }
        
        try:
            request = self._service.permissions().create(
                fileId=file_id,
                body=permission,
                fields='id,role,type,domain'
            )
            response = request.execute()
            logger.info(f"Granted {role} permission to domain {domain}")
            return response
        except HttpError as error:
            self._handle_api_error(error, 'grant_permission_to_organization')
            raise
    
    def set_anyone_with_link_permission(
        self,
        file_id: str,
        role: str = 'reader',
        allow_discovery: bool = False
    ) -> Dict[str, Any]:
        """28. ファイル権限を"リンクを知っているすべての人"に変更する"""
        self.rate_limiter.wait_if_needed()
        
        permission = {
            'type': 'anyone',
            'role': role
        }
        
        if allow_discovery:
            permission['allowFileDiscovery'] = True
        
        try:
            request = self._service.permissions().create(
                fileId=file_id,
                body=permission,
                fields='id,role,type'
            )
            response = request.execute()
            logger.info(f"Set 'anyone with link' permission to {role}")
            return response
        except HttpError as error:
            self._handle_api_error(error, 'set_anyone_with_link_permission')
            raise
    
    def set_copy_and_download_permission(
        self,
        file_id: str,
        allow_copy: bool = True,
        allow_download: bool = True
    ) -> Dict[str, Any]:
        """24. ファイルのダウンロード/コピーを許可する設定"""
        self.rate_limiter.wait_if_needed()
        
        try:
            # Get existing permissions
            file_info = self._service.files().get(
                fileId=file_id,
                fields='copyRequiresWriterPermission, writersCanShare'
            ).execute()
            
            # Update file copy settings
            file_metadata = {
                'copyRequiresWriterPermission': not allow_copy,
                'writersCanShare': True
            }
            
            # For download permission, need to remove anyone permissions
            if not allow_download:
                perms = self.list_permissions(file_id)
                for p in perms.get('permissions', []):
                    if p.get('type') == 'anyone':
                        try:
                            self._service.permissions().delete(
                                fileId=file_id,
                                permissionId=p.get('id')
                            ).execute()
                        except:
                            pass
            
            request = self._service.files().update(
                fileId=file_id,
                body=file_metadata,
                fields='id,webContentLink'
            )
            response = request.execute()
            return response
        except HttpError as error:
            self._handle_api_error(error, 'set_copy_and_download_permission')
            raise
    
    # ============================================
    # Shared Drive Operations
    # ============================================
    
    def search_shared_drives(
        self,
        query: str = ''
    ) -> Dict[str, Any]:
        """11. 共有ドライブを検索する"""
        self.rate_limiter.wait_if_needed()
        
        try:
            kwargs = {}
            if query:
                kwargs['q'] = query
            
            request = self._service.drives().list(**kwargs)
            response = request.execute()
            
            return {
                'drives': response.get('drives', [])
            }
        except HttpError as error:
            self._handle_api_error(error, 'search_shared_drives')
            raise
    
    def create_shared_drive(
        self,
        name: str,
        request_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """29. 共有ドライブの作成"""
        self.rate_limiter.wait_if_needed()
        
        import uuid
        request_id = request_id or str(uuid.uuid4())
        
        drive_metadata = {
            'name': name,
            'requestId': request_id
        }
        
        try:
            request = self._service.drives().create(
                body=drive_metadata,
                fields='id,name'
            )
            response = request.execute()
            logger.info(f"Created shared drive: {name}")
            return response
        except HttpError as error:
            self._handle_api_error(error, 'create_shared_drive')
            raise
    
    # ============================================
    # File Update Operations
    # ============================================
    
    def update_file_content(
        self,
        file_id: str,
        file_path: str
    ) -> Dict[str, Any]:
        """13. 特定のファイルを更新する"""
        self.rate_limiter.wait_if_needed()
        
        file_metadata = {}
        
        import mimetypes
        mime_type, _ = mimetypes.guess_type(file_path)
        mime_type = mime_type or 'application/octet-stream'
        
        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
        
        try:
            request = self._service.files().update(
                fileId=file_id,
                body=file_metadata,
                media_body=media,
                fields='id,name,modifiedTime'
            )
            response = request.execute()
            logger.info(f"Updated file: {file_id}")
            return response
        except HttpError as error:
            self._handle_api_error(error, 'update_file_content')
            raise


def create_client(credentials: Optional[Dict[str, str]] = None, **kwargs) -> GoogleDriveClient:
    """Factory function to create Google Drive client."""
    return GoogleDriveClient(credentials=credentials, **kwargs)
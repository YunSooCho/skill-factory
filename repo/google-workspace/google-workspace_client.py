"""
Google Workspace Admin SDK Client

This module provides a comprehensive client for interacting with Google Workspace Admin SDK.
It supports 13 API actions for user and group management, and 2 webhook triggers.

Author: Yoom Integration
Version: 1.0.0
"""

import os
import logging
from typing import Optional, Dict, List, Any, Union
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
    """Simple rate limiter for Google Workspace API calls."""
    
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


class GoogleWorkspaceClient:
    """
    Google Workspace Admin SDK Client
    
    Provides comprehensive access to Google Workspace administrative functionality including:
    - User management (create, update, delete, suspend)
    - Group management (create, list, add/remove members)
    - Directory API operations
    """
    
    # OAuth 2.0 scopes for Admin SDK
    SCOPES = [
        'https://www.googleapis.com/auth/admin.directory.user',
        'https://www.googleapis.com/auth/admin.directory.group',
        'https://www.googleapis.com/auth/admin.directory.group.member'
    ]
    
    def __init__(
        self,
        domain: str,
        credentials: Optional[Dict[str, str]] = None,
        token_file: Optional[str] = None,
        credentials_file: Optional[str] = None,
        admin_email: Optional[str] = None
    ):
        """
        Initialize Google Workspace client.
        
        Args:
            domain: The Google Workspace domain (e.g., 'example.com')
            credentials: OAuth credentials dict with access_token, refresh_token, etc.
            token_file: Path to token file for persistent authentication
            credentials_file: Path to OAuth 2.0 client secrets JSON file
            admin_email: Email address of the admin user (for service accounts)
        
        Raises:
            ImportError: If google-api-python-client is not installed
            ValueError: If authentication fails or domain is not provided
        """
        if not GOOGLE_API_AVAILABLE:
            raise ImportError(
                "google-api-python-client is required. "
                "Install it with: pip install google-api-python-client google-auth-oauthlib"
            )
        
        if not domain:
            raise ValueError("Domain is required")
        
        self.domain = domain
        self.rate_limiter = RateLimiter(max_calls=100, period=100)
        self._service_user = None
        self._service_group = None
        self._credentials = None
        
        # Authenticate
        if credentials:
            self._credentials = self._credentials_from_dict(credentials)
        elif token_file and os.path.exists(token_file):
            self._credentials = self._load_token(token_file)
        elif credentials_file:
            self._credentials = self._authenticate_local(credentials_file, admin_email)
        
        if not self._credentials:
            raise ValueError("Authentication failed. Provide credentials, token_file, or credentials_file.")
        
        # Build services
        self._service_user = build('admin', 'directory_v1', credentials=self._credentials)
        self._service_group = build('admin', 'directory_v1', credentials=self._credentials)
        
        logger.info(f"Google Workspace client initialized for domain: {domain}")
    
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
    
    def _authenticate_local(self, credentials_file: str, admin_email: Optional[str] = None) -> Credentials:
        """
        Authenticate using OAuth 2.0 flow with local callback.
        
        Args:
            credentials_file: Path to OAuth 2.0 client secrets JSON file
            admin_email: Email address of the admin user (for service accounts)
        """
        creds = None
        token_file = credentials_file.replace('.json', '_tokens.pickle')
        
        # Load existing token
        if os.path.exists(token_file):
            import pickle
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
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
        elif error.resp.status == 409:
            logger.error(f"Resource already exists for {operation}: {error}")
        elif error.resp.status == 400:
            logger.error(f"Bad request for {operation}: {error}")
        elif error.resp.status == 429:
            logger.warning(f"Rate limit exceeded for {operation}, consider adding delay")
        else:
            logger.error(f"API error in {operation}: {error}")
        raise
    
    # ============================================
    # User Management (6 actions)
    # ============================================
    
    def create_user(
        self,
        primary_email: str,
        given_name: str,
        family_name: str,
        password: str,
        suspended: bool = False,
        org_unit_path: str = '/'
    ) -> Dict[str, Any]:
        """
        7. 새로운 사용자를 추가하기 (Add New User)
        
        Creates a new user in Google Workspace.
        
        Args:
            primary_email: Primary email address (e.g., 'user@example.com')
            given_name: First name
            family_name: Last name
            password: Initial password
            suspended: Whether the user is suspended (default: False)
            org_unit_path: Organizational unit path (default: '/')
        
        Returns:
            Dictionary with user details including id, primaryEmail, name
        
        Raises:
            HttpError: If user already exists or validation fails
        """
        self.rate_limiter.wait_if_needed()
        
        user_body = {
            'primaryEmail': primary_email,
            'name': {
                'givenName': given_name,
                'familyName': family_name
            },
            'password': password,
            'suspended': suspended,
            'orgUnitPath': org_unit_path,
            'changePasswordAtNextLogin': False
        }
        
        try:
            request = self._service_user.users().insert(
                body=user_body,
                domain=self.domain
            )
            response = request.execute()
            
            logger.info(f"Created user: {primary_email}")
            return {
                'id': response.get('id'),
                'primaryEmail': response.get('primaryEmail'),
                'name': response.get('name'),
                'suspended': response.get('suspended'),
                'orgUnitPath': response.get('orgUnitPath')
            }
        except HttpError as error:
            self._handle_api_error(error, 'create_user')
            raise
    
    def delete_user(
        self,
        user_key: str
    ) -> Dict[str, Any]:
        """
        1. 사용자를 삭제하기 (Delete User)
        
        Deletes a user from Google Workspace.
        
        Args:
            user_key: User email or primary email address
        
        Returns:
            Confirmation dictionary
        
        Raises:
            HttpError: If user not found or permission denied
        """
        self.rate_limiter.wait_if_needed()
        
        try:
            request = self._service_user.users().delete(userKey=user_key)
            request.execute()
            
            logger.info(f"Deleted user: {user_key}")
            return {'success': True, 'userKey': user_key}
        except HttpError as error:
            self._handle_api_error(error, 'delete_user')
            raise
    
    def suspend_user(
        self,
        user_key: str
    ) -> Dict[str, Any]:
        """
        2. 사용자를 중지하기 (Suspend User)
        
        Suspends a user account.
        
        Args:
            user_key: User email or primary email address
        
        Returns:
            Confirmation dictionary
        
        Raises:
            HttpError: If user not found
        """
        self.rate_limiter.wait_if_needed()
        
        user_body = {
            'suspended': True
        }
        
        try:
            request = self._service_user.users().update(
                userKey=user_key,
                body=user_body
            )
            request.execute()
            
            logger.info(f"Suspended user: {user_key}")
            return {'success': True, 'userKey': user_key, 'suspended': True}
        except HttpError as error:
            self._handle_api_error(error, 'suspend_user')
            raise
    
    def require_password_change(
        self,
        user_key: str
    ) -> Dict[str, Any]:
        """
        3. 사용자에게 비밀번호 변경 요구하기 (Require Password Change)
        
        Forces the user to change password at next login.
        
        Args:
            user_key: User email or primary email address
        
        Returns:
            Confirmation dictionary
        
        Raises:
            HttpError: If user not found
        """
        self.rate_limiter.wait_if_needed()
        
        user_body = {
            'changePasswordAtNextLogin': True
        }
        
        try:
            request = self._service_user.users().update(
                userKey=user_key,
                body=user_body
            )
            request.execute()
            
            logger.info(f"Required password change for user: {user_key}")
            return {'success': True, 'userKey': user_key, 'changePasswordAtNextLogin': True}
        except HttpError as error:
            self._handle_api_error(error, 'require_password_change')
            raise
    
    def search_user(
        self,
        query: str,
        max_results: int = 100
    ) -> Dict[str, Any]:
        """
        5. 사용자 검색하기 (Search User)
        
        Searches for users matching the query.
        
        Args:
            query: Search query (e.g., 'email:john@example.com', 'name:John', 'orgUnitPath:/Users')
            max_results: Maximum number of results to return
        
        Returns:
            Dictionary with list of matching users
        
        Raises:
            HttpError: If query is invalid
        """
        self.rate_limiter.wait_if_needed()
        
        try:
            request = self._service_user.users().list(
                domain=self.domain,
                query=query,
                maxResults=max_results
            )
            response = request.execute()
            
            users = response.get('users', [])
            logger.info(f"Found {len(users)} users matching query: {query}")
            
            return {
                'users': [
                    {
                        'id': user.get('id'),
                        'primaryEmail': user.get('primaryEmail'),
                        'name': user.get('name'),
                        'suspended': user.get('suspended'),
                        'orgUnitPath': user.get('orgUnitPath')
                    }
                    for user in users
                ],
                'total': len(users)
            }
        except HttpError as error:
            self._handle_api_error(error, 'search_user')
            raise
    
    def list_users(
        self,
        max_results: int = 100,
        customer: str = 'my_customer',
        query: Optional[str] = None,
        page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        13. 사용자 목록 가져오기 (Get User List)
        
        Retrieves a paginated list of users in the domain.
        
        Args:
            max_results: Maximum number of results to return
            customer: Customer ID (default: 'my_customer')
            query: Optional search query
            page_token: Pagination token for next page
        
        Returns:
            Dictionary with users list and pagination info
        """
        self.rate_limiter.wait_if_needed()
        
        kwargs = {
            'domain': self.domain,
            'maxResults': max_results,
            'customer': customer
        }
        
        if query:
            kwargs['query'] = query
        if page_token:
            kwargs['pageToken'] = page_token
        
        try:
            request = self._service_user.users().list(**kwargs)
            response = request.execute()
            
            users = response.get('users', [])
            
            return {
                'users': [
                    {
                        'id': user.get('id'),
                        'primaryEmail': user.get('primaryEmail'),
                        'name': user.get('name'),
                        'suspended': user.get('suspended'),
                        'orgUnitPath': user.get('orgUnitPath'),
                        'isAdmin': user.get('isAdmin', False)
                    }
                    for user in users
                ],
                'total': len(users),
                'nextPageToken': response.get('nextPageToken')
            }
        except HttpError as error:
            self._handle_api_error(error, 'list_users')
            raise
    
    def update_user(
        self,
        user_key: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        11. 사용자 정보 업데이트하기 (Update User Information)
        
        Updates user information.
        
        Args:
            user_key: User email or primary email address
            **kwargs: Fields to update (givenName, familyName, suspended, orgUnitPath, etc.)
        
        Returns:
            Dictionary with updated user details
        
        Raises:
            HttpError: If user not found or validation fails
        """
        self.rate_limiter.wait_if_needed()
        
        # Get current user info first
        try:
            request = self._service_user.users().get(userKey=user_key)
            current = request.execute()
        except HttpError as error:
            if error.resp.status == 404:
                logger.error(f"User not found: {user_key}")
                raise ValueError(f"User not found: {user_key}")
            raise
        
        # Build update body with only changed fields
        update_body = {}
        
        # Handle name fields
        if 'givenName' in kwargs or 'familyName' in kwargs:
            current_name = current.get('name', {})
            update_body['name'] = {
                'givenName': kwargs.get('givenName', current_name.get('givenName')),
                'familyName': kwargs.get('familyName', current_name.get('familyName'))
            }
        
        # Handle other fields
        for field in ['suspended', 'suspensionReason', 'orgUnitPath', 'primaryEmail']:
            if field in kwargs:
                update_body[field] = kwargs[field]
        
        try:
            request = self._service_user.users().update(
                userKey=user_key,
                body=update_body
            )
            response = request.execute()
            
            logger.info(f"Updated user: {user_key}")
            return {
                'id': response.get('id'),
                'primaryEmail': response.get('primaryEmail'),
                'name': response.get('name'),
                'suspended': response.get('suspended'),
                'orgUnitPath': response.get('orgUnitPath')
            }
        except HttpError as error:
            self._handle_api_error(error, 'update_user')
            raise
    
    # ============================================
    # Group Management (7 actions)
    # ============================================
    
    def create_group(
        self,
        email: str,
        name: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        12. 그룹 생성하기 (Create Group)
        
        Creates a new group in Google Workspace.
        
        Args:
            email: Group email address
            name: Group display name
            description: Optional group description
        
        Returns:
            Dictionary with group details
        
        Raises:
            HttpError: If group already exists or validation fails
        """
        self.rate_limiter.wait_if_needed()
        
        group_body = {
            'email': email,
            'name': name
        }
        
        if description:
            group_body['description'] = description
        
        try:
            request = self._service_group.groups().insert(
                body=group_body,
                domain=self.domain
            )
            response = request.execute()
            
            logger.info(f"Created group: {email}")
            return {
                'id': response.get('id'),
                'email': response.get('email'),
                'name': response.get('name'),
                'description': response.get('description'),
                'directMembersCount': response.get('directMembersCount', 0)
            }
        except HttpError as error:
            self._handle_api_error(error, 'create_group')
            raise
    
    def list_groups(
        self,
        max_results: int = 100,
        customer: str = 'my_customer',
        page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        9. 그룹 목록 가져오기 (Get Group List)
        
        Retrieves a paginated list of groups.
        
        Args:
            max_results: Maximum number of results to return
            customer: Customer ID (default: 'my_customer')
            page_token: Pagination token for next page
        
        Returns:
            Dictionary with groups list and pagination info
        """
        self.rate_limiter.wait_if_needed()
        
        kwargs = {
            'domain': self.domain,
            'maxResults': max_results,
            'customer': customer
        }
        
        if page_token:
            kwargs['pageToken'] = page_token
        
        try:
            request = self._service_group.groups().list(**kwargs)
            response = request.execute()
            
            groups = response.get('groups', [])
            
            return {
                'groups': [
                    {
                        'id': group.get('id'),
                        'email': group.get('email'),
                        'name': group.get('name'),
                        'description': group.get('description'),
                        'directMembersCount': group.get('directMembersCount', 0)
                    }
                    for group in groups
                ],
                'total': len(groups),
                'nextPageToken': response.get('nextPageToken')
            }
        except HttpError as error:
            self._handle_api_error(error, 'list_groups')
            raise
    
    def search_groups(
        self,
        query: str,
        max_results: int = 100
    ) -> Dict[str, Any]:
        """
        6. 그룹 검색하기 (Search Groups)
        
        Searches for groups matching the query.
        
        Args:
            query: Search query (e.g., 'email:*@example.com', 'name:Team')
            max_results: Maximum number of results to return
        
        Returns:
            Dictionary with list of matching groups
        """
        self.rate_limiter.wait_if_needed()
        
        try:
            request = self._service_group.groups().list(
                domain=self.domain,
                query=query,
                maxResults=max_results
            )
            response = request.execute()
            
            groups = response.get('groups', [])
            logger.info(f"Found {len(groups)} groups matching query: {query}")
            
            return {
                'groups': [
                    {
                        'id': group.get('id'),
                        'email': group.get('email'),
                        'name': group.get('name'),
                        'description': group.get('description'),
                        'directMembersCount': group.get('directMembersCount', 0)
                    }
                    for group in groups
                ],
                'total': len(groups)
            }
        except HttpError as error:
            self._handle_api_error(error, 'search_groups')
            raise
    
    def add_member_to_group(
        self,
        group_key: str,
        member_email: str,
        role: str = 'MEMBER'
    ) -> Dict[str, Any]:
        """
        10. 그룹에 멤버 추가하기 (Add Member to Group)
        
        Adds a member to a group.
        
        Args:
            group_key: Group email or id
            member_email: Email of member to add
            role: Member role (MEMBER, MANAGER, OWNER)
        
        Returns:
            Dictionary with member details
        
        Raises:
            HttpError: If group or user not found
        """
        self.rate_limiter.wait_if_needed()
        
        member_body = {
            'email': member_email,
            'role': role
        }
        
        try:
            request = self._service_group.members().insert(
                groupKey=group_key,
                body=member_body
            )
            response = request.execute()
            
            logger.info(f"Added member {member_email} to group {group_key}")
            return {
                'id': response.get('id'),
                'email': response.get('email'),
                'role': response.get('role'),
                'status': response.get('status'),
                'type': response.get('type')
            }
        except HttpError as error:
            self._handle_api_error(error, 'add_member_to_group')
            raise
    
    def remove_member_from_group(
        self,
        group_key: str,
        member_key: str
    ) -> Dict[str, Any]:
        """
        4. 그룹에서 멤버 삭제하기 (Remove Member from Group)
        
        Removes a member from a group.
        
        Args:
            group_key: Group email or id
            member_key: Member email or id
        
        Returns:
            Confirmation dictionary
        
        Raises:
            HttpError: If group or member not found
        """
        self.rate_limiter.wait_if_needed()
        
        try:
            request = self._service_group.members().delete(
                groupKey=group_key,
                memberKey=member_key
            )
            request.execute()
            
            logger.info(f"Removed member {member_key} from group {group_key}")
            return {'success': True, 'groupKey': group_key, 'memberKey': member_key}
        except HttpError as error:
            self._handle_api_error(error, 'remove_member_from_group')
            raise
    
    def list_group_members(
        self,
        group_key: str,
        max_results: int = 100,
        roles: Optional[List[str]] = None,
        page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        8. 그룹의 멤버 목록 가져오기 (Get Group Member List)
        
        Retrieves a paginated list of group members.
        
        Args:
            group_key: Group email or id
            max_results: Maximum number of results to return
            roles: Filter by roles (e.g., ['MEMBER', 'MANAGER'])
            page_token: Pagination token for next page
        
        Returns:
            Dictionary with members list and pagination info
        """
        self.rate_limiter.wait_if_needed()
        
        kwargs = {
            'groupKey': group_key,
            'maxResults': max_results
        }
        
        if roles:
            kwargs['roles'] = ','.join(roles)
        if page_token:
            kwargs['pageToken'] = page_token
        
        try:
            request = self._service_group.members().list(**kwargs)
            response = request.execute()
            
            members = response.get('members', [])
            
            return {
                'groupKey': group_key,
                'members': [
                    {
                        'id': member.get('id'),
                        'email': member.get('email'),
                        'role': member.get('role'),
                        'status': member.get('status'),
                        'type': member.get('type')
                    }
                    for member in members
                ],
                'total': len(members),
                'nextPageToken': response.get('nextPageToken')
            }
        except HttpError as error:
            self._handle_api_error(error, 'list_group_members')
            raise


# Webhook Handlers (for Triggers)
class GoogleWorkspaceWebhooks:
    """
    Webhook handlers for Google Workspace triggers.
    
    Google Workspace provides notifications via Pub/Sub for events.
    """
    
    @staticmethod
    def setup_user_events_subscription(
        project_id: str,
        topic_name: str,
        payload_format: str = 'JSON_API_V1'
    ) -> Dict[str, Any]:
        """
        Sets up a Pub/Sub subscription for user events.
        
        Args:
            project_id: Google Cloud project ID
            topic_name: Pub/Sub topic name
            payload_format: Payload format (JSON_API_V1, ...)
        
        Returns:
            Configuration details for the subscription
        """
        return {
            'type': 'Google Cloud Pub/Sub',
            'subscription_type': 'user_events',
            'setup_required': True,
            'instructions': [
                '1. Enable Pub/Sub API in Google Cloud Console',
                '2. Create a Pub/Sub topic',
                '3. Create user watch using Admin SDK API',
                '4. Subscribe your webhook endpoint to the topic'
            ],
            'api_endpoint': f'https://admin.googleapis.com/admin/directory/v1/users/watch',
            'fields': ['id', 'primaryEmail', 'name', 'suspended', 'orgUnitPath']
        }
    
    @staticmethod
    def setup_group_events_subscription(
        project_id: str,
        topic_name: str
    ) -> Dict[str, Any]:
        """
        Sets up a Pub/Sub subscription for group events.
        
        Args:
            project_id: Google Cloud project ID
            topic_name: Pub/Sub topic name
        
        Returns:
            Configuration details for the subscription
        """
        return {
            'type': 'Google Cloud Pub/Sub',
            'subscription_type': 'group_events',
            'setup_required': True,
            'instructions': [
                '1. Enable Pub/Sub API in Google Cloud Console',
                '2. Create a Pub/Sub topic',
                '3. Create group watch using Admin SDK API',
                '4. Subscribe your webhook endpoint to the topic'
            ],
            'api_endpoint': f'https://admin.googleapis.com/admin/directory/v1/groups/watch'
        }
    
    @staticmethod
    def handle_user_created_webhook(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handler for 'User Registered' trigger.
        
        Args:
            payload: Webhook payload
        
        Returns:
            Processed data
        """
        return {
            'trigger_type': 'user_created',
            'data': payload,
            'processed_at': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def handle_user_updated_webhook(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handler for 'User Updated' trigger.
        
        Args:
            payload: Webhook payload
        
        Returns:
            Processed data
        """
        return {
            'trigger_type': 'user_updated',
            'data': payload,
            'processed_at': datetime.utcnow().isoformat()
        }


# Convenience function for quick access
def create_client(
    domain: str,
    credentials: Optional[Dict[str, str]] = None,
    **kwargs
) -> GoogleWorkspaceClient:
    """Factory function to create Google Workspace client."""
    return GoogleWorkspaceClient(domain=domain, credentials=credentials, **kwargs)
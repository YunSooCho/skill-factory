"""
Canny Feature Request Platform API Client

This module provides a Python client for interacting with the Canny
feature request platform API.
"""

import requests
from typing import Dict, List, Optional, Any


class CannyClient:
    """
    Client for Canny Feature Request Platform API.

    Canny provides:
    - Feature request collection
    - Feedback management
    - User voting
    - Status tracking
    - Roadmap management
    - Activity tracking
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://canny.io/api/v1",
        timeout: int = 30
    ):
        """
        Initialize the Canny client.

        Args:
            api_key: Your Canny API key
            base_url: API base URL (default: https://canny.io/api/v1)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.params = {'apiKey': api_key}

    def _request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an authenticated request to the Canny API.

        Args:
            endpoint: API endpoint
            params: Query parameters
            data: Request body data

        Returns:
            Response JSON
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(
            url,
            params=params,
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def list_posts(
        self,
        board_id: Optional[str] = None,
        limit: int = 100,
        skip: int = 0,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List posts.

        Args:
            board_id: Filter by board ID (optional)
            limit: Maximum number of results
            skip: Number of results to skip
            status: Filter by status (optional)

        Returns:
            List of posts
        """
        params = {
            'limit': limit,
            'skip': skip
        }
        if board_id:
            params['board'] = board_id
        if status:
            params['status'] = status

        return self._request('/posts/list', params=params)

    def get_post(self, post_id: str) -> Dict[str, Any]:
        """
        Get post details.

        Args:
            post_id: Post ID

        Returns:
            Post details
        """
        return self._request('/posts/retrieve', params={'id': post_id})

    def create_post(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new post.

        Args:
            data: Post data including authorID, boardID, title, details, etc.

        Returns:
            Created post
        """
        return self._request('/posts/create', data=data)

    def update_post(self, post_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a post.

        Args:
            post_id: Post ID
            data: Fields to update

        Returns:
            Updated post
        """
        data['id'] = post_id
        return self._request('/posts/update', data=data)

    def change_post_status(
        self,
        post_id: str,
        status: str
    ) -> Dict[str, Any]:
        """
        Change post status.

        Args:
            post_id: Post ID
            status: New status (planning, in_progress, implemented, etc.)

        Returns:
            Updated post
        """
        return self._request('/posts/changeStatus', data={
            'id': post_id,
            'status': status
        })

    def delete_post(self, post_id: str) -> Dict[str, Any]:
        """
        Delete a post.

        Args:
            post_id: Post ID

        Returns:
            Deletion result
        """
        return self._request('/posts/delete', data={'id': post_id})

    def list_comments(
        self,
        post_id: str,
        limit: int = 100,
        skip: int = 0
    ) -> Dict[str, Any]:
        """
        List comments for a post.

        Args:
            post_id: Post ID
            limit: Maximum number of comments
            skip: Number of comments to skip

        Returns:
            List of comments
        """
        return self._request('/comments/list', params={
            'post': post_id,
            'limit': limit,
            'skip': skip
        })

    def create_comment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a comment.

        Args:
            data: Comment data including authorID, postID, value, etc.

        Returns:
            Created comment
        """
        return self._request('/comments/create', data=data)

    def delete_comment(self, comment_id: str) -> Dict[str, Any]:
        """
        Delete a comment.

        Args:
            comment_id: Comment ID

        Returns:
            Deletion result
        """
        return self._request('/comments/delete', data={'id': comment_id})

    def list_voters(
        self,
        post_id: str,
        limit: int = 100,
        skip: int = 0
    ) -> Dict[str, Any]:
        """
        List voters for a post.

        Args:
            post_id: Post ID
            limit: Maximum number of voters
            skip: Number of voters to skip

        Returns:
            List of voters
        """
        return self._request('/users/listVoters', params={
            'post': post_id,
            'limit': limit,
            'skip': skip
        })

    def create_vote(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a vote.

        Args:
            data: Vote data including userID, postID, score

        Returns:
            Vote result
        """
        return self._request('/votes/create', data=data)

    def delete_vote(self, user_id: str, post_id: str) -> Dict[str, Any]:
        """
        Delete a vote.

        Args:
            user_id: User ID
            post_id: Post ID

        Returns:
            Deletion result
        """
        return self._request('/votes/delete', data={
            'userID': user_id,
            'postID': post_id
        })

    def list_boards(self, limit: int = 50, skip: int = 0) -> Dict[str, Any]:
        """
        List boards.

        Args:
            limit: Maximum number of results
            skip: Number of results to skip

        Returns:
            List of boards
        """
        return self._request('/boards/list', params={
            'limit': limit,
            'skip': skip
        })

    def get_board(self, board_id: str) -> Dict[str, Any]:
        """
        Get board details.

        Args:
            board_id: Board ID

        Returns:
            Board details
        """
        return self._request('/boards/retrieve', params={'id': board_id})

    def create_board(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new board.

        Args:
            data: Board data including name, etc.

        Returns:
            Created board
        """
        return self._request('/boards/create', data=data)

    def update_board(self, board_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a board.

        Args:
            board_id: Board ID
            data: Fields to update

        Returns:
            Updated board
        """
        data['id'] = board_id
        return self._request('/boards/update', data=data)

    def list_users(
        self,
        limit: int = 100,
        skip: int = 0,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List users.

        Args:
            limit: Maximum number of results
            skip: Number of results to skip
            search: Search query (optional)

        Returns:
            List of users
        """
        params = {
            'limit': limit,
            'skip': skip
        }
        if search:
            params['search'] = search

        return self._request('/users/list', params=params)

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Get user details.

        Args:
            user_id: User ID

        Returns:
            User details
        """
        return self._request('/users/retrieve', params={'id': user_id})

    def create_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a user.

        Args:
            data: User data including name, email, etc.

        Returns:
            Created user
        """
        return self._request('/users/create', data=data)

    def get_user_by_email(self, email: str) -> Dict[str, Any]:
        """
        Get user by email.

        Args:
            email: User email

        Returns:
            User details
        """
        return self._request('/users/retrieveByEmail', params={'email': email})

    def list_tags(
        self,
        post_id: Optional[str] = None,
        limit: int = 100,
        skip: int = 0
    ) -> Dict[str, Any]:
        """
        List tags.

        Args:
            post_id: Filter by post ID (optional)
            limit: Maximum number of results
            skip: Number of results to skip

        Returns:
            List of tags
        """
        params = {
            'limit': limit,
            'skip': skip
        }
        if post_id:
            params['post'] = post_id

        return self._request('/tags/list', params=params)

    def create_tag(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a tag.

        Args:
            data: Tag data including name, color

        Returns:
            Created tag
        """
        return self._request('/tags/create', data=data)

    def attach_tag(self, post_id: str, tag_id: str) -> Dict[str, Any]:
        """
        Attach a tag to a post.

        Args:
            post_id: Post ID
            tag_id: Tag ID

        Returns:
            Result
        """
        return self._request('/tags/attach', data={
            'postID': post_id,
            'tagID': tag_id
        })

    def detach_tag(self, post_id: str, tag_id: str) -> Dict[str, Any]:
        """
        Detach a tag from a post.

        Args:
            post_id: Post ID
            tag_id: Tag ID

        Returns:
            Result
        """
        return self._request('/tags/detach', data={
            'postID': post_id,
            'tagID': tag_id
        })

    def list_changelogs(
        self,
        limit: int = 50,
        skip: int = 0
    ) -> Dict[str, Any]:
        """
        List changelogs.

        Args:
            limit: Maximum number of results
            skip: Number of results to skip

        Returns:
            List of changelogs
        """
        return self._request('/changelogs/list', params={
            'limit': limit,
            'skip': skip
        })

    def create_changelog(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a changelog entry.

        Args:
            data: Changelog data including label, value, type, etc.

        Returns:
            Created changelog
        """
        return self._request('/changelogs/create', data=data)

    def delete_changelog(self, changelog_id: str) -> Dict[str, Any]:
        """
        Delete a changelog.

        Args:
            changelog_id: Changelog ID

        Returns:
            Deletion result
        """
        return self._request('/changelogs/delete', data={'id': changelog_id})

    def list_activities(
        self,
        object_id: Optional[str] = None,
        limit: int = 100,
        skip: int = 0
    ) -> Dict[str, Any]:
        """
        List activities.

        Args:
            object_id: Filter by object ID (optional)
            limit: Maximum number of results
            skip: Number of results to skip

        Returns:
            List of activities
        """
        params = {
            'limit': limit,
            'skip': skip
        }
        if object_id:
            params['objectID'] = object_id

        return self._request('/activities/list', params=params)
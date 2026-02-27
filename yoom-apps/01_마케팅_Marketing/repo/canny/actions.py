"""
Canny API Actions
Yoom에서 실행 가능한 API 액션 구현
"""

from typing import Optional, Dict, Any, List
from .client import CannyClient


class CannyActions(CannyClient):
    """Canny API 액션"""

    # ========== 사용자 관련 액션 ==========

    def create_or_update_user_and_company(
        self,
        user_id: Optional[str] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,
        avatar_url: Optional[str] = None,
        company_id: Optional[str] = None,
        company_name: Optional[str] = None,
        created: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        사용자 및 회사 생성 또는 업데이트

        Args:
            user_id: 사용자 ID
            email: 사용자 이메일
            name: 사용자 이름
            avatar_url: 아바타 URL
            company_id: 회사 ID
            company_name: 회사 이름
            created: 생성 시간 (ISO string)

        Returns:
            생성/업데이트된 사용자 정보
        """
        data = {}

        if user_id:
            data["userID"] = user_id
        if email:
            data["email"] = email
        if name:
            data["name"] = name
        if avatar_url:
            data["avatarURL"] = avatar_url
        if company_id:
            data["companyID"] = company_id
        if company_name:
            data["companyName"] = company_name
        if created:
            data["created"] = created

        return self._request("users/create_or_update", data)

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        사용자 정보 가져오기

        Args:
            user_id: 사용자 ID

        Returns:
            사용자 정보
        """
        return self._request("/users/retrieve", {"userID": user_id})

    def list_users(
        self,
        limit: int = 100,
        cursor: Optional[str] = None,
        created_after: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        사용자 목록 가져오기

        Args:
            limit: 최대 개수
            cursor: 커서 (pagination)
            created_after: 해당 날짜 이후 생성된 사용자

        Returns:
            사용자 목록
        """
        data = {
            "limit": limit
        }

        if cursor:
            data["cursor"] = cursor

        if created_after:
            data["createdAfter"] = created_after

        return self._request("/users/list", data)

    # ========== 회사 관련 액션 ==========

    def update_company(
        self,
        company_id: str,
        name: Optional[str] = None,
        logo_url: Optional[str] = None,
        created: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        회사 업데이트

        Args:
            company_id: 회사 ID
            name: 회사 이름
            logo_url: 로고 URL
            created: 생성 시간 (ISO string)

        Returns:
            업데이트된 회사 정보
        """
        data = {
            "companyID": company_id
        }

        if name:
            data["name"] = name

        if logo_url:
            data["logoURL"] = logo_url

        if created:
            data["created"] = created

        return self._request("companies/update", data)

    def search_companies(
        self,
        query: str,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        회사 검색

        Args:
            query: 검색 쿼리
            limit: 최대 개수

        Returns:
            검색된 회사 목록
        """
        return self._request(
            "companies/search",
            {
                "query": query,
                "limit": limit
            }
        )

    # ========== 게시글 관련 액션 ==========

    def create_post(
        self,
        board_id: str,
        author_id: str,
        title: str,
        details: Optional[str] = None,
        status: Optional[str] = None,
        created: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        게시글 생성

        Args:
            board_id: 보드 ID
            author_id: 작성자 ID
            title: 제목
            details: 상세 내용
            status: 상태 (open, closed, etc.)
            created: 생성 시간 (ISO string)

        Returns:
            생성된 게시글 정보
        """
        data = {
            "boardID": board_id,
            "authorID": author_id,
            "title": title
        }

        if details:
            data["details"] = details

        if status:
            data["status"] = status

        if created:
            data["created"] = created

        return self._request("posts/create", data)

    def change_post_status(
        self,
        post_id: str,
        status: str,
        author_id: str,
        status_change_note: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        게시글 상태 변경

        Args:
            post_id: 게시글 ID
            status: 새로운 상태 (open, closed, etc.)
            author_id: 상태 변경을 수행하는 사용자 ID
            status_change_note: 상태 변경 노트

        Returns:
            업데이트된 게시글 정보
        """
        data = {
            "postID": post_id,
            "status": status,
            "authorID": author_id
        }

        if status_change_note:
            data["statusChangeNote"] = status_change_note

        return self._request("posts/change_status", data)

    def search_posts(
        self,
        board_id: str,
        query: Optional[str] = None,
        limit: int = 100,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        게시글 검색

        Args:
            board_id: 보드 ID
            query: 검색 쿼리
            limit: 최대 개수
            status: 상태 필터 (open, closed, etc.)

        Returns:
            검색된 게시글 목록
        """
        data = {
            "boardID": board_id,
            "limit": limit
        }

        if query:
            data["query"] = query

        if status:
            data["status"] = status

        return self._request("posts/search", data)

    # ========== 댓글 관련 액션 ==========

    def create_comment(
        self,
        post_id: str,
        author_id: str,
        value: str,
        created: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        댓글 생성

        Args:
            post_id: 게시글 ID
            author_id: 작성자 ID
            value: 댓글 내용
            created: 생성 시간 (ISO string)

        Returns:
            생성된 댓글 정보
        """
        data = {
            "postID": post_id,
            "authorID": author_id,
            "value": value
        }

        if created:
            data["created"] = created

        return self._request("comments/create", data)

    # ========== 보드 관련 액션 ==========

    def list_boards(self, limit: int = 100) -> Dict[str, Any]:
        """
        보드 목록 가져오기

        Args:
            limit: 최대 개수

        Returns:
            보드 목록
        """
        return self._request("boards/list", {"limit": limit})
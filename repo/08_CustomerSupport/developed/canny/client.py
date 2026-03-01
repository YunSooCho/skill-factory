"""
Canny Client
피드백 및 기능 요청 관리 API 클라이언트
"""

import requests
from typing import Optional, Dict, List, Any


class CannyClient:
    """
    Canny API 클라이언트

    사용자 피드백, 기능 요청 관리를 위한 클라이언트
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://canny.io/api/v1",
        timeout: int = 30
    ):
        """
        Canny 클라이언트 초기화

        Args:
            api_key: Canny API 키
            base_url: API 기본 URL
            timeout: 요청 타임아웃 (초)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

    def _request(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        API 요청 전송

        Args:
            endpoint: API 엔드포인트
            data: 요청 데이터
            params: URL 파라미터

        Returns:
            API 응답 데이터

        Raises:
            requests.RequestException: API 요청 실패
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        payload = {'apiKey': self.api_key}

        if data:
            payload.update(data)

        response = self.session.post(
            url,
            json=payload,
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def create_post(
        self,
        title: str,
        description: str,
        author_id: str,
        board_id: str,
        category_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        새 피드백/게시물 생성

        Args:
            title: 제목
            description: 설명
            author_id: 작성자 ID
            board_id: 보드 ID
            category_id: 카테고리 ID
            tags: 태그 목록
            details: 추가 세부사항

        Returns:
            생성된 게시물 정보
        """
        data = {
            'title': title,
            'details': description,
            'authorID': author_id,
            'boardID': board_id
        }

        if category_id:
            data['categoryID'] = category_id
        if tags:
            data['tags'] = tags
        if details:
            data['details'] = details

        return self._request('/posts/create', data=data)

    def get_post(self, post_id: str) -> Dict[str, Any]:
        """
        게시물 조회

        Args:
            post_id: 게시물 ID

        Returns:
            게시물 정보
        """
        return self._request('/posts/retrieve', data={'id': post_id})

    def list_posts(
        self,
        board_id: Optional[str] = None,
        author_id: Optional[str] = None,
        limit: int = 50,
        skip: int = 0,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        게시물 목록 조회

        Args:
            board_id: 보드 ID 필터
            author_id: 작성자 ID 필터
            limit: 반환할 항목 수
            skip: 건너뛸 항목 수
            status: 상태 필터

        Returns:
            게시물 목록
        """
        data = {'limit': limit, 'skip': skip}

        if board_id:
            data['boardID'] = board_id
        if author_id:
            data['authorID'] = author_id
        if status:
            data['status'] = status

        response = self._request('/posts/list', data=data)
        return response.get('posts', [])

    def update_post(
        self,
        post_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        게시물 업데이트

        Args:
            post_id: 게시물 ID
            title: 새 제목
            description: 새 설명
            status: 새 상태
            tags: 새 태그 목록

        Returns:
            업데이트된 게시물 정보
        """
        data = {'id': post_id}

        if title:
            data['title'] = title
        if description:
            data['details'] = description
        if status:
            data['status'] = status
        if tags:
            data['tags'] = tags

        return self._request('/posts/update', data=data)

    def create_comment(
        self,
        post_id: str,
        author_id: str,
        content: str,
        parent_comment_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        댓글 생성

        Args:
            post_id: 게시물 ID
            author_id: 작성자 ID
            content: 댓글 내용
            parent_comment_id: 부모 댓글 ID (대댓글용)

        Returns:
            생성된 댓글 정보
        """
        data = {
            'postID': post_id,
            'authorID': author_id,
            'value': content
        }

        if parent_comment_id:
            data['parentID'] = parent_comment_id

        return self._request('/comments/create', data=data)

    def list_comments(
        self,
        post_id: str,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict[str, Any]]:
        """
        댓글 목록 조회

        Args:
            post_id: 게시물 ID
            limit: 반환할 항목 수
            skip: 건너뛸 항목 수

        Returns:
            댓글 목록
        """
        data = {
            'postID': post_id,
            'limit': limit,
            'skip': skip
        }

        response = self._request('/comments/list', data=data)
        return response.get('comments', [])

    def create_vote(
        self,
        post_id: str,
        author_id: str,
        score: int = 1
    ) -> Dict[str, Any]:
        """
        투표 생성

        Args:
            post_id: 게시물 ID
            author_id: 작성자 ID
            score: 투표 가중치

        Returns:
            투표 정보
        """
        data = {
            'postID': post_id,
            'authorID': author_id,
            'score': score
        }

        return self._request('/votes/create', data=data)

    def delete_vote(
        self,
        post_id: str,
        author_id: str
    ) -> Dict[str, Any]:
        """
        투표 삭제

        Args:
            post_id: 게시물 ID
            author_id: 작성자 ID

        Returns:
            삭제 결과
        """
        data = {
            'postID': post_id,
            'authorID': author_id
        }

        return self._request('/votes/delete', data=data)

    def create_user(
        self,
        name: str,
        email: str,
        avatar_url: Optional[str] = None,
        companies: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        사용자 생성

        Args:
            name: 이름
            email: 이메일
            avatar_url: 아바타 URL
            companies: 회사 리스트

        Returns:
            생성된 사용자 정보
        """
        data = {
            'name': name,
            'email': email,
            'createIfNotExists': 'true'
        }

        if avatar_url:
            data['avatarURL'] = avatar_url
        if companies:
            data['companies'] = companies

        return self._request('/users/create', data=data)

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        사용자 조회

        Args:
            user_id: 사용자 ID

        Returns:
            사용자 정보
        """
        return self._request('/users/retrieve', data={'id': user_id})

    def list_boards(self) -> List[Dict[str, Any]]:
        """
        보드 목록 조회

        Returns:
            보드 목록
        """
        response = self._request('/boards/list')
        return response.get('boards', [])

    def get_board(self, board_id: str) -> Dict[str, Any]:
        """
        보드 조회

        Args:
            board_id: 보드 ID

        Returns:
            보드 정보
        """
        return self._request('/boards/retrieve', data={'id': board_id})

    def create_status_change(
        self,
        post_id: str,
        user_id: str,
        status: str,
        comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        상태 변경 이력 생성

        Args:
            post_id: 게시물 ID
            user_id: 사용자 ID
            status: 새 상태
            comment: 변경 사유 코멘트

        Returns:
            상태 변경 정보
        """
        data = {
            'postID': post_id,
            'userID': user_id,
            'eventType': 'statusChange',
            'value': status
        }

        if comment:
            data['comment'] = comment

        return self._request('/timelineEntries/create', data=data)

    def close(self):
        """세션 종료"""
        self.session.close()
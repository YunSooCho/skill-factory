"""
AskHandle Client
고객 문의 및 요청 관리 API 클라이언트
"""

import requests
from typing import Optional, Dict, List, Any
from datetime import datetime


class AskHandleClient:
    """
    AskHandle API 클라이언트

    高객 문의, 요청, 티켓 관리를 위한 클라이언트
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.askhandle.com/v1",
        timeout: int = 30
    ):
        """
        AskHandle 클라이언트 초기화

        Args:
            api_key: AskHandle API 키
            base_url: API 기본 URL
            timeout: 요청 타임아웃 (초)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        API 요청 전송

        Args:
            method: HTTP 메서드
            endpoint: API 엔드포인트
            data: 요청 본문 데이터
            params: URL 파라미터

        Returns:
            API 응답 데이터

        Raises:
            requests.RequestException: API 요청 실패
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def create_ticket(
        self,
        title: str,
        description: str,
        requester_name: str,
        requester_email: str,
        priority: str = "medium",
        category: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        새로운 티켓 생성

        Args:
            title: 티켓 제목
            description: 티켓 설명
            requester_name: 요청자 이름
            requester_email: 요청자 이메일
            priority: 우선순위 (low, medium, high, urgent)
            category: 티켓 카테고리
            tags: 티켓 태그 목록

        Returns:
            생성된 티켓 정보
        """
        data = {
            'title': title,
            'description': description,
            'requester': {
                'name': requester_name,
                'email': requester_email
            },
            'priority': priority
        }

        if category:
            data['category'] = category
        if tags:
            data['tags'] = tags

        return self._request('POST', '/tickets', data=data)

    def get_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """
        티켓 상세 조회

        Args:
            ticket_id: 티켓 ID

        Returns:
            티켓 상세 정보
        """
        return self._request('GET', f'/tickets/{ticket_id}')

    def list_tickets(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        티켓 목록 조회

        Args:
            status: 상태 필터 (open, in_progress, resolved, closed)
            priority: 우선순위 필터
            limit: 반환할 항목 수
            offset: 오프셋

        Returns:
            티켓 목록
        """
        params = {'limit': limit, 'offset': offset}
        if status:
            params['status'] = status
        if priority:
            params['priority'] = priority

        response = self._request('GET', '/tickets', params=params)
        return response.get('tickets', [])

    def update_ticket(
        self,
        ticket_id: str,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assignee_id: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        티켓 업데이트

        Args:
            ticket_id: 티켓 ID
            status: 새 상태
            priority: 새 우선순위
            assignee_id: 담당자 ID
            tags: 업데이트할 태그 목록

        Returns:
            업데이트된 티켓 정보
        """
        data = {}
        if status:
            data['status'] = status
        if priority:
            data['priority'] = priority
        if assignee_id:
            data['assignee_id'] = assignee_id
        if tags:
            data['tags'] = tags

        return self._request('PUT', f'/tickets/{ticket_id}', data=data)

    def add_comment(
        self,
        ticket_id: str,
        comment: str,
        author_name: str,
        author_email: str,
        is_internal: bool = False
    ) -> Dict[str, Any]:
        """
        티켓에 댓글 추가

        Args:
            ticket_id: 티켓 ID
            comment: 댓글 내용
            author_name: 작성자 이름
            author_email: 작성자 이메일
            is_internal: 내부용 댓글 여부

        Returns:
            추가된 댓글 정보
        """
        data = {
            'comment': comment,
            'author': {
                'name': author_name,
                'email': author_email
            },
            'is_internal': is_internal
        }

        return self._request('POST', f'/tickets/{ticket_id}/comments', data=data)

    def get_ticket_comments(self, ticket_id: str) -> List[Dict[str, Any]]:
        """
        티켓 댓글 목록 조회

        Args:
            ticket_id: 티켓 ID

        Returns:
            댓글 목록
        """
        response = self._request('GET', f'/tickets/{ticket_id}/comments')
        return response.get('comments', [])

    def create_customer(
        self,
        name: str,
        email: str,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        새 고객 생성

        Args:
            name: 고객 이름
            email: 고객 이메일
            phone: 전화번호
            company: 회사명
            metadata: 추가 메타데이터

        Returns:
            생성된 고객 정보
        """
        data = {
            'name': name,
            'email': email
        }

        if phone:
            data['phone'] = phone
        if company:
            data['company'] = company
        if metadata:
            data['metadata'] = metadata

        return self._request('POST', '/customers', data=data)

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """
        고객 조회

        Args:
            customer_id: 고객 ID

        Returns:
            고객 정보
        """
        return self._request('GET', f'/customers/{customer_id}')

    def list_customers(
        self,
        search: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        고객 목록 조회

        Args:
            search: 검색어
            limit: 반환할 항목 수
            offset: 오프셋

        Returns:
            고객 목록
        """
        params = {'limit': limit, 'offset': offset}
        if search:
            params['search'] = search

        response = self._request('GET', '/customers', params=params)
        return response.get('customers', [])

    def get_statistics(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        통계 정보 조회

        Args:
            start_date: 시작 날짜 (YYYY-MM-DD)
            end_date: 종료 날짜 (YYYY-MM-DD)

        Returns:
            통계 정보
        """
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date

        return self._request('GET', '/statistics', params=params)

    def close(self):
        """세션 종료"""
        self.session.close()
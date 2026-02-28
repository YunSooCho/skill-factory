"""
Reamaze Client
고객관계 관리 및 지원 티켓 API 클라이언트
"""

import requests
from typing import Optional, Dict, List, Any


class ReamazeClient:
    """
    Reamaze API 클라이언트

    고객관계 관리, 지원 티켓, 채팅 관리를 위한 클라이언트
    """

    def __init__(
        self,
        api_key: str,
        account: str,
        base_url: str = "https://api.reamaze.com",
        timeout: int = 30
    ):
        """
        Reamaze 클라이언트 초기화

        Args:
            api_key: Reamaze API 키
            account: Reamaze 계정 (브랜드)
            base_url: API 기본 URL
            timeout: 요청 타임아웃 (초)
        """
        self.api_key = api_key
        self.account = account
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.auth = (api_key, '')
        self.session.headers.update({
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
        url = f"{self.base_url}/{self.account}/{endpoint.lstrip('/')}"
        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def create_conversation(
        self,
        subject: str,
        message: str,
        customer_email: str,
        customer_name: Optional[str] = None,
        channel: str = "email",
        tags: Optional[List[str]] = None,
        user_assignee: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        새 대화(티켓) 생성

        Args:
            subject: 제목
            message: 메시지 내용
            customer_email: 고객 이메일
            customer_name: 고객 이름
            channel: 채널 타입 (email, chat, facebook, twitter)
            tags: 태그 목록
            user_assignee: 담당자 이메일

        Returns:
            생성된 대화 정보
        """
        data = {
            'conversation': {
                'subject': subject,
                'message': {
                    'body': message
                },
                'customer': {
                    'email': customer_email,
                    'name': customer_name
                },
                'channel': channel
            }
        }

        if tags:
            data['conversation']['tags'] = tags
        if user_assignee:
            data['conversation']['user'] = {'email': user_assignee}

        return self._request('POST', '/conversations', data=data)

    def get_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """
        대화 조회

        Args:
            conversation_id: 대화 ID (slug)

        Returns:
            대화 상세 정보
        """
        return self._request('GET', f'/conversations/{conversation_id}')

    def list_conversations(
        self,
        status: Optional[str] = None,
        channel: Optional[str] = None,
        limit: int = 50,
        page: int = 1
    ) -> List[Dict[str, Any]]:
        """
        대화 목록 조회

        Args:
            status: 상태 필터 (open, pending, resolved, archived)
            channel: 채널 필터
            limit: 반환할 항목 수
            page: 페이지 번호

        Returns:
            대화 목록
        """
        params = {'limit': limit, 'page': page}
        if status:
            params['status'] = status
        if channel:
            params['channel'] = channel

        response = self._request('GET', '/conversations', params=params)
        return response.get('conversations', [])

    def update_conversation(
        self,
        conversation_id: str,
        status: Optional[str] = None,
        user_assignee: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        대화 업데이트

        Args:
            conversation_id: 대화 ID
            status: 새 상태
            user_assignee: 새 담당자
            tags: 새 태그 목록

        Returns:
            업데이트된 대화 정보
        """
        data = {}
        if status:
            data['status'] = status
        if user_assignee:
            data['user'] = {'email': user_assignee}
        if tags:
            data['tags'] = tags

        return self._request('PUT', f'/conversations/{conversation_id}', data={'conversation': data})

    def add_message(
        self,
        conversation_id: str,
        body: str,
        internal: bool = False,
        attachments: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        대화에 메시지 추가

        Args:
            conversation_id: 대화 ID
            body: 메시지 내용
            internal: 내부용 메시지 여부
            attachments: 첨부파일 URLs

        Returns:
            추가된 메시지 정보
        """
        data = {
            'message': {
                'body': body,
                'internal': internal
            }
        }

        if attachments:
            data['message']['attachments'] = attachments

        return self._request('POST', f'/conversations/{conversation_id}/messages', data=data)

    def list_messages(
        self,
        conversation_id: str,
        limit: int = 50,
        page: int = 1
    ) -> List[Dict[str, Any]]:
        """
        대화 메시지 목록 조회

        Args:
            conversation_id: 대화 ID
            limit: 반환할 항목 수
            page: 페이지 번호

        Returns:
            메시지 목록
        """
        params = {'limit': limit, 'page': page}
        response = self._request('GET', f'/conversations/{conversation_id}/messages', params=params)
        return response.get('messages', [])

    def create_customer(
        self,
        email: str,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        location: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        새 고객 생성

        Args:
            email: 고객 이메일
            name: 고객 이름
            phone: 전화번호
            company: 회사명
            location: 위치
            metadata: 추가 메타데이터

        Returns:
            생성된 고객 정보
        """
        data = {
            'customer': {
                'email': email
            }
        }

        if name:
            data['customer']['name'] = name
        if phone:
            data['customer']['phone'] = phone
        if company:
            data['customer']['company'] = company
        if location:
            data['customer']['location'] = location
        if metadata:
            data['customer']['customAttributes'] = metadata

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
        page: int = 1
    ) -> List[Dict[str, Any]]:
        """
        고객 목록 조회

        Args:
            search: 검색어 (이름, 이메일, 회사)
            limit: 반환할 항목 수
            page: 페이지 번호

        Returns:
            고객 목록
        """
        params = {'limit': limit, 'page': page}
        if search:
            params['q'] = search

        response = self._request('GET', '/customers', params=params)
        return response.get('customers', [])

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        사용자(직원) 조회

        Args:
            user_id: 사용자 ID

        Returns:
            사용자 정보
        """
        return self._request('GET', f'/users/{user_id}')

    def list_users(self) -> List[Dict[str, Any]]:
        """
        사용자(직원) 목록 조회

        Returns:
            사용자 목록
        """
        response = self._request('GET', '/users')
        return response.get('users', [])

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

    def create_article(
        self,
        title: str,
        content: str,
        category_id: str,
        published: bool = False
    ) -> Dict[str, Any]:
        """
        도움말 문서(아티클) 생성

        Args:
            title: 문서 제목
            content: 문서 내용 (HTML/Markdown)
            category_id: 카테고리 ID
            published: 게시 여부

        Returns:
            생성된 문서 정보
        """
        data = {
            'article': {
                'title': title,
                'content': content,
                'category_id': category_id,
                'published': published
            }
        }

        return self._request('POST', '/articles', data=data)

    def list_channels(self) -> List[Dict[str, Any]]:
        """
        채널 목록 조회

        Returns:
            채널 목록
        """
        response = self._request('GET', '/channels')
        return response.get('channels', [])

    def close(self):
        """세션 종료"""
        self.session.close()
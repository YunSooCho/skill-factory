"""
Respond.io Client
멀티채널 고객지원 API 클라이언트
"""

import requests
from typing import Optional, Dict, List, Any


class RespondIOClient:
    """
    Respond.io API 클라이언트

    멀티채널 고객지원, 메시지 관리, 고객 추적을 위한 클라이언트
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.respond.io/v1",
        timeout: int = 30
    ):
        """
        Respond.io 클라이언트 초기화

        Args:
            api_key: Respond.io API 키
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

    def create_message(
        self,
        channel_id: str,
        text: str,
        customer_id: Optional[str] = None,
        file_urls: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        메시지 전송

        Args:
            channel_id: 채널 ID
            text: 메시지 내용
            customer_id: 고객 ID (선택)
            file_urls: 파일 URL 목록
            metadata: 추가 메타데이터

        Returns:
            전송된 메시지 정보
        """
        data = {
            'channelId': channel_id,
            'text': text
        }

        if customer_id:
            data['customerId'] = customer_id
        if file_urls:
            data['fileUrls'] = file_urls
        if metadata:
            data['metadata'] = metadata

        return self._request('POST', '/messages', data=data)

    def get_message(self, message_id: str) -> Dict[str, Any]:
        """
        메시지 조회

        Args:
            message_id: 메시지 ID

        Returns:
            메시지 정보
        """
        return self._request('GET', f'/messages/{message_id}')

    def list_messages(
        self,
        conversation_id: Optional[str] = None,
        channel_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        메시지 목록 조회

        Args:
            conversation_id: 대화 ID 필터
            channel_id: 채널 ID 필터
            limit: 반환할 항목 수
            offset: 오프셋

        Returns:
            메시지 목록
        """
        params = {'limit': limit, 'offset': offset}
        if conversation_id:
            params['conversationId'] = conversation_id
        if channel_id:
            params['channelId'] = channel_id

        response = self._request('GET', '/messages', params=params)
        return response.get('messages', [])

    def create_conversation(
        self,
        customer_id: str,
        channel_id: str,
        initial_message: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        새 대화 생성

        Args:
            customer_id: 고객 ID
            channel_id: 채널 ID
            initial_message: 초기 메시지
            tags: 태그 목록

        Returns:
            생성된 대화 정보
        """
        data = {
            'customerId': customer_id,
            'channelId': channel_id
        }

        if initial_message:
            data['initialMessage'] = initial_message
        if tags:
            data['tags'] = tags

        return self._request('POST', '/conversations', data=data)

    def get_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """
        대화 조회

        Args:
            conversation_id: 대화 ID

        Returns:
            대화 정보
        """
        return self._request('GET', f'/conversations/{conversation_id}')

    def list_conversations(
        self,
        status: Optional[str] = None,
        channel_id: Optional[str] = None,
        assigned_to: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        대화 목록 조회

        Args:
            status: 상태 필터 (open, pending, closed)
            channel_id: 채널 ID 필터
            assigned_to: 담당자 ID 필터
            limit: 반환할 항목 수
            offset: 오프셋

        Returns:
            대화 목록
        """
        params = {'limit': limit, 'offset': offset}
        if status:
            params['status'] = status
        if channel_id:
            params['channelId'] = channel_id
        if assigned_to:
            params['assignedTo'] = assigned_to

        response = self._request('GET', '/conversations', params=params)
        return response.get('conversations', [])

    def update_conversation(
        self,
        conversation_id: str,
        status: Optional[str] = None,
        assigned_to: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        대화 업데이트

        Args:
            conversation_id: 대화 ID
            status: 새 상태
            assigned_to: 새 담당자
            tags: 새 태그 목록

        Returns:
            업데이트된 대화 정보
        """
        data = {}
        if status:
            data['status'] = status
        if assigned_to:
            data['assignedTo'] = assigned_to
        if tags:
            data['tags'] = tags

        return self._request('PUT', f'/conversations/{conversation_id}', data=data)

    def close_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """
        대화 종료

        Args:
            conversation_id: 대화 ID

        Returns:
            종료된 대화 정보
        """
        return self._request('POST', f'/conversations/{conversation_id}/close')

    def create_customer(
        self,
        external_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        avatar_url: Optional[str] = None,
        custom_attributes: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        새 고객 생성

        Args:
            external_id: 외부 시스템 고객 ID
            name: 이름
            email: 이메일
            phone: 전화번호
            avatar_url: 아바터 URL
            custom_attributes: 사용자 정의 속성

        Returns:
            생성된 고객 정보
        """
        data = {'externalId': external_id}

        if name:
            data['name'] = name
        if email:
            data['email'] = email
        if phone:
            data['phone'] = phone
        if avatar_url:
            data['avatarUrl'] = avatar_url
        if custom_attributes:
            data['customAttributes'] = custom_attributes

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

    def update_customer(
        self,
        customer_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        avatar_url: Optional[str] = None,
        custom_attributes: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        고객 업데이트

        Args:
            customer_id: 고객 ID
            name: 새 이름
            email: 새 이메일
            phone: 새 전화번호
            avatar_url: 새 아바타 URL
            custom_attributes: 사용자 정의 속성

        Returns:
            업데이트된 고객 정보
        """
        data = {}
        if name:
            data['name'] = name
        if email:
            data['email'] = email
        if phone:
            data['phone'] = phone
        if avatar_url:
            data['avatarUrl'] = avatar_url
        if custom_attributes:
            data['customAttributes'] = custom_attributes

        return self._request('PUT', f'/customers/{customer_id}', data=data)

    def list_channels(self) -> List[Dict[str, Any]]:
        """
        채널 목록 조회

        Returns:
            채널 목록
        """
        response = self._request('GET', '/channels')
        return response.get('channels', [])

    def list_users(self) -> List[Dict[str, Any]]:
        """
        사용자 목록 조회

        Returns:
            사용자 목록
        """
        response = self._request('GET', '/users')
        return response.get('users', [])

    def assign_conversation(
        self,
        conversation_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        대화 담당자 지정

        Args:
            conversation_id: 대화 ID
            user_id: 사용자 ID

        Returns:
            업데이트된 대화 정보
        """
        data = {
            'conversationId': conversation_id,
            'userId': user_id
        }

        return self._request('POST', '/conversations/assign', data=data)

    def add_note(
        self,
        conversation_id: str,
        content: str,
        author_id: str
    ) -> Dict[str, Any]:
        """
        대화에 노트 추가

        Args:
            conversation_id: 대화 ID
            content: 노트 내용
            author_id: 작성자 ID

        Returns:
            추가된 노트 정보
        """
        data = {
            'conversationId': conversation_id,
            'content': content,
            'authorId': author_id
        }

        return self._request('POST', '/conversations/notes', data=data)

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
            params['startDate'] = start_date
        if end_date:
            params['endDate'] = end_date

        return self._request('GET', '/statistics', params=params)

    def close(self):
        """세션 종료"""
        self.session.close()
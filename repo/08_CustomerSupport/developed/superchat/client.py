"""
Superchat Client
라이브채팅 및 고객지원 API 클라이언트
"""

import requests
from typing import Optional, Dict, List, Any


class SuperchatClient:
    """
    Superchat API 클라이언트

    라이브채팅, 고객지원, 챗봇 관리를 위한 클라이언트
    """

    def __init__(
        self,
        api_key: str,
        account_id: str,
        base_url: str = "https://api.superchat.com/v1",
        timeout: int = 30
    ):
        """
        Superchat 클라이언트 초기화

        Args:
            api_key: Superchat API 키
            account_id: 계정 ID
            base_url: API 기본 URL
            timeout: 요청 타임아웃 (초)
        """
        self.api_key = api_key
        self.account_id = account_id
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'X-Account-Id': account_id,
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

    def start_chat(
        self,
        customer_name: str,
        customer_email: Optional[str] = None,
        initial_message: Optional[str] = None,
        channel: str = "web",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        새 채팅 시작

        Args:
            customer_name: 고객 이름
            customer_email: 고객 이메일
            initial_message: 초기 메시지
            channel: 채널 타입 (web, whatsapp, messenger, telegram)
            metadata: 추가 메타데이터

        Returns:
            생성된 채팅 정보
        """
        data = {
            'customerName': customer_name,
            'channel': channel
        }

        if customer_email:
            data['customerEmail'] = customer_email
        if initial_message:
            data['initialMessage'] = initial_message
        if metadata:
            data['metadata'] = metadata

        return self._request('POST', '/chats', data=data)

    def get_chat(self, chat_id: str) -> Dict[str, Any]:
        """
        채팅 조회

        Args:
            chat_id: 채팅 ID

        Returns:
            채팅 상세 정보
        """
        return self._request('GET', f'/chats/{chat_id}')

    def list_chats(
        self,
        status: Optional[str] = None,
        channel: Optional[str] = None,
        assigned_to: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        채팅 목록 조회

        Args:
            status: 상태 필터 (active, closed, archived)
            channel: 채널 필터
            assigned_to: 담당자 ID 필터
            limit: 반환할 항목 수
            offset: 오프셋

        Returns:
            채팅 목록
        """
        params = {'limit': limit, 'offset': offset}
        if status:
            params['status'] = status
        if channel:
            params['channel'] = channel
        if assigned_to:
            params['assignedTo'] = assigned_to

        response = self._request('GET', '/chats', params=params)
        return response.get('chats', [])

    def send_message(
        self,
        chat_id: str,
        message: str,
        message_type: str = "text",
        sender_type: str = "agent",
        file_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        메시지 전송

        Args:
            chat_id: 채팅 ID
            message: 메시지 내용
            message_type: 메시지 타입 (text, image, video, file, location)
            sender_type: 발신자 타입 (agent, customer, bot, system)
            file_url: 파일 URL

        Returns:
            전송된 메시지 정보
        """
        data = {
            'chatId': chat_id,
            'message': message,
            'messageType': message_type,
            'senderType': sender_type
        }

        if file_url:
            data['fileUrl'] = file_url

        return self._request('POST', '/messages', data=data)

    def get_messages(
        self,
        chat_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        메시지 목록 조회

        Args:
            chat_id: 채팅 ID
            limit: 반환할 항목 수
            offset: 오프셋

        Returns:
            메시지 목록
        """
        params = {'limit': limit, 'offset': offset}
        response = self._request('GET', f'/chats/{chat_id}/messages', params=params)
        return response.get('messages', [])

    def update_chat(
        self,
        chat_id: str,
        status: Optional[str] = None,
        assigned_to: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        채팅 업데이트

        Args:
            chat_id: 채팅 ID
            status: 새 상태
            assigned_to: 새 담당자
            tags: 태그 목록

        Returns:
            업데이트된 채팅 정보
        """
        data = {}
        if status:
            data['status'] = status
        if assigned_to:
            data['assignedTo'] = assigned_to
        if tags:
            data['tags'] = tags

        return self._request('PUT', f'/chats/{chat_id}', data=data)

    def close_chat(self, chat_id: str) -> Dict[str, Any]:
        """
        채팅 종료

        Args:
            chat_id: 채팅 ID

        Returns:
            종료된 채팅 정보
        """
        return self._request('POST', f'/chats/{chat_id}/close')

    def assign_chat(
        self,
        chat_id: str,
        agent_id: str
    ) -> Dict[str, Any]:
        """
        채팅 담당자 지정

        Args:
            chat_id: 채팅 ID
            agent_id: 에이전트 ID

        Returns:
            업데이트된 채팅 정보
        """
        data = {
            'chatId': chat_id,
            'agentId': agent_id
        }

        return self._request('POST', '/chats/assign', data=data)

    def create_customer(
        self,
        name: str,
        email: str,
        phone: Optional[str] = None,
        avatar_url: Optional[str] = None,
        company: Optional[str] = None,
        custom_attributes: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        새 고객 생성

        Args:
            name: 이름
            email: 이메일
            phone: 전화번호
            avatar_url: 아바타 URL
            company: 회사
            custom_attributes: 사용자 정의 속성

        Returns:
            생성된 고객 정보
        """
        data = {
            'name': name,
            'email': email
        }

        if phone:
            data['phone'] = phone
        if avatar_url:
            data['avatarUrl'] = avatar_url
        if company:
            data['company'] = company
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
        company: Optional[str] = None,
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
            company: 새 회사
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
        if company:
            data['company'] = company
        if custom_attributes:
            data['customAttributes'] = custom_attributes

        return self._request('PUT', f'/customers/{customer_id}', data=data)

    def create_bot(
        self,
        name: str,
        welcome_message: str,
        handoff_message: str,
        ai_provider: str = "openai",
        ai_model: str = "gpt-4o-mini",
        knowledge_base: Optional[str] = None,
        is_active: bool = False
    ) -> Dict[str, Any]:
        """
        AI 챗봇 생성

        Args:
            name: 봇 이름
            welcome_message: 환영 메시지
            handoff_message: 에이전트 전달 메시지
            ai_provider: AI 제공자 (openai, anthropic, google)
            ai_model: AI 모델
            knowledge_base: 지식 베이스 ID
            is_active: 활성화 여부

        Returns:
            생성된 봇 정보
        """
        data = {
            'name': name,
            'welcomeMessage': welcome_message,
            'handoffMessage': handoff_message,
            'aiProvider': ai_provider,
            'aiModel': ai_model,
            'isActive': is_active
        }

        if knowledge_base:
            data['knowledgeBase'] = knowledge_base

        return self._request('POST', '/bots', data=data)

    def get_bot(self, bot_id: str) -> Dict[str, Any]:
        """
        봇 조회

        Args:
            bot_id: 봇 ID

        Returns:
            봇 정보
        """
        return self._request('GET', f'/bots/{bot_id}')

    def list_bots(self) -> List[Dict[str, Any]]:
        """
        봇 목록 조회

        Returns:
            봇 목록
        """
        response = self._request('GET', '/bots')
        return response.get('bots', [])

    def update_bot(
        self,
        bot_id: str,
        name: Optional[str] = None,
        welcome_message: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        봇 업데이트

        Args:
            bot_id: 봇 ID
            name: 새 이름
            welcome_message: 새 환영 메시지
            is_active: 활성화 상태

        Returns:
            업데이트된 봇 정보
        """
        data = {}
        if name:
            data['name'] = name
        if welcome_message:
            data['welcomeMessage'] = welcome_message
        if is_active is not None:
            data['isActive'] = is_active

        return self._request('PUT', f'/bots/{bot_id}', data=data)

    def create_canned_response(
        self,
        title: str,
        content: str,
        shortcuts: Optional[List[str]] = None,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        템플릿 응답 생성

        Args:
            title: 제목
            content: 내용
            shortcuts: 단축키 목록
            category: 카테고리

        Returns:
            생성된 템플릿 응답 정보
        """
        data = {
            'title': title,
            'content': content
        }

        if shortcuts:
            data['shortcuts'] = shortcuts
        if category:
            data['category'] = category

        return self._request('POST', '/canned-responses', data=data)

    def list_canned_responses(
        self,
        category: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        템플릿 응답 목록 조회

        Args:
            category: 카테고리 필터
            limit: 반환할 항목 수

        Returns:
            템플릿 응답 목록
        """
        params = {'limit': limit}
        if category:
            params['category'] = category

        response = self._request('GET', '/canned-responses', params=params)
        return response.get('cannedResponses', [])

    def get_analytics(
        self,
        start_date: str,
        end_date: str,
        metric: str = "all"
    ) -> Dict[str, Any]:
        """
        분석 데이터 조회

        Args:
            start_date: 시작 날짜 (YYYY-MM-DD)
            end_date: 종료 날짜 (YYYY-MM-DD)
            metric: 메트릭 (all, messages, chats, satisfaction, response_time)

        Returns:
            분석 데이터
        """
        params = {
            'startDate': start_date,
            'endDate': end_date,
            'metric': metric
        }

        return self._request('GET', '/analytics', params=params)

    def list_agents(self) -> List[Dict[str, Any]]:
        """
        에이전트 목록 조회

        Returns:
            에이전트 목록
        """
        response = self._request('GET', '/agents')
        return response.get('agents', [])

    def close(self):
        """세션 종료"""
        self.session.close()
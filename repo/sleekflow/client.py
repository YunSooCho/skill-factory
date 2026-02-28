"""
Sleekflow Client
채팅 및 고객지원 워크플로우 API 클라이언트
"""

import requests
from typing import Optional, Dict, List, Any


class SleekflowClient:
    """
    Sleekflow API 클라이언트

    채팅, 워크플로우 자동화, 고객 트래킹을 위한 클라이언트
    """

    def __init__(
        self,
        api_key: str,
        workspace_id: str,
        base_url: str = "https://api.sleekflow.io/v1",
        timeout: int = 30
    ):
        """
        Sleekflow 클라이언트 초기화

        Args:
            api_key: Sleekflow API 키
            workspace_id: 워크스페이스 ID
            base_url: API 기본 URL
            timeout: 요청 타임아웃 (초)
        """
        self.api_key = api_key
        self.workspace_id = workspace_id
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'X-Workspace-Id': workspace_id,
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

    def create_chat_session(
        self,
        customer_id: str,
        channel: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        새 채팅 세션 생성

        Args:
            customer_id: 고객 ID
            channel: 채널 타입 (web, whatsapp, messenger, telegram)
            metadata: 추가 메타데이터

        Returns:
            생성된 채팅 세션 정보
        """
        data = {
            'customerId': customer_id,
            'channel': channel
        }

        if metadata:
            data['metadata'] = metadata

        return self._request('POST', '/chat/sessions', data=data)

    def get_chat_session(self, session_id: str) -> Dict[str, Any]:
        """
        채팅 세션 조회

        Args:
            session_id: 채팅 세션 ID

        Returns:
            채팅 세션 정보
        """
        return self._request('GET', f'/chat/sessions/{session_id}')

    def list_chat_sessions(
        self,
        customer_id: Optional[str] = None,
        status: Optional[str] = None,
        channel: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        채팅 세션 목록 조회

        Args:
            customer_id: 고객 ID 필터
            status: 상태 필터 (active, closed, archived)
            channel: 채널 필터
            limit: 반환할 항목 수
            offset: 오프셋

        Returns:
            채팅 세션 목록
        """
        params = {'limit': limit, 'offset': offset}
        if customer_id:
            params['customerId'] = customer_id
        if status:
            params['status'] = status
        if channel:
            params['channel'] = channel

        response = self._request('GET', '/chat/sessions', params=params)
        return response.get('sessions', [])

    def send_message(
        self,
        session_id: str,
        text: str,
        message_type: str = "text",
        sender_type: str = "agent",
        file_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        메시지 전송

        Args:
            session_id: 채팅 세션 ID
            text: 메시지 내용
            message_type: 메시지 타입 (text, image, video, file)
            sender_type: 발신자 타입 (agent, customer, bot)
            file_url: 파일 URL

        Returns:
            전송된 메시지 정보
        """
        data = {
            'sessionId': session_id,
            'text': text,
            'messageType': message_type,
            'senderType': sender_type
        }

        if file_url:
            data['fileUrl'] = file_url

        return self._request('POST', '/chat/messages', data=data)

    def get_messages(
        self,
        session_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        메시지 목록 조회

        Args:
            session_id: 채팅 세션 ID
            limit: 반환할 항목 수
            offset: 오프셋

        Returns:
            메시지 목록
        """
        params = {'limit': limit, 'offset': offset}
        response = self._request('GET', f'/chat/sessions/{session_id}/messages', params=params)
        return response.get('messages', [])

    def create_workflow(
        self,
        name: str,
        description: str,
        steps: List[Dict[str, Any]],
        trigger_type: str = "manual",
        is_active: bool = False
    ) -> Dict[str, Any]:
        """
        새 워크플로우 생성

        Args:
            name: 워크플로우 이름
            description: 설명
            steps: 워크플로우 단계 목록
            trigger_type: 트리거 타입 (manual, schedule, event)
            is_active: 활성화 여부

        Returns:
            생성된 워크플로우 정보
        """
        data = {
            'name': name,
            'description': description,
            'steps': steps,
            'triggerType': trigger_type,
            'isActive': is_active
        }

        return self._request('POST', '/workflows', data=data)

    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        워크플로우 조회

        Args:
            workflow_id: 워크플로우 ID

        Returns:
            워크플로우 상세 정보
        """
        return self._request('GET', f'/workflows/{workflow_id}')

    def list_workflows(
        self,
        is_active: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        워크플로우 목록 조회

        Args:
            is_active: 활성화 상태 필터
            limit: 반환할 항목 수
            offset: 오프셋

        Returns:
            워크플로우 목록
        """
        params = {'limit': limit, 'offset': offset}
        if is_active is not None:
            params['isActive'] = is_active

        response = self._request('GET', '/workflows', params=params)
        return response.get('workflows', [])

    def trigger_workflow(
        self,
        workflow_id: str,
        customer_id: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        워크플로우 트리거

        Args:
            workflow_id: 워크플로우 ID
            customer_id: 고객 ID
            parameters: 워크플로우 파라미터

        Returns:
            트리거 결과
        """
        data = {
            'workflowId': workflow_id,
            'customerId': customer_id
        }

        if parameters:
            data['parameters'] = parameters

        return self._request('POST', '/workflows/trigger', data=data)

    def create_template(
        self,
        name: str,
        category: str,
        content: str,
        variables: Optional[List[str]] = None,
        language: str = "ko"
    ) -> Dict[str, Any]:
        """
        메시지 템플릿 생성

        Args:
            name: 템플릿 이름
            category: 카테고리 (greeting, followup, notification)
            content: 템플릿 내용
            variables: 변수 목록
            language: 언어 코드

        Returns:
            생성된 템플릿 정보
        """
        data = {
            'name': name,
            'category': category,
            'content': content,
            'language': language
        }

        if variables:
            data['variables'] = variables

        return self._request('POST', '/templates', data=data)

    def get_template(self, template_id: str) -> Dict[str, Any]:
        """
        템플릿 조회

        Args:
            template_id: 템플릿 ID

        Returns:
            템플릿 정보
        """
        return self._request('GET', f'/templates/{template_id}')

    def list_templates(
        self,
        category: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        템플릿 목록 조회

        Args:
            category: 카테고리 필터
            limit: 반환할 항목 수
            offset: 오프셋

        Returns:
            템플릿 목록
        """
        params = {'limit': limit, 'offset': offset}
        if category:
            params['category'] = category

        response = self._request('GET', '/templates', params=params)
        return response.get('templates', [])

    def create_bot(
        self,
        name: str,
        description: str,
        greeting_message: str,
        ai_model: str = "gpt-4",
        knowledge_base: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        AI 챗봇 생성

        Args:
            name: 봇 이름
            description: 설명
            greeting_message: 환영 메시지
            ai_model: AI 모델 (gpt-3.5, gpt-4, claude)
            knowledge_base: 지식 베이스 ID

        Returns:
            생성된 봇 정보
        """
        data = {
            'name': name,
            'description': description,
            'greetingMessage': greeting_message,
            'aiModel': ai_model
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

    def get_analytics(
        self,
        start_date: str,
        end_date: str,
        metric: str = "all",
        channel: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        분석 데이터 조회

        Args:
            start_date: 시작 날짜 (YYYY-MM-DD)
            end_date: 종료 날짜 (YYYY-MM-DD)
            metric: 메트릭 (all, messages, sessions, satisfaction)
            channel: 채널 필터

        Returns:
            분석 데이터
        """
        params = {
            'startDate': start_date,
            'endDate': end_date,
            'metric': metric
        }

        if channel:
            params['channel'] = channel

        return self._request('GET', '/analytics', params=params)

    def track_customer_event(
        self,
        customer_id: str,
        event_name: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        고객 이벤트 추적

        Args:
            customer_id: 고객 ID
            event_name: 이벤트 이름
            properties: 이벤트 속성

        Returns:
            추적 결과
        """
        data = {
            'customerId': customer_id,
            'eventName': event_name
        }

        if properties:
            data['properties'] = properties

        return self._request('POST', '/customers/events', data=data)

    def close(self):
        """세션 종료"""
        self.session.close()
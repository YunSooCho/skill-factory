"""
Product Fruits Client
제품 온보딩 및 사용자 가이드 API 클라이언트
"""

import requests
from typing import Optional, Dict, List, Any


class ProductFruitsClient:
    """
    Product Fruits API 클라이언트

    제품 온보딩, 사용자 가이드, 투어, 툴팁 관리를 위한 클라이언트
    """

    def __init__(
        self,
        api_key: str,
        workspace_id: str,
        base_url: str = "https://api.productfruits.com",
        timeout: int = 30
    ):
        """
        Product Fruits 클라이언트 초기화

        Args:
            api_key: Product Fruits API 키
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

    def create_tour(
        self,
        name: str,
        description: str,
        steps: List[Dict[str, Any]],
        target_url_pattern: str,
        trigger_type: str = "manual",
        is_active: bool = False
    ) -> Dict[str, Any]:
        """
        새 투어 생성

        Args:
            name: 투어 이름
            description: 투어 설명
            steps: 투어 단계 목록
            target_url_pattern: 타겟 URL 패턴
            trigger_type: 트리거 타입 (manual, auto, onboarding)
            is_active: 활성화 여부

        Returns:
            생성된 투어 정보
        """
        data = {
            'name': name,
            'description': description,
            'steps': steps,
            'targetUrlPattern': target_url_pattern,
            'triggerType': trigger_type,
            'isActive': is_active
        }

        return self._request('POST', '/tours', data=data)

    def get_tour(self, tour_id: str) -> Dict[str, Any]:
        """
        투어 조회

        Args:
            tour_id: 투어 ID

        Returns:
            투어 상세 정보
        """
        return self._request('GET', f'/tours/{tour_id}')

    def list_tours(
        self,
        is_active: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        투어 목록 조회

        Args:
            is_active: 활성화 상태 필터
            limit: 반환할 항목 수
            offset: 오프셋

        Returns:
            투어 목록
        """
        params = {'limit': limit, 'offset': offset}
        if is_active is not None:
            params['isActive'] = is_active

        response = self._request('GET', '/tours', params=params)
        return response.get('tours', [])

    def update_tour(
        self,
        tour_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        steps: Optional[List[Dict[str, Any]]] = None,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        투어 업데이트

        Args:
            tour_id: 투어 ID
            name: 새 이름
            description: 새 설명
            steps: 새 단계 목록
            is_active: 활성화 여부

        Returns:
            업데이트된 투어 정보
        """
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        if steps:
            data['steps'] = steps
        if is_active is not None:
            data['isActive'] = is_active

        return self._request('PUT', f'/tours/{tour_id}', data=data)

    def create_tooltip(
        self,
        name: str,
        selector: str,
        content: str,
        position: str = "top",
        trigger_type: str = "hover",
        is_active: bool = False
    ) -> Dict[str, Any]:
        """
        새 툴팁 생성

        Args:
            name: 툴팁 이름
            selector: CSS 선택자
            content: 툴팁 내용
            position: 위치 (top, right, bottom, left)
            trigger_type: 트리거 타입 (hover, click)
            is_active: 활성화 여부

        Returns:
            생성된 툴팁 정보
        """
        data = {
            'name': name,
            'selector': selector,
            'content': content,
            'position': position,
            'triggerType': trigger_type,
            'isActive': is_active
        }

        return self._request('POST', '/tooltips', data=data)

    def get_tooltip(self, tooltip_id: str) -> Dict[str, Any]:
        """
        툴팁 조회

        Args:
            tooltip_id: 툴팁 ID

        Returns:
            툴팁 상세 정보
        """
        return self._request('GET', f'/tooltips/{tooltip_id}')

    def list_tooltips(
        self,
        is_active: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        툴팁 목록 조회

        Args:
            is_active: 활성화 상태 필터
            limit: 반환할 항목 수
            offset: 오프셋

        Returns:
            툴팁 목록
        """
        params = {'limit': limit, 'offset': offset}
        if is_active is not None:
            params['isActive'] = is_active

        response = self._request('GET', '/tooltips', params=params)
        return response.get('tooltips', [])

    def update_tooltip(
        self,
        tooltip_id: str,
        name: Optional[str] = None,
        selector: Optional[str] = None,
        content: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        툴팁 업데이트

        Args:
            tooltip_id: 툴팁 ID
            name: 새 이름
            selector: 새 CSS 선택자
            content: 새 내용
            is_active: 활성화 여부

        Returns:
            업데이트된 툴팁 정보
        """
        data = {}
        if name:
            data['name'] = name
        if selector:
            data['selector'] = selector
        if content:
            data['content'] = content
        if is_active is not None:
            data['isActive'] = is_active

        return self._request('PUT', f'/tooltips/{tooltip_id}', data=data)

    def create_checklist(
        self,
        name: str,
        description: str,
        items: List[Dict[str, Any]],
        target_url_pattern: str,
        is_active: bool = False
    ) -> Dict[str, Any]:
        """
        새 체크리스트 생성

        Args:
            name: 체크리스트 이름
            description: 체크리스트 설명
            items: 체크리스트 항목 목록
            target_url_pattern: 타겟 URL 패턴
            is_active: 활성화 여부

        Returns:
            생성된 체크리스트 정보
        """
        data = {
            'name': name,
            'description': description,
            'items': items,
            'targetUrlPattern': target_url_pattern,
            'isActive': is_active
        }

        return self._request('POST', '/checklists', data=data)

    def get_checklist(self, checklist_id: str) -> Dict[str, Any]:
        """
        체크리스트 조회

        Args:
            checklist_id: 체크리스트 ID

        Returns:
            체크리스트 상세 정보
        """
        return self._request('GET', f'/checklists/{checklist_id}')

    def get_user_progress(
        self,
        user_id: str,
        checklist_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        사용자 진행상황 조회

        Args:
            user_id: 사용자 ID
            checklist_id: 체크리스트 ID (선택)

        Returns:
            진행상황정보
        """
        params = {'userId': user_id}
        if checklist_id:
            params['checklistId'] = checklist_id

        return self._request('GET', '/user-progress', params=params)

    def track_event(
        self,
        user_id: str,
        event_name: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        사용자 이벤트 추적

        Args:
            user_id: 사용자 ID
            event_name: 이벤트 이름
            properties: 이벤트 속성

        Returns:
            이벤트 추적 결과
        """
        data = {
            'userId': user_id,
            'eventName': event_name
        }

        if properties:
            data['properties'] = properties

        return self._request('POST', '/events/track', data=data)

    def create_announcement(
        self,
        name: str,
        content: str,
        target_url_pattern: str,
        display_type: str = "modal",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        is_active: bool = False
    ) -> Dict[str, Any]:
        """
        새 공지사항 생성

        Args:
            name: 공지사항 이름
            content: 공지사항 내용
            target_url_pattern: 타겟 URL 패턴
            display_type: 표시 타입 (modal, banner, tooltip)
            start_date: 시작 날짜 (YYYY-MM-DD)
            end_date: 종료 날짜 (YYYY-MM-DD)
            is_active: 활성화 여부

        Returns:
            생성된 공지사항 정보
        """
        data = {
            'name': name,
            'content': content,
            'targetUrlPattern': target_url_pattern,
            'displayType': display_type,
            'isActive': is_active
        }

        if start_date:
            data['startDate'] = start_date
        if end_date:
            data['endDate'] = end_date

        return self._request('POST', '/announcements', data=data)

    def get_announcements(
        self,
        is_active: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        공지사항 목록 조회

        Args:
            is_active: 활성화 상태 필터
            limit: 반환할 항목 수
            offset: 오프셋

        Returns:
            공지사항 목록
        """
        params = {'limit': limit, 'offset': offset}
        if is_active is not None:
            params['isActive'] = is_active

        response = self._request('GET', '/announcements', params=params)
        return response.get('announcements', [])

    def get_analytics(
        self,
        start_date: str,
        end_date: str,
        content_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        분석 데이터 조회

        Args:
            start_date: 시작 날짜 (YYYY-MM-DD)
            end_date: 종료 날짜 (YYYY-MM-DD)
            content_type: 콘텐츠 타입 필터 (tour, tooltip, checklist)

        Returns:
            분석 데이터
        """
        params = {
            'startDate': start_date,
            'endDate': end_date
        }
        if content_type:
            params['contentType'] = content_type

        return self._request('GET', '/analytics', params=params)

    def close(self):
        """세션 종료"""
        self.session.close()
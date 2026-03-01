"""
Statuspage Client
서비스 상태 모니터링 API 클라이언트
"""

import requests
from typing import Optional, Dict, List, Any


class StatuspageClient:
    """
    Statuspage API 클라이언트

    서비스 상태 모니터링, 인시던트 관리, 메인테넌스 예약을 위한 클라이언트
    """

    def __init__(
        self,
        api_key: str,
        page_id: str,
        base_url: str = "https://api.statuspage.io/v1",
        timeout: int = 30
    ):
        """
        Statuspage 클라이언트 초기화

        Args:
            api_key: Statuspage API 키
            page_id: 상태페이지 ID
            base_url: API 기본 URL
            timeout: 요청 타임아웃 (초)
        """
        self.api_key = api_key
        self.page_id = page_id
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'OAuth {api_key}',
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

    def get_page_summary(self) -> Dict[str, Any]:
        """
        상태페이지 요약 조회

        Returns:
            페이지 요약 정보
        """
        return self._request('GET', f'/pages/{self.page_id}')

    def list_components(
        self,
        page_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        컴포넌트 목록 조회

        Args:
            page_id: 페이지 ID (선택 - 기본값은 초기화 시 설정)

        Returns:
            컴포넌트 목록
        """
        pid = page_id if page_id else self.page_id
        response = self._request('GET', f'/pages/{pid}/components')
        return response.get('components', [])

    def create_component(
        self,
        name: str,
        status: str = "operational",
        description: Optional[str] = None,
        only_show_if_degraded: bool = False,
        showcase: bool = False,
        group_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        컴포넌트 생성

        Args:
            name: 컴포넌트 이름
            status: 초기 상태 (operational, degraded, partial_outage, major_outage, under_maintenance)
            description: 설명
            only_show_if_degraded: 문제 발생 시에만 표시
            showcase: 메인 컴포넌트로 표시
            group_id: 그룹 ID

        Returns:
            생성된 컴포넌트 정보
        """
        data = {
            'component': {
                'name': name,
                'status': status,
                'only_show_if_degraded': only_show_if_degraded,
                'showcase': showcase
            }
        }

        if description:
            data['component']['description'] = description
        if group_id:
            data['component']['group_id'] = group_id

        return self._request('POST', f'/pages/{self.page_id}/components', data=data)

    def get_component(self, component_id: str) -> Dict[str, Any]:
        """
        컴포넌트 조회

        Args:
            component_id: 컴포넌트 ID

        Returns:
            컴포넌트 정보
        """
        return self._request('GET', f'/pages/{self.page_id}/components/{component_id}')

    def update_component(
        self,
        component_id: str,
        status: Optional[str] = None,
        description: Optional[str] = None,
        only_show_if_degraded: Optional[bool] = None,
        showcase: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        컴포넌트 업데이트

        Args:
            component_id: 컴포넌트 ID
            status: 새 상태
            description: 새 설명
            only_show_if_degraded: 표시 옵션
            showcase: 쇼케이스 옵션

        Returns:
            업데이트된 컴포넌트 정보
        """
        data = {'component': {}}

        if status:
            data['component']['status'] = status
        if description:
            data['component']['description'] = description
        if only_show_if_degraded is not None:
            data['component']['only_show_if_degraded'] = only_show_if_degraded
        if showcase is not None:
            data['component']['showcase'] = showcase

        return self._request('PATCH', f'/pages/{self.page_id}/components/{component_id}', data=data)

    def delete_component(self, component_id: str) -> Dict[str, Any]:
        """
        컴포넌트 삭제

        Args:
            component_id: 컴포넌트 ID

        Returns:
            삭제 결과
        """
        return self._request('DELETE', f'/pages/{self.page_id}/components/{component_id}')

    def create_incident(
        self,
        name: str,
        status: str = "investigating",
        body: Optional[str] = None,
        incident_updates: Optional[List[Dict[str, Any]]] = None,
        component_ids: Optional[List[str]] = None,
        components: Optional[Dict[str, str]] = None,
        deliver_notifications: bool = True,
        impact_override: Optional[str] = None,
        scheduled_for: Optional[str] = None,
        auto_transition_to_maintenance: bool = False,
        auto_transition_to_operational: bool = False
    ) -> Dict[str, Any]:
        """
        인시던트 생성

        Args:
            name: 인시던트 이름
            status: 상태 (investigating, identified, monitoring, resolved, scheduled, in_progress, verifying, completed)
            body: 설명
            incident_updates: 업데이트 목록
            component_ids: 영향받는 컴포넌트 ID 목록
            components: 컴포넌트 상태 맵 {id: status}
            deliver_notifications: 알림 전송 여부
            impact_override: 영향도 (critical, major, minor, none)
            scheduled_for: 예약 시간 (YYYY-MM-DDTHH:MM:SS)
            auto_transition_to_maintenance: 메인테넌스로 자동 전환
            auto_transition_to_operational: 정상 상태로 자동 전환

        Returns:
            생성된 인시던트 정보
        """
        data = {
            'incident': {
                'name': name,
                'status': status,
                'deliver_notifications': deliver_notifications
            }
        }

        if body:
            data['incident']['body'] = body
        if incident_updates:
            data['incident']['incident_updates'] = incident_updates
        if component_ids:
            data['incident']['component_ids'] = component_ids
        if components:
            data['incident']['components'] = components
        if impact_override:
            data['incident']['impact_override'] = impact_override
        if scheduled_for:
            data['incident']['scheduled_for'] = scheduled_for
        if auto_transition_to_maintenance:
            data['incident']['auto_transition_to_maintenance'] = auto_transition_to_maintenance
        if auto_transition_to_operational:
            data['incident']['auto_transition_to_operational'] = auto_transition_to_operational

        return self._request('POST', f'/pages/{self.page_id}/incidents', data=data)

    def get_incident(self, incident_id: str) -> Dict[str, Any]:
        """
        인시던트 조회

        Args:
            incident_id: 인시던트 ID

        Returns:
            인시던트 정보
        """
        return self._request('GET', f'/pages/{self.page_id}/incidents/{incident_id}')

    def list_incidents(
        self,
        status: Optional[str] = None,
        impact: Optional[str] = None,
        limit: int = 50,
        page: int = 1
    ) -> List[Dict[str, Any]]:
        """
        인시던트 목록 조회

        Args:
            status: 상태 필터
            impact: 영향도 필터
            limit: 반환할 항목 수
            page: 페이지 번호

        Returns:
            인시던트 목록
        """
        params = {'limit': limit, 'page': page}
        if status:
            params['status'] = status
        if impact:
            params['impact'] = impact

        response = self._request('GET', f'/pages/{self.page_id}/incidents', params=params)
        return response.get('incidents', [])

    def update_incident(
        self,
        incident_id: str,
        status: Optional[str] = None,
        name: Optional[str] = None,
        body: Optional[str] = None,
        component_ids: Optional[List[str]] = None,
        components: Optional[Dict[str, str]] = None,
        deliver_notifications: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        인시던트 업데이트

        Args:
            incident_id: 인시던트 ID
            status: 새 상태
            name: 새 이름
            body: 새 설명
            component_ids: 영향받는 컴포넌트 ID 목록
            components: 컴포넌트 상태 맵
            deliver_notifications: 알림 전송 여부

        Returns:
            업데이트된 인시던트 정보
        """
        data = {'incident': {}}

        if status:
            data['incident']['status'] = status
        if name:
            data['incident']['name'] = name
        if body:
            data['incident']['body'] = body
        if component_ids:
            data['incident']['component_ids'] = component_ids
        if components:
            data['incident']['components'] = components
        if deliver_notifications is not None:
            data['incident']['deliver_notifications'] = deliver_notifications

        return self._request('PATCH', f'/pages/{self.page_id}/incidents/{incident_id}', data=data)

    def delete_incident(self, incident_id: str) -> Dict[str, Any]:
        """
        인시던트 삭제

        Args:
            incident_id: 인시던트 ID

        Returns:
            삭제 결과
        """
        return self._request('DELETE', f'/pages/{self.page_id}/incidents/{incident_id}')

    def create_incident_update(
        self,
        incident_id: str,
        body: str,
        status: Optional[str] = None,
        deliver_notifications: bool = True
    ) -> Dict[str, Any]:
        """
        인시던트 업데이트 추가

        Args:
            incident_id: 인시던트 ID
            body: 업데이트 내용
            status: 새 상태
            deliver_notifications: 알림 전송 여부

        Returns:
            추가된 업데이트 정보
        """
        data = {
            'incident_update': {
                'body': body,
                'deliver_notifications': deliver_notifications
            }
        }

        if status:
            data['incident_update']['status'] = status

        return self._request('POST', f'/pages/{self.page_id}/incidents/{incident_id}/incident_updates', data=data)

    def list_incident_updates(
        self,
        incident_id: str
    ) -> List[Dict[str, Any]]:
        """
        인시던트 업데이트 목록 조회

        Args:
            incident_id: 인시던트 ID

        Returns:
            업데이트 목록
        """
        response = self._request('GET', f'/pages/{self.page_id}/incidents/{incident_id}/incident_updates')
        return response.get('incident_updates', [])

    def create_maintenance(
        self,
        name: str,
        scheduled_for: str,
        scheduled_until: str,
        status: str = "scheduled",
        body: Optional[str] = None,
        component_ids: Optional[List[str]] = None,
        components: Optional[Dict[str, str]] = None,
        auto_transition_to_operational: bool = False,
        auto_transition_to_in_progress: bool = False
    ) -> Dict[str, Any]:
        """
        메인테넌스 생성

        Args:
            name: 메인테넌스 이름
            scheduled_for: 시작 시간 (YYYY-MM-DDTHH:MM:SS)
            scheduled_until: 종료 시간 (YYYY-MM-DDTHH:MM:SS)
            status: 상태 (scheduled, in_progress, verifying, completed)
            body: 설명
            component_ids: 영향받는 컴포넌트 ID 목록
            components: 컴포넌트 상태 맵
            auto_transition_to_operational: 정상 상태로 자동 전환
            auto_transition_to_in_progress: 진행 중 상태로 자동 전환

        Returns:
            생성된 메인테넌스 정보
        """
        data = {
            'scheduled_maintenance': {
                'name': name,
                'scheduled_for': scheduled_for,
                'scheduled_until': scheduled_until,
                'status': status,
                'auto_transition_to_operational': auto_transition_to_operational,
                'auto_transition_to_in_progress': auto_transition_to_in_progress
            }
        }

        if body:
            data['scheduled_maintenance']['body'] = body
        if component_ids:
            data['scheduled_maintenance']['component_ids'] = component_ids
        if components:
            data['scheduled_maintenance']['components'] = components

        return self._request('POST', f'/pages/{self.page_id}/scheduled-maintenances', data=data)

    def list_maintenances(
        self,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        메인테넌스 목록 조회

        Args:
            status: 상태 필터
            limit: 반환할 항목 수

        Returns:
            메인테넌스 목록
        """
        params = {'limit': limit}
        if status:
            params['status'] = status

        response = self._request('GET', f'/pages/{self.page_id}/scheduled-maintenances', params=params)
        return response.get('scheduled_maintenances', [])

    def update_maintenance(
        self,
        maintenance_id: str,
        name: Optional[str] = None,
        status: Optional[str] = None,
        body: Optional[str] = None,
        scheduled_for: Optional[str] = None,
        scheduled_until: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        메인테넌스 업데이트

        Args:
            maintenance_id: 메인테넌스 ID
            name: 새 이름
            status: 새 상태
            body: 새 설명
            scheduled_for: 새 시작 시간
            scheduled_until: 새 종료 시간

        Returns:
            업데이트된 메인테넌스 정보
        """
        data = {'scheduled_maintenance': {}}

        if name:
            data['scheduled_maintenance']['name'] = name
        if status:
            data['scheduled_maintenance']['status'] = status
        if body:
            data['scheduled_maintenance']['body'] = body
        if scheduled_for:
            data['scheduled_maintenance']['scheduled_for'] = scheduled_for
        if scheduled_until:
            data['scheduled_maintenance']['scheduled_until'] = scheduled_until

        return self._request('PATCH', f'/pages/{self.page_id}/scheduled-maintenances/{maintenance_id}', data=data)

    def delete_maintenance(self, maintenance_id: str) -> Dict[str, Any]:
        """
        메인테넌스 삭제

        Args:
            maintenance_id: 메인테넌스 ID

        Returns:
            삭제 결과
        """
        return self._request('DELETE', f'/pages/{self.page_id}/scheduled-maintenances/{maintenance_id}')

    def get_subscribers(
        self,
        limit: int = 50,
        page: int = 1
    ) -> List[Dict[str, Any]]:
        """
        구독자 목록 조회

        Args:
            limit: 반환할 항목 수
            page: 페이지 번호

        Returns:
            구독자 목록
        """
        params = {'limit': limit, 'page': page}
        response = self._request('GET', f'/pages/{self.page_id}/subscribers', params=params)
        return response.get('subscribers', [])

    def close(self):
        """세션 종료"""
        self.session.close()
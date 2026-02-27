"""
Demio API Client
Webinar platform for virtual events
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import time


class DemioError(Exception):
    """Demio API 에러"""
    pass


class RateLimitError(DemioError):
    """Rate limit exceeded"""
    pass


class DemioClient:
    """
    Demio API Client
    Webinar hosting and registration automation
    """

    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.demio.com/v1"):
        """
        Demio API 클라이언트 초기화

        Args:
            api_key: Demio API key
            api_secret: Demio API secret
            base_url: API 기본 URL
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = (api_key, api_secret)
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests (10 requests/second)

    def _handle_rate_limit(self) -> None:
        """Rate limiting 처리"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)
        self.last_request_time = time.time()

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        API 요청 실행

        Args:
            method: HTTP 메서드 (GET, POST, PUT, DELETE)
            endpoint: API 엔드포인트
            params: 쿼리 파라미터
            data: 요청 본문 데이터

        Returns:
            API 응답

        Raises:
            DemioError: API 에러 발생 시
            RateLimitError: Rate limit 초과 시
        """
        self._handle_rate_limit()

        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=30
            )

            # Rate limit 처리
            if response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")

            response.raise_for_status()

            if response.text:
                return response.json()
            return {}

        except requests.exceptions.RequestException as e:
            if e.response:
                if e.response.status_code == 401:
                    raise DemioError("Invalid API credentials")
                elif e.response.status_code == 403:
                    raise DemioError("Access forbidden")
                elif e.response.status_code == 404:
                    raise DemioError("Resource not found")

            raise DemioError(f"API request failed: {str(e)}")

    def list_events(
        self,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        이벤트 목록 조회

        Args:
            status: 상태 필터 ('scheduled', 'completed', 'active', 'cancelled')
            limit: 반환할 최대 결과 수
            offset: 페이지 오프셋

        Returns:
            이벤트 목록
            {
                "events": [
                    {
                        "id": int,
                        "name": str,
                        "status": str,
                        "start_date": str,
                        "end_date": str,
                        "timezone": str,
                        "is_recurring": bool,
                        "registrants_count": int,
                        "attendees_count": int
                    },
                    ...
                ],
                "total": int
            }
        """
        params = {}

        if status:
            params['status'] = status

        if limit:
            params['limit'] = limit

        if offset:
            params['offset'] = offset

        return self._make_request('GET', '/events', params=params)

    def get_event(self, event_id: int) -> Dict[str, Any]:
        """
        이벤트 상세 정보 조회

        Args:
            event_id: 이벤트 ID

        Returns:
            이벤트 상세 정보
            {
                "id": int,
                "name": str,
                "description": str,
                "status": str,
                "start_date": str,
                "end_date": str,
                "timezone": str,
                "duration": int,
                "registration_link": str,
                "registrants_count": int,
                "attendees_count": int,
                "is_recurring": bool,
                "presenter": dict,
                "rooms": list
            }
        """
        return self._make_request('GET', f'/events/{event_id}')

    def list_event_participants(
        self,
        event_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        이벤트 참여자 목록 조회

        Args:
            event_id: 이벤트 ID
            limit: 반환할 최대 결과 수
            offset: 페이지 오프셋

        Returns:
            참여자 목록
            {
                "participants": [
                    {
                        "uuid": str,
                        "name": str,
                        "email": str,
                        "first_name": str,
                        "last_name": str,
                        "joined_at": str,
                        "left_at": str,
                        "attendance_duration": int,
                        "is_attended": bool,
                        "join_link": str
                    },
                    ...
                ],
                "total": int
            }
        """
        params = {}

        if limit:
            params['limit'] = limit

        if offset:
            params['offset'] = offset

        return self._make_request('GET', f'/events/{event_id}/participants', params=params)

    def get_event_registrants(
        self,
        event_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        이벤트 등록자 목록 조회

        Args:
            event_id: 이벤트 ID
            limit: 반환할 최대 결과 수
            offset: 페이지 오프셋

        Returns:
            등록자 목록
            {
                "registrants": [
                    {
                        "uuid": str,
                        "name": str,
                        "email": str,
                        "first_name": str,
                        "last_name": str,
                        "registered_at": str,
                        "join_link": str,
                        "attended": bool
                    },
                    ...
                ],
                "total": int
            }
        """
        params = {}

        if limit:
            params['limit'] = limit

        if offset:
            params['offset'] = offset

        return self._make_request('GET', f'/events/{event_id}/registrants', params=params)

    def register_event_participant(
        self,
        event_id: int,
        email: str,
        name: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        이벤트 참여자 등록

        Args:
            event_id: 이벤트 ID
            email: 참여자 이메일
            name: 참여자 이름
            first_name: 이름 (선택, name과 우선시)
            last_name: 성 (선택)
            custom_fields: 커스텀 필드 사전

        Returns:
            등록 결과
            {
                "uuid": str,
                "name": str,
                "email": str,
                "join_link": str,
                "registered_at": str
            }
        """
        data = {
            'email': email,
            'name': name
        }

        if first_name:
            data['firstName'] = first_name

        if last_name:
            data['lastName'] = last_name

        if custom_fields:
            data['customFields'] = custom_fields

        return self._make_request('POST', f'/events/{event_id}/register', data=data)

    def cancel_registration(self, event_id: int, email: str) -> Dict[str, Any]:
        """
        참여자 등록 취소

        Args:
            event_id: 이벤트 ID
            email: 참여자 이메일

        Returns:
            취소 결과
        """
        return self._make_request('POST', f'/events/{event_id}/registrations/cancel', data={'email': email})

    def get_upcoming_events(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        다가오는 이벤트 목록 조회

        Args:
            limit: 반환할 최대 결과 수

        Returns:
            다가오는 이벤트 목록
        """
        return self.list_events(status='scheduled', limit=limit)

    def get_completed_events(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        완료된 이벤트 목록 조회

        Args:
            limit: 반환할 최대 결과 수

        Returns:
            완료된 이벤트 목록
        """
        return self.list_events(status='completed', limit=limit)


if __name__ == "__main__":
    import os

    # 테스트 코드
    api_key = os.environ.get('DEMIO_API_KEY', 'your-api-key')
    api_secret = os.environ.get('DEMIO_API_SECRET', 'your-api-secret')
    client = DemioClient(api_key, api_secret)

    try:
        # 이벤트 목록 조회 테스트
        events = client.list_events(status='scheduled', limit=5)
        print("Events:", events)

        # 특정 이벤트 조회 테스트
        if events.get('events'):
            event_id = events['events'][0]['id']
            event = client.get_event(event_id)
            print("Event details:", event)

            # 참여자 목록 조회 테스트
            participants = client.list_event_participants(event_id)
            print("Participants:", participants)

            # 등록자 목록 조회 테스트
            registrants = client.get_event_registrants(event_id)
            print("Registrants:", registrants)

            # 새 참여자 등록 테스트
            registration_result = client.register_event_participant(
                event_id=event_id,
                email='new@example.com',
                name='New Participant'
            )
            print("Registration result:", registration_result)

    except Exception as e:
        print(f"Error: {str(e)}")
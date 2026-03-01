"""
Customer.io API Client
Customer engagement and automation platform
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import time


class CustomerIOError(Exception):
    """Customer.io API 에러"""
    pass


class RateLimitError(CustomerIOError):
    """Rate limit exceeded"""
    pass


class CustomerIOClient:
    """
    Customer.io API Client
    Customer data, segmentation, and event tracking
    """

    def __init__(
        self,
        site_id: str,
        api_key: str,
        region: str = "us",  # 'us' or 'eu'
        base_url: Optional[str] = None
    ):
        """
        Customer.io API 클라이언트 초기화

        Args:
            site_id: Customer.io Site ID
            api_key: Customer.io API key
            region: 리전 ('us' or 'eu')
            base_url: API 기본 URL (None이면 자동 설정)
        """
        self.site_id = site_id
        self.api_key = api_key
        self.region = region

        if base_url:
            self.base_url = base_url
        else:
            if region == "eu":
                self.base_url = "https://api-eu.customer.io/v1"
            else:
                self.base_url = "https://api.customer.io/v1"

        self.session = requests.Session()
        self.session.auth = (site_id, api_key)
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.last_request_time = 0
        self.min_request_interval = 0.05  # 60ms between requests

        # Track API URL
        if region == "eu":
            self.track_url = "https://track-eu.customer.io/v1"
        else:
            self.track_url = "https://track.customer.io/v1"

        self.track_session = requests.Session()
        self.track_session.auth = (site_id, api_key)
        self.track_session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

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
        use_track_api: bool = False,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        API 요청 실행

        Args:
            method: HTTP 메서드 (GET, POST, PUT, DELETE)
            endpoint: API 엔드포인트
            use_track_api: Track API 사용 여부
            params: 쿼리 파라미터
            data: 요청 본문 데이터

        Returns:
            API 응답

        Raises:
            CustomerIOError: API 에러 발생 시
            RateLimitError: Rate limit 초과 시
        """
        self._handle_rate_limit()

        if use_track_api:
            url = f"{self.track_url}{endpoint}"
            session = self.track_session
        else:
            url = f"{self.base_url}{endpoint}"
            session = self.session

        try:
            response = session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=30
            )

            # Rate limit 처리
            if response.status_code == 429:
                retry_after = response.headers.get('Retry-After', 10)
                raise RateLimitError(f"Rate limit exceeded. Retry after {retry_after} seconds")

            response.raise_for_status()

            if response.text:
                return response.json()
            return {}

        except requests.exceptions.RequestException as e:
            if e.response:
                if e.response.status_code == 401:
                    raise CustomerIOError("Invalid API credentials")
                elif e.response.status_code == 404:
                    raise CustomerIOError("Resource not found")
                elif e.response.status_code == 422:
                    error_data = e.response.json() if e.response.text else {}
                    raise CustomerIOError(f"Validation error: {error_data}")

            raise CustomerIOError(f"API request failed: {str(e)}")

    def create_customer(
        self,
        id: str,
        email: Optional[str] = None,
        name: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        created_at: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        고객 생성

        Args:
            id: 고객 ID (필수, 변경 불가)
            email: 이메일 주소
            name: 이름
            attributes: 추가 속성 사전
            created_at: 생성 날짜 (Unix timestamp)

        Returns:
            생성된 고객 정보
        """
        data = {'id': id}

        if email:
            data['email'] = email

        if name:
            data['name'] = name

        if attributes:
            data.update(attributes)

        if created_at:
            data['created_at'] = created_at

        return self._make_request('PUT', f'/customers/{id}', data=data)

    def update_customer(
        self,
        id: str,
        email: Optional[str] = None,
        name: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        고객 정보 업데이트

        Args:
            id: 고객 ID
            email: 새 이메일
            name: 새 이름
            attributes: 업데이트할 속성

        Returns:
            업데이트된 고객 정보
        """
        data = {}

        if email:
            data['email'] = email

        if name:
            data['name'] = name

        if attributes:
            data.update(attributes)

        return self._make_request('PUT', f'/customers/{id}', data=data)

    def delete_customer(self, id: str) -> Dict[str, Any]:
        """
        고객 삭제

        Args:
            id: 고객 ID

        Returns:
            삭제 결과
        """
        return self._make_request('DELETE', f'/customers/{id}')

    def get_customer(self, id: str) -> Dict[str, Any]:
        """
        고객 정보 조회

        Args:
            id: 고객 ID

        Returns:
            고객 상세 정보
        """
        return self._make_request('GET', f'/customers/{id}')

    def add_customer_to_segment(
        self,
        customer_id: str,
        segment_id: int
    ) -> Dict[str, Any]:
        """
        수동 세그먼트에 고객 추가

        Args:
            customer_id: 고객 ID
            segment_id: 세그먼트 ID

        Returns:
            결과
        """
        return self._make_request(
            'POST',
            f'/customers/{customer_id}/segments/{segment_id}'
        )

    def remove_customer_from_segment(
        self,
        customer_id: str,
        segment_id: int
    ) -> Dict[str, Any]:
        """
        수동 세그먼트에서 고객 삭제

        Args:
            customer_id: 고객 ID
            segment_id: 세그먼트 ID

        Returns:
            결과
        """
        return self._make_request(
            'DELETE',
            f'/customers/{customer_id}/segments/{segment_id}'
        )

    def track_customer_event(
        self,
        customer_id: str,
        name: str,
        data: Optional[Dict[str, Any]] = None,
        timestamp: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        고객 이벤트 추적

        Args:
            customer_id: 고객 ID
            name: 이벤트 이름
            data: 이벤트 데이터
            timestamp: 이벤트 타임스탬프 (Unix timestamp)

        Returns:
            추적 결과
        """
        event_data = {
            'name': name
        }

        if data:
            event_data['data'] = data

        if timestamp:
            event_data['timestamp'] = timestamp

        return self._make_request(
            'POST',
            f'/customers/{customer_id}/events',
            data=event_data,
            use_track_api=True
        )

    def track_anonymous_event(
        self,
        name: str,
        data: Optional[Dict[str, Any]] = None,
        timestamp: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        익명 이벤트 추적 (이름 없는 사용자 이벤트)

        Args:
            name: 이벤트 이름
            data: 이벤트 데이터
            timestamp: 이벤트 타임스탬프 (Unix timestamp)

        Returns:
            추적 결과
        """
        event_data = {
            'name': name
        }

        if data:
            event_data['data'] = data

        if timestamp:
            event_data['timestamp'] = timestamp

        return self._make_request(
            'POST',
            '/events',
            data=event_data,
            use_track_api=True
        )

    def submit_form(
        self,
        form_id: int,
        customer_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        폼 제출

        Args:
            form_id: 폼 ID
            customer_id: 고객 ID
            data: 폼 데이터

        Returns:
            제출 결과
        """
        form_data = {
            'data': data
        }

        return self._make_request(
            'POST',
            f'/forms/{form_id}/submitions',
            data=form_data
        )

    def list_customers(
        self,
        limit: Optional[int] = None,
        start: Optional[str] = None,
        email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        고객 목록 조회

        Args:
            limit: 반환할 최대 결과 수
            start: 페이징 시작점 (고객 ID)
            email: 이메일로 필터링

        Returns:
            고객 목록
        """
        params = {}

        if limit:
            params['limit'] = limit

        if start:
            params['start'] = start

        if email:
            params['email'] = email

        return self._make_request('GET', '/customers', params=params)

    def get_customer_activities(
        self,
        customer_id: str,
        limit: Optional[int] = None,
        start: Optional[str] = None,
        type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        고객 활동 내역 조회

        Args:
            customer_id: 고객 ID
            limit: 반환할 최대 결과 수
            start: 페이징 시작점
            type: 활동 타입 필터
                ('email_actioned', 'email_opened', 'email_clicked', etc.)

        Returns:
            활동 목록
        """
        params = {}

        if limit:
            params['limit'] = limit

        if start:
            params['start'] = start

        if type:
            params['type'] = type

        return self._make_request('GET', f'/customers/{customer_id}/activities', params=params)


def create_customerio_client(
    site_id: str,
    api_key: str,
    region: str = "us"
) -> CustomerIOClient:
    """
    Customer.io 클라이언트 생성 (Factory function)

    Args:
        site_id: Customer.io Site ID
        api_key: Customer.io API key
        region: 리전 ('us' or 'eu')

    Returns:
        CustomerIOClient 인스턴스
    """
    return CustomerIOClient(site_id, api_key, region)


if __name__ == "__main__":
    import os

    # 테스트 코드
    site_id = os.environ.get('CUSTOMERIO_SITE_ID', 'your-site-id')
    api_key = os.environ.get('CUSTOMERIO_API_KEY', 'your-api-key')
    client = create_customerio_client(site_id, api_key)

    try:
        # 고객 생성 테스트
        result = client.create_customer(
            id='customer_123',
            email='test@example.com',
            name='Test User',
            attributes={'plan': 'premium', 'signup_date': '2026-02-28'}
        )
        print("Created customer:", result)

        # 고객 업데이트 테스트
        update_result = client.update_customer(
            id='customer_123',
            attributes={'last_login': '2026-02-28'}
        )
        print("Updated customer:", update_result)

        # 이벤트 추적 테스트
        event_result = client.track_customer_event(
            customer_id='customer_123',
            name='purchase_completed',
            data={'amount': 99.99, 'product': 'Premium Plan'}
        )
        print("Tracked event:", event_result)

        # 익명 이벤트 추적 테스트
        anon_result = client.track_anonymous_event(
            name='page_viewed',
            data={'page': '/pricing', 'referrer': 'google.com'}
        )
        print("Tracked anonymous event:", anon_result)

        # 세그먼트 추가 테스트
        segment_result = client.add_customer_to_segment(
            customer_id='customer_123',
            segment_id=1
        )
        print("Added to segment:", segment_result)

        # 세그먼트 삭제 테스트
        remove_result = client.remove_customer_from_segment(
            customer_id='customer_123',
            segment_id=1
        )
        print("Removed from segment:", remove_result)

        # 고객 삭제 테스트
        delete_result = client.delete_customer(id='customer_123')
        print("Deleted customer:", delete_result)

    except Exception as e:
        print(f"Error: {str(e)}")
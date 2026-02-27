"""
Cuenote SMS API Client
Japanese SMS marketing service
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import time


class CuenoteSMSError(Exception):
    """Cuenote SMS API 에러"""
    pass


class RateLimitError(CuenoteSMSError):
    """Rate limit exceeded"""
    pass


class CuenoteSMSClient:
    """
    Cuenote SMS API Client
    Address book management and SMS delivery in Japan
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://api.cuenote.jp/api/v1"
    ):
        """
        Cuenote SMS API 클라이언트 초기화

        Args:
            api_key: Cuenote API key
            api_secret: Cuenote API secret
            base_url: API 기본 URL
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = (api_key, api_secret)
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests

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
            CuenoteSMSError: API 에러 발생 시
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
                    raise CuenoteSMSError("Invalid API credentials")
                elif e.response.status_code == 403:
                    raise CuenoteSMSError("Access forbidden")
                elif e.response.status_code == 404:
                    raise CuenoteSMSError("Resource not found")

            raise CuenoteSMSError(f"API request failed: {str(e)}")

    def create_address_book(
        self,
        name: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        주소록 생성

        Args:
            name: 주소록 이름
            description: 주소록 설명

        Returns:
            생성된 주소록 정보
            {
                "addressBookId": str,
                "name": str,
                "description": str,
                "createdAt": str
            }
        """
        data = {'name': name}

        if description:
            data['description'] = description

        return self._make_request('POST', '/addressbooks', data=data)

    def list_address_books(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        주소록 목록 조회

        Args:
            limit: 반환할 최대 결과 수
            offset: 페이지 오프셋

        Returns:
            주소록 목록
            {
                "addressBooks": [
                    {
                        "addressBookId": str,
                        "name": str,
                        "description": str,
                        "count": int,
                        "createdAt": str
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

        return self._make_request('GET', '/addressbooks', params=params)

    def get_address_book(self, address_book_id: str) -> Dict[str, Any]:
        """
        주소록 상세 정보 조회

        Args:
            address_book_id: 주소록 ID

        Returns:
            주소록 상세 정보
        """
        return self._make_request('GET', f'/addressbooks/{address_book_id}')

    def update_address_book(
        self,
        address_book_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        주소록 업데이트

        Args:
            address_book_id: 주소록 ID
            name: 새 이름
            description: 새 설명

        Returns:
            업데이트된 주소록 정보
        """
        data = {}

        if name:
            data['name'] = name

        if description:
            data['description'] = description

        return self._make_request('PUT', f'/addressbooks/{address_book_id}', data=data)

    def delete_address_book(self, address_book_id: str) -> Dict[str, Any]:
        """
        주소록 삭제

        Args:
            address_book_id: 주소록 ID

        Returns:
            삭제 결과
        """
        return self._make_request('DELETE', f'/addressbooks/{address_book_id}')

    def create_sms_delivery_phone_numbers(
        self,
        phone_numbers: List[str],
        message: str,
        scheduled_at: Optional[str] = None,
        track_urls: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        전화번호로 SMS 배포 생성

        Args:
            phone_numbers: 전화번호 목록 (국가 코드 포함, 예: ["+819012345678"])
            message: 메시지 내용
            scheduled_at: 예약 시간 (ISO 8601 format)
            track_urls: URL 추적 사용 여부

        Returns:
            배포 결과
            {
                "deliveryId": str,
                "status": str,  # scheduled, sent, completed, failed
                "messageCount": int,
                "createdAt": str,
                "scheduledAt": str
            }
        """
        data = {
            'phoneNumbers': phone_numbers,
            'message': message
        }

        if scheduled_at:
            data['scheduledAt'] = scheduled_at

        if track_urls is not None:
            data['trackUrls'] = track_urls

        return self._make_request('POST', '/deliveries/sms', data=data)

    def create_sms_delivery_address_book(
        self,
        address_book_id: str,
        message: str,
        scheduled_at: Optional[str] = None,
        track_urls: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        주소록을 사용하여 SMS 배포 생성

        Args:
            address_book_id: 주소록 ID
            message: 메시지 내용
            scheduled_at: 예약 시간 (ISO 8601 format)
            track_urls: URL 추적 사용 여부

        Returns:
            배포 결과
        """
        data = {
            'addressBookId': address_book_id,
            'message': message
        }

        if scheduled_at:
            data['scheduledAt'] = scheduled_at

        if track_urls is not None:
            data['trackUrls'] = track_urls

        return self._make_request('POST', '/deliveries/sms', data=data)

    def update_sms_delivery(
        self,
        delivery_id: str,
        phone_numbers: Optional[List[str]] = None,
        message: Optional[str] = None,
        scheduled_at: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        SMS 배포 업데이트 (예약 전에만 가능)

        Args:
            delivery_id: 배포 ID
            phone_numbers: 새 전화번호 목록
            message: 새 메시지
            scheduled_at: 새 예약 시간

        Returns:
            업데이트된 배포 정보
        """
        data = {}

        if phone_numbers:
            data['phoneNumbers'] = phone_numbers

        if message:
            data['message'] = message

        if scheduled_at:
            data['scheduledAt'] = scheduled_at

        return self._make_request('PUT', f'/deliveries/{delivery_id}', data=data)

    def get_delivery(self, delivery_id: str) -> Dict[str, Any]:
        """
        배포 상세 정보 조회

        Args:
            delivery_id: 배포 ID

        Returns:
            배포 상세 정보
            {
                "deliveryId": str,
                "status": str,
                "message": str,
                "totalRecipients": int,
                "sentCount": int,
                "deliveredCount": int,
                "failedCount": int,
                "createdAt": str,
                "scheduledAt": str,
                "completedAt": str
            }
        """
        return self._make_request('GET', f'/deliveries/{delivery_id}')

    def search_deliveries(
        self,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        배포 검색

        Args:
            status: 상태 필터 ('scheduled', 'sent', 'completed', 'failed')
            limit: 반환할 최대 결과 수
            offset: 페이지 오프셋
            date_from: 시작 날짜 (ISO 8601 format)
            date_to: 종료 날짜 (ISO 8601 format)

        Returns:
            배포 목록
            {
                "deliveries": [
                    {
                        "deliveryId": str,
                        "status": str,
                        "message": str,
                        "totalRecipients": int,
                        "createdAt": str
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

        if date_from:
            params['dateFrom'] = date_from

        if date_to:
            params['dateTo'] = date_to

        return self._make_request('GET', '/deliveries', params=params)

    def add_recipient_to_address_book(
        self,
        address_book_id: str,
        phone_number: str,
        name: Optional[str] = None,
        attributes: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        주소록에 수신자 추가

        Args:
            address_book_id: 주소록 ID
            phone_number: 전화번호
            name: 이름
            attributes: 추가 속성

        Returns:
            추가 결과
        """
        data = {
            'phoneNumber': phone_number
        }

        if name:
            data['name'] = name

        if attributes:
            data['attributes'] = attributes

        return self._make_request(
            'POST',
            f'/addressbooks/{address_book_id}/recipients',
            data=data
        )

    def get_delivery_recipients(
        self,
        delivery_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        배포 수신자 목록 조회

        Args:
            delivery_id: 배포 ID
            limit: 반환할 최대 결과 수
            offset: 페이지 오프셋

        Returns:
            수신자 목록
            {
                "recipients": [
                    {
                        "recipientId": str,
                        "phoneNumber": str,
                        "status": str,  # sent, delivered, failed
                        "deliveredAt": str,
                        "errorMessage": str
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

        return self._make_request('GET', f'/deliveries/{delivery_id}/recipients', params=params)


def create_cuenote_sms_client(api_key: str, api_secret: str) -> CuenoteSMSClient:
    """
    Cuenote SMS 클라이언트 생성 (Factory function)

    Args:
        api_key: Cuenote API key
        api_secret: Cuenote API secret

    Returns:
        CuenoteSMSClient 인스턴스
    """
    return CuenoteSMSClient(api_key, api_secret)


if __name__ == "__main__":
    import os

    # 테스트 코드
    api_key = os.environ.get('CUENOTE_API_KEY', 'your-api-key')
    api_secret = os.environ.get('CUENOTE_API_SECRET', 'your-api-secret')
    client = create_cuenote_sms_client(api_key, api_secret)

    try:
        # 주소록 생성 테스트
        address_book = client.create_address_book(
            name='Test Customers',
            description='Test address book'
        )
        print("Created address book:", address_book)

        address_book_id = address_book.get('addressBookId')

        # 주소록 목록 조회 테스트
        list_result = client.list_address_books(limit=10)
        print("Address books:", list_result)

        # 주소록 상세 조회 테스트
        detail_result = client.get_address_book(address_book_id)
        print("Address book detail:", detail_result)

        # SMS 배포 생성 테스트
        delivery_result = client.create_sms_delivery_phone_numbers(
            phone_numbers=['+819012345678'],
            message='Test message from API',
            scheduled_at='2026-02-28T10:00:00Z'
        )
        print("Created delivery:", delivery_result)

        delivery_id = delivery_result.get('deliveryId')

        # 배포 조회 테스트
        get_delivery = client.get_delivery(delivery_id)
        print("Delivery details:", get_delivery)

        # 배포 검색 테스트
        search_result = client.search_deliveries(status='scheduled', limit=5)
        print("Search results:", search_result)

        # 배포 업데이트 테스트
        update_result = client.update_sms_delivery(
            delivery_id=delivery_id,
            scheduled_at='2026-02-28T12:00:00Z'
        )
        print("Updated delivery:", update_result)

        # 주소록 업데이트 테스트
        update_book = client.update_address_book(
            address_book_id=address_book_id,
            name='Updated Name'
        )
        print("Updated address book:", update_book)

        # 주소록 삭제 테스트
        delete_book = client.delete_address_book(address_book_id)
        print("Deleted address book:", delete_book)

    except Exception as e:
        print(f"Error: {str(e)}")
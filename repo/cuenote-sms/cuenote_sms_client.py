import requests
import time
from typing import Dict, List, Optional
from datetime import datetime


class CuenoteSMSAPIError(Exception):
    """Cuenote SMS API 에러"""
    pass


class CuenoteSMSRateLimitError(CuenoteSMSAPIError):
    """Rate limit 초과 에러"""
    pass


class CuenoteSMSClient:
    """
    Cuenote SMS API Client

    API key authentication을 사용합니다.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.cuenote.jp/api/v1",
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """
        Cuenote SMS 클라이언트 초기화

        Args:
            api_key: API key
            base_url: API 베이스 URL
            timeout: 요청 타임아웃 (초)
            max_retries: 최대 재시도 횟수
            retry_delay: 재시도 간 지연 (초)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # Rate limiting
        self._last_request_time = 0
        self._min_request_interval = 0.1  # 최소 요청 간격 (초)

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Dict:
        """
        API 요청 전송 (재시도 및 rate limiting 포함)

        Returns:
            API 응답
        Raises:
            CuenoteSMSAPIError: API 오류
            CuenoteSMSRateLimitError: Rate limit 초과
        """
        current_time = time.time()
        time_since_last_request = current_time - self._last_request_time
        if time_since_last_request < self._min_request_interval:
            time.sleep(self._min_request_interval - time_since_last_request)

        url = f"{self.base_url}{endpoint}"

        request_headers = {
            'X-Cuenote-API-Key': self.api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if headers:
            request_headers.update(headers)

        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    json=json_data,
                    headers=request_headers,
                    timeout=self.timeout
                )

                self._last_request_time = time.time()

                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', self.retry_delay))
                    if attempt < self.max_retries - 1:
                        time.sleep(retry_after)
                        continue
                    else:
                        raise CuenoteSMSRateLimitError(
                            f"Rate limit exceeded. Retry after {retry_after} seconds"
                        )

                if not response.ok:
                    error_data = response.text
                    try:
                        error_data = response.json()
                    except ValueError:
                        pass
                    raise CuenoteSMSAPIError(
                        f"API error {response.status_code}: {error_data}"
                    )

                return response.json()

            except requests.exceptions.RequestException as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                else:
                    raise CuenoteSMSAPIError(f"Request failed: {str(e)}")

        raise CuenoteSMSAPIError(f"Max retries exceeded: {str(last_error)}")

    # ===== ADDRESS BOOK ACTIONS =====

    def get_address_book(self, address_book_id: str) -> Dict:
        """
        주소록 가져오기

        Args:
            address_book_id: 주소록 ID

        Returns:
            주소록 정보
        """
        if not address_book_id:
            raise ValueError("address_book_id is required")

        return self._make_request('GET', f'/address-books/{address_book_id}')

    def list_address_books(
        self,
        limit: int = 100,
        offset: int = 0,
        name: Optional[str] = None
    ) -> Dict:
        """
        주소록 목록 가져오기

        Args:
            limit: 최대 반환 개수
            offset: 오프셋
            name: 이름으로 필터링

        Returns:
            주소록 목록
        """
        params = {
            'limit': min(limit, 1000),
            'offset': offset
        }
        if name:
            params['name'] = name

        return self._make_request('GET', '/address-books', params=params)

    def create_address_book(
        self,
        name: str,
        description: Optional[str] = None
    ) -> Dict:
        """
        주소록 생성

        Args:
            name: 주소록 이름
            description: 설명

        Returns:
            생성된 주소록 정보
        """
        if not name:
            raise ValueError("name is required")

        data = {'name': name}
        if description:
            data['description'] = description

        return self._make_request('POST', '/address-books', json_data=data)

    def update_address_book(
        self,
        address_book_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict:
        """
        주소록 업데이트

        Args:
            address_book_id: 주소록 ID
            name: 새 이름
            description: 새 설명

        Returns:
            업데이트된 주소록 정보
        """
        if not address_book_id:
            raise ValueError("address_book_id is required")

        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description

        if not data:
            raise ValueError("At least one field to update is required")

        return self._make_request('PUT', f'/address-books/{address_book_id}', json_data=data)

    def delete_address_book(self, address_book_id: str) -> Dict:
        """
        주소록 삭제

        Args:
            address_book_id: 주소록 ID

        Returns:
            삭제 결과
        """
        if not address_book_id:
            raise ValueError("address_book_id is required")

        return self._make_request('DELETE', f'/address-books/{address_book_id}')

    # ===== SMS DELIVERY ACTIONS =====

    def get_delivery(self, delivery_id: str) -> Dict:
        """
        배송 가져오기

        Args:
            delivery_id: 배송 ID

        Returns:
            배송 정보
        """
        if not delivery_id:
            raise ValueError("delivery_id is required")

        return self._make_request('GET', f'/deliveries/{delivery_id}')

    def search_deliveries(
        self,
        address_book_id: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict:
        """
        배송 검색

        Args:
            address_book_id: 주소록 ID로 필터링
            status: 상태로 필터링
            start_date: 시작 날짜 (YYYY-MM-DD)
            end_date: 종료 날짜 (YYYY-MM-DD)
            limit: 최대 반환 개수
            offset: 오프셋

        Returns:
            배송 목록
        """
        params = {
            'limit': min(limit, 1000),
            'offset': offset
        }

        if address_book_id:
            params['address_book_id'] = address_book_id
        if status:
            params['status'] = status
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date

        return self._make_request('GET', '/deliveries', params=params)

    def create_sms_delivery_by_phone_numbers(
        self,
        message: str,
        phone_numbers: List[str],
        sender: Optional[str] = None,
        send_at: Optional[str] = None,
        tracking_id: Optional[str] = None
    ) -> Dict:
        """
        SMS 배송 생성 (전화번호)

        Args:
            message: 메시지 내용
            phone_numbers: 전화번호 목록
            sender: 발신자 번호 (선택사항)
            send_at: 예약 발송 시간 (YYYY-MM-DD HH:MM:SS)
            tracking_id: 추적 ID

        Returns:
            생성된 배송 정보
        """
        if not message:
            raise ValueError("message is required")
        if not phone_numbers or len(phone_numbers) == 0:
            raise ValueError("phone_numbers is required and must not be empty")

        data = {
            'message': message,
            'phone_numbers': phone_numbers
        }

        if sender:
            data['sender'] = sender
        if send_at:
            data['send_at'] = send_at
        if tracking_id:
            data['tracking_id'] = tracking_id

        return self._make_request('POST', '/deliveries', json_data=data)

    def update_sms_delivery_by_phone_numbers(
        self,
        delivery_id: str,
        phone_numbers: Optional[List[str]] = None,
        message: Optional[str] = None,
        send_at: Optional[str] = None
    ) -> Dict:
        """
        SMS 배송 업데이트 (전화번호)

        Args:
            delivery_id: 배송 ID
            phone_numbers: 전화번호 목록 (추가/제거)
            message: 메시지 내용
            send_at: 예약 발송 시간 변경

        Returns:
            업데이트된 배송 정보
        """
        if not delivery_id:
            raise ValueError("delivery_id is required")

        data = {}
        if phone_numbers:
            data['phone_numbers'] = phone_numbers
        if message:
            data['message'] = message
        if send_at:
            data['send_at'] = send_at

        if not data:
            raise ValueError("At least one field to update is required")

        return self._make_request('PUT', f'/deliveries/{delivery_id}', json_data=data)

    # ===== CLOSE =====

    def close(self):
        """
        클라이언트 리소스 정리
        """
        self.session = None
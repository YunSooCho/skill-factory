import requests
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class CloudContactAPIError(Exception):
    """CloudContact API 에러"""
    pass


class CloudContactRateLimitError(CloudContactAPIError):
    """Rate limit 초과 에러"""
    pass


class CloudContactClient:
    """
    CloudContact AI API Client

    API key authentication을 사용합니다.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.cloudcontact.ai/v1",
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """
        CloudContact AI 클라이언트 초기화

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

        Args:
            method: HTTP 메서드 (GET, POST, PUT, DELETE)
            endpoint: API 엔드포인트
            params: 쿼리 파라미터
            data: 폼 데이터
            json_data: JSON body
            headers: 추가 헤더

        Returns:
            API 응답 (字典)

        Raises:
            CloudContactAPIError: API 오류 발생 시
            CloudContactRateLimitError: Rate limit 초과 시
        """
        # Rate limiting
        current_time = time.time()
        time_since_last_request = current_time - self._last_request_time
        if time_since_last_request < self._min_request_interval:
            time.sleep(self._min_request_interval - time_since_last_request)

        url = f"{self.base_url}{endpoint}"

        request_headers = {
            'Authorization': f'Bearer {self.api_key}',
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

                # Rate limit 체크 (HTTP 429)
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', self.retry_delay))
                    if attempt < self.max_retries - 1:
                        time.sleep(retry_after)
                        continue
                    else:
                        raise CloudContactRateLimitError(
                            f"Rate limit exceeded. Retry after {retry_after} seconds"
                        )

                # 오류 응답 처리
                if not response.ok:
                    error_data = response.text
                    try:
                        error_data = response.json()
                    except ValueError:
                        pass
                    raise CloudContactAPIError(
                        f"API error {response.status_code}: {error_data}"
                    )

                return response.json()

            except requests.exceptions.RequestException as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                else:
                    raise CloudContactAPIError(f"Request failed: {str(e)}")

        raise CloudContactAPIError(f"Max retries exceeded: {str(last_error)}")

    # ===== CONTACT ACTIONS =====

    def create_contact(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        company: Optional[str] = None,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
        custom_fields: Optional[Dict] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        새로운 연락처 생성

        Args:
            name: 전체 이름
            email: 이메일 주소
            phone: 전화번호
            first_name: 이름
            last_name: 성
            company: 회사명
            title: 직함
            tags: 태그 목록
            custom_fields: 커스텀 필드
            metadata: 추가 메타데이터

        Returns:
            생성된 연락처 정보

        Raises:
            CloudContactAPIError: API 오류 발생 시
        """
        data = {}

        if name:
            data['name'] = name
        if email:
            data['email'] = email
        if phone:
            data['phone'] = phone
        if first_name:
            data['first_name'] = first_name
        if last_name:
            data['last_name'] = last_name
        if company:
            data['company'] = company
        if title:
            data['title'] = title
        if tags:
            data['tags'] = tags
        if custom_fields:
            data['custom_fields'] = custom_fields
        if metadata:
            data['metadata'] = metadata

        if not data:
            raise ValueError("At least one field is required")

        return self._make_request('POST', '/contacts', json_data=data)

    def search_contacts(
        self,
        query: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None
    ) -> Dict:
        """
        연락처 검색

        Args:
            query: 전체 텍스트 검색 쿼리
            email: 이메일로 필터링
            phone: 전화번호로 필터링
            company: 회사명으로 필터링
            tags: 태그로 필터링
            limit: 최대 반환 개수
            offset: 오프셋
            sort_by: 정렬 기준 필드
            sort_order: 정렬 순서 (asc, desc)

        Returns:
            연락처 목록

        Raises:
            CloudContactAPIError: API 오류 발생 시
        """
        params = {
            'limit': min(limit, 1000),
            'offset': offset
        }

        if query:
            params['query'] = query
        if email:
            params['email'] = email
        if phone:
            params['phone'] = phone
        if company:
            params['company'] = company
        if tags:
            params['tags'] = ','.join(tags)
        if sort_by:
            params['sort_by'] = sort_by
        if sort_order:
            if sort_order not in ['asc', 'desc']:
                raise ValueError("sort_order must be 'asc' or 'desc'")
            params['sort_order'] = sort_order

        return self._make_request('GET', '/contacts', params=params)

    # ===== SMS CAMPAIGN ACTIONS =====

    def sent_sms_messages_by_campaign(
        self,
        campaign_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict:
        """
        캠페인별 발송된 SMS 메시지 조회

        Args:
            campaign_id: 캠페인 ID
            start_date: 시작 날짜 (YYYY-MM-DD)
            end_date: 종료 날짜 (YYYY-MM-DD)
            limit: 최대 반환 개수
            offset: 오프셋

        Returns:
            SMS 메시지 목록

        Raises:
            CloudContactAPIError: API 오류 발생 시
        """
        if not campaign_id:
            raise ValueError("campaign_id is required")

        params = {
            'campaign_id': campaign_id,
            'limit': min(limit, 1000),
            'offset': offset
        }

        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date

        return self._make_request('GET', '/sms/campaigns/messages', params=params)

    def get_sent_sms_messages(
        self,
        message_id: Optional[str] = None,
        recipient: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict:
        """
        발송된 SMS 메시지 조회

        Args:
            message_id: 메시지 ID
            recipient: 수신자 번호
            start_date: 시작 날짜 (YYYY-MM-DD)
            end_date: 종료 날짜 (YYYY-MM-DD)
            status: 상태 필터
            limit: 최대 반환 개수
            offset: 오프셋

        Returns:
            SMS 메시지 목록

        Raises:
            CloudContactAPIError: API 오류 발생 시
        """
        params = {
            'limit': min(limit, 1000),
            'offset': offset
        }

        if message_id:
            params['message_id'] = message_id
        if recipient:
            params['recipient'] = recipient
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        if status:
            params['status'] = status

        return self._make_request('GET', '/sms/messages', params=params)

    # ===== CLOSE =====

    def close(self):
        """
        클라이언트 리소스 정리
        """
        self.session = None
import requests
import time
from typing import Dict, List, Optional, Union
from datetime import datetime
import hmac
import hashlib


class PinterestAPIError(Exception):
    """Pinterest API 에러"""
    pass


class PinterestRateLimitError(PinterestAPIError):
    """Rate limit 초과 에러"""
    pass


class PinterestClient:
    """
    Pinterest API v5 Client

    OAuth 2.0 인증을 사용합니다.
    """

    def __init__(
        self,
        access_token: str,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
        base_url: str = "https://api.pinterest.com/v5",
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """
        Pinterest API 클라이언트 초기화

        Args:
            access_token: OAuth 2.0 access token
            app_id: Pinterest 앱 ID (필요시)
            app_secret: Pinterest 앩 시크릿 (필요시)
            base_url: API 베이스 URL
            timeout: 요청 타임아웃 (초)
            max_retries: 최대 재시도 횟수
            retry_delay: 재시도 간 지연 (초)
        """
        self.access_token = access_token
        self.app_id = app_id
        self.app_secret = app_secret
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
            method: HTTP 메서드 (GET, POST, PATCH, DELETE)
            endpoint: API 엔드포인트
            params: 쿼리 파라미터
            data: 폼 데이터
            json_data: JSON body
            headers: 추가 헤더

        Returns:
            API 응답 (字典)

        Raises:
            PinterestAPIError: API 오류 발생 시
            PinterestRateLimitError: Rate limit 초과 시
        """
        # Rate limiting
        current_time = time.time()
        time_since_last_request = current_time - self._last_request_time
        if time_since_last_request < self._min_request_interval:
            time.sleep(self._min_request_interval - time_since_last_request)

        url = f"{self.base_url}{endpoint}"
        request_headers = {
            'Authorization': f'Bearer {self.access_token}',
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
                        raise PinterestRateLimitError(
                            f"Rate limit exceeded. Retry after {retry_after} seconds"
                        )

                # 오류 응답 처리
                if not response.ok:
                    error_data = response.text
                    try:
                        error_data = response.json()
                    except ValueError:
                        pass
                    raise PinterestAPIError(
                        f"API error {response.status_code}: {error_data}"
                    )

                return response.json()

            except requests.exceptions.RequestException as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                else:
                    raise PinterestAPIError(f"Request failed: {str(e)}")

        raise PinterestAPIError(f"Max retries exceeded: {str(last_error)}")

    # ===== PIN ACTIONS =====

    def get_pin(self, pin_id: str) -> Dict:
        """
        특정 Pin 정보 조회

        Args:
            pin_id: Pin ID

        Returns:
            Pin 정보 (URL, description, media 등 포함)

        Raises:
            PinterestAPIError: API 오류 발생 시
        """
        if not pin_id:
            raise ValueError("pin_id is required")

        return self._make_request('GET', f'/pins/{pin_id}')

    def create_pin(
        self,
        board_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        link: Optional[str] = None,
        media_source: Optional[Dict] = None,
       alt_text: Optional[str] = None
    ) -> Dict:
        """
        새로운 Pin 생성

        Args:
            board_id: 보드 ID
            title: Pin 제목
            description: Pin 설명
            link: 연결 링크
            media_source: 미디어 소스 (예: {"source_type": "image_url", "url": "https://..."})
            alt_text: 이미지 대체 텍스트

        Returns:
            생성된 Pin 정보

        Raises:
            PinterestAPIError: API 오류 발생 시
        """
        if not board_id:
            raise ValueError("board_id is required")

        data = {
            'board_id': board_id
        }

        if title:
            data['title'] = title
        if description:
            data['description'] = description
        if link:
            data['link'] = link
        if media_source:
            data['media_source'] = media_source
        if alt_text:
            data['alt_text'] = alt_text

        return self._make_request('POST', '/pins', json_data=data)

    def list_pins(
        self,
        board_id: Optional[str] = None,
        pin_ids: Optional[List[str]] = None,
        page_size: int = 25,
        bookmark: Optional[str] = None
    ) -> Dict:
        """
        Pin 목록 조회

        Args:
            board_id: 보드 ID (특정 보드의 Pin만 조회)
            pin_ids: Pin ID 목록
            page_size: 페이지 크기 (최대 100)
            bookmark: 다음 페이지를 위한 bookmark

        Returns:
            Pin 목록

        Raises:
            PinterestAPIError: API 오류 발생 시
        """
        params = {}

        if board_id:
            params['board_id'] = board_id
        if pin_ids:
            params['pin_ids'] = ','.join(pin_ids)
        if page_size:
            params['page_size'] = min(page_size, 100)
        if bookmark:
            params['bookmark'] = bookmark

        # 특정 보드의 Pins를 조회하는 경우
        if board_id:
            return self._make_request('GET', f'/boards/{board_id}/pins', params=params)

        # Pin IDs로 조회하는 경우
        if pin_ids:
            return self._make_request('GET', '/pins', params=params)

        raise ValueError("Either board_id or pin_ids is required")

    # ===== BOARD ACTIONS =====

    def get_board(self, board_id: str) -> Dict:
        """
        특정 보드 정보 조회

        Args:
            board_id: 보드 ID

        Returns:
            보드 정보

        Raises:
            PinterestAPIError: API 오류 발생 시
        """
        if not board_id:
            raise ValueError("board_id is required")

        return self._make_request('GET', f'/boards/{board_id}')

    def create_board(
        self,
        name: str,
        description: Optional[str] = None,
        privacy: str = 'PUBLIC'
    ) -> Dict:
        """
        새로운 보드 생성

        Args:
            name: 보드 이름
            description: 보드 설명
            privacy: privcy 설정 (PUBLIC 또는 SECRET)

        Returns:
            생성된 보드 정보

        Raises:
            PinterestAPIError: API 오류 발생 시
        """
        if not name:
            raise ValueError("name is required")

        if privacy not in ['PUBLIC', 'SECRET']:
            raise ValueError("privacy must be either 'PUBLIC' or 'SECRET'")

        data = {
            'name': name,
            'privacy': privacy
        }

        if description:
            data['description'] = description

        return self._make_request('POST', '/boards', json_data=data)

    def update_board(
        self,
        board_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        privacy: Optional[str] = None
    ) -> Dict:
        """
        보드 정보 업데이트

        Args:
            board_id: 보드 ID
            name: 새 보드 이름
            description: 새 보드 설명
            privacy: 새 privacy 설정

        Returns:
            업데이트된 보드 정보

        Raises:
            PinterestAPIError: API 오류 발생 시
        """
        if not board_id:
            raise ValueError("board_id is required")

        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        if privacy:
            if privacy not in ['PUBLIC', 'SECRET']:
                raise ValueError("privacy must be either 'PUBLIC' or 'SECRET'")
            data['privacy'] = privacy

        if not data:
            raise ValueError("At least one field to update is required")

        return self._make_request('PATCH', f'/boards/{board_id}', json_data=data)

    def list_boards(
        self,
        page_size: int = 25,
        bookmark: Optional[str] = None,
        privacy: Optional[str] = None
    ) -> Dict:
        """
        보드 목록 조회

        Args:
            page_size: 페이지 크기 (최대 100)
            bookmark: 다음 페이지를 위한 bookmark
            privacy: privacy 필터 (all, public, secret)

        Returns:
            보드 목록

        Raises:
            PinterestAPIError: API 오류 발생 시
        """
        params = {}

        if page_size:
            params['page_size'] = min(page_size, 100)
        if bookmark:
            params['bookmark'] = bookmark
        if privacy:
            if privacy not in ['all', 'public', 'secret']:
                raise ValueError("privacy must be one of: all, public, secret")
            params['privacy'] = privacy

        return self._make_request('GET', '/boards', params=params)

    # ===== WEBHOOK HANDLING =====

    def verify_webhook_signature(
        self,
        payload: Union[str, bytes],
        signature: str,
        webhook_secret: str
    ) -> bool:
        """
        Webhook 서명 검증

        Args:
            payload: Webhook payload
            signature: X-Pinterest-Signature 헤더 값
            webhook_secret: Webhook secret

        Returns:
            서명 유효성 여부
        """
        if isinstance(payload, str):
            payload_bytes = payload.encode('utf-8')
        else:
            payload_bytes = payload

        expected_signature = hmac.new(
            webhook_secret.encode('utf-8'),
            payload_bytes,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature.lstrip('sha256='))

    def handle_webhook_event(
        self,
        payload: Dict,
        signature: Optional[str] = None,
        webhook_secret: Optional[str] = None
    ) -> Dict:
        """
        Webhook 이벤트 처리

        Args:
            payload: Webhook payload (JSON)
            signature: X-Pinterest-Signature 헤더 값
            webhook_secret: Webhook secret

        Returns:
            처리된 이벤트 정보

        Raises:
            PinterestAPIError: Webhook 처리 실패 시
        """
        # 서명 검증
        if signature and webhook_secret:
            payload_json = str(payload).encode('utf-8')
            if not self.verify_webhook_signature(payload_json, signature, webhook_secret):
                raise PinterestAPIError("Invalid webhook signature")

        # 이벤트 데이터 추출
        event_data = {
            'event_id': payload.get('event_id'),
            'event_type': payload.get('event_data', {}).get('code'),
            'event_time': payload.get('event_time'),
            'data': payload.get('event_data', {})
        }

        return event_data

    # ===== CLOSE =====

    def close(self):
        """
        클라이언트 리소스 정리
        """
        self.session = None
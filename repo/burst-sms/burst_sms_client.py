import requests
import time
from typing import Dict, List, Optional
from datetime import datetime
import hmac
import hashlib


class BurstSMSAPIError(Exception):
    """Burst SMS API 에러"""
    pass


class BurstSMSRateLimitError(BurstSMSAPIError):
    """Rate limit 초과 에러"""
    pass


class BurstSMSClient:
    """
    Burst SMS API Client

    API key authentication을 사용합니다.
    """

    def __init__(
        self,
        api_key: str,
        api_secret: Optional[str] = None,
        base_url: str = "https://api.transmitsms.com",
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """
        Burst SMS 클라이언트 초기화

        Args:
            api_key: API key
            api_secret: API secret (필요시)
            base_url: API 베이스 URL
            timeout: 요청 타임아웃 (초)
            max_retries: 최대 재시도 횟수
            retry_delay: 재시도 간 지연 (초)
        """
        self.api_key = api_key
        self.api_secret = api_secret
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
            method: HTTP 메서드 (GET, POST, DELETE)
            endpoint: API 엔드포인트
            params: 쿼리 파라미터
            data: 폼 데이터
            json_data: JSON body
            headers: 추가 헤더

        Returns:
            API 응답 (字典)

        Raises:
            BurstSMSAPIError: API 오류 발생 시
            BurstSMSRateLimitError: Rate limit 초과 시
        """
        # Rate limiting
        current_time = time.time()
        time_since_last_request = current_time - self._last_request_time
        if time_since_last_request < self._min_request_interval:
            time.sleep(self._min_request_interval - time_since_last_request)

        url = f"{self.base_url}{endpoint}"

        # API 인증 - 기본 인증 헤더
        auth = requests.auth.HTTPBasicAuth(self.api_key, self.api_secret or '')

        request_headers = {
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
                    auth=auth,
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
                        raise BurstSMSRateLimitError(
                            f"Rate limit exceeded. Retry after {retry_after} seconds"
                        )

                # 오류 응답 처리
                if not response.ok:
                    error_data = response.text
                    try:
                        error_data = response.json()
                    except ValueError:
                        pass
                    raise BurstSMSAPIError(
                        f"API error {response.status_code}: {error_data}"
                    )

                return response.json()

            except requests.exceptions.RequestException as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                else:
                    raise BurstSMSAPIError(f"Request failed: {str(e)}")

        raise BurstSMSAPIError(f"Max retries exceeded: {str(last_error)}")

    # ===== SMS ACTIONS =====

    def send_sms(
        self,
        message: str,
        to: str,
        from_: Optional[str] = None,
        send_at: Optional[str] = None,
        validity: Optional[int] = None,
        reply_type: Optional[str] = None,
        max_split: Optional[int] = None,
        scheduled: Optional[str] = None
    ) -> Dict:
        """
        SMS 발송

        Args:
            message: 메시지 내용
            to: 수신 번호 (국가 코드 포함: +821012345678)
            from_: 발신 번호 (선택사항)
            send_at: 예약 발송 시간 (YYYY-MM-DD HH:MM:SS)
            validity: 유효 시간 (분)
            reply_type: 답장 유형
            max_split: 최대 분할 개수
            scheduled: 예약 발송 여부

        Returns:
            발송된 메시지 정보

        Raises:
            BurstSMSAPIError: API 오류 발생 시
        """
        if not message:
            raise ValueError("message is required")
        if not to:
            raise ValueError("to (recipient number) is required")

        data = {
            'message': message,
            'to': to
        }

        if from_:
            data['from'] = from_
        if send_at:
            data['send_at'] = send_at
        if validity:
            data['validity'] = validity
        if reply_type:
            data['reply_type'] = reply_type
        if max_split:
            data['max_split'] = max_split
        if scheduled:
            data['scheduled'] = scheduled

        return self._make_request('POST', '/send-sms.json', data=data)

    def list_related_messages(
        self,
        message_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> Dict:
        """
        관련 메시지 목록 조회

        Args:
            message_id: 메시지 ID
            limit: 최대 반환 개수
            offset: 오프셋

        Returns:
            관련 메시지 목록

        Raises:
            BurstSMSAPIError: API 오류 발생 시
        """
        if not message_id:
            raise ValueError("message_id is required")

        params = {
            'message_id': message_id,
            'limit': min(limit, 1000),
            'offset': offset
        }

        return self._make_request('GET', '/get-sms-messages.json', params=params)

    def retrieve_messages(
        self,
        message_id: Optional[str] = None,
        message_ids: Optional[List[str]] = None,
        to: Optional[str] = None,
        from_: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        status: Optional[str] = None
    ) -> Dict:
        """
        메시지 조회

        Args:
            message_id: 단일 메시지 ID
            message_ids: 메시지 ID 목록
            to: 수신 번호와 매칭
            from_: 발신 번호와 매칭
            start_date: 시작 날짜 (YYYY-MM-DD)
            end_date: 종료 날짜 (YYYY-MM-DD)
            limit: 최대 반환 개수
            offset: 오프셋
            status: 상태 필터

        Returns:
            메시지 목록

        Raises:
            BurstSMSAPIError: API 오류 발생 시
        """
        params = {
            'limit': min(limit, 1000),
            'offset': offset
        }

        if message_id:
            params['message_id'] = message_id
        if message_ids:
            params['message_ids'] = ','.join(message_ids)
        if to:
            params['to'] = to
        if from_:
            params['from'] = from_
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        if status:
            params['status'] = status

        return self._make_request('GET', '/get-sms-messages.json', params=params)

    # ===== WEBHOOK HANDLING =====

    def verify_webhook_signature(
        self,
        payload: str,
        signature: str,
        webhook_secret: str
    ) -> bool:
        """
        Webhook 시그니처 검증

        Args:
            payload: Webhook payload (json string)
            signature: X-Signature 헤더 값
            webhook_secret: Webhook secret

        Returns:
            시그니처 유효성 여부
        """
        payload_bytes = payload.encode('utf-8')

        expected_signature = hmac.new(
            webhook_secret.encode('utf-8'),
            payload_bytes,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature.lstrip('sha256='))

    def handle_new_message_webhook(
        self,
        payload: Dict,
        signature: Optional[str] = None,
        webhook_secret: Optional[str] = None
    ) -> Dict:
        """
        New Message Webhook 이벤트 처리

        Args:
            payload: Webhook payload
            signature: X-Signature 헤더 값
            webhook_secret: Webhook secret

        Returns:
            처리된 이벤트信息
        """
        if signature and webhook_secret:
            payload_str = str(payload)
            if not self.verify_webhook_signature(payload_str, signature, webhook_secret):
                raise BurstSMSAPIError("Invalid webhook signature")

        event_data = {
            'event_type': 'new_message',
            'timestamp': payload.get('timestamp'),
            'message_id': payload.get('message_id'),
            'from': payload.get('from'),
            'to': payload.get('to'),
            'message': payload.get('message'),
            'status': payload.get('status'),
            'raw_payload': payload
        }

        return event_data

    def handle_received_message_webhook(
        self,
        payload: Dict,
        signature: Optional[str] = None,
        webhook_secret: Optional[str] = None
    ) -> Dict:
        """
        Received Message Webhook 이벤트 처리

        Args:
            payload: Webhook payload
            signature: X-Signature 헤더 값
            webhook_secret: Webhook secret

        Returns:
            처리된 이벤트信息
        """
        if signature and webhook_secret:
            payload_str = str(payload)
            if not self.verify_webhook_signature(payload_str, signature, webhook_secret):
                raise BurstSMSAPIError("Invalid webhook signature")

        event_data = {
            'event_type': 'received_message',
            'timestamp': payload.get('timestamp'),
            'message_id': payload.get('message_id'),
            'from': payload.get('from'),
            'to': payload.get('to'),
            'message': payload.get('message'),
            'raw_payload': payload
        }

        return event_data

    # ===== CLOSE =====

    def close(self):
        """
        클라이언트 리소스 정리
        """
        self.session = None
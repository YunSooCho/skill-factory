"""
Delighted API Client
Customer feedback and NPS surveys
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
from flask import Flask, request, jsonify
import time
import threading


class DelightedError(Exception):
    """Delighted API 에러"""
    pass


class RateLimitError(DelightedError):
    """Rate limit exceeded"""
    pass


class DelightedClient:
    """
    Delighted API Client
    Customer satisfaction surveys and feedback collection
    """

    def __init__(self, api_key: str, base_url: str = "https://api.delighted.com/v1"):
        """
        Delighted API 클라이언트 초기화

        Args:
            api_key: Delighted API key
            base_url: API 기본 URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = (api_key, '')
        self.session.headers.update({
            'Accept': 'application/json'
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
            DelightedError: API 에러 발생 시
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
                retry_after = int(response.headers.get('Retry-After', 1))
                raise RateLimitError(f"Rate limit exceeded. Retry after {retry_after} seconds")

            response.raise_for_status()

            if response.text:
                return response.json()
            return {}

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise DelightedError("Invalid API key")
            elif e.response.status_code == 403:
                raise DelightedError("API feature not available on current plan")
            elif e.response.status_code == 422:
                error_data = e.response.json()
                raise DelightedError(f"Validation error: {error_data}")
            raise DelightedError(f"API request failed: {str(e)}")

        except requests.exceptions.RequestException as e:
            raise DelightedError(f"API request failed: {str(e)}")

    def get_metrics(
        self,
        since: Optional[str] = None,
        until: Optional[str] = None,
        trend: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        NPS 메트릭 조회

        Args:
            since: 시작일 (YYYY-MM-DD)
            until: 종료일 (YYYY-MM-DD)
            trend: 트렌드 기간 (30d, 90d, etc.)

        Returns:
            메트릭 데이터
            {
                "nps": float,
                "promoters": int,
                "passives": int,
                "detractors": int,
                "promoters_percentage": float,
                "passives_percentage": float,
                "detractors_percentage": float,
                "average_score": float,
                "total_responses": int
            }
        """
        params = {}
        if since:
            params['since'] = since
        if until:
            params['until'] = until
        if trend:
            params['trend'] = trend

        return self._make_request('GET', '/metrics', params=params)

    def create_person(self, person: Dict[str, Any]) -> Dict[str, Any]:
        """
        사람 생성

        Args:
            person: 사람 정보
                {
                    "email": str,
                    "name": str,
                    "properties": dict,
                    "locale": str,  # en, es, fr, de, pt, it, nl, cs, da, pt-BR
                    "send": bool   # 설문조사 바로 전송 여부
                }

        Returns:
            생성된 사람 정보
        """
        return self._make_request('POST', '/people', data=person)

    def update_person(
        self,
        person_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        사람 정보 업데이트

        Args:
            person_id: 사람 ID
            updates: 업데이트할 정보
                {
                    "email": str,
                    "name": str,
                    "properties": dict,
                    "properties_to_delete": list
                }

        Returns:
            업데이트된 사람 정보
        """
        return self._make_request('PUT', f'/people/{person_id}', data=updates)

    def create_or_update_person(self, person: Dict[str, Any]) -> Dict[str, Any]:
        """
        사람 생성 또는 업데이트 (email을 기반)

        Args:
            person: 사람 정보

        Returns:
            사람 정보
        """
        return self._make_request('PUT', '/people', data=person)

    def search_people(
        self,
        email: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        사람 검색

        Args:
            email: 이메일 주소로 검색
            limit: 반환할 최대 결과 수
            page: 페이지 번호

        Returns:
            사람 목록
        """
        params = {}
        if email:
            params['email'] = email
        if limit:
            params['per_page'] = limit
        if page:
            params['page'] = page

        return self._make_request('GET', '/people', params=params)

    def unsubscribe_people(
        self,
        email: Optional[str] = None,
        person_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        사람 구독 취소 (설문조스에서 제외)

        Args:
            email: 이메일 주소
            person_id: 사람 ID (둘 중 하나 제공 필요)

        Returns:
            결과
        """
        data = {}
        if email:
            data['email'] = email
        if person_id:
            data['person_id'] = person_id

        if not data:
            raise DelightedError("Either email or person_id must be provided")

        return self._make_request('POST', '/unsubscribes', data=data)

    def search_survey_responses(
        self,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        trend: Optional[str] = None,
        min_score: Optional[int] = None,
        max_score: Optional[int] = None,
        person_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        설문조사 응답 검색

        Args:
            per_page: 페이지당 결과 수
            page: 페이지 번호
            since: 시작일 (YYYY-MM-DD)
            until: 종료일 (YYYY-MM-DD)
            trend: 트렌드 기간
            min_score: 최소 점수 (0-10)
            max_score: 최대 점수 (0-10)
            person_id: 특정 사람의 응답 검색

        Returns:
            응답 목록
        """
        params = {}
        if per_page:
            params['per_page'] = per_page
        if page:
            params['page'] = page
        if since:
            params['since'] = since
        if until:
            params['until'] = until
        if trend:
            params['trend'] = trend
        if min_score is not None:
            params['min_score'] = min_score
        if max_score is not None:
            params['max_score'] = max_score
        if person_id:
            params['person_id'] = person_id

        return self._make_request('GET', '/responses', params=params)

    def add_survey_response(
        self,
        person_email: str,
        score: int,
        comment: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        설문조사 응답 추가 (소스로부터)
        注意: これは主に他のソースからの回答を追加する場合に使用

        Args:
            person_email: 사람 이메일
            score: 점수 (0-10)
            comment: 코멘트
            properties: 추가 속성

        Returns:
            추가된 응답 정보
        """
        data = {
            'person_email': person_email,
            'score': score
        }

        if comment:
            data['comment'] = comment

        if properties:
            data.update(properties)

        return self._make_request('POST', '/responses', data=data)

    def delete_person(self, person_id: str) -> Dict[str, Any]:
        """
        사람 삭제

        Args:
            person_id: 사람 ID

        Returns:
            삭제 결과
        """
        return self._make_request('DELETE', f'/people/{person_id}')


class DelightedWebhookHandler:
    """
    Delighted Web 핸들러
    Flask 서버로 웹훅 수신 및 처리
    """

    def __init__(self, port: int = 5000, webhook_path: str = '/webhook'):
        """
        웹훅 핸들러 초기화

        Args:
            port: 서버 포트
            webhook_path: 웹훅 경로
        """
        self.app = Flask(__name__)
        self.port = port
        self.webhook_path = webhook_path
        self.response_handlers = {
            'response.created': [],
            'comment.created': [],
            'person.unsubscribed': []
        }
        self._setup_routes()

    def _setup_routes(self):
        """Flask 라우트 설정"""
        @self.app.route(self.webhook_path, methods=['POST'])
        def handle_webhook():
            event = request.get_json()

            if not event:
                return jsonify({'error': 'Invalid payload'}), 400

            event_type = event.get('event')
            event_data = event.get('data', {})

            # 이벤트 타입별 핸들러 실행
            handlers = self.response_handlers.get(event_type, [])
            if handlers:
                for handler in handlers:
                    try:
                        handler(event_data)
                    except Exception as e:
                        print(f"Error in webhook handler: {e}")

            return jsonify({'status': 'received'}), 200

        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({'status': 'healthy'}), 200

    def on_new_response(self, handler: callable):
        """
        새 응답 이벤트 핸들러 등록
        """
        self.response_handlers['response.created'].append(handler)

    def on_new_unsubscribe(self, handler: callable):
        """
        구독 취소 이벤트 핸들러 등록
        """
        self.response_handlers['person.unsubscribed'].append(handler)

    def on_new_comment(self, handler: callable):
        """
        새 코멘트 이벤트 핸들러 등록
        """
        self.response_handlers['comment.created'].append(handler)

    def run(self, host: str = '0.0.0.0', debug: bool = False):
        """
        웹훅 서버 시작

        Args:
            host: 호스트 주소
            debug: 디버그 모드
        """
        def run_server():
            self.app.run(host=host, port=self.port, debug=debug, threaded=True)

        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
        print(f"Delighted webhook server started on port {self.port}")
        return thread


def create_delighted_client(api_key: str) -> DelightedClient:
    """
    Delighted 클라이언트 생성 (Factory function)

    Args:
        api_key: Delighted API key

    Returns:
        DelightedClient 인스턴스
    """
    return DelightedClient(api_key)


if __name__ == "__main__":
    import os

    # 테스트 코드
    api_key = os.environ.get('DELIGHTED_API_KEY', 'your-api-key')
    client = create_delighted_client(api_key)

    try:
        # 메트릭 조회 테스트
        metrics = client.get_metrics()
        print("Metrics:", metrics)

        # 사람 생성 테스트
        result = client.create_person({
            'email': 'test@example.com',
            'name': 'Test User',
            'properties': {'plan': 'premium'},
            'send': False
        })
        print("Created person:", result)

        # 응답 검색 테스트
        responses = client.search_survey_responses(per_page=5)
        print("Survey responses:", responses)

        # 웹훅 서버 테스트
        def handle_new_response(data):
            print(f"New response received: {data}")

        def handle_new_unsubscribe(data):
            print(f"Person unsubscribed: {data}")

        webhook_handler = DelightedWebhookHandler(port=5001)
        webhook_handler.on_new_response(handle_new_response)
        webhook_handler.on_new_unsubscribe(handle_new_unsubscribe)
        webhook_handler.run()

        # 서버 유지
        while True:
            time.sleep(1)

    except Exception as e:
        print(f"Error: {str(e)}")
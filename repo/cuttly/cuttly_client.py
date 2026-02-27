"""
Cuttly API Client
API Documentation: https://cutt.ly/api
"""

import requests
import base64
from typing import Dict, List, Optional, Any
from datetime import datetime
import time


class CuttlyError(Exception):
    """Cuttly API 에러"""
    pass


class RateLimitError(CuttlyError):
    """Rate limit exceeded"""
    pass


class CuttlyClient:
    """
    Cuttly API Client
    URL Shortener and Analytics API
    """

    def __init__(self, api_key: str, base_url: str = "https://cutt.ly/api/api.php"):
        """
        Cuttly API 클라이언트 초기화

        Args:
            api_key: Cuttly API key
            base_url: API 기본 URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests (10 requests/second)

    def _handle_rate_limit(self) -> None:
        """Rate limiting 처리"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)
        self.last_request_time = time.time()

    def _make_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        API 요청 실행

        Args:
            params: 요청 파라미터

        Returns:
            API 응답

        Raises:
            CuttlyError: API 에러 발생 시
            RateLimitError: Rate limit 초과 시
        """
        self._handle_rate_limit()

        params['key'] = self.api_key

        try:
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            # 에러 처리
            if data.get('url', {}).get('status') == '4':
                raise RateLimitError(f"Rate limit exceeded: {data.get('url', {}).get('title')}")
            elif data.get('url', {}).get('status') == '2':
                raise CuttlyError(f"Invalid URL: {data.get('url', {}).get('title')}")
            elif data.get('url', {}).get('status') == '3':
                raise CuttlyError(f"Invalid API key: {data.get('url', {}).get('title')}")
            elif data.get('url', {}).get('status') == '5':
                raise CuttlyError(f"Short URL already exists: {data.get('url', {}).get('title')}")

            return data

        except requests.exceptions.RequestException as e:
            raise CuttlyError(f"API request failed: {str(e)}")

    def shorten_url(
        self,
        url: str,
        name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        public: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        URL 단축

        Args:
            url: 단축할 원본 URL
            name: 사용자 정의 단축 URL 이름 (선택)
            tags: 태그 목록 (선택)
            public: 공개 여부 (선택)

        Returns:
            단축 URL 정보
            {
                "url": {
                    "status": int,
                    "shortLink": str,
                    "title": str,
                    ...
                }
            }
        """
        params = {'short': url}

        if name:
            params['name'] = name

        if tags:
            params['tags'] = ','.join(tags)

        if public is not None:
            params['public'] = '1' if public else '0'

        return self._make_request(params)

    def get_analytics(
        self,
        url: str,
        limit: Optional[int] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        단축 URL 분석 데이터 조회

        Args:
            url: 분석할 단축 URL
            limit: 반환할 최대 결과 수 (선택)
            date_from: 시작 날짜 (YYYY-MM-DD, 선택)
            date_to: 종료 날짜 (YYYY-MM-DD, 선택)

        Returns:
            분석 데이터
            {
                "url": {
                    "status": int,
                    "fullLink": str,
                    "title": str,
                    "clicks": int,
                    "date": str,
                    ...
                }
            }
        """
        params = {'stats': url}

        if limit:
            params['limit'] = str(limit)

        if date_from:
            params['dateFrom'] = date_from

        if date_to:
            params['dateTo'] = date_to

        return self._make_request(params)


class CuttlyClientV2:
    """
    Cuttly API V2 Client (Advanced features)
    This provides more advanced analytics and management features.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.cutt.ly"):
        """
        Cuttly V2 API 클라이언트 초기화

        Args:
            api_key: Cuttly API key
            base_url: API 기본 URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        self.last_request_time = 0
        self.min_request_interval = 0.1

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
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        API 요청 실행

        Args:
            method: HTTP 메서드 (GET, POST, PUT, DELETE)
            endpoint: API 엔드포인트
            data: 요청 본문 데이터
            params: 쿼리 파라미터

        Returns:
            API 응답
        """
        self._handle_rate_limit()

        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            if e.response and e.response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")
            raise CuttlyError(f"API request failed: {str(e)}")


# Factory function for easy instantiation
def create_cuttly_client(api_key: str, use_v2: bool = False) -> Any:
    """
    Cuttly 클라이언트 생성

    Args:
        api_key: Cuttly API key
        use_v2: V2 API 사용 여부

    Returns:
        CuttlyClient 또는 CuttlyClientV2 인스턴스
    """
    if use_v2:
        return CuttlyClientV2(api_key)
    return CuttlyClient(api_key)


if __name__ == "__main__":
    # 테스트 코드
    import os

    api_key = os.environ.get('CUTTLY_API_KEY', 'your-api-key')
    client = create_cuttly_client(api_key)

    try:
        # URL 단축 테스트
        result = client.shorten_url('https://example.com', name='test-link')
        print("Shortened URL:", result)

        # 분석 데이터 조회 테스트
        short_link = result.get('url', {}).get('shortLink')
        if short_link:
            analytics = client.get_analytics(short_link)
            print("Analytics:", analytics)

    except Exception as e:
        print(f"Error: {str(e)}")
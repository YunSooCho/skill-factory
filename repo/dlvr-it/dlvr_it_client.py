"""
Dlvr.it API Client
Social media scheduling and automation
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import time


class DlvrItError(Exception):
    """Dlvr.it API 에러"""
    pass


class RateLimitError(DlvrItError):
    """Rate limit exceeded"""
    pass


class DlvrItClient:
    """
    Dlvr.it API Client
    Social media content scheduling and publishing
    """

    def __init__(self, api_key: str, base_url: str = "https://api.dlvrit.com/v1"):
        """
        Dlvr.it API 클라이언트 초기화

        Args:
            api_key: Dlvr.it API key
            base_url: API 기본 URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'X-DLVRI-PublicKey': api_key
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
            DlvrItError: API 에러 발생 시
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
                    raise DlvrItError("Invalid API key")
                elif e.response.status_code == 403:
                    raise DlvrItError("Access forbidden")

            raise DlvrItError(f"API request failed: {str(e)}")

    def list_accounts(self) -> Dict[str, Any]:
        """
        연결된 소셜 미디어 계정 목록 조회

        Returns:
            계정 목록
            {
                "accounts": [
                    {
                        "id": str,
                        "name": str,
                        "provider": str,  # twitter, facebook, instagram, linkedin, etc.
                        "handle": str,
                        "avatar_url": str,
                        "category": str,
                        "is_active": bool
                    },
                    ...
                ]
            }
        """
        return self._make_request('GET', '/accounts')

    def get_account(self, account_id: str) -> Dict[str, Any]:
        """
        특정 계정 상세 정보 조회

        Args:
            account_id: 계정 ID

        Returns:
            계정 상세 정보
        """
        return self._make_request('GET', f'/accounts/{account_id}')

    def list_routes(self) -> Dict[str, Any]:
        """
        라우트 목록 조회
        라우트는 하나 이상의 소셜 미디어 계정을 포함하는 그룹

        Returns:
            라우트 목록
            {
                "routes": [
                    {
                        "id": str,
                        "name": str,
                        "accounts": [
                            {
                                "id": str,
                                "provider": str,
                                "handle": str
                            },
                            ...
                        ],
                        "is_default": bool,
                        "created_at": str
                    },
                    ...
                ]
            }
        """
        return self._make_request('GET', '/routes')

    def get_route(self, route_id: str) -> Dict[str, Any]:
        """
        특정 라우트 상세 정보 조회

        Args:
            route_id: 라우트 ID

        Returns:
            라우트 상세 정보
        """
        return self._make_request('GET', f'/routes/{route_id}')

    def create_post_to_account(
        self,
        account_id: str,
        content: str,
        scheduled_at: Optional[str] = None,
        media_urls: Optional[List[str]] = None,
        link_url: Optional[str] = None,
        link_title: Optional[str] = None,
        link_description: Optional[str] = None,
        link_image_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        특정 계정에 게시물 생성

        Args:
            account_id: 게시할 계정 ID
            content: 게시물 내용
            scheduled_at: 예약 시간 (ISO 8601 format, 비어있으면 즉시 게시)
            media_urls: 미디어 URL 목록 (이미지, 비디오)
            link_url: 공유할 링크 URL
            link_title: 링크 제목
            link_description: 링크 설명
            link_image_url: 링크 이미지 URL

        Returns:
            생성된 게시물 정보
            {
                "id": str,
                "status": str,  # scheduled, published, failed
                "account_id": str,
                "content": str,
                "scheduled_at": str,
                "created_at": str,
                "post_url": str  # 게시된 게시물 URL
            }
        """
        data = {
            'account_id': account_id,
            'content': content
        }

        if scheduled_at:
            data['scheduled_at'] = scheduled_at

        if media_urls:
            data['media_urls'] = media_urls

        if link_url:
            data['link_url'] = link_url

        if link_title:
            data['meta'] = {
                'link_title': link_title,
                'link_description': link_description,
                'link_image_url': link_image_url
            }

        return self._make_request('POST', '/posts', data=data)

    def create_post_to_route(
        self,
        route_id: str,
        content: str,
        scheduled_at: Optional[str] = None,
        media_urls: Optional[List[str]] = None,
        link_url: Optional[str] = None,
        link_title: Optional[str] = None,
        link_description: Optional[str] = None,
        link_image_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        라우트의 모든 계정에 게시물 생성

        Args:
            route_id: 라우트 ID
            content: 게시물 내용
            scheduled_at: 예약 시간 (ISO 8601 format)
            media_urls: 미디어 URL 목록
            link_url: 공유할 링크 URL
            link_title: 링크 제목
            link_description: 링크 설명
            link_image_url: 링크 이미지 URL

        Returns:
            생성된 게시물들 정보
            {
                "posts": [
                    {
                        "id": str,
                        "status": str,
                        "account_id": str,
                        "route_id": str,
                        "content": str,
                        "scheduled_at": str,
                        "created_at": str
                    },
                    ...
                ]
            }
        """
        data = {
            'route_id': route_id,
            'content': content
        }

        if scheduled_at:
            data['scheduled_at'] = scheduled_at

        if media_urls:
            data['media_urls'] = media_urls

        if link_url:
            data['link_url'] = link_url

        if link_title:
            data['meta'] = {
                'link_title': link_title,
                'link_description': link_description,
                'link_image_url': link_image_url
            }

        return self._make_request('POST', '/posts/batch', data=data)

    def get_post(self, post_id: str) -> Dict[str, Any]:
        """
        게시물 상세 정보 조회

        Args:
            post_id: 게시물 ID

        Returns:
            게시물 상세 정보
        """
        return self._make_request('GET', f'/posts/{post_id}')

    def delete_post(self, post_id: str) -> Dict[str, Any]:
        """
        게시물 삭제 (예약된 게시물만 가능)

        Args:
            post_id: 게시물 ID

        Returns:
            삭제 결과
        """
        return self._make_request('DELETE', f'/posts/{post_id}')

    def list_posts(
        self,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        게시물 목록 조회

        Args:
            status: 상태 필터 ('scheduled', 'published', 'failed')
            limit: 반환할 최대 결과 수
            offset: 페이지 오프셋

        Returns:
            게시물 목록
        """
        params = {}

        if status:
            params['status'] = status

        if limit:
            params['limit'] = limit

        if offset:
            params['offset'] = offset

        return self._make_request('GET', '/posts', params=params)

    def get_scheduled_posts(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        예약된 게시물 목록 조회

        Args:
            limit: 반환할 최대 결과 수

        Returns:
            예약된 게시물 목록
        """
        return self.list_posts(status='scheduled', limit=limit)


if __name__ == "__main__":
    import os

    # 테스트 코드
    api_key = os.environ.get('DLVRIT_API_KEY', 'your-api-key')
    client = DlvrItClient(api_key)

    try:
        # 계정 목록 조회 테스트
        accounts = client.list_accounts()
        print("Accounts:", accounts)

        # 라우트 목록 조회 테스트
        routes = client.list_routes()
        print("Routes:", routes)

        # 게시물 생성 테스트 (account)
        if accounts.get('accounts'):
            account_id = accounts['accounts'][0]['id']
            post_result = client.create_post_to_account(
                account_id=account_id,
                content='Test post from API!',
                scheduled_at='2026-02-28T10:00:00Z'
            )
            print("Created post:", post_result)

        # 게시물 생성 테스트 (route)
        if routes.get('routes'):
            route_id = routes['routes'][0]['id']
            batch_result = client.create_post_to_route(
                route_id=route_id,
                content='Batch post from API!',
                scheduled_at='2026-02-28T11:00:00Z'
            )
            print("Created batch post:", batch_result)

    except Exception as e:
        print(f"Error: {str(e)}")
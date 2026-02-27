"""
Dash API Client
Digital Asset Management (DAM) API
"""

import requests
import base64
import os
from typing import Dict, List, Optional, Any, Union, BinaryIO
from datetime import datetime
import time
import mimetypes


class DashError(Exception):
    """Dash API 에러"""
    pass


class RateLimitError(DashError):
    """Rate limit exceeded"""
    pass


class DashClient:
    """
    Dash API Client
    Digital Asset Management for creative teams
    """

    def __init__(self, api_key: str, base_url: str = "https://api.dashhq.com"):
        """
        Dash API 클라이언트 초기화

        Args:
            api_key: Dash API key or JWT token
            base_url: API 기본 URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.last_request_time = 0
        self.min_request_interval = 0.05  # 50ms between requests (20 requests/second)

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
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, BinaryIO]] = None
    ) -> Dict[str, Any]:
        """
        API 요청 실행

        Args:
            method: HTTP 메서드 (GET, POST, PUT, DELETE)
            endpoint: API 엔드포인트
            data: 요청 본문 데이터
            params: 쿼리 파라미터
            files: 파일 데이터

        Returns:
            API 응답

        Raises:
            DashError: API 에러 발생 시
            RateLimitError: Rate limit 초과 시
        """
        self._handle_rate_limit()

        url = f"{self.base_url}{endpoint}"

        headers = self.session.headers.copy()
        if files:
            headers.pop('Content-Type', None)  # multipart/form-data를 위해 제거

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                params=params,
                files=files,
                timeout=60
            )
            response.raise_for_status()

            result = response.json()

            # 에러 처리
            if result.get('error'):
                if response.status_code == 429:
                    raise RateLimitError(f"Rate limit exceeded: {result.get('error')}")
                raise DashError(f"API error: {result.get('error')}")

            return result

        except requests.exceptions.RequestException as e:
            if e.response and e.response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")
            raise DashError(f"API request failed: {str(e)}")

    def search_assets(
        self,
        query: Optional[str] = None,
        tags: Optional[List[str]] = None,
        asset_type: Optional[str] = None,
        folder_id: Optional[str] = None,
        created_after: Optional[str] = None,
        created_before: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        에셋 검색

        Args:
            query: 검색 쿼리 (파일 이름, 메타데이터 등)
            tags: 태그 필터
            asset_type: 에셋 타입 필터 (image, video, document, audio, etc.)
            folder_id: 폴더 ID 필터
            created_after: 생성일 시작 (ISO 8601 format)
            created_before: 생성일 종료 (ISO 8601 format)
            limit: 반환할 최대 결과 수
            offset: 페이지 오프셋

        Returns:
            에셋 목록
            {
                "assets": [
                    {
                        "id": str,
                        "name": str,
                        "type": str,
                        "url": str,
                        "thumbnail_url": str,
                        "created_at": str,
                        "updated_at": str,
                        "metadata": dict,
                        "tags": list
                    },
                    ...
                ],
                "total": int,
                "limit": int,
                "offset": int
            }
        """
        params = {}

        if query:
            params['q'] = query

        if tags:
            params['tags'] = ','.join(tags)

        if asset_type:
            params['type'] = asset_type

        if folder_id:
            params['folder_id'] = folder_id

        if created_after:
            params['created_after'] = created_after

        if created_before:
            params['created_before'] = created_before

        if limit:
            params['limit'] = limit

        if offset:
            params['offset'] = offset

        return self._make_request('GET', '/v1/assets', params=params)

    def get_asset(self, asset_id: str) -> Dict[str, Any]:
        """
        에셋 상세 정보 조회

        Args:
            asset_id: 에셋 ID

        Returns:
            에셋 상세 정보
            {
                "id": str,
                "name": str,
                "type": str,
                "size": int,
                "mimetype": str,
                "url": str,
                "thumbnail_url": str,
                "created_at": str,
                "updated_at": str,
                "metadata": dict,
                "tags": list,
                "versions": list
            }
        """
        return self._make_request('GET', f'/v1/assets/{asset_id}')

    def download_asset(
        self,
        asset_id: str,
        output_path: Optional[str] = None,
        version: Optional[str] = None
    ) -> Union[bytes, str]:
        """
        에셋 다운로드

        Args:
            asset_id: 에셋 ID
            output_path: 저장 경로 (None이면 바이너리 반환)
            version: 다운로드할 버전 (기본값: 최신)

        Returns:
            바이너리 데이터 또는 저장된 파일 경로
        """
        self._handle_rate_limit()

        params = {}
        if version:
            params['version'] = version

        url = f"{self.base_url}/v1/assets/{asset_id}/download"

        try:
            response = self.session.get(url, params=params, headers={
                'Authorization': f'Bearer {self.api_key}'
            }, timeout=120)
            response.raise_for_status()

            content = response.content

            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(content)
                return output_path
            else:
                return content

        except requests.exceptions.RequestException as e:
            raise DashError(f"Download failed: {str(e)}")

    def get_asset_file_url(
        self,
        asset_id: str,
        version: Optional[str] = None,
        expires_in: Optional[int] = 3600
    ) -> str:
        """
        에셋 파일 URL 조회 (signed URL)

        Args:
            asset_id: 에셋 ID
            version: 버전 (기본값: 최신)
            expires_in: URL 만료 시간 (초, 기본값: 1시간)

        Returns:
            Signed URL
        """
        params = {}
        if version:
            params['version'] = version
        if expires_in:
            params['expires_in'] = expires_in

        result = self._make_request('GET', f'/v1/assets/{asset_id}/url', params=params)
        return result.get('url')

    def delete_asset(self, asset_id: str) -> Dict[str, Any]:
        """
        에셋 삭제

        Args:
            asset_id: 에셋 ID

        Returns:
            삭제 결과
            {
                "success": bool,
                "message": str
            }
        """
        return self._make_request('DELETE', f'/v1/assets/{asset_id}')

    def upload_asset(
        self,
        file_path: str,
        name: Optional[str] = None,
        folder_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        에셋 업로드

        Args:
            file_path: 업로드할 파일 경로
            name: 에셋 이름 (기본값: 파일명)
            folder_id: 업로드할 폴더 ID
            tags: 태그 목록
            metadata: 메타데이터 사전

        Returns:
            업로드된 에셋 정보
        """
        if not os.path.exists(file_path):
            raise DashError(f"File not found: {file_path}")

        filename = name or os.path.basename(file_path)

        files = {'file': (filename, open(file_path, 'rb'))}

        data = {}
        if folder_id:
            data['folder_id'] = folder_id

        if tags:
            data['tags'] = ','.join(tags)

        if metadata:
            for key, value in metadata.items():
                data[f'metadata[{key}]'] = value

        try:
            result = self._make_request('POST', '/v1/assets', data=data, files=files)
            return result
        finally:
            files['file'][1].close()

    def update_asset(
        self,
        asset_id: str,
        name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        에셋 업데이트

        Args:
            asset_id: 에셋 ID
            name: 새 이름
            tags: 태그 목록 (전체 교체)
            metadata: 메타데이터 (병합)

        Returns:
            업데이트된 에셋 정보
        """
        data = {}

        if name:
            data['name'] = name

        if tags is not None:
            data['tags'] = tags

        if metadata:
            data['metadata'] = metadata

        return self._make_request('PUT', f'/v1/assets/{asset_id}', data=data)


if __name__ == "__main__":
    # 테스트 코드
    import os

    api_key = os.environ.get('DASH_API_KEY', 'your-api-key')
    client = DashClient(api_key)

    try:
        # 에셋 검색 테스트
        search_result = client.search_assets(query='logo', limit=5)
        print("Search results:", search_result)

        # 특정 에셋 조회 테스트
        if search_result.get('assets'):
            asset_id = search_result['assets'][0]['id']
            asset = client.get_asset(asset_id)
            print("Asset details:", asset)

            # URL 조회 테스트
            file_url = client.get_asset_file_url(asset_id)
            print("Asset URL:", file_url)

            # 다운로드 테스트
            downloaded_path = client.download_asset(asset_id, '/tmp/test_asset.png')
            print("Downloaded to:", downloaded_path)

    except Exception as e:
        print(f"Error: {str(e)}")
"""
Canny API Client
"""

import requests
from typing import Optional, Dict, Any, List


class CannyClient:
    """Canny API 클라이언트"""

    BASE_URL = "https://canny.io/api/v1"

    def __init__(self, api_key: str):
        """
        Canny 클라이언트 초기화

        Args:
            api_key: Canny API 키
        """
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def _request(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        HTTP 요청 전송

        Args:
            endpoint: API 엔드포인트
            data: 요청 데이터
            params: 쿼리 파라미터

        Returns:
            응답 데이터
        """
        url = f"{self.BASE_URL}/{endpoint}"

        # API 키를 모든 요청에 추가
        request_data = {
            "apiKey": self.api_key
        }

        if data:
            request_data.update(data)

        try:
            response = requests.post(
                url,
                headers=self.headers,
                data=request_data,
                params=params
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            try:
                error_data = response.json()
                error_msg = error_data.get('error', error_msg)
            except:
                pass
            raise Exception(f"API 요청 실패: {error_msg}")
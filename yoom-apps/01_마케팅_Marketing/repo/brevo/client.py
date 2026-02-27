"""
Brevo API Client
"""

import requests
from typing import Optional, Dict, Any, List


class BrevoClient:
    """Brevo API 클라이언트"""

    BASE_URL = "https://api.brevo.com/v3"

    def __init__(self, api_key: str):
        """
        Brevo 클라이언트 초기화

        Args:
            api_key: Brevo API 키
        """
        self.api_key = api_key
        self.headers = {
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json"
        }

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        HTTP 요청 전송

        Args:
            method: HTTP 메서드 (GET, POST, PUT, DELETE)
            endpoint: API 엔드포인트
            data: 요청 바디
            params: 쿼리 파라미터

        Returns:
            응답 데이터
        """
        url = f"{self.BASE_URL}{endpoint}"

        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, params=params)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method == "PUT":
                response = requests.put(url, headers=self.headers, json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"지원하지 않는 HTTP 메서드: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"API 요청 실패: {str(e)}")
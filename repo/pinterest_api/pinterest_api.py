#!/usr/bin/env python3
"""
Pinterest API - Yoom Apps 자동화
API 액션: Get Pin, Create Pin, Get Board, Create Board, List Pins, Update Board, List Boards
"""

import os
import requests
from typing import Optional, Dict, List, Any
from dataclasses import dataclass

@dataclass
class PinterestConfig:
    """Pinterest API 설정"""
    access_token: str
    base_url: str = "https://api.pinterest.com/v5/"
    api_version: str = "v5"
    timeout: int = 30

    @classmethod
    def from_env(cls):
        """환경 변수에서 설정 로드"""
        access_token = os.getenv("PINTEREST_ACCESS_TOKEN")
        if not access_token:
            raise ValueError("PINTEREST_ACCESS_TOKEN 환경 변수가 필요합니다")
        return cls(access_token=access_token)

class PinterestAPI:
    """Pinterest API 클라이언트"""

    def __init__(self, config: PinterestConfig):
        self.config = config
        self.base_url = config.base_url
        self.headers = {
            "Authorization": f"Bearer {config.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        API 요청

        Args:
            method: HTTP 메서드 (GET, POST, PATCH, DELETE)
            endpoint: API 엔드포인트 (예: "pins/{pin_id}")
            params: 쿼리 파라미터
            data: 요청 본문

        Returns:
            응답 JSON

        Raises:
            requests.RequestException: API 요청 실패 시
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=data,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            error_msg = f"API 요청 실패: {e}"
            if e.response is not None:
                error_msg += f" (Status: {e.response.status_code}, Body: {e.response.text})"
            raise requests.RequestException(error_msg) from e

    # ==================== PINS API ====================

    def get_pin(self, pin_id: str) -> Dict[str, Any]:
        """
        핀(Pin) 정보 조회

        Args:
            pin_id: 핀 ID

        Returns:
            핀 정보 (id, title, description, link, media 등)
        """
        return self._request("GET", f"pins/{pin_id}")

    def create_pin(self, title: str, link: str, board_id: str,
                   description: Optional[str] = None,
                   media_source: Optional[Dict] = None) -> Dict[str, Any]:
        """
        핀(Pin) 생성

        Args:
            title: 핀 제목
            link: 핀의 메인 링크
            board_id: 보드 ID
            description: 핀 설명 (선택 사항)
            media_source: 미디어 소스 정보 (선택 사항)

        Returns:
            생성된 핀 정보 (id, board, title, description 등)
        """
        request_data = {
            "board_id": board_id,
            "title": title,
            "link": link
        }

        if description:
            request_data["description"] = description

        if media_source:
            request_data["media_source"] = media_source

        return self._request("POST", "pins", data=request_data)

    def list_pins(self, board_id: Optional[str] = None,
                  page_size: int = 25,
                  bookmark: Optional[str] = None) -> Dict[str, Any]:
        """
        핀(Pin) 목록 조회

        Args:
            board_id: 보드 ID (선택 사항, 없으면 전체 핀 반환)
            page_size: 페이지 크기 (최대 100)
            bookmark: 페이징용 북마크

        Returns:
            핀 목록 (items, bookmark 등)
        """
        params = {"page_size": page_size}

        if board_id:
            params["board_id"] = board_id

        if bookmark:
            params["bookmark"] = bookmark

        return self._request("GET", "pins", params=params)

    # ==================== BOARDS API ====================

    def get_board(self, board_id: str) -> Dict[str, Any]:
        """
        보드(Board) 정보 조회

        Args:
            board_id: 보드 ID

        Returns:
            보드 정보 (id, name, description, pin_count 등)
        """
        return self._request("GET", f"boards/{board_id}")

    def create_board(self, name: str,
                    description: Optional[str] = None,
                    privacy: str = "PUBLIC") -> Dict[str, Any]:
        """
        보드(Board) 생성

        Args:
            name: 보드 이름 (최대 255자)
            description: 보드 설명 (선택 사항, 최대 600자)
            privacy: 보드 공개 설정 (PUBLIC 또는 SECRET)

        Returns:
            생성된 보드 정보 (id, name, description, privacy 등)
        """
        request_data = {
            "name": name,
            "privacy": privacy
        }

        if description:
            request_data["description"] = description

        return self._request("POST", "boards", data=request_data)

    def update_board(self, board_id: str,
                    name: Optional[str] = None,
                    description: Optional[str] = None,
                    privacy: Optional[str] = None) -> Dict[str, Any]:
        """
        보드(Board) 업데이트

        Args:
            board_id: 보드 ID
            name: 새로운 보드 이름 (선택 사항)
            description: 새로운 보드 설명 (선택 사항)
            privacy: 새로운 보드 공개 설정 (선택 사항)

        Returns:
            업데이트된 보드 정보
        """
        request_data = {}

        if name:
            request_data["name"] = name

        if description:
            request_data["description"] = description

        if privacy:
            request_data["privacy"] = privacy

        return self._request("PATCH", f"boards/{board_id}", data=request_data)

    def list_boards(self, page_size: int = 25,
                   bookmark: Optional[str] = None) -> Dict[str, Any]:
        """
        보드(Board) 목록 조회

        Args:
            page_size: 페이지 크기 (최대 100)
            bookmark: 페이징용 북마크

        Returns:
            보드 목록 (items, bookmark 등)
        """
        params = {"page_size": page_size}

        if bookmark:
            params["bookmark"] = bookmark

        return self._request("GET", "boards", params=params)

    # ==================== WEBHOOKS ====================

    def register_webhook(self, callback_url: str, fields: List[str]) -> Dict[str, Any]:
        """
        Webhook 등록 (트리거용)

        Args:
            callback_url: Webhook 수신 URL
            fields: 알림받을 필드 목록 (예: ["pins", "boards", ""])

        Returns:
            Webhook 등록 정보
        """
        request_data = {
            "destination": callback_url,
            "fields": [{"id": field} for field in fields]
        }

        return self._request("POST", "webhooks", data=request_data)

# ==================== 샘플 코드 및 테스트 ====================

if __name__ == "__main__":
    """테스트 케이드"""

    # 환경 변수에서 설정 로드
    try:
        config = PinterestConfig.from_env()
        client = PinterestAPI(config)

        print("=== Pinterest API 테스트 ===")

        # 보드 목록 조회
        print("\n[1] 보드 목록 조회")
        boards = client.list_boards(page_size=10)
        print(f"✅ 보드 조회 완료: {len(boards.get('items', []))}개의 보드")
        if boards.get('items'):
            for board in boards['items'][:3]:
                print(f"  - {board['name']} (ID: {board['id']})")

        # 새로운 보드 생성 (테스트용)
        print("\n[2] 새로운 보드 생성")
        new_board = client.create_board(
            name="테스트 보드 - Yoom Automation",
            description="Yoom Apps 자동화 테스트용 보드",
            privacy="SECRET"
        )
        board_id = new_board['id']
        print(f"✅ 보드 생성 완료: {new_board['name']} (ID: {board_id})")

        # 보드 상세 조회
        print("\n[3] 보드 상세 조회")
        board_detail = client.get_board(board_id)
        print(f"✅ 보드 조회 완료: {board_detail['name']}")
        print(f"  설명: {board_detail.get('description', '없음')}")
        print(f"  공개 여부: {board_detail['privacy']}")

        # 핀 목록 조회
        print("\n[4] 핀 목록 조회")
        pins = client.list_pins(board_id=board_id, page_size=5)
        print(f"✅ 핀 조회 완료: {len(pins.get('items', []))}개의 핀")

        # 보드 업데이트
        print("\n[5] 보드 업데이트")
        updated_board = client.update_board(
            board_id=board_id,
            description="Yoom Apps 자동화 테스트용 보드 (업데이트됨)"
        )
        print(f"✅ 보드 업데이트 완료: {updated_board['description']}")

        # 완료
        print("\n=== 모든 테스트 완료 ===")
        print(f"테스트 보드 ID: {board_id}")
        print(f"\n참고: 실제 사용 시 핀 생성을 위해서는 미디어 소스 준비가 필요합니다")
        print("미디어 업로드 API를 통해서 이미지를 먼저 업로드해야 합니다")

    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        print("\n참고: 테스트 실행 전에 PINTEREST_ACCESS_TOKEN 환경 변수를 설정하세요")
        print("예: export PINTEREST_ACCESS_TOKEN='your_access_token_here'")
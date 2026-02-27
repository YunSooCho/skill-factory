"""
Canny API Triggers
Yoom에서 실행 가능한 트리거 구현 (Webhook 기반)
"""

from typing import Optional, Dict, Any, List, Callable
from .client import CannyClient


class CannyTriggers(CannyClient):
    """Canny API 트리거 (Webhook 기반)"""

    # ========== Webhook 관리 ==========

    def create_webhook(
        self,
        url: str,
        events: List[str]
    ) -> Dict[str, Any]:
        """
        Webhook 생성

        Args:
            url: Webhook URL
            events: 수신할 이벤트 리스트

        Returns:
            생성된 웹훅 정보
        """
        data = {
            "url": url,
            "events": events
        }
        return self._request("webhooks/create", data)

    def list_webhooks(self) -> Dict[str, Any]:
        """
        Webhook 목록 가져오기

        Returns:
            웹훅 목록
        """
        return self._request("webhooks/list", {})

    def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """
        Webhook 삭제

        Args:
            webhook_id: 웹훅 ID

        Returns:
            삭제 결과
        """
        return self._request("webhooks/delete", {"webhookID": webhook_id})

    # ========== 트리거 유틸리티 ==========

    def setup_new_post_trigger(
        self,
        webhook_url: str
    ) -> Dict[str, Any]:
        """
        새 게시글 트리거 설정

        Args:
            webhook_url: Yoom Webhook URL

        Returns:
            생성된 웹훅 정보
        """
        return self.create_webhook(
            url=webhook_url,
            events=["post.created"]
        )

    def setup_deleted_post_trigger(
        self,
        webhook_url: str
    ) -> Dict[str, Any]:
        """
        게시글 삭제 트리거 설정

        Args:
            webhook_url: Yoom Webhook URL

        Returns:
            생성된 웹훅 정보
        """
        return self.create_webhook(
            url=webhook_url,
            events=["post.deleted"]
        )

    def setup_changed_post_status_trigger(
        self,
        webhook_url: str
    ) -> Dict[str, Any]:
        """
        게시글 상태 변경 트리거 설정

        Args:
            webhook_url: Yoom Webhook URL

        Returns:
            생성된 웹훅 정보
        """
        return self.create_webhook(
            url=webhook_url,
            events=["post.statusChanged"]
        )

    def setup_tag_added_to_post_trigger(
        self,
        webhook_url: str
    ) -> Dict[str, Any]:
        """
        게시글 태그 추가 트리거 설정

        Args:
            webhook_url: Yoom Webhook URL

        Returns:
            생성된 웹훅 정보
        """
        return self.create_webhook(
            url=webhook_url,
            events=["post.tagAdded"]
        )

    def setup_new_comment_trigger(
        self,
        webhook_url: str
    ) -> Dict[str, Any]:
        """
        새 댓글 트리거 설정

        Args:
            webhook_url: Yoom Webhook URL

        Returns:
            생성된 웹훅 정보
        """
        return self.create_webhook(
            url=webhook_url,
            events=["comment.created"]
        )

    def setup_deleted_comment_trigger(
        self,
        webhook_url: str
    ) -> Dict[str, Any]:
        """
        댓글 삭제 트리거 설정

        Args:
            webhook_url: Yoom Webhook URL

        Returns:
            생성된 웹훅 정보
        """
        return self.create_webhook(
            url=webhook_url,
            events=["comment.deleted"]
        )

    def setup_new_vote_trigger(
        self,
        webhook_url: str
    ) -> Dict[str, Any]:
        """
        새 투표 트리거 설정

        Args:
            webhook_url: Yoom Webhook URL

        Returns:
            생성된 웹훅 정보
        """
        return self.create_webhook(
            url=webhook_url,
            events=["vote.created"]
        )

    def setup_deleted_vote_trigger(
        self,
        webhook_url: str
    ) -> Dict[str, Any]:
        """
        투표 삭제 트리거 설정

        Args:
            webhook_url: Yoom Webhook URL

        Returns:
            생성된 웹훅 정보
        """
        return self.create_webhook(
            url=webhook_url,
            events=["vote.deleted"]
        )

    # ========== Webhook 페이로드 파싱 ==========

    @staticmethod
    def parse_webhook_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Webhook 페이로드 파싱

        Args:
            payload: Webhook 페이로드

        Returns:
            파싱된 데이터
        """
        return {
            "event_type": payload.get("type"),
            "timestamp": payload.get("created_at"),
            "post_id": payload.get("post") and payload.get("post", {}).get("id"),
            "post": payload.get("post"),
            "comment_id": payload.get("comment") and payload.get("comment", {}).get("id"),
            "comment": payload.get("comment"),
            "user_id": payload.get("user") and payload.get("user", {}).get("id"),
            "user": payload.get("user"),
            "previous_status": payload.get("previous_status"),
            "new_status": payload.get("new_status"),
            "tag": payload.get("tag"),
            "data": payload
        }

    # ========== 이벤트 핸들러 ==========

    def register_event_handler(
        self,
        event_type: str,
        handler: Callable[[Dict[str, Any]], None]
    ) -> None:
        """
        이벤트 핸들러 등록 (로컬 개발용)

        Args:
            event_type: 이벤트 유형
            handler: 핸들러 함수
        """
        if not hasattr(self, '_event_handlers'):
            self._event_handlers = {}

        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []

        self._event_handlers[event_type].append(handler)

    def trigger_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        """
        이벤트 트리거

        Args:
            event_type: 이벤트 유형
            payload: 이벤트 데이터
        """
        if hasattr(self, '_event_handlers') and event_type in self._event_handlers:
            for handler in self._event_handlers[event_type]:
                handler(payload)
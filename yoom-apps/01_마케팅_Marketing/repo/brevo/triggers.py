"""
Brevo API Triggers
Yoom에서 실행 가능한 트리거 구현 (Webhook 기반)
"""

from typing import Optional, Dict, Any, List, Callable
from .client import BrevoClient


class BrevoTriggers(BrevoClient):
    """Brevo API 트리거 (Webhook 기반)"""

    # ========== Webhook 관리 ==========

    def create_webhook(
        self,
        url: str,
        description: str,
        events: List[str],
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Webhook 생성

        Args:
            url: Webhook URL
            description: 웹훅 설명
            events: 이벤트 리스트
            headers: 추가 헤더

        Returns:
            생성된 웹훅 정보
        """
        data = {
            "url": url,
            "description": description,
            "events": events
        }

        if headers:
            data["headers"] = headers

        return self._request("POST", "/webhooks", data=data)

    def get_webhook(self, webhook_id: int) -> Dict[str, Any]:
        """
        Webhook 정보 가져오기

        Args:
            webhook_id: 웹훅 ID

        Returns:
            웹훅 정보
        """
        return self._request("GET", f"/webhooks/{webhook_id}")

    def list_webhooks(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Webhook 목록 가져오기

        Args:
            limit: 최대 개수
            offset: 오프셋

        Returns:
            웹훅 목록
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        return self._request("GET", "/webhooks", params=params)

    def update_webhook(
        self,
        webhook_id: int,
        url: Optional[str] = None,
        description: Optional[str] = None,
        events: Optional[List[str]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Webhook 업데이트

        Args:
            webhook_id: 웹훅 ID
            url: 새로운 URL
            description: 새로운 설명
            events: 새로운 이벤트 리스트
            headers: 새로운 헤더

        Returns:
            업데이트된 웹훅 정보
        """
        data = {}

        if url:
            data["url"] = url

        if description:
            data["description"] = description

        if events:
            data["events"] = events

        if headers:
            data["headers"] = headers

        return self._request("PUT", f"/webhooks/{webhook_id}", data=data)

    def delete_webhook(self, webhook_id: int) -> Dict[str, Any]:
        """
        Webhook 삭제

        Args:
            webhook_id: 웹훅 ID

        Returns:
            삭제 결과
        """
        return self._request("DELETE", f"/webhooks/{webhook_id}")

    # ========== 트리거 유틸리티 ==========

    def setup_contact_created_trigger(
        self,
        webhook_url: str,
        description: str = "연락처 생성 트리거"
    ) -> Dict[str, Any]:
        """
        연락처 생성 트리거 설정
        연락처가 새로 생성되면 Webhook 호출

        Args:
            webhook_url: Yoom Webhook URL
            description: 웹훅 설명

        Returns:
            생성된 웹훅 정보
        """
        return self.create_webhook(
            url=webhook_url,
            description=description,
            events=["contact_created"]
        )

    def setup_marketing_email_opened_trigger(
        self,
        webhook_url: str,
        description: str = "마케팅 이메일 개봉 트리거"
    ) -> Dict[str, Any]:
        """
        마케팅 이메일 개봉 트리거 설정
        마케팅 이메일이 열리면 Webhook 호출

        Args:
            webhook_url: Yoom Webhook URL
            description: 웹훅 설명

        Returns:
            생성된 웹훅 정보
        """
        return self.create_webhook(
            url=webhook_url,
            description=description,
            events=["marketing_email_opened"]
        )

    def setup_marketing_email_clicked_trigger(
        self,
        webhook_url: str,
        description: str = "마케팅 이메일 클릭 트리거"
    ) -> Dict[str, Any]:
        """
        마케팅 이메일 클릭 트리거 설정
        마케팅 이메일의 링크가 클릭되면 Webhook 호출

        Args:
            webhook_url: Yoom Webhook URL
            description: 웹훅 설명

        Returns:
            생성된 웹훅 정보
        """
        return self.create_webhook(
            url=webhook_url,
            description=description,
            events=["marketing_email_clicked"]
        )

    def setup_marketing_email_sent_trigger(
        self,
        webhook_url: str,
        description: str = "마케팅 이메일 송신 트리거"
    ) -> Dict[str, Any]:
        """
        마케팅 이메일 송신 트리거 설정
        마케팅 이메일이 송신되면 Webhook 호출

        Args:
            webhook_url: Yoom Webhook URL
            description: 웹훅 설명

        Returns:
            생성된 웹훅 정보
        """
        return self.create_webhook(
            url=webhook_url,
            description=description,
            events=["marketing_email_sent"]
        )

    def setup_marketing_email_unsubscribed_trigger(
        self,
        webhook_url: str,
        description: str = "마케팅 이메일 구독 해지 트리거"
    ) -> Dict[str, Any]:
        """
        마케팅 이메일 구독 해지 트리거 설정
        마케팅 이메일 배송이 중지되면 Webhook 호출

        Args:
            webhook_url: Yoom Webhook URL
            description: 웹훅 설명

        Returns:
            생성된 웹훅 정보
        """
        return self.create_webhook(
            url=webhook_url,
            description=description,
            events=["marketing_email_unsubscribed"]
        )

    def setup_transactional_email_sent_trigger(
        self,
        webhook_url: str,
        description: str = "거래 이메일 송신 트리거"
    ) -> Dict[str, Any]:
        """
        거래 이메일 송신 트리거 설정
        거래 이메일이 송신되면 Webhook 호출

        Args:
            webhook_url: Yoom Webhook URL
            description: 웹훅 설명

        Returns:
            생성된 웹훅 정보
        """
        return self.create_webhook(
            url=webhook_url,
            description=description,
            events=["transactional_email_sent"]
        )

    def setup_transactional_email_opened_trigger(
        self,
        webhook_url: str,
        description: str = "거래 이메일 개봉 트리거"
    ) -> Dict[str, Any]:
        """
        거래 이메일 개봉 트리거 설정
        거래 이메일이 열리면 Webhook 호출

        Args:
            webhook_url: Yoom Webhook URL
            description: 웹훅 설명

        Returns:
            생성된 웹훅 정보
        """
        return self.create_webhook(
            url=webhook_url,
            description=description,
            events=["transactional_email_opened"]
        )

    def setup_transactional_email_clicked_trigger(
        self,
        webhook_url: str,
        description: str = "거래 이메일 클릭 트리거"
    ) -> Dict[str, Any]:
        """
        거래 이메일 클릭 트리거 설정
        거래 이메일의 링크가 클릭되면 Webhook 호출

        Args:
            webhook_url: Yoom Webhook URL
            description: 웹훅 설명

        Returns:
            생성된 웹훅 정보
        """
        return self.create_webhook(
            url=webhook_url,
            description=description,
            events=["transactional_email_clicked"]
        )

    # ========== Webhook 이벤트 페이로드 파싱 ==========

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
            "event_type": payload.get("event"),
            "timestamp": payload.get("timestamp"),
            "email": payload.get("email"),
            "contact_id": payload.get("contact_id"),
            "campaign_id": payload.get("campaign_id"),
            "message_id": payload.get("message_id"),
            "data": payload.get("data", {})
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
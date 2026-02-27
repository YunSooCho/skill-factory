"""
Brevo API Actions
Yoom에서 실행 가능한 API 액션 구현
"""

from typing import Optional, Dict, Any, List
from .client import BrevoClient


class BrevoActions(BrevoClient):
    """Brevo API 액션"""

    # ========== 연락처 액션 ==========

    def create_contact(
        self,
        email: str,
        attributes: Optional[Dict[str, Any]] = None,
        list_ids: Optional[List[int]] = None,
        update_enabled: bool = False
    ) -> Dict[str, Any]:
        """
        연락처 생성

        Args:
            email: 연락처 이메일
            attributes: 연락처 속성 (이름, 성명, 전화번호 등)
            list_ids: 추가할 리스트 ID 목록
            update_enabled: 이메일이 이미 존재할 경우 업데이트 여부

        Returns:
            생성된 연락처 정보
        """
        data = {
            "email": email,
            "updateEnabled": update_enabled
        }

        if attributes:
            data["attributes"] = attributes

        if list_ids:
            data["listIds"] = list_ids

        return self._request("POST", "/contacts", data=data)

    def update_contact(
        self,
        email: str,
        attributes: Optional[Dict[str, Any]] = None,
        list_ids: Optional[List[int]] = None,
       unlink_list_ids: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        연락처 업데이트

        Args:
            email: 연락처 이메일
            attributes: 업데이트할 속성
            list_ids: 추가할 리스트 ID 목록
            unlink_list_ids: 제거할 리스트 ID 목록

        Returns:
            업데이트된 연락처 정보
        """
        data = {}

        if attributes:
            data["attributes"] = attributes

        if list_ids:
            data["listIds"] = list_ids

        if unlink_list_ids:
            data["unlinkListIds"] = unlink_list_ids

        return self._request("PUT", f"/contacts/{email}", data=data)

    def get_contact(self, email: str) -> Dict[str, Any]:
        """
        연락처 정보 가져오기

        Args:
            email: 연락처 이메일

        Returns:
            연락처 정보
        """
        return self._request("GET", f"/contacts/{email}")

    def add_contact_to_list(self, list_id: int, emails: List[str]) -> Dict[str, Any]:
        """
        기존 연락처를 리스트에 추가

        Args:
            list_id: 리스트 ID
            emails: 추가할 이메일 목록

        Returns:
            추가 결과
        """
        data = {
            "emails": emails
        }
        return self._request("POST", f"/contacts/lists/{list_id}/contacts/add", data=data)

    # ========== 이메일 액션 ==========

    def send_transactional_email(
        self,
        sender: Dict[str, str],
        to: List[Dict[str, str]],
        subject: str,
        html_content: Optional[str] = None,
        text_content: Optional[str] = None,
        cc: Optional[List[Dict[str, str]]] = None,
        bcc: Optional[List[Dict[str, str]]] = None,
        reply_to: Optional[Dict[str, str]] = None,
        attachment: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        거래 이메일 송신

        Args:
            sender: 발신자 정보 {"email": "...", "name": "..."}
            to: 수신자 정보 목록 [{"email": "...", "name": "..."}]
            subject: 이메일 제목
            html_content: HTML 본문
            text_content: 텍스트 본문
            cc: CC 수신자
            bcc: BCC 수신자
            reply_to: 회신 주소
            attachment: 첨부파일 [{"name": "...", "content": "..."}]

        Returns:
            송신 결과
        """
        data = {
            "sender": sender,
            "to": to,
            "subject": subject
        }

        if html_content:
            data["htmlContent"] = html_content

        if text_content:
            data["textContent"] = text_content

        if cc:
            data["cc"] = cc

        if bcc:
            data["bcc"] = bcc

        if reply_to:
            data["replyTo"] = reply_to

        if attachment:
            data["attachment"] = attachment

        return self._request("POST", "/smtp/email", data=data)

    def get_email_campaign_report(
        self,
        campaign_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        이메일 캠페인 리포트 가져오기

        Args:
            campaign_id: 캠페인 ID
            start_date: 시작 날짜 (YYYY-MM-DD)
            end_date: 종료 날짜 (YYYY-MM-DD)

        Returns:
            캠페인 리포트
        """
        params = {}

        if start_date:
            params["startDate"] = start_date

        if end_date:
            params["endDate"] = end_date

        return self._request("GET", f"/emailCampaigns/{campaign_id}", params=params)

    def send_campaign_report(self, campaign_id: int, recipients: List[str]) -> Dict[str, Any]:
        """
        캠페인 리포트 송신

        Args:
            campaign_id: 캠페인 ID
            recipients: 수신자 이메일 목록

        Returns:
            송신 결과
        """
        data = {
            "recipients": {
                "email": recipients
            }
        }
        return self._request("POST", f"/emailCampaigns/{campaign_id}/sendReport", data=data)

    # ========== SMS 액션 ==========

    def create_sms_campaign(
        self,
        name: str,
        sender: str,
        content: str,
        recipients: Dict[str, Any],
        scheduled_at: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        SMS 캠페인 생성

        Args:
            name: 캠페인 이름
            sender: 발신자 이름
            content: SMS 내용
            recipients: 수신자 정보 {"listIds": [1, 2], ...}
            scheduled_at: 예약 발송 시간

        Returns:
            생성된 캠페인 정보
        """
        data = {
            "name": name,
            "sender": sender,
            "content": content,
            "recipients": recipients
        }

        if scheduled_at:
            data["scheduledAt"] = scheduled_at

        return self._request("POST", "/smsCampaigns", data=data)

    def send_sms_campaign_now(self, campaign_id: int) -> Dict[str, Any]:
        """
        SMS 캠페인 즉시 송신

        Args:
            campaign_id: 캠페인 ID

        Returns:
            송신 결과
        """
        return self._request("POST", f"/smsCampaigns/{campaign_id}/sendNow")

    # ========== WhatsApp 액션 ==========

    def send_whatsapp_message(
        self,
        recipient: str,
        content: str,
        to_type: str = "phone"
    ) -> Dict[str, Any]:
        """
        WhatsApp 메시지 송신

        Args:
            recipient: 수신자 (전화번호 또는 email)
            content: 메시지 내용
            to_type: 수신자 유형 ("phone" 또는 "email")

        Returns:
            송신 결과
        """
        data = {
            "recipient": recipient,
            "content": content,
            "type": to_type
        }
        return self._request("POST", "/whatsapp/send", data=data)
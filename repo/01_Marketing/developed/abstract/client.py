"""
Abstract API Client

Yoom Apps 자동화를 위한 Abstract API 통합 클라이언트.
"""

import os
import requests
from typing import Optional, Dict, Any
from datetime import datetime


class AbstractClient:
    """
    Abstract API 클라이언트

    지원하는 API:
    - Exchange Rates API
    - Phone Validation API
    - Date & Time API
    - IP Geolocation API
    - Email Validation API
    - Holidays API
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        AbstractClient 초기화

        Args:
            api_key: Abstract API 키. None이면 환경변수 ABSTRACT_API_KEY 사용
        """
        self.api_key = api_key or os.getenv("ABSTRACT_API_KEY")
        if not self.api_key:
            raise ValueError("Abstract API 키가 필요합니다. "
                           "환경변수 ABSTRACT_API_KEY를 설정하거나 인자로 전달하세요.")

        self.base_url = "https://api.abstractapi.com/v1"
        self.session = requests.Session()

    # ==================== Exchange Rates API ====================

    def get_live_exchange_rates(self) -> Dict[str, Any]:
        """
        실시간 환율 조회

        Returns:
            환율 정보 응답 (USD 기준)
        """
        url = f"{self.base_url}/exchange_rates"
        params = {"api_key": self.api_key}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def convert_exchange_rates(
        self,
        amount: float,
        base: str,
        target: str
    ) -> Dict[str, Any]:
        """
        환율 변환

        Args:
            amount: 변환할 금액
            base: 기준 통화 (ex: USD)
            target: 대상 통화 (ex: KRW)

        Returns:
            변환된 금액 정보
        """
        url = f"{self.base_url}/exchange_rates/convert"
        params = {
            "api_key": self.api_key,
            "api_base": base,
            "api_target": target,
            "api_amount": str(amount)
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    # ==================== Phone Validation API ====================

    def validate_phone_number(
        self,
        phone_number: str,
        country_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        전화번호 유효성 검사

        Args:
            phone_number: 전화번호 (E.164 형식 권장)
            country_code: 국가 코드 (ex: US, KR)

        Returns:
            전화번호 유효성 검사 결과
        """
        url = f"{self.base_url}/phone_validation"
        params = {
            "api_key": self.api_key,
            "phone_number": phone_number
        }
        if country_code:
            params["country_code"] = country_code
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    # ==================== Date & Time API ====================

    def get_current_time(
        self,
        location: Optional[str] = None,
        timezone: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        현재 시간 조회

        Args:
            location: 도시 또는 지역명 (ex: Tokyo, New York)
            timezone: 타임존 (ex: Asia/Tokyo, America/New_York)

        Returns:
            현재 시간 정보
        """
        url = f"{self.base_url}/date_time"
        params = {"api_key": self.api_key}
        if location:
            params["location"] = location
        if timezone:
            params["timezone"] = timezone
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def convert_time(
        self,
        base_location: str,
        base_date: str,
        base_time: str,
        target_location: str
    ) -> Dict[str, Any]:
        """
        시간 변환

        Args:
            base_location: 기준 도시 (ex: Tokyo)
            base_date: 기준 날짜 (YYYY-MM-DD 형식)
            base_time: 기준 시간 (HH:MM 형식, 24시간제)
            target_location: 대상 도시 (ex: New York)

        Returns:
            변환된 시간 정보
        """
        url = f"{self.base_url}/date_time/convert"
        params = {
            "api_key": self.api_key,
            "base_location": base_location,
            "base_date": base_date,
            "base_time": base_time,
            "target_location": target_location
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    # ==================== IP Geolocation API ====================

    def get_ip_geolocation(self, ip_address: str) -> Dict[str, Any]:
        """
        IP 주소 기반 지리적 정보 조회

        Args:
            ip_address: IP 주소

        Returns:
            IP 지리적 정보 (국가, 도시, 위도/경도 등)
        """
        url = f"{self.base_url}/ip_geolocation"
        params = {
            "api_key": self.api_key,
            "ip_address": ip_address
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    # ==================== Email Validation API ====================

    def validate_email(self, email: str) -> Dict[str, Any]:
        """
        이메일 유효성 검사

        Args:
            email: 이메일 주소

        Returns:
            이메일 유효성 검사 결과 (형식, MX 레코드, SMTP 등)
        """
        url = f"{self.base_url}/email_verification"
        params = {
            "api_key": self.api_key,
            "email": email
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    # ==================== Holidays API ====================

    def get_country_holidays(
        self,
        country: str,
        year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        국가 공휴일 조회

        Args:
            country: 국가 코드 (ISO 3166-1 alpha-2, ex: US, KR, JP)
            year: 연도 (지정하지 않으면 현재 연도)

        Returns:
            연중 공휴일 목록
        """
        if year is None:
            year = datetime.now().year

        url = f"{self.base_url}/holidays"
        params = {
            "api_key": self.api_key,
            "country": country,
            "year": year
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def close(self):
        """세션 종료"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
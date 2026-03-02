"""
Abstract API Client

Yoom Apps自動化のためのAbstract API統合クライアント。
"""

import os
import requests
from typing import Optional, Dict, Any
from datetime import datetime


class AbstractClient:
    """
    Abstract API クライアント

    サポートするAPI：
    - Exchange Rates API
    - Phone Validation API
    - Date & Time API
    - IP Geolocation API
    - Email Validation API
    - Holidays API
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        AbstractClient 初期化

        Args:
            api_key: Abstract API キー。 Noneの場合、環境変数ABSTRACT_API_KEYを使用する
        """
        self.api_key = api_key or os.getenv("ABSTRACT_API_KEY")
        if not self.api_key:
            raise ValueError("Abstract API キーが必要です。"
                           「環境変数ABSTRACT_API_KEYを設定するか、引数として渡してください。」）

        self.base_url = "https://api.abstractapi.com/v1"
        self.session = requests.Session()

    # ==================== Exchange Rates API ====================

    def get_live_exchange_rates(self) -> Dict[str, Any]:
        """
        リアルタイム為替レートの表示

        Returns:
            為替レート情報の回答(USDに基づく)
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
        為替レート変換

        Args:
            amount: 変換する金額
            base: 基準通貨 (ex: USD)
            target: 宛先通貨 (ex: JPY)

        Returns:
            変換された金額情報
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
        電話番号の検証

        Args:
            phone_number：電話番号（E.164形式を推奨）
            country_code: 国コード (ex: US, JP)

        Returns:
            電話番号検証結果
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
        現在時刻の照会

        Args:
            location: 都市または地域名 (ex: Tokyo, New York)
            timezone: タイムゾーン (ex: Asia/Tokyo, America/New_York)

        Returns:
            現在時刻情報
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
        時間変換

        Args:
            base_location：基準都市（ex：東京）
            base_date：基準日（YYYY-MM-DD形式）
            base_time：基準時間（HH：MM形式、24時間制）
            target_location: 対象都市 (ex: New York)

        Returns:
            変換された時間情報
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
        IPアドレスベースの地理的情報検索

        Args:
            ip_address: IP アドレス

        Returns:
            IP地理的情報（国、都市、緯度/経度など）
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
        電子メールの検証

        Args:
            email: メールアドレス

        Returns:
            電子メールの検証結果（フォーマット、MXレコード、SMTPなど）
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
        国の祝日の照会

        Args:
            country: 国コード (ISO 3166-1 alpha-2, ex: US, KR, JP)
            year：年（指定しない場合は現在の年）

        Returns:
            年中祝日一覧
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
        """セッション終了"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
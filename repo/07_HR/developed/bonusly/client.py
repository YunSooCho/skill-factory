"""
Bonusly API Client - Employee Recognition & Rewards Platform
"""

import requests
import time
from typing import Optional, Dict, Any, List


class BonuslyError(Exception):
    """Base exception for Bonusly"""

class BonuslyRateLimitError(BonuslyError):
    """Rate limit exceeded"""

class BonuslyAuthenticationError(BonuslyError):
    """Authentication failed"""

class BonuslyClient:
    BASE_URL = "https://bonus.ly/api/v3"

    def __init__(self, api_key: str, timeout: int = 30):
        """
        Initialize Bonusly client

        Args:
            api_key: Bonusly API key
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

        # Rate limiting
        self.last_request_time = 0
        self.min_delay = 0.5

    def _enforce_rate_limit(self):
        """Enforce rate limiting"""
        current = time.time()
        elapsed = current - self.last_request_time
        if elapsed < self.min_delay:
            time.sleep(self.min_delay - elapsed)
        self.last_request_time = time.time()

    def _handle_response(self, resp: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        if resp.status_code == 429:
            raise BonuslyRateLimitError("Rate limit exceeded")
        if resp.status_code == 401 or resp.status_code == 403:
            raise BonuslyAuthenticationError("Authentication failed")
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise BonuslyError(f"Error ({resp.status_code}): {error_data}")
            except Exception:
                raise BonuslyError(f"Error ({resp.status_code}): {resp.text}")

        if resp.status_code == 204:
            return {}

        return resp.json()

    # Users
    def get_users(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of users"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/users", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/users/{user_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def get_current_user(self) -> Dict[str, Any]:
        """Get current user details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/users/me", timeout=self.timeout)
        return self._handle_response(resp)

    # Bonuses
    def get_bonuses(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list of bonuses"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/bonuses", params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_bonus(self, bonus_id: str) -> Dict[str, Any]:
        """Get specific bonus details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/bonuses/{bonus_id}", timeout=self.timeout)
        return self._handle_response(resp)

    def create_bonus(self, bonus_data: Dict) -> Dict[str, Any]:
        """Create a bonus"""
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/bonuses", json=bonus_data, timeout=self.timeout)
        return self._handle_response(resp)

    def delete_bonus(self, bonus_id: str) -> Dict[str, Any]:
        """Delete a bonus"""
        self._enforce_rate_limit()
        resp = self.session.delete(f"{self.BASE_URL}/bonuses/{bonus_id}", timeout=self.timeout)
        return self._handle_response(resp)

    # Rewards
    def get_rewards(self) -> Dict[str, Any]:
        """Get list of available rewards"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/rewards", timeout=self.timeout)
        return self._handle_response(resp)

    def get_reward(self, reward_id: str) -> Dict[str, Any]:
        """Get reward details"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/rewards/{reward_id}", timeout=self.timeout)
        return self._handle_response(resp)

    # Achievements
    def get_achievements(self) -> Dict[str, Any]:
        """Get list of achievements"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/achievements", timeout=self.timeout)
        return self._handle_response(resp)

    # Leaderboards
    def get_leaderboard(self) -> Dict[str, Any]:
        """Get leaderboard"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/leaderboard", timeout=self.timeout)
        return self._handle_response(resp)

    # Company
    def get_company(self) -> Dict[str, Any]:
        """Get company information"""
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/company", timeout=self.timeout)
        return self._handle_response(resp)
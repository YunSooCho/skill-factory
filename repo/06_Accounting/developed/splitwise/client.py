"""
Splitwise API Client - Expense Sharing Platform

Splitwise is a popular expense-sharing app that helps track shared expenses
and settle debts between friends, roommates, and groups.
"""

import requests
import time
from typing import Optional, Dict, Any, List


class SplitwiseError(Exception):
    """Base exception for Splitwise errors"""

class SplitwiseRateLimitError(SplitwiseError):
    """Rate limit exceeded"""

class SplitwiseAuthenticationError(SplitwiseError):
    """Authentication failed"""

class SplitwiseClient:
    """
    Client for Splitwise REST API.
    API: https://dev.splitwise.com/
    """

    BASE_URL = "https://www.splitwise.com/api/v3.0"

    def __init__(self, api_key: str, consumer_key: Optional[str] = None,
                 consumer_secret: Optional[str] = None, timeout: int = 30):
        """
        Initialize Splitwise client.

        Args:
            api_key: Splitwise API key
            consumer_key: OAuth consumer key (optional)
            consumer_secret: OAuth consumer secret (optional)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
        self.min_delay = 0.2
        self.last_request_time = 0

    def _enforce_rate_limit(self):
        """Enforce rate limiting between requests"""
        current = time.time()
        if (current - self.last_request_time) < self.min_delay:
            time.sleep(self.min_delay - (current - self.last_request_time))
        self.last_request_time = time.time()

    def _handle_response(self, resp: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors"""
        if resp.status_code == 429:
            raise SplitwiseRateLimitError("Rate limit exceeded")
        if resp.status_code == 401:
            raise SplitwiseAuthenticationError("Authentication failed")
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise SplitwiseError(f"Error ({resp.status_code}): {error_data}")
            except:
                raise SplitwiseError(f"Error ({resp.status_code}): {resp.text}")
        return resp.json()

    def get_current_user(self) -> Dict[str, Any]:
        """
        Get information about the current authenticated user.

        Returns:
            User information
        """
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/get_current_user",
                               timeout=self.timeout)
        return self._handle_response(resp)

    def get_user(self, user_id: int) -> Dict[str, Any]:
        """
        Get information about a specific user.

        Args:
            user_id: User ID

        Returns:
            User information
        """
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/get_user/{user_id}",
                               timeout=self.timeout)
        return self._handle_response(resp)

    def get_friends(self, limit: int = 100) -> Dict[str, Any]:
        """
        Get list of friends.

        Args:
            limit: Maximum number of results

        Returns:
            List of friends
        """
        self._enforce_rate_limit()
        params = {'limit': limit}
        resp = self.session.get(f"{self.BASE_URL}/get_friends",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_groups(self) -> Dict[str, Any]:
        """
        Get list of groups.

        Returns:
            List of groups
        """
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/get_groups",
                               timeout=self.timeout)
        return self._handle_response(resp)

    def get_group(self, group_id: int) -> Dict[str, Any]:
        """
        Get information about a specific group.

        Args:
            group_id: Group ID

        Returns:
            Group information
        """
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/get_group/{group_id}",
                               timeout=self.timeout)
        return self._handle_response(resp)

    def create_group(self, name: str, simplify_by_default: bool = True,
                     users: Optional[List[int]] = None) -> Dict[str, Any]:
        """
        Create a new group.

        Args:
            name: Group name
            simplify_by_default: Whether to simplify debts
            users: List of user IDs to add to group

        Returns:
            Created group
        """
        self._enforce_rate_limit()
        data = {
            'name': name,
            'simplify_by_default': simplify_by_default
        }
        if users:
            data['users'] = users
        resp = self.session.post(f"{self.BASE_URL}/create_group",
                                json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_group(self, group_id: int, group_data: Dict) -> Dict[str, Any]:
        """
        Update an existing group.

        Args:
            group_id: Group ID
            group_data: Updated group data

        Returns:
            Updated group
        """
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/update_group/{group_id}"
        resp = self.session.post(url, json=group_data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_expenses(self, group_id: Optional[int] = None,
                     friend_id: Optional[int] = None,
                     dated_after: Optional[str] = None,
                     dated_before: Optional[str] = None,
                     updated_after: Optional[str] = None,
                     updated_before: Optional[str] = None,
                     limit: int = 100) -> Dict[str, Any]:
        """
        Get list of expenses.

        Args:
            group_id: Filter by group ID
            friend_id: Filter by friend ID
            dated_after: Filter expenses after this date (YYYY-MM-DD)
            dated_before: Filter expenses before this date (YYYY-MM-DD)
            updated_after: Filter updated after this datetime
            updated_before: Filter updated before this datetime
            limit: Maximum number of results

        Returns:
            List of expenses
        """
        self._enforce_rate_limit()
        params = {'limit': limit}
        if group_id:
            params['group_id'] = group_id
        if friend_id:
            params['friend_id'] = friend_id
        if dated_after:
            params['dated_after'] = dated_after
        if dated_before:
            params['dated_before'] = dated_before
        if updated_after:
            params['updated_after'] = updated_after
        if updated_before:
            params['updated_before'] = updated_before

        resp = self.session.get(f"{self.BASE_URL}/get_expenses",
                               params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_expense(self, expense_id: int) -> Dict[str, Any]:
        """
        Get information about a specific expense.

        Args:
            expense_id: Expense ID

        Returns:
            Expense information
        """
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/get_expense/{expense_id}",
                               timeout=self.timeout)
        return self._handle_response(resp)

    def create_expense(self, description: str, cost: float,
                      payment_method: int, group_id: Optional[int] = None,
                      friend_ids: Optional[List[int]] = None,
                      split_equally: bool = True,
                      date: str = None,
                      category_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Create a new expense.

        Args:
            description: Expense description
            cost: Amount of expense
            payment_method: Payment method (0=other, 1=cash, 2=credit card)
            group_id: Group ID (optional)
            friend_ids: List of friend IDs (if not using group)
            split_equally: Whether to split equally
            date: Date in YYYY-MM-DD format
            category_id: Category ID

        Returns:
            Created expense
        """
        self._enforce_rate_limit()
        data = {
            'description': description,
            'cost': str(cost),
            'payment_method': payment_method,
            'split_equally': split_equally
        }
        if group_id:
            data['group_id'] = group_id
        if friend_ids:
            data['friend_ids'] = friend_ids
        if date:
            data['date'] = date
        if category_id:
            data['category_id'] = category_id

        resp = self.session.post(f"{self.BASE_URL}/create_expense",
                                json=data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_expense(self, expense_id: int, expense_data: Dict) -> Dict[str, Any]:
        """
        Update an existing expense.

        Args:
            expense_id: Expense ID
            expense_data: Updated expense data

        Returns:
            Updated expense
        """
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/update_expense/{expense_id}",
                                json=expense_data, timeout=self.timeout)
        return self._handle_response(resp)

    def delete_expense(self, expense_id: int) -> Dict[str, Any]:
        """
        Delete an expense.

        Args:
            expense_id: Expense ID

        Returns:
            Deletion confirmation
        """
        self._enforce_rate_limit()
        resp = self.session.post(f"{self.BASE_URL}/delete_expense/{expense_id}",
                                timeout=self.timeout)
        return self._handle_response(resp)

    def get_notifications(self, limit: int = 100) -> Dict[str, Any]:
        """
        Get list of notifications.

        Args:
            limit: Maximum number of results

        Returns:
            List of notifications
        """
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/get_notifications",
                               params={'limit': limit}, timeout=self.timeout)
        return self._handle_response(resp)

    def get_categories(self) -> Dict[str, Any]:
        """
        Get list of expense categories.

        Returns:
            List of categories
        """
        self._enforce_rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/get_categories",
                               timeout=self.timeout)
        return self._handle_response(resp)

    def send_reminder(self, group_id: int, user_id: int) -> Dict[str, Any]:
        """
        Send a reminder to a user to clear their debts.

        Args:
            group_id: Group ID
            user_id: User ID to remind

        Returns:
            Reminder confirmation
        """
        self._enforce_rate_limit()
        url = f"{self.BASE_URL}/send_reminder/{group_id}/{user_id}"
        resp = self.session.get(url, timeout=self.timeout)
        return self._handle_response(resp)
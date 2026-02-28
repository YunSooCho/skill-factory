"""
AskHandle Customer Support API Client

This module provides a Python client for interacting with the AskHandle
customer support platform API.
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime


class AskHandleClient:
    """
    Client for AskHandle Customer Support Platform API.

    AskHandle provides:
    - Ticket management
    - Multi-channel support (email, chat, social)
    - Team collaboration
    - Knowledge base
    - Customer management
    - Automation and workflows
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.askhandle.com/v1",
        timeout: int = 30
    ):
        """
        Initialize the AskHandle client.

        Args:
            api_key: Your AskHandle API key
            base_url: API base URL (default: https://api.askhandle.com/v1)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an authenticated request to the API.

        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            data: Request body data

        Returns:
            Response JSON
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(
            method,
            url,
            params=params,
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def get_tickets(
        self,
        status: Optional[str] = None,
        assignee: Optional[str] = None,
        priority: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get list of tickets.

        Args:
            status: Filter by status (optional)
            assignee: Filter by assignee (optional)
            priority: Filter by priority (optional)
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of tickets
        """
        params = {
            'limit': limit,
            'offset': offset
        }
        if status:
            params['status'] = status
        if assignee:
            params['assignee'] = assignee
        if priority:
            params['priority'] = priority

        result = self._request('GET', '/tickets', params=params)
        return result.get('tickets', [])

    def get_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """
        Get ticket details.

        Args:
            ticket_id: Ticket ID

        Returns:
            Ticket details
        """
        return self._request('GET', f'/tickets/{ticket_id}')

    def create_ticket(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new ticket.

        Args:
            data: Ticket data including customer_id, subject, description, priority, etc.

        Returns:
            Created ticket details
        """
        return self._request('POST', '/tickets', data=data)

    def update_ticket(self, ticket_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a ticket.

        Args:
            ticket_id: Ticket ID
            data: Fields to update

        Returns:
            Updated ticket details
        """
        return self._request('PUT', f'/tickets/{ticket_id}', data=data)

    def delete_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """
        Delete a ticket.

        Args:
            ticket_id: Ticket ID

        Returns:
            Deletion result
        """
        return self._request('DELETE', f'/tickets/{ticket_id}')

    def add_comment(
        self,
        ticket_id: str,
        message: str,
        internal: bool = False,
        author_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add a comment to a ticket.

        Args:
            ticket_id: Ticket ID
            message: Comment message
            internal: Whether comment is internal only
            author_id: Author ID (optional)

        Returns:
            Created comment details
        """
        data = {
            'message': message,
            'internal': internal
        }
        if author_id:
            data['author_id'] = author_id

        return self._request('POST', f'/tickets/{ticket_id}/comments', data=data)

    def get_comments(self, ticket_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get comments for a ticket.

        Args:
            ticket_id: Ticket ID
            limit: Maximum number of comments

        Returns:
            List of comments
        """
        params = {'limit': limit}
        result = self._request('GET', f'/tickets/{ticket_id}/comments', params=params)
        return result.get('comments', [])

    def assign_ticket(
        self,
        ticket_id: str,
        assignee_id: str,
        comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Assign a ticket to an agent.

        Args:
            ticket_id: Ticket ID
            assignee_id: Agent user ID to assign to
            comment: Optional assignment comment

        Returns:
            Updated ticket details
        """
        data = {'assignee_id': assignee_id}
        if comment:
            data['assign_comment'] = comment

        return self._request('POST', f'/tickets/{ticket_id}/assign', data=data)

    def change_status(
        self,
        ticket_id: str,
        status: str,
        comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Change ticket status.

        Args:
            ticket_id: Ticket ID
            status: New status
            comment: Optional status change comment

        Returns:
            Updated ticket details
        """
        data = {'status': status}
        if comment:
            data['comment'] = comment

        return self._request('POST', f'/tickets/{ticket_id}/status', data=data)

    def merge_tickets(
        self,
        target_ticket_id: str,
        source_ticket_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Merge multiple tickets into one.

        Args:
            target_ticket_id: ID of target ticket (merged into)
            source_ticket_ids: List of ticket IDs to merge

        Returns:
            Merge result
        """
        data = {
            'target_ticket_id': target_ticket_id,
            'source_ticket_ids': source_ticket_ids
        }

        return self._request('POST', '/tickets/merge', data=data)

    def get_customers(
        self,
        email: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get list of customers.

        Args:
            email: Filter by email (optional)
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of customers
        """
        params = {
            'limit': limit,
            'offset': offset
        }
        if email:
            params['email'] = email

        result = self._request('GET', '/customers', params=params)
        return result.get('customers', [])

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """
        Get customer details.

        Args:
            customer_id: Customer ID

        Returns:
            Customer details
        """
        return self._request('GET', f'/customers/{customer_id}')

    def create_customer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new customer.

        Args:
            data: Customer data including name, email, phone, etc.

        Returns:
            Created customer details
        """
        return self._request('POST', '/customers', data=data)

    def update_customer(self, customer_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update customer information.

        Args:
            customer_id: Customer ID
            data: Fields to update

        Returns:
            Updated customer details
        """
        return self._request('PUT', f'/customers/{customer_id}', data=data)

    def get_customer_tickets(self, customer_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get tickets for a customer.

        Args:
            customer_id: Customer ID
            limit: Maximum number of tickets

        Returns:
            List of tickets
        """
        params = {'limit': limit}
        result = self._request('GET', f'/customers/{customer_id}/tickets', params=params)
        return result.get('tickets', [])

    def get_agents(self) -> List[Dict[str, Any]]:
        """
        Get list of support agents.

        Returns:
            List of agents
        """
        result = self._request('GET', '/agents')
        return result.get('agents', [])

    def get_agent(self, agent_id: str) -> Dict[str, Any]:
        """
        Get agent details.

        Args:
            agent_id: Agent ID

        Returns:
            Agent details
        """
        return self._request('GET', f'/agents/{agent_id}')

    def get_queues(self) -> List[Dict[str, Any]]:
        """
        Get list of ticket queues.

        Returns:
            List of queues
        """
        result = self._request('GET', '/queues')
        return result.get('queues', [])

    def get_articles(
        self,
        category: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get knowledge base articles.

        Args:
            category: Filter by category (optional)
            limit: Maximum number of articles
            offset: Pagination offset

        Returns:
            List of articles
        """
        params = {
            'limit': limit,
            'offset': offset
        }
        if category:
            params['category'] = category

        result = self._request('GET', '/articles', params=params)
        return result.get('articles', [])

    def get_article(self, article_id: str) -> Dict[str, Any]:
        """
        Get article details.

        Args:
            article_id: Article ID

        Returns:
            Article details
        """
        return self._request('GET', f'/articles/{article_id}')

    def create_article(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a knowledge base article.

        Args:
            data: Article data including title, content, category, etc.

        Returns:
            Created article details
        """
        return self._request('POST', '/articles', data=data)

    def get_tags(self) -> List[Dict[str, Any]]:
        """
        Get list of tags.

        Returns:
            List of tags
        """
        result = self._request('GET', '/tags')
        return result.get('tags', [])

    def search(self, query: str, limit: int = 20) -> Dict[str, Any]:
        """
        Search across tickets, customers, and articles.

        Args:
            query: Search query
            limit: Maximum number of results per type

        Returns:
            Search results
        """
        params = {'query': query, 'limit': limit}
        return self._request('GET', '/search', params=params)

    def get_statistics(
        self,
        start_date: str,
        end_date: str
    ) -> Dict[str, Any]:
        """
        Get support statistics.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            Statistics including ticket volumes, response times, etc.
        """
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        return self._request('GET', '/statistics', params=params)

    def create_ticket_from_webhook(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a ticket from webhook data.

        Args:
            data: Webhook data

        Returns:
            Created ticket details
        """
        return self._request('POST', '/webhooks/ticket', data=data)
import requests
from typing import Dict, List, Optional


class KasikaClient:
    """Client for Kasika API - Japanese CRM Platform"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.kasika.jp"
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}

    def invite_employee(self, email: str, **kwargs) -> Dict:
        data = {'email': email, **kwargs}
        return self._request('POST', '/v1/employees/invite', json=data)

    def send_inquiry_notification_email(self, data: Dict) -> Dict:
        return self._request('POST', '/v1/inquiry/notification', json=data)

    def get_sales_action_types(self) -> List[Dict]:
        result = self._request('GET', '/v1/sales/actions/types')
        return result.get('types', [])

    def get_customer(self, customer_id: str) -> Dict:
        return self._request('GET', f'/v1/customers/{customer_id}')

    def bulk_delete_customer_tags(self, customer_ids: List[str], tag: str) -> Dict:
        return self._request('POST', '/v1/customers/tags/bulk-delete', json={
            'customer_ids': customer_ids,
            'tag': tag
        })

    def delete_customer(self, customer_id: str) -> Dict:
        return self._request('DELETE', f'/v1/customers/{customer_id}')

    def export_customer_csv(self, **filter_params) -> str:
        result = self._request('POST', '/v1/customers/export', json=filter_params)
        return result.get('download_url', '')

    def update_sales_action(self, action_id: str, data: Dict) -> Dict:
        return self._request('PUT', f'/v1/sales/actions/{action_id}', json=data)

    def assign_agent_by_postal_code(self, postal_code: str) -> Dict:
        return self._request('POST', '/v1/agents/assign', json={'postal_code': postal_code})

    def get_inquiry(self, inquiry_id: str) -> Dict:
        return self._request('GET', f'/v1/inquiries/{inquiry_id}')

    def create_sales_action(self, action_data: Dict) -> Dict:
        return self._request('POST', '/v1/sales/actions', json=action_data)

    def get_sales_action_types_list(self) -> List[Dict]:
        result = self._request('GET', '/v1/sales/actions/types/list')
        return result.get('types', [])

    def get_customer_id_change_history(self, customer_id: str) -> List[Dict]:
        return self._request('GET', f'/v1/customers/{customer_id}/id/history')

    def add_customer_external_activity(self, customer_id: str, activity: Dict) -> Dict:
        return self._request('POST', f'/v1/customers/{customer_id}/activities', json=activity)

    def remove_customer_agent(self, customer_id: str, agent_id: str) -> Dict:
        return self._request('DELETE', f'/v1/customers/{customer_id}/agents/{agent_id}')

    def add_email_address(self, customer_id: str, email: str) -> Dict:
        return self._request('POST', f'/v1/customers/{customer_id}/emails', json={'email': email})

    def update_employee_status(self, employee_id: str, status: str) -> Dict:
        return self._request('PUT', f'/v1/employees/{employee_id}/status', json={'status': status})

    def delete_inquiry(self, inquiry_id: str) -> Dict:
        return self._request('DELETE', f'/v1/inquiries/{inquiry_id}')

    def update_customer(self, customer_id: str, data: Dict) -> Dict:
        return self._request('PUT', f'/v1/customers/{customer_id}', json=data)

    def register_customer(self, customer_data: Dict) -> Dict:
        return self._request('POST', '/v1/customers', json=customer_data)

    def add_customer_agent(self, customer_id: str, agent_id: str, **kwargs) -> Dict:
        data = {'agent_id': agent_id, **kwargs}
        return self._request('POST', f'/v1/customers/{customer_id}/agents', json=data)

    def export_optout_customers_csv(self, **filter_params) -> str:
        result = self._request('POST', '/v1/customers/export/optout', json=filter_params)
        return result.get('download_url', '')

    def bulk_add_customer_tags(self, customer_ids: List[str], tag: str) -> Dict:
        return self._request('POST', '/v1/customers/tags/bulk-add', json={
            'customer_ids': customer_ids,
            'tag': tag
        })

    def export_hot_customers_csv(self, **filter_params) -> str:
        result = self._request('POST', '/v1/customers/export/hot', json=filter_params)
        return result.get('download_url', '')

    def list_sales_actions(self, **filter_params) -> List[Dict]:
        result = self._request('GET', '/v1/sales/actions', params=filter_params)
        return result.get('actions', [])
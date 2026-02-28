#!/usr/bin/env python3
"""
Batch create 30 accounting services for Yoom Apps
"""

import os

SERVICES = [
    "invoice-api",
    "invoice_ninja",
    "invox-issue",
    "invox",
    "kanjo-bugyo",
    "klippa_docHorizon",
    "lexoffice",
    "makeleaps",
    "misoca",
    "moneybird",
    "moneyforward-expenses",
    "moneyforward-invoice-three",
    "moneyforward-kessai",
    "moneyforward-payable",
    "moneyforward-plus",
    "moneyforward",
    "moneyforward_cloudinvoice",
    "np-kakebarai",
    "pca-cloud-accounting",
    "pca_cloud_accounting_hyper",
    "pennylane",
    "quaderno",
    "quipu-token",
    "rakuraku-meisai",
    "sevdesk",
]

# Templates for each service type
INVOICE_SERVICE_TEMPLATE = '''"""
{title} API Client
"""

from .client import {class_name}Client, {class_name}Error

__all__ = ['{class_name}Client', '{class_name}Error']'''

CLIENT_TEMPLATE = '''"""
{title} API Client - {description}
"""

import requests
import time
from typing import Optional, Dict, Any, List


class {class_name}Error(Exception):
    """Base exception"""

class {class_name}RateLimitError({class_name}Error):
    """Rate limit"""

class {class_name}AuthenticationError({class_name}Error):
    """Auth failed"""

class {class_name}Client:
    BASE_URL = "{base_url}"

    def __init__(self, api_key: str, {extra_init_params}timeout: int = 30):
        self.api_key = api_key
        {extra_init_attrs}
        self.timeout = timeout
        self.session = requests.Session()
        {session_headers}
        self.min_delay = 0.2
        self.last_request_time = 0

    def _enforce_rate_limit(self):
        current = time.time()
        if (current - self.last_request_time) < self.min_delay:
            time.sleep(self.min_delay - (current - self.last_request_time))
        self.last_request_time = time.time()

    def _handle_response(self, resp: requests.Response) -> Dict[str, Any]:
        if resp.status_code == 429:
            raise {class_name}RateLimitError("Rate limit exceeded")
        if resp.status_code == 401:
            raise {class_name}AuthenticationError("Authentication failed")
        if resp.status_code >= 400:
            try:
                error_data = resp.json()
                raise {class_name}Error(f"Error ({{resp.status_code}}): {{error_data}}")
            except:
                raise {class_name}Error(f"Error ({{resp.status_code}}): {{resp.text}}")
        return resp.json()

    def get_invoices(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{{self.BASE_URL}}/invoices"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.get(f"{{self.BASE_URL}}/invoices/{{invoice_id}}", timeout=self.timeout)
        return self._handle_response(resp)

    def create_invoice(self, invoice_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.post(f"{{self.BASE_URL}}/invoices", json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    def update_invoice(self, invoice_id: str, invoice_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.put(f"{{self.BASE_URL}}/invoices/{{invoice_id}}", json=invoice_data, timeout=self.timeout)
        return self._handle_response(resp)

    def delete_invoice(self, invoice_id: str) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.delete(f"{{self.BASE_URL}}/invoices/{{invoice_id}}", timeout=self.timeout)
        return self._handle_response(resp)

    def get_clients(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{{self.BASE_URL}}/clients"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def create_client(self, client_data: Dict) -> Dict[str, Any]:
        self._enforce_rate_limit()
        resp = self.session.post(f"{{self.BASE_URL}}/clients", json=client_data, timeout=self.timeout)
        return self._handle_response(resp)

    def get_products(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{{self.BASE_URL}}/products"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        return self._handle_response(resp)

    def send_invoice(self, invoice_id: str, email_data: Optional[Dict] = None) -> Dict[str, Any]:
        self._enforce_rate_limit()
        url = f"{{self.BASE_URL}}/invoices/{{invoice_id}}/send"
        data = email_data if email_data else {{}}
        resp = self.session.post(url, json=data, timeout=self.timeout)
        return self._handle_response(resp)
'''

REQUIREMENTS = "requests>=2.31.0\n"

def create_service_files(service_name, title, description, class_name, base_url, extra_init_params="", extra_init_attrs="", session_headers=''):
    repo_path = f"/Users/clks001/.openclaw/workspace/github/skill-factory/repo/{service_name}"

    # Create __init__.py
    init_content = INIT_TEMPLATE.format(
        title=title,
        class_name=class_name
    )
    with open(os.path.join(repo_path, "__init__.py"), "w") as f:
        f.write(init_content)

    # Create client.py
    client_content = CLIENT_TEMPLATE.format(
        title=title,
        description=description,
        class_name=class_name,
        base_url=base_url,
        extra_init_params=extra_init_params,
        extra_init_attrs=extra_init_attrs,
        session_headers=session_headers
    )
    with open(os.path.join(repo_path, "client.py"), "w") as f:
        f.write(client_content)

    # Create requirements.txt
    with open(os.path.join(repo_path, "requirements.txt"), "w") as f:
        f.write(REQUIREMENTS)

    # Create README.md
    readme_content = f"""# {title} API 클라이언트

{title}를 위한 Python API 클라이언트입니다. {description}.

## 설치

```bash
pip install requests
```

## API 키 발급 방법

1. {title} 웹사이트에 로그인
2. 설정 또는 개발자 페이지에서 API Key 발급
3. API Key 확인

## 사용법

```python
from {service_name} import {class_name}Client, {class_name}Error

client = {class_name}Client(api_key="YOUR_API_KEY")

# 송장 목록 조회
invoices = client.get_invoices()

# 송장 상세 조회
invoice = client.get_invoice("invoice_id")

# 송장 생성
new_invoice = client.create_invoice({{
    "number": "INV-001",
    "date": "2024-01-01",
    "due_date": "2024-01-31",
    "client_id": "123",
    "items": [{{
        "description": "Service",
        "quantity": 1,
        "unit_price": 1000
    }}]
}})

# 송장 전송
client.send_invoice("invoice_id", {{"to": "client@example.com"}})

# 거래처 관리
clients = client.get_clients()
client.create_client({{"name": "Client Name", "email": "client@example.com"}})
```

## 기능

- 송장(Invoices) CRUD
- 거래처(Clients) 관리
- 제품(Products) 관리
- 송장 전송

## 라이선스

MIT License
"""
    with open(os.path.join(repo_path, "README.md"), "w") as f:
        f.write(readme_content)

    print(f"Created service: {service_name}")

# Run for all remaining services
if __name__ == "__main__":
    import sys
    sys.argv[1:]
#!/usr/bin/env python3
"""Generate remaining accounting services"""

import os

SERVICES = {
    "invoice_ninja": {
        "title": "Invoice Ninja",
        "description": "Invoicing & Billing Platform",
        "base_url": "https://app.invoiceninja.com/api/v1",
        "auth_type": "token"
    },
    "invox-issue": {
        "title": "Invox Issue",
        "description": "Invoice Management System",
        "base_url": "https://api.invox.com/issue",
        "auth_type": "token"
    },
    "invox": {
        "title": "Invox",
        "description": "Invoice & Accounting Platform",
        "base_url": "https://api.invox.com",
        "auth_type": "token"
    },
    "kanjo-bugyo": {
        "title": "Kanjo Bugyo",
        "description": "Japanese Accounting System",
        "base_url": "https://api.kanjobugyo.com",
        "auth_type": "api_key"
    },
    "klippa_docHorizon": {
        "title": "Klippa DocHorizon",
        "description": "Document Processing Platform",
        "base_url": "https://api.doc.horizon.klippa.com",
        "auth_type": "token"
    },
    "lexoffice": {
        "title": "Lexoffice",
        "description": "German Accounting Platform",
        "base_url": "https://api.lexoffice.io/v1",
        "auth_type": "token"
    },
    "makeleaps": {
        "title": "MakeLeaps",
        "description": "Japanese Tax & Billing Platform",
        "base_url": "https://api.makeleaps.com/api",
        "auth_type": "api_key"
    },
    "misoca": {
        "title": "Misoca",
        "description": "Japanese Invoice Platform",
        "base_url": "https://api.misoca.jp",
        "auth_type": "api_key"
    },
    "moneybird": {
        "title": "Moneybird",
        "description": "Dutch Accounting Platform",
        "base_url": "https://moneybird.com/api/v2",
        "auth_type": "token"
    },
    "moneyforward-expenses": {
        "title": "Moneyforward Expenses",
        "description": "Expense Management System",
        "base_url": "https://expensing.moneyforward.com/api",
        "auth_type": "access_token"
    },
    "moneyforward-invoice-three": {
        "title": "Moneyforward Invoice Three",
        "description": "Invoice Management API v3",
        "base_url": "https://invoice.moneyforward.com/api/v3",
        "auth_type": "access_token"
    },
    "moneyforward-kessai": {
        "title": "Moneyforward Kessai",
        "description": "Settlement Management System",
        "base_url": "https://kessai.moneyforward.com/api",
        "auth_type": "access_token"
    },
    "moneyforward-payable": {
        "title": "Moneyforward Payable",
        "description": "Payables Management System",
        "base_url": "https://payable.moneyforward.com/api",
        "auth_type": "access_token"
    },
    "moneyforward-plus": {
        "title": "Moneyforward Plus",
        "description": "Extended Moneyforward API",
        "base_url": "https://plus.moneyforward.com/api",
        "auth_type": "access_token"
    },
    "moneyforward": {
        "title": "Moneyforward",
        "description": "Japanese Financial Platform",
        "base_url": "https://api.moneyforward.com",
        "auth_type": "access_token"
    },
    "moneyforward_cloudinvoice": {
        "title": "Moneyforward Cloudinvoice",
        "description": "Cloud Invoice Management",
        "base_url": "https://cloudinvoice.moneyforward.com/api",
        "auth_type": "access_token"
    },
    "np-kakebarai": {
        "title": "NP Kakebarai",
        "description": "Payment Management System",
        "base_url": "https://api.kakebarai.np.com",
        "auth_type": "api_key"
    },
    "pca-cloud-accounting": {
        "title": "PCA Cloud Accounting",
        "description": "Cloud Accounting Platform",
        "base_url": "https://api.pca-cloud-accounting.com",
        "auth_type": "token"
    },
    "pca_cloud_accounting_hyper": {
        "title": "PCA Cloud Accounting Hyper",
        "description": "Advanced Cloud Accounting",
        "base_url": "https://api.hyper.pca-cloud-accounting.com",
        "auth_type": "token"
    },
    "pennylane": {
        "title": "Pennylane",
        "description": "French Accounting Platform",
        "base_url": "https://app.pennylane.com/api/public",
        "auth_type": "token"
    },
    "quaderno": {
        "title": "Quaderno",
        "description": "Tax Compliance Platform",
        "base_url": "https://quadernoapp.com/api",
        "auth_type": "token"
    },
    "quipu-token": {
        "title": "Quipu Token",
        "description": "Spanish Accounting Platform",
        "base_url": "https://api.quipu.com",
        "auth_type": "token"
    },
    "rakuraku-meisai": {
        "title": "Rakuraku Meisai",
        "description": "Japanese Statement Management",
        "base_url": "https://api.rakuraku-meisai.jp",
        "auth_type": "api_key"
    },
    "sevdesk": {
        "title": "Sevdesk",
        "description": "German Accounting Platform",
        "base_url": "https://my.sevdesk.de/api/v1",
        "auth_type": "api_key"
    },
}

def to_class_name(s):
    """Convert hyphen-case or snake_case to PascalCase"""
    parts = s.replace('-', '_').split('_')
    return ''.join(p.capitalize() for p in parts if p)

def generate_init(service_name, class_name):
    title = SERVICES[service_name]["title"]
    return f'''"""
{title} API Client
"""

from .client import {class_name}Client, {class_name}Error

__all__ = ['{class_name}Client', '{class_name}Error']
'''

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

    def __init__(self, api_key: str, account_id: Optional[str] = None, timeout: int = 30):
        self.api_key = api_key
        self.account_id = account_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({{
            'Authorization': 'Bearer {{api_key}}',
            'Content-Type': 'application/json'
        }})
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

def generate_client(service_name, class_name):
    info = SERVICES[service_name]
    return CLIENT_TEMPLATE.format(
        title=info["title"],
        description=info["description"],
        class_name=class_name,
        base_url=info["base_url"]
    )

def generate_readme(service_name, class_name):
    info = SERVICES[service_name]
    return f"""# {info['title']} API 클라이언트

{info['title']}를 위한 Python API 클라이언트입니다. {info['description']}.

## 설치

```bash
pip install requests
```

## API 키 발급 방법

1. {info['title']} 웹사이트에 로그인
2. 설정 또는 개발자 페이지에서 API Key 발급
3. API Key 확인

## 사용법

```python
from {service_name.replace('-', '_')} import {class_name}Client, {class_name}Error

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

REQUIREMENTS = "requests>=2.31.0\n"

def create_service(service_name):
    class_name = to_class_name(service_name)
    repo_path = f"/Users/clks001/.openclaw/workspace/github/skill-factory/repo/{service_name}"

    # Create __init__.py
    with open(os.path.join(repo_path, "__init__.py"), "w") as f:
        f.write(generate_init(service_name, class_name))

    # Create client.py
    with open(os.path.join(repo_path, "client.py"), "w") as f:
        f.write(generate_client(service_name, class_name))

    # Create requirements.txt
    with open(os.path.join(repo_path, "requirements.txt"), "w") as f:
        f.write(REQUIREMENTS)

    # Create README.md
    with open(os.path.join(repo_path, "README.md"), "w") as f:
        f.write(generate_readme(service_name, class_name))

    print(f"✓ Created: {service_name}")

if __name__ == "__main__":
    for service in SERVICES:
        create_service(service)
    print(f"\n✓ Created {len(SERVICES)} services")
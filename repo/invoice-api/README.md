# Invoice API 클라이언트

Invoice API를 위한 Python API 클라이언트입니다. 범용 송장 관리 기능을 제공합니다.

## 설치

```bash
pip install requests
```

## API 키 발급 방법

1. Invoice API 웹사이트에 로그인
2. 설정 > API Keys 메뉴에서 API Key 생성
3. API Key 확인

## 사용법

```python
from invoice_api import InvoiceAPIClient, InvoiceAPIError

client = InvoiceAPIClient(api_key="YOUR_API_KEY", account_id="YOUR_ACCOUNT_ID")

# 송장 목록 조회
invoices = client.get_invoices()

# 송장 상세 조회
invoice = client.get_invoice("invoice_id")

# 송장 생성
new_invoice = client.create_invoice({
    "number": "INV-001",
    "date": "2024-01-01",
    "due_date": "2024-01-31",
    "client_id": "123",
    "items": [{
        "description": "Service",
        "quantity": 1,
        "unit_price": 1000
    }]
})

# 송장 전송
client.send_invoice("invoice_id", {"to": "client@example.com"})

# 결제 관리
payments = client.get_payments()
client.create_payment({
    "invoice_id": "123",
    "amount": 1000,
    "date": "2024-01-15"
})

# 반복 송장
recurring_invoices = client.get_recurring_invoices()
```

## 기능

- 송장(Invoices) CRUD
- 거래처(Clients) 관리
- 제품(Products) 관리
- 송장 전송
- 결제(Payments) 관리
- 반복 송장(Recurring Invoices) 관리

## 라이선스

MIT License
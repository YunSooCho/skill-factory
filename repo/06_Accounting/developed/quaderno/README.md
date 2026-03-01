# Quaderno API 클라이언트

Quaderno를 위한 Python API 클라이언트입니다. Tax Compliance Platform.

## 설치

```bash
pip install requests
```

## API 키 발급 방법

1. Quaderno 웹사이트에 로그인
2. 설정 또는 개발자 페이지에서 API Key 발급
3. API Key 확인

## 사용법

```python
from quaderno import QuadernoClient, QuadernoError

client = QuadernoClient(api_key="YOUR_API_KEY")

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

# 거래처 관리
clients = client.get_clients()
client.create_client({"name": "Client Name", "email": "client@example.com"})
```

## 기능

- 송장(Invoices) CRUD
- 거래처(Clients) 관리
- 제품(Products) 관리
- 송장 전송

## 라이선스

MIT License

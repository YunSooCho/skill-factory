# Fatture in Cloud API 클라이언트

Fatture in Cloud를 위한 Python API 클라이언트입니다. 이탈리아 청구서 및 결제 관리 기능을 제공합니다.

## 설치

```bash
pip install requests
```

## API 키 발급 방법

1. [Fatture in Cloud](https://app.fattureincloud.it/)에 로그인
2. Settings > Developer > App Settings 이동
3. OAuth 앱 생성 또는 API 키 발급
4. Access Token 및 Company ID 확인

## 사용법

```python
from fatture_in_cloud import FattureInCloudClient, FattureInCloudError

client = FattureInCloudClient(access_token="YOUR_ACCESS_TOKEN", company_id="YOUR_COMPANY_ID")

# 청구서 목록 조회
invoices = client.get_invoices()

# 청구서 상세 조회
invoice = client.get_invoice("document_id")

# 청구서 생성
new_invoice = client.create_invoice({
    "date": "2024-01-01",
    "number": "INV-001",
    "currency": {
        "id": "EUR"
    },
    "client": {
        "id": 123
    },
    "items_list": [{
        "product": {
            "id": 456
        },
        "qty": 1,
        "unit_price": {
            "net_price": 1000
        }
    }]
})

# 청구서 이메일 발송
client.send_invoice("document_id", sender_id="1")

# 거래처 관리
clients = client.get_clients()
client.create_client({
    "data": {
        "name": "Client Name",
        "email": "client@example.com",
        "vat_number": "IT00000000000"
    }
})
```

## 기능

- 청구서 (Issued Documents) CRUD
- 수신 문서 (Received Documents) 관리
- 거래처 (Clients) 관리
- 제품 (Products) 관리
- 청구서 이메일 발송

## 라이선스

MIT License
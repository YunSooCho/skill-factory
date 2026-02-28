# Fakturoid API 클라이언트

Fakturoid을 위한 Python API 클라이언트입니다. 체코 송장 및 결제 관리 기능을 제공합니다.

## 설치

```bash
pip install requests
```

## API 키 발급 방법

1. [Fakturoid](https://app.fakturoid.cz/)에 로그인
2. Settings > API Keys 메뉴로 이동
3. API Key 생성 (Email과 API Key 필요)
4. Slug 확인 (계정 URL에서 확인 가능)

## 사용법

```python
from fakturoid import FakturoidClient, FakturoidError

client = FakturoidClient(
    email="your@email.com",
    api_key="YOUR_API_KEY",
    slug="your-slug"
)

# 송장 목록 조회
invoices = client.get_invoices(status="sent")

# 송장 상세 조회
invoice = client.get_invoice("invoice_id")

# 송장 생성
new_invoice = client.create_invoice({
    "subject_id": "123",
    "number": "2024001",
    "issued_on": "2024-01-01",
    "due_on": "2024-01-31",
    "lines": [{
        "name": "Service",
        "quantity": 1,
        "unit_price": 1000,
        "vat_rate": 21
    }]
})

# 송장 전송
client.send_invoice("invoice_id", message="Message")

# 송장 결제 처리
client.pay_invoice("invoice_id", "2024-01-15", "VS001", 1210.0)
```

## 기능

- 송장 CRUD (생성, 조회, 수정, 삭제)
- 거래처(Subject) 관리
- 송장 템플릿(Generator) 관리
- 송장 전송 및 결제 처리
- 계정 정보 조회

## 라이선스

MIT License
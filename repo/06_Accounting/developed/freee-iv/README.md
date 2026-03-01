# Freee Invoice API 클라이언트

Freee Invoice를 위한 Python API 클라이언트입니다. 일본 송장 및 회계 관리 기능을 제공합니다.

## 설치

```bash
pip install requests
```

## API 키 발급 방법

1. [Freee Developers](https://developers.freee.co.jp/)에 접속
2. 애플리케이션 등록
3. OAuth2 인증을 통해 Access Token 획득
4. Company ID 확인

## 사용법

```python
from freee_iv import FreeeIVClient, FreeeIVError

client = FreeeIVClient(access_token="YOUR_ACCESS_TOKEN", company_id="YOUR_COMPANY_ID")

# 송장(거래) 목록 조회
invoices = client.get_invoices()

# 송장 상세 조회
invoice = client.get_invoice("invoice_id")

# 송장 생성
new_invoice = client.create_invoice({
    "issue_date": "2024-01-01",
    "payment_date": "2024-01-31",
    "partner_id": 123,
    "type": "income",
    "details": [{
        "item_id": 456,
        "quantity": 1,
        "unit_price": 1000
    }]
})

# 거래처 관리
partners = client.get_partners()

# 품목 관리
items = client.get_items()

# 지갑 거래 내역
wallet_txns = client.get_wallet_txns("wallet_id")
```

## 기능

- 송장/거래(Deals) CRUD
- 거래처(Partners) 관리
- 품목(Items) 관리
- 지갑 거래(Wallet Transactions) 관리
- 송장 이메일 발송
- 회사 정보 조회

## 라이선스

MIT License
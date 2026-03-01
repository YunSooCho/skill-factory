# Freee API 클라이언트

Freee를 위한 Python API 클라이언트입니다. 일본 종합 회계 플랫폼 기능을 제공합니다.

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
from freee import FreeeClient, FreeeError

client = FreeeClient(access_token="YOUR_ACCESS_TOKEN", company_id="YOUR_COMPANY_ID")

# 거래 내역 조회
deals = client.get_deals()

# 거래 상세 조회
deal = client.get_deal("deal_id")

# 거래 생성
new_deal = client.create_deal({
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

# 지갑/자산 관리
walletables = client.get_walletables()
wallet_txns = client.get_wallet_txns("wallet_id")

# 경비 관리
expenses = client.get_expenses()
client.create_expense({
    "date": "2024-01-01",
    "walletable_id": 123,
    "amount": 500,
    "orignal_amount": 500
})

# 계좌이동
client.create_transfer({
    "from_walletable_id": 123,
    "to_walletable_id": 456,
    "date": "2024-01-01",
    "amount": 1000
})
```

## 기능

- 거래(Deals) CRUD
- 거래처(Partners) 관리
- 지갑/자산(Walletables) 관리
- 지갑 거래(Wallet Transactions) 관리
- 직접 경비(Direct Expenses) 관리
- 계좌이동(Transfers) 관리
- 송금 템플릿 관리

## 라이선스

MIT License
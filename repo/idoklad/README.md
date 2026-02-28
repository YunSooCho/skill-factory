# iDoklad API 클라이언트

iDoklad를 위한 Python API 클라이언트입니다. 체코 회계 시스템 기능을 제공합니다.

## 설치

```bash
pip install requests
```

## API 키 발급 방법

1. [iDoklad Developers](https://developers.idoklad.cz/)에 접속
2. 애플리케이션 등록 (Client ID, Client Secret 획득)
3. OAuth2 인증을 통해 Refresh Token 획득

## 사용법

```python
from idoklad import IdokladClient, IdokladError

client = IdokladClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    refresh_token="YOUR_REFRESH_TOKEN"
)

# 송장 발행 목록 조회
invoices = client.get_issued_invoices()

# 송장 상세 조회
invoice = client.get_issued_invoice("invoice_id")

# 송장 발행
new_invoice = client.create_issued_invoice({
    "DateOfIssuance": "2024-01-01T00:00:00Z",
    "DateOfTaxableSupply": "2024-01-01T00:00:00Z",
    "DateOfMaturity": "2024-01-31T00:00:00Z",
    "PartnerId": 123,
    "Items": [{
        "Name": "Service",
        "Price": 1000,
        "PriceType": 0,
        "Amount": 1,
        "VatRateType": 1
    }]
})

# 거래처 관리
contacts = client.get_contacts()

# 수신 송장 관리
received_invoices = client.get_received_invoices()

# 계좌 내역
bank_accounts = client.get_bank_accounts()
bank_movements = client.get_bank_movements("account_id")

# 송장 이메일 발송
client.send_invoice_by_email("invoice_id", {
    "Email": "client@example.com",
    "Message": "Invoice message"
})
```

## 기능

- 발행 송장(Issued Invoices) CRUD
- 수신 송장(Received Invoices) 관리
- 거래처(Contacts) 관리
- 계좌(Bank Accounts) 및 이동 내역 관리
- 송장 이메일 발송
- 자사 정보 조회

## 라이선스

MIT License
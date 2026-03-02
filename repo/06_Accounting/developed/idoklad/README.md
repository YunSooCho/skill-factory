#iDoklad APIクライアント

iDoklad用のPython APIクライアント。チェコ会計システムの機能を提供します。

## インストール

```bash
pip install requests
```

## API キーの発行方法

1. [iDoklad Developers](https://developers.idoklad.cz/)에 接続
2. アプリケーション登録(Client ID、Client Secret獲得)
3. OAuth2認証でリフレッシュトークンを獲得

##使用法

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

## 機能

- 発行請求書(Issued Invoices) CRUD
- 受信請求書（Received Invoices）管理
- 取引先（Contacts）管理
- 口座(Bank Accounts)と移動履歴管理
- 請求書メール送信
- 自社情報の照会

##ライセンス

MIT License
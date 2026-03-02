#Invoice APIクライアント

Invoice API用のPython APIクライアント。汎用請求書管理機能を提供します。

## インストール

```bash
pip install requests
```

## API キーの発行方法

1. Invoice APIウェブサイトにログイン
2. 設定 > API Keys メニューから API Key を生成
3. API Keyの確認

##使用法

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

## 機能

- 請求書(Invoices) CRUD
- 取引先(Clients)管理
- 製品(Products)管理
- 請求書転送
- 決済（Payments）管理
- 繰り返し請求書(Recurring Invoices)管理

##ライセンス

MIT License
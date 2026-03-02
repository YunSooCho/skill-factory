#Moneyforward Payable APIクライアント

Moneyforward Payable用のPython APIクライアントです。 Payables Management System。

## インストール

```bash
pip install requests
```

## API キーの発行方法

1. Moneyforward Payableウェブサイトにログイン
2. 設定ページまたは開発者ページで API Key を発行
3. API Keyの確認

##使用法

```python
from moneyforward_payable import MoneyforwardPayableClient, MoneyforwardPayableError

client = MoneyforwardPayableClient(api_key="YOUR_API_KEY")

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

## 機能

- 請求書(Invoices) CRUD
- 取引先(Clients)管理
- 製品(Products)管理
- 請求書転送

##ライセンス

MIT License

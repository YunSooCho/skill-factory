#Fatture in Cloud API クライアント

Fatture in Cloud用のPython APIクライアント。イタリアの請求書と支払い管理機能を提供します。

## インストール

```bash
pip install requests
```

## API キーの発行方法

1. [Fatture in Cloud](https://app.fattureincloud.it/)에 ログイン
2. Settings > Developer > App Settingsの移動
3. OAuthアプリの生成またはAPIキーの発行
4. Access Token と Company ID の確認

##使用法

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

## 機能

- 請求書 (Issued Documents) CRUD
- 受信文書(Received Documents)の管理
- 取引先（クライアント）の管理
- 製品(Products)管理
- 請求書Eメールを送信

##ライセンス

MIT License
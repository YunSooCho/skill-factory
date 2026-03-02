#Fakturoid APIクライアント

Fakturoid用のPython APIクライアント。チェコの請求書と支払い管理機能を提供します。

## インストール

```bash
pip install requests
```

## API キーの発行方法

1. [Fakturoid](https://app.fakturoid.cz/)에 ログイン
2. Settings > API Keys メニューに移動
3. API Keyの生成(EmailとAPI Keyが必要)
4. Slug 確認 (アカウント URL で確認可能)

##使用法

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

## 機能

- 請求書CRUD(作成、照会、修正、削除)
- 取引先(Subject)管理
- 請求書テンプレート（Generator）管理
- 請求書の転送と支払い処理
- アカウント情報の照会

##ライセンス

MIT License
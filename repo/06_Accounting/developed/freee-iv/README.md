#Free Invoice APIクライアント

Freee Invoice用のPython APIクライアント。日本の請求書および会計管理機能を提供します。

## インストール

```bash
pip install requests
```

## API キーの発行方法

1. [Freee Developers](https://developers.freee.co.jp/)에 接続
2. アプリケーション登録
3. OAuth2認証でAccess Tokenを取得
4. Company IDの確認

##使用法

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

## 機能

- 請求書/取引(Deals) CRUD
- 取引先(Partners)管理
- アイテム(Items)管理
- ウォレット取引（Wallet Transactions）管理
- 請求書メール送信
- 会社情報の照会

##ライセンス

MIT License
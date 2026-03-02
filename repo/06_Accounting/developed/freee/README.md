#Freee API クライアント

Freee用のPython APIクライアントです。日本総合会計プラットフォーム機能を提供します。

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

## 機能

- 取引(Deals) CRUD
- 取引先(Partners)管理
- ウォレット/資産(Walletables)管理
- ウォレット取引（Wallet Transactions）管理
- 直接経費（Direct Expenses）管理
- 口座移動(Transfers)管理
- 送金テンプレートの管理

##ライセンス

MIT License
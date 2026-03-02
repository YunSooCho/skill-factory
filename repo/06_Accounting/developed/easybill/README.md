#Easybill APIクライアント

Online invoicing and billing platform 用の Python クライアントです。

## 概要

Online invoicing and billing platform.このクライアントは、OAuth認証を介してEasybill APIにアクセスします。

## インストール

\`\`\`bash
pip install requests
\`\`\`

または：

\`\`\`bash
pip install -r requirements.txt
\`\`\`

## OAuthアクセストークン発行

1. そのサービスでアプリを登録する
2. OAuth 2.0フローによるアクセストークンの発行
3. 発行されたトークンを安全に保存

##使用法

### 初期化

\`\`\`python
from easybill import EasybillClient, EasybillError

client = EasybillClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- invoices
- customers
- documents
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_invoices()

#データ生成
result = client.create_invoice(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_invoices()
except EasybillAuthenticationError:
    print("認証失敗")
except EasybillRateLimitError:
    print("速度制限超過")
except EasybillError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

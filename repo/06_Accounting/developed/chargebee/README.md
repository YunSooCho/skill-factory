#Chargebee APIクライアント

Subscription and recurring billing platform 用の Python クライアントです。

## 概要

Subscription and recurring billing platform.このクライアントは、OAuth 認証を介して Chargebee API にアクセスします。

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
from chargebee import ChargebeeClient, ChargebeeError

client = ChargebeeClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- subscribers
- invoices
- subscriptions
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_subscribers()

#データ生成
result = client.create_subscriber(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_subscribers()
except ChargebeeAuthenticationError:
    print("認証失敗")
except ChargebeeRateLimitError:
    print("速度制限超過")
except ChargebeeError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

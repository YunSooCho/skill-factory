# Pingdom APIクライアント

Website monitoring and analytics 用の Python クライアントです。

## 概要

Website monitoring and analytics.このクライアントはOAuth認証を介してPingdom APIにアクセスします。

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
from pingdom import PingdomClient, PingdomError

client = PingdomClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- checks
- results
- analysis
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_checks()

#データ生成
result = client.create_check(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_checks()
except PingdomAuthenticationError:
    print("認証失敗")
except PingdomRateLimitError:
    print("速度制限超過")
except PingdomError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

#ChartMogul APIクライアント

SaaS analytics and metrics platform 用の Python クライアントです。

## 概要

SaaS analytics and metrics platform.このクライアントはOAuth認証を介してChartMogul APIにアクセスします。

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
from chartmogul import ChartmogulClient, ChartmogulError

client = ChartmogulClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- metrics
- customers
- subscriptions
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_metrics()

#データ生成
result = client.create_metric(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_metrics()
except ChartmogulAuthenticationError:
    print("認証失敗")
except ChartmogulRateLimitError:
    print("速度制限超過")
except ChartmogulError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

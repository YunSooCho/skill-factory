#TMetric APIクライアント

Time tracking and productivityのためのPythonクライアント。

## 概要

Time tracking and productivity.このクライアントはOAuth認証を介してTMetric APIにアクセスします。

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
from tmetric import TmetricClient, TmetricError

client = TmetricClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- time_entries
- projects
- tasks
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_time_entries()

#データ生成
result = client.create_time_entrie(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_time_entries()
except TmetricAuthenticationError:
    print("認証失敗")
except TmetricRateLimitError:
    print("速度制限超過")
except TmetricError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

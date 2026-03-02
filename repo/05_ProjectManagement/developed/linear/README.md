#Linear APIクライアント

Project and issue tracking platform 用の Python クライアントです。

## 概要

Project and issue tracking platform.このクライアントはOAuth認証を介してLinear APIにアクセスします。

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
from linear import LinearClient, LinearError

client = LinearClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- issues
- projects
- teams
- cycles
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_issues()

#データ生成
result = client.create_issue(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_issues()
except LinearAuthenticationError:
    print("認証失敗")
except LinearRateLimitError:
    print("速度制限超過")
except LinearError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

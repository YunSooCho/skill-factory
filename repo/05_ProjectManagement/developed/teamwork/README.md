#Teamwork APIクライアント

Project management and collaboration 用の Python クライアントです。

## 概要

Project management and collaboration.このクライアントは、OAuth認証を介してTeamwork APIにアクセスします。

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
from teamwork import TeamworkClient, TeamworkError

client = TeamworkClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- projects
- tasks
- milestones
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_projects()

#データ生成
result = client.create_project(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_projects()
except TeamworkAuthenticationError:
    print("認証失敗")
except TeamworkRateLimitError:
    print("速度制限超過")
except TeamworkError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

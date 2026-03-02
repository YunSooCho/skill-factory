#Jooto APIクライアント

Project management platform (Japanese) 用の Python クライアントです。

## 概要

プロジェクト管理プラットフォーム（日本）。このクライアントはOAuth認証を介してJooto APIにアクセスします。

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
from jooto import JootoClient, JootoError

client = JootoClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- projects
- tasks
- comments
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
except JootoAuthenticationError:
    print("認証失敗")
except JootoRateLimitError:
    print("速度制限超過")
except JootoError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

#Workast APIクライアント

Task and project managementのためのPythonクライアント。

## 概要

タスクとプロジェクト管理。このクライアントはOAuth認証を介してWorkast APIにアクセスします。

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
from workast import WorkastClient, WorkastError

client = WorkastClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- tasks
- lists
- teams
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_tasks()

#データ生成
result = client.create_task(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_tasks()
except WorkastAuthenticationError:
    print("認証失敗")
except WorkastRateLimitError:
    print("速度制限超過")
except WorkastError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

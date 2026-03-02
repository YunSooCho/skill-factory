#Taiga APIクライアント

Agile project management platform用のPythonクライアント。

## 概要

Agile project management platform.このクライアントはOAuth認証を介してTaiga APIにアクセスします。

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
from taiga import TaigaClient, TaigaError

client = TaigaClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- projects
- issues
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
except TaigaAuthenticationError:
    print("認証失敗")
except TaigaRateLimitError:
    print("速度制限超過")
except TaigaError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

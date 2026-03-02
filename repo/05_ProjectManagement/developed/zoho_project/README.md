# Zoho プロジェクト API クライアント

Project management and collaboration 用の Python クライアントです。

## 概要

Project management and collaboration.このクライアントは、OAuth認証を介してZoho Projects APIにアクセスします。

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
from zoho_project import ZohoProjectClient, ZohoProjectError

client = ZohoProjectClient(
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
except ZohoProjectAuthenticationError:
    print("認証失敗")
except ZohoProjectRateLimitError:
    print("速度制限超過")
except ZohoProjectError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

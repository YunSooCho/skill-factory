# Sonderplan APIクライアント

Project planning platform 用の Python クライアントです。

## 概要

プロジェクト計画プラットフォーム。このクライアントは、OAuth 認証を通じて Sonderplan API にアクセスします。

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
from sonderplan import SonderplanClient, SonderplanError

client = SonderplanClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- plans
- tasks
- milestones
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_plans()

#データ生成
result = client.create_plan(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_plans()
except SonderplanAuthenticationError:
    print("認証失敗")
except SonderplanRateLimitError:
    print("速度制限超過")
except SonderplanError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

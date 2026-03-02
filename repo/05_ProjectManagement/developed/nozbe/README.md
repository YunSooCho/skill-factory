#Nozbe APIクライアント

Task and project management platform 用の Python クライアントです。

## 概要

Task and project management platform.このクライアントはOAuth認証を介してNozbe APIにアクセスします。

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
from nozbe import NozbeClient, NozbeError

client = NozbeClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- tasks
- projects
- contexts
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
except NozbeAuthenticationError:
    print("認証失敗")
except NozbeRateLimitError:
    print("速度制限超過")
except NozbeError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

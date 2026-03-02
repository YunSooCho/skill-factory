#Paymo APIクライアント

Project management and time trackingのためのPythonクライアント。

## 概要

Project management and time tracking.このクライアントはOAuth認証を介してPaymo APIにアクセスします。

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
from paymo import PaymoClient, PaymoError

client = PaymoClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- tasks
- projects
- time_entries
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
except PaymoAuthenticationError:
    print("認証失敗")
except PaymoRateLimitError:
    print("速度制限超過")
except PaymoError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

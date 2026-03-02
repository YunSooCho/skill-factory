# Keeping API クライアント

CRM and sales platform用のPythonクライアント。

## 概要

CRM and sales platform.このクライアントはOAuth認証を介してKeeping APIにアクセスします。

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
from keeping import KeepingClient, KeepingError

client = KeepingClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- contacts
- deals
- tasks
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_contacts()

#データ生成
result = client.create_contact(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_contacts()
except KeepingAuthenticationError:
    print("認証失敗")
except KeepingRateLimitError:
    print("速度制限超過")
except KeepingError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

#Zoho Desk APIクライアント

Customer support and help desk用のPythonクライアント。

## 概要

Customer support and help desk.このクライアントは、OAuth認証を介してZoho Desk APIにアクセスします。

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
from zoho_desk import ZohoDeskClient, ZohoDeskError

client = ZohoDeskClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- tickets
- contacts
- tickets
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_tickets()

#データ生成
result = client.create_ticket(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_tickets()
except ZohoDeskAuthenticationError:
    print("認証失敗")
except ZohoDeskRateLimitError:
    print("速度制限超過")
except ZohoDeskError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

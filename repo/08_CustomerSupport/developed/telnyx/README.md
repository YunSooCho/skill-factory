# Telnyx API クライアント

Communication and telecommunications API 用の Python クライアントです。

## 概要

Communication and telecommunications API。このクライアントはOAuth認証を介してTelnyx APIにアクセスします。

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
from telnyx import TelnyxClient, TelnyxError

client = TelnyxClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- messages
- numbers
- calls
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_messages()

#データ生成
result = client.create_message(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_messages()
except TelnyxAuthenticationError:
    print("認証失敗")
except TelnyxRateLimitError:
    print("速度制限超過")
except TelnyxError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

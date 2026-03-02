#SignUpGenius APIクライアント

Online sign up and scheduling platform 用の Python クライアントです。

## 概要

オンラインでのサインアップとスケジュールのプラットフォーム。このクライアントは、OAuth 認証を通じて SignUpGenius API にアクセスします。

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
from signupgenius import SignupgeniusClient, SignupgeniusError

client = SignupgeniusClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- signups
- groups
- users
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_signups()

#データ生成
result = client.create_signup(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_signups()
except SignupgeniusAuthenticationError:
    print("認証失敗")
except SignupgeniusRateLimitError:
    print("速度制限超過")
except SignupgeniusError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

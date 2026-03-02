# Moco API クライアント

Time tracking and project managementのためのPythonクライアント。

## 概要

Time tracking and project management.このクライアントはOAuth認証を介してMoco APIにアクセスします。

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
from moco import MocoClient, MocoError

client = MocoClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- time_entries
- projects
- customers
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_time_entries()

#データ生成
result = client.create_time_entrie(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_time_entries()
except MocoAuthenticationError:
    print("認証失敗")
except MocoRateLimitError:
    print("速度制限超過")
except MocoError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

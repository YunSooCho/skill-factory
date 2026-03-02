# Trello API クライアント

Kanban board project managementのためのPythonクライアント。

## 概要

カンバンボードプロジェクト管理。このクライアントはOAuth認証を介してTrello APIにアクセスします。

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
from trello import TrelloClient, TrelloError

client = TrelloClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- boards
- cards
- lists
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_boards()

#データ生成
result = client.create_board(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_boards()
except TrelloAuthenticationError:
    print("認証失敗")
except TrelloRateLimitError:
    print("速度制限超過")
except TrelloError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

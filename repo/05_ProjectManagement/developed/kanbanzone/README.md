#KanbanZone APIクライアント

Kanban project management platformのためのPythonクライアント。

## 概要

カンバンプロジェクト管理プラットフォーム。このクライアントは、OAuth 認証を通じて KanbanZone API にアクセスします。

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
from kanbanzone import KanbanzoneClient, KanbanzoneError

client = KanbanzoneClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- boards
- cards
- zones
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
except KanbanzoneAuthenticationError:
    print("認証失敗")
except KanbanzoneRateLimitError:
    print("速度制限超過")
except KanbanzoneError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

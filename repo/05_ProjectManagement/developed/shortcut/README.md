# Shortcut APIクライアント

Project management platform 用の Python クライアントです。

## 概要

プロジェクト管理プラットフォーム。このクライアントはOAuth認証を介してShortcut APIにアクセスします。

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
from shortcut import ShortcutClient, ShortcutError

client = ShortcutClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- stories
- epics
- projects
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_stories()

#データ生成
result = client.create_storie(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_stories()
except ShortcutAuthenticationError:
    print("認証失敗")
except ShortcutRateLimitError:
    print("速度制限超過")
except ShortcutError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

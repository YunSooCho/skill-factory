#Bakuraku Kyotsukanri APIクライアント

Shared management platform用のPythonクライアント。

## 概要

Shared management platform.このクライアントは、OAuth認証を通じてBakuraku Kyotsukanri APIにアクセスします。

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
from bakuraku_kyotsukanri import BakurakuKyotsukanriClient, BakurakuKyotsukanriError

client = BakurakuKyotsukanriClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- shared_items
- permissions
- groups
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_shared_items()

#データ生成
result = client.create_shared_item(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_shared_items()
except BakurakuKyotsukanriAuthenticationError:
    print("認証失敗")
except BakurakuKyotsukanriRateLimitError:
    print("速度制限超過")
except BakurakuKyotsukanriError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

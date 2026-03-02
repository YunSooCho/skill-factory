#Resource Guru APIクライアント

Resource scheduling and planning 用の Python クライアントです。

## 概要

Resource scheduling and planning.このクライアントは、OAuth認証を介してResource Guru APIにアクセスします。

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
from resource_guru import ResourceGuruClient, ResourceGuruError

client = ResourceGuruClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- resources
- bookings
- leaves
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_resources()

#データ生成
result = client.create_resource(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_resources()
except ResourceGuruAuthenticationError:
    print("認証失敗")
except ResourceGuruRateLimitError:
    print("速度制限超過")
except ResourceGuruError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

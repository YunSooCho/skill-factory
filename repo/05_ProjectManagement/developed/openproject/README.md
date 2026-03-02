#OpenProject APIクライアント

Open source project managementのためのPythonクライアント。

## 概要

オープンソースプロジェクト管理。このクライアントはOAuth認証を介してOpenProject APIにアクセスします。

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
from openproject import OpenprojectClient, OpenprojectError

client = OpenprojectClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- work_packages
- projects
- users
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_work_packages()

#データ生成
result = client.create_work_package(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_work_packages()
except OpenprojectAuthenticationError:
    print("認証失敗")
except OpenprojectRateLimitError:
    print("速度制限超過")
except OpenprojectError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

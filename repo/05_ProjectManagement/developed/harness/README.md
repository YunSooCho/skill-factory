#Harness APIクライアント

Software delivery and DevOps platform用のPythonクライアント。

## 概要

Software delivery and DevOps platform.このクライアントはOAuth認証を介してHarness APIにアクセスします。

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
from harness import HarnessClient, HarnessError

client = HarnessClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- pipelines
- deployments
- services
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_pipelines()

#データ生成
result = client.create_pipeline(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_pipelines()
except HarnessAuthenticationError:
    print("認証失敗")
except HarnessRateLimitError:
    print("速度制限超過")
except HarnessError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

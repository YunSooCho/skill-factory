#DX Suite API クライアント

Digital transformation platform用のPythonクライアントです。

## 概要

デジタル変換プラットフォーム。このクライアントは、OAuth認証を介してDX Suite APIにアクセスします。

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
from dx_suite import DxSuiteClient, DxSuiteError

client = DxSuiteClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- workflows
- documents
- tasks
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_workflows()

#データ生成
result = client.create_workflow(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_workflows()
except DxSuiteAuthenticationError:
    print("認証失敗")
except DxSuiteRateLimitError:
    print("速度制限超過")
except DxSuiteError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

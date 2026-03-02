#Just SFA API クライアント

Sales Force Automation platform用のPythonクライアント。

## 概要

Sales Force Automation platform.このクライアントはOAuth認証を介してJust SFA APIにアクセスします。

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
from just_sfa import JustSfaClient, JustSfaError

client = JustSfaClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- leads
- deals
- activities
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_leads()

#データ生成
result = client.create_lead(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_leads()
except JustSfaAuthenticationError:
    print("認証失敗")
except JustSfaRateLimitError:
    print("速度制限超過")
except JustSfaError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

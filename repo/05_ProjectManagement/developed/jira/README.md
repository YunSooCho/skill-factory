#Jira APIクライアント

Issue and project tracking platformのためのPythonクライアント。

## 概要

Issue and project tracking platform.このクライアントは、OAuth認証を介してJira APIにアクセスします。

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
from jira import JiraClient, JiraError

client = JiraClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- issues
- projects
- users
- sprints
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_issues()

#データ生成
result = client.create_issue(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_issues()
except JiraAuthenticationError:
    print("認証失敗")
except JiraRateLimitError:
    print("速度制限超過")
except JiraError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

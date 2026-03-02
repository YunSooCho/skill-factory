# Bakuraku Shinsei Keihiseisan API クライアント

Application and trip fee calculationのためのPythonクライアント。

## 概要

Application and trip fee calculation.このクライアントは、OAuth認証を通じてBakuraku Shinsei Keihiseisan APIにアクセスします。

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
from bakuraku_shinsei_keihiseisan import BakurakuShinseiKeihiseisanClient, BakurakuShinseiKeihiseisanError

client = BakurakuShinseiKeihiseisanClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

###主な機能

\`\`\`python
- applications
- calculations
- fees
\`\`\`

### 例

\`\`\`python
#データ検索
result = client.get_applications()

#データ生成
result = client.create_application(
    name="Example Name"
)
\`\`\`

## エラー処理

\`\`\`python
try:
    result = client.get_applications()
except BakurakuShinseiKeihiseisanAuthenticationError:
    print("認証失敗")
except BakurakuShinseiKeihiseisanRateLimitError:
    print("速度制限超過")
except BakurakuShinseiKeihiseisanError as e:
    print(f"リクエストに失敗しました: {str(e)}")
\`\`\`

##ライセンス

MIT License

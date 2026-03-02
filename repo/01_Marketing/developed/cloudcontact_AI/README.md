#CloudContact AI API クライアント

CloudContact AI用のPythonクライアントです。 AIベースの顧客センター管理機能を提供します。

## 概要

CloudContact AIはAIベースのカスタマーセンタープラットフォームです。このクライアントは、OAuth認証を介してCloudContact AI APIにアクセスします。

## インストール

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## OAuthアクセストークン発行

1. そのサービスでアプリを登録する
2. OAuth 2.0フローによるアクセストークンの発行
3. 発行されたトークンを安全に保存

##使用法

### 初期化

```python
from cloudcontact_AI import CloudContactAIClient, CloudcontactAIError

client = CloudContactAIClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
```

###主な機能

- contacts
- calls
- chats

### 例

```python
# 연락처 조회
contacts = client.get_contacts()

# 연락처 생성
contact = client.create_contact(name="John Doe", email="john@example.com")

# 통화 기록 조회
calls = client.get_calls()

# 채팅 기록 조회
chats = client.get_chats()
```

## エラー処理

```python
try:
    contacts = client.get_contacts()
except CloudcontactAIAuthenticationError:
    print("인증 실패")
except CloudcontactAIRateLimitError:
    print("속도 제한 초과")
except CloudcontactAIError as e:
    print(f"요청 실패: {str(e)}")
```

##ライセンス

MIT License
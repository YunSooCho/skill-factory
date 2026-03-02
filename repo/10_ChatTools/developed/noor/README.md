#Noor APIクライアント

Noor API用のPython APIクライアント。

## 概要

このクライアントはNoor APIにアクセスし、メンバーリストの検索とメッセージの公開機能を提供します。

## インストール

依存パッケージ：

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## API キー発行

1. Noor開発者ポータルへのアクセス
2. アプリの生成とAPIキーの発行
3. 発行された API キーの保存

##使用法

### 初期化

```python
from noor import NoorClient

client = NoorClient(
    api_key="YOUR_API_KEY"
)
```

### サンプルコード

```python
# 전체 멤버 목록 조회
members = client.get_members(limit=20)
print(members)

# 특정 그룹의 멤버 조회
group_members = client.get_members(group_id="group123", limit=10)
print(group_members)

# 간단한 메시지 게시
result = client.post_message(
    chat_id="chat123",
    text="Hello from Noor API!"
)
print(result)

# 멘션이 포함된 메시지 게시
result = client.post_message(
    chat_id="chat123",
    text="Hello @user1 and @user2!",
    mention_user_ids=["user1", "user2"]
)

# 리플라이 메시지 게시
result = client.post_message(
    chat_id="chat123",
    text="This is a reply",
    reply_to_message_id="msg456"
)
```

## APIアクション

- `get_members` - Get Members
- `post_message` - Post Message

## アクションパラメータ

### get_members
- `group_id`(string, optional) - グループID(フィルタリング用)
- `limit` (integer, optional) - 返す結果の数 (デフォルト: 50)
- `offset`（integer、optional） - ページネーションオフセット（デフォルト：0）

### post_message
- `chat_id`(string, required) - チャットID
- `text`(string, required) - 投稿するメッセージの内容
- `mention_user_ids`（array of strings、optional） - メンションするユーザーIDのリスト
- `reply_to_message_id`(string, optional) - リプライするメッセージID

## エラー処理

```python
try:
    result = client.post_message("chat123", "Hello!")
except ValueError as e:
    print("Validation error:", str(e))
except Exception as e:
    print("Error:", str(e))
```

## Rate Limiting

API リクエストのレートリミットが適用される場合があります。

##ライセンス

MIT License
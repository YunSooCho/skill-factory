#Talknote APIクライアント

Talknote用のPython APIクライアント。

## 概要

このクライアントは、Talknote API にアクセスしてスレッドとメモにメッセージを投稿する機能を提供します。

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

1. Talknote開発者ポータルへのアクセス
2. アプリの生成とAPIキーの発行
3. 発行された API キーの保存

##使用法

### 初期化

```python
from talknote import TalknoteClient

client = TalknoteClient(
    api_key="YOUR_API_KEY"
)
```

### サンプルコード

```python
# 스레드에 메시지 게시
result = client.post_message_to_thread(
    thread_id="thread123",
    message="This is a message to the thread."
)
print(result)

# 멘션이 포함된 스레드 메시지 게시
result = client.post_message_to_thread(
    thread_id="thread123",
    message="@user1 Please check this.",
    mention_user_ids=["user1", "user2"]
)

# 노트에 메시지 게시
result = client.post_message_to_note(
    note_id="note456",
    message="This is a message to the note."
)
print(result)

# 멘션이 포함된 노트 메시지 게시
result = client.post_message_to_note(
    note_id="note456",
    message="@team Important update!",
    mention_user_ids=["user1", "user2", "user3"]
)
```

## APIアクション

- `post_message_to_thread` - スレッドにメッセージを投稿
- `post_message_to_note` - ノートへメッセージを投稿

## アクションパラメータ

### post_message_to_thread
- `thread_id`(string, required) - スレッドID
- `message` (string, required) - 投稿するメッセージの内容
- `mention_user_ids`（array of strings、optional） - メンションするユーザーIDのリスト

### post_message_to_note
- `note_id`(string, required) - ノートID
- `message` (string, required) - 投稿するメッセージの内容
- `mention_user_ids`（array of strings、optional） - メンションするユーザーIDのリスト

## エラー処理

```python
try:
    result = client.post_message_to_thread("thread123", "Hello!")
except ValueError as e:
    print("Validation error:", str(e))
except Exception as e:
    print("Error:", str(e))
```

## Rate Limiting

API リクエストのレートリミットが適用される場合があります。

##ライセンス

MIT License
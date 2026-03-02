#MEGA APIクライアント

MEGA API用のPython APIクライアント。

## 概要

このクライアントはMEGA APIにアクセスし、テキストメッセージの送信と削除を提供します。

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

1. MEGA開発者ポータルへのアクセス
2. アプリの生成とAPIキーの発行
3. 発行された API キーの保存

##使用法

### 初期化

```python
from megaapi import MegaapiClient

client = MegaapiClient(
    api_key="YOUR_API_KEY"
)
```

### サンプルコード

```python
# 텍스트 메시지 전송
result = client.send_text_message(
    chat_id="chat123",
    text="Hello from MEGA API!"
)
print(result)

# 리플라이 메시지 전송
result = client.send_text_message(
    chat_id="chat123",
    text="This is a reply",
    reply_to_message_id="msg456"
)

# 메시지 삭제 (발신자만)
result = client.delete_message(
    chat_id="chat123",
    message_id="msg456",
    for_all_users=False
)

# 메시지 삭제 (모든 사용자)
result = client.delete_message(
    chat_id="chat123",
    message_id="msg789",
    for_all_users=True
)
```

## APIアクション

- `send_text_message` - Send Text Message
- `delete_message` - Delete Message

## アクションパラメータ

### send_text_message
- `chat_id`(string, required) - チャットIDまたはユーザーID
- `text`(string, required) - 送信するメッセージの内容
- `reply_to_message_id`(string, optional) - リプライするメッセージID

### delete_message
- `chat_id`(string, required) - チャットID
- `message_id`(string, required) - 削除するメッセージID
- `for_all_users`（boolean、optional） - すべてのユーザーに対して削除するかどうか（デフォルト：false）

## エラー処理

```python
try:
    result = client.send_text_message("chat123", "Hello!")
except ValueError as e:
    print("Validation error:", str(e))
except Exception as e:
    print("Error:", str(e))
```

## Rate Limiting

API リクエストのレートリミットが適用される場合があります。

##ライセンス

MIT License
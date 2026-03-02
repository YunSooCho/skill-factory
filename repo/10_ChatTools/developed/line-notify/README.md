# Line Notify APIクライアント

Line Notify用のPython APIクライアント。

## 概要

このクライアントは、Line Notify APIにアクセスし、トークルームに通知メッセージと画像を送信する機能を提供します。

## インストール

依存パッケージ：

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## APIトークン発行

1. LINE Notifyウェブサイトへのアクセス: https://notify-bot.line.me
2. ログイン後「ログイン」ボタンをクリック
3. 「トークンを発行する」（トークン発行）をクリック
4. トークン名の入力後に発行
5. 発行されたトークンの保存

またはLINE Notify公式開発者ドキュメントを参照してください。
https://notify-bot.line.me/doc/en/

##使用法

### 初期化

```python
from line_notify import LineNotifyClient

client = LineNotifyClient(
    access_token="YOUR_ACCESS_TOKEN"
)
```

### サンプルコード

```python
# 텍스트 메시지 전송
result = client.send_message("Hello from Line Notify!")
print(result)

# 스티커와 함께 메시지 전송
result = client.send_message(
    "Hello with sticker!",
    sticker_package_id=1,
    sticker_id=1
)

# 이미지 URL과 함께 메시지 전송
result = client.send_message_with_image(
    "Hello with image!",
    image_url="https://example.com/image.jpg"
)

# 로컬 이미지 파일과 함께 메시지 전송
result = client.send_message_with_image(
    "Hello with local image!",
    image_path="/path/to/image.jpg"
)

# 상태 확인
status = client.get_status()
print(status)
```

## APIアクション

- `send_message` - トークルームにメッセージを送信する
- `send_message_with_image` - トークルームへのメッセージと画像の転送
- `get_status` - 接続状態の確認

## エラー処理

```python
try:
    result = client.send_message("Hello!")
except ValueError as e:
    print("Validation error:", str(e))
except Exception as e:
    print("Error:", str(e))
```

## Rate Limiting

Line Notifyはリクエストのレートリミットが適用されます。過剰な要求は429エラーを返します。

##ステッカー情報

公式ステッカーリストは、次のURLで確認できます。
https://devdocs.line.me/files/sticker_list.pdf

## 注意事項

- メッセージは最大1000文字まで可能です
- 画像はJPEGまたはPNG形式のみをサポートします
- 画像サイズは最大10MBです

##ライセンス

MIT License
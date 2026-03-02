# Telegram Bot API クライアント

Telegram Bot API用のPython APIクライアント。

## 概要

このクライアントはTelegram Bot APIにアクセスし、メッセージの送信、更新の受信、Webフックの設定など、さまざまなタスクをサポートします。

## インストール

依存パッケージ：

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## Bot Tokenの発行

1. Telegramで@BotFatherボットを検索する
2. `/newbot` コマンド入力
3. ボット名の作成
4. ボットユーザー名の作成（@で始まる必要があります）
5. 発行されたBot Tokenの貯蔵

APIドキュメント：
https://core.telegram.org/bots/api

##使用法

### 初期化

```python
from telegram import TelegramClient

client = TelegramClient(
    bot_token="YOUR_BOT_TOKEN"
)
```

### サンプルコード

```python
# 간단한 메시지 전송
result = client.send_message(
    chat_id="channel_name_or_chat_id",
    text="Hello from Telegram Bot API!"
)
print(result)

# Markdown 파싱으로 메시지 전송
result = client.send_message(
    chat_id="channel_name_or_chat_id",
    text="*Bold text* and _italic text_",
    parse_mode="Markdown"
)

# HTML 파싱으로 메시지 전송
result = client.send_message(
    chat_id="channel_name_or_chat_id",
    text="<b>Bold text</b> and <i>italic text</i>",
    parse_mode="HTML"
)

# 리플라이 메시지 전송
result = client.send_message(
    chat_id="channel_name_or_chat_id",
    text="This is a reply!",
    reply_to_message_id="123"
)

# 웹 페이지 미리보기 비활성화
result = client.send_message(
    chat_id="channel_name_or_chat_id",
    text="Check this link: https://example.com",
    disable_web_page_preview=True
)

# 알림 없이 메시지 전송 (silent)
result = client.send_message(
    chat_id="channel_name_or_chat_id",
    text="Silent message",
    disable_notification=True
)

# 봇 정보 조회
bot_info = client.get_me()
print(f"Bot: {bot_info.get('first_name')} (@{bot_info.get('username')})")

# 업데이트 수신 (long polling)
updates = client.get_updates(timeout=30)
print(f"Updates: {updates}")

# Webhook 설정
result = client.set_webhook("https://your-webhook-url.com")

# Webhook 정보 조회
webhook_info = client.get_webhook_info()
print(f"Webhook: {webhook_info.get('url')}")

# Webhook 삭제
result = client.delete_webhook()
```

## APIアクション

- `send_message` - メッセージを送信
- `get_me` - ボット情報の照会
- `get_updates` - 更新を受け取る（long polling）
- `set_webhook` - Webhook設定
- `delete_webhook` - Webhookを削除
- `get_webhook_info` - Webhook情報の照会

## アクションパラメータ

### send_message
- `chat_id`(string, required) - ターゲットチャットID(username@または数値ID)
- `text`(string, required) - 送信するメッセージの内容
- `parse_mode`(string, optional) - テキスト解析モード(Markdown、MarkdownV2、HTML)
- `disable_web_page_preview`(boolean, optional) - リンクプレビューを無効にする
- `disable_notification` (boolean, optional) - 通知なしで送信
- `reply_to_message_id`(string, optional) - リプライするメッセージID

## Parse Modeオプション

1. **Markdown**: デフォルトの Markdown 形式
   - `*bold*` - 太字
   - `_italic_` - 傾斜
   - `[text](url)` - リンク

2. **MarkdownV2**: 拡張 Markdown 形式
   - `*bold \*text\**` - 太字
   - `_italic \*text\__` - 傾く
   - `[text](url)` - リンク

3. **HTML**: HTML形式
   - `<b>text</b>` - 太字
   - `<i>text</i>` - 傾斜
   - `<a href="url">text</a>` - リンク

## エラー処理

```python
try:
    result = client.send_message("chat_id", "Hello!")
except ValueError as e:
    print("Validation error:", str(e))
except Exception as e:
    print("Error:", str(e))
```

## Webhook vs Long Polling

### Webhook (推奨)
- プッシュ方式でリアルタイムアップデートを受信
- HTTPS Webサーバーが必要
- `set_webhook()` に設定

### Long Polling
- ポーリング方式でアップデートを受信
- 別途ウェブサーバー不要
- `get_updates()`で受信

## Rate Limiting

Telegram APIにはレートリミットが適用されます。
- グループチャット：毎秒20メッセージ
- プライベートチャット：毎秒30メッセージ
- グループあたり1秒あたり1メッセージ

## 参考資料

- Telegram Bot API: https://core.telegram.org/bots/api
- @BotFather: TelegramでBotFatherボットと会話

##ライセンス

MIT License
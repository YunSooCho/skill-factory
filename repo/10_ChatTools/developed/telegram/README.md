# Telegram Bot API 클라이언트

Telegram Bot API를 위한 Python API 클라이언트입니다.

## 개요

이 클라이언트는 Telegram Bot API에 접근하여 메시지 전송, 업데이트 수신, 웹훅 설정 등 다양한 작업을 지원합니다.

## 설치

의존성 패키지:

```bash
pip install requests
```

또는:

```bash
pip install -r requirements.txt
```

## Bot Token 발급

1. Telegram에서 @BotFather 봇 검색
2. `/newbot` 명령어 입력
3. 봇 이름 작성
4. 봇 사용자 이름 작성 (@로 시작해야 함)
5. 발급된 Bot Token 저장

API 문서:
https://core.telegram.org/bots/api

## 사용법

### 초기화

```python
from telegram import TelegramClient

client = TelegramClient(
    bot_token="YOUR_BOT_TOKEN"
)
```

### 예시 코드

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

## API 액션

- `send_message` - メッセージを送信
- `get_me` - 봇 정보 조회
- `get_updates` - 업데이트 수신 (long polling)
- `set_webhook` - Webhook 설정
- `delete_webhook` - Webhook 삭제
- `get_webhook_info` - Webhook 정보 조회

## 액션 파라미터

### send_message
- `chat_id` (string, required) - 대상 채팅 ID (username@ 또는 숫자 ID)
- `text` (string, required) - 전송할 메시지 내용
- `parse_mode` (string, optional) - 텍스트 파싱 모드 (Markdown, MarkdownV2, HTML)
- `disable_web_page_preview` (boolean, optional) - 링크 미리보기 비활성화
- `disable_notification` (boolean, optional) - 알림 없이 전송
- `reply_to_message_id` (string, optional) - 리플라이할 메시지 ID

## Parse Mode 옵션

1. **Markdown**: 기본 Markdown 형식
   - `*bold*` - 굵게
   - `_italic_` - 기울임
   - `[text](url)` - 링크

2. **MarkdownV2**: 향상된 Markdown 형식
   - `*bold \*text\**` - 굵게
   - `_italic \*text\__` - 기울임
   - `[text](url)` - 링크

3. **HTML**: HTML 형식
   - `<b>text</b>` - 굵게
   - `<i>text</i>` - 기울임
   - `<a href="url">text</a>` - 링크

## 에러 처리

```python
try:
    result = client.send_message("chat_id", "Hello!")
except ValueError as e:
    print("Validation error:", str(e))
except Exception as e:
    print("Error:", str(e))
```

## Webhook vs Long Polling

### Webhook (권장)
- 푸시 방식으로 실시간 업데이트 수신
- HTTPS 웹서버 필요
- `set_webhook()`으로 설정

### Long Polling
- 폴링 방식으로 업데이트 수신
- 별도의 웹서버 불필요
- `get_updates()`로 수신

## Rate Limiting

Telegram API는 레이트 리밋이 적용됩니다:
- 그룹 채팅: 초당 20개 메시지
- 개인 채팅: 초당 30개 메시지
- 그룹당 초당 1개 메시지

## 참고 문서

- Telegram Bot API: https://core.telegram.org/bots/api
- @BotFather: Telegram에서 BotFather 봇과 대화

## 라이선스

MIT License
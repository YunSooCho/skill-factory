# Pinterest API 클라이언트

Pinterest API v5를 위한 Python 클라이언트입니다.

## 개요

이 클라이언트는 OAuth 2.0 인증을 사용하여 Pinterest API에 접근하고, Pin/Board 관리 및 Webhook 처리를 지원합니다.

## 설치

의존성 패키지:

```bash
pip install requests
```

또는:

```bash
pip install -r requirements.txt
```

## API 키 발급

1. [Pinterest Apps](https://developers.pinterest.com/apps/)에서 새 앱 생성
2. 앱 설정에서 App ID 및 App Secret 확인
3. OAuth 인증 수행하여 Access Token 발급
   - OAuth 2.0 Authorization Code Flow 또는 Implicit Flow 사용
4. 발급된 Access Token 저장

## 사용법

### 초기화

```python
from pinterest.pinterest_client import PinterestClient

client = PinterestClient(
    access_token="YOUR_ACCESS_TOKEN",
    app_id="YOUR_APP_ID",  # 필요시
    app_secret="YOUR_APP_SECRET",  # 필요시
    timeout=30
)
```

### 예시 코드

#### Pin 생성

```python
# 새 Pin 생성
pin = client.create_pin(
    board_id="BOARD_ID",
    title="My Amazing Pin",
    description="This is a description for my pin",
    link="https://example.com",
    media_source={
        "source_type": "image_url",
        "url": "https://example.com/image.jpg"
    }
)
print("Pin created:", pin['id'])
```

#### Pin 조회

```python
# 특정 Pin 조회
pin_info = client.get_pin("PIN_ID")
print(pin_info)

# 리스트 조회
pins = client.list_pins(board_id="BOARD_ID", page_size=25)
for pin in pins['items']:
    print(pin['id'], pin['title'])
```

#### Board 생성 및 관리

```python
# 새 Board 생성
board = client.create_board(
    name="My Favorite Pins",
    description="Collection of my favorite pins",
    privacy="PUBLIC"
)
print("Board created:", board['id'])

# 정보 업데이트
updated_board = client.update_board(
    board_id="BOARD_ID",
    name="Updated Board Name"
)
print(updated_board)

# Board 목록
boards = client.list_boards()
for board in boards['items']:
    print(board['id'], board['name'])
```

#### Webhook 처리

```python
# Webhook 이벤트 처리
import json
from flask import Flask, request

app = Flask(__name__)
webhook_secret = "YOUR_WEBHOOK_SECRET"

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    payload = request.json
    signature = request.headers.get('X-Pinterest-Signature')

    # 서명 검증 및 이벤트 처리
    event = client.handle_webhook_event(
        payload=payload,
        signature=signature,
        webhook_secret=webhook_secret
    )

    print("Event type:", event['event_type'])
    print("Event data:", event['data'])

    return {"status": "received"}
```

## API 액션

### Pin
- `get_pin(pin_id)` - 특정 Pin 정보 조회
- `create_pin(board_id, ..., media_source)` - 새로운 Pin 생성
- `list_pins(board_id=None, ...)` - Pin 목록 조회

### Board
- `get_board(board_id)` - 특정 보드 정보 조회
- `create_board(name, ...)` - 새로운 보드 생성
- `update_board(board_id, ...)` - 보드 정보 업데이트
- `list_boards(...)` - 보드 목록 조회

### Webhook
- `verify_webhook_signature(payload, signature, secret)` - Webhook 서명 검증
- `handle_webhook_event(payload, ...)` - Webhook 이벤트 처리

## 트리거

이 서비스는 다음 Webhook 트리거를 지원합니다:

- **New Pin Created** - 새로운 Pin 생성 시

Webhook 설정은 Pinterest Apps 페이지에서 수행하십시오.

## 에러 처리

```python
from pinterest.pinterest_client import PinterestAPIError, PinterestRateLimitError

try:
    pin = client.get_pin("PIN_ID")
except PinterestRateLimitError as e:
    print(f"Rate limit exceeded: {e}")
    # 재시도 로직 추가
except PinterestAPIError as e:
    print(f"API error: {e}")
```

## Rate Limiting

클라이언트는 API 요청 간 최소 0.1초 지연을 적용합니다. 너무 많은 요청이 발생하면 `PinterestRateLimitError`가 발생합니다.

## 라이선스

MIT License
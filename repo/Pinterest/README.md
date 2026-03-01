# Pinterest API Client

Pinterest API 클라이언트입니다.

## 설치

```bash
pip install requests
```

## API 키 발급

1. Pinterest API 앱 등록: https://developers.pinterest.com/apps/

2. 앱 생성 후 OAuth 2.0 클라이언트 ID 및 시크릿 확인

3. Access 토큰 발급:
   - OAuth 2.0 인증 또는
   - 앱 설정에서 토큰 생성

## 사용 예시

```python
from client import PinterestClient

# 클라이언트 초기화
client = PinterestClient(access_token="your_access_token")

# Pin 생성
pin = client.create_pin(
    title="My Pin",
    description="Amazing pin",
    link="https://example.com",
    board_id="board_id",
    image_url="https://example.com/image.jpg"
)

# 보드 생성
board = client.create_board(
    name="My Board",
    description="My awesome board"
)

# Pin 목록 조회
pins = client.list_pins(board_id="board_id")

# 보드 목록 조회
boards = client.list_boards()
```

## API 메서드

- `get_pin(pin_id)` - Pin 세부 정보 조회
- `create_pin(...)` - Pin 생성
- `get_board(board_id)` - 보드 세부 정보 조회
- `create_board(...)` - 보드 생성
- `list_pins(...)` - Pin 목록 조회
- `update_board(...)` - 보드 업데이트
- `list_boards(...)` - 보드 목록 조회
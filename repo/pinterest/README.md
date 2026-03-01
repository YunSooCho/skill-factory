# Pinterest API 클라이언트

Pinterest API를 위한 Python 클라이언트입니다. 핀, 보드 및 사용자 콘텐츠 관리 기능을 제공합니다.

## 개요

Pinterest는 시각적 발견 및 소셜 북마크 플랫폼입니다. 이 클라이언트는 OAuth 인증을 통해 Pinterest API에 접근합니다.

## 설치

```bash
pip install requests
```

또는:

```bash
pip install -r requirements.txt
```

## OAuth 액세스 토큰 발급

1. [Pinterest Developers](https://developers.pinterest.com/)에서 앱 등록
2. OAuth 2.0 흐름을 통해 액세스 토큰 발급
3. 발급된 토큰을 안전하게 저장

## 사용법

### 초기화

```python
from pinterest import PinterestClient, PinterestError

client = PinterestClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
```

### 사용자 정보

```python
user = client.get_user_account()
```

### 보드 관리

```python
# 보드 목록
boards = client.get_boards()

# 특정 보드 조회
board = client.get_board("board_id")

# 보드 생성
board = client.create_board(
    name="My Board",
    description="My favorite pins"
)

# 보드 업데이트
board = client.update_board("board_id", description="Updated description")

# 보드 삭제
client.delete_board("board_id")
```

### 핀 관리

```python
# 모든 핀
pins = client.get_pins()

# 특정 보드의 핀
pins = client.get_pins(board_id="board_id")

# 핀 상세 조회
pin = client.get_pin("pin_id")

# 핀 생성
pin = client.create_pin(
    board_id="board_id",
    title="My Pin",
    description="Pin description",
    source_url="https://example.com",
    media_source={
        "source_type": "image_url",
        "url": "https://example.com/image.jpg"
    }
)

# 핀 업데이트
pin = client.update_pin("pin_id", title="Updated Title")

# 핀 삭제
client.delete_pin("pin_id")
```

## 에러 처리

```python
try:
    board = client.create_board(name="New Board")
except PinterestAuthenticationError:
    print("인증 실패")
except PinterestRateLimitError:
    print("속도 제한 초과")
except PinterestError as e:
    print(f"요청 실패: {str(e)}")
```

## 라이선스

MIT License

## 지원

- [Pinterest Developers](https://developers.pinterest.com/)
- [API 문서](https://developers.pinterest.com/docs/api/v5/)
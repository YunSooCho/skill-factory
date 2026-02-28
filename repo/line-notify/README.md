# Line Notify API 클라이언트

Line Notify를 위한 Python API 클라이언트입니다.

## 개요

이 클라이언트는 Line Notify API에 접근하여 토크룸으로 알림 메시지와 이미지를 전송하는 기능을 제공합니다.

## 설치

의존성 패키지:

```bash
pip install requests
```

또는:

```bash
pip install -r requirements.txt
```

## API 토큰 발급

1. LINE Notify 웹사이트 접속: https://notify-bot.line.me
2. 로그인 후 "로그인" 버튼 클릭
3. "トークンを発行する" (토큰 발행) 클릭
4. 토큰 이름 입력 후 발행
5. 발행된 토큰 저장

또는 LINE Notify 공식 개발자 문서 참조:
https://notify-bot.line.me/doc/en/

## 사용법

### 초기화

```python
from line_notify import LineNotifyClient

client = LineNotifyClient(
    access_token="YOUR_ACCESS_TOKEN"
)
```

### 예시 코드

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

## API 액션

- `send_message` - 토크룸에 메시지 전송
- `send_message_with_image` - 토크룸에 메시지와 이미지 전송
- `get_status` - 연결 상태 확인

## 에러 처리

```python
try:
    result = client.send_message("Hello!")
except ValueError as e:
    print("Validation error:", str(e))
except Exception as e:
    print("Error:", str(e))
```

## Rate Limiting

Line Notify는 요청에 대한 레이트 리밋이 적용됩니다. 과도한 요청은 429 에러를 반환합니다.

## 스티커 정보

공식 스티커 리스트는 다음 URL에서 확인 가능:
https://devdocs.line.me/files/sticker_list.pdf

## 주의사항

- 메시지는 최대 1000자까지 가능합니다
- 이미지는 JPEG 또는 PNG 형식만 지원합니다
- 이미지 크기는 최대 10MB 입니다

## 라이선스

MIT License
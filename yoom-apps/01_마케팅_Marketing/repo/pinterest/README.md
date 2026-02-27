# Pinterest API Integration for Yoom

Pinterest API v5 클라이언트 - Yoom 연동용

## 설치

```bash
pip install requests
```

## 설정

```python
fromPinterest import PinterestClient

client = PinterestClient(
    access_token='your_access_token',
    app_id='your_app_id'
)
```

## API 액션

### Get Pin
```python
pin = client.get_pin('pin_id')
```

### Create Pin
```python
from Pinterest import PinCreateRequest

request = PinCreateRequest(
    board_id='board_id',
    source_url='https://example.com/image.jpg',
    media_source={
        'source_type': 'image_url',
        'url': 'https://example.com/image.jpg'
    },
    title='My Pin',
    description='Pin description'
)
pin = client.create_pin(request)
```

### Get Board
```python
board = client.get_board('board_id')
```

### Create Board
```python
from Pinterest import BoardCreateRequest

request = BoardCreateRequest(
    name='My Board',
    description='My board description',
    privacy='public'  # or 'secret'
)
board = client.create_board(request)
```

### List Pins
```python
result = client.list_pins(board_id='board_id', page_size=25)
pins = result['items']
next_cursor = result['cursor']
```

### List Boards
```python
result = client.list_boards(page_size=25)
boards = result['items']
next_cursor = result['cursor']
```

### Update Board
```python
board = client.update_board(
    'board_id',
    name='New Name',
    description='New Description',
    privacy='public'
)
```

## 트리거

### New Pin
새 핀이 생성될 때 웹훅을 통해 트리거됨 (웹훅 설정 필요)

## API 문서

- Pinterest API: https://developers.pinterest.com/docs/api/v5/
- OAuth 인증: https://developers.pinterest.com/docs/getting-started/authentication/

## 라이선스

MIT License
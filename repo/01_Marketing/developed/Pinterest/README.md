# Pinterest API Client

Pinterest API クライアントです。

## インストール

```bash
pip install requests
```

## API キー発行

1. Pinterest API アプリ登録: https://developers.pinterest.com/apps/

2. アプリ作成後のOAuth 2.0クライアントIDとシークレットの確認

3. Accessトークン発行：
   - OAuth 2.0認証または
   - アプリ設定でトークンを生成

## 使用例

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

## APIメソッド

- `get_pin(pin_id)` - Pin 詳細の照会
- `create_pin(...)` - Pin 生成
- `get_board(board_id)` - ボード詳細の照会
- `create_board(...)` - ボードの作成
- `list_pins(...)` - Pin リスト照会
- `update_board(...)` - ボードアップデート
- `list_boards(...)` - ボードリストの照会
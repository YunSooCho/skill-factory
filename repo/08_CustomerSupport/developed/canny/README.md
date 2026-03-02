# Canny SDK

Cannyは、ユーザーフィードバックと機能要求を管理するためのPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [Cannyウェブサイト]（https://canny.io)에にアクセスしてアカウントを作成します。
2. Settings > API Keys メニューに移動します。
3. [Create API Key]ボタンをクリックして新しいAPIキーを生成します。
4. 生成された API キーを安全な場所に保存します。

##使用法

### クライアントの初期化

```python
from canny import CannyClient

client = CannyClient(
    api_key="your_api_key_here",
    base_url="https://canny.io/api/v1"
)
```

###フィードバック投稿の作成

```python
post = client.create_post(
    title="API 속도 개선 요청",
    description="현재 API 응답 시간이 너무 느립니다. 개선이 필요합니다.",
    author_id="user_123",
    board_id="board_456",
    tags=["성능", "API"]
)

print(f"게시물 ID: {post['id']}")
```

###投稿リストの閲覧

```python
posts = client.list_posts(
    board_id="board_456",
    status="open",
    limit=20
)

for post in posts:
    print(f"{post['id']}: {post['title']} ({post['status']})")
```

###投稿の更新

```python
updated_post = client.update_post(
    post_id="post_123",
    status="planned",
    tags=["진행중", "성능"]
)
```

###コメントを追加

```python
comment = client.create_comment(
    post_id="post_123",
    author_id="user_456",
    content="동의합니다. 지금도 로딩이 오래 걸리네요."
)
```

###投票の作成

```python
vote = client.create_vote(
    post_id="post_123",
    author_id="user_789",
    score=1
)
```

### ユーザーの作成

```python
user = client.create_user(
    name="김철수",
    email="cheolsu@example.com",
    avatar_url="https://example.com/avatar.jpg",
    companies=["ABC Corp"]
)
```

### ボードリストの照会

```python
boards = client.list_boards()

for board in boards:
    print(f"{board['id']}: {board['name']}")
```

### 状態の変更

```python
status_change = client.create_status_change(
    post_id="post_123",
    user_id="admin_123",
    status="inProgress",
    comment="개발 시작했습니다. 2주 내에 완료 예정입니다."
)
```

## 機能

- ✅フィードバック投稿の作成、照会、更新
- ✅コメント管理
- ✅投票機能
- ✅ユーザー管理
- ✅ボード管理
- ✅ステータス変更追跡

##ライセンス

MIT License
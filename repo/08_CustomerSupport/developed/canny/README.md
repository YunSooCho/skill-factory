# Canny SDK

Canny는 사용자 피드백 및 기능 요청 관리를 위한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [Canny 웹사이트](https://canny.io)에 접속하여 계정을 생성합니다.
2. Settings > API Keys 메뉴로 이동합니다.
3. 'Create API Key' 버튼을 클릭하여 새 API 키를 생성합니다.
4. 생성된 API 키를 안전한 곳에 저장합니다.

## 사용법

### 클라이언트 초기화

```python
from canny import CannyClient

client = CannyClient(
    api_key="your_api_key_here",
    base_url="https://canny.io/api/v1"
)
```

### 피드백 게시물 생성

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

### 게시물 목록 조회

```python
posts = client.list_posts(
    board_id="board_456",
    status="open",
    limit=20
)

for post in posts:
    print(f"{post['id']}: {post['title']} ({post['status']})")
```

### 게시물 업데이트

```python
updated_post = client.update_post(
    post_id="post_123",
    status="planned",
    tags=["진행중", "성능"]
)
```

### 댓글 추가

```python
comment = client.create_comment(
    post_id="post_123",
    author_id="user_456",
    content="동의합니다. 지금도 로딩이 오래 걸리네요."
)
```

### 투표 생성

```python
vote = client.create_vote(
    post_id="post_123",
    author_id="user_789",
    score=1
)
```

### 사용자 생성

```python
user = client.create_user(
    name="김철수",
    email="cheolsu@example.com",
    avatar_url="https://example.com/avatar.jpg",
    companies=["ABC Corp"]
)
```

### 보드 목록 조회

```python
boards = client.list_boards()

for board in boards:
    print(f"{board['id']}: {board['name']}")
```

### 상태 변경

```python
status_change = client.create_status_change(
    post_id="post_123",
    user_id="admin_123",
    status="inProgress",
    comment="개발 시작했습니다. 2주 내에 완료 예정입니다."
)
```

## 기능

- ✅ 피드백 게시물 생성, 조회, 업데이트
- ✅ 댓글 관리
- ✅ 투표 기능
- ✅ 사용자 관리
- ✅ 보드 관리
- ✅ 상태 변경 추적

## 라이선스

MIT License
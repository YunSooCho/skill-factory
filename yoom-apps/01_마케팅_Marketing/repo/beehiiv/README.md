# Beehiiv API Integration

Beehiiv의 REST API를 사용하여 뉴스레터 구독자, 게시물, 세그먼트를 관리하는 Python 라이브러리입니다.

## 설치

```bash
pip install requests
```

## 사용법

### 클라이언트 초기화

```python
from beehiiv import BeehiivClient

client = BeehiivClient(
    api_key="your_api_key_here",
    publication_id="your_publication_id_here"
)
```

### 구독 관리

```python
# 구독 생성
subscription = client.create_subscription(
    email="user@example.com",
    pub_id="publication_id",
    ref_code="welcome_referral",
    send_welcome_email=True
)

# ID로 구독 조회
subscription = client.get_subscription(subscription_id="sub_id")

# 이메일로 구독 조회
subscription = client.get_subscription_by_email(email="user@example.com")

# 구독 업데이트
updated = client.update_subscription(
    subscription_id="sub_id",
    custom_fields={"name": "John Doe"}
)

# 구독 삭제
client.delete_subscription(subscription_id="sub_id")

# 태그 추가
client.add_tags_to_subscription(
    subscription_id="sub_id",
    tags=["vip", "early-adopter"]
)

# 구독자 ID 목록
subscriber_ids = client.list_subscriber_ids(limit=100)
```

### 게시물 관리

```python
# 단일 게시물 조회
post = client.get_post(post_id="post_id")

# 게시물 검색
posts = client.search_posts(
    status="published",
    limit=20,
    page=1
)
```

### 세그먼트 관리

```python
# 모든 세그먼트 조회
segments = client.retrieve_segments()
```

## API 리소스

| 리소스 | 설명 |
|--------|------|
| `/publications/{id}/subscriptions` | 구독 관리 |
| `/publications/{id}/posts` | 게시물 관리 |
| `/publications/{id}/segments` | 세그먼트 관리 |

## 예외 처리

```python
from beehiiv import BeehiivClient, BeehiivAPIError, BeehiivAuthError

try:
    subscription = client.create_subscription(email="user@example.com")
except BeehiivAuthError as e:
    print("인증 오류:", e)
except BeehiivAPIError as e:
    print("API 오류:", e)
```

## API 메서드

### Subscriptions

| 메서드 | 설명 |
|--------|------|
| `create_subscription()` | 새 구독 생성 |
| `get_subscription(id)` | ID로 구독 조회 |
| `get_subscription_by_email(email)` | 이메일로 구독 조회 |
| `update_subscription(id, ...)` | 구독 업데이트 |
| `delete_subscription(id)` | 구독 삭제 |
| `add_tags_to_subscription(id, tags)` | 태그 추가 |
| `list_subscriber_ids()` | 구독자 ID 목록 |

### Posts

| 메서드 | 설명 |
|--------|------|
| `get_post(id)` | 단일 게시물 조회 |
| `search_posts()` | 게시물 검색 |

### Segments

| 메서드 | 설명 |
|--------|------|
| `retrieve_segments()` | 세그먼트 조회 |

## API 참조

- [Beehiiv API Reference](https://www.beehiiv.com/api-reference/)
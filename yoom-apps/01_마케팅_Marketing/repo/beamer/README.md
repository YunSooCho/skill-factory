# Beamer API Integration

Beamer의 REST API를 사용하여 게시물(Post)을 관리하는 Python 라이브러리입니다.

## 설치

```bash
pip install requests
```

## 사용법

### 클라이언트 초기화

```python
from beamer import BeamerClient

client = BeamerClient(api_key="your_api_key_here")
```

### 게시물 생성

```python
# 간단한 게시물 생성
post = client.create_post(
    headline="새로운 기능 출시!",
    content="<p>We're excited to announce...</p>",
    category="improvement",
    publish=True
)

# 링크가 있는 게시물
post = client.create_post(
    headline="블로그 게시물",
    content="<p>Check out our latest blog post!</p>",
    link="https://example.com/blog",
    linkText="자세히 보기",
    publish=True
)

# 이미지와 카테고리가 있는 게시물
post = client.create_post(
    headline="버그 수정 릴리스",
    content="<p>버그가 수정되었습니다.</p>",
    category="fix",
    image_url="https://example.com/image.png",
    publish=True
)
```

### 게시물 목록

```python
# 모든 게시물
posts = client.list_posts()

# 페이지네이션
posts = client.list_posts(limit=20, page=1)

# 게시된 게시물만
posts = client.list_posts(published=True)
```

### 게시물 삭제

```python
client.delete_post(post_id="post_id_here")
```

## API 엔드포인트

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/posts` | POST | 게시물 생성 |
| `/posts` | GET | 게시물 목록 |
| `/posts/{id}` | DELETE | 게시물 삭제 |

## 예외 처리

```python
from beamer import BeamerClient, BeamerAPIError, BeamerAuthError

try:
    post = client.create_post(headline="테스트", content="<p>테스트</p>")
except BeamerAuthError as e:
    print("인증 오류:", e)
except BeamerAPIError as e:
    print("API 오류:", e)
```

## 파라미터

### create_post()

| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| headline | str | ✅ | 게시물 제목 |
| content | str | ✅ | HTML 형식의 콘텐츠 |
| category | str | ❌ | 카테고리 (new, improvement, fix 등) |
| date | str | ❌ | ISO 8601 형식의 날짜 |
| link | str | ❌ | 외부 링크 URL |
| linkText | str | ❌ | 링크 텍스트 |
| linkIcon | str | ❌ | 링크 아이콘 URL |
| publish | bool | ❌ | 즉시 게시 여부 |
| top | bool | ❌ | 상단 고정 여부 |
| user_segment_external_id | str | ❌ | 단일 사용자 세그먼트 ID |
| user_segments_external_ids | List[str] | ❌ | 사용자 세그먼트 ID 목록 |
| language | str | ❌ | 언어 코드 (en, es, ja 등) |
| image_url | str | ❌ | 커버 이미지 URL |
| change_type | str | ❌ | 변경 유형 |

## API 참조

- [Beamer API Documentation](https://www.usebeamer.com/docs/api/)
# Dlvr.it API Client

Dlvr.it용 Python 클라이언트 - 소셜 미디어 자동 게시

## 설치

```bash
pip install -r requirements.txt
```

## API Key 획득

1. [Dlvr.it 계정 생성](https://dlvrit.com/)
2. 로그인 후 Settings > API Keys 접근
3. API Key 생성
4. API 키 복사

## 사용법

### 클라이언트 초기화

```python
from dlvr_it_client import DlvrItClient

client = DlvrItClient(api_key='your-api-key')
```

### 계정 목록 조회

```python
accounts = client.list_accounts()

for account in accounts['accounts']:
    print(f"{account['provider']}: {account['handle']}")
    print(f"ID: {account['id']}")
```

### 라우트 목록 조회

```python
routes = client.list_routes()

for route in routes['routes']:
    print(f"{route['name']}: {len(route['accounts'])} accounts")
```

### 계정에 게시물 생성

```python
# 계정 ID로 단일 게시
post = client.create_post_to_account(
    account_id='account-123',
    content='Check out this amazing content!',
    scheduled_at='2024-02-28T10:00:00Z',  # 선택: 예약 시간
    media_urls=['https://example.com/image.jpg'],  # 선택
    link_url='https://example.com',  # 선택
    link_title='Example Post'  # 선택
)

print(f"Post ID: {post['id']}")
print(f"Status: {post['status']}")
```

### 라우트에 게시물 생성 (여러 계정에 한 번에)

```python
result = client.create_post_to_route(
    route_id='route-456',
    content='This will be posted to all accounts in the route!',
    scheduled_at='2024-02-28T11:00:00Z',
    media_urls=['https://example.com/video.mp4']
)

for post in result['posts']:
    print(f"Posted to account {post['account_id']}: {post['id']}")
```

### 게시물 상세 조회

```python
post = client.get_post(post_id='post-789')
print(f"Content: {post['content']}")
print(f"Status: {post['status']}")
```

### 게시물 삭제 (예약된 게시물만)

```python
client.delete_post(post_id='post-789')
```

### 게시물 목록 조회

```python
posts = client.list_posts(
    status='scheduled',  # scheduled, published, failed
    limit=10
)

for post in posts['posts']:
    print(f"{post['content'][:50]}... - {post['status']}")
```

### 예약된 게시물 목록

```python
scheduled = client.get_scheduled_posts(limit=20)
```

## 주요 기능

1. **다중 계정 지원**: 페이스북, 트위터, 인스타그램, 링크드인 등
2. **라우트 관리**: 계정 그룹 필터링
3. **예약 게시**: 지정된 시간에 자동 게시
4. **미디어 첨부**: 이미지, 비디오 지원
5. **링크 썸네일**: Open Graph 메타데이터 처리

## 에러 처리

```python
from dlvr_it_client import DlvrItError, RateLimitError

try:
    post = client.create_post_to_account(
        account_id='account-123',
        content='Test post'
    )
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except DlvrItError as e:
    print(f"API error: {e}")
```

## API 제한

- 기본 제한: 초당 10 요청
- 무료 요금제: 월 10 게시
- 유료 요금제: 무제한 게시

## 지원

자세한 API 문서: [Dlvr.it Developer Documentation](https://dlvrit.com/developers/)
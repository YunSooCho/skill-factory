# LaunchDarkly API Client

A Python client for interacting with LaunchDarkly's REST API.

## API Key 발급 방법

1. [LaunchDarkly](https://app.launchdarkly.com/)에 로그인
2. 우측 상단 프로필 아이콘 클릭 → Account Settings
3. Authorization 탭 → Access Tokens → Create Token
4. 토큰 이름 입력 및 권한 선택
5. 생성된 토큰을 안전하게 저장

**권한 설정:**
- `Reader`: 읽기 전용
- `Writer`: 플래그/세그먼트 생성 및 수정 가능
- `Admin`: 모든 권한

## 설치

```bash
pip install -r requirements.txt
```

## 사용법

### 기본 설정

```python
from launchdarkly import LaunchDarklyClient

# 클라이언트 초기화
client = LaunchDarklyClient(
    access_token="api-xxxxx-xxxxx-xxxxx-xxxxx",
    default_project_key="my-project",
    default_env_key="production"
)
```

### 피처 플래그 관리

```python
# 플래그 생성
flag = client.create_flag(
    key="new-feature",
    name="New Feature",
    description="Enable new feature for users",
    kind="boolean",
    default_variation=0
)

# 플래그 조회
flag = client.get_flag("new-feature")

# 플래그 목록 조회
flags = client.list_flags(project_key="my-project", tag="experiment")

# 플래그 ON/OFF
updated_flag = client.update_flag(
    key="new-feature",
    on=True,
    default_variation=0
)

# 플래그 삭제
client.delete_flag("new-feature")
```

### 사용자 세그먼트 관리

```python
# 세그먼트 생성
segment = client.create_segment(
    key="premium-users",
    name="Premium Users",
    description="Users with premium subscription",
    rules=[{
        "clauseType": "segmentMatch",
        "values": ["premium-subscription"]
    }]
)

# 세그먼트 조회
segment = client.get_segment("premium-users")

# 세그먼트 목록
segments = client.list_segments()
```

### 프로젝트 및 환경 관리

```python
# 프로젝트 목록
projects = client.list_projects()

# 특정 프로젝트 정보
project = client.get_project("my-project")

# 환경 목록
environments = client.list_environments(project_key="my-project")

# 특정 환경 정보
env = client.get_environment(project_key="my-project", env_key="production")
```

### 사용자 검색

```python
# 사용자 검색
users = client.search_users(
    filter='email contains "@company.com"',
    sort="lastSeen",
    limit=50
)

# 사용자 생성 (대시보드용)
user = client.create_user(
    key="user-123",
    email="user@example.com",
    name="John Doe",
    custom={"plan": "premium"}
)
```

### 웹훅 관리

```python
# 웹훅 생성
webhook = client.create_webhook(
    url="https://your-app.com/webhook",
    secret="your-secret",
    sign=True
)

# 웹훅 목록
webhooks = client.list_webhooks()

# 웹훅 삭제
client.delete_webhook(webhook_id)
```

## 예시 코드

### 플래그 A/B 테스트 설정

```python
# 멀티바리에이트 플래그 생성
flag = client.create_flag(
    key="homepage-variation",
    name="Homepage A/B Test",
    description="Test different homepage layouts",
    kind="multivariate",
    variations=[
        {"value": "control", "_name": "Control"},
        {"value": "variant-a", "_name": "Variant A"},
        {"value": "variant-b", "_name": "Variant B"},
    ],
    tags=["ab-test", "homepage"]
)

# 롤아웃 비율 설정 (프로젝트 키 필요)
client.update_flag(
    key="homepage-variation",
    on=True
)
```

### 세그먼트 기반 타겟팅

```python
# 베타 테스터 세그먼트 생성
segment = client.create_segment(
    key="beta-testers",
    name="Beta Testers",
    description="Internal beta testing team",
    included=["user-alpha", "user-beta", "user-gamma"]
)

# 플래그에 세그먼트 규칙 적용 (추후 업데이트 시)
# rules 파라미터를 사용하여 세그먼트를 포함
```

## API 레퍼런스

### LaunchDarklyClient

| 메서드 | 설명 |
|--------|------|
| `create_flag()` | 피처 플래그 생성 |
| `get_flag()` | 플래그 조회 |
| `update_flag()` | 플래그 업데이트 |
| `delete_flag()` | 플래그 삭제 |
| `list_flags()` | 플래그 목록 |
| `create_segment()` | 세그먼트 생성 |
| `get_segment()` | 세그먼트 조회 |
| `list_segments()` | 세그먼트 목록 |
| `list_projects()` | 프로젝트 목록 |
| `get_project()` | 프로젝트 조회 |
| `search_users()` | 사용자 검색 |
| `list_webhooks()` | 웹훅 목록 |

## 에러 처리

```python
from launchdarkly import (
    LaunchDarklyError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    ResourceNotFoundError
)

try:
    flag = client.get_flag("new-feature")
except AuthenticationError:
    print("API 토큰이 유효하지 않습니다.")
except ResourceNotFoundError:
    print("플래그를 찾을 수 없습니다.")
except RateLimitError as e:
    print(f"Rate limit 초과: {e.retry_after}초 후 다시 시도하세요.")
except LaunchDarklyError as e:
    print(f"Error: {e.message}")
```

## Rate Limiting

LaunchDarkly API는 대부분의 엔드포인트에 대해 분당 60회 요청 제한이 있습니다.
클라이언트는 자동으로 rate limiting을 적용합니다.

## 라이선스

MIT License

## 더 많은 정보

- [LaunchDarkly API 문서](https://apidocs.launchdarkly.com/)
- [LaunchDarkly 공식 문서](https://docs.launchdarkly.com/)
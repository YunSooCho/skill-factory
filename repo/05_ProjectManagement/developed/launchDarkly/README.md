# LaunchDarkly API 클라이언트

LaunchDarkly를 위한 Python 클라이언트입니다. 기능 플래그 관리 기능을 제공합니다.

## 개요

LaunchDarkly는 기능 플래그 관리 플랫폼입니다. 이 클라이언트는 API를 통해 LaunchDarkly에 접근합니다.

## 설치

```bash
pip install requests
```

또는:

```bash
pip install -r requirements.txt
```

## API 키 발급

1. [LaunchDarkly](https://launchdarkly.com/)에서 계정 생성
2. API 키 발급
3. 발급된 키를 안전하게 저장

## 사용법

### 초기화

```python
from launchdarkly import LaunchDarklyClient, LaunchDarklyError

client = LaunchDarklyClient(
    access_token="YOUR_API_KEY",
    timeout=30
)
```

### 주요 기능

- flags
- projects
- environments

### 예시

```python
# 프로젝트 조회
projects = client.get_projects()

# 플래그 조회
flags = client.get_flags("my-project")

# 특정 플래그 조회
flag = client.get_flag("my-project", "my-flag", environment_key="production")

# 플래그 생성
flag = client.create_flag(
    "my-project",
    "my-flag",
    name="My Flag",
    description="A feature flag"
)

# 환경 조회
environments = client.get_environments("my-project")
```

## 에러 처리

```python
try:
    flags = client.get_flags("my-project")
except LaunchDarklyAuthenticationError:
    print("인증 실패")
except LaunchDarklyRateLimitError:
    print("속도 제한 초과")
except LaunchDarklyError as e:
    print(f"요청 실패: {str(e)}")
```

## 라이선스

MIT License

## 지원

- [LaunchDarkly Documentation](https://docs.launchdarkly.com/)
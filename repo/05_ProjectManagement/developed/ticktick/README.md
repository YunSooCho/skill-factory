# TickTick API 클라이언트

Task and to-do list management를 위한 Python 클라이언트입니다.

## 개요

Task and to-do list management. 이 클라이언트는 OAuth 인증을 통해 TickTick API에 접근합니다.

## 설치

\`\`\`bash
pip install requests
\`\`\`

또는:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

## OAuth 액세스 토큰 발급

1. 해당 서비스에서 앱 등록
2. OAuth 2.0 흐름을 통해 액세스 토큰 발급
3. 발급된 토큰을 안전하게 저장

## 사용법

### 초기화

\`\`\`python
from ticktick import TicktickClient, TicktickError

client = TicktickClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
\`\`\`

### 주요 기능

\`\`\`python
- tasks
- lists
- projects
\`\`\`

### 예시

\`\`\`python
# 데이터 조회
result = client.get_tasks()

# 데이터 생성
result = client.create_task(
    name="Example Name"
)
\`\`\`

## 에러 처리

\`\`\`python
try:
    result = client.get_tasks()
except TicktickAuthenticationError:
    print("인증 실패")
except TicktickRateLimitError:
    print("속도 제한 초과")
except TicktickError as e:
    print(f"요청 실패: {str(e)}")
\`\`\`

## 라이선스

MIT License

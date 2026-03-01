# Product Fruits SDK

Product Fruits는 제품 온보딩 및 사용자 가이드 관리를 위한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [Product Fruits 웹사이트](https://productfruits.com)에 접속하여 계정을 생성합니다.
2. 대시보드에서 Settings > API Keys 메뉴로 이동합니다.
3. 'Create API Key' 버튼을 클릭하여 새 API 키를 생성합니다.
4. 생성된 API 키와 Workspace ID를 안전한 곳에 저장합니다.

## 사용법

### 클라이언트 초기화

```python
from product_fruits import ProductFruitsClient

client = ProductFruitsClient(
    api_key="your_api_key_here",
    workspace_id="your_workspace_id",
    base_url="https://api.productfruits.com"
)
```

### 투어 생성

```python
tour = client.create_tour(
    name="신규 사용자 온보딩",
    description="새 사용자를 위한 기능 안내",
    steps=[
        {
            "title": "환영합니다!",
            "content": "서비스를 이용해 주셔서 감사합니다.",
            "selector": ".welcome-message",
            "position": "center"
        },
        {
            "title": "대시보드",
            "content": "여기서 주요 통계를 확인할 수 있습니다.",
            "selector": ".dashboard",
            "position": "right"
        }
    ],
    target_url_pattern="/dashboard*",
    trigger_type="onboarding",
    is_active=True
)

print(f"투어 ID: {tour['id']}")
```

### 툴팁 생성

```python
tooltip = client.create_tooltip(
    name="도움말 툴팁",
    selector=".help-button",
    content="클릭하면 도움말을 볼 수 있습니다.",
    position="top",
    trigger_type="hover",
    is_active=True
)
```

### 체크리스트 생성

```python
checklist = client.create_checklist(
    name="회원가입 완료 체크리스트",
    description="서비스 사용을 위해 다음 항목을 완료해 주세요.",
    items=[
        {
            "title": "프로필 설정",
            "description": "프로필 정보를 입력해 주세요.",
            "targetUrl": "/profile"
        },
        {
            "title": "이메일 인증",
            "description": "인증 이메일을 확인해 주세요.",
            "targetUrl": "/verify-email"
        }
    ],
    target_url_pattern="/onboarding*",
    is_active=True
)
```

### 사용자 진행상황 조회

```python
progress = client.get_user_progress(
    user_id="user_123",
    checklist_id="checklist_456"
)

print(f"진행률: {progress['completionPercentage']}%")
print(f"완료 항목: {progress['completedItems']}/{progress['totalItems']}")
```

### 이벤트 추적

```python
client.track_event(
    user_id="user_123",
    event_name="tour_completed",
    properties={
        "tour_id": "tour_456",
        "completion_time": 120
    }
)
```

### 공지사항 생성

```python
announcement = client.create_announcement(
    name="새로운 기능 알림",
    content="새로운 기능이 추가되었습니다!",
    target_url_pattern="/",
    display_type="banner",
    start_date="2024-01-01",
    end_date="2024-01-31",
    is_active=True
)
```

### 분석 데이터 조회

```python
analytics = client.get_analytics(
    start_date="2024-01-01",
    end_date="2024-01-31",
    content_type="tour"
)

print(f"투어 조회수: {analytics['tourViews']}")
print(f"완료율: {analytics['completionRate']}%")
```

## 기능

- ✅ 투어 관리 (생성, 조회, 업데이트)
- ✅ 툴팁 관리
- ✅ 체크리스트 관리
- ✅ 사용자 진행상황 추적
- ✅ 이벤트 추적
- ✅ 공지사항 관리
- ✅ 분석 및 리포트

## 라이선스

MIT License
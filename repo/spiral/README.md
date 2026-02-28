# Spiral 비즈니스 플랫폼 SDK

Spiral은 통합 비즈니스 관리 플랫폼에 대한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [Spiral](https://spiralplatform.com)에 접속하여 계정을 생성합니다.
2. 설정(Settings) > API Keys 섹션으로 이동합니다.
3. 새 API 키를 생성합니다.
4. 생성된 API 키를 안전한 곳에 저장합니다.

## 사용법

### 클라이언트 초기화

```python
from spiral import SpiralClient

client = SpiralClient(
    api_key="your_api_key_here"
)
```

### 고객 관리

```python
# 고객 목록
customers = client.get_customers(page=1, per_page=50)

# 고객 생성
client.create_customer(
    name="홍길동",
    email="hong@example.com",
    phone="010-1234-5678",
    company="ABC Corporation"
)

# 고객 업데이트 및 삭제
client.update_customer(customer_id="id", name="수정된 이름")
client.delete_customer(customer_id="id")
```

### 프로젝트 관리

```python
# 프로젝트 목록
projects = client.get_projects(page=1, per_page=50, customer_id="customer_id")

# 프로젝트 생성
client.create_project(
    name="웹 개발 프로젝트",
    customer_id="customer_id",
    description="반응형 웹사이트 개발",
    status="active"
)
```

### 작업 관리

```python
# 작업 목록
tasks = client.get_tasks(page=1, per_page=50, project_id="project_id")

# 작업 생성
client.create_task(
    title="디자인 완료",
    project_id="project_id",
    description="메인 페이지 UI 디자인",
    status="in_progress",
    priority="high"
)
```

### 판매 기회(Deal) 관리

```python
# 딜 목록
deals = client.get_deals(page=1, per_page=50)

# 딜 생성
client.create_deal(
    title="연간 계약",
    customer_id="customer_id",
    amount=12000000,
    stage="negotiation"
)
```

## 주요 기능

- ✅ 고객 관리
- ✅ 프로젝트 관리
- ✅ 작업(Task) 관리
- ✅ 판매 기회(Deal) 추적
- ✅ 리포트

## 라이선스

MIT License
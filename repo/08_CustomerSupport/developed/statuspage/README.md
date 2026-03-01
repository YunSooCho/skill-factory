# Statuspage SDK

Statuspage는 서비스 상태 모니터링 및 인시던트 관리를 위한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [Statuspage.io 웹사이트](https://statuspage.io)에 접속하여 계정을 생성합니다.
2. 새 상태페이지를 생성하거나 기존 페이지의 설정 메뉴로 이동합니다.
3. API > API Tokens에서 새 API 토큰을 생성합니다.
4. 페이지 ID(URL에서 확인 가능)와 API 토큰을 안전한 곳에 저장합니다.

## 사용법

### 클라이언트 초기화

```python
from statuspage import StatuspageClient

client = StatuspageClient(
    api_key="your_api_key_here",
    page_id="your_page_id",
    base_url="https://api.statuspage.io/v1"
)
```

### 상태페이지 요약 조회

```python
summary = client.get_page_summary()

print(f"페이지 이름: {summary['name']}")
print(f"URL: {summary['url']}")
print(f"전체 상태: {summary['status_indicator']}")
```

### 컴포넌트 생성

```python
component = client.create_component(
    name="API 서버",
    status="operational",
    description="메인 API 서비스",
    showcase=True
)

print(f"컴포넌트 ID: {component['id']}")
```

### 컴포넌트 상태 업데이트

```python
updated = client.update_component(
    component_id="component_123",
    status="degraded"
)
```

### 컴포넌트 목록 조회

```python
components = client.list_components()

for component in components:
    print(f"{component['name']}: {component['status']}")
```

### 인시던트 생성

```python
incident = client.create_incident(
    name="API 서버 응답 지연",
    status="investigating",
    body="현재 API 서버의 응답 시간이 평소보다 느립니다. 원인을 조사 중입니다.",
    component_ids=["component_123"],
    components={"component_123": "degraded"},
    impact_override="major",
    deliver_notifications=True
)

print(f"인시던트 ID: {incident['id']}")
```

### 인시던트 업데이트

```python
updated = client.update_incident(
    incident_id="incident_456",
    status="identified",
    body="데이터베이스 쿼리 성능 문제로 확인되었습니다."
)
```

### 인시던트 해결

```python
updated = client.update_incident(
    incident_id="incident_456",
    status="resolved",
    body="인덱스 최적화를 완료하여 서비스가 정상화되었습니다.",
    components={"component_123": "operational"}
)
```

### 인시던트 목록 조회

```python
incidents = client.list_incidents(
    status="open",
    impact="major",
    limit=20
)

for incident in incidents:
    print(f"{incident['name']} - {incident['status']} ({incident['impact']})")
```

### 인시던트 업데이트 추가

```python
update = client.create_incident_update(
    incident_id="incident_456",
    body="문제가 해결되어 정상 상태로 복귀했습니다.",
    status="resolved"
)

print(f"업데이트 ID: {update['id']}")
```

### 메인테넌스 생성

```python
maintenance = client.create_maintenance(
    name="데이터베이스 서버 업그레이드",
    scheduled_for="2024-02-15T02:00:00Z",
    scheduled_until="2024-02-15T04:00:00Z",
    status="scheduled",
    body="데이터베이스 서버 버전 업그레이드 예정입니다.",
    component_ids=["component_123"],
    components={"component_123": "under_maintenance"},
    auto_transition_to_in_progress=True,
    auto_transition_to_operational=True
)

print(f"메인테넌스 ID: {maintenance['id']}")
```

### 메인테넌스 목록 조회

```python
maintenances = client.list_maintenances(
    status="scheduled",
    limit=10
)

for maintenance in maintenances:
    print(f"{maintenance['name']}: {maintenance['scheduled_for']}")
```

### 메인테넌스 업데이트

```python
updated = client.update_maintenance(
    maintenance_id="maintenance_789",
    status="completed"
)
```

### 구독자 목록 조회

```python
subscribers = client.get_subscribers(limit=50)

for sub in subscribers:
    print(f"{sub['email']} - {sub['mode']}")
```

## 컴포넌트 상태

- **operational**: 정상
- **degraded**: 성능 저하
- **partial_outage**: 부분 장애
- **major_outage**: 주요 장애
- **under_maintenance**: 메인테넌스 중

## 인시던트 상태

- **investigating**: 조사 중
- **identified**: 원인 파악
- **monitoring**: 모니터링 중
- **resolved**: 해결됨
- **postmortem**: 사후 분석

## 영향도

- **critical**: 치명적
- **major**: 주요
- **minor**: 사소
- **none**: 없음

## 기능

- ✅ 컴포넌트 관리 (생성, 조회, 업데이트, 삭제)
- ✅ 인시던트 관리
- ✅ 인시던트 업데이트 추가
- ✅ 메인테넌스 예약 및 관리
- ✅ 구독자 관리
- ✅ 상태페이지 요약 조회

## 라이선스

MIT License
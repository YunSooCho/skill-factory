# Canbus 비즈니스 관리 SDK

Canbus는 프로젝트 및 작업 관리를 위한 플랫폼에 대한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [Canbus 웹사이트](https://www.canbus.io)에 접속하여 계정을 생성합니다.
2. 설정(Settings) > API Keys 섹션으로 이동합니다.
3. 'Create API Key' 버튼을 클릭하여 새 API 키를 생성합니다.
4. 생성된 API 키를 안전한 곳에 저장합니다.

## 사용법

### 클라이언트 초기화

```python
from canbus import CanbusClient

client = CanbusClient(
    api_key="your_api_key_here"
)
```

### 워크스페이스 관리

```python
# 모든 워크스페이스 목록
workspaces = client.get_workspaces()
for ws in workspaces:
    print(f"워크스페이스 ID: {ws['id']}, 이름: {ws['name']}")

# 워크스페이스 생성
new_workspace = client.create_workspace(
    name="마케팅 팀",
    description="마케팅 캠페인 관리"
)

# 워크스페이스 상세 정보
workspace = client.get_workspace(workspace_id="workspace_id")

# 워크스페이스 수정
client.update_workspace(
    workspace_id="workspace_id",
    name="마케팅 및 SEO 팀"
)

# 워크스페이스 삭제
client.delete_workspace(workspace_id="workspace_id")
```

### 프로젝트 관리

```python
# 프로젝트 목록
projects = client.get_projects(workspace_id="workspace_id")
for project in projects:
    print(f"프로젝트: {project['name']}, 상태: {project['status']}")

# 프로젝트 생성
project = client.create_project(
    workspace_id="workspace_id",
    name="Q1 마케팅 캠페인",
    description="2024년 1분기 마케팅 활동",
    status="active",
    priority="high",
    start_date="2024-01-01",
    end_date="2024-03-31"
)
print(f"생성된 프로젝트 ID: {project['id']}")

# 프로젝트 수정
client.update_project(
    workspace_id="workspace_id",
    project_id="project_id",
    status="in_progress",
    priority="urgent"
)

# 프로젝트 삭제
client.delete_project(workspace_id="workspace_id", project_id="project_id")
```

### 작업(Task) 관리

```python
# 작업 목록 조회
tasks = client.get_tasks(
    workspace_id="workspace_id",
    project_id="project_id",
    status="todo",
    limit=20
)

for task in tasks:
    print(f"작업: {task['title']}, 담당자: {task.get('assignee')}")

# 작업 생성
task = client.create_task(
    workspace_id="workspace_id",
    project_id="project_id",
    title="랜딩 페이지 디자인",
    description="메인 랜딩 페이지 UI/UX 디자인",
    status="todo",
    priority="high",
    assignee_id="user_id",
    due_date="2024-01-15",
    tags=["디자인", "우선순위"]
)

# 작업 상세 조회
task = client.get_task(
    workspace_id="workspace_id",
    project_id="project_id",
    task_id="task_id"
)

# 작업 수정
client.update_task(
    workspace_id="workspace_id",
    project_id="project_id",
    task_id="task_id",
    status="in_progress",
    assignee_id="new_user_id"
)

# 작업 삭제
client.delete_task(
    workspace_id="workspace_id",
    project_id="project_id",
    task_id="task_id"
)
```

### 댓글 관리

```python
# 작업 댓글 작성
comment = client.create_task_comment(
    workspace_id="workspace_id",
    project_id="project_id",
    task_id="task_id",
    comment="디자인 초안 검토가 필요합니다.",
    author="홍길동"
)

# 작업 댓글 목록
comments = client.get_task_comments(
    workspace_id="workspace_id",
    project_id="project_id",
    task_id="task_id"
)
```

### 팀 멤버 관리

```python
# 팀 멤버 목록
members = client.get_team_members(workspace_id="workspace_id")
for member in members:
    print(f"멤버: {member['name']}, 역할: {member['role']}")

# 팀 멤버 초대
client.add_team_member(
    workspace_id="workspace_id",
    email="newuser@example.com",
    role="editor"
)

# 팀 멤버 제거
client.remove_team_member(
    workspace_id="workspace_id",
    member_id="member_id"
)
```

### 리포트 및 통계

```python
# 리포트 생성
report = client.get_reports(
    workspace_id="workspace_id",
    project_id="project_id",
    start_date="2024-01-01",
    end_date="2024-01-31"
)

# 프로젝트 통계
stats = client.get_project_statistics(
    workspace_id="workspace_id",
    project_id="project_id"
)
print(f"완료된 작업: {stats['completedTasks']}")
print(f"진행 중인 작업: {stats['inProgressTasks']}")
```

### 검색

```python
# 작업 검색
results = client.search_tasks(
    workspace_id="workspace_id",
    query="디자인",
    project_id="project_id"
)

for task in results:
    print(f"검색 결과: {task['title']}")
```

### 라벨 관리

```python
# 라벨 목록
labels = client.get_labels(workspace_id="workspace_id")

# 라벨 생성
label = client.create_label(
    workspace_id="workspace_id",
    name="긴급",
    color="#FF0000"
)
```

### 활동 로그

```python
# 워크스페이스 활동 로그
activities = client.get_activity_log(
    workspace_id="workspace_id",
    limit=50
)

for activity in activities:
    print(f"{activity['timestamp']}: {activity['description']}")
```

## 주요 기능

- ✅ 워크스페이스 관리
- ✅ 프로젝트 생성 및 관리
- ✅ 작업(Task) CRUD 작업
- ✅ 팀 멤버 관리
- ✅ 댓글 및 협업 기능
- ✅ 리포트 및 통계
- ✅ 작업 검색
- ✅ 라벨 및 태그 관리
- ✅ 활동 로그 추적

## 라이선스

MIT License
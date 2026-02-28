# Asana OAuth API 클라이언트

Asana OAuth를 위한 Python API 클라이언트입니다. 프로젝트 및 작업 관리 기능을 제공합니다.

## 개요

Asana는 프로젝트 관리 및 협업 플랫폼입니다. 이 클라이언트는 OAuth 인증을 통해 Asana API에 접근합니다.

## 설치

```bash
pip install requests
```

또는:

```bash
pip install -r requirements.txt
```

## OAuth 액세스 토큰 발급

1. [Asana Developers](https://developers.asana.com/)에서 앱 등록
2. OAuth 2.0 흐름을 통해 액세스 토큰 발급
3. 발급된 토큰을 안전하게 저장

## 사용법

### 초기화

```python
from asana_oauth import AsanaOAuthClient, AsanaOAuthError

client = AsanaOAuthClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
```

### 워크스페이스 조회

```python
workspaces = client.get_workspaces()
```

### 팀 조회

```python
teams = client.get_teams(workspace_id="123456789")
```

### 프로젝트 조회

```python
# 모든 프로젝트
projects = client.get_projects()

# 특정 워크스페이스
projects = client.get_projects(workspace="123456789")

# 특정 팀
projects = client.get_projects(team="987654321")
```

### 프로젝트 생성

```python
project = client.create_project(
    workspace="123456789",
    name="My Project",
    team="987654321"
)
```

### 작업 조회

```python
# 프로젝트의 작업
tasks = client.get_tasks(project="project_id")

# 특정 사용자의 작업
tasks = client.get_tasks(assignee="user_id")

# 완료된 작업
tasks = client.get_tasks(completed=True)
```

### 작업 생성

```python
task = client.create_task(
    workspace="123456789",
    name="New Task",
    project="project_id",
    assignee="user_id",
    due_on="2024-12-31"
)
```

### 작업 완료

```python
task = client.complete_task("task_id")
```

### 작업 업데이트

```python
task = client.update_task(
    "task_id",
    name="Updated Name",
    notes="Updated notes",
    due_on="2024-12-31"
)
```

### 섹션 관리

```python
# 섹션 조회
sections = client.get_sections("project_id")

# 섹션 생성
section = client.create_section("project_id", "To Do")

# 작업을 섹션에 추가
result = client.add_task_to_section("section_id", "task_id")
```

### 사용자 관리

```python
# 워크스페이스 사용자
users = client.get_users("workspace_id")

# 사용자 정보
user = client.get_user("user_id")
```

### 코멘트 추가

```python
comment = client.add_comment_to_task("task_id", "This is a comment")
```

### 작업 검색

```python
results = client.search_tasks(
    query="important",
    workspace="workspace_id"
)
```

### 파일 첨부

```python
attachment = client.attach_file_to_task("task_id", "document.pdf")
```

## 에러 처리

```python
try:
    task = client.create_task(workspace, name)
except AsanaOAuthAuthenticationError:
    print("인증 실패")
except AsanaOAuthRateLimitError:
    print("속도 제한 초과")
except AsanaOAuthError as e:
    print(f"요청 실패: {str(e)}")
```

## 라이선스

MIT License

## 지원

- [Asana Developers](https://developers.asana.com/)
- [API 문서](https://developers.asana.com/docs)
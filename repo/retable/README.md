# Retable 협업 스프레드시트 SDK

Retable는 현대적인 스프레드시트 및 데이터베이스 협업 플랫폼에 대한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [Retable.io](https://retable.io)에 접속하여 계정을 생성합니다.
2. 프로필 설정(Settings) > API Keys 섹션으로 이동합니다.
3. 새 API 키를 생성합니다.
4. 생성된 API 키를 안전한 곳에 저장합니다.

## 사용법

### 클라이언트 초기화

```python
from retable import RetableClient

client = RetableClient(
    api_key="your_api_key_here"
)
```

### 워크스페이스 관리

```python
# 모든 워크스페이스 목록
workspaces = client.get_workspaces()
for ws in workspaces:
    print(f"워크스페이스 ID: {ws['id']}, 이름: {ws['name']}")

# 워크스페이스 상세 정보
workspace = client.get_workspace(workspace_id="workspace_id")

# 워크스페이스 생성
new_workspace = client.create_workspace(
    name="마케팅 팀",
    description="마케팅 활동 관리"
)

# 워크스페이스 업데이트
client.update_workspace(
    workspace_id="workspace_id",
    name="마케팅 및 SEO 팀"
)

# 워크스페이스 삭제
client.delete_workspace(workspace_id="workspace_id")
```

### 프로젝트 관리

```python
# 워크스페이스 내 프로젝트 목록
projects = client.get_projects(workspace_id="workspace_id")
for project in projects:
    print(f"프로젝트 ID: {project['id']}, 이름: {project['name']}")

# 프로젝트 상세 정보
project = client.get_project(project_id="project_id")

# 프로젝트 생성
new_project = client.create_project(
    workspace_id="workspace_id",
    name="Q1 캠페인",
    description="2024년 1분기 마케팅 캠페인"
)

# 프로젝트 업데이트
client.update_project(
    project_id="project_id",
    name="Q1 캠페인 (수정)"
)

# 프로젝트 삭제
client.delete_project(project_id="project_id")
```

### 테이블 관리

```python
# 프로젝트 내 테이블 목록
tables = client.get_tables(project_id="project_id")
for table in tables:
    print(f"테이블 ID: {table['id']}, 이름: {table['name']}")

# 테이블 상세 정보
table = client.get_table(table_id="table_id")

# 테이블 생성
new_table = client.create_table(
    project_id="project_id",
    name="작업 목록",
    description="프로젝트 작업 추적"
)

# 테이블 업데이트
client.update_table(
    table_id="table_id",
    name="작업 항목"
)

# 테이블 삭제
client.delete_table(table_id="table_id")
```

### 열(Column) 관리

```python
# 테이블 내 열 목록
columns = client.get_columns(table_id="table_id")
for col in columns:
    print(f"열 ID: {col['id']}, 이름: {col['name']}, 유형: {col['type']}")

# 열 상세 정보
column = client.get_column(column_id="column_id")

# 텍스트 열 생성
text_column = client.create_column(
    table_id="table_id",
    type="text",
    name="제목",
    description="작업 제목"
)

# 드롭다운 열 생성
dropdown_column = client.create_column(
    table_id="table_id",
    type="dropdown",
    name="상태",
    options={
        "choices": ["진행 중", "완료", "보류"]
    }
)

# 날짜 열 생성
date_column = client.create_column(
    table_id="table_id",
    type="date",
    name="마감일"
)

# 열 업데이트
client.update_column(
    column_id="column_id",
    name="제목 (수정)"
)

# 열 삭제
client.delete_column(column_id="column_id")
```

### 행(Row) 관리

```python
# 행 목록 조회
rows = client.get_rows(
    table_id="table_id",
    limit=100,
    offset=0,
    sort_by="column_id",
    sort_order="desc"
)

for row in rows['rows']:
    print(f"행 ID: {row['id']}")
    for cell_id, cell_value in row['cells'].items():
        print(f"  {cell_id}: {cell_value}")

# 특정 행 조회
row = client.get_row(row_id="row_id")

# 행 생성
new_row = client.create_row(
    table_id="table_id",
    cells={
        "column_id_1": "새 작업",
        "column_id_2": "진행 중",
        "column_id_3": "2024-12-25"
    }
)

# 행 업데이트
client.update_row(
    row_id="row_id",
    cells={
        "column_id_2": "완료",
        "column_id_1": "완료된 작업"
    }
)

# 행 삭제
client.delete_row(row_id="row_id")
```

### 일괄 작업

```python
# 여러 행 일괄 생성
batch_result = client.batch_create_rows(
    table_id="table_id",
    rows=[
        {"cells": {"col1": "작업 1", "col2": "진행 중"}},
        {"cells": {"col1": "작업 2", "col2": "보류"}},
        {"cells": {"col1": "작업 3", "col2": "진행 중"}}
    ]
)

# 여러 행 일괄 업데이트
batch_update = client.batch_update_rows(
    updates=[
        {"row_id": "row1", "cells": {"col2": "완료"}},
        {"row_id": "row2", "cells": {"col2": "완료"}}
    ]
)

# 여러 행 일괄 삭제
client.batch_delete_rows(["row1", "row2", "row3"])
```

### 쿼리 및 필터링

```python
# 쿼리로 행 검색
filtered_rows = client.query_rows(
    table_id="table_id",
    filter_by={
        "conditions": [
            {
                "column_id": "status_column",
                "operator": "equals",
                "value": "진행 중"
            }
        ]
    },
    limit=50
)

# 복합 쿼리
filtered_rows = client.query_rows(
    table_id="table_id",
    filter_by={
        "operator": "AND",
        "conditions": [
            {
                "column_id": "status_column",
                "operator": "equals",
                "value": "진행 중"
            },
            {
                "column_id": "date_column",
                "operator": "before",
                "value": "2024-12-31"
            }
        ]
    }
)
```

### 뷰(View) 관리

```python
# 테이블 뷰 목록
views = client.get_views(table_id="table_id")
for view in views:
    print(f"뷰 ID: {view['id']}, 이름: {view['name']}, 유형: {view['type']}")

# 뷰 상세 정보
view = client.get_view(view_id="view_id")

# 뷰 생성
new_view = client.create_view(
    table_id="table_id",
    type="grid",
    name="진행 중 작업",
    filters={
        "conditions": [
            {
                "column_id": "status_column",
                "operator": "equals",
                "value": "진행 중"
            }
        ]
    },
    sorts=[
        {
            "column_id": "date_column",
            "direction": "asc"
        }
    ]
)

# 뷰 업데이트
client.update_view(
    view_id="view_id",
    name="긴급 작업"
)

# 뷰 삭제
client.delete_view(view_id="view_id")
```

### 폼(Form) 관리

```python
# 프로젝트 내 폼 목록
forms = client.get_forms(project_id="project_id")
for form in forms:
    print(f"폼 ID: {form['id']}, 이름: {form['name']}")

# 폼 상세 정보
form = client.get_form(form_id="form_id")

# 폼 생성
new_form = client.create_form(
    table_id="table_id",
    name="작업 제출",
    description="새 작업을 제출합니다",
    fields=["column_id_1", "column_id_2"]
)

# 폼 업데이트
client.update_form(
    form_id="form_id",
    name="업데이트된 폼",
    fields=["column_id_1", "column_id_2", "column_id_3"]
)

# 폼 삭제
client.delete_form(form_id="form_id")
```

### 멤버 관리

```python
# 워크스페이스 멤버 목록
members = client.get_members(workspace_id="workspace_id")
for member in members:
    print(f"멤버: {member['email']}, 역할: {member['role']}")

# 멤버 추가
client.add_member(
    workspace_id="workspace_id",
    email="newuser@example.com",
    role="editor"
)

# 멤버 역할 업데이트
client.update_member(
    member_id="member_id",
    role="admin"
)

# 멤버 제거
client.remove_member(member_id="member_id")
```

### 파일 관리

```python
# 파일 업로드
uploaded_file = client.upload_file(
    file_path="/path/to/document.pdf",
    filename="문서.pdf"
)
print(f"파일 ID: {uploaded_file['id']}")

# 파일 삭제
client.delete_file(file_id="file_id")
```

## 열 유형

Retable는 다양한 열 유형을 지원합니다:

- **text**: 텍스트
- **number**: 숫자
- **dropdown**: 드롭다운 선택
- **single_select**: 단일 선택
- **multi_select**: 다중 선택
- **date**: 날짜
- **date_time**: 날짜 및 시간
- **checkbox**: 체크박스
- **email**: 이메일
- **phone**: 전화번호
- **url**: URL
- **currency**: 통화
- **percent**: 백분율
- **rating**: 등급
- **formula**: 수식
- **auto_number**: 자동 번호
- **created_at**: 생성일시
- **updated_at**: 수정일시
- **created_by**: 작성자
- **file**: 파일 첨부

## 뷰 유형

- **grid**: 그리드 뷰 (기본)
- **kanban**: 칸반 보드
- **calendar**: 캘린더 뷰
- **timeline**: 타임라인 뷰
- **gallery**: 갤러리 뷰

## 역할 유형

- **owner**: 소유자
- **admin**: 관리자
- **editor**: 편집자
- **commenter**: 댓글 작성자
- **member**: 멤버
- **viewer**: 뷰어

## 주요 기능

- ✅ 워크스페이스 및 프로젝트 관리
- ✅ 테이블 CRUD 작업
- ✅ 열(Column) 관리
- ✅ 행(Row) CRUD 작업
- ✅ 일괄 작업 지원
- ✅ 쿼리 및 필터링
- ✅ 뷰(View) 관리
- ✅ 폼(Form) 생성
- ✅ 팀 멤버 관리
- ✅ 파일 첨부

## 라이선스

MIT License
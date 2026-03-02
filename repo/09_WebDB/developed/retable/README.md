＃RetableコラボレーションスプレッドシートSDK

Retableは、現代のスプレッドシートおよびデータベースコラボレーションプラットフォーム用のPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [Retable.io](https://retable.io)에 にアクセスしてアカウントを作成します。
2. プロファイル設定 (Settings) > API Keys セクションに移動します。
3. 新しい API キーを生成します。
4. 生成された API キーを安全な場所に保存します。

##使用法

### クライアントの初期化

```python
from retable import RetableClient

client = RetableClient(
    api_key="your_api_key_here"
)
```

### ワークスペース管理

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

###プロジェクト管理

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

### テーブル管理

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

### 列(Column)の管理

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

### 行(Row)管理

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

### バッチジョブ

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

###クエリとフィルタリング

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

### ビュー(View)の管理

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

### フォーム(Form)の管理

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

###メンバーの管理

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

###ファイル管理

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

##列タイプ

Retableはさまざまな列タイプをサポートしています。

- **text**: テキスト
- **number**: 数字
- **dropdown**: ドロップダウン選択
- **single_select**: 単一選択
- **multi_select**：複数選択
- **date**: 日付
- **date_time**: 日時
- **checkbox**: チェックボックス
- **email**: メール
- **phone**: 電話番号
- **url**: URL
- **currency**: 通貨
- **percent**: パーセント
- **rating**: 評価
- **formula**: 式
- **auto_number**: 自動番号
- **created_at**：作成日時
- **updated_at**：編集日時
- **created_by**: 作成者
- **file**: ファイル添付

## ビュータイプ

- **grid**: グリッドビュー(基本)
- **kanban**: カンバンボード
- **calendar**: カレンダービュー
- **timeline**: タイムラインビュー
- **gallery**: ギャラリービュー

##ロールタイプ

- **owner**: 所有者
- **admin**: 管理者
- **editor**: 編集者
- **commenter**: コメント作成者
- **member**: メンバー
- **viewer**: ビューア

##主な機能

- ✅ワークスペースとプロジェクト管理
- ✅テーブルCRUD操作
- ✅列(Column)管理
- ✅行（Row）CRUD操作
- ✅バッチジョブのサポート
- ✅クエリとフィルタリング
- ✅ ビュー(View)管理
- ✅ フォーム(Form)の生成
- ✅チームメンバー管理
- ✅ファイル添付

##ライセンス

MIT License
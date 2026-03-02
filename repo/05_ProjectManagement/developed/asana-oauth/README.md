#Asana OAuth APIクライアント

Asana OAuth用のPython APIクライアント。プロジェクトとタスク管理機能を提供します。

## 概要

Asanaはプロジェクト管理とコラボレーションプラットフォームです。このクライアントは、OAuth認証を介してAsana APIにアクセスします。

## インストール

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## OAuthアクセストークン発行

1. [Asana Developers](https://developers.asana.com/)에서アプリ登録
2. OAuth 2.0フローによるアクセストークンの発行
3. 発行されたトークンを安全に保存

##使用法

### 初期化

```python
from asana_oauth import AsanaOAuthClient, AsanaOAuthError

client = AsanaOAuthClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
```

### ワークスペースの検索

```python
workspaces = client.get_workspaces()
```

###チーム検索

```python
teams = client.get_teams(workspace_id="123456789")
```

###プロジェクトの照会

```python
# 모든 프로젝트
projects = client.get_projects()

# 특정 워크스페이스
projects = client.get_projects(workspace="123456789")

# 특정 팀
projects = client.get_projects(team="987654321")
```

###プロジェクトの作成

```python
project = client.create_project(
    workspace="123456789",
    name="My Project",
    team="987654321"
)
```

### ジョブの照会

```python
# 프로젝트의 작업
tasks = client.get_tasks(project="project_id")

# 특정 사용자의 작업
tasks = client.get_tasks(assignee="user_id")

# 완료된 작업
tasks = client.get_tasks(completed=True)
```

### ジョブの作成

```python
task = client.create_task(
    workspace="123456789",
    name="New Task",
    project="project_id",
    assignee="user_id",
    due_on="2024-12-31"
)
```

### ジョブ完了

```python
task = client.complete_task("task_id")
```

### ジョブの更新

```python
task = client.update_task(
    "task_id",
    name="Updated Name",
    notes="Updated notes",
    due_on="2024-12-31"
)
```

###セクション管理

```python
# 섹션 조회
sections = client.get_sections("project_id")

# 섹션 생성
section = client.create_section("project_id", "To Do")

# 작업을 섹션에 추가
result = client.add_task_to_section("section_id", "task_id")
```

### ユーザー管理

```python
# 워크스페이스 사용자
users = client.get_users("workspace_id")

# 사용자 정보
user = client.get_user("user_id")
```

###コメントを追加

```python
comment = client.add_comment_to_task("task_id", "This is a comment")
```

###ジョブ検索

```python
results = client.search_tasks(
    query="important",
    workspace="workspace_id"
)
```

### ファイルの添付

```python
attachment = client.attach_file_to_task("task_id", "document.pdf")
```

## エラー処理

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

##ライセンス

MIT License

## サポート

- [Asana Developers](https://developers.asana.com/)
- [APIドキュメント]（https://developers.asana.com/docs)
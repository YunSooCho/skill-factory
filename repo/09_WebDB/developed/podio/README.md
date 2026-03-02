#Podio WebデータベースSDK

Podioは、柔軟なWebデータベースとコラボレーションプラットフォーム用のPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [Podio開発者ポータル]（https://developers.podio.com/)에にアクセスします。
2. 「API Keys」セクションで新しいアプリケーションを作成します。
3. Client IDとClient Secretを発行します。
4. OAuth認証用にユーザー名とパスワードを準備します。

##使用法

### クライアントの初期化

```python
from podio import PodioClient

client = PodioClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    username="your_email@example.com",
    password="your_password"
)
```

###ゾーンとアプリの管理

```python
# 모든 영역(워크스페이스) 목록
workspaces = client.get_workspaces()
for ws in workspaces:
    print(f"워크스페이스 ID: {ws['space_id']}, 이름: {ws['name']}")

# 영역 상세 정보
workspace = client.get_workspace(space_id=12345)

# 영역 내 앱 목록
apps = client.get_workspace_apps(space_id=12345)
for app in apps:
    print(f"앱 ID: {app['app_id']}, 이름: {app['config']['name']}")

# 앱 검색
apps = client.search_apps(query="프로젝트")

# 앱 상세 정보
app = client.get_app(app_id=12345)
print(f"앱 이름: {app['config']['name']}")

# 앱 필드 목록
fields = client.get_app_fields(app_id=12345)
for field in fields:
    print(f"필드 ID: {field['field_id']}, 유형: {field['type']}")

# 앱 아이템 목록
items = client.get_app_items(
    app_id=12345,
    limit=50,
    sort_by="created_on"
)
```

### アイテム管理

```python
# 아이템 필터링
filtered_items = client.filter_items(
    app_id=12345,
    filters={
        "filters": [
            {
                "key": "status",
                "values": ["진행 중"]
            }
        ]
    },
    limit=20
)

# 아이템 상세 정보
item = client.get_item(item_id=45678)
print(f"아이템 제목: {item['title']}")

# 아이템 생성
new_item = client.add_item(
    app_id=12345,
    fields={
        "title": "새 프로젝트",
        "status": "계획 중",
        "deadline": "2024-12-31",
        "priority": "높음"
    },
    external_id="project-001"
)

# 아이템 수정
client.update_item(
    item_id=45678,
    fields={
        "status": "진행 중",
        "progress": 50
    }
)

# 아이템 복제
cloned_item = client.clone_item(
    item_id=45678
)

# 아이템 삭제
client.delete_item(item_id=45678)
```

### コメントの管理

```python
# 아이템 댓글 목록
comments = client.get_item_comments(item_id=45678)
for comment in comments:
    print(f"댓글: {comment['value']}")

# 댓글 상세 정보
comment = client.get_comment(comment_id=78901)

# 댓글 추가
new_comment = client.add_comment(
    item_id=45678,
    text="이 작업이 완료되었습니다.",
    file_ids=[123, 456]  # 첨부 파일 ID (선택사항)
)

# 댓글 수정
client.update_comment(
    comment_id=78901,
    text="업데이트된 댓글 내용"
)

# 댓글 삭제
client.delete_comment(comment_id=78901)
```

### タスク(Task)の管理

```python
# 작업 목록 조회
tasks = client.get_tasks(space_id=12345)
for task in tasks:
    print(f"작업: {task['text']}, 마감일: {task.get('due_date')}")

# 작업 상세 정보
task = client.get_task(task_id=11111)

# 작업 생성
new_task = client.create_task(
    text="보고서 작성",
    description="분기 보고서 작성 및 검토",
    due_date="2024-12-25",
    responsible=22222,  # 담당자 사용자 ID
    private=False,
    space_id=12345
)

# 작업 수정
client.update_task(
    task_id=11111,
    text="보고서 작성 (수정)",
    status="active",
    due_date="2024-12-28"
)

# 작업 할당
client.assign_task(
    task_id=11111,
    user_id=33333,
    text="이 작업을 처리해주세요"
)

# 작업 완료 표시
client.complete_task(task_id=11111)

# 작업 미완료 표시
client.incomplete_task(task_id=11111)

# 작업 삭제
client.delete_task(task_id=11111)

# 작업 레이블 생성
label = client.create_task_label(
    task_id=11111,
    text="긴급",
    color="#FF0000"
)
```

###組織とユーザーの管理

```python
# 모든 조직 목록
organizations = client.get_organizations()
for org in organizations:
    print(f"조직 ID: {org['org_id']}, 이름: {org['name']}")

# 조직 상세 정보
org = client.get_organization(org_id=44444)

# 사용자 정보 조회
user = client.get_user(user_id=55555)

# 현재 사용자 정보
current_user = client.get_current_user()
print(f"현재 사용자: {current_user['profile']['name']}")
```

###関係管理

```python
# 관련 아이템 조회
related_items = client.get_relationships(
    app_id=12345,
    item_id=45678,
    field_id=66666
)
```

###アクティビティストリーム

```python
# 객체 활동 스트림 조회
activities = client.get_activity_stream(
    object_type="item",
    object_id=45678,
    limit=20
)

for activity in activities:
    print(f"날짜: {activity['created_on']}")
    print(f"작업: {activity['text']}")
```

##主な機能

- ✅ゾーンとアプリの管理
- ✅アイテムCRUDの操作とフィルタリング
- ✅コメント管理
- ✅タスク（Task）の作成、割り当て、完了
- ✅ ラベル管理
- ✅ユーザーと組織の管理
- ✅アクティビティストリーム追跡
- ✅関係と参照管理
- ✅ファイル添付サポート

##認証

Podio は OAuth 2.0 認証を使用します。クライアントは自動的にアクセストークンを管理し、有効期限が切れると更新します。

##ライセンス

MIT License
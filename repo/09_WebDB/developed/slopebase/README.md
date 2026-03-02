#SlopebaseデータベースSDK

Slopebaseは、最新のデータベース管理プラットフォーム用のPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [Slopebase](https://slopebase.com)에 にアクセスしてアカウントを作成します。
2. 「設定」(Settings) > API Keys セクションに移動します。
3. 新しい API キーを生成します。
4. 生成された API キーを安全な場所に保存します。

##使用法

### クライアントの初期化

```python
from slopebase import SlopebaseClient

client = SlopebaseClient(
    api_key="your_api_key_here"
)
```

### データベース管理

```python
# 모든 데이터베이스 목록
databases = client.get_databases()
for db in databases:
    print(f"데이터베이스 ID: {db['id']}, 이름: {db['name']}")

# 데이터베이스 상세 정보
db = client.get_database(database_id="database_id")

# 데이터베이스 생성
new_db = client.create_database(
    name="프로젝트 데이터",
    description="프로젝트 관리용 데이터베이스"
)

# 데이터베이스 업데이트
client.update_database(
    database_id="database_id",
    name="프로젝트 데이터 (수정)"
)

# 데이터베이스 삭제
client.delete_database(database_id="database_id")
```

### テーブル管理

```python
# 데이터베이스 내 테이블 목록
tables = client.get_tables(database_id="database_id")
for table in tables:
    print(f"테이블 ID: {table['id']}, 이름: {table['name']}")

# 테이블 상세 정보
table = client.get_table(table_id="table_id")

# 테이블 생성
new_table = client.create_table(
    database_id="database_id",
    name="고객",
    schema=[
        {"name": "name", "type": "text", "required": True},
        {"name": "email", "type": "text", "unique": True},
        {"name": "age", "type": "integer"},
        {"name": "created_at", "type": "timestamp"}
    ]
)

# 테이블 삭제
client.delete_table(table_id="table_id")
```

### レコード管理

```python
# 레코드 목록 조회
records = client.get_records(
    table_id="table_id",
    limit=100,
    offset=0
)

for record in records['records']:
    print(f"레코드 ID: {record['id']}, 데이터: {record['data']}")

# 특정 레코드 조회
record = client.get_record(table_id="table_id", record_id="record_id")

# 레코드 생성
new_record = client.create_record(
    table_id="table_id",
    data={
        "name": "홍길동",
        "email": "hong@example.com",
        "age": 30
    }
)

# 레코드 업데이트
client.update_record(
    table_id="table_id",
    record_id="record_id",
    data={"age": 31, "name": "홍길동 (수정)"}
)

# 레코드 삭제
client.delete_record(table_id="table_id", record_id="record_id")
```

### クエリとバッチ処理

```python
# 레코드 쿼리
filtered_records = client.query_records(
    table_id="table_id",
    query={
        "filters": [
            {"field": "age", "operator": "greater_than", "value": 25},
            {"field": "email", "operator": "contains", "value": "example"}
        ],
        "sort": [{"field": "created_at", "direction": "desc"}]
    },
    limit=50
)

# 일괄 레코드 생성
batch_result = client.batch_create_records(
    table_id="table_id",
    records=[
        {"name": "철수", "age": 25, "email": "ch@example.com"},
        {"name": "영희", "age": 28, "email": "ye@example.com"}
    ]
)

# 일괄 레코드 업데이트
client.batch_update_records(
    updates=[
        {"record_id": "id1", "data": {"age": 26}},
        {"record_id": "id2", "data": {"age": 29}}
    ]
)

# 일괄 레코드 삭제
client.batch_delete_records(["id1", "id2", "id3"])
```

### ユーザー管理

```python
# 모든 사용자 목록
users = client.get_users()
for user in users:
    print(f"사용자: {user['name']}, 이메일: {user['email']}, 역할: {user['role']}")

# 사용자 생성
new_user = client.create_user(
    email="newuser@example.com",
    name="새 사용자",
    role="editor"
)

# 사용자 업데이트
client.update_user(
    user_id="user_id",
    role="admin"
)

# 사용자 삭제
client.delete_user(user_id="user_id")
```

##主な機能

- ✅データベースCRUD操作
- ✅テーブル作成とスキーマ管理
- ✅レコードCRUD操作
- ✅クエリとフィルタリング
- ✅バッチジョブのサポート
- ✅ユーザー管理

##ライセンス

MIT License
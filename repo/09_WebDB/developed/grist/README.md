＃GristスプレッドシートデータベースSDK

Gristは、スプレッドシートとデータベースの利点を組み合わせたプラットフォーム用のPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [Grist ウェブサイト](https://www.getgrist.com)에 にアクセスしてアカウントを作成します。
2. 右上のプロファイルアイコン > Account Settings をクリックします。
3. API Keysセクションで、[Create API Key]ボタンをクリックします。
4. API キーの名前を入力して生成します。
5. 生成された API キーを安全な場所に保存します。

##使用法

### クライアントの初期化

```python
from grist import GristClient

client = GristClient(
    api_key="your_api_key_here",
    base_url="https://docs.getgrist.com/api"
)
```

### 文書管理

```python
# 모든 문서 목록
docs = client.list_docs()
for doc in docs:
    print(f"문서 ID: {doc['id']}, 이름: {doc['name']}")

# 새 문서 생성
new_doc = client.create_doc(
    name="프로젝트 관리",
    is_workspace=False
)
print(f"생성된 문서 ID: {new_doc['id']}")

# 문서 상세 정보
details = client.get_doc(doc_id="new_doc_id")
print(f"문서 정보: {details}")

# 문서 이름 수정
client.update_doc(doc_id="doc_id", name="프로젝트 관리 2024")

# 문서 삭제
client.delete_doc(doc_id="doc_id")
```

### テーブル管理

```python
# 테이블 목록
tables = client.list_tables(doc_id="doc_id")
for table in tables:
    print(f"테이블 ID: {table['id']}, 이름: {table['name']}")

# 새 테이블 생성
columns = [
    {'id': 'name', 'type': 'Text'},
    {'id': 'age', 'type': 'Numeric'},
    {'id': 'email', 'type': 'Text', 'isFormula': False}
]
client.create_table(
    doc_id="doc_id",
    table_id="Employees",
    columns=columns
)
```

### レコード管理

```python
# 레코드 생성
record = client.create_record(
    doc_id="doc_id",
    table_id="Employees",
    fields={
        'name': '홍길동',
        'age': 30,
        'email': 'hong@example.com'
    }
)
print(f"생성된 레코드 ID: {record['id']}")

# 레코드 조회
record = client.get_record(
    doc_id="doc_id",
    table_id="Employees",
    record_id=1
)
print(f"레코드: {record}")

# 레코드 목록 조회
records = client.list_records(
    doc_id="doc_id",
    table_id="Employees",
    limit=50
)
for record in records:
    print(f"{record['id']}: {record['fields']}")

# 필터를 사용한 레코드 검색
filtered = client.list_records(
    doc_id="doc_id",
    table_id="Employees",
    filter={'ages': {'operator': '>', 'value': 25}}
)

# 정렬
sorted_records = client.list_records(
    doc_id="doc_id",
    table_id="Employees",
    sort=[{'field': 'age', 'order': 'desc'}]
)

# 레코드 업데이트
updated = client.update_record(
    doc_id="doc_id",
    table_id="Employees",
    record_id=1,
    fields={
        'age': 31,
        'email': 'newemail@example.com'
    }
)

# 레코드 삭제
client.delete_record(
    doc_id="doc_id",
    table_id="Employees",
    record_id=1
)
```

### バッチジョブ

```python
# 여러 레코드 생성
new_records = [
    {'fields': {'name': '김철수', 'age': 28, 'email': 'kim@example.com'}},
    {'fields': {'name': '이영희', 'age': 32, 'email': 'lee@example.com'}},
    {'fields': {'name': '박민수', 'age': 27, 'email': 'park@example.com'}}
]

result = client.create_records(
    doc_id="doc_id",
    table_id="Employees",
    records=new_records
)
print(f"생성된 레코드 수: {len(result)}")

# 여러 레코드 업데이트
updates = [
    {'id': 1, 'fields': {'age': 29}},
    {'id': 2, 'fields': {'age': 33}}
]

client.update_records(
    doc_id="doc_id",
    table_id="Employees",
    records=updates
)

# 여러 레코드 삭제
client.delete_records(
    doc_id="doc_id",
    table_id="Employees",
    record_ids=[1, 2, 3]
)
```

### 列管理

```python
# 컬럼 정보 조회
columns = client.get_columns(
    doc_id="doc_id",
    table_id="Employees"
)
for col in columns:
    print(f"컬럼 ID: {col['id']}, 타입: {col['type']}")

# 새 컬럼 추가
client.add_column(
    doc_id="doc_id",
    table_id="Employees",
    col_id="department",
    type="Text"
)

# 수식 컬럼 추가
client.add_column(
    doc_id="doc_id",
    table_id="Employees",
    col_id="baseSalary",
    type="Numeric",
    formula="age * 100000"
)
```

###クエリと検索

```python
# 고급 쿼리
results = client.query(
    doc_id="doc_id",
    table_id="Employees",
    filter_str="$age > 30",
    sort="$age",
    limit=20
)

for record in results:
    print(f"{record['fields']['name']}: {record['fields']['age']}")
```

### アクセス権の管理

```python
# 접근 권한 조회
permissions = client.get_access_permissions(doc_id="doc_id")

# 접근 권한 설정
client.set_access_permissions(
    doc_id="doc_id",
    users=[
        {'email': 'user1@example.com', 'access': 'Owners'},
        {'email': 'user2@example.com', 'access': 'Editors'}
    ]
)
```

### ユーザー情報

```python
# 현재 사용자 프로필
profile = client.get_user_profile()
print(f"사용자명: {profile['name']}")
print(f"이메일: {profile['email']}")
```

##主な機能

- ✅文書の作成、照会、修正、削除
- ✅テーブルと列の管理
- ✅レコードCRUD操作（シングルとバッチ）
- ✅フィルタリングとソート
- ✅数式列のサポート
- ✅アクセス権の管理
- ✅高度なクエリ機能
- ✅リアルタイムデータ同期

##ライセンス

MIT License
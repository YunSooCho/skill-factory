# QuintaDB データベース SDK

QuintaDBは、強力なオンラインデータベースとフォームプラットフォーム用のPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [QuintaDB](https://quintadb.com)에 にアクセスしてアカウントを作成します。
2. 「設定」(Settings) > API Keys セクションに移動します。
3. 新しい API トークンを生成します。
4. 生成された API トークンを安全な場所に保存します。

##使用法

### クライアントの初期化

```python
from quintadb import QuintaDBClient

client = QuintaDBClient(
    api_token="your_api_token_here"
)
```

### データベース管理

```python
# 모든 데이터베이스 목록
databases = client.get_databases()
for db in databases['databases']:
    print(f"데이터베이스 ID: {db['id']}, 이름: {db['name']}")

# 데이터베이스 상세 정보
db = client.get_database(database_id=12345)
print(f"이름: {db['name']}, 설명: {db['description']}")

# 데이터베이스 내 테이블 목록
tables = client.get_database_tables(database_id=12345)
for table in tables['tables']:
    print(f"테이블 ID: {table['id']}, 이름: {table['name']}")

# 데이터베이스 통계
stats = client.get_database_statistics(database_id=12345)
print(f"테이블 수: {stats['tables_count']}")
```

### テーブル管理

```python
# 테이블 상세 정보
table = client.get_table(table_id=67890)

# 테이블 내 필드 목록
fields = client.get_table_fields(table_id=67890)
for field in fields['fields']:
    print(f"필드 ID: {field['id']}, 유형: {field['type']}, 이름: {field['label']}")

# 테이블 통계
stats = client.get_table_statistics(table_id=67890)
print(f"레코드 수: {stats['records_count']}")
```

### フィールド管理

```python
# 필드 상세 정보
field = client.get_field(field_id=11111)

# 필드 생성
new_field = client.create_field(
    table_id=67890,
    type="text",
    label="제목",
    position=1,
    required=True
)

# 드롭다운 필드 생성
dropdown_field = client.create_field(
    table_id=67890,
    type="dropdown",
    label="상태",
    position=2,
    options="진행 중,완료,보류"
)

# 필드 업데이트
client.update_field(
    field_id=11111,
    label="작업 제목",
    required=True
)

# 필드 삭제
client.delete_field(field_id=11111)
```

### レコード管理

```python
# 레코드 목록 조회
records = client.get_records(
    table_id=67890,
    per_page=100,
    page=1
)

for record in records['records']:
    print(f"레코드 ID: {record['id']}")

# 특정 레코드 조회
record = client.get_record(record_id=22222, table_id=67890)

# 레코드 생성
new_record = client.create_record(
    table_id=67890,
    record={
        'field_11111': '새 작업 제목',
        'field_22222': '2024-12-25',
        'field_33333': '진행 중'
    }
)

# 레코드 업데이트
client.update_record(
    record_id=22222,
    table_id=67890,
    record={
        'field_33333': '완료',
        'field_44444': '설명 업데이트'
    }
)

# 레코드 삭제
client.delete_record(record_id=22222, table_id=67890)

# 레코드 수 조회
count = client.get_count(table_id=67890)
print(f"총 레코드: {count['count']}")
```

### レコードのフィルタリングと検索

```python
# 레코드 필터링
filtered_records = client.filter_records(
    table_id=67890,
    query="field_33333 = '진행 중'",
    per_page=50
)

# 레코드 검색
search_results = client.search_records(
    table_id=67890,
    query="긴급",
    per_page=50
)
```

### ビュー(View)の管理

```python
# 테이블 뷰 목록
views = client.get_views(table_id=67890)
for view in views['views']:
    print(f"뷰 ID: {view['id']}, 이름: {view['name']}")

# 뷰 상세 정보
view = client.get_view(view_id=33333)

# 뷰에서 레코드 조회
view_records = client.get_view_records(
    table_id=67890,
    view_id=33333,
    per_page=100
)

# 뷰 생성
new_view = client.create_view(
    table_id=67890,
    name="긴급 작업",
    view_type="table",
    column_ids="11111,22222,33333",
    conditions="field_33333 = '진행 중' AND field_44444 = '높음'"
)

# 뷰 업데이트
client.update_view(
    view_id=33333,
    name="긴급 진행 중 작업",
    conditions="field_33333 = '진행 중'"
)

# 뷰 삭제
client.delete_view(view_id=33333)
```

### フォーム(Form)の管理

```python
# 모든 폼 목록
forms = client.get_forms()
for form in forms['forms']:
    print(f"폼 ID: {form['id']}, 이름: {form['name']}")

# 폼 상세 정보
form = client.get_form(form_id=44444)

# 폼 생성
new_form = client.create_form(
    table_id=67890,
    name="작업 제출 폼",
    description="새 작업을 제출합니다"
)

# 폼 업데이트
client.update_form(
    form_id=44444,
    name="업데이트된 폼",
    description="폼 설명 업데이트"
)

# 폼 삭제
client.delete_form(form_id=44444)
```

### ユーザー管理

```python
# 모든 사용자 목록
users = client.get_users()
for user in users['users']:
    print(f"사용자 ID: {user['id']}, 이름: {user['name']}, 이메일: {user['email']}")

# 사용자 상세 정보
user = client.get_user(user_id=55555)

# 사용자 생성
new_user = client.create_user(
    email="newuser@example.com",
    name="새 사용자",
    role="admin"
)

# 사용자 업데이트
client.update_user(
    user_id=55555,
    name="수정된 이름",
    role="user"
)

# 사용자 삭제
client.delete_user(user_id=55555)
```

###ロール管理

```python
# 모든 역할 목록
roles = client.get_roles()
for role in roles['roles']:
    print(f"역할 ID: {role['id']}, 이름: {role['name']}")

# 역할 상세 정보
role = client.get_role(role_id=66666)
```

###ファイル管理

```python
# 파일 업로드
uploaded_file = client.upload_file(
    file_path="/path/to/document.pdf",
    filename="문서.pdf"
)
print(f"파일 ID: {uploaded_file['file']['id']}")

# 파일 정보 조회
file_info = client.get_file(file_id=77777)

# 파일 삭제
client.delete_file(file_id=77777)
```

### クエリの例

```python
# 정확한 값 일치
query = "field_33333 = '진행 중'"

# 부등호
query = "field_22222 > '2024-01-01'"

# AND 연산
query = "field_33333 = '진행 중' AND field_44444 = '높음'"

# OR 연산
query = "field_33333 = '진행 중' OR field_33333 = '확인 중'"

# 복잡한 쿼리
query = "(field_33333 = '진행 중' OR field_33333 = '확인 중') AND field_44444 = '높음'"
```

## フィールドタイプ

QuintaDBはさまざまなフィールドタイプをサポートしています。

- **text**: テキストフィールド
- **textarea**: 複数行のテキストフィールド
- **dropdown**: ドロップダウンフィールド
- **radio**: ラジオボタン
- **checkbox**: チェックボックス
- **number**: 数値フィールド
- **date**: 日付フィールド
- **date_time**: 日時フィールド
- **currency**: 通貨フィールド
- **email**: メールフィールド
- **url**: URL フィールド
- **phone**：電話番号フィールド
- **file**: ファイルアップロードフィールド
- **image**: イメージフィールド
- **user**: ユーザーフィールド
- **formula**: 数式フィールド

##主な機能

- ✅データベースとテーブルの管理
- ✅フィールドCRUD操作
- ✅レコード管理
- ✅レコードのフィルタリングと検索
- ✅ ビュー(View)の作成と管理
- ✅ フォーム(Form)の作成と管理
- ✅ユーザーと役割の管理
- ✅ファイルのアップロードと管理
- ✅統計と報告

##ライセンス

MIT License
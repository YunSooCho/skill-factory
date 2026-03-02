＃QuickBaseローコードプラットフォームSDK

QuickBaseは、オンデマンドのローコードWebアプリケーションプラットフォーム用のPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [QuickBase]（https://www.quickbase.com/)에にアクセスしてアカウントにログインします。
2. 「設定」(Home) > 「My Preferences」 > 「User Token」セクションに移動します。
3. User Token を作成します（アクセス権を設定します）。
4. QuickBase Realm Hostname（例：mycompany.quickbase.com）を確認します。

##使用法

### クライアントの初期化

```python
from quickbase import QuickBaseClient

client = QuickBaseClient(
    user_token="your_user_token_here",
    realm_hostname="yourcompany.quickbase.com"
)
```

###アプリ管理

```python
# 모든 앱 목록
apps = client.get_apps()
for app in apps:
    print(f"앱 ID: {app['id']}, 이름: {app['name']}")

# 앱 상세 정보
app = client.get_app(app_id="app_id")

# 앱 생성
new_app = client.create_app(
    name="프로젝트 관리",
    description="프로젝트 추적 시스템"
)

# 앱 업데이트
client.update_app(
    app_id="app_id",
    name="프로젝트 관리 (업데이트)",
    description="향상된 프로젝트 추적 시스템"
)

# 앱 삭제
client.delete_app(app_id="app_id")
```

### テーブル管理

```python
# 앱 내 테이블 목록
tables = client.get_tables(app_id="app_id")
for table in tables:
    print(f"테이블 ID: {table['id']}, 이름: {table['name']}")

# 테이블 상세 정보
table = client.get_table(table_id="table_id", app_id="app_id")

# 테이블 생성
new_table = client.create_table(
    app_id="app_id",
    name="작업",
    description="프로젝트 작업",
    singleton=False
)

# 테이블 업데이트
client.update_table(
    table_id="table_id",
    app_id="app_id",
    name="작업 항목",
    description="개별 작업 항목"
)

# 테이블 삭제
client.delete_table(table_id="table_id", app_id="app_id")
```

### フィールド管理

```python
# 테이블 내 필드 목록
fields = client.get_fields(table_id="table_id")
for field in fields:
    print(f"필드 ID: {field['id']}, 유형: {field['type']}, 라벨: {field['label']}")

# 필드 상세 정보
field = client.get_field(field_id="field_id", table_id="table_id")

# 필드 생성
new_field = client.create_field(
    table_id="table_id",
    type="text",
    label="작업 제목",
    description="작업의 제목",
    required=True,
    field_help="명확하고 간결한 제목을 입력하세요"
)

# 필드 업데이트
client.update_field(
    field_id="field_id",
    table_id="table_id",
    label="작업 제목 (수정)",
    required=True
)

# 필드 삭제
client.delete_field(field_id="field_id", table_id="table_id")
```

### レコード管理

```python
# 레코드 조회
records = client.get_records(
    table_id="table_id",
    fields=["6", "7", "8"],  # 필드 ID들
    skip=0,
    top=100
)

for record in records['data']:
    print(f"레코드 ID: {record['6']['value']}")

# 특정 필드만 조회
records = client.get_records(
    table_id="table_id",
    fields=["6", "15"],
    where="'15'='진행 중'"
)

# 정렬하여 조회
records = client.get_records(
    table_id="table_id",
    sort_by=["8-ASC", "12-DESC"]
)

# 단일 레코드 조회
record = client.get_record(record_id="rid", table_id="table_id")

# 레코드 생성
new_record = client.add_record(
    table_id="table_id",
    data={
        "7": {"value": "새 작업 제목"},
        "8": {"value": "2024-12-25"},
        "12": {"value": "높음"}
    },
    fields_to_return=["6", "7", "8"]
)

# 레코드 업데이트
client.update_record(
    record_id="rid",
    table_id="table_id",
    data={
        "7": {"value": "수정된 제목"},
        "12": {"value": "긴급"}
    }
)

# 여러 레코드 일괄 업데이트
client.update_records(
    table_id="table_id",
    records=[
        {
            "6": {"value": "rid1"},
            "12": {"value": "완료"}
        },
        {
            "6": {"value": "rid2"},
            "12": {"value": "완료"}
        }
    ]
)

# 레코드 삭제
client.delete_record(record_id="rid", table_id="table_id")

# 여러 레코드 일괄 삭제
client.delete_records(
    table_id="table_id",
    record_ids=["rid1", "rid2", "rid3"]
)
```

###クエリとフィルタリング

```python
# WHERE 쿼리
results = client.query(
    table_id="table_id",
    where="'15'='진행 중' AND '12'='높음'",
    select=["6", "7", "8"],
    top=50
)

# 복잡한 쿼리
results = client.query(
    table_id="table_id",
    where="'8' < '2024-01-01' OR '12'='긴급'",
    skip=0,
    top=100
)
```

### レポート管理

```python
# 테이블 리포트 목록
reports = client.get_reports(table_id="table_id")
for report in reports:
    print(f"리포트 ID: {report['id']}, 이름: {report['name']}")

# 리포트 실행
report_data = client.run_report(
    table_id="table_id",
    report_id="report_id",
    skip=0,
    top=50
)

for record in report_data['data']:
    print(f"데이터: {record}")
```

### ユーザー管理

```python
# 앱 사용자 목록
users = client.get_users(app_id="app_id")
for user in users:
    print(f"사용자: {user['email']}")

# 사용자 상세 정보
user = client.get_user(user_id="user_id", app_id="app_id")

# 사용자 초대
invitation = client.invite_user(
    email="newuser@example.com",
    app_id="app_id",
    role_id="role_id"
)

# 현재 사용자 정보
current_user = client.get_current_user()
print(f"이메일: {current_user['email']}")
```

### 役割の管理

```python
# 앱 역할 목록
roles = client.get_roles(app_id="app_id")
for role in roles:
    print(f"역할 ID: {role['id']}, 이름: {role['name']}")
```

### フォーム管理

```python
# 폼 생성
new_form = client.create_form(
    table_id="table_id",
    name="빠른 입력 폼",
    description="빠른 작업 입력을 위한 폼"
)

# 테이블 폼 목록
forms = client.get_forms(table_id="table_id")
for form in forms:
    print(f"폼 ID: {form['id']}, 이름: {form['name']}")
```

## フィールドタイプ

QuickBaseはさまざまなフィールドタイプをサポートしています。

- **text**: テキストフィールド
- **rich-text**: リッチテキストフィールド
- **numeric**: 数値フィールド
- **currency**: 通貨フィールド
- **percent**: パーセントフィールド
- **date**: 日付フィールド
- **date-time**: 日時フィールド
- **checkbox**: チェックボックスフィールド
- **phone**：電話番号フィールド
- **email**: メールフィールド
- **url**: URL フィールド
- **user**: ユーザーフィールド
- **file**: ファイル添付フィールド
- **multi-select-text**: 複数選択テキストフィールド
- **record-id**：レコードIDフィールド（主にフィールド6）

## クエリ文法の例

```python
# 정확한 값 일치
where="'15'='진행 중'"

# 부등호
where="'8' >= '2024-01-01'"
where="'12' <= '50'"

# AND 연산
where="'15'='진행 중' AND '12'='높음'"

# OR 연산
where="'15'='진행 중' OR '15'='검토 중'"

# NOT 연산
where="NOT ('15'='완료')"

# 괄호 사용
where="('15'='진행 중' OR '15'='검토 중') AND '12'='높음'"

# NULL 체크
where="'20' is null"
where="'20' is not null"
```

##主な機能

- ✅アプリケーションCRUD操作
- ✅テーブル管理
- ✅フィールドの作成と修正
- ✅レコードの挿入、更新、削除
- ✅クエリとフィルタリング
- ✅レポートの実行
- ✅ユーザーと役割の管理
- ✅フォーム管理
- ✅バッチジョブのサポート

##ライセンス

MIT License
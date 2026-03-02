# Zoho Creator ローコードプラットフォーム SDK

Zoho Creatorは、Zohoのローコードアプリケーション開発プラットフォーム用のPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [Zoho Developer Console](https://zoho.com/creator/)에 接続します。
2. 新しいアプリケーションを作成するか、既存のアプリケーションを選択します。
3. Settings > API Settings に移動します。
4. OAuth認証を設定し、クライアントID、クライアント秘密を発行します。
5. アクセストークンを生成します。
6. Account Owner ID（例：123456789）を確認します。
7. アプリケーションのリンク名を確認します。

##使用法

### クライアントの初期化

```python
from zoho_creator import ZohoCreatorClient

client = ZohoCreatorClient(
    auth_token="your_auth_token_here",
    owner="your_owner_id",
    app_link_name="your_app_name"
)
```

### フォーム(Form)の管理

```python
# 모든 폼 목록
forms = client.get_forms()
for form in forms:
    print(f"폼: {form['display_name']} ({form['link_name']})")

# 폼 상세 정보
form = client.get_form(form_link_name="Customer")

# 애플리케이션 설정
settings = client.get_settings()
print(f"설정: {settings}")
```

### レコード管理

```python
# 레코드 목록 조회
records = client.get_records(
    form_link_name="Customer",
    limit=100,
    offset=0
)

for record in records['data']:
    print(f"ID: {record['ID']}, 데이터: {record}")

# 조건으로 레코드 조회
filtered_records = client.get_records(
    form_link_name="Customer",
    criteria="Status == 'Active'"
)

# 특정 레코드 조회
record = client.get_record(
    form_link_name="Customer",
    record_id="123456789"
)

# 레코드 생성
new_record = client.create_record(
    form_link_name="Customer",
    data={
        "Name": "홍길동",
        "Email": "hong@example.com",
        "Phone": "010-1234-5678",
        "Status": "Active"
    }
)

# 레코드 업데이트
updated_record = client.update_record(
    form_link_name="Customer",
    record_id="123456789",
    data={
        "Phone": "010-9876-5432",
        "Status": "Inactive"
    }
)

# 레코드 삭제
client.delete_record(
    form_link_name="Customer",
    record_id="123456789"
)
```

### バッチジョブ

```python
# 일괄 레코드 생성
batch_result = client.batch_create_records(
    form_link_name="Customer",
    records=[
        {"Name": "철수", "Email": "c@example.com", "Status": "Active"},
        {"Name": "영희", "Email": "y@example.com", "Status": "Active"},
        {"Name": "민수", "Email": "m@example.com", "Status": "Active"}
    ]
)

# 일괄 레코드 업데이트
client.batch_update_records(
    form_link_name="Customer",
    updates=[
        {"ID": "id1", "Status": "Inactive"},
        {"ID": "id2", "Status": "Inactive"}
    ]
)

# 일괄 레코드 삭제
client.batch_delete_records(
    form_link_name="Customer",
    record_ids=["id1", "id2", "id3"]
)
```

### フィールド管理

```python
# 폼의 모든 필드 목록
fields = client.get_fields(form_link_name="Customer")
for field in fields:
    print(f"필드: {field['field_name']}, 유형: {field['field_type']}")

# 새 필드 추가
new_field = client.add_field(
    form_link_name="Customer",
    field_name="Company",
    field_type="text",
    options={"required": True}
)

# 필드 삭제
client.delete_field(
    form_link_name="Customer",
    field_link_name="Company"
)
```

### レポート管理

```python
# 모든 리포트 목록
reports = client.get_reports()
for report in reports:
    print(f"리포트: {report['display_name']} ({report['link_name']})")

# 리포트 상세 정보
report = client.get_report(report_link_name="All_Customers")

# 리포트 실행
report_data = client.execute_report(
    report_link_name="Active_Customers",
    limit=50,
    criteria="Status == 'Active'"
)

for record in report_data['data']:
    print(f"데이터: {record}")
```

###検索

```python
# 필드로 검색
search_results = client.search_records(
    form_link_name="Customer",
    search_field="Email",
    search_text="example.com",
    limit=100
)

for result in search_results['data']:
    print(f"결과: {result}")
```

### 関連レコード

```python
# 관련 레코드 조회 (Lookup 관계)
related = client.get_related_records(
    form_link_name="Order",
    record_id="order_id",
    related_form_link_name="Customer"
)
```

### コメントの管理

```python
# 레코드에 댓글 추가
client.add_comment(
    form_link_name="Customer",
    record_id="record_id",
    comment="이 고객을 검토해주세요"
)

# 레코드의 모든 댓글 조회
comments = client.get_comments(
    form_link_name="Customer",
    record_id="record_id"
)

for comment in comments:
    print(f"댓글: {comment['content']}, 작성자: {comment['added_by']}")
```

###ファイル管理

```python
# 파일 업로드
uploaded_file = client.upload_file(
    form_link_name="Customer",
    record_id="record_id",
    field_name="Profile_Image",
    file_path="/path/to/image.jpg"
)

# 파일 다운로드
file_info = client.download_file(
    form_link_name="Customer",
    record_id="record_id",
    field_name="Profile_Image"
)
```

### ワークフロー

```python
# 커스텀 워크플로우 트리거
result = client.trigger_workflow(
    form_link_name="Customer",
    workflow_name="Send_Welcome_Email",
    record_id="record_id"
)

# 레코드 없이 트리거
result = client.trigger_workflow(
    form_link_name="Customer",
    workflow_name="Daily_Report_Generation"
)
```

###統計

```python
# 폼 통계
stats = client.get_statistics(form_link_name="Customer")
print(f"총 레코드: {stats['total_records']}")
print(f"오늘 추가된 레코드: {stats['records_added_today']}")

# 페이지 목록
pages = client.get_pages()
for page in pages:
    print(f"페이지: {page['title']} ({page['link_name']})")
```

## フィールドタイプの例

- **text**: テキスト
- **multiline**: 複数行テキスト
- **number**: 数字
- **currency**: 通貨
- **email**: メール
- **phone**: 電話番号
- **date**: 日付
- **datetime**: 日時
- **boolean**: ブール (true/false)
- **file**: ファイルのアップロード
- **image**: イメージ
- **lookup**: 照会フィールド
- **dropdown**: ドロップダウン
- **radio**: ラジオボタン
- **checkbox**: チェックボックス
- **multiselect**: 複数選択
- **url**: URL
- **formula**: 式

＃＃クエリ条件（Criteria）の例

```python
# 단일 조건
criteria = "Status == 'Active'"

# 여러 조건 (AND)
criteria = "Status == 'Active' && City == '서울'"

# 여러 조건 (OR)
criteria = "Status == 'Active' || Status == 'Pending'"

# 비교 연산자
criteria = "Age > 18"
criteria = "Created_Date == '2024-01-01'"
criteria = "Name starts_with '홍'"
criteria = "Email contains '@'"
```

##主な機能

- ✅フォーム（フォーム）とレコード管理
- ✅ CRUD操作
- ✅バッチジョブのサポート
- ✅フィールド管理
- ✅レポートの作成と実行
- ✅検索機能
- ✅レコード関係
- ✅コメント機能
- ✅ファイルのアップロード/ダウンロード
- ✅ワークフロートリガ
- ✅統計と分析

##認証

Zoho Creator は OAuth 2.0 認証を使用します。クライアントは発行されたアクセストークンを使用して認証します。

##ライセンス

MIT License
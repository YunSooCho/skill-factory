# QuintaDB 데이터베이스 SDK

QuintaDB는 강력한 온라인 데이터베이스 및 양식 플랫폼에 대한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [QuintaDB](https://quintadb.com)에 접속하여 계정을 생성합니다.
2. 설정(Settings) > API Keys 섹션으로 이동합니다.
3. 새 API 토큰을 생성합니다.
4. 생성된 API 토큰을 안전한 곳에 저장합니다.

## 사용법

### 클라이언트 초기화

```python
from quintadb import QuintaDBClient

client = QuintaDBClient(
    api_token="your_api_token_here"
)
```

### 데이터베이스 관리

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

### 테이블 관리

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

### 필드 관리

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

### 레코드 관리

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

### 레코드 필터링 및 검색

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

### 뷰(View) 관리

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

### 폼(Form) 관리

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

### 사용자 관리

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

### 역할 관리

```python
# 모든 역할 목록
roles = client.get_roles()
for role in roles['roles']:
    print(f"역할 ID: {role['id']}, 이름: {role['name']}")

# 역할 상세 정보
role = client.get_role(role_id=66666)
```

### 파일 관리

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

### 쿼리 예제

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

## 필드 유형

QuintaDB는 다양한 필드 유형을 지원합니다:

- **text**: 텍스트 필드
- **textarea**: 여러 행 텍스트 필드
- **dropdown**: 드롭다운 필드
- **radio**: 라디오 버튼
- **checkbox**: 체크박스
- **number**: 숫자 필드
- **date**: 날짜 필드
- **date_time**: 날짜 및 시간 필드
- **currency**: 통화 필드
- **email**: 이메일 필드
- **url**: URL 필드
- **phone**: 전화번호 필드
- **file**: 파일 업로드 필드
- **image**: 이미지 필드
- **user**: 사용자 필드
- **formula**: 수식 필드

## 주요 기능

- ✅ 데이터베이스 및 테이블 관리
- ✅ 필드 CRUD 작업
- ✅ 레코드 관리
- ✅ 레코드 필터링 및 검색
- ✅ 뷰(View) 생성 및 관리
- ✅ 폼(Form) 생성 및 관리
- ✅ 사용자 및 역할 관리
- ✅ 파일 업로드 및 관리
- ✅ 통계 및 보고

## 라이선스

MIT License
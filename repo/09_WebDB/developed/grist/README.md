# Grist 스프레드시트 데이터베이스 SDK

Grist는 스프레드시트와 데이터베이스의 장점을 결합한 플랫폼에 대한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [Grist 웹사이트](https://www.getgrist.com)에 접속하여 계정을 생성합니다.
2. 우측 상단의 프로필 아이콘 > Account Settings를 클릭합니다.
3. API Keys 섹션에서 'Create API Key' 버튼을 클릭합니다.
4. API 키의 이름을 입력하고 생성합니다.
5. 생성된 API 키를 안전한 곳에 저장합니다.

## 사용법

### 클라이언트 초기화

```python
from grist import GristClient

client = GristClient(
    api_key="your_api_key_here",
    base_url="https://docs.getgrist.com/api"
)
```

### 문서(Document) 관리

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

### 테이블 관리

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

### 레코드 관리

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

### 배치 작업

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

### 컬럼 관리

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

### 쿼리 및 검색

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

### 접근 권한 관리

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

### 사용자 정보

```python
# 현재 사용자 프로필
profile = client.get_user_profile()
print(f"사용자명: {profile['name']}")
print(f"이메일: {profile['email']}")
```

## 주요 기능

- ✅ 문서 생성, 조회, 수정, 삭제
- ✅ 테이블 및 컬럼 관리
- ✅ 레코드 CRUD 작업 (단일 및 배치)
- ✅ 필터링 및 정렬
- ✅ 수식 컬럼 지원
- ✅ 접근 권한 관리
- ✅ 고급 쿼리 기능
- ✅ 실시간 데이터 동기화

## 라이선스

MIT License
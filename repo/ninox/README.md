# Ninox 저코드 데이터베이스 SDK

Ninox는 저코드(low-code)로 데이터베이스를 구축하고 관리할 수 있는 플랫폼에 대한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [Ninox 웹사이트](https://www.ninox.com)에 접속하여 계정을 생성합니다.
2. Settings > API 섹션으로 이동합니다.
3. 'Create API Token' 버튼을 클릭하여 새 API 토큰을 생성합니다.
4. 생성된 토큰을 안전한 곳에 저장합니다.

## 사용법

### 클라이언트 초기화

```python
from ninox import NinoxClient

client = NinoxClient(
    api_key="your_api_token_here"
)
```

### 팀 및 데이터베이스 관리

```python
# 모든 팀 목록
teams = client.list_teams()
for team in teams:
    print(f"팀 ID: {team['id']}, 이름: {team['name']}")

# 팀 상세 정보
team = client.get_team(team_id="team_id")
print(f"팀 정보: {team}")

# 데이터베이스 목록
databases = client.list_databases(team_id="team_id")
for db in databases:
    print(f"데이터베이스 ID: {db['id']}, 이름: {db['name']}")

# 데이터베이스 상세 정보
database = client.get_database(team_id="team_id", database_id="db_id")
print(f"데이터베이스: {database}")

# 데이터베이스 스키마 조회
schema = client.get_schema(team_id="team_id", database_id="db_id")
```

### 테이블 관리

```python
# 테이블 목록
tables = client.list_tables(team_id="team_id", database_id="db_id")
for table in tables:
    print(f"테이블 ID: {table['id']}, 이름: {table['name']}")

# 테이블 상세 정보
table = client.get_table(team_id="team_id", database_id="db_id", table_id="table_id")
```

### 레코드 CRUD 작업

```python
# 레코드 생성
record = client.create_record(
    team_id="team_id",
    database_id="db_id",
    table_id="Customers",
    fields={
        'Name': '홍길동',
        'Email': 'hong@example.com',
        'Phone': '010-1234-5678',
        'City': '서울'
    }
)
print(f"생성된 레코드 ID: {record.get('id')}")

# 레코드 조회
record = client.get_record(
    team_id="team_id",
    database_id="db_id",
    table_id="Customers",
    record_id="record_id"
)
print(f"레코드: {record}")

# 레코드 목록 조회
records = client.list_records(
    team_id="team_id",
    database_id="db_id",
    table_id="Customers",
    limit=50
)
for record in records:
    print(f"{record.get('id')}: {record}")

# 레코드 업데이트
updated = client.update_record(
    team_id="team_id",
    database_id="db_id",
    table_id="Customers",
    record_id="record_id",
    fields={
        'Phone': '010-9876-5432',
        'City': '부산'
    }
)

# 레코드 삭제
client.delete_record(
    team_id="team_id",
    database_id="db_id",
    table_id="Customers",
    record_id="record_id"
)
```

### 정렬 및 페이지네이션

```python
# 정렬된 레코드 목록
sorted_records = client.list_records(
    team_id="team_id",
    database_id="db_id",
    table_id="Customers",
    sort="Name",
    limit=20
)

# 페이지네이션
page1 = client.list_records(
    team_id="team_id",
    database_id="db_id",
    table_id="Customers",
    limit=20,
    offset=0
)

page2 = client.list_records(
    team_id="team_id",
    database_id="db_id",
    table_id="Customers",
    limit=20,
    offset=20
)
```

### 배치 작업

```python
# 여러 레코드 동시 생성
new_records = [
    {'Name': '김철수', 'Email': 'kim@example.com'},
    {'Name': '이영희', 'Email': 'lee@example.com'},
    {'Name': '박민수', 'Email': 'park@example.com'}
]

result = client.create_records(
    team_id="team_id",
    database_id="db_id",
    table_id="Customers",
    records=new_records
)

# 여러 레코드 동시 업데이트
updates = [
    {'id': 'record_id_1', 'Name': '수정된 이름1'},
    {'id': 'record_id_2', 'Name': '수정된 이름2'}
]

client.update_records(
    team_id="team_id",
    database_id="db_id",
    table_id="Customers",
    records=updates
)

# 여러 레코드 동시 삭제
client.delete_records(
    team_id="team_id",
    database_id="db_id",
    table_id="Customers",
    record_ids=['id1', 'id2', 'id3']
)
```

### 쿼리 및 검색

```python
# 쿼리 실행
results = client.query_records(
    team_id="team_id",
    database_id="db_id",
    table_id="Customers",
    query='Name = "홍길동"'
)

# 조건부 쿼리
results = client.query_records(
    team_id="team_id",
    database_id="db_id",
    table_id="Customers",
    query='City = "서울" and Email like "%@example.com"'
)

# 레코드 수 계산
count = client.count_records(
    team_id="team_id",
    database_id="db_id",
    table_id="Customers"
)
print(f"총 레코드 수: {count}")

# 조건부 레코드 수 계산
filtered_count = client.count_records(
    team_id="team_id",
    database_id="db_id",
    table_id="Customers",
    query='City = "서울"'
)
```

### 파일 업로드

```python
# 레코드에 파일 첨부
client.upload_file(
    team_id="team_id",
    database_id="db_id",
    table_id="Documents",
    record_id="record_id",
    field_name="Attachment",
    file_path="/path/to/document.pdf",
    file_name="custom_name.pdf"
)
```

### 관계 설정

```python
# 레코드 간 관계 설정
client.create_relationship(
    team_id="team_id",
    database_id="db_id",
    table_id="Orders",
    record_id="order_id",
    relation_field="Customer",
    related_record_id="customer_id"
)
```

### 웹훅 관리

```python
# 웹훅 생성
webhook = client.create_webhook(
    team_id="team_id",
    database_id="db_id",
    table_id="Customers",
    webhook_url="https://your-server.com/webhook",
    events=["create", "update", "delete"],
    active=True
)

# 웹훅 목록
webhooks = client.list_webhooks(team_id="team_id", database_id="db_id")

# 웹훅 삭제
client.delete_webhook(
    team_id="team_id",
    database_id="db_id",
    webhook_id="webhook_id"
)
```

### 사용자 정보

```python
# 현재 사용자 정보
user_info = client.get_user_info()
print(f"사용자: {user_info['name']}")
```

## 주요 기능

- ✅ 팀 및 데이터베이스 관리
- ✅ 테이블 및 스키마 조회
- ✅ 레코드 CRUD 작업 (단일 및 배치)
- ✅ 고급 쿼리 기능
- ✅ 파일 업로드 및 관리
- ✅ 테이블 간 관계 설정
- ✅ 웹훅 지원
- ✅ 정렬 및 페이지네이션
- ✅ 실시간 데이터 동기화

## 라이선스

MIT License
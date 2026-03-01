# QuickBase 로우코드 플랫폼 SDK

QuickBase는 온디맨드 로우코드 웹 애플리케이션 플랫폼에 대한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [QuickBase](https://www.quickbase.com/)에 접속하여 계정을 로그인합니다.
2. 설정(Home) > My Preferences > User Token 섹션으로 이동합니다.
3. User Token을 생성합니다 (액세스 권한을 설정합니다).
4. QuickBase Realm Hostname (예: mycompany.quickbase.com)을 확인합니다.

## 사용법

### 클라이언트 초기화

```python
from quickbase import QuickBaseClient

client = QuickBaseClient(
    user_token="your_user_token_here",
    realm_hostname="yourcompany.quickbase.com"
)
```

### 앱 관리

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

### 테이블 관리

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

### 필드 관리

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

### 레코드 관리

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

### 쿼리 및 필터링

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

### 리포트 관리

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

### 사용자 관리

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

### 역할 관리

```python
# 앱 역할 목록
roles = client.get_roles(app_id="app_id")
for role in roles:
    print(f"역할 ID: {role['id']}, 이름: {role['name']}")
```

### 폼 관리

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

## 필드 유형

QuickBase는 다양한 필드 유형을 지원합니다:

- **text**: 텍스트 필드
- **rich-text**: 리치 텍스트 필드
- **numeric**: 숫자 필드
- **currency**: 통화 필드
- **percent**: 백분율 필드
- **date**: 날짜 필드
- **date-time**: 날짜 및 시간 필드
- **checkbox**: 체크박스 필드
- **phone**: 전화번호 필드
- **email**: 이메일 필드
- **url**: URL 필드
- **user**: 사용자 필드
- **file**: 파일 첨부 필드
- **multi-select-text**: 다중 선택 텍스트 필드
- **record-id**: 레코드 ID 필드 (주로 필드 6)

## 쿼리 문법 예제

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

## 주요 기능

- ✅ 애플리케이션 CRUD 작업
- ✅ 테이블 관리
- ✅ 필드 생성 및 수정
- ✅ 레코드 삽입, 업데이트, 삭제
- ✅ 쿼리 및 필터링
- ✅ 리포트 실행
- ✅ 사용자 및 역할 관리
- ✅ 폼 관리
- ✅ 일괄 작업 지원

## 라이선스

MIT License
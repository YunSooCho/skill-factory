# Zoho Creator 로우코드 플랫폼 SDK

Zoho Creator는 Zoho의 로우코드 애플리케이션 개발 플랫폼에 대한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [Zoho Developer Console](https://zoho.com/creator/)에 접속합니다.
2. 새 애플리케이션을 생성하거나 기존 애플리케이션을 선택합니다.
3. Settings > API Settings로 이동합니다.
4. OAuth 인증을 설정하고 클라이언트 ID, 클라이언트 비밀을 발급받습니다.
5. 액세스 토큰을 생성합니다.
6. Account Owner ID (예: 123456789)를 확인합니다.
7. 애플리케이션 Link Name을 확인합니다.

## 사용법

### 클라이언트 초기화

```python
from zoho_creator import ZohoCreatorClient

client = ZohoCreatorClient(
    auth_token="your_auth_token_here",
    owner="your_owner_id",
    app_link_name="your_app_name"
)
```

### 폼(Form) 관리

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

### 레코드 관리

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

### 일괄 작업

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

### 필드 관리

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

### 리포트 관리

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

### 검색

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

### 관련 레코드

```python
# 관련 레코드 조회 (Lookup 관계)
related = client.get_related_records(
    form_link_name="Order",
    record_id="order_id",
    related_form_link_name="Customer"
)
```

### 댓글 관리

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

### 파일 관리

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

### 워크플로우

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

### 통계

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

## 필드 유형 예시

- **text**: 텍스트
- **multiline**: 여러 줄 텍스트
- **number**: 숫자
- **currency**: 통화
- **email**: 이메일
- **phone**: 전화번호
- **date**: 날짜
- **datetime**: 날짜 및 시간
- **boolean**: 부울 (참/거짓)
- **file**: 파일 업로드
- **image**: 이미지
- **lookup**: 조회 필드
- **dropdown**: 드롭다운
- **radio**: 라디오 버튼
- **checkbox**: 체크박스
- **multiselect**: 다중 선택
- **url**: URL
- **formula**: 수식

## 쿼리 조건(Criteria) 예시

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

## 주요 기능

- ✅ 폼(Form) 및 레코드 관리
- ✅ CRUD 작업
- ✅ 일괄 작업 지원
- ✅ 필드 관리
- ✅ 리포트 생성 및 실행
- ✅ 검색 기능
- ✅ 레코드 관계
- ✅ 댓글 기능
- ✅ 파일 업로드/다운로드
- ✅ 워크플로우 트리거
- ✅ 통계 및 분석

## 인증

Zoho Creator는 OAuth 2.0 인증을 사용합니다. 클라이언트는 발급받은 액세스 토큰을 사용하여 인증합니다.

## 라이선스

MIT License
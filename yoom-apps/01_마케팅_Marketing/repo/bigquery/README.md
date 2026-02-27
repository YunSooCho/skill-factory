# Google BigQuery API Integration

Google Cloud BigQuery를 사용하여 데이터 쿼리, 레코드 생성, 검색을 수행하는 Python 라이브러리입니다.

## 설치

```bash
pip install google-cloud-bigquery
```

## 사용법

### 클라이언트 초기화

```python
from bigquery import BigQueryClient

# 환경 변수 사용 (GOOGLE_APPLICATION_CREDENTIALS)
client = BigQueryClient(project_id="your_project_id")

# 서비스 계정 파일 사용
client = BigQueryClient(
    project_id="your_project_id",
    credentials_path="/path/to/service-account.json"
)

# 서비스 계정 정보 사용
client = BigQueryClient(
    project_id="your_project_id",
    credentials={
        "type": "service_account",
        "project_id": "your_project_id",
        "private_key_id": "...",
        "private_key": "...",
        "client_email": "...",
        # ...
    }
)
```

### 쿼리 실행

```python
# 간단한 쿼리
results = client.execute_query("""
    SELECT name, total, tip
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    LIMIT 10
""")

# 파라미터가 있는 쿼리
query = """
    SELECT name, total
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state = @state
    LIMIT @limit
"""
params = [
    bigquery.ScalarQueryParameter("state", "STRING", "CA"),
    bigquery.ScalarQueryParameter("limit", "INT64", 100),
]
results = client.execute_query(query, query_parameters=params)

# 결과 테이블 지정
job_info = client.query_with_job(
    query="SELECT * FROM source_table WHERE condition = true",
    destination_table="my_project.my_dataset.result_table",
    write_disposition="WRITE_TRUNCATE"
)
```

### 레코드 생성

```python
# 단일 레코드 생성
client.create_row(
    dataset_id="my_dataset",
    table_id="my_table",
    row_data={
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com"
    }
)

# 다중 레코드 생성
client.create_rows(
    dataset_id="my_dataset",
    table_id="my_table",
    rows_data=[
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 35}
    ]
)
```

### 레코드 검색

```python
# 모든 레코드
rows = client.search_rows(
    dataset_id="my_dataset",
    table_id="my_table"
)

# 필터 적용
rows = client.search_rows(
    dataset_id="my_dataset",
    table_id="my_table",
    filters={"age": 30, "status": "active"},
    limit=100
)
```

### 테이블 정보

```python
table_info = client.get_table(
    dataset_id="my_dataset",
    table_id="my_table"
)

print(f"Rows: {table_info['num_rows']}")
print(f"Schema: {table_info['schema']}")
```

## API 메서드

| 메서드 | 설명 |
|--------|------|
| `execute_query()` | SQL 쿼리 실행 |
| `query_with_job()` | 쿼리 실행 (결과 테이블 지정 가능) |
| `create_row()` | 단일 레코드 생성 |
| `create_rows()` | 다중 레코드 생성 |
| `search_rows()` | 레코드 검색 |
| `get_table()` | 테이블 정보 조회 |

## 예외 처리

```python
from bigquery import BigQueryClient, BigQueryAPIError, BigQueryAuthError

try:
    results = client.execute_query("SELECT * FROM table")
except BigQueryAuthError as e:
    print("인증 오류:", e)
except BigQueryAPIError as e:
    print("API 오류:", e)
```

## 인증

Google Cloud 인증은 다음 방법 중 하나로 설정할 수 있습니다:

1. **환경 변수**: `GOOGLE_APPLICATION_CREDENTIALS`에 서비스 계정 JSON 파일 경로 설정
2. **서비스 계정 파일**: `credentials_path` 매개변수로 파일 경로 제공
3. **서비스 계정 정보**: `credentials` 매개변수로 직접 제공
4. **Application Default Credentials**: 기본 자격 증명 사용 (gcloud auth login 등)

## API 참조

- [BigQuery REST API](https://cloud.google.com/bigquery/docs/reference/rest)
- [BigQuery Python Client](https://cloud.google.com/python/docs/reference/bigquery/latest)
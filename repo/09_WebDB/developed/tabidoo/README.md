# Tabidoo 데이터베이스 SDK

Tabidoo는 간편한 데이터베이스 관리 플랫폼에 대한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [Tabidoo](https://tabidoo.io)에 접속하여 계정을 생성합니다.
2. 설정(Settings) > API Keys 섹션으로 이동합니다.
3. 새 API 키를 생성합니다.
4. 생성된 API 키를 안전한 곳에 저장합니다.

## 사용법

### 클라이언트 초기화

```python
from tabidoo import TabidooClient

client = TabidooClient(
    api_key="your_api_key_here"
)
```

### 테이블 관리

```python
# 모든 테이블 목록
tables = client.get_tables()

# 테이블 생성
new_table = client.create_table(
    name="고객",
    columns=[
        {"name": "이름", "type": "text", "required": True},
        {"name": "이메일", "type": "email", "unique": True},
        {"name": "나이", "type": "number"},
        {"name": "생성일", "type": "date"}
    ]
)

# 테이블 삭제
client.delete_table(table_id="table_id")
```

### 행(Row) 관리

```python
# 행 목록 조회
rows = client.get_rows(table_id="table_id", limit=100)

# 행 생성
client.create_row(
    table_id="table_id",
    data={
        "이름": "홍길동",
        "이메일": "hong@example.com",
        "나이": 30
    }
)

# 행 업데이트
client.update_row(
    table_id="table_id",
    row_id="row_id",
    data={"나이": 31}
)

# 행 삭제
client.delete_row(table_id="table_id", row_id="row_id")
```

### 쿼리 및 일괄 처리

```python
# 쿼리
filtered_rows = client.query_rows(
    table_id="table_id",
    filter_by={
        "conditions": [
            {"column": "나이", "operator": "greater_than", "value": 25}
        ]
    },
    limit=50
)

# 일괄 행 생성
client.batch_create_rows(
    table_id="table_id",
    rows=[
        {"이름": "철수", "이메일": "c@example.com"},
        {"이름": "영희", "이메일": "y@example.com"}
    ]
)
```

### 열(Column) 관리

```python
# 열 목록
columns = client.get_columns(table_id="table_id")

# 열 추가
client.add_column(
    table_id="table_id",
    name="전화번호",
    type="text"
)

# 열 삭제
client.delete_column(table_id="table_id", column_id="column_id")
```

### 폼(Form) 관리

```python
# 폼 목록
forms = client.get_forms(table_id="table_id")

# 폼 생성
client.create_form(
    table_id="table_id",
    name="고객 등록",
    fields=["이름", "이메일", "나이"]
)

# 폼 삭제
client.delete_form(form_id="form_id")
```

## 주요 기능

- ✅ 테이블 관리
- ✅ 행(Row) CRUD 작업
- ✅ 열(Column) 관리
- ✅ 쿼리 및 필터링
- ✅ 일괄 작업 지원
- ✅ 폼(Form) 생성

## 라이선스

MIT License
# SheetRocks 스프레드시트 SDK

SheetRocks는 현대적인 스프레드시트 관리 플랫폼에 대한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [SheetRocks.io](https://sheetrocks.io)에 접속하여 계정을 생성합니다.
2. 설정(Settings) > API Keys 섹션으로 이동합니다.
3. 새 API 키를 생성합니다.
4. 생성된 API 키를 안전한 곳에 저장합니다.

## 사용법

### 클라이언트 초기화

```python
from sheetrocks import SheetRocksClient

client = SheetRocksClient(
    api_key="your_api_key_here"
)
```

### 스프레드시트 관리

```python
# 모든 스프레드시트 목록
spreadsheets = client.get_spreadsheets()
for sheet in spreadsheets:
    print(f"스프레드시트 ID: {sheet['id']}, 이름: {sheet['title']}")
    print(f"설명: {sheet['description']}, 수정일: {sheet['updated_at']}")

# 스프레드시트 상세 정보
spreadsheet = client.get_spreadsheet(spreadsheet_id="spreadsheet_id")

# 스프레드시트 생성
new_spreadsheet = client.create_spreadsheet(
    title="프로젝트 관리",
    description="프로젝트 추적용 스프레드시트"
)

# 스프레드시트 업데이트
client.update_spreadsheet(
    spreadsheet_id="spreadsheet_id",
    title="프로젝트 관리 (업데이트)"
)

# 스프레드시트 복제
duplicate = client.duplicate_spreadsheet(
    spreadsheet_id="spreadsheet_id",
    title="프로젝트 관리 사본"
)

# 스프레드시트 삭제
client.delete_spreadsheet(spreadsheet_id="spreadsheet_id")
```

### 시트(Sheet) 관리

```python
# 스프레드시트 내 시트 목록
sheets = client.get_sheets(spreadsheet_id="spreadsheet_id")
for sheet in sheets:
    print(f"시트 ID: {sheet['id']}, 이름: {sheet['title']}")
    print(f"행 수: {sheet['row_count']}, 열 수: {sheet['column_count']}")

# 시트 상세 정보
sheet = client.get_sheet(sheet_id="sheet_id")

# 시트 생성
new_sheet = client.create_sheet(
    spreadsheet_id="spreadsheet_id",
    title="작업 추적",
    row_count=1000,
    column_count=10
)

# 시트 크기 조정
client.update_sheet(
    sheet_id="sheet_id",
    row_count=2000,
    column_count=15
)

# 시트 이름 변경
client.update_sheet(
    sheet_id="sheet_id",
    title="업데이트된 시트"
)

# 시트 삭제
client.delete_sheet(sheet_id="sheet_id")
```

### 셀(Cell) 관리

```python
# 범위 내 셀 조회
cells = client.get_cells(
    sheet_id="sheet_id",
    range="A1:D10"
)

for row in cells['values']:
    for cell_value in row:
        print(cell_value, end="\t")
    print()

# 특정 셀 조회
cell = client.get_cell(
    sheet_id="sheet_id",
    cell="A1"
)
print(f"A1 값: {cell['value']}")

# 셀 값 업데이트
client.update_cell(
    sheet_id="sheet_id",
    cell="A1",
    value="제목",
    format={
        "bold": True,
        "font_size": 14,
        "background_color": "#FF0000"
    }
)

# 여러 셀 일괄 업데이트
client.update_cells(
    sheet_id="sheet_id",
    updates=[
        {"cell": "A1", "value": "이름"},
        {"cell": "B1", "value": "부서"},
        {"cell": "C1", "value": "연봉"}
    ]
)

# 범위 지우기
client.clear_range(
    sheet_id="sheet_id",
    range="A1:C100"
)

# 범위 복사
client.copy_range(
    sheet_id="sheet_id",
    source_range="A1:D10",
    destination="F1:I10"
)
```

### 행(Row) 관리

```python
# 전체 행 조회
row = client.get_row(
    sheet_id="sheet_id",
    row_number=2
)

# 행 업데이트
client.update_row(
    sheet_id="sheet_id",
    row_number=2,
    values=["홍길동", "마케팅", 50000000]
)

# 새 행 추가
client.append_row(
    sheet_id="sheet_id",
    values=["철수", "개발", 80000000]
)

# 행 삭제
client.delete_row(
    sheet_id="sheet_id",
    row_number=5
)
```

### 열(Column) 관리

```python
# 전체 열 조회
column = client.get_column(
    sheet_id="sheet_id",
    column_letter="A"
)

# 열 업데이트
client.update_column(
    sheet_id="sheet_id",
    column_letter="A",
    values=["홍길동", "철수", "영희", "민수"]
)

# 새 열 추가
client.append_column(
    sheet_id="sheet_id",
    values=["2024-01-01", "2024-01-02", "2024-01-03"]
)

# 열 삭제
client.delete_column(
    sheet_id="sheet_id",
    column_letter="D"
)
```

### 데이터 내보내기/가져오기

```python
# 시트 내보내기
export_result = client.export_sheet(
    sheet_id="sheet_id",
    format="xlsx",
    range="A1:Z100"
)
print(f"다운로드 URL: {export_result['download_url']}")

# CSV로 내보내기
csv_export = client.export_sheet(
    sheet_id="sheet_id",
    format="csv"
)

# 데이터 가져오기
import_data = [
    ["이름", "나이", "성별"],
    ["홍길동", 30, "남"],
    ["영희", 25, "여"],
    ["철수", 35, "남"]
]

client.import_data(
    sheet_id="sheet_id",
    data=import_data,
    start_cell="A1"
)
```

### 검색

```python
# 스프레드시트 내 검색
results = client.search(
    spreadsheet_id="spreadsheet_id",
    query="홍길동"
)

for result in results:
    print(f"시트: {result['sheet_title']}, 셀: {result['cell']}, 값: {result['value']}")

# 특정 시트에서 검색
sheet_results = client.search(
    spreadsheet_id="spreadsheet_id",
    query="마케팅",
    sheet_id="sheet_id"
)
```

### 공유 및 권한 관리

```python
# 권한 목록 조회
permissions = client.get_permissions(spreadsheet_id="spreadsheet_id")

# 권한 추가
client.add_permission(
    spreadsheet_id="spreadsheet_id",
    email="user@example.com",
    role="editor"
)

# 권한 제거
client.remove_permission(
    spreadsheet_id="spreadsheet_id",
    permission_id="permission_id"
)
```

### 댓글 관리

```python
# 셀에 댓글 추가
client.add_comment(
    sheet_id="sheet_id",
    cell="A1",
    text="이 값을 확인해주세요"
)

# 시트 내 모든 댓글 조회
comments = client.get_comments(sheet_id="sheet_id")

for comment in comments:
    print(f"셀: {comment['cell']}, 댓글: {comment['text']}, 작성자: {comment['author']}")

# 댓글 삭제
client.delete_comment(
    sheet_id="sheet_id",
    comment_id="comment_id"
)
```

### 필터링

```python
# 필터 추가
client.add_filter(
    sheet_id="sheet_id",
    range="A1:D100",
    criteria=[
        {
            "column": "C",
            "operator": "greater_than",
            "value": 50000000
        },
        {
            "column": "B",
            "operator": "equals",
            "value": "마케팅"
        }
    ]
)

# 필터 제거
client.remove_filter(
    sheet_id="sheet_id",
    filter_id="filter_id"
)
```

### 셀 형식 지정 예시

```python
# 굴게체 및 색상
 client.update_cell(
    sheet_id="sheet_id",
    cell="A1",
    value="중요",
    format={
        "bold": True,
        "font_color": "#FFFFFF",
        "background_color": "#FF0000",
        "font_size": 16
    }
)

# 숫자 형식
client.update_cell(
    sheet_id="sheet_id",
    cell="B2",
    value=50000.50,
    format={
        "number_format": "currency",
        "decimal_places": 2
    }
)

# 날짜 형식
client.update_cell(
    sheet_id="sheet_id",
    cell="C2",
    value="2024-12-25",
    format={
        "number_format": "date",
        "date_format": "YYYY-MM-DD"
    }
)
```

## 권한(Role) 유형

- **owner**: 소유자 (모든 권한)
- **editor**: 편집자 (읽기 및 쓰기)
- **commenter**: 댓글러 (읽기 및 댓글)
- **viewer**: 뷰어 (읽기 전용)

## 지원하는 내보내기 형식

- **xlsx**: Excel 파일
- **xls**: 이전 Excel 형식
- **csv**: CSV 파일
- **pdf**: PDF 문서
- **html**: HTML 형식

## 연산자(Operator) 예시

- **equals**: 같음
- **not_equals**: 다름
- **greater_than**: 보다 큼
- **less_than**: 보다 작음
- **greater_than_or_equals**: 보다 크거나 같음
- **less_than_or_equals**: 보다 작거나 같음
- **contains**: 포함
- **starts_with**: 시작
- **ends_with**: 끝
- **not_contains**: 포함하지 않음

## 주요 기능

- ✅ 스프레드시트 CRUD
- ✅ 시트(Sheet) 관리
- ✅ 셀(Cell) 관리
- ✅ 행 및 열 관리
- ✅ 범위 작업
- ✅ 데이터 내보내기/가져오기
- ✅ 검색 기능
- ✅ 공유 및 권한 관리
- ✅ 댓글 기능
- ✅ 필터링
- ✅ 셀 서식 지정

## 라이선스

MIT License
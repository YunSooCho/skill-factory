＃SheetRocksスプレッドシートSDK

SheetRocksは、現代のスプレッドシート管理プラットフォーム用のPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [SheetRocks.io]（https://sheetrocks.io)에にアクセスしてアカウントを作成します。
2. 「設定」(Settings) > API Keys セクションに移動します。
3. 新しい API キーを生成します。
4. 生成された API キーを安全な場所に保存します。

##使用法

### クライアントの初期化

```python
from sheetrocks import SheetRocksClient

client = SheetRocksClient(
    api_key="your_api_key_here"
)
```

### スプレッドシートの管理

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

### シートの管理

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

### セル(Cell)の管理

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

### 行(Row)の管理

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

### 列(Column)の管理

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

### データのエクスポート/インポート

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

###検索

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

### 共有と権限の管理

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

### コメントの管理

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

###フィルタリング

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

### セル書式の例

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

## 権限 (Role) タイプ

- **owner**：所有者（すべての権限）
- **editor**：編集者（読み取りと書き込み）
- **commenter**: コメント(読書とコメント)
- **viewer**：ビューア（読み取り専用）

## サポートするエクスポート形式

- **xlsx**: Excel ファイル
- **xls**: 古いExcel形式
- **csv**: CSVファイル
- **pdf**: PDF文書
- **html**：HTML形式

## 演算子(Operator)の例

- **equals**: 同じ
- **not_equals**: 相違
- **greater_than**: より大きい
- **less_than**: より小さい
- **greater_than_or_equals**: より大きいか等しい
- **less_than_or_equals**: より小さいか等しい
- **contains**: 含む
- **starts_with**: スタート
- **ends_with**: 終了
- **not_contains**: 含まない

##主な機能

- ✅スプレッドシートCRUD
- ✅シート(Sheet)管理
- ✅セル（Cell）管理
- ✅ 行と列の管理
- ✅範囲操作
- ✅データのエクスポート/インポート
- ✅検索機能
- ✅共有と権限管理
- ✅コメント機能
- ✅フィルタリング
- ✅セルの書式設定

##ライセンス

MIT License
#TabidooデータベースSDK

Tabidooは、簡単なデータベース管理プラットフォーム用のPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [Tabidoo](https://tabidoo.io)에 にアクセスしてアカウントを作成します。
2. 「設定」(Settings) > API Keys セクションに移動します。
3. 新しい API キーを生成します。
4. 生成された API キーを安全な場所に保存します。

##使用法

### クライアントの初期化

```python
from tabidoo import TabidooClient

client = TabidooClient(
    api_key="your_api_key_here"
)
```

### テーブル管理

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

### 行(Row)の管理

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

### クエリとバッチ処理

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

### 列(Column)の管理

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

### フォーム(Form)の管理

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

##主な機能

- ✅テーブル管理
- ✅行（Row）CRUD操作
- ✅列(Column)管理
- ✅クエリとフィルタリング
- ✅バッチジョブのサポート
- ✅ フォーム(Form)の生成

##ライセンス

MIT License
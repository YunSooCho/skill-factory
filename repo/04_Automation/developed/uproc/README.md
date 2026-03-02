#Uproc APIクライアント

Uproc用のPython APIクライアントです。データ処理機能を提供します。

## 概要

Uprocは、データ行処理およびバッチ処理機能を提供するサービスです。

## インストール

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## API キー発行

1. [Uproc]（https://uproc.com/)에서アカウントの作成
2. API キー発行
3. API キーを安全に保存

##使用法

### 初期化

```python
from uproc import UprocClient, UprocError

client = UprocClient(
    api_key="YOUR_API_KEY",
    timeout=60
)
```

### 単一行処理

```python
result = client.process_row(
    row_data={
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1-555-1234"
    },
    process_type="standard"
)
```

### 複数行の処理

```python
rows = [
    {"name": "John", "score": 85},
    {"name": "Jane", "score": 92},
    {"name": "Bob", "score": 78}
]

result = client.process_multiple_rows(
    rows=rows,
    process_type="batch"
)
```

### ジョブステータスの確認

```python
status = client.get_job_status("job_id_here")
print(f"Status: {status.get('status')}")
```

## エラー処理

```python
try:
    result = client.process_row(row_data)
except UprocAuthenticationError:
    print("API 키가 올바르지 않습니다")
except UprocRateLimitError:
    print("속도 제한이 초과되었습니다")
except UprocError as e:
    print(f"요청 실패: {str(e)}")
```

##ライセンス

MIT License
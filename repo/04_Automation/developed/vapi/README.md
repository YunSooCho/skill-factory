#Vapi APIクライアント

Vapi用のPython APIクライアントです。音声通話の自動化機能を提供します。

## 概要

VapiはAIベースの音声通話自動化サービスです。コール生成、ログ検索、分析などの機能を提供します。

## インストール

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## API キー発行

1. [Vapi]（https://vapi.ai/)에서アカウントを作成
2. API キー発行
3. API キーを安全に保存

##使用法

### 初期化

```python
from vapi import VapiClient, VapiError

client = VapiClient(
    api_key="YOUR_API_KEY",
    timeout=60
)
```

###発信通話の生成

```python
result = client.create_outbound_call(
    phone_number="+821012345678",
    assistant_id="assistant_id_here",
    customer_name="John Doe"
)

call_id = result.get("id")
print(f"Call ID: {call_id}")
```

###通話検索

```python
result = client.search_calls(
    limit=10,
    status="completed",
    assistant_id="assistant_id_here"
)

for call in result.get("calls", []):
    print(f"- {call.get('id')}: {call.get('status')}")
```

### ログ検索

```python
result = client.search_logs(
    call_id="call_id_here",
    level="info",
    limit=50
)
```

### データ分析

```python
result = client.search_data_analytics(
    start_date="2024-01-01",
    end_date="2024-01-31",
    metrics=["call_count", "duration", "success_rate"],
    group_by="day"
)
```

### ファイルのアップロード

```python
result = client.upload_file(
    file="audio.mp3",
    file_type="audio",
    name="greeting"
)

file_id = result.get("id")
print(f"File ID: {file_id}")
```

### 通話詳細の照会

```python
call = client.get_call("call_id_here")
print(f"Status: {call.get('status')}")
print(f"Duration: {call.get('duration')}")
```

## エラー処理

```python
try:
    result = client.create_outbound_call(phone_number, assistant_id)
except VapiAuthenticationError:
    print("API 키가 올바르지 않습니다")
except VapiRateLimitError:
    print("속도 제한이 초과되었습니다")
except VapiError as e:
    print(f"요청 실패: {str(e)}")
```

##ライセンス

MIT License

## サポート

- [Vapi公式サイト]（https://vapi.ai/)
- [Vapiドキュメント]（https://docs.vapi.ai/)
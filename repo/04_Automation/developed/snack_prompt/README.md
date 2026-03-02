#Snack Prompt APIクライアント

Snack Prompt用のPython APIクライアント。要素検索機能を提供します。

## 概要

Snack Promptは、プロンプトテンプレート、UI要素など、さまざまな要素を検索して活用できるサービスです。

## インストール

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## API キー発行

1. [Snack Prompt]（https://snackprompt.com/)에서アカウントの作成
2.ダッシュボードでAPIキーを発行する
3. API キーを安全に保存

##使用法

### 初期化

```python
from snack_prompt import SnackPromptClient, SnackPromptError

client = SnackPromptClient(
    api_key="YOUR_API_KEY",
    timeout=30
)
```

###要素検索

```python
try:
    result = client.search_elementals(
        query="productivity",
        limit=10
    )
    print(f"Found {result.get('total', 0)} elementals")
    for elemental in result.get('elementals', []):
        print(f"- {elemental.get('name')}")
except SnackPromptError as e:
    print("Error:", str(e))
```

### カテゴリとタグフィルタ

```python
result = client.search_elementals(
    query="marketing",
    category="templates",
    tags=["email", "automation"],
    limit=20
)
```

### 特定の要素の詳細検索

```python
try:
    elemental = client.get_elemental("elemental_id_here")
    print("Name:", elemental.get("name"))
    print("Description:", elemental.get("description"))
except SnackPromptError as e:
    print("Error:", str(e))
```

### カテゴリリストの照会

```python
categories = client.list_categories()
for category in categories.get('categories', []):
    print(f"- {category.get('name')}")
```

## エラー処理

```python
from snack_prompt import SnackPromptError, SnackPromptRateLimitError, SnackPromptAuthenticationError

try:
    result = client.search_elementals("query")
except SnackPromptAuthenticationError:
    print("API 키가 올바르지 않습니다")
except SnackPromptRateLimitError:
    print("속도 제한이 초과되었습니다")
except SnackPromptError as e:
    print(f"요청 실패: {str(e)}")
```

##ライセンス

MIT License
# Snack Prompt API 클라이언트

Snack Prompt를 위한 Python API 클라이언트입니다. 요소(Elemental) 검색 기능을 제공합니다.

## 개요

Snack Prompt는 프롬프트 템플릿, UI 요소 등 다양한 요소를 검색하고 활용할 수 있는 서비스입니다.

## 설치

```bash
pip install requests
```

또는:

```bash
pip install -r requirements.txt
```

## API 키 발급

1. [Snack Prompt](https://snackprompt.com/)에서 계정 생성
2. 대시보드에서 API 키 발급
3. API 키를 안전하게 저장

## 사용법

### 초기화

```python
from snack_prompt import SnackPromptClient, SnackPromptError

client = SnackPromptClient(
    api_key="YOUR_API_KEY",
    timeout=30
)
```

### 요소 검색

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

### 카테고리 및 태그 필터

```python
result = client.search_elementals(
    query="marketing",
    category="templates",
    tags=["email", "automation"],
    limit=20
)
```

### 특정 요소 상세 조회

```python
try:
    elemental = client.get_elemental("elemental_id_here")
    print("Name:", elemental.get("name"))
    print("Description:", elemental.get("description"))
except SnackPromptError as e:
    print("Error:", str(e))
```

### 카테고리 목록 조회

```python
categories = client.list_categories()
for category in categories.get('categories', []):
    print(f"- {category.get('name')}")
```

## 에러 처리

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

## 라이선스

MIT License
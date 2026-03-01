# TextCortex AI API 클라이언트

TextCortex AI를 위한 Python API 클라이언트입니다. 다양한 텍스트 생성 및 변환 기능을 제공합니다.

## 개요

TextCortex AI는 텍스트 요약, 생성, 번역, 재작성 등 다양한 AI 기반 텍스트 기능을 제공합니다.

## 설치

```bash
pip install requests
```

또는:

```bash
pip install -r requirements.txt
```

## API 키 발급

1. [TextCortex](https://textcortex.com/)에서 계정 생성
2. API 키 발급
3. API 키를 안전하게 저장

## 사용법

### 초기화

```python
from textcortex_ai import TextCortexClient, TextCortexError

client = TextCortexClient(
    api_key="YOUR_API_KEY",
    timeout=30
)
```

### 1. 텍스트 요약

```python
result = client.generate_summary(
    text="Long text to summarize...",
    max_length=100
)
print("Summary:", result.get("summary"))
```

### 2. 제품 설명 생성

```python
result = client.generate_product_description(
    product_name="Smart Watch",
    features="Water resistant, Heart rate monitor, GPS",
    tone="professional"
)
```

### 3. 텍스트 단순화

```python
result = client.simplify_text(
    text="Complex technical text...",
    target_level="simple"
)
```

### 4. 번역

```python
result = client.translate_text(
    text="Hello world",
    target_language="Korean"
)
```

### 5. paraphrase (의역)

```python
result = client.paraphrase_text(
    text="Original text...",
    tone="formal"
)
```

### 6. 텍스트 재작성

```python
result = client.rewrite_text(
    text="Text to rewrite...",
    style="creative"
)
```

### 7. 소셜 미디어 포스트 생성

```python
result = client.generate_social_media_post(
    topic="New product launch",
    platform="twitter",
    tone="engaging"
)
```

### 8. 텍스트 완성

```python
result = client.generate_text_completion(
    prompt="Once upon a time...",
    max_tokens=200
)
```

### 9. 코드 생성

```python
result = client.generate_code(
    prompt="Create a function to sort a list",
    language="python"
)
```

### 10. 이메일 생성

```python
result = client.generate_email(
    subject="Meeting Request",
    purpose="Request a meeting next week",
    tone="professional"
)
```

## 에러 처리

```python
from textcortex_ai import TextCortexError, TextCortexRateLimitError, TextCortexAuthenticationError

try:
    result = client.generate_summary("text")
except TextCortexAuthenticationError:
    print("API 키가 올바르지 않습니다")
except TextCortexRateLimitError:
    print("속도 제한이 초과되었습니다")
except TextCortexError as e:
    print(f"요청 실패: {str(e)}")
```

## 라이선스

MIT License

## 지원

- [TextCortex 공식 사이트](https://textcortex.com/)
- [TextCortex API 문서](https://api.textcortex.com/)
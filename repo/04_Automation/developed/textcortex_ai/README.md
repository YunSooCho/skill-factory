#TextCortex AI APIクライアント

TextCortex AI用のPython APIクライアントです。さまざまなテキスト生成および変換機能を提供します。

## 概要

TextCortex AIは、テキストの要約、生成、翻訳、書き換えなど、さまざまなAIベースのテキスト機能を提供します。

## インストール

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## API キー発行

1. [TextCortex](https://textcortex.com/)에서 アカウントの作成
2. API キー発行
3. API キーを安全に保存

##使用法

### 初期化

```python
from textcortex_ai import TextCortexClient, TextCortexError

client = TextCortexClient(
    api_key="YOUR_API_KEY",
    timeout=30
)
```

### 1. テキストの要約

```python
result = client.generate_summary(
    text="Long text to summarize...",
    max_length=100
)
print("Summary:", result.get("summary"))
```

### 2. 製品説明の生成

```python
result = client.generate_product_description(
    product_name="Smart Watch",
    features="Water resistant, Heart rate monitor, GPS",
    tone="professional"
)
```

### 3. テキストの簡略化

```python
result = client.simplify_text(
    text="Complex technical text...",
    target_level="simple"
)
```

### 4. 翻訳

```python
result = client.translate_text(
    text="Hello world",
    target_language="Korean"
)
```

### 5. paraphrase (義務)

```python
result = client.paraphrase_text(
    text="Original text...",
    tone="formal"
)
```

### 6. テキストの書き換え

```python
result = client.rewrite_text(
    text="Text to rewrite...",
    style="creative"
)
```

### 7. ソーシャルメディアポストの作成

```python
result = client.generate_social_media_post(
    topic="New product launch",
    platform="twitter",
    tone="engaging"
)
```

### 8. テキストの完成

```python
result = client.generate_text_completion(
    prompt="Once upon a time...",
    max_tokens=200
)
```

### 9. コード生成

```python
result = client.generate_code(
    prompt="Create a function to sort a list",
    language="python"
)
```

### 10. 電子メールの生成

```python
result = client.generate_email(
    subject="Meeting Request",
    purpose="Request a meeting next week",
    tone="professional"
)
```

## エラー処理

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

##ライセンス

MIT License

## サポート

- [TextCortex公式サイト]（https://textcortex.com/)
- [TextCortex APIドキュメント]（https://api.textcortex.com/)
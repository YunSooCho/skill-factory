# Refiner SDK

RefinerはAIベースのコンテンツ最適化ツールのためのPython SDKです。

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [Refinerウェブサイト]（https://refiner.ai)에にアクセスしてアカウントを作成します。
2.ダッシュボードでAPI Keysメニューに移動します。
3. [Create New API Key]ボタンをクリックして新しいAPIキーを生成します。
4. 生成された API キーを安全な場所に保存します。

##使用法

### クライアントの初期化

```python
from refiner import RefinerClient

client = RefinerClient(
    api_key="your_api_key_here",
    base_url="https://api.refiner.ai/v1"
)
```

###テキストの最適化

```python
result = client.refine_text(
    text="이 제품은 정말 좋아요. 강력 추천합니다.",
    tone="professional",
    length="same",
    goal="설득력 향상"
)

print(f"최적화된 텍스트: {result['refinedText']}")
print(f"변경 사항: {result['changes']}")
```

###パラフレージング

```python
result = client.paraphrase(
    text="고객 서비스가 매우 만족스럽습니다.",
    style="business",
    variations=3
)

for variant in result['variations']:
    print(f"- {variant}")
```

###テキストの要約

```python
result = client.summarize(
    text="긴 문서의 내용...",
    max_length=200,
    format="bullet"
)

print(f"요약: {result['summary']}")
```

###文法チェック

```python
result = client.check_grammar(
    text="그거는 잘 이해가 안돼요.",
    language="ko"
)

for error in result['errors']:
    print(f"오류: {error['message']}")
    print(f"수정: {error['suggestion']}")
```

### テキスト拡張

```python
result = client.expand_text(
    text="우리 회사는 AI 기술에 집중합니다.",
    context="제품 소개서",
    length=300
)

print(f"확장된 텍스트: {result['expandedText']}")
```

###翻訳

```python
result = client.translate(
    text="Hello, how are you?",
    target_language="ko",
    source_language="en"
)

print(f"번역: {result['translatedText']}")
```

###感性分析

```python
result = client.detect_sentiment(
    text="이 제품은 정말 훌륭합니다. 다시 구매하고 싶어요!"
)

print(f"감성: {result['sentiment']}")  # positive, negative, neutral
print(f"점수: {result['score']}")
print(f"신뢰도: {result['confidence']}")
```

### キーワード抽出

```python
result = client.extract_keywords(
    text="AI 기술을 활용한 고객 지원 서비스는 비용 절감과 효율성 향상에 기여합니다.",
    max_keywords=5
)

for keyword in result['keywords']:
    print(f"{keyword['word']}: {keyword['score']}")
```

###タイトルの作成

```python
result = client.generate_title(
    text="긴 문서 또는 게시물 본문...",
    count=5,
    style="engaging"
)

for title in result['titles']:
    print(f"- {title}")
```

### 読みやすさの改善

```python
result = client.improve_readability(
    text="복잡한 기술 설명...",
    target_audience="general",
    reading_level="medium"
)

print(f"개선된 텍스트: {result['improvedText']}")
print(f"원본 난이도: {result['originalLevel']}")
print(f"개선 후 난이도: {result['improvedLevel']}")
```

### バッチ処理

```python
texts = [
    "첫 번째 텍스트",
    "두 번째 텍스트",
    "세 번째 텍스트"
]

result = client.batch_refine(
    texts=texts,
    operation="refine",
    tone="professional"
)

for item in result['results']:
    print(f"원본: {item['original']}")
    print(f"결과: {item['result']}\\n")
```

### 使用統計

```python
stats = client.get_usage_stats(
    start_date="2024-01-01",
    end_date="2024-01-31"
)

print(f"총 API 호출: {stats['totalCalls']}")
print(f"토큰 사용량: {stats['tokenUsage']}")
```

## 機能

- ✅テキストの最適化（投稿を修正）
- ✅パラフレージング（再書き込み）
- ✅テキストサマリー
- ✅文法とスペルチェック
- ✅テキスト拡張
- ✅多言語翻訳
- ✅感性分析
- ✅キーワード抽出
- ✅タイトルの作成
- ✅ 読みやすさの改善
- ✅バッチ処理

##ライセンス

MIT License
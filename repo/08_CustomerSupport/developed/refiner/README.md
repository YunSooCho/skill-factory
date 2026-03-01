# Refiner SDK

Refiner는 AI 기반 콘텐츠 최적화 도구를 위한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [Refiner 웹사이트](https://refiner.ai)에 접속하여 계정을 생성합니다.
2. 대시보드에서 API Keys 메뉴로 이동합니다.
3. 'Create New API Key' 버튼을 클릭하여 새 API 키를 생성합니다.
4. 생성된 API 키를 안전한 곳에 저장합니다.

## 사용법

### 클라이언트 초기화

```python
from refiner import RefinerClient

client = RefinerClient(
    api_key="your_api_key_here",
    base_url="https://api.refiner.ai/v1"
)
```

### 텍스트 최적화

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

### 파라프레이징

```python
result = client.paraphrase(
    text="고객 서비스가 매우 만족스럽습니다.",
    style="business",
    variations=3
)

for variant in result['variations']:
    print(f"- {variant}")
```

### 텍스트 요약

```python
result = client.summarize(
    text="긴 문서의 내용...",
    max_length=200,
    format="bullet"
)

print(f"요약: {result['summary']}")
```

### 문법 검사

```python
result = client.check_grammar(
    text="그거는 잘 이해가 안돼요.",
    language="ko"
)

for error in result['errors']:
    print(f"오류: {error['message']}")
    print(f"수정: {error['suggestion']}")
```

### 텍스트 확장

```python
result = client.expand_text(
    text="우리 회사는 AI 기술에 집중합니다.",
    context="제품 소개서",
    length=300
)

print(f"확장된 텍스트: {result['expandedText']}")
```

### 번역

```python
result = client.translate(
    text="Hello, how are you?",
    target_language="ko",
    source_language="en"
)

print(f"번역: {result['translatedText']}")
```

### 감성 분석

```python
result = client.detect_sentiment(
    text="이 제품은 정말 훌륭합니다. 다시 구매하고 싶어요!"
)

print(f"감성: {result['sentiment']}")  # positive, negative, neutral
print(f"점수: {result['score']}")
print(f"신뢰도: {result['confidence']}")
```

### 키워드 추출

```python
result = client.extract_keywords(
    text="AI 기술을 활용한 고객 지원 서비스는 비용 절감과 효율성 향상에 기여합니다.",
    max_keywords=5
)

for keyword in result['keywords']:
    print(f"{keyword['word']}: {keyword['score']}")
```

### 제목 생성

```python
result = client.generate_title(
    text="긴 문서 또는 게시물 본문...",
    count=5,
    style="engaging"
)

for title in result['titles']:
    print(f"- {title}")
```

### 가독성 개선

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

### 배치 처리

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

### 사용 통계

```python
stats = client.get_usage_stats(
    start_date="2024-01-01",
    end_date="2024-01-31"
)

print(f"총 API 호출: {stats['totalCalls']}")
print(f"토큰 사용량: {stats['tokenUsage']}")
```

## 기능

- ✅ 텍스트 최적화 (글 고치기)
- ✅ 파라프레이징 (다시 쓰기)
- ✅ 텍스트 요약
- ✅ 문법 및 맞춤법 검사
- ✅ 텍스트 확장
- ✅ 다국어 번역
- ✅ 감성 분석
- ✅ 키워드 추출
- ✅ 제목 생성
- ✅ 가독성 개선
- ✅ 배치 처리

## 라이선스

MIT License
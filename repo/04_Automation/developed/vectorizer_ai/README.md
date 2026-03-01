# Vectorizer AI API 클라이언트

Vectorizer AI를 위한 Python API 클라이언트입니다. 이미지를 벡터 그래픽으로 변환하는 기능을 제공합니다.

## 개요

Vectorizer AI는 래스터 이미지(SVG, PNG 등)를 벡터 그래픽으로 변환하는 서비스입니다.

## 설치

```bash
pip install requests
```

또는:

```bash
pip install -r requirements.txt
```

## API 키 발급

1. [Vectorizer AI](https://vectorizer.ai/)에서 계정 생성
2. API 키 발급
3. API 키를 안전하게 저장

## 사용법

### 초기화

```python
from vectorizer_ai import VectorizerAIClient, VectorizerAIError

client = VectorizerAIClient(
    api_key="YOUR_API_KEY",
    timeout=60
)
```

### 이미지 벡터화

```python
result = client.vectorize_image(
    image="logo.png",
    output_format="svg",
    detail_level="high",
    colors="color"
)

job_id = result.get("job_id")
```

### 작업 상태 확인

```python
status = client.get_vectorization_status(job_id)
print(f"Status: {status.get('status')}")
```

### 벡터 파일 다운로드

```python
# 메모리에 다운로드
content = client.download_vector(job_id)

# 파일로 저장
output_path = client.download_vector(job_id, "output.svg")
print(f"Saved to: {output_path}")
```

## 에러 처리

```python
try:
    result = client.vectorize_image("input.png")
except VectorizerAIAuthenticationError:
    print("API 키가 올바르지 않습니다")
except VectorizerAIRateLimitError:
    print("속도 제한이 초과되었습니다")
except VectorizerAIError as e:
    print(f"요청 실패: {str(e)}")
```

## 라이선스

MIT License

## 지원

- [Vectorizer AI 공식 사이트](https://vectorizer.ai/)
- [Vectorizer AI 문서](https://docs.vectorizer.ai/)
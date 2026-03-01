# Stability AI API 클라이언트

Stability AI를 위한 Python API 클라이언트입니다. 이미지 생성, 그리고 편집 기능을 제공합니다.

## 개요

Stability AI는 Stable Diffusion 기반의 최신 이미지 생성 및 편집 서비스입니다. 다양한 이미지 생성, 편집, 배경 제거 등의 기능을 제공합니다.

## 설치

```bash
pip install requests
```

또는:

```bash
pip install -r requirements.txt
```

## API 키 발급

1. [Stability AI](https://platform.stability.ai/)에서 계정 생성
2. API 키 발급
3. API 키를 안전하게 저장

## 사용법

### 초기화

```python
from stability_ai import StabilityAIClient, StabilityAIError

client = StabilityAIClient(
    api_key="YOUR_API_KEY",
    timeout=60
)
```

### 1. 이미지 아웃페인팅 (확장)

```python
try:
    result = client.outpaint_image(
        image="input.jpg",
        prompt="beautiful landscape with mountains",
        left=256,
        right=256,
        top=128,
        bottom=128
    )
    print("Generated images:", result.get("images", []))
except StabilityAIError as e:
    print("Error:", str(e))
```

### 2. 이미지 생성 (Stable Image Core)

```python
result = client.generate_image_core(
    prompt="A beautiful sunset over the ocean",
    negative_prompt="blurry, low quality",
    width=1024,
    height=1024,
    steps=30,
    seed=42
)
```

### 3. 고화질 이미지 생성 (Stable Image Ultra)

```python
result = client.generate_image_ultra(
    prompt="Professional product photo, studio lighting",
    negative_prompt="dark, grainy"
)
```

### 4. 객체 제거

```python
result = client.remove_object(
    image="photo.jpg",
    prompt="remove the person in the background"
)
```

### 5. 배경 제거

```python
result = client.remove_background(
    image="product.png",
    output_format="png"
)
```

### 6. 구조 기반 이미지 생성

```python
result = client.generate_from_structure(
    structure="sketch.jpg",
    prompt="modern building design",
    negative_prompt="ugly"
)
```

### 7. 이미지 인페인팅

```python
result = client.inpaint_image(
    image="photo.jpg",
    mask="mask.png",  # 마스크 (수정할 영역)
    prompt="replace with new content"
)
```

### 8. 레퍼런스 기반 이미지 생성 (Ultra)

```python
result = client.generate_from_reference_ultra(
    reference="reference.jpg",
    prompt="similar style, different content",
    strength=0.6
)
```

### 9. 스케치에서 이미지 생성

```python
result = client.generate_from_sketch(
    sketch="drawing.png",
    prompt="convert to realistic photo",
    negative_prompt="cartoonish"
)
```

## API 메서드

### outpaint_image
이미지를 선택한 방향으로 확장합니다.

### generate_image_core
기본 이미지 생성 (Core 모델).

### generate_image_ultra
고화질 이미지 생성 (Ultra 모델).

### remove_object
이미지에서 원하지 않는 객체 제거.

### remove_background
이미지 배경 제거.

### generate_from_structure
구조/스켈레톤을 기반으로 이미지 생성.

### inpaint_image
마스크를 사용하여 이미지 부분 수정.

### generate_from_reference_ultra
레퍼런스 이미지 비슷하게 생성 (Ultra).

### generate_from_sketch
스케치/드로잉에서 실사 이미지 생성.

## 에러 처리

```python
from stability_ai import StabilityAIError, StabilityAIRateLimitError, StabilityAIAuthenticationError

try:
    result = client.generate_image_core("A beautiful landscape")
except StabilityAIAuthenticationError:
    print("API 키가 올바르지 않습니다")
except StabilityAIRateLimitError:
    print("속도 제한이 초과되었습니다")
except StabilityAIError as e:
    print(f"요청 실패: {str(e)}")
```

## Rate Limiting

API 요청 간 최소 100ms 지연이 적용됩니다.

## 라이선스

MIT License

## 지원

- [Stability AI 플랫폼](https://platform.stability.ai/)
- [API 문서](https://platform.stability.ai/docs)
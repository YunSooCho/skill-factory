# Templated API 클라이언트

Templated를 위한 Python API 클라이언트입니다. 템플릿 기반 문서 생성 및 렌더링을 지원합니다.

## 개요

Templated는 템플릿을 사용하여 PDF, 이미지 등의 문서를 자동으로 생성하는 서비스입니다.

## 설치

```bash
pip install requests
```

또는:

```bash
pip install -r requirements.txt
```

## API 키 발급

1. [Templated](https://templated.io/)에서 계정 생성
2. API 키 발급
3. API 키를 안전하게 저장

## 사용법

### 초기화

```python
from templated import TemplatedClient, TemplatedError

client = TemplatedClient(
    api_key="YOUR_API_KEY",
    timeout=60
)
```

### 템플릿 검색

```python
result = client.search_templates(
    query="invoice",
    category="business",
    limit=10
)

for template in result.get("templates", []):
    print(f"- {template.get('name')}: {template.get('id')}")
```

### 렌더 생성

```python
result = client.create_render(
    template_id="template_id_here",
    data={
        "title": "Invoice #001",
        "date": "2024-01-15",
        "items": [
            {"name": "Service A", "amount": 100},
            {"name": "Service B", "amount": 200}
        ],
        "total": 300
    },
    format="pdf"
)

render_id = result.get("render_id")
print(f"Render ID: {render_id}")
```

### 이미지 업로드

```python
result = client.upload_image(
    image="logo.png",
    name="company-logo"
)

image_url = result.get("url")
print(f"Image URL: {image_url}")
```

### 렌더 다운로드

```python
# 메모리에 다운로드
content = client.download_render(render_id)

# 파일로 저장
output_path = client.download_render(render_id, "output.pdf")
print(f"Saved to: {output_path}")
```

### 여러 렌더 병합

```python
result = client.merge_renders(
    render_ids=["render1", "render2", "render3"],
    output_format="pdf"
)

merged_render_id = result.get("render_id")
```

### 렌더 상태 확인

```python
status = client.get_render_status(render_id)
print(f"Status: {status.get('status')}")  # "pending", "completed", "failed"
```

## 에러 처리

```python
from templated import TemplatedError, TemplatedRateLimitError, TemplatedAuthenticationError

try:
    result = client.create_render(template_id, data)
except TemplatedAuthenticationError:
    print("API 키가 올바르지 않습니다")
except TemplatedRateLimitError:
    print("속도 제한이 초과되었습니다")
except TemplatedError as e:
    print(f"요청 실패: {str(e)}")
```

## 라이선스

MIT License

## 지원

- [Templated 공식 사이트](https://templated.io/)
- [Templated 문서](https://docs.templated.io/)
# Brushup API 클라이언트

Brushup을 위한 Python API 클라이언트입니다. 디자인 검토 기능을 제공합니다.

## 설치

```bash
pip install requests
```

## 사용법

```python
from brushup import BrushupClient, BrushupError

client = BrushupClient(api_key="YOUR_API_KEY")

# 디자인 검토 생성
review = client.create_design_review({
    "projectId": "123",
    "designUrl": "https://example.com/preview"
})
```

## 라이선스

MIT License
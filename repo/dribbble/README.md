# Dribbble API 클라이언트

Dribbble를 위한 Python API 클라이언트입니다. 디자인 플랫폼 기능을 제공합니다.

## 설치

```bash
pip install requests
```

## 사용법

```python
from dribbble import DribbbleClient, DribbbleError

client = DribbbleClient(access_token="YOUR_ACCESS_TOKEN")

# 샷 조회
shots = client.get_shots()

# 프로젝트 조회
projects = client.get_projects()
```

## 라이선스

MIT License
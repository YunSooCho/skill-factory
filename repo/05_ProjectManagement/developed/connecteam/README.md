# Connecteam API 클라이언트

Connecteam을 위한 Python API 클라이언트입니다. 인력 관리 기능을 제공합니다.

## 설치

```bash
pip install requests
```

## 사용법

```python
from connecteam import ConnecteamClient, ConnecteamError

client = ConnecteamClient(api_token="YOUR_API_TOKEN")

# 직원 조회
employees = client.get_employees()

# 교대 생성
shift = client.create_shift({"employeeId": "123", "start": "2024-01-01T09:00:00Z"})
```

## 라이선스

MIT License
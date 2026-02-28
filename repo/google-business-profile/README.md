# Google Business Profile API 클라이언트

Google Business Profile를 위한 Python API 클라이언트입니다.

## 개요

이 클라이언트는 Google Business Profile API에 접근하여 비즈니스 위치 정보를 관리합니다.

## 설치

의존성 패키지:

```bash
pip install requests
```

또는:

```bash
pip install -r requirements.txt
```

## API 키 발급

1. [Google Cloud Console](https://console.cloud.google.com/)에서 프로젝트 생성
2. Google My Business API 사용 설정
3. OAuth 2.0 또는 Service Account 인증 토큰 발급
4. 발급된 Access Token 저장

## 사용법

### 초기화

```python
from google_business_profile.google_business_profile_client import GoogleBusinessProfileClient

client = GoogleBusinessProfileClient(
    access_token="YOUR_ACCESS_TOKEN",
    timeout=30
)
```

### 예시 코드

```python
# 계정의 모든 위치 조회
locations = client.get_locations(
    account_id="accounts/123456789",
    page_size=100
)
print("Locations:", locations)

# 특정 위치 상세 조회
location_detail = client.get_location(
    location_id="locations/987654321"
)
print("Location detail:", location_detail)
```

## API 액션

- `get_locations` - 계정의 비즈니스 위치 목록 조회
- `get_location` - 특정 비즈니스 위치 상세 조회

## 에러 처리

```python
try:
    result = client.get_locations("accounts/123456789")
except Exception as e:
    print("Error:", str(e))
```

## Rate Limiting

API 요청 간 최소 0.1초 지연이 적용됩니다. 너무 많은 요청이 발생하면 Rate Limit 에러가 발생할 수 있습니다.

## 라이선스

MIT License
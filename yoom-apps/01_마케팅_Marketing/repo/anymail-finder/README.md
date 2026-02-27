# Anymail Finder Integration for Yoom

이메일 찾기 및 검증 API 클라이언트

## 설치
```bash
pip install requests
```

## 사용법
```python
from AnymailFinder import AnymailFinderClient

client = AnymailFinderClient(api_key='your_api_key')

# 개인 이메일 찾기
result = client.search_person_email(
    first_name='John',
    last_name='Doe',
    company='Google'
)

# 회사 이메일 찾기
results = client.search_company_email(company='Google')

# 이메일 검증
validation = client.validate_email('john.doe@google.com')
```

## API 액션
- Search Person's Email
- Search Company's Email
- Validate Email
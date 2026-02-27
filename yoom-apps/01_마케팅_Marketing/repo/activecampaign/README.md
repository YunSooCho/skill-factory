# ActiveCampaign API Integration for Yoom

ActiveCampaign 마케팅 오토메이션 API 클라이언트 - Yoom 연동용

## 설치

```bash
pip install requests
```

## 설정

```python
from Activecampaign import ActiveCampaignClient

client = ActiveCampaignClient(
    api_key='your_api_key',
    api_url='https://youraccount.api-us1.com'
)
```

## API 액션

### 계정 관리
```python
# 계정 생성
account = client.create_account(name='회사명', account_url='https://example.com')

# 계정 조회
account = client.get_account('account_id')

# 계정 업데이트
account = client.update_account('account_id', name='새 회사명')

# 계정 삭제
client.delete_account('account_id')
```

### 연락처 관리
```python
# 연락처 생성
contact = client.create_contact(
    email='user@example.com',
    first_name='John',
    last_name='Doe',
    phone='010-1234-5678',
    field_values={'field_1': '값1', 'field_2': '값2'}
)

# 연락처 조회
contact = client.get_contact('contact_id')

# 연락처 검색
contact = client.search_contact('user@example.com')

# 연락처 리스트
contacts = client.list_contacts(limit=20)

# 연락처 삭제
client.delete_contact('contact_id')
```

### 리스트 관리
```python
# 리스트에 추가
client.add_contact_to_list('contact_id', 'list_id')

# 리스트에서 제거
client.remove_contact_from_list('contact_id', 'list_id')
```

### 오토메이션
```python
# 오토메이션에 추가
client.add_contact_to_automation('contact_id', 'automation_id')
```

### 딜 (거래) 관리
```python
# 딜 생성
deal = client.create_deal(
    contact_id='contact_id',
    value=1000.0,
    currency='USD',
    title='신규 거래',
    stage=1,
    account_id='account_id'  # 선택사항
)
```

### 계정-연락처 연결
```python
# 연락처를 계정에 연결
client.associate_account_contact(
    account_id='account_id',
    contact_id='contact_id',
    job_title='CEO'
)
```

### 노트 추가
```python
# 노트 추가
note = client.add_note('contact_id', '중요한 통화 완료')
```

### 연락처 점수
```python
# 연락처 점수 조회
score = client.get_contact_score('contact_id')
print(f"Score: {score}")
```

## 트리거

- **Deal Created**: 새 딜이 생성될 때
- **Contact Added**: 연락처가 추가될 때
- **Contact Created**: 연락처가 생성될 때
- **Contact Field Value Created**: 커스텀 필드 값이 생성될 때

## API 문서

- ActiveCampaign API: https://developers.activecampaign.com/
- API URL 형식: `https://youraccount.api-us1.com`

## 라이선스

MIT License
# AWeber Integration for Yoom

이메일 마케팅 API 클라이언트

## 설치
```bash
pip install requests
```

## 사용법
```python
from Aweber import AWeberClient

client = AWeberClient(
    access_token='your_token',
    account_id='account_id'
)

# 구독자 생성
sub = client.create_subscriber(
    email='user@example.com',
    list_id='list_id',
    name='John Doe'
)

# 구독자 찾기
sub = client.find_subscriber('user@example.com', 'list_id')

# 구독자 이동
client.move_subscriber('user@example.com', 'from_list', 'to_list')
```

## API 액션
- Get Subscriber
- Find Subscriber
- Create Subscriber
- Update Subscriber by Email
- Delete Subscriber by Email
- Move Subscriber
- Search List
- Get Broadcast Open
- Get Broadcast Click
- Get Broadcast Statistic
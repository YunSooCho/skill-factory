# AdRoll API Integration for Yoom

AdRoll 디지털 마케팅 API 클라이언트 - Yoom 연동용

## 설치

```bash
pip install requests
```

## 설정

```python
from Adroll import AdRollClient

client = AdRollClient(
    api_key='your_api_key',
    advertiser_eid='advertiser_eid'  # 선택사항
)
```

## API 액션

### List Segments
```python
# 광고주의 모든 세그먼트 조회
segments = client.list_segments()

# 필터링
segments = client.list_segments(
    advertiser_eid='adv_xxx',
    segment_type='rule',
    status='active',
    limit=50
)

for segment in segments:
    print(f"{segment.name}: {segment.type} - {segment.size} users")
```

### Create Segment
```python
# 요청 객체 사용
from Adroll import SegmentCreateRequest

request = SegmentCreateRequest(
    name='방문자 세그먼트',
    type='api',
    description='웹사이트 방문자',
    advertiser_eid='adv_xxx'
)
segment = client.create_segment(request)

# 또는 직접 매개변수 사용
segment = client.create_segment(
    name='구매자 세그먼트',
    type='upload',
    description='구매한 사용자'
)
```

### Get Segment
```python
segment = client.get_segment('seg_xxx')
print(f"Name: {segment.name}")
print(f"Size: {segment.size}")
```

### Update Segment
```python
segment = client.update_segment(
    'seg_xxx',
    name='새 이름',
    description='업데이트된 설명',
    status='active'
)
```

### Delete Segment
```python
client.delete_segment('seg_xxx')
```

## 세그먼트 유형

- **rule**: 규칙 기반 세그먼트 (자동 생성)
- **upload**: CSV 업로드 세그먼트
- **api**: API로 동적으로 관리되는 세그먼트

## API 문서

- AdRoll API: https://developers.adroll.com/docs/
- API Key 발급: https://app.adroll.com/

## 라이선스

MIT License
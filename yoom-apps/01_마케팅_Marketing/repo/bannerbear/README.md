# Bannerbear Integration for Yoom

이미지/비디오 생성 API 클라이언트

## 설치
```bash
pip install requests
```

## 사용법
```python
from Bannerbear import BannerbearClient

client = BannerbearClient(api_key='your_api_key')

# 이미지 생성
img = client.create_image(
    template='tpl_xxx',
    modifications=[
        {'name': 'text', 'text': 'Hello World'},
        {'name': 'image', 'image_url': 'https://example.com/image.jpg'}
    ]
)

# 스크린샷 생성
shot = client.create_screenshot('https://example.com', width=1200)

# 디테일 조회
details = client.get_image_detail(img.uid)
```

## API 액션
- Create Image
- Create Video
- Create Movie
- Create Screenshot
- Create Collection
- Get Image Detail
- Get Video Detail
- Get Movie Detail
- Get Screenshot Detail
- Get Collection Detail
- Get File Data
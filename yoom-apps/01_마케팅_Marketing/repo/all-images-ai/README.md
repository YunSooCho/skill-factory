# All Images AI Integration for Yoom

이미지 생성 API 클라이언트

## 설치
```bash
pip install requests
```

## 사용법
```python
from AllImagesAi import AllImagesAIClient

client = AllImagesAIClient(api_key='your_api_key')

gen = client.create_image_generation(
    prompt='A beautiful sunset over mountains',
    width=1024,
    height=1024
)

result = client.get_image_generation(gen.id)
print(result.status)
```

## API 액션
- Create Image Generation
- Get Image Generation
- Search Image Generations
- Get Image
- Delete Image Generation
# Abyssale API Integration for Yoom

Abyssale 이미지/비디오 생성 API 클라이언트 - Yoom 연동용

## 설치

```bash
pip install requests
```

## 설정

```python
from Abyssale import AbyssaleClient

client = AbyssaleClient(api_key='your_api_key')
```

## API 액션

### Generate Content
```python
# 템플릿에서 이미지/비디오 생성
content = client.generate_content(
    template_uuid='tpl_xxx',
    format_uuid='fmt_xxx',  # 선택사항 - 지정하지 않으면 모든 포맷 생성
    elements={
        'title': '환영합니다',
        'subtitle': '특별한 할인',
        'image_url': 'https://example.com/image.jpg',
        'color': '#FF5733'
    },
    asynchronous=False
)

# 완료 상태 확인
for fmt in content.formats:
    print(f"{fmt.type} {fmt.width}x{fmt.height}: {fmt.url}")
```

### Get File
```python
file_info = client.get_file('file_id')
print(f"Name: {file_info.name}")
print(f"URL: {file_info.url}")
print(f"Size: {file_info.size}")
```

### Get Generation Status
```python
status = client.get_generation_status('generation_id')
print(f"Status: {status.status}")

# 폴링으로 완료 대기
completed = client.poll_generation('generation_id', max_wait=60)
print(f"Generated: {completed.url}")
```

### Upload File
```python
file = client.upload_file('/path/to/image.jpg')
print(f"Uploaded: {file.url}")
```

### List Templates
```python
templates = client.list_templates()
for template in templates:
    print(f"{template['name']}: {template['id']}")
```

## 트리거

### New Generation
새로운 콘텐츠가 생성될 때 웹훅을 통해 트리거됨

## Elements 예시

```python
elements = {
    # 텍스트 요소
    'title': '배너 제목',
    'subtitle': '부제목',
    'description': '상세 설명',

    # 이미지 요소
    'image_url': 'https://example.com/image.jpg',
    'logo_url': 'https://example.com/logo.png',

    # 스타일 요소
    'color': '#FFFFFF',
    'background_color': '#FF0000',

    # 커스텀 요소
    'button_text': '클릭하세요',
    'price': '$99.00',
    'discount': '50%'
}
```

## API 문서

- Abyssale API: https://docs.abyssale.com/
- API Key 발급: https://app.abyssale.com/

## 라이선스

MIT License
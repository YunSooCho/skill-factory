# BannerBite Integration for Yoom

미디어 생성 API 클라이언트

## 설치
```bash
pip install requests
```

## 사용법
```python
from Bannerbite import BannerBiteClient

client = BannerBiteClient(api_key='your_api_key')

# 프로젝트 리스트
projects = client.list_projects()

# 프로젝트 조회
project = client.get_project('proj_xxx')

# 바이트 검색
bites = client.search_bites_by_project('proj_xxx')

# 미디어 렌더링
media = client.render_media(
    template_id='tpl_xxx',
    data={'title': 'Hello', 'subtitle': 'World'}
)
```

## API 액션
- List Projects
- Get Project
- Search Bites by Project ID
- Get Bite
- Render Media
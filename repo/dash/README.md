# Dash API Client

Dash DAM (Digital Asset Management)용 Python 클라이언트

## 설치

```bash
pip install -r requirements.txt
```

## API Key 획득

1. [Dash 계정 생성](https://www.dashhq.com/)
2. Workspace 설정에서 API key 생성
3. 로그인 후 Settings > API & Integrations 접근
4. Generate API Key 버튼 클릭
5. API 키 복사

## 사용법

### 클라이언트 초기화

```python
from dash_client import DashClient

client = DashClient(api_key='your-api-key')
```

### 에셋 검색

```python
result = client.search_assets(
    query='logo',  # 검색 쿼리
    tags=['branding'],
    asset_type='image',  # image, video, document, audio
    limit=10
)

for asset in result['assets']:
    print(f"{asset['name']}: {asset['url']}")
```

### 에셋 업로드

```python
result = client.upload_asset(
    file_path='/path/to/image.png',
    name='Branding Logo',
    folder_id='folder-123',  # 선택
    tags=['logo', 'brand'],
    metadata={'campaign': 'spring-2024'}
)

asset_id = result['id']
print(f"Uploaded asset with ID: {asset_id}")
```

### 에셋 상세 조회

```python
asset = client.get_asset(asset_id='asset-123')
print(f"Name: {asset['name']}")
print(f"Type: {asset['type']}")
print(f"Size: {asset['size']} bytes")
```

### 에셋 다운로드

```python
# 파일 경로로 저장
saved_path = client.download_asset(
    asset_id='asset-123',
    output_path='/tmp/logo.png'
)
print(f"Saved to: {saved_path}")

# 바이너리로 직접 받기
binary_data = client.download_asset(asset_id='asset-123')
```

### Signed URL 획득

```python
signed_url = client.get_asset_file_url(
    asset_id='asset-123',
    expires_in=3600  # 1시간 유효
)
print(f"Signed URL: {signed_url}")
```

### 에셋 업데이트

```python
client.update_asset(
    asset_id='asset-123',
    name='New Name',
    tags=['updated', 'new-tag'],
    metadata={'status': 'approved'}
)
```

### 에셋 삭제

```python
result = client.delete_asset(asset_id='asset-123')
print(f"Deleted: {result['success']}")
```

## 주요 기능

1. **에셋 검색**: 이름, 태그, 타입, 날짜로 검색
2. **에셋 업로드**: 로컬 파일 서버로 업로드
3. **에셋 다운로드**: 서버에서 로컬로 다운로드
4. **Signed URL**: 안전하게 공유 가능한 URL 생성
5. **메타데이터 관리**: 커스텀 속성 저장

## 에러 처리

```python
from dash_client import DashError, RateLimitError

try:
    asset = client.get_asset('asset-123')
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except DashError as e:
    print(f"API error: {e}")
```

## API 제한

- 기본 제한: 초당 20 요청
- 무료 요금제: 10GB 저장소
- 유료 요금제: 무제한 업로드

## 지원

자세한 API 문서: [Dash Documentation](https://www.dashhq.com/developers/)
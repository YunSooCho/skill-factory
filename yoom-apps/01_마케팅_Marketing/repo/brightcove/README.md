# Brightcove API Integration

Brightcove 비디오 플랫폼의 API를 사용하여 비디오를 관리하는 Python 라이브러리입니다.

## 설치

```bash
pip install requests
```

## 사용법

### 클라이언트 초기화

```python
from brightcove import BrightcoveClient

client = BrightcoveClient(
    account_id="your_account_id",
    client_id="your_client_id",
    client_secret="your_client_secret"
)
```

### 비디오 관리

```python
# 비디오 생성
video = client.create_video(
    name="My Video",
    description="Video description",
    tags=["promo", "marketing"],
    state="ACTIVE"
)
print(f"Video ID: {video['id']}")

# 비디오 조회
video = client.get_video(video_id="video_id_here")

# 비디오 목록
videos = client.list_videos(
    limit=20,
    sort="-created_at",
    tags=["promo"]
)

# 비디오 업데이트
updated = client.update_video(
    video_id="video_id_here",
    name="Updated Name",
    tags=["updated"]
)

# 비디오 삭제
client.delete_video(video_id="video_id_here")
```

### 파일 업로드

```python
# 업로드 URL 생성
upload_info = client.get_upload_url(video_id="video_id_here")
upload_url = upload_info["upload_endpoint"]

# 로컬 파일에서 업로드
client.upload_file_to_url(
    upload_url=upload_url,
    file_path="/path/to/video.mp4"
)
```

### 미디어 인제스트

```python
# Dynamic Ingest
ingest_result = client.ingest_media(
    video_id="video_id_here",
    video_source="s3://bucket/video.mp4",
    source_type="vod",
    profile="multi-platform-standard-static"
)
```

### 전체 워크플로우

```python
# 비디오 생성, 업로드, 인제스트를 한 번에
result = client.upload_and_ingest_video(
    video_name="Complete Video",
    video_file_path="/path/to/video.mp4",
    description="Complete workflow example",
    tags=["workflow", "test"]
)

print(f"Video ID: {result['video_id']}")
print(f"Ingest Job: {result['ingest']['jobId']}")
```

## API 엔드포인트

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/accounts/{account}/videos` | POST | 비디오 생성 |
| `/accounts/{account}/videos/{id}` | GET | 비디오 조회 |
| `/accounts/{account}/videos/{id}` | PATCH | 비디오 업데이트 |
| `/accounts/{account}/videos/{id}` | DELETE | 비디오 삭제 |
| `/accounts/{account}/videos` | GET | 비디오 목록 |
| `/accounts/{account}/videos/{id}/upload-urls` | POST | 업로드 URL 생성 |
| `/accounts/{account}/videos/{id}/ingest-requests` | POST | 미디어 인제스트 |

## API 메서드

| 메서드 | 설명 |
|--------|------|
| `create_video()` | 비디오 생성 |
| `get_video()` | 비디오 조회 |
| `list_videos()` | 비디오 목록 |
| `update_video()` | 비디오 업데이트 |
| `delete_video()` | 비디오 삭제 |
| `get_upload_url()` | 업로드 URL 생성 |
| `upload_file_to_url()` | 파일 업로드 |
| `ingest_media()` | 미디어 인제스트 |
| `upload_and_ingest_video()` | 전체 워크플로우 |

## 예외 처리

```python
from brightcove import BrightcoveClient, BrightcoveAPIError, BrightcoveAuthError, BrightcoveRateLimitError

try:
    video = client.create_video(name="Test Video")
except BrightcoveAuthError as e:
    print("인증 오류:", e)
except BrightcoveRateLimitError as e:
    print("요청 한도 초과:", e)
except BrightcoveAPIError as e:
    print("API 오류:", e)
```

## 인증

Brightcove API는 OAuth 2.0 인증을 사용합니다.

1. [Brightcove Studio](https://studio.brightcove.com/)에서 API 자격 증명 생성
2. Account ID, Client ID, Client Secret 획득
3. 클라이언트 초기화시 이러한 값을 사용

## API 참조

- [Brightcove CMS API](https://apis.support.brightcove.com/cms/index.html)
- [Brightcove Ingest API](https://apis.support.brightcove.com/ingest/index.html)
- [Brightcove OAuth](https://apis.support.brightcove.com/oauth/index.html)
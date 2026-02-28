# Shotstack API 클라이언트

Shotstack를 위한 Python API 클라이언트입니다. 비디오 생성, 오디오 생성, 이미지 생성 및 자산 관리를 지원합니다.

## 개요

Shotstack은 클라우드 기반 비디오 생성 플랫폼으로, 텍스트에서 오디오/이미지 생성, 이미지에서 비디오 생성, 완전한 비디오 렌더링 워크플로우 실행 등의 기능을 제공합니다.

## 설치

의존성 패키지:

```bash
pip install requests
```

또는:

```bash
pip install -r requirements.txt
```

## API 키 발급

1. [Shotstack](https://shotstack.io/)에서 계정 생성
2. 대시보드에서 API 키 발급
3. Stage 또는 Production 환경 키를 선택
4. API 키를 안전하게 저장

## 사용법

### 초기화

```python
from shotstack import ShotstackClient, ShotstackError

client = ShotstackClient(
    api_key="YOUR_API_KEY",
    timeout=60
)
```

### 1. 자산 정보 조회

```python
try:
    asset_info = client.get_asset_information("asset_id_here")
    print("Asset ID:", asset_info.get("id"))
    print("Asset Type:", asset_info.get("type"))
    print("Status:", asset_info.get("status"))
except ShotstackError as e:
    print("Error:", str(e))
```

### 2. 자산 다운로드

```python
try:
    output_path = client.download_asset_data("asset_id_here", "output.mp4")
    print(f"Downloaded to: {output_path}")
except ShotstackError as e:
    print("Error:", str(e))
```

### 3. 텍스트-투-스피치 (TTS) 오디오 생성

```python
try:
    result = client.generate_text_to_speech(
        text="안녕하세요! 반갑습니다.",
        voice="samantha",
        speed=1.0,
        pitch=1.0,
        output_format="mp3"
    )
    print("Audio asset ID:", result.get("assetId"))
except ShotstackError as e:
    print("Error:", str(e))
```

### 4. 워크플로우 작업 시작 (비디오 렌더링)

```python
workflow_config = {
    "timeline": {
        "soundtrack": {
            "src": "https://shotstack-ingest-api-v1-source.s3.amazonaws.com/source/music/example.mp3",
            "effect": "fadeInFadeOut"
        },
        "tracks": [
            {
                "clips": [
                    {
                        "asset": {
                            "type": "html",
                            "html": "<h1>Hello World</h1>",
                            "css": "h1 { color: red; }"
                        },
                        "start": 0,
                        "length": 5
                    }
                ]
            }
        ]
    },
    "output": {
        "format": "mp4",
        "resolution": "hd"
    }
}

try:
    job = client.start_workflow_job(workflow_config)
    print("Render job ID:", job.get("id"))
    print("Status:", job.get("status"))
except ShotstackError as e:
    print("Error:", str(e))
```

### 5. 텍스트-투-이미지 생성

```python
try:
    result = client.generate_text_to_image(
        prompt="A beautiful sunset over the ocean",
        width=1024,
        height=1024,
        num_images=1,
        style="realistic"
    )
    print("Image asset IDs:", result.get("assetIds", []))
except ShotstackError as e:
    print("Error:", str(e))
```

### 6. 파일 목록 조회

```python
try:
    files = client.list_files(limit=50, offset=0)
    print("Total files:", files.get("total", 0))
    for file in files.get("assets", []):
        print(f"- {file.get('id')}: {file.get('type')}")
except ShotstackError as e:
    print("Error:", str(e))
```

### 7. 파일 업로드

```python
try:
    result = client.upload_file(
        "path/to/local/file.mp4",
        file_type="video"
    )
    print("Uploaded asset ID:", result.get("assetId"))
except ShotstackError as e:
    print("Error:", str(e))
```

### 8. 이미지-투-비디오 생성

```python
try:
    result = client.generate_image_to_video(
        image_asset_id="image_asset_id_here",
        duration=5.0,
        motion="zoom",
        audio_asset_id="audio_asset_id_here"  # Optional
    )
    print("Video asset ID:", result.get("assetId"))
except ShotstackError as e:
    print("Error:", str(e))
```

### 렌더링 상태 확인

```python
render_id = "render_job_id_here"
try:
    status = client.get_render_status(render_id)
    print("Status:", status.get("status"))  # "queued", "processing", "finished", "failed"
    if status.get("status") == "finished":
        print("Video URL:", status.get("url"))
except ShotstackError as e:
    print("Error:", str(e))
```

## API 메서드

### get_asset_information
자산의 상세 정보를 조회합니다.

**매개변수:**
- `asset_id` (str): 조회할 자산 ID

**반환값:**
- `dict`: 자산 정보 (ID, 타입, 상태, URL 등)

### download_asset_data
자산을 로컬 파일로 다운로드합니다.

**매개변수:**
- `asset_id` (str): 다운로드할 자산 ID
- `output_path` (str): 저장할 로컬 파일 경로

**반환값:**
- `str`: 다운로드된 파일 경로

### generate_text_to_speech
텍스트를 오디오로 변환합니다.

**매개변수:**
- `text` (str): 변환할 텍스트
- `voice` (str): 음성 (기본값: "samantha")
- `speed` (float): 속도 배수 (기본값: 1.0)
- `pitch` (float): 피치 배수 (기본값: 1.0)
- `output_format` (str): 오디오 형식, "mp3" 또는 "wav" (기본값: "mp3")

**반환값:**
- `dict`: 생성 결과와 자산 ID

### start_workflow_job
비디오 렌더링 워크플로우 작업을 시작합니다.

**매개변수:**
- `workflow_config` (dict): 워크플로우 설정 (timeline, output 등)

**반환값:**
- `dict`: 작업 정보와 작업 ID

### generate_text_to_image
텍스트 프롬프트로 이미지를 생성합니다.

**매개변수:**
- `prompt` (str): 이미지 생성 프롬프트
- `width` (int): 너비 (기본값: 1024)
- `height` (int): 높이 (기본값: 1024)
- `num_images` (int): 생성할 이미지 수 (기본값: 1)
- `style` (str, optional): 스타일

**반환값:**
- `dict`: 생성 결과와 자산 ID 목록

### list_files
업로드된 파일과 자산 목록을 조회합니다.

**매개변수:**
- `limit` (int): 반환할 결과 수 (기본값: 100)
- `offset` (int): 건너뛸 결과 수 (기본값: 0)
- `file_type` (str, optional): 파일 타입 필터

**반환값:**
- `dict`: 파일 목록

### upload_file
파일을 Shotstack에 업로드합니다.

**매개변수:**
- `file_path` (str): 업로드할 로컬 파일 경로
- `file_type` (str, optional): 파일 타입

**반환값:**
- `dict`: 업로드 결과와 자산 ID

### generate_image_to_video
이미지에서 비디오를 생성합니다.

**매개변수:**
- `image_asset_id` (str): 원본 이미지 자산 ID
- `duration` (float): 비디오 길이 (초) (기본값: 5.0)
- `motion` (str, optional): 모션 효과 ("zoom", "pan" 등)
- `audio_asset_id` (str, optional): 배경 오디오 자산 ID

**반환값:**
- `dict`: 생성 결과와 자산 ID

### get_render_status
렌더링 작업의 상태를 조회합니다.

**매개변수:**
- `render_id` (str): 렌더링 작업 ID

**반환값:**
- `dict`: 렌더링 상태

## 에러 처리

```python
from shotstack import ShotstackError, ShotstackRateLimitError, ShotstackAuthenticationError

try:
    result = client.generate_text_to_speech("Hello world")
except ShotstackAuthenticationError:
    print("API 키가 올바르지 않습니다")
except ShotstackRateLimitError:
    print("속도 제한이 초과되었습니다. 잠시 후 다시 시도하세요")
except ShotstackError as e:
    print(f"요청 실패: {str(e)}")
```

## Rate Limiting

API 요청 간 최소 100ms 지연이 자동으로 적용됩니다.

## 예시 코드

### 비디오 생성 전체 예시

```python
from shotstack import ShotstackClient, ShotstackError
import time

client = ShotstackClient(api_key="YOUR_API_KEY")

try:
    # 1. 오디오 생성 (TTS)
    audio_result = client.generate_text_to_speech(
        text="환영합니다! 이것은 자동 생성된 비디오입니다.",
        voice="samantha"
    )
    audio_asset_id = audio_result.get("assetId")
    print(f"Audio asset ID: {audio_asset_id}")

    # 2. 이미지 생성
    image_result = client.generate_text_to_image(
        prompt="Modern office workspace",
        width=1280,
        height=720
    )
    image_asset_id = image_result.get("assetIds", [])[0]
    print(f"Image asset ID: {image_asset_id}")

    # 3. 워크플로우 시작 (비디오 렌더링)
    workflow_config = {
        "timeline": {
            "tracks": [
                {
                    "clips": [
                        {
                            "asset": {
                                "type": "image",
                                "src": f"https://shotstack-api-sources.s3.ap-southeast-2.amazonaws.com/assets/{image_asset_id}"
                            },
                            "start": 0,
                            "length": 5,
                            "transition": {
                                "type": "fade",
                                "duration": 0.5
                            }
                        }
                    ]
                }
            ]
        },
        "output": {
            "format": "mp4",
            "resolution": "hd"
        }
    }

    render_job = client.start_workflow_job(workflow_config)
    render_id = render_job.get("id")
    print(f"Render job ID: {render_id}")

    # 4. 렌더링 상태 확인
    while True:
        status = client.get_render_status(render_id)
        print(f"Status: {status.get('status')}")

        if status.get("status") == "finished":
            print(f"Video ready: {status.get('url')}")
            break
        elif status.get("status") == "failed":
            print("Render failed!")
            break

        time.sleep(5)

except ShotstackError as e:
    print(f"Error: {str(e)}")
```

## 라이선스

MIT License

## 지원

- [Shotstack 공식 사이트](https://shotstack.io/)
- [Shotstack 문서](https://shotstack.io/docs/)
- [API 참조](https://shotstack.io/docs/api/)
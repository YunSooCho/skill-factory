#Shotstack APIクライアント

Shotstack用のPython APIクライアントです。ビデオ生成、オーディオ生成、画像生成、資産管理をサポートします。

## 概要

Shotstackはクラウドベースのビデオ生成プラットフォームで、テキストからオーディオ/画像を生成し、画像からビデオを生成し、完全なビデオレンダリングワークフローを実行するなどの機能を提供します。

## インストール

依存パッケージ：

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## API キー発行

1. [Shotstack](https://shotstack.io/)에서 アカウントの作成
2.ダッシュボードでAPIキーを発行する
3. Stage または Production 環境キーを選択
4. API キーを安全に保存

##使用法

### 初期化

```python
from shotstack import ShotstackClient, ShotstackError

client = ShotstackClient(
    api_key="YOUR_API_KEY",
    timeout=60
)
```

### 1. 資産情報の照会

```python
try:
    asset_info = client.get_asset_information("asset_id_here")
    print("Asset ID:", asset_info.get("id"))
    print("Asset Type:", asset_info.get("type"))
    print("Status:", asset_info.get("status"))
except ShotstackError as e:
    print("Error:", str(e))
```

### 2. 資産のダウンロード

```python
try:
    output_path = client.download_asset_data("asset_id_here", "output.mp4")
    print(f"Downloaded to: {output_path}")
except ShotstackError as e:
    print("Error:", str(e))
```

### 3. テキスト・ツー・スピーチ（TTS）オーディオの生成

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

### 4. ワークフロータスクの開始（ビデオレンダリング）

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

### 5. テキスト・ツー・イメージの生成

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

### 6. ファイルリストの照会

```python
try:
    files = client.list_files(limit=50, offset=0)
    print("Total files:", files.get("total", 0))
    for file in files.get("assets", []):
        print(f"- {file.get('id')}: {file.get('type')}")
except ShotstackError as e:
    print("Error:", str(e))
```

### 7. ファイルのアップロード

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

### 8. 画像ツービデオを作成

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

### レンダリングステータスの確認

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

## APIメソッド

### get_asset_information
資産の詳細情報を照会します。

**パラメータ：**
- `asset_id`（str）：照会する資産ID

**戻り値:**
- `dict`：資産情報（ID、タイプ、ステータス、URLなど）

### download_asset_data
アセットをローカルファイルにダウンロードします。

**パラメータ：**
- `asset_id`（str）：ダウンロードする資産ID
- `output_path`（str）：保存するローカルファイルパス

**戻り値:**
- `str`：ダウンロードされたファイルパス

### generate_text_to_speech
テキストをオーディオに変換します。

**パラメータ：**
- `text`（str）：変換するテキスト
- `voice` (str): 音声 (デフォルト: "samantha")
- `speed`（float）：速度倍数（デフォルト：1.0）
- `pitch`（float）：ピッチ倍数（デフォルト：1.0）
- `output_format`（str）：オーディオフォーマット、「mp3」または「wav」（デフォルト：「mp3」）

**戻り値:**
- `dict`：生成結果と資産ID

### start_workflow_job
ビデオレンダリングワークフロー操作を開始します。

**パラメータ：**
- `workflow_config`（dict）：ワークフロー設定（タイムライン、出力など）

**戻り値:**
- `dict`：ジョブ情報とジョブID

### generate_text_to_image
テキストプロンプトで画像を生成します。

**パラメータ：**
- `prompt`（str）：画像生成のプロンプト
- `width` (int): 幅 (デフォルト: 1024)
- `height`（int）：高さ（デフォルト：1024）
- `num_images`（int）：生成する画像の数（デフォルト：1）
- `style` (str, optional): スタイル

**戻り値:**
- `dict`：生成結果と資産IDのリスト

### list_files
アップロードされたファイルと資産のリストを検索します。

**パラメータ：**
- `limit`（int）：返される結果の数（デフォルト：100）
- `offset`（int）：スキップした結果の数（デフォルト：0）
- `file_type` (str, optional): ファイルタイプフィルタ

**戻り値:**
- `dict`：ファイルリスト

### upload_file
ファイルをShotstackにアップロードします。

**パラメータ：**
- `file_path`（str）：アップロードするローカルファイルパス
- `file_type` (str, optional): ファイルタイプ

**戻り値:**
- `dict`：アップロード結果とアセットID

### generate_image_to_video
画像からビデオを生成します。

**パラメータ：**
- `image_asset_id`（str）：元の画像資産ID
- `duration`（float）：ビデオの長さ（秒）（デフォルト：5.0）
- `motion`（str、optional）：モーション効果（「zoom」、「pan」など）
- `audio_asset_id`（str、optional）：バックグラウンドオーディオアセットID

**戻り値:**
- `dict`：生成結果と資産ID

### get_render_status
レンダリング操作の状態を照会します。

**パラメータ：**
- `render_id`（str）：レンダリングジョブID

**戻り値:**
- `dict`：レンダリングステータス

## エラー処理

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

APIリクエスト間の最低100msの遅延が自動的に適用されます。

## 例コード

### ビデオ生成の完全な例

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

##ライセンス

MIT License

## サポート

- [Shotstack公式サイト]（https://shotstack.io/)
- [Shotstackドキュメント]（https://shotstack.io/docs/)
- [APIリファレンス]（https://shotstack.io/docs/api/)
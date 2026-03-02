#Stability AI APIクライアント

Stability AI用のPython APIクライアント。画像を生成し、編集機能を提供します。

## 概要

Stability AIは、Stable Diffusionベースの最新の画像作成および編集サービスです。さまざまな画像の作成、編集、背景の削除などの機能を提供します。

## インストール

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## API キー発行

1. [Stability AI](https://platform.stability.ai/)에서 アカウントの作成
2. API キー発行
3. API キーを安全に保存

##使用法

### 初期化

```python
from stability_ai import StabilityAIClient, StabilityAIError

client = StabilityAIClient(
    api_key="YOUR_API_KEY",
    timeout=60
)
```

### 1. イメージアウトペインティング(拡張)

```python
try:
    result = client.outpaint_image(
        image="input.jpg",
        prompt="beautiful landscape with mountains",
        left=256,
        right=256,
        top=128,
        bottom=128
    )
    print("Generated images:", result.get("images", []))
except StabilityAIError as e:
    print("Error:", str(e))
```

### 2. イメージの作成 (Stable Image Core)

```python
result = client.generate_image_core(
    prompt="A beautiful sunset over the ocean",
    negative_prompt="blurry, low quality",
    width=1024,
    height=1024,
    steps=30,
    seed=42
)
```

### 3. 高画質画像の生成 (Stable Image Ultra)

```python
result = client.generate_image_ultra(
    prompt="Professional product photo, studio lighting",
    negative_prompt="dark, grainy"
)
```

### 4. オブジェクトの削除

```python
result = client.remove_object(
    image="photo.jpg",
    prompt="remove the person in the background"
)
```

### 5. 背景を削除

```python
result = client.remove_background(
    image="product.png",
    output_format="png"
)
```

### 6. 構造ベースの画像の生成

```python
result = client.generate_from_structure(
    structure="sketch.jpg",
    prompt="modern building design",
    negative_prompt="ugly"
)
```

### 7. イメージインペインティング

```python
result = client.inpaint_image(
    image="photo.jpg",
    mask="mask.png",  # 마스크 (수정할 영역)
    prompt="replace with new content"
)
```

### 8. リファレンスベースの画像を生成する（Ultra）

```python
result = client.generate_from_reference_ultra(
    reference="reference.jpg",
    prompt="similar style, different content",
    strength=0.6
)
```

### 9. スケッチから画像を作成

```python
result = client.generate_from_sketch(
    sketch="drawing.png",
    prompt="convert to realistic photo",
    negative_prompt="cartoonish"
)
```

## APIメソッド

### outpaint_image
画像を選択した方向に拡大します。

### generate_image_core
基本画像の生成(Coreモデル).

### generate_image_ultra
高精細画像生成(Ultraモデル)

### remove_object
画像から不要なオブジェクトを削除します。

### remove_background
画像の背景を削除します。

### generate_from_structure
構造/スケルトンに基づいて画像を作成します。

### inpaint_image
マスクを使用した画像部分の修正。

### generate_from_reference_ultra
参照画像のように生成（Ultra）。

### generate_from_sketch
スケッチ/図面で実写画像を作成します。

## エラー処理

```python
from stability_ai import StabilityAIError, StabilityAIRateLimitError, StabilityAIAuthenticationError

try:
    result = client.generate_image_core("A beautiful landscape")
except StabilityAIAuthenticationError:
    print("API 키가 올바르지 않습니다")
except StabilityAIRateLimitError:
    print("속도 제한이 초과되었습니다")
except StabilityAIError as e:
    print(f"요청 실패: {str(e)}")
```

## Rate Limiting

API リクエスト間に少なくとも 100ms の遅延が適用されます。

##ライセンス

MIT License

## サポート

- [Stability AIプラットフォーム]（https://platform.stability.ai/)
- [APIドキュメント]（https://platform.stability.ai/docs)
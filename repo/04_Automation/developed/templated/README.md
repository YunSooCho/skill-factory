#Templated APIクライアント

Templated用のPython APIクライアント。テンプレートベースの文書の作成とレンダリングをサポートします。

## 概要

テンプレートは、テンプレートを使用してPDF、画像などの文書を自動的に生成するサービスです。

## インストール

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## API キー発行

1. [Templated](https://templated.io/)에서 アカウントの作成
2. API キー発行
3. API キーを安全に保存

##使用法

### 初期化

```python
from templated import TemplatedClient, TemplatedError

client = TemplatedClient(
    api_key="YOUR_API_KEY",
    timeout=60
)
```

###テンプレート検索

```python
result = client.search_templates(
    query="invoice",
    category="business",
    limit=10
)

for template in result.get("templates", []):
    print(f"- {template.get('name')}: {template.get('id')}")
```

###レンダリング

```python
result = client.create_render(
    template_id="template_id_here",
    data={
        "title": "Invoice #001",
        "date": "2024-01-15",
        "items": [
            {"name": "Service A", "amount": 100},
            {"name": "Service B", "amount": 200}
        ],
        "total": 300
    },
    format="pdf"
)

render_id = result.get("render_id")
print(f"Render ID: {render_id}")
```

###画像のアップロード

```python
result = client.upload_image(
    image="logo.png",
    name="company-logo"
)

image_url = result.get("url")
print(f"Image URL: {image_url}")
```

###レンダリングダウンロード

```python
# 메모리에 다운로드
content = client.download_render(render_id)

# 파일로 저장
output_path = client.download_render(render_id, "output.pdf")
print(f"Saved to: {output_path}")
```

### 複数のレンダーをマージ

```python
result = client.merge_renders(
    render_ids=["render1", "render2", "render3"],
    output_format="pdf"
)

merged_render_id = result.get("render_id")
```

### レンダーの状態を確認する

```python
status = client.get_render_status(render_id)
print(f"Status: {status.get('status')}")  # "pending", "completed", "failed"
```

## エラー処理

```python
from templated import TemplatedError, TemplatedRateLimitError, TemplatedAuthenticationError

try:
    result = client.create_render(template_id, data)
except TemplatedAuthenticationError:
    print("API 키가 올바르지 않습니다")
except TemplatedRateLimitError:
    print("속도 제한이 초과되었습니다")
except TemplatedError as e:
    print(f"요청 실패: {str(e)}")
```

##ライセンス

MIT License

## サポート

- [Templated公式サイト]（https://templated.io/)
- [Templatedドキュメント]（https://docs.templated.io/)
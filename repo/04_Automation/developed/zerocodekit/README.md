#ZeroCodeKit APIクライアント

ZeroCodeKit用のPython APIクライアント。さまざまなユーティリティ機能を提供します。

## 概要

ZeroCodeKitは、ファイル変換、コード生成、データ処理など、さまざまなユーティリティ機能を提供するサービスです。

## インストール

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## API キー発行

1. [ZeroCodeKit]（https://zerocodekit.com/)에서アカウントの作成
2. API キー発行
3. API キーを安全に保存

##使用法

### 初期化

```python
from zerocodekit import ZeroCodeKitClient, ZeroCodeKitError

client = ZeroCodeKitClient(
    api_key="YOUR_API_KEY",
    timeout=60
)
```

### 1. DOCXをPDFに変換

```python
result = client.convert_docx_to_pdf("document.docx")
```

### 2. ランダム文字列の生成

```python
result = client.generate_random_string(
    length=12,
    include_numbers=True,
    include_symbols=True
)
```

### 3. 無料メールを確認

```python
result = client.check_free_email("user@gmail.com")
```

### 4. PDF分割

```python
result = client.split_pdf("file.pdf", pages=[1, 2, 3])
```

### 5. バーコードの生成

```python
result = client.generate_barcode(data="123456", barcode_type="QR")
```

### 6. タイムゾーン変換

```python
result = client.convert_timezone(
    datetime_str="2024-01-01 12:00:00",
    from_timezone="UTC",
    to_timezone="Asia/Seoul"
)
```

### 7. 画像の生成

```python
result = client.generate_image(
    prompt="A beautiful landscape",
    size="1024x1024"
)
```

### 8. PDFをBase64に変換

```python
result = client.pdf_to_base64("document.pdf")
```

### 9. HTML/URLをPDFに変換

```python
result = client.html_to_pdf(
    html_content="<h1>Hello World</h1>",
    url="https://example.com"
)
```

### 10. 名前の分割

```python
result = client.split_name("John Doe")
```

### 11. 数値の生成

```python
result = client.generate_number(min_val=1, max_val=1000)
```

### 12. 一時ストレージファイルのアップロード

```python
result = client.upload_temp_file(
    file_data="data.pdf",
    filename="doc.pdf",
    content_type="application/pdf"
)
```

### 13. テキストハッシュ化

```python
result = client.hash_text(text="secret", algorithm="sha256")
```

### 14. ロゴURLの取得

```python
result = client.get_logo_url("example.com")
```

### 15. PDFを画像に変換

```python
result = client.pdf_to_image("file.pdf", page=1)
```

### 16. Pythonコードの生成

```python
result = client.generate_python_code(prompt="Create a function to sort a list")
```

### 17. IPアドレスを地理情報に変換

```python
result = client.ip_to_geolocation(ip_address="8.8.8.8")
```

### 18. JavaScriptコードの生成

```python
result = client.generate_javascript_code(prompt="Create a function to validate email")
```

### 19. QRコードの生成

```python
result = client.generate_qrcode(data="https://example.com", size=300)
```

### 20. サムネイルのインポート

```python
result = client.get_thumbnail(url="https://example.com/image.jpg")
```

### 21. HTML/URLを画像に変換

```python
result = client.html_to_image(
    html_content="<h1>Hello</h1>",
    url="https://example.com"
)
```

## エラー処理

```python
try:
    result = client.generate_image("A cat")
except ZeroCodeKitAuthenticationError:
    print("API 키가 올바르지 않습니다")
except ZeroCodeKitRateLimitError:
    print("속도 제한이 초과되었습니다")
except ZeroCodeKitError as e:
    print(f"요청 실패: {str(e)}")
```

##ライセンス

MIT License

## サポート

- [ZeroCodeKit公式サイト]（https://zerocodekit.com/)
- [ZeroCodeKitドキュメント]（https://docs.zerocodekit.com/)
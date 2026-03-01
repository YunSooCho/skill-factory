# ZeroCodeKit API 클라이언트

ZeroCodeKit를 위한 Python API 클라이언트입니다. 다양한 유틸리티 기능을 제공합니다.

## 개요

ZeroCodeKit은 파일 변환, 코드 생성, 데이터 처리 등 다양한 유틸리티 기능을 제공하는 서비스입니다.

## 설치

```bash
pip install requests
```

또는:

```bash
pip install -r requirements.txt
```

## API 키 발급

1. [ZeroCodeKit](https://zerocodekit.com/)에서 계정 생성
2. API 키 발급
3. API 키를 안전하게 저장

## 사용법

### 초기화

```python
from zerocodekit import ZeroCodeKitClient, ZeroCodeKitError

client = ZeroCodeKitClient(
    api_key="YOUR_API_KEY",
    timeout=60
)
```

### 1. DOCX를 PDF로 변환

```python
result = client.convert_docx_to_pdf("document.docx")
```

### 2. 랜덤 문자열 생성

```python
result = client.generate_random_string(
    length=12,
    include_numbers=True,
    include_symbols=True
)
```

### 3. 무료 이메일 확인

```python
result = client.check_free_email("user@gmail.com")
```

### 4. PDF 분할

```python
result = client.split_pdf("file.pdf", pages=[1, 2, 3])
```

### 5. 바코드 생성

```python
result = client.generate_barcode(data="123456", barcode_type="QR")
```

### 6. 시간대 변환

```python
result = client.convert_timezone(
    datetime_str="2024-01-01 12:00:00",
    from_timezone="UTC",
    to_timezone="Asia/Seoul"
)
```

### 7. 이미지 생성

```python
result = client.generate_image(
    prompt="A beautiful landscape",
    size="1024x1024"
)
```

### 8. PDF를 Base64로 변환

```python
result = client.pdf_to_base64("document.pdf")
```

### 9. HTML/URL을 PDF로 변환

```python
result = client.html_to_pdf(
    html_content="<h1>Hello World</h1>",
    url="https://example.com"
)
```

### 10. 이름 분할

```python
result = client.split_name("John Doe")
```

### 11. 숫자 생성

```python
result = client.generate_number(min_val=1, max_val=1000)
```

### 12. 임시 스토리지 파일 업로드

```python
result = client.upload_temp_file(
    file_data="data.pdf",
    filename="doc.pdf",
    content_type="application/pdf"
)
```

### 13. 텍스트 해시화

```python
result = client.hash_text(text="secret", algorithm="sha256")
```

### 14. 로고 URL 가져오기

```python
result = client.get_logo_url("example.com")
```

### 15. PDF를 이미지로 변환

```python
result = client.pdf_to_image("file.pdf", page=1)
```

### 16. Python 코드 생성

```python
result = client.generate_python_code(prompt="Create a function to sort a list")
```

### 17. IP 주소를 지리 정보로 변환

```python
result = client.ip_to_geolocation(ip_address="8.8.8.8")
```

### 18. JavaScript 코드 생성

```python
result = client.generate_javascript_code(prompt="Create a function to validate email")
```

### 19. QR 코드 생성

```python
result = client.generate_qrcode(data="https://example.com", size=300)
```

### 20. 썸네일 가져오기

```python
result = client.get_thumbnail(url="https://example.com/image.jpg")
```

### 21. HTML/URL을 이미지로 변환

```python
result = client.html_to_image(
    html_content="<h1>Hello</h1>",
    url="https://example.com"
)
```

## 에러 처리

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

## 라이선스

MIT License

## 지원

- [ZeroCodeKit 공식 사이트](https://zerocodekit.com/)
- [ZeroCodeKit 문서](https://docs.zerocodekit.com/)
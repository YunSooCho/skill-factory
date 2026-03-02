# Abstract API Client

Yoom Apps自動化のためのAbstract API統合クライアント。

## サポートする API サービス

|サービス|機能
|--------|------|
| **Exchange Rates API** |リアルタイム為替レートの表示、為替レートの変換|
| **Phone Validation API** |電話番号の検証|
| **Date & Time API** |現在時刻照会、タイムゾーン変換|
| **IP Geolocation API** | IPアドレスベースの地理的情報検索|
| **Email Validation API** |電子メールの検証
| **Holidays API** |国の祝日の照会

## インストール

```bash
pip install -r requirements.txt
```

## API キーの発行方法

1. [Abstract API](https://www.abstractapi.com/) 接続
2. アカウントの作成とログイン
3. DashboardからAPI Keyを発行
4. 環境変数に設定

```bash
export ABSTRACT_API_KEY=your_api_key_here
```

## 使用例

```python
from abstract import AbstractClient

# 클라이언트 초기화 (환경변수 ABSTRACT_API_KEY 필요)
client = AbstractClient()

# 또는 직접 API 키 전달
# client = AbstractClient(api_key="your_api_key_here")

try:
    # 1. 환율 조회
    rates = client.get_live_exchange_rates()
    print(f"Current USD Exchange Rates: {rates}")

    # 환율 변환
    result = client.convert_exchange_rates(100, "USD", "KRW")
    print(f"100 USD = {result.get('total_amount', 'N/A')} KRW")

    # 2. 전화번호 검증
    phone_info = client.validate_phone_number("+8210123456789", "KR")
    print(f"Phone Validation: {phone_info}")

    # 3. 현재 시간 조회
    time_info = client.get_current_time(location="Tokyo")
    print(f"Current Tokyo Time: {time_info}")

    # 시간대 변환
    converted = client.convert_time("Tokyo", "2025-03-02", "12:00", "New York")
    print(f"Tokyo 12:00 = New York {converted}")

    # 4. IP 지리적 정보
    geo_info = client.get_ip_geolocation("8.8.8.8")
    print(f"IP 8.8.8.8 Location: {geo_info}")

    # 5. 이메일 검증
    email_info = client.validate_email("test@example.com")
    print(f"Email Validation: {email_info}")

    # 6. 공휴일 조회
    holidays = client.get_country_holidays("KR", 2025)
    print(f"South Korea 2025 Holidays: {holidays}")

finally:
    client.close()
```

## API詳細

### Exchange Rates API

```python
# 실시간 환율 조회 (USD 기준)
rates = client.get_live_exchange_rates()

# 환율 변환
result = client.convert_exchange_rates(amount=100, base="USD", target="KRW")
```

### Phone Validation API

```python
# 전화번호 유효성 검사
phone_info = client.validate_phone_number("01012345678", "KR")
```

### Date & Time API

```python
# 현재 시간 조회
time_info = client.get_current_time(location="Tokyo")

# 시간대 변환
converted = client.convert_time(
    base_location="Tokyo",
    base_date="2025-03-02",
    base_time="12:00",
    target_location="New York"
)
```

### IP Geolocation API

```python
# IP 지리적 정보 조회
geo_info = client.get_ip_geolocation("8.8.8.8")
```

### Email Validation API

```python
# 이메일 유효성 검사
email_info = client.validate_email("test@example.com")
```

### Holidays API

```python
# 2025년 대한민국 공휴일 조회
holidays = client.get_country_holidays("KR", 2025)
```

## エラー処理

```python
from abstract import AbstractClient
from requests.exceptions import HTTPError

try:
    client = AbstractClient()
    result = client.get_live_exchange_rates()
except ValueError as e:
    print(f"API Key 오류: {e}")
except HTTPError as e:
    print(f"API 요청 실패: {e.response.status_code}")
except Exception as e:
    print(f"오류 발생: {e}")
finally:
    client.close()
```

# Context Managerの使用

```python
from abstract import AbstractClient

with AbstractClient() as client:
    rates = client.get_live_exchange_rates()
    print(rates)
# 자동으로 세선 종료
```

##ライセンス

MIT License
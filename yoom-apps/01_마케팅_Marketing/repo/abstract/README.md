# Abstract API Integration for Yoom

Abstract API 클라이언트 - Yoom 연동용

## 설치

```bash
pip install requests
```

## 설정

```python
from Abstract import AbstractClient

client = AbstractClient(api_key='your_api_key')
```

## API 액션

### Live Exchange Rates
```python
rates = client.live_exchange_rates(base='USD')
print(rates['EUR'])  # 0.95
```

### Convert Exchange Rates
```python
result = client.convert_exchange_rates(
    base='USD',
    target='EUR',
    amount=100
)
print(result['converted_amount'])  # 95.00
```

### Phone Number Validation
```python
validation = client.validate_phone_number(
    phone='+14155552671',
    country='US'
)
print(validation.is_valid)  # True
print(validation.line_type)  # mobile
```

### Get Current Time
```python
time_info = client.get_current_time(timezone='Asia/Seoul')
print(time_info.datetime)  # 2024-02-27 21:49:00
```

### Convert Time
```python
result = client.convert_time(
    base_location='New York',
    base_datetime='2024-02-27 08:00',
    target_location='Tokyo'
)
print(result['datetime'])  # 2024-02-27 22:00
```

### IP Geolocation
```python
geo = client.get_geolocation('8.8.8.8')
print(geo.country)  # United States
print(geo.country_code)  # US
print(geo.city)  # Mountain View
print(geo.latitude)  # 37.40599
print(geo.longitude)  # -122.078514
```

### Email Validation
```python
validation = client.validate_email('test@example.com')
print(validation.is_valid)  # True
print(validation.is_deliverable)  # True
print(validation.quality_score)  # 0.85
```

### Country Holidays
```python
holidays = client.get_country_holidays(country='KR', year=2024)
for holiday in holidays.holidays:
    print(f"{holiday.name}: {holiday.date_iso}")
```

## API 문서

- Abstract API: https://docs.abstractapi.com/
- API Key 발급: https://app.abstractapi.com/

## 라이선스

MIT License
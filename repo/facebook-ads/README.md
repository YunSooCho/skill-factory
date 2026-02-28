# Facebook Ads API 클라이언트

Facebook Ads를 위한 Python API 클라이언트입니다.

## 개요

이 클라이언트는 Facebook Ads API에 접근하여 광고 성과 보고서 및 Webhook 처리를 지원합니다.

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

1. [Meta for Developers](https://developers.facebook.com/)에서 앱 생성
2. Ads 앱 설정에서 Access Token 발급
3. 발급된 Access Token 및 Webhook Secret 저장

## 사용법

### 초기화

```python
from facebook_ads.facebook_ads_client import FacebookAdsClient

client = FacebookAdsClient(
    access_token="YOUR_ACCESS_TOKEN",
    webhook_secret="YOUR_WEBHOOK_SECRET",  # 옵션
    timeout=30
)
```

### 예시 코드

```python
# 광고 계정 보고서 생성
fields = ['impressions', 'clicks', 'spend']
report = client.create_account_report(
    account_id="ACT123456789",
    fields=fields,
    date_preset='last_28d'
)
print("Report:", report)

# 캠페인 보고서
campaign_report = client.create_campaign_report(
    account_id="ACT123456789",
    fields=['campaign_name', 'impressions', 'clicks']
)
print("Campaign report:", campaign_report)
```

## API 액션

- `create_account_report` - 계정 광고 보고서 생성
- `get_account_report` - 계정 광고 보고서 조회
- `create_campaign_report` - 캠페인 보고서 생성
- `get_campaign_report` - 캠페인 보고서 조회
- `create_adset_report` - 광고 세트 보고서 생성
- `get_adset_report` - 광고 세트 보고서 조회
- `create_ad_report` - 광고 보고서 생성
- `get_ad_report` - 광고 보고서 조회

## Webhook 트리거

- **Webhook** - 이 서비스는 Webhook 트리거를 지원합니다

Webhook 설정은 Meta for Developers 페이지에서 수행하십시오.

## 에러 처리

```python
try:
    result = client.create_account_report("ACT123456789", fields=['impressions'])
except Exception as e:
    print("Error:", str(e))
```

## Rate Limiting

API 요청 간 최소 0.1초 지연이 적용됩니다. 너무 많은 요청이 발생하면 Rate Limit 에러가 발생할 수 있습니다.

## 라이선스

MIT License
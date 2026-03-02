#Facebook Ads API クライアント

Facebook Ads用のPython APIクライアント。

## 概要

このクライアントはFacebook Ads APIにアクセスし、広告パフォーマンスレポートとWebhook処理をサポートします。

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

1. [Meta for Developers](https://developers.facebook.com/)에서 アプリの作成
2. Adsアプリ設定でAccess Tokenを発行
3. 発行された Access Token および Webhook Secret の保存

##使用法

### 初期化

```python
from facebook_ads.facebook_ads_client import FacebookAdsClient

client = FacebookAdsClient(
    access_token="YOUR_ACCESS_TOKEN",
    webhook_secret="YOUR_WEBHOOK_SECRET",  # 옵션
    timeout=30
)
```

### サンプルコード

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

## APIアクション

- `create_account_report` - アカウント広告レポートの生成
- `get_account_report` - アカウント広告レポートの検索
- `create_campaign_report` - キャンペーンレポートの生成
- `get_campaign_report` - キャンペーンレポートの照会
- `create_adset_report` - 広告セットレポートの生成
- `get_adset_report` - 広告セットレポートの照会
- `create_ad_report` - 広告レポートの生成
- `get_ad_report` - 広告レポートの照会

## Webhookトリガー

- **Webhook** - このサービスはWebhookトリガーをサポートします

Webhook の設定は、Meta for Developers ページで行います。

## エラー処理

```python
try:
    result = client.create_account_report("ACT123456789", fields=['impressions'])
except Exception as e:
    print("Error:", str(e))
```

## Rate Limiting

APIリクエスト間の最小0.1秒遅延が適用されます。要求が多すぎると、Rate Limitエラーが発生する可能性があります。

##ライセンス

MIT License
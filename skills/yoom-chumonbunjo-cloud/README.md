# Yoom Integration - Chumonbunjo Cloud

Yoom 앱 서비스와 OpenClaw 연계 스킬

## 서비스 정보
- **서비스명**: Chumonbunjo Cloud
- **카テゴリー**: セールス
- **Yoom URL**: https://lp.yoom.fun/apps/chumonbunjo-cloud

## 연계 정보
- **연계 방식**: API
- **인증 방식**: OAuth/API Key
- **API 액ション**: 28個
- **トリガー**: 0個

## 設置

```bash
pip install aiohttp
pip install requests
```

## 環境変数

```bash
YOOM_CHUMONBUNJO-CLOUD_BASE_URL=https://api.example.com
YOOM_CHUMONBUNJO-CLOUD_API_KEY=your_api_key_here
```

## 使い方

```python
from integration import ChumonbunjoCloudClient

client = ChumonbunjoCloudClient()
# 操作実行
```

## テスト

TEST_GUIDE.md 参照

# Agendor テストガイド

## テスト可否
✅ テスト可能 (REST API 기반)

## 事前準備

1. Agendor アカウント (開発者アカウント推奨)
2. `OAuth/API Key` 資格証明を取得
3. 環境変数設定

```bash
export YOOM_AGENDOR_BASE_URL=https://api.agendor.com
export YOOM_AGENDOR_API_KEY=your_key
```

## 基本接続テスト

```python
from integration import AgendorClient

client = AgendorClient()
# 接続成功時は例外が発生しない
```


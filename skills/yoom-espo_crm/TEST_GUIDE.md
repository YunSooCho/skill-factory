# Espo_crm テストガイド

## テスト可否
✅ テスト可能 (REST API 기반)

## 事前準備

1. Espo_crm アカウント (開発者アカウント推奨)
2. `OAuth/API Key` 資格証明を取得
3. 環境変数設定

```bash
export YOOM_ESPO_CRM_BASE_URL=https://api.espo_crm.com
export YOOM_ESPO_CRM_API_KEY=your_key
```

## 基本接続テスト

```python
from integration import Espo_crmClient

client = Espo_crmClient()
# 接続成功時は例外が発生しない
```


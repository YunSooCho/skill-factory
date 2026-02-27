# Next Sfa テストガイド

## テスト可否
✅ テ스트可能 (REST API 기반)

## 環境変数

```bash
YOOM_NEXT_SFA_BASE_URL=https://api.next-sfa.com
YOOM_NEXT_SFA_API_KEY=your_api_key_here
YOOM_NEXT_SFA_AUTH_TOKEN=your_auth_token_here
```

## 依存关系

```bash
pip install aiohttp requests flask
```

## 基本接続テスト

```python
from integration import NextSfaClient

client = NextSfaClient()
```

## トリガー

1. 대응 이력 등록
2. 사안 업데이트
3. 사안 등록
4. 수주 정보 등록
5. 기업 등록
6. 수주 정보 업데이트
7. 대응 이력 업데이트
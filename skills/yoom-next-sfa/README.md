# Yoom Integration - Next Sfa

Yoom 앱 서비스와 OpenClaw 연계 스킬

## 서비스 정보
- **서비스명**: Next Sfa
- **카테고리**: セールス (Sales)
- **Yoom URL**: https://lp.yoom.fun/apps/next-sfa

## 연계 정보
- **연계 방식**: API
- **인증 방식**: OAuth
- **API 액션**: 28개
- **トリガー**: 7개
- **テンプレート**: 6개

## 주요 기능

- **기업 관리**: 기업 등록, 검색, 업데이트
- **사안 관리**: 사안 등록, 검색, 업데이트
- **수주 관리**: 수주 정보 등록, 검색, 업데이트
- **매출 관리**: 매출 정보 관리
- **대응 이력**: 대응 이력 등록, 검색, 업데이트
- **기업 담당자**: 기업 담당자 관리

## 설치

```bash
pip install aiohttp requests flask
```

## 환경 변수

```bash
YOOM_NEXT_SFA_BASE_URL=https://api.next-sfa.com
YOOM_NEXT_SFA_API_KEY=your_api_key_here
YOOM_NEXT_SFA_AUTH_TOKEN=your_auth_token_here
```

## 사용법

```python
from integration import NextSfaClient

client = NextSfaClient()

# 기업 등록
company = await client.register_company(name="ABC 株式会社")

# 사안 등록
opportunity = await client.register_opportunity(company_id=123, opportunity_name="新規案件")

# 수주 등록
order = await client.register_order_info(opportunity_id=456, amount=5000000)
```
# Yoom Integration - Hot Profile

Yoom 앱 서비스와 OpenClaw 연계 스킬

## 서비스 정보
- **서비스명**: Hot Profile
- **カテゴリー**: セールス (Sales)
- **Yoom URL**: https://lp.yoom.fun/apps/hot-profile

## 연계 정보
- **연계 방식**: API
- **인증 방식**: OAuth
- **API 액션**: 31개
- **トリガー**: 13개
- **テンプレート**: 6개

## 주요 기능

- **명사 관리**: 명사 정보 등록, 업데이트, 검색
- **리드 관리**: 리드 검색, 등록, 업데이트
- **상담 관리**: 상담 검색, 등록, 업데이트, 스테이지 관리
- **회사 관리**: 회사 등록, 검색, 업데이트
- **보고 관리**: 보고 관리 등록, 검색, 업데이트
- **상품 마스터**: 상품 마스터 관리
- **테스크**: 테스크 관리

## 설치

```bash
# 기본 의존성
pip install aiohttp

# API 추가 의존성
pip install requests flask

# 웹훅 서버용
pip install flask
```

## 환경 변수

```bash
# Hot Profile API 설정
YOOM_HOT_PROFILE_BASE_URL=https://api.hot-profile.com
YOOM_HOT_PROFILE_API_KEY=your_api_key_here
YOOM_HOT_PROFILE_AUTH_TOKEN=your_auth_token_here  # OAuth 경우
```

## 사용법

### Python API

```python
from integration import HotProfileClient

# 클라이언트 설정
client = HotProfileClient()

# 리드 검색
leads = await client.search_leads(
    keyword="田中"
)

# 명사 정보 등록
name_card = await client.register_name_card(
    name="田中 太郎",
    company="ABC 株式会社",
    email="tanaka@example.com",
    phone="090-1234-5678"
)

# 상담 등록
opportunity = await client.register_opportunity(
    lead_id=12345,
    opportunity_name="新規システム開発案件",
    stage="商談中",
    amount=5000000
)

# 상담 스테이지 업데이트
await client.update_opportunity(
    opportunity_id=67890,
    stage="契約確定"
)
```

### Web훅 트리거 설정

```python
from integration import HotProfileTriggers

triggers = HotProfileTriggers(client)

# 명사 등록 시 트리거
await triggers.on_name_card_registered(lambda data: print("명사가 등록되었습니다:", data))

# 상담 스테이지 업데이트 시 트리거
await triggers.on_opportunity_updated_to_stage(lambda data: print("상담 스테이지가 변경되었습니다:", data))
```

## 테스트

테스트 가이드는 `TEST_GUIDE.md`를 참고하세요.

## API 액션 목록 (完整)

1. 명사의 커스텀 필드 업데이트
2. 보고 관리 업데이트
3. 리드 검색
4. 명사 정보 등록
5. 상담 업데이트
6. 상담의 커스텀 필드 업데이트
7. 상품 마스터 검색
8. 테스크 검색
9. 명사 정보 업데이트
10. 리드 업데이트
11. 회사 등록
12. 회사 검색
13. 리드의 커스텀 필드 업데이트
14. 보고 관리의 커스텀 필드 업데이트
15. 리드 정보 가져오기
16. 상담의 필드 정보 가져오기
17. 상담 검색
18. 상품 마스터 업데이트
19. 보고 관리 등록
20. 회사의 필드 정보 가져오기
21. 상품 마스터 등록
22. 보고 관리 검색
23. 리드의 필드 정보 가져오기
24. 리드 등록
25. 회사 정보 가져오기
26. 회사의 커스텀 필드 업데이트
27. 보고 관리의 필드 정보 가져오기
28. 회사 업데이트
29. 명사의 필드 정보 가져오기
30. 상담 등록
31. 명사 검색

## 트리거 목록

1. 명사가 등록되면
2. 테스크가 업데이트되면
3. 리드가 업데이트되면
4. 회사가 업데이트되면
5. 테스크가 생성되면
6. 보고 관리가 생성되면
7. 보고 관리가 업데이트되면
8. 회사가 생성되면
9. 상담이 생성되면
10. 명사가 업데이트되면
11. 상담이 업데이트되면
12. 리드가 생성되면
13. 상담이 지정된 스테이지로 업데이트되면

## 참고

- Yoom 원본: https://lp.yoom.fun/apps/hot-profile
- 생성일: 2025-02-27
- 작성: OpenClaw
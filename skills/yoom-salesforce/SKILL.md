# Salesforce Yoom 연계 스킬

Salesforce와 OpenClaw 연결을 위한 스킬입니다.

## 연계 정보
- **연계 방식**: SDK (simple-salesforce)
- **인증 방식**: OAuth
- **API 액션**: 95개 (상위 20개만 구현)
- **상세**: 전체 95개 API 액션 - 개별 구현 필요

## 주요 API 액션 (상위 20개)
1. 보고서 다운로드 (レポートをダウンロード)
2. 상담 오브젝트 레코드 업데이트
3. 커스텀 오브젝트 레코드 생성
4. 이메일 메시지 가져오기
5. 이메일 메시지를 인물에 연결
6. 리드 오브젝트에 행동 등록
7. Chatter를 Chatter 그룹에 게시
8. 거래처 오브젝트 레코드 검색
9. 커스텀 오브젝트에 활동 이력 등록
10. 거래처 오브젝트에 활동 이력 등록

## 테스트 가능 여부
✅ 테스트 가능 (SDK 기반)

## 환경 변수
```bash
YOOM_SALESFORCE_BASE_URL=https://yourinstance.my.salesforce.com
YOOM_SALESFORCE_AUTH_TOKEN=your_token
YOOM_SALESFORCE_CLIENT_ID=client_id
YOOM_SALESFORCE_CLIENT_SECRET=client_secret
YOOM_SALESFORCE_USERNAME=username
YOOM_SALESFORCE_PASSWORD=password
```
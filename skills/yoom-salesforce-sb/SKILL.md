# Salesforce Sb Yoom 연계 스킬

Salesforce Sb와 OpenClaw 연결을 위한 스킬입니다.

## 연계 정보
- **연계 방식**: SDK (simple-salesforce)
- **인증 방식**: OAuth
- **API 액션**: 92개 (상위 20개만 구현)

## 주요 API 액션 (상위 20개)
1. 보고서 다운로드
2. 상담 오브젝트 레코드 업데이트
3. 커스텀 오브젝트 레코드 생성
4. 이메일 메시지를 인물에 연결
5. 리드 오브젝트에 행동 등록
...

## 테스트 가능 여부
✅ 테스트 가능 (SDK 기반)

## 환경 변수
```bash
YOOM_SALESFORCE_SB_USERNAME=username
YOOM_SALESFORCE_SB_PASSWORD=password
YOOM_SALESFORCE_SB_AUTH_TOKEN=token
```
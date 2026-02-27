# Yoom Apps 749개 연계 스킬 개발 플랜

## 🎯 프로젝트 목표
- **대상**: Yoom Apps 749개 서비스
- **목표**: 각 서비스별로 OpenClaw 연계 스킬 개발
- **방식**: 하트비트 기반 순차적 추진

## 📊 현재 현황 (2025-02-27)

### 카테고리별 분석 완료 ✅
| 카테고리 | 앱 수 | 연계 점수 |
|---------|------|----------|
| 마케팅 | 161개 | 8.13 |
| 영업 | 81개 | 17.67 |
| 업무일반 | 67개 | 9.15 |
| 오토메이션 | 61개 | 7.13 |
| 프로젝트 관리 | 58개 | 14.67 |
| 회계/경리 | 49개 | 15.53 |
| 인사/노무 | 38개 | 14.45 |
| CS | 36개 | 11.79 |
| Web DB | 27개 | 10.66 |
| 채팅 도구 | 24개 | 11.08 |
| ... 그 외 카테고리 10개 | ~130개 | - |

## 🚀 7단계 추진 계획

### 1단계: 업무(카테고리)별 일람화 ✅ 완료
- [x] 749개 서비스 카테고리 분석
- [x] 연계 점수 산출 (API 액션 + 트리거 + 템플릿)
- [x] 우선순위 정렬 데이터 추출
- [x] 결과 저장: `yoom-analysis/` 폴더

### 2단계: 연계 우선순위 설정 ⏳ 진행 중
#### 우선순위 기준
1. **높음 (High)**: API 액션 10개 이상, SDK 존재, OAuth 지원
2. **중간 (Medium)**: API 액션 5-9개, API 문서 존재
3. **낮음 (Low)**: API 액션 5개 미만, 웹 조작만 가능

#### 타겟 카테고리 (상위 5개)
1. **마케팅 (161개)** - 도구가 많아 ROI 높음
2. **영업 (81개)** - 연계 점수 높음 (17.67)
3. **업무일반 (67개)** - 활용도 높음
4. **프로젝트 관리 (58개)** - 자동화 효과 큼
5. **회계/경리 (49개)** - 데이터 연동 중요

### 3단계: 각 서비스별 연계 방법 설계 ⏳
#### 결정 요소
- **API 기반**: REST API, GraphQL 공식 문서 확인
- **SDK 기반**: Python/JavaScript SDK 존재 시 우선
- **웹 조작**: 로그인 필요, LLM 기반 자동화

#### 설계 템플릿
```yaml
service_name: GitHub
integration_method: [api/sdk/web]
api_documentation: https://docs.github.com/rest
auth_type: [oauth/api_key/token]
automation_feasibility: [high/medium/low]
estimated_cost: [low/medium/high]
```

### 4단계: 자동 연계 가능 서비스 스킬 작성 & 테스트 ⏳
#### 자동 연계 조건
- 공식 API 존재
- 인증 방식이 API Key 또는 OAuth
- Python SDK 제공 (있으면 코스트 절감)

#### 테스트 항목
- [ ] 인증 테스트
- [ ] 기본 CRUD 작동 확인
- [ ] 에러 핸들링 검증

### 5단계: 연계 확인 불가 서비스 스킬 작성 & 매뉴얼 작성 ⏳
#### 웹 조작 기반 스킬
- 로그인/탐색 스텝 명시화
- 캡처 또는 로그 확인 가이드

### 6단계: 749시스템 전체 스킬 작성 완료 ⏳
#### 일정 예상
- 배치 단위: 50개/배치 (총 15배치)
- 하트비트 주기: 2시간
- 예상 완료 기간: 30일 (하루 1배치 기준)

### 7단계: 코스트 최적화 검토 ⏳
#### 코스트 우선순위
1. **SDK 활용** → LLM 호출 최소화
2. **API 직접 호출** → 안정적이고 빠름
3. **LLM 기반 웹 조작** → 최후 수단

## 📋 하트비트 워크플로우

### � 하트비트 수행 태스크
```python
# 하트비트 수행 시마다:
1. 현재 진행 단계 확인 (/Users/clks001/.openclaw/workspace/github/skill-factory/yoom-integration-state.json)
2. 다음 타겟 서비스 로드
3. 서비스 조사:
   - API/SDK 존재 확인
   - 인증 방식 확인
   - 코스트 추정
4. 연계 스킬 작성 (또는 매뉴얼 작성)
5. 진행 상태 업데이트
6. 진행률 보고 (20개 단위로)
```

### 상태 파일 구조
```json
{
  "current_phase": 2,
  "current_batch": 1,
  "current_service_index": 0,
  "services_completed": [],
  "services_in_progress": [],
  "services_pending": [],
  "last_updated": "2025-02-27T14:30:00+09:00"
}
```

## 🛠️ 필요한 파일

### 1. 상태 추적
- `/ Users/clks001/.openclaw/workspace/github/skill-factory/yoom-integration-state.json`
- `/ Users/clks001/.openclaw/workspace/github/skill-factory/yoom-integration-progress.md`

### 2. 스킬 템플릿
- `/ Users/clks001/.openclaw/workspace/github/skill-factory/skills/yoom-integration-template/`
  - SKILL.md
  - api-integration.py (템플릿)
  - web-automation.py (템플릿)

### 3. 결과 저장소
- 각 서비스별 연계 스킬: `skills/yoom-{service-name}/`

## 📌 다음 액션

1. **HEARTBEAT.md 업데이트**: 이 프로젝트의 하트비트 워크플로우 추가
2. **상태 파일 생성**: `yoom-integration-state.json` 초기화
3. **2단계 시작**: 우선순위 설정 및 첫번째 배치(50개) 선정

---
*마지막 업데이트: 2025-02-27 14:30 JST*
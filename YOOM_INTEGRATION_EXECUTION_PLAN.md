# Yoom Apps 749개 연계 스킬 개발 - 실행 플랜 완료

## 📋 프로젝트 개요

- **목표**: Yoom Apps 749개 서비스의 OpenClaw 연계 스킬 개발
- **작성일**: 2025-02-27 14:40 JST
- **현 상태**: 1단계~3단계 완료, 4단계 진행 중

---

## ✅ 완료된 단계

### 1단계: 업무(카테고리)별 일람화 완료 ✅
- **결과**: 749개 서비스 분석 완료
- **카테고리 발견**: 20개
- **상위 카테고리**:
  - 마케팅: 161개
  - 영업: 81개
  - 업무일반: 67개
  - 오토메이션: 61개
  - 프로젝트 관리: 58개
- **저장 위치**: `yoom-analysis/all_apps_analysis.json`

### 2단계: 연계 우선순위 설정 완료 ✅
- **우선순위 기준**:
  - 카테고리 순위 (영업 > 회계/경리 > EC/POS > 수발주 > 파일관리)
  - 연계 점수 (API 액션 + 트리거 + 템플릿)
- **배치 구성**: 15개 배치 (50개/배치)
- **상위 10개 서비스**:
  1. Salesforce
  2. Salesforce Sb
  3. Senses
  4. Zoho CRM Oauth
  5. Hot Profile
  - 모두 우선순위 점수: 150 (HIGH)
- **저장 위치**: `yoom-integration/prioritized_services.json`, `batch_config.json`

### 3단계: 연계 방법 설계 자동화 완료 ✅
- **연계 방식 결정 로직**:
  - API 액션 5개 이상 → API 기반
  - 인기 서비스 (Slack, GitHub, Notion 등) → SDK 기반
  - 그 외 → 웹 조작 기반
- **테스트 완료**: Salesforce 스킬 생성 성공
- **스킬 템플릿**:
  - API 기반: `skills/yoom-integration-template/integration.py`
  - 웹 조작: `skills/yoom-integration-template/web_automation.py`

---

## 🚀 4단계~7단계 실행 방법

### 하트비트 워크플로우

하트비트마다 다음 명령어로 다음 서비스 처리:

```bash
cd /Users/clks001/.openclaw/workspace/github/skill-factory
python3 scripts/yoom_heartbeat_workflow.py --max-services 1
```

**파라미터**:
- `--max-services`: 한 번에 처리할 서비스 수 (기본: 1)

### 크론 설정 (자동화)

매 2시간마다 5개 서비스씩 처리:

```bash
# HEARTBEAT.md에 추가
0 */2 * * * cd /Users/clks001/.openclaw/workspace/github/skill-factory && python3 scripts/yoom_heartbeat_workflow.py --max-services 5
```

---

## 📊 예정 일정

| 단계 | 설명 | 상태 | 예상 완료일 |
|------|------|------|-----------|
| 1 | 카테고리별 일람화 | ✅ 완료 | 2025-02-27 |
| 2 | 연계 우선순위 설정 | ✅ 완료 | 2025-02-27 |
| 3 | 연계 방법 설계 | ✅ 완료 | 2025-02-27 |
| 4 | 자동 연계 스킬 작성 & 테스트 | ⏳ 진행 중 | 2025-03-03 (7일) |
| 5 | 연계 확인 불가 서비스 스킬 & 매뉴얼 | ⏳ 대기 | 2025-03-10 (7일) |
| 6 | 749개 스킬 전체 작성 완료 | ⏳ 대기 | 2025-03-17 (7일) |
| 7 | 코스트 최적화 검토 | ⏳ 대기 | 2025-03-20 (3일) |

**총 예상 기간**: 약 21일 (하루 35개 기준)

---

## 📁 파일 구조

```
/Users/clks001/.openclaw/workspace/github/skill-factory/
├── yoom-analysis/              # 1단계 분석 결과
│   ├── all_apps_analysis.json
│   ├── category_summary.json
│   └── priority_sorted_apps.json
│
├── yoom-integration/           # 2~3단계 결과
│   ├── batch_config.json       # 배치 정보
│   └── prioritized_services.json
│
├── yoom-integration-state.json # 전체 상태 추적
│
├── skills/
│   └── yoom-integration-template/  # 스킬 템플릿
│       ├── SKILL.md
│       ├── integration.py      # API/SDK 템플릿
│       ├── web_automation.py   # 웹 조작 템플릿
│
├── skills/yoom-*/              # 생성된 스킬들 (개별 서비스)
│   ├── yoom-salesforce/
│   ├── yoom-zoho-crm-oauth/
│   └── ...
│
└── scripts/
    ├── analyze_yoom_categories.py   # 1단계 스크립트
    ├── prioritize_services.py       # 2단계 스크립트
    └── yoom_heartbeat_workflow.py   # 3~7단계 자동화
```

---

## 🔑 코스트 최적화 전략

### SDK 활용 (최우선)
**대상**:
- Slack: `slack_sdk`
- GitHub: `PyGithub`
- Notion: `notion-client`
- Google: `google-api-python-client`
- AWS: `boto3`
- Salesforce: `simple-salesforce`

**효과**:
- LLM 호출 최소화 (코드로 직접 처리)
- 안정적이고 빠른 응답
- API 비용 절감

### API 직접 호출
- REST API/GraphQL 사용
- OAuth 또는 API Key 인증
- 중복 호출 결과 캐싱

### LLM 기반 웹 조작 (최후)
- 공식 API가 없는 경우에만 사용
- 로그인/탐색 스텝 명시화
- 테스트 가이드 제공

---

## 📌 다음 액션

### 즉시 실행

```bash
# 현재 진행 상황 확인
cat yoom-integration-state.json

# 다음 5개 서비스 처리
python3 scripts/yoom_heartbeat_workflow.py --max-services 5

# 진행 상황 보고
python3 scripts/progress_report.py  # (생성 필요)
```

### 모니터링 포인트

1. **매 20 완료마다 진행률 보고**
2. **배치 완료 시점 (50개/배치)**
3. **SDK 제공 서비스 식별**
4. **자동화 불가 서비스 목록화**

---

## 📦 포함된 도구

### 1. 카테고리 분석 (`analyze_yoom_categories.py`)
- 749개 서비스 파싱
- 카테고리별 분류
- 연계 점수 산출

### 2. 우선순위 설정 (`prioritize_services.py`)
- 3단계 우선순위 시스템 (HIGH/MEDIUM/LOW)
- 배치 구성 (50개/배치)
- 점수 기반 정렬

### 3. 하트비트 워크플로우 (`yoom_heartbeat_workflow.py`)
- 상태 자동 로드/저장
- 서비스별 연계 방식 결정
- 스킬 자동 생성 (템플릿 기반)
- 진행률 추적

### 4. 스킬 템플릿
- **API 기반**: 인증 + CRUD + 커스텀 액션
- **웹 조작**: Playwright/Selenium 기반 브라우저 자동화
- **자동화 가능 여부 판단**

---

## 🎯 최종 목표

1. ✅ 749개 서비스 카테고리 분류 완료
2. ✅ 우선순위 점수 기반 배치 구성 완료
3. ✅ 스킬 템플릿 및 자동화 스크립트 완료
4. ⏳ 749개 연계 스킬 작성 (진행 중)
5. ⏳ 각 스킬 테스트 및 검증
6. ⏳ 코스트 최적화 검토

---

*마지막 업데이트: 2025-02-27 14:40 JST*
# Skill Factory

**Skill Factory - 자동화된 일본 SaaS 스킬 생성 시스템**

> 일본의 SaaS 시스템을 전부 오픈 클로랑 연동합니다. API가 있든 없든, SDK가 있든 없든, 모든 수단과 방법을 가리지 않고 OpenClaw가 쓸 수 있게 만듭니다.

---

## 🎯 목표

일본 전체 SaaS 생태계를 커버하는 **1000개+ 서비스 스펙**을 자동으로 발견하고 작성하여, OpenClaw가 대량 스킬 생성에 사용할 수 있는 데이터베이스를 구축합니다.

---

## 📊 현재 상태

| 항목 | 수치 |
|-----|------|
| 발견된 서비스 | 11 |
| 스펙 작성 완료 | 11 |
| 서비스별 md 파일 | 16 |
| 하트비트 실행 주기 | 30분 |

---

## 🚀 기능

### 1. 자동 서비스 발견
- `scripts/real_service_discovery.py` - 현재 파이썬 하드코딩 방식
- `industry_service_discovery.py` - 업종별 서비스 분석
- **추후**: 더 동적이고 확장 가능한 방식으로 업그레이드 계획

### 2. 스펙 자동 생성
- `SERVICES_SPEC.md` - 전체 서비스 목록 (업종별 분류)
- `services/*.md` - 서비스별 스펙 파일
- 발견 → 스펙 작성 → Git commit & push 자동화

### 3. 하트비트 자동 실행
- 30분마다 자동으로 서비스 발견과 스펙 업데이트 실행
- OpenClaw 하트비트와 연동하여 수행

---

## 🔄 워크플로우

### 단계별 접근

**1단계: 스펙 대량 생산** (현재 단계)
```
서비스 발견 → 스펙 작성 → Git 저장 (1000개 목표)
```

**2단계: 스킬 생성** (다음 단계)
```
스펙 → AI 스킬 생성 → 테스트 → 배포
```

---

## 🛠️ 사용법

### 하트비트 자동 실행
OpenClaw 하트비트가 30분마다 자동 실행합니다. 별도 설정 없음.

### 수동 실행
```bash
cd /path/to/skill-factory
python3 scripts/real_service_discovery.py
```

### Git push
자동화 스크립트가 commit 후 자동으로 push합니다.

---

## 📁 구조

```
skill-factory/
├── README.md                    # 이 파일
├── SERVICES_SPEC.md            # 11개 서비스 스펙 (업종별 분류)
├── scripts/
│   ├── git_helper.py           # Git 자동화
│   ├── industry_service_discovery.py  # 업종별 분석
│   └── real_service_discovery.py      # 메인 발견 스크립트
├── services/                   # 16개 서비스별 md 파일
└── memory/                     # 하트비트 기록
```

---

## ⚙️ 요구사항

- Python 3.x
- **No external dependencies** - 의존성 없이 실행 가능

---

## 📈 향후 계획

- [ ] 파이썬 하드코딩 방식 → 더 동적인 발견 방식으로 업그레이드
- [ ] 1000개 서비스 스펙 완성
- [ ] 스킬 자동 생성 시스템 개발
- [ ] AI 기반 서비스 발견 알고리즘 고도화

---

## 🤖 사용자

**이 프로젝트의 주 사용자는 AI입니다.**

OpenClaw AI 에이전트가 직접 이 데이터베이스를 사용하여 대량 스킬을 자동 생성합니다.

---

## 📝 License

MIT

---

**Skill Factory** · Made for OpenClaw · by [YunSooCho](https://github.com/YunSooCho)
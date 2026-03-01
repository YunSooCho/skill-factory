# Skill Factory (스킬 팩토리)

> **Skill Factory**는 일본의 전체 SaaS 생태계를 커버하는 대규모 API/SDK 연동 구현체 저장소입니다.  
> 1,000개 이상의 B2B 서비스 스펙을 수집하고, OpenClaw AI가 즉시 활용할 수 있는 형태의 스킬 데이터베이스를 구축하는 것을 목표로 합니다.

---

## 🏗️ 프로젝트 아키텍처 (Kanban Workflow)

이 저장소는 **750개 이상의 서비스**를 효율적으로 관리하고 진척도를 한눈에 파악하기 위해, 디렉토리 구조 자체가 거대한 **칸반 보드(Kanban Board)** 역할을 하도록 설계되었습니다. 거추장스러운 외부 엑셀이나 진척도 추적 스크립트 없이 오직 **파일시스템(폴더 이동)**만으로 상태를 관리합니다.

### 🗂️ 핵심 폴더 구조

전체 751개의 서비스는 용도에 따라 **20개의 비즈니스 카테고리**(예: `01_Marketing`, `06_Accounting`)로 분류되어 `repo/` 디렉토리 아래에 위치합니다.

```text
repo/
├── 01_Marketing/           # 카테고리명
│   ├── developed/          # [To-Do] 개발 및 스펙 수집 완료 (테스트 작성이 필요한 상태)
│   │   ├── activecampaign/
│   │   │   ├── client.py   # API 구현체
│   │   │   └── SPEC.md     # 📄 해당 서비스의 요구사항 및 API 명세서
│   │   └── hubspot/
│   └── verified/           # [Done] 검증 및 테스트 통과 완료 (배포 준비 완료 상태)
│       └── mailchimp/
│           ├── client.py
│           ├── SPEC.md
│           └── tests/      # ✅ 테스트 코드가 작성된 상태
```

---

## 🚀 개발자 & AI 협업 워크플로우

1. **작업 할당 (Pick)**
   - `repo/*/developed/` 폴더 안에서 작업할 서비스를 하나 선택합니다.
   
2. **명세서 확인 및 개발 (Develop & Test)**
   - 해당 서비스 폴더 안에 동봉된 `SPEC.md`를 열고 요구사항을 확인합니다.
   - `client.py`에 API 연동 코드를 구현하고, `tests/` 폴더를 만들어 검증 코드를 작성합니다.

3. **작업 완료 처리 (Move to Verified)**
   - 기능 및 테스트 작성이 100% 완료되면, 해당 서비스의 폴더를 통째로 **`developed/` 에서 `verified/` 로 이동(Move)** 시킵니다.
   - 이 "폴더를 이동하는 행위" 자체가 진척률 상승을 의미하는 물리적 증표가 됩니다.

---

## 📊 진척률 파악 방법

기존에 존재하던 복잡한 Python 진척도 추적 스크립트는 모두 제거되었습니다(Legacy). 
현재 통합 상태나 팀의 생산성을 확인하고 싶다면, 단순히 터미널에서 **`verified` 폴더와 `developed` 폴더의 개수를 세어보는 것**으로 100% 정확한 실시간 진척도를 파악할 수 있습니다.

```bash
# 예시: 검증 완료된 서비스 개수 파악
find repo/ -type d -path "*/verified/*" -mindepth 1 -maxdepth 1 | wc -l
```

---

## ⚙️ 요구사항

- Python 3.10+
- `aiohttp`, `pytest` 등 개별 서비스 `requirements.txt`에 명시된 패키지
- **Zero Configuration**: 복잡한 의존성 없이 즉시 실행 가능하도록 설계

---

## 🤖 대상 사용자

**이 프로젝트의 주 사용자는 AI입니다.**

OpenClaw AI 시스템이 이 저장소의 구조(`client.py`, `SPEC.md`)를 즉시 파싱하여 수백 개의 연동 스킬을 자동 생성하고 서비스형 에이전트에 주입합니다.

---

## 📝 License

MIT License

**Skill Factory** · Made for OpenClaw · by [YunSooCho](https://github.com/YunSooCho)
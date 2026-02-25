# Skill Factory Heartbeat - Auto Service Discovery

## 🧞 작업 (30분마다 자동 실행)

### 1. 서비스 발견 & 스펙 생성
```bash
cd /path/to/skill-factory
python3 scripts/auto_discover.py
```

### 2. Git 자동화
```bash
cd /path/to/skill-factory
python3 scripts/git_helper.py commit --message "feat: Auto-service-discovery" --push
```

## 📁 업데이트 대상

- `SERVICES_SPEC.md` - 전체 서비스 목록
- `services/*.md` - 서비스별 스펙 파일
- `memory/discovered-services.json` - 발견된 서비스 DB
- `memory/heartbeat-log.md` - 하트비트 기록

## 🎯 목표

- 30분마다 최소 10개 새로운 서비스 추가
- 누적 1000개 서비스 스펙 완성
- Git 자동 commit & push
- 중단 없는 자동화 실행

## 🔒 보안

- memory/ 폴더는 .gitignore로 git 제외됨 (내부 DB만 커밋)
- 민감한 정보는 git에 저장되지 않음

---

### 하트비트 명령어 (OpenClaw AI용)

하트비트가 실행될 때:
1. `cd /Users/clks001/.openclaw/workspace/github/skill-factory`
2. `python3 scripts/auto_discover.py` - 자동 서비스 발견 & 스펙 생성
3. `python3 scripts/git_helper.py commit --message "feat: Auto-service-discovery $(date)" --push` - Git 자동화
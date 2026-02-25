# Skill Factory Heartbeat - AI-led Service Discovery

## 🧞 작업 (30분마다 자동 실행)

하트비트 트리거 시, **skill-factory-service-finder 스킬을 사용하여**: 1. AI 분석: SERVICES_SPEC.md 읽고 부족한 분야 식별
2. AI 발견: 부족한 분야 기반으로 웹 검색 & 서비스 발견 (최소 10개)
3. AI 등록: SERVICES_SPEC.md 업데이트 (단일 테이블)
4. Git 자동화 (선택): commit & push

## 📁 업데이트 대상

- `SERVICES_SPEC.md` - 전체 서비스 목록 (단일 테이블)

## 🎯 목표

- 30분마다 최소 10개 새로운 서비스 추가
- 누적 1000개 서비스 스펙 완성
- AI가 주도적으로 서비스 발견

---

### 하트비트 명령어 (OpenClaw AI용)

하트비트가 실행될 때:
1. `cd /Users/clks001/.openclaw/workspace/github/skill-factory`
2. AI 분석:
   - `cat SERVICES_SPEC.md` - 현재 서비스 목록 read
   - 부족한 분야/카테고리 식별
   - 새로운 분야나 빈 공간 도출
3. AI 발견:
   - 부족한 분야를 기반으로 웹 검색
   - 각 분야에서 최소 10개 새로운 서비스 발견
4. AI 등록:
   - `SERVICES_SPEC.md` 업데이트 (단일 테이블에 추가)
   - 포맷: `| # | サービス | カテゴリー | ホームページ |` 유지
5. Git 자동화 (선택):
   - `git add SERVICES_SPEC.md && git commit -m "feat: AI-led service discovery" && git push`
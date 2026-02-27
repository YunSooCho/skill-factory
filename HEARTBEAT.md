# HEARTBEAT.md

## 하트비트 워크플로우

하트비트마다 다음 순서로 Yoom Apps 연계 스킬을 개발합니다:

### 1. 서비스 발견 (기존)
```bash
python3 scripts/real_service_discovery.py
```

### 2. 정밀 연계 스킬 개발 (신규)
```bash
python3 scripts/yoom_detailed_integration.py --max-services 5
```

**설명**:
- 카테고리별 우선순위에 따라 다음 서비스 선택
- Yoom MD 파일에서 API 액션, 트리거, 템플릿 추출
- 각 API 액션/트리거 별로 꼼꼼히 스킬 구현
- 테스트 가능 여부와 필요한 자격증명 기재
- `YOOM_INTEGRATION_PROGRESS.md`에 진척 상황 업데이트

**처리 서비스 수**: `--max-services`로 조절 (기본: 1개, 권장: 3-5개/하트비트)

### 3. Git 커밋 & 푸시
```bash
git add -A && git commit -m "Add Yoom integration skills" && git push
```

---

## 실행 주기

**권장**: 30분마다 3-5개 서비스 처리
- 749개 서비스 / 5개/하트비트 = 약 150 하트비트
- 30분 간격 = 약 75시간 = 약 3일

**빠르게**: 2-3분마다 1개 서비스 처리
- 749개 서비스 / 1개/하트비트 = 749 하트비트
- 2분 간격 = 약 1500분 = 약 25시간

---

## 예약 실행 (Cron)

```bash
# 매 30분마다 5개 서비스 처리
*/30 * * * * cd /Users/clks001/.openclaw/workspace/github/skill-factory && python3 scripts/yoom_detailed_integration.py --max-services 5 && git add -A && git commit -m "heartbeat: add Yoom skills" && git push

# 또는 2분마다 1개 서비스 처리 (빠르게 완료)
*/2 * * * * cd /Users/clks001/.openclaw/workspace/github/skill-factory && python3 scripts/yoom_detailed_integration.py --max-services 1
```
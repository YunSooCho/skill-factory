#!/usr/bin/env python3
"""
Yoom Apps 연계 우선순위 설정 및 배치 구성
"""

import json
from pathlib import Path

ANALYSIS_DIR = Path(__file__).parent.parent / "yoom-analysis"
STATE_FILE = Path(__file__).parent.parent / "yoom-integration-state.json"
OUTPUT_DIR = Path(__file__).parent.parent / "yoom-integration"
OUTPUT_DIR.mkdir(exist_ok=True)

# 우선순위 카테고리 (점수 높은 순)
PRIORITY_CATEGORIES = [
    "** セールス",           # 81개, 점수 17.67 (최고)
    "** 会計・経理",         # 49개, 점수 15.53
    "** EC・POSシステム",    # 19개, 점수 16.37
    "** 受発注・在庫管理",   # 18개, 점수 15.33
    "** ファイル管理",        # 12개, 점수 15.47
    "** ワークフロー",        # 9개,  점수 14.71
    "** プロジェクト管理",    # 58개, 점수 14.67
    "** 人事・労務",          # 38개, 점수 14.45
    "** 契約締結",           # 18개, 점수 12.01
    "** 決済",               # 14개, 점수 11.14

    # 중간 우선순위
    "** カスタマーサポート", # 36개, 점수 11.79
    "** Webデータベース",     # 27개, 점수 10.66
    "** ナレッジベース",      # 5개,  점수 9.88
    "** 業務一般",          # 67개, 점수 9.15
    "** チャットツール",     # 24개, 점수 11.08

    # 낮은 우선순위
    "** マーケティング",     # 161개, 점수 8.13 (개수 많음)
    "** カレンダー",         # 11개, 점수 7.22
    "** Webサイト制作",      # 18개, 점수 7.14
    "** オートメーション",    # 61개, 점수 7.13
    "** 入力フォーム",       # 23개, 점수 4.38 (최저)
]

def calculate_priority_score(app):
    """
    우선순위 점수 계산:

    1. 카테고리 순위 (상위일수록 높은 점수)
    2. 연계 점수 (API/트리거/템플릿 합산)
    3. 인기도/사용성
    """
    # 카테고리 순위 점수 (0-100, 높을수록 우선)
    cat_rank_score = 100
    try:
        cat_rank = PRIORITY_CATEGORIES.index(app["category"])
        cat_rank_score = 100 - (cat_rank * 5)  # 순위가 낮을수록 점수 감소
    except ValueError:
        cat_rank_score = 0  # 목록에 없는 카테고리

    # 연계 점수 정규화 (0-50)
    integration_score = min(50, app["integration_score"] * 3)

    # 총점
    total_score = cat_rank_score + integration_score

    return {
        "priority_score": total_score,
        "category_priority_score": cat_rank_score,
        "integration_score": integration_score,
        "priority_level": determine_priority_level(total_score)
    }

def determine_priority_level(total_score):
    if total_score >= 120:
        return "HIGH"
    elif total_score >= 80:
        return "MEDIUM"
    else:
        return "LOW"

def main():
    print("🔍 우선순위 설정 시작...")

    # 분석 결과 로드
    analysis_file = ANALYSIS_DIR / "priority_sorted_apps.json"
    with open(analysis_file, 'r', encoding='utf-8') as f:
        apps = json.load(f)

    print(f"📊 {len(apps)}개 서비스 로드 완료")

    # 각 앱의 우선순위 점수 계산
    prioritized_apps = []
    for app in apps:
        priority_data = calculate_priority_score(app)
        app.update(priority_data)
        prioritized_apps.append(app)

    # 우선순위 점수로 정렬
    prioritized_apps.sort(key=lambda x: x["priority_score"], reverse=True)

    # 배치 생성 (50개씩)
    BATCH_SIZE = 50
    batches = []
    for i in range(0, len(prioritized_apps), BATCH_SIZE):
        batch = prioritized_apps[i:i+BATCH_SIZE]
        batches.append({
            "batch_number": len(batches) + 1,
            "size": len(batch),
            "services": batch,
            "summary": {
                "high_priority": len([s for s in batch if s["priority_level"] == "HIGH"]),
                "medium_priority": len([s for s in batch if s["priority_level"] == "MEDIUM"]),
                "low_priority": len([s for s in batch if s["priority_level"] == "LOW"])
            }
        })

    # 결과 저장
    (OUTPUT_DIR / "prioritized_services.json").write_text(
        json.dumps(prioritized_apps, ensure_ascii=False, indent=2)
    )

    (OUTPUT_DIR / "batch_config.json").write_text(
        json.dumps(batches, ensure_ascii=False, indent=2)
    )

    # 상태 파일 업데이트
    with open(STATE_FILE, 'r', encoding='utf-8') as f:
        state = json.load(f)

    state["phase"]["2"]["status"] = "completed"
    state["phase"]["2"]["completed_at"] = "2025-02-27T14:35:00+09:00"
    state["phase"]["3"]["status"] = "in_progress"
    state["stats"]["current_batch_services"] = batches[0]["services"]
    state["stats"]["batch_progress"]["services_in_current_batch"] = batches[0]["size"]

    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 우선순위 설정 완료")
    print(f"   - 총 {len(batches)}개 배치 생성")
    print(f"   - 상위 10개 서비스:")

    for i, app in enumerate(prioritized_apps[:10], 1):
        print(f"     {i}. {app['service_name']} ({app['category']}) - 점수: {app['priority_score']:.1f} ({app['priority_level']})")

    # 배치 요약
    print(f"\n📋 배치 현황:")
    for batch in batches[:3]:
        total = batch["summary"]["high_priority"] + batch["summary"]["medium_priority"] + batch["summary"]["low_priority"]
        print(f"   배치 #{batch['batch_number']}: {batch['size']}개 "
              f"(HIGH: {batch['summary']['high_priority']}, "
              f"MEDIUM: {batch['summary']['medium_priority']}, "
              f"LOW: {batch['summary']['low_priority']})")

    print(f"\n📁 결과 저장 위치:")
    print(f"   - {OUTPUT_DIR / 'prioritized_services.json'}")
    print(f"   - {OUTPUT_DIR / 'batch_config.json'}")

if __name__ == "__main__":
    main()
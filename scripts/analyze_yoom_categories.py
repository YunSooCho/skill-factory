#!/usr/bin/env python3
"""
Yoom Apps 749개 서비스를 카테고리별로 분류하고 분석하는 스크립트
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict
import hashlib

YOOM_APPS_DIR = Path(__file__).parent.parent / "yoom-apps"
OUTPUT_DIR = Path(__file__).parent.parent / "yoom-analysis"
OUTPUT_DIR.mkdir(exist_ok=True)

def parse_yoom_app(file_path):
    """Yoom app markdown 파일 파싱"""
    content = file_path.read_text()

    # 기본 정보 추출
    service_name = re.search(r'サービス名:\s*(.+)', content)
    url = re.search(r'URL:\s*(.+)', content)
    category = re.search(r'カテゴリー:\s*(.+)', content)

    # API 액션 수 추출
    api_actions = re.search(r'APIアクション.*?(\d+)個', content)
    api_actions_count = int(api_actions.group(1)) if api_actions else 0

    # 트리거 수 추출
    triggers = re.search(r'トリガー.*?(\d+)個', content)
    triggers_count = int(triggers.group(1)) if triggers else 0

    # 템플릿 수 추출
    templates = re.search(r'テンプレート.*?(\d+)개', content)
    templates_count = int(templates.group(1)) if templates else 0

    return {
        "file": file_path.stem,
        "service_name": service_name.group(1).strip() if service_name else file_path.stem,
        "url": url.group(1).strip() if url else None,
        "category": category.group(1).strip() if category else "분류안됨",
        "api_actions": api_actions_count,
        "triggers": triggers_count,
        "templates": templates_count,
        "integration_score": api_actions_count + triggers_count * 0.5 + templates_count * 0.3
    }

def analyze_all_apps():
    """모든 Yoom Apps 분석"""
    apps = []

    for md_file in sorted(YOOM_APPS_DIR.glob("*.md")):
        app_data = parse_yoom_app(md_file)
        apps.append(app_data)

    return apps

def categorize_apps(apps):
    """카테고리별로 앱 그룹화"""
    categories = defaultdict(list)

    for app in apps:
        categories[app["category"]].append(app)

    return categories

def main():
    print("🔍 Yoom Apps 분석 시작...")

    # 모든 앱 분석
    apps = analyze_all_apps()
    print(f"📊 총 {len(apps)}개 앱 분석 완료")

    # 카테고리별 분류
    categories = categorize_apps(apps)

    # 결과 저장
    result = {
        "total_apps": len(apps),
        "total_categories": len(categories),
        "categories": {
            cat: {
                "count": len(apps_list),
                "apps": apps_list
            } for cat, apps_list in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True)
        }
    }

    # 전체 분석 결과 저장
    (OUTPUT_DIR / "all_apps_analysis.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2)
    )

    # 카테고리별 요약
    summary = []
    for cat, data in sorted(result["categories"].items(), key=lambda x: x[1]["count"], reverse=True):
        summary.append({
            "category": cat,
            "count": data["count"],
            "integration_score": sum(app["integration_score"] for app in data["apps"]) / data["count"] if data["count"] > 0 else 0
        })

    (OUTPUT_DIR / "category_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2)
    )

    # 우선순위 정렬 (연계 점수순)
    sorted_apps = sorted(apps, key=lambda x: x["integration_score"], reverse=True)
    (OUTPUT_DIR / "priority_sorted_apps.json").write_text(
        json.dumps(sorted_apps, ensure_ascii=False, indent=2)
    )

    print(f"✅ 분석 결과 저장 완료:")
    print(f"   - {OUTPUT_DIR / 'all_apps_analysis.json'}")
    print(f"   - {OUTPUT_DIR / 'category_summary.json'}")
    print(f"   - {OUTPUT_DIR / 'priority_sorted_apps.json'}")

    # 요약 출력
    print(f"\n📋 카테고리별 현황:")
    for cat, data in sorted(result["categories"].items(), key=lambda x: x[1]["count"], reverse=True)[:10]:
        print(f"   {cat}: {data['count']}개")

if __name__ == "__main__":
    main()
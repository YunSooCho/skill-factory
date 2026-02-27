#!/usr/bin/env python3
"""
Yoom Apps Integration - 실제 연계 사양 기반 스킬 개발

각 서비스의 연계 사양(API 액션/트리거/템플릿)을 웹 리서치하여 실제 구현
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional

# 경로 설정
WORKSPACE = Path(__file__).parent.parent
YOOM_APPS_DIR = WORKSPACE / "yoom-apps"
STATE_FILE = WORKSPACE / "yoom-integration-state.json"
SKILLS_DIR = WORKSPACE / "skills"

class ServiceIntegrator:
    """
    서비스별 연계 사양 기반 스킬 개발자
    """

    def __init__(self, service_file: str):
        self.service_file = service_file
        self.md_file = YOOM_APPS_DIR / f"{service_file}.md"

        if not self.md_file.exists():
            raise FileNotFoundError(f"{service_file}.md 파일이 존재하지 않습니다.")

        # MD 파일 파싱
        self.spec = self.parse_md_file()

    def parse_md_file(self) -> Dict:
        """
        Yoom Apps MD 파일 파싱

        Returns:
            {
                "service_name": str,
                "url": str,
                "category": str,
                "api_actions": [
                    {"name": str, "description": str},
                    ...
                ],
                "triggers": [
                    {"name": str, "description": str},
                    ...
                ],
                "templates": [
                    {"name": str, "url": str},
                    ...
                ]
            }
        """
        content = self.md_file.read_text()

        spec = {
            "service_name": "",
            "url": "",
            "category": "",
            "api_actions": [],
            "triggers": [],
            "templates": []
        }

        # 기본 정보
        service_name = re.search(r'サービス名:\s*(.+)', content)
        url = re.search(r'URL:\s*(.+)', content)
        category = re.search(r'カテゴリー:\s*(.+)', content)

        if service_name:
            spec["service_name"] = service_name.group(1).strip()
        if url:
            spec["url"] = url.group(1).strip()
        if category:
            spec["category"] = category.group(1).strip()

        # API 액션 추출
        api_section = re.search(r'### APIアクション一覧:.*?(?=\n###|\n##)', content, re.DOTALL)
        if api_section:
            actions_text = api_section.group(0)
            # 번호 리스트 추출 (1. **Action Name**)
            actions = re.findall(r'\d+\.\s+\*\*(.+?)\*\*\n?', actions_text)
            for action in actions:
                spec["api_actions"].append({
                    "name": action.strip(),
                    "description": ""
                })

        # 트리거 추출
        trigger_section = re.search(r'### トリガー一覧:.*?(?=\n###|\n##)', content, re.DOTALL)
        if trigger_section:
            triggers_text = trigger_section.group(0)
            triggers = re.findall(r'\d+\.\s+\*\*(.+?)\*\*\n?', triggers_text)
            for trigger in triggers:
                spec["triggers"].append({
                    "name": trigger.strip(),
                    "description": ""
                })

        # 템플릿 추출
        template_section = re.search(r'### テンプレート一覧:.*?(?=\n##|\Z)', content, re.DOTALL)
        if template_section:
            templates_text = template_section.group(0)
            # URL 추출
            template_urls = re.findall(r'\[テンプレート\]\((.+?)\)', templates_text)
            for url in template_urls:
                spec["templates"].append({
                    "name": "template",
                    "url": url.strip()
                })

        return spec

    def generate_research_query(self) -> List[str]:
        """
        웹 리서치용 쿼리 생성

        Returns:
            서비스 API/SDK 검색어 리스트
        """
        service_name = self.spec["service_name"]
        queries = []

        # 기본 API 검색
        queries.append(f"{service_name} API documentation")

        # 공식 API 사이트 포착
        queries.append(f"{service_name} REST API endpoints")

        # SDK 검색
        queries.append(f"{service_name} Python SDK")

        # 인증 방식
        queries.append(f"{service_name} API authentication")

        return queries

    def print_spec(self):
        """연계 사양 출력"""
        print("=" * 70)
        print(f"🔍 서비스 연계 사양: {self.spec['service_name']}")
        print("=" * 70)
        print(f"   📁 파일: {self.service_file}.md")
        print(f"   🌐 URL: {self.spec['url']}")
        print(f"   📂 카테고리: {self.spec['category']}")
        print()
        print(f"   🔄 API 액션 ({len(self.spec['api_actions'])}개):")
        for i, action in enumerate(self.spec['api_actions'], 1):
            print(f"      {i}. {action['name']}")
        print()
        print(f"   🎯 트리거 ({len(self.spec['triggers'])}개):")
        for i, trigger in enumerate(self.spec['triggers'], 1):
            print(f"      {i}. {trigger['name']}")
        print()
        print(f"   📋 템플릿 ({len(self.spec['templates'])}개):")
        for i, template in enumerate(self.spec['templates'][:3], 1):
            print(f"      {i}. {template['url']}")
        if len(self.spec['templates']) > 3:
            print(f"      ... 외 {len(self.spec['templates'])-3}개")
        print()
        print("=" * 70)
        print("🔎 웹 리서치용 검색어:")
        for i, query in enumerate(self.generate_research_query(), 1):
            print(f"   {i}. {query}")
        print("=" * 70)

    def export_spec(self) -> Dict:
        """연계 사양 JSON으로 내보내기"""
        return self.spec

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Yoom Apps Service Spec Parser")
    parser.add_argument("service_file", help="서비스 파일명 (확장자 제외, 예: pinterest)")
    parser.add_argument("--export", action="store_true", help="JSON으로 내보내기")

    args = parser.parse_args()

    try:
        integrator = ServiceIntegrator(args.service_file)
        integrator.print_spec()

        if args.export:
            spec_json = integrator.export_spec()
            output_file = WORKSPACE / f"yoom-integration/{args.service_file}_spec.json"

            # 디렉토리 생성
            output_file.parent.mkdir(parents=True, exist_ok=True)

            output_file.write_text(
                json.dumps(spec_json, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )

            print(f"\n✅ 스펙 내보내기 완료: {output_file}")

    except Exception as e:
        print(f"❌ 에러: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
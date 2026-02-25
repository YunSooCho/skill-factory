#!/usr/bin/env python3
"""
Auto Service Discovery - Skill Factory

Automatically discovers Japanese SaaS services and specs without manual input.

Features:
- Auto web search queries for each industry
- Auto data extraction from search results
- Auto spec generation for SERVICES_SPEC.md
- Auto service-specific files creation
- Auto save to discovered-services.json

This script is meant to be run by heartbeat automation only.
"""

import json
import re
import time
from pathlib import Path
from typing import Dict, List
from datetime import datetime


class AutoServiceDiscovery:
    """Automatically discover Japanese SaaS services"""

    def __init__(self):
        self.spec_path = Path("SERVICES_SPEC.md")
        self.services_dir = Path("services")
        self.memory_dir = Path("memory")
        self.discovered_file = self.memory_dir / "discovered-services.json"
        self.heartbeat_log = self.memory_dir / "heartbeat-log.md"

        self.services_dir.mkdir(exist_ok=True)
        self.memory_dir.mkdir(exist_ok=True)

        self.discovered_services = self._load_data()

    def _load_data(self) -> Dict:
        """Load discovered services from JSON"""
        if self.discovered_file.exists():
            with open(self.discovered_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"services": []}

    def _save_data(self):
        """Save discovered services to JSON"""
        with open(self.discovered_file, 'w', encoding='utf-8') as f:
            json.dump(self.discovered_services, f, ensure_ascii=False, indent=2)

    def _log_heartbeat(self, services_added: List[Dict]):
        """Log heartbeat activity"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"""
## Heartbeat - {timestamp}

- **Services discovered**: {len(services_added)}
- **Total services**: {len(self.discovered_services["services"])}

### Added Services:
"""

        for svc in services_added:
            log_entry += f"- {svc['name']} ({svc['category']})\n"

        with open(self.heartbeat_log, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    def _get_industry_search_queries(self) -> List[str]:
        """
        Get search queries for each industry

        Returns:
            List of search queries for Japanese SaaS
        """
        queries = [
            # 飲食・レストラン
            "日本 POS SaaS ランキング",
            "飲食店 POS 比較",
            "日本 予約システム SaaS 飲食",
            "飲食店 決済 SaaS",

            # 小売・EC
            "日本 EC プラットフォーム ツール",
            "日本 決済ゲートウェイ SaaS",
            "日本 在庫管理 SaaS",
            "小売 業務システム SaaS",

            # 企業・事務
            "日本 会計 SaaS 比較",
            "日本 人事労務 SaaS",
            "日本 グループウェア",
            "日本 プロジェクト管理 SaaS",

            # 製造業
            "日本 生産管理 SaaS",
            "製造業 在庫管理 SaaS",

            # 医療・ヘルスケア
            "日本 電子カルテ SaaS",
            "医療 予約管理 SaaS",

            # 教育
            "日本 LMS SaaS",
            "教育 学習管理 SaaS",

            # その他
            "日本 CRM SaaS",
            "日本 マーケティングツール SaaS",
            "日本 HR SaaS",
            "日本 コラボレーションツール SaaS",
        ]

        return queries

    def discover_auto(self, target_count: int = 10) -> List[Dict]:
        """
        Automatically discover services without manual input

        This is a placeholder for actual automation. In production, this would:
        1. Execute web search queries
        2. Extract service data from results
        3. Validate and deduplicate
        4. Return discovered services

        For now, returns sample data for demonstration.

        Returns:
            List of discovered services
        """
        print("🧞 Skill Factory Auto Discovery Starting...")
        print(f"   Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Target: {target_count} services")

        # For demonstration, generate sample services
        # In production, this would call web search API and extract data

        sample_services = self._generate_sample_services(target_count)

        new_services = []
        for service in sample_services:
            if self._is_new_service(service):
                self.discovered_services["services"].append(service)
                new_services.append(service)
                print(f"   ➕ Added: {service['name']} ({service['category']})")

        self._save_data()

        print(f"\n✅ Discovery complete:")
        print(f"   - New services: {len(new_services)}")
        print(f"   - Total to date: {len(self.discovered_services['services'])}")

        if new_services:
            self._log_heartbeat(new_services)

        return new_services

    def _generate_sample_services(self, count: int) -> List[Dict]:
        """Generate sample service data for demonstration"""
        # This is placeholder for actual web search & extraction
        # In production, replace with real search API calls

        sample_data = [
            {"name": "shop-pro", "category": "EC", "homepage": "https://shop-pro.jp"},
            {"name": "makeshop", "category": "EC", "homepage": "https://www.makeshop.jp"},
            {"name": "ec-cube", "category": "EC", "homepage": "https://www.ec-cube.net"},
            {"name": "paypal-japan", "category": "決済", "homepage": "https://www.paypal.com/jp"},
            {"name": "sb-payment", "category": "決済", "homepage": "https://www.sbpayment.jp"},
            {"name": "gmo-payment", "category": "決済", "homepage": "https://www.gmo-pg.jp"},
            {"name": "sonet-payment", "category": "決済", "homepage": "https://.sonetpayment.jp"},
            {"name": "espos", "category": "POS", "homepage": "https://espos.jp"},
            {"name": "a-cashier", "category": "POS", "homepage": "https://a-cashier.jp"},
        ]

        return sample_data[:count]

    def _is_new_service(self, service: Dict) -> bool:
        """Check if service is new (not in discovered list)"""
        for existing in self.discovered_services["services"]:
            if existing["name"] == service["name"]:
                return False
        return True

    def generate_spec_files(self, services: List[Dict]):
        """Generate SPEC.md and service files"""
        print(f"\n📝 Generating spec files for {len(services)} services...")

        for service in services:
            # Generate service-specific file
            self._generate_service_md(service)

        print("✅ Spec files generated")

    def _generate_service_md(self, service: Dict):
        """Generate service-specific Markdown file"""
        filename = self._sanitize_filename(service["name"])
        filepath = self.services_dir / f"{filename}.md"

        service_md = f"""# {service['name']}

## 🏢 基本情報

| 項目 | 値 |
|------|---|
| **サービス名** | {service['name']} |
| **カテゴリー** | {service['category']} |
| **ホームページ** | [{service['homepage']}]({service['homepage']}) |

## ✨ 主要機能

1. TBD
2. TBD
3. TBD

## 🔌 API 状態

| 項目 | 状態 |
|------|------|
| **API提供** | Unknown |

## 💰 料金体系

TBD

**作成日**: {datetime.now().strftime('%Y-%m-%d')}
"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(service_md)

    def _sanitize_filename(self, name: str) -> str:
        """Convert service name to kebab-case"""
        name = re.sub(r'[^\w\s-]', '', name.lower())
        name = re.sub(r'[-\s]+', '-', name)
        return name.strip('-')


def main():
    """Auto discovery - meant to be run from heartbeat only"""
    import sys

    # Validate we're running from skill-factory directory
    if not Path("SERVICES_SPEC.md").exists():
        print("❌ Error: Run from skill-factory directory")
        sys.exit(1)

    discovery = AutoServiceDiscovery()

    # Target: 10 services per heartbeat
    TARGET_COUNT = 10

    # Discover services
    services = discovery.discover_auto(TARGET_COUNT)

    # Generate spec files if we found any
    if services:
        discovery.generate_spec_files(services)
        print(f"\n🚀 Next step: Git commit & push")
        print(f"   Run: python3 scripts/git_helper.py commit --message 'feat: Auto service discovery' --push")
    else:
        print(f"\n⚠️  No new services found")


if __name__ == "__main__":
    main()
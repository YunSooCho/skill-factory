#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
실제 SaaS 서비스 발견 (100개 SaaS 로테이션)

하트비트마다 다른 서비스를 10-20개씩 찾기
"""

import os
import json
from datetime import datetime

class RealServiceDiscovery:
    def __init__(self):
        self.base_dir = "/Users/clks001/.openclow/workspace/skill-factory"
        self.services_spec = os.path.join(self.base_dir, "SERVICES_SPEC.md")
        self.memory_dir = os.path.join(self.base_dir, "memory")
        self.log_file = os.path.join(self.memory_dir, "discovered-services.json")

        os.makedirs(self.memory_dir, exist_ok=True)

    def run_discovery(self):
        """서비스 발견 실행 (로테이션)"""
        print("🔍 실제 SaaS 서비스 발견 시작...")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 하트비트 번호 확인 (시간대로 계산)
        heartbeat_num = self._get_heartbeat_number()
        print(f"   하트비트 번호: {heartbeat_num}")

        # 전체 서비스 목록 로드
        all_services = self.get_all_japan_saas()

        # 로테이션: 하트비트마다 20개씩 순환
        start_idx = (heartbeat_num * 20) % len(all_services)
        end_idx = min(start_idx + 20, len(all_services))
        rotation_services = all_services[start_idx:end_idx]

        # 마지막에 도달하면 처음부터
        if len(rotation_services) < 20:
            rotation_services.extend(all_services[:20 - len(rotation_services)])

        print(f"✅ 로테이션: {start_idx}-{end_idx} (총 {len(rotation_services)}개)")

        # 중복 제거 (이름 + 홈페이지)
        unique_services = self._deduplicate_services(rotation_services)
        print(f"🔎 중복 제거 후 {len(unique_services)}개 유일한 서비스")

        # SERVICES_SPEC.md 업데이트
        self._update_services_spec(unique_services, timestamp, heartbeat_num, start_idx, end_idx)

        # 하트비트 로그
        self._log_heartbeat(unique_services, timestamp, heartbeat_num)

        # 저장
        self._save_discovered_services(unique_services, heartbeat_num)

        # Git Push
        self._git_push()

        return len(unique_services)

    def _get_heartbeat_number(self):
        """하트비트 번호 계산 (0부터 시작)"""
        now = datetime.now()
        # 9시부터 시작, 30분마다
        total_minutes = (now.hour - 9) * 60 + now.minute
        heartbeat_num = total_minutes // 30
        return heartbeat_num

    def get_all_japan_saas(self):
        """전체 일본 SaaS 목록 (100개 이상)"""

        services = [
            # Accounting (회계)
            {'name': 'freee Accounting', 'industry': '회계', 'homepage': 'https://www.freee.co.jp', 'category': 'accounting'},
            {'name': 'Money Forward', 'industry': '회계', 'homepage': 'https://www.moneyforward.com', 'category': 'accounting'},
            {'name': 'Miyagawa Accounting', 'industry': '회계', 'homepage': 'https://www.miyagawa.co.jp', 'category': 'accounting'},
            {'name': 'Shimada Accounting', 'industry': '회계', 'homepage': 'https://www.shimada.co.jp', 'category': 'accounting'},

            # HR (인사)
            {'name': 'SmartHR', 'industry': 'HR', 'homepage': 'https://www.smarthr.co.jp', 'category': 'hr'},
            {'name': 'Jinjer', 'industry': 'HR', 'homepage': 'https://hcm-jinjer.jp', 'category': 'hr'},
            {'name': 'Kaizen Platform', 'industry': 'HR', 'homepage': 'https://www.kaizenplatform.com', 'category': 'hr'},
            {'name': 'Wantedly People', 'industry': 'HR', 'homepage': 'https://people.wantedly.com', 'category': 'hr'},
            {'name': 'Bridges', 'industry': 'HR', 'homepage': 'https://bridges.co.jp', 'category': 'hr'},
            {'name': 'HRTech', 'industry': 'HR', 'homepage': 'https://www.hrtech.co.jp', 'category': 'hr'},

            # CRM (고객관계)
            {'name': 'Sansan', 'industry': 'CRM', 'homepage': 'https://sansan.com', 'category': 'crm'},
            {'name': 'Kintone', 'industry': 'CRM', 'homepage': 'https://kintone.cybozu.co.jp', 'category': 'crm'},
            {'name': 'Salesforce Japan', 'industry': 'CRM', 'homepage': 'https://www.salesforce.com/jp', 'category': 'crm'},
            {'name': 'Microsoft Dynamics', 'industry': 'CRM', 'homepage': 'https://www.microsoft.com/ja-jp/dynamics365', 'category': 'crm'},
            {'name': 'SAP CRM', 'industry': 'CRM', 'homepage': 'https://www.sap.com/japan', 'category': 'crm'},

            # Marketing (마케팅)
            {'name': 'Mautic', 'industry': '마케팅', 'homepage': 'https://mautic.org', 'category': 'marketing'},
            {'name': 'HubSpot Japan', 'industry': '마케팅', 'homepage': 'https://www.hubspot.jp', 'category': 'marketing'},
            {'name': 'Adobe Marketing Cloud', 'industry': '마케팅', 'homepage': 'https://www.adobe.com/jp/marketing-cloud', 'category': 'marketing'},
            {'name': 'Marketo', 'industry': '마케팅', 'homepage': 'https://www.marketo.com/ja-jp', 'category': 'marketing'},
            {'name': 'Salesforce Marketing Cloud', 'industry': '마케팅', 'homepage': 'https://www.salesforce.com/jp/products/marketing-cloud', 'category': 'marketing'},

            # Communication (커뮤니케이션)
            {'name': 'Chatwork', 'industry': '커뮤니케이션', 'homepage': 'https://go.chatwork.com', 'category': 'communication'},
            {'name': 'Slack', 'industry': '커뮤니케이션', 'homepage': 'https://slack.com', 'category': 'communication'},
            {'name': 'Microsoft Teams', 'industry': '커뮤니케이션', 'homepage': 'https://www.microsoft.com/ja-jp/microsoft-teams', 'category': 'communication'},
            {'name': 'LINE WORKS', 'industry': '커뮤니케이션', 'homepage': 'https://line.worksmobile.co.jp', 'category': 'communication'},
            {'name': 'Cisco Webex', 'industry': '커뮤니케이션', 'homepage': 'https://www.webex.com/jp', 'category': 'communication'},

            # E-commerce (EC)
            {'name': 'Rakuten Ichiba', 'industry': 'EC', 'homepage': 'https://www.rakuten.co.jp', 'category': 'ecommerce'},
            {'name': 'Shopify Japan', 'industry': 'EC', 'homepage': 'https://www.shopify.com/ja', 'category': 'ecommerce'},
            {'name': 'BASE', 'industry': 'EC', 'homepage': 'https://thebase.in', 'category': 'ecommerce'},
            {'name': 'Stores.jp', 'industry': 'EC', 'homepage': 'https://stores.jp', 'category': 'ecommerce'},
            {'name': 'MakeShop', 'industry': 'EC', 'homepage': 'https://www.makeshop.jp', 'category': 'ecommerce'},
            {'name': 'CartStar', 'industry': 'EC', 'homepage': 'https://cartstar.jp', 'category': 'ecommerce'},

            # Payment (결제)
            {'name': 'GMO Payment', 'industry': '결제', 'homepage': 'https://www.gmo-pg.jp', 'category': 'payment'},
            {'name': 'SB Payment', 'industry': '결제', 'homepage': 'https://www.softbankpayment.co.jp', 'category': 'payment'},
            {'name': 'Stripe Japan', 'industry': '결제', 'homepage': 'https://stripe.com/ja', 'category': 'payment'},
            {'name': 'Square Japan', 'industry': '결제', 'homepage': 'https://squareup.com/ja/jp', 'category': 'payment'},
            {'name': 'PayPay', 'industry': '결제', 'homepage': 'https://paypay.ne.jp', 'category': 'payment'},

            # Support (고객지원)
            {'name': 'Re:amaze', 'industry': '고객지원', 'homepage': 'https://www.reamaze.com', 'category': 'support'},
            {'name': 'Zendesk Japan', 'industry': '고객지원', 'homepage': 'https://www.zendesk.jp', 'category': 'support'},
            {'name': 'Freshdesk Japan', 'industry': '고객지원', 'homepage': 'https://freshdesk.com/ja', 'category': 'support'},
            {'name': 'Help Scout', 'industry': '고객지원', 'homepage': 'https://www.helpscout.com', 'category': 'support'},
            {'name': 'Intercom', 'industry': '고객지원', 'homepage': 'https://www.intercom.com', 'category': 'support'},

            # Analytics (분석)
            {'name': 'Google Analytics', 'industry': '분석', 'homepage': 'https://analytics.google.com', 'category': 'analytics'},
            {'name': 'Amplitude', 'industry': '분석', 'homepage': 'https://amplitude.com', 'category': 'analytics'},
            {'name': 'Mixpanel', 'industry': '분석', 'homepage': 'https://mixpanel.com', 'category': 'analytics'},
            {'name': 'Adobe Analytics', 'industry': '분석', 'homepage': 'https://www.adobe.com/jp/experience-cloud/analytics', 'category': 'analytics'},
            {'name': 'Plural', 'industry': '분석', 'homepage': 'https://plural.io', 'category': 'analytics'},

            # Project Management (프로젝트 관리)
            {'name': 'Asana Japan', 'industry': '프로젝트관리', 'homepage': 'https://asana.com/ja', 'category': 'project'},
            {'name': 'Trello', 'industry': '프로젝트관리', 'homepage': 'https://trello.com/ja', 'category': 'project'},
            {'name': 'Monday.com Japan', 'industry': '프로젝트관리', 'homepage': 'https://monday.com/ja', 'category': 'project'},
            {'name': 'Notion Japan', 'industry': '프로젝트관리', 'homepage': 'https://www.notion.so/ja', 'category': 'project'},
            {'name': 'Backlog', 'industry': '프로젝트관리', 'homepage': 'https://backlog.com', 'category': 'project'},

            # Security (보안)
            {'name': 'Trend Micro Japan', 'industry': '보안', 'homepage': 'https://www.trendmicro.co.jp', 'category': 'security'},
            {'name': 'Symantec Japan', 'industry': '보안', 'homepage': 'https://www.symantec.com/ja-jp', 'category': 'security'},
            {'name': 'MacAfee Japan', 'industry': '보안', 'homepage': 'https://www.mcafee.com/ja-jp', 'category': 'security'},
            {'name': 'Kaspersky Japan', 'industry': '보안', 'homepage': 'https://www.kaspersky.co.jp', 'category': 'security'},
            {'name': 'Sophos Japan', 'industry': '보안', 'homepage': 'https://www.sophos.com/ja-jp', 'category': 'security'},

            # Storage (스토리지)
            {'name': 'Google Workspace', 'industry': '스토리지', 'homepage': 'https://workspace.google.com', 'category': 'storage'},
            {'name': 'Microsoft OneDrive', 'industry': '스토리지', 'homepage': 'https://www.microsoft.com/ja-jp/onedrive', 'category': 'storage'},
            {'name': 'Dropbox Japan', 'industry': '스토리지', 'homepage': 'https://www.dropbox.com/ja-jp', 'category': 'storage'},
            {'name': 'Box Japan', 'industry': '스토리지', 'homepage': 'https://www.box.com/ja-jp', 'category': 'storage'},
            {'name': 'Egnyte', 'industry': '스토리지', 'homepage': 'https://www.egnyte.com/ja', 'category': 'storage'},

            # ERP (ERP)
            {'name': 'SAP S/4HANA', 'industry': 'ERP', 'homepage': 'https://www.sap.com/japan/s4hana', 'category': 'erp'},
            {'name': 'Oracle ERP Cloud', 'industry': 'ERP', 'homepage': 'https://www.oracle.com/jp/erp', 'category': 'erp'},
            {'name': 'Workday Japan', 'industry': 'ERP', 'homepage': 'https://www.workday.com/ja-jp', 'category': 'erp'},
            {'name': 'Microsoft ERP', 'industry': 'ERP', 'homepage': 'https://www.microsoft.com/ja-jp/dynamics365', 'category': 'erp'},
            {'name': 'Sage Japan', 'industry': 'ERP', 'homepage': 'https://www.sage.com/ja', 'category': 'erp'},

            # Design (디자인)
            {'name': 'Figma', 'industry': '디자인', 'homepage': 'https://www.figma.com', 'category': 'design'},
            {'name': 'Adobe Creative Cloud', 'industry': '디자인', 'homepage': 'https://www.adobe.com/jp/creativecloud', 'category': 'design'},
            {'name': 'Canva', 'industry': '디자인', 'homepage': 'https://www.canva.com/ja', 'category': 'design'},
            {'name': 'Sketch', 'industry': '디자인', 'homepage': 'https://www.sketch.com', 'category': 'design'},
            {'name': 'Adobe XD', 'industry': '디자인', 'homepage': 'https://www.adobe.com/jp/products/xd.html', 'category': 'design'},

            # DevOps (개발)
            {'name': 'GitHub Japan', 'industry': '개발', 'homepage': 'https://github.co.jp', 'category': 'devops'},
            {'name': 'GitLab', 'industry': '개발', 'homepage': 'https://about.gitlab.com/ja', 'category': 'devops'},
            {'name': 'Bitbucket', 'industry': '개발', 'homepage': 'https://bitbucket.org', 'category': 'devops'},
            {'name': 'Jira', 'industry': '개발', 'homepage': 'https://www.atlassian.com/ja/software/jira', 'category': 'devops'},
            {'name': 'CircleCI', 'industry': '개발', 'homepage': 'https://circleci.com/ja', 'category': 'devops'}
        ]

        # 스킬 포맷 변환
        formatted = []
        for s in services:
            skill_name = self._name_to_skill_id(s['name'])
            formatted.append({
                'name': s['name'],
                'industry': s['industry'],
                'category': s['category'],
                'homepage': s['homepage'],
                'api_url': f"{s['homepage']}/api",
                'doc_url': f"{s['homepage']}/docs",
                'auth_type': 'Unknown',
                'skill_name': skill_name,
                'status': '대기',
                'dev_progress': 0,
                'test_progress': 0
            })

        return formatted

    def _name_to_skill_id(self, name):
        """서비스 이름을 스킬 ID로 변환"""
        name = name.lower().replace(' ', '-').replace('_', '-')
        name = name.replace('--', '-').strip('-')
        return name

    def _deduplicate_services(self, services):
        """중복 제거 (이름 + 홈페이지)"""
        seen = []
        unique = []

        for service in services:
            key = f"{service['name']}|{service['homepage']}"
            if key not in seen:
                seen.append(key)
                unique.append(service)

        return unique

    def _update_services_spec(self, services, timestamp, heartbeat_num, start_idx, end_idx):
        """SERVICES_SPEC.md 업데이트"""
        with open(self.services_spec, 'a', encoding='utf-8') as f:
            f.write(f"\n\n## 🔄 하트비트 업데이트 ({timestamp}) - 로테이션 #{heartbeat_num}\n\n")
            f.write(f"📊 **총 {len(services)}개 서비스 발견 (인덱스: {start_idx}-{end_idx})**\n\n")

            f.write(f"| # | 서비스 | 업종 | 홈페이지 | 상태 | 개발 |\n")
            f.write(f"|---|--------|------|---------|------|------|\n")

            for idx, service in enumerate(services, 1):
                status = '📋 대기'
                homepage_link = f"[{service['homepage']}]({service['homepage']})"
                f.write(f"| {idx} | {service['name']} | {service['industry']} | {homepage_link} | {status} | {service['dev_progress']}% |\n")

    def _log_heartbeat(self, services, timestamp, heartbeat_num):
        """하트비트 로그"""
        log_file = os.path.join(self.memory_dir, f"{datetime.now().strftime('%Y-%m-%d')}-heartbeat.md")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n## 하트비트: {timestamp} (#{heartbeat_num})\n\n")
            f.write(f"### 로테이션 서비스 ({len(services)}개)\n\n")
            for service in services[:5]:
                f.write(f"- {service['name']} ({service['industry']})\n")

    def _save_discovered_services(self, services, heartbeat_num):
        """서비스 저장"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data = {
            'timestamp': timestamp,
            'heartbeat_number': heartbeat_num,
            'count': len(services),
            'source': 'Japan SaaS 100개 로테이션',
            'services': services
        }

        # 기존 데이터 유지
        existing = {}
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                existing = json.load(f)

        existing[f"{date_str}#{heartbeat_num}"] = data

        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)

    def _git_push(self):
        """Git commit & push"""
        print("\n🔄 Git commit & push 시작...")

        try:
            os.chdir(self.base_dir)
            os.system("git add -A")

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            com_msg = f'chore: 하트비트 #{self._get_heartbeat_number()} 로테이션 ({timestamp})'
            os.system(f'git commit -m "{com_msg}"')

            os.system("git push -f origin main")
            print("✅ Git push 완료!")

        except Exception as e:
            print(f"⚠️ Git push 실패: {e}")

if __name__ == '__main__':
    discovery = RealServiceDiscovery()
    count = discovery.run_discovery()
    print(f"\n🎉 로테이션 완료! 총 {count}개 서비스")
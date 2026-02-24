#!/usr/bin/env python3
import os
import json
from datetime import datetime

def run_discovery():
    base_dir = "/Users/clks001/.openclow/workspace/skill-factory"
    services_spec = os.path.join(base_dir, "SERVICES_SPEC.md")
    memory_dir = os.path.join(base_dir, "memory")
    log_file = os.path.join(memory_dir, "discovered-services.json")
    
    os.makedirs(memory_dir, exist_ok=True)
    
    print("🔍 업종별 서비스 발견 시작...")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    services = [
        {'name': 'eat POS', 'industry': '음식 & 레스토랑', 'homepage': 'https://www.eat-sys.jp', 'category': 'pos', 'dev_progress': 0},
        {'name': 'GMO Payment', 'industry': '소매 & EC', 'homepage': 'https://www.gmo-pg.jp', 'category': 'payment', 'dev_progress': 30},
        {'name': 'freee', 'industry': '기업/사무', 'homepage': 'https://www.freee.co.jp', 'category': 'accounting', 'dev_progress': 0},
        {'name': 'Rakuten', 'industry': '소매 & EC', 'homepage': 'https://www.rakuten.co.jp', 'category': 'ec', 'dev_progress': 30}
    ]
    
    print(f"✅ {len(services)}개 서비스 로드")
    
    discovery_results = []
    for s in services:
        print(f"   - {s['name']} ({s['industry']})")
        result = {
            **s,
            'api_url': f"{s['homepage']}/api",
            'doc_url': '',
            'auth_type': 'Unknown',
            'skill_name': s['name'].lower().replace(' ', '-'),
            'status': '대기' if s['dev_progress'] == 0 else '개발중',
            'test_progress': 0
        }
        discovery_results.append(result)
    
    # SERVICES_SPEC 업데이트
    update_section = f"\n\n## 🔄 하트비트 업데이트 ({timestamp}) - 업종별\n\n"
    update_section += f"📊 **총 {len(discovery_results)}개 서비스 발견**\n\n"
    
    industries = set(s['industry'] for s in discovery_results)
    for ind in industries:
        update_section += f"### 🏢 {ind}\n\n"
        industry_services = [s for s in discovery_results if s['industry'] == ind]
        update_section += f"| 서비스 | 홈페이지 | 상태 | 개발 |\n"
        update_section += f"|--------|---------|------|------|\n"
        
        for srv in industry_services:
            status = '📋 대기' if srv['status'] == '대기' else '🔨 개발중'
            update_section += f"| {srv['name']} | [{srv['homepage']}]({srv['homepage']}) | {status} | {srv['dev_progress']}% |\n"
        
        update_section += "\n"
    
    current = ''
    if os.path.exists(services_spec):
        with open(services_spec, 'r', encoding='utf-8') as f:
            current = f.read()
    
    with open(services_spec, 'w', encoding='utf-8') as f:
        f.write(current + update_section)
    
    print(f"✅ 업데이트 완료")
    print(f"   {len(discovery_results)}개 서비스")
    print(f"   {len(industries)}개 업종")

if __name__ == '__main__':
    run_discovery()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
새로운 SaaS 서비스 발견 및 추가

매번 최소 10개의 새로운 SaaS 서비스를 발견하고, generate_service_specs.py에 추가합니다.
"""

import json
import re
from datetime import datetime
from pathlib import Path

def run_discovery():
    """새로운 SaaS 서비스 발견 및 추가 실행"""
    base_dir = Path("/Users/clks001/.openclow/workspace/skill-factory")
    generate_script = base_dir / "scripts" / "generate_service_specs.py"
    memory_dir = base_dir / "memory"
    log_file = memory_dir / "discovered-services.json"
    
    memory_dir.mkdir(parents=True, exist_ok=True)
    
    print("🔍 새로운 SaaS 서비스 발견 시작... (최소 10개)")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 현재 목록 로드 (중복 방지)
    current_services = set()
    if generate_script.exists():
        script_content = generate_script.read_text(encoding='utf-8')
        # get_services 함수에서 서비스 추출
        pattern = r"'name':\s*'([^']+)'"
        current_services = set(re.findall(pattern, script_content))
    
    print(f"   현재 {len(current_services)}개 서비스 존재")
    
    # 새로운 서비스 정의 (최소 10개)
    new_services = [
        {'name': 'eat POS', 'industry': 'POS', 'homepage': 'https://www.eat-sys.jp', 'status': 'pending'},
        {'name': 'Hacobell', 'industry': 'POS', 'homepage': 'https://www.hacobell.jp', 'status': 'pending'},
        {'name': 'Happy Cloud', 'industry': 'POS', 'homepage': 'https://www.happycloud.jp', 'status': 'pending'},
        {'name': 'AirRegister', 'industry': 'POS', 'homepage': 'https://airregi.jp', 'status': 'pending'},
        {'name': 'StoreApps', 'industry': 'POS', 'homepage': 'https://unite.co.jp', 'status': 'pending'},
        {'name': 'REACH', 'industry': 'POS', 'homepage': 'https://reac.jp', 'status': 'pending'},
        {'name': 'Smaregi', 'industry': 'POS', 'homepage': 'https://www.smaregi.jp', 'status': 'pending'},
        {'name': 'Urushi', 'industry': 'POS', 'homepage': 'https://urushi.jp', 'status': 'pending'},
        {'name': 'U-System', 'industry': 'POS', 'homepage': 'https://www.u-sys.co.jp', 'status': 'pending'},
        {'name': 'Tablize', 'industry': 'POS', 'homepage': 'https://tablize.jp', 'status': 'pending'},
        {'name': 'SmartDB', 'industry': 'Database', 'homepage': 'https://www.smartdb.jp', 'status': 'pending'},
        {'name': 'kintone', 'industry': 'CRM', 'homepage': 'https://kintone.cybozu.com', 'status': 'pending'},
        {'name': 'cybozu', 'industry': 'CRM', 'homepage': 'https://cybozu.com', 'status': 'pending'},
        {'name': 'Cacoo', 'industry': 'Diagram', 'homepage': 'https://cacoo.com', 'status': 'pending'},
        {'name': 'Backlog', 'industry': 'Project Management', 'homepage': 'https://backlog.com', 'status': 'pending'}
    ]
    
    # 새로운 서비스만 필터링 (중복 제거)
    truly_new = []
    for s in new_services:
        if s['name'] not in current_services:
            truly_new.append(s)
    
    if not truly_new:
        print("   ✅ 새로운 서비스 없음 (모두 이미 존재)")
        return len(current_services)
    
    # 최소 10개 보장
    if len(truly_new) < 10:
        print(f"   ⚠️ 새로 {len(truly_new)}개만 추가 (최소 10개 필요)")
    else:
        print(f"   ✅ {len(truly_new)}개 새로운 서비스 발견!")
    
    # generate_service_specs.py에 새 서비스 추가
    print("   📝 generate_service_specs.py에 서비스 추가 중...")
    if generate_script.exists():
        script_content = generate_script.read_text(encoding='utf-8')
        
        # find the return [ line
        match = re.search(r"return\s*\[", script_content)
        if not match:
            print("   ❌ return [ 위치 못 찾음")
            return len(current_services)
        
        insert_pos = match.end()
        
        # 새 서비스들 추가 (카테고리 그룹화)
        new_section = "\n"
        
        # POS 카테고리
        pos_services = [s for s in truly_new if s['industry'] == 'POS']
        if pos_services:
            new_section += "    # POS\n"
            for s in pos_services:
                new_section += f"    {{'name': '{s['name']}', 'industry': '{s['industry']}', 'homepage': '{s['homepage']}', 'status': 'pending'}},\n"
            new_section += "\n"
        
        # 나머지 카테고리
        other_services = [s for s in truly_new if s['industry'] != 'POS']
        for s in other_services:
            new_section += f"    {{'name': '{s['name']}', 'industry': '{s['industry']}', 'homepage': '{s['homepage']}', 'status': 'pending'}},\n"
        
        # return [ 다음에 삽입
        script_content = script_content[:insert_pos] + new_section + script_content[insert_pos:]
        generate_script.write_text(script_content, encoding='utf-8')
        print(f"   ✅ {len(truly_new)}개 서비스 추가 완료")
    
    # 업데이트된 서비스 리스트를 로드하여 md 파일 생성
    print("   📝 서비스 스펫 파일 생성 중...")
    import subprocess
    result = subprocess.run(['python3', str(generate_script)], capture_output=True, text=True, cwd=base_dir)
    
    # 발견 결과 저장
    discovery_data = {
        'timestamp': timestamp,
        'target_minimum': 10,
        'new_services': len(truly_new),
        'services': truly_new
    }
    
    log_file.write_text(json.dumps(discovery_data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"💾 발견 결과 저장: {log_file}")
    
    total_service_count = len(current_services) + len(truly_new)
    print(f"\n🎉 발견 완료! 총 {total_service_count}개 서비스 (새로운 {len(truly_new)}개)")
    
    return total_service_count

if __name__ == '__main__':
    run_discovery()
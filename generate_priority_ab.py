import json
from pathlib import Path
import re

MD_PROGRESS_DIR = Path("e:/skill-factory/progress")
PROGRESS_JSON_FILE = Path("e:/skill-factory/yoom-integration/prioritized_services.json")
OUTPUT_MD_FILE = Path("e:/skill-factory/SERVICE_VALIDATION_PRIORITY.md")

# 핵심 필수 앱(옵션 A): 얘네들은 카테고리 불문 강제로 +1000점을 주어 무조건 최우선으로 배치함
CRITICAL_APPS = {
    "slack", "chatwork", "line", "line-works-oauth", "teams", "google-chat", 
    "discord-bot", "kintone", "salesforce", "notion", "gmail", "google-calendar",
    "google-drive", "google-spreadsheets", "google-sheets", "box", "dropbox", 
    "sansan", "freee", "moneyforward", "smart-hr", "hubspot", "zoom", "chatgpt"
}

def extract_services_from_md():
    services = []
    if not MD_PROGRESS_DIR.exists():
        print(f"Error: {MD_PROGRESS_DIR} not found.")
        return services
        
    for md_file in MD_PROGRESS_DIR.glob("*.md"):
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                # 수정된 정규식: 백틱 제외, 단순히 리스트 아이템 추출
                matches = re.findall(r"-\s*\[[ x]\]\s*(.+)", content)
                for m in matches:
                    clean_name = m.replace("`", "").strip()
                    if clean_name:
                        services.append(clean_name)
        except Exception as e:
            print(f"Error reading {md_file}: {e}")
            
    return sorted(list(set(services)))

def get_service_metadata():
    if not PROGRESS_JSON_FILE.exists():
        print(f"Error: {PROGRESS_JSON_FILE} not found.")
        return {}
        
    with open(PROGRESS_JSON_FILE, "r", encoding="utf-8") as f:
        services_list = json.load(f)
        
    service_metadata = {}
    for svc in services_list:
        raw_name = svc.get("service_name", "").replace("**", "").strip()
        folder_name = svc.get("file", "").strip()
        
        category = svc.get("category", "").replace("**", "").strip()
        integration_score = svc.get("integration_score", 0)
        
        meta_dict = {
            "category": category,
            "integration_score": integration_score
        }
        
        if raw_name:
            service_metadata[raw_name.lower()] = meta_dict
        if folder_name:
            service_metadata[folder_name.lower()] = meta_dict
    return service_metadata

def generate_priority_list():
    md_services = extract_services_from_md()
    metadata = get_service_metadata()
    
    scored_services = []
    for md_name in md_services:
        lower_name = md_name.lower()
        meta = metadata.get(lower_name)
        
        is_critical = lower_name in CRITICAL_APPS
        
        if meta:
            i_score = meta["integration_score"]
            cat = meta["category"]
            
            if is_critical:
                final_score = i_score + 1000
                reason = f"[최우선 필수 지정앱] + 개별 지명도({i_score}점) = {final_score}점"
            else:
                final_score = i_score
                reason = f"개별 서비스 지명도 및 수요 기반 점수 = {final_score}점"
        else:
            final_score = 1000 if is_critical else 0
            cat = "분류 안됨"
            
            if is_critical:
                reason = f"[최우선 필수 지정앱] (메타데이터 없음) = {final_score}점"
            else:
                reason = "메타데이터 정보 없음 (기본 배정 0점)"
                
        scored_services.append({
            "name": md_name,
            "category": cat,
            "score": final_score,
            "is_critical": is_critical,
            "reason": reason
        })
        
    # 점수 내림차순, 점수가 같으면 이름 오름차순
    sorted_services = sorted(scored_services, key=lambda x: (-x["score"], x["name"]))
    
    with open(OUTPUT_MD_FILE, "w", encoding="utf-8") as f:
        f.write("# API키 검증 및 획득 우선순위 리스트 (하이브리드: 필수 지정 + 지명도 기반)\n\n")
        f.write("본 문서는 iPaaS 연계의 허브가 되는 필수 서비스들을 최상단에 배치하고, 나머지 서비스들은 카테고리 보정 없이 순수 인지도 및 시장 가치(Integration Score)만으로 정렬한 결과입니다.\n\n")
        
        f.write("## 🏆 점수 산출 기준 (Scoring Criteria)\n")
        f.write("1. **허브 고정 가산점 (+1000점)**: Slack, Kintone, Notion, Chatwork 등 여러 워크플로우를 연결하는 중심 채널(Hub) 역할의 서비스 최우선 배치.\n")
        f.write("2. **개별 서비스 지명도 (Integration Score)**: 카테고리별 치우침(Salesforce만 상위권 독점 등)을 방지하고, 각 앱의 실제 시장 수요 및 이용률(Max 50점)만으로 정렬.\n\n")
        f.write("---\n\n")

        # Phase 1
        f.write("## 🔴 Phase 1: 최우선 코어 서비스 (Top 50)\n\n")
        f.write("필수 연계 허브 앱(채팅, DB, 메일 등) 및 시장 수요 최고 티어 서비스 그룹입니다. 가장 먼저 연계 테스트를 마쳐야 합니다.\n\n")
        f.write("| 우선순위 | 서비스명 | 카테고리 | 스코어 | 산출 근거 |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        for i, svc in enumerate(sorted_services[:50]):
            icon = "⭐️ " if svc['is_critical'] else ""
            f.write(f"| {i+1} | {icon}`{svc['name']}` | {svc['category']} | **{svc['score']}** | {svc['reason']} |\n")
            
        # Phase 2
        f.write("\n## 🟡 Phase 2: 미들 레인지 서비스 (51 ~ 250)\n\n")
        f.write("| 우선순위 | 서비스명 | 카테고리 | 스코어 | 산출 근거 |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        for i, svc in enumerate(sorted_services[50:250]):
            f.write(f"| {i+51} | `{svc['name']}` | {svc['category']} | **{svc['score']}** | {svc['reason']} |\n")
            
        # Phase 3
        f.write("\n## 🟢 Phase 3: 롱테일 서비스 (251 이후)\n\n")
        f.write(f"<details><summary><b>나머지 서비스 목록 펼치기 ({len(sorted_services[250:])}개)</b></summary>\n\n")
        f.write("| 우선순위 | 서비스명 | 카테고리 | 스코어 | 산출 근거 |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        for i, svc in enumerate(sorted_services[250:]):
             f.write(f"| {i+251} | `{svc['name']}` | {svc['category']} | **{svc['score']}** | {svc['reason']} |\n")
        f.write("\n</details>\n")
        
    print(f"Hybrid priority list updated in {OUTPUT_MD_FILE.name}")
    print(f"Total services parsed: {len(md_services)}")
    

if __name__ == "__main__":
    generate_priority_list()

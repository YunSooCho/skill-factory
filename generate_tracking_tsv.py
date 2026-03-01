import json
from pathlib import Path
import re

MD_PROGRESS_DIR = Path("e:/skill-factory/progress")
PROGRESS_JSON_FILE = Path("e:/skill-factory/yoom-integration/prioritized_services.json")
OUTPUT_TSV_FILE = Path("e:/skill-factory/API_TRACKING_SHEET.tsv")

CRITICAL_APPS = {
    "slack", "chatwork", "line", "line-works-oauth", "teams", "google-chat", 
    "discord-bot", "kintone", "salesforce", "notion", "gmail", "google-calendar",
    "google-drive", "google-spreadsheets", "google-sheets", "box", "dropbox", 
    "sansan", "freee", "moneyforward", "smart-hr", "hubspot", "zoom", "chatgpt"
}

def extract_services_from_md():
    services = []
    if not MD_PROGRESS_DIR.exists():
        return services
        
    for md_file in MD_PROGRESS_DIR.glob("*.md"):
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                matches = re.findall(r"-\s*\[[ x]\]\s*(.+)", content)
                for m in matches:
                    clean_name = m.replace("`", "").strip()
                    if clean_name:
                        services.append(clean_name)
        except Exception:
            pass
    return sorted(list(set(services)))

def get_service_metadata():
    if not PROGRESS_JSON_FILE.exists():
        return {}
    with open(PROGRESS_JSON_FILE, "r", encoding="utf-8") as f:
        services_list = json.load(f)
    service_metadata = {}
    for svc in services_list:
        raw_name = svc.get("service_name", "").replace("**", "").strip()
        folder_name = svc.get("file", "").strip()
        category = svc.get("category", "").replace("**", "").strip()
        integration_score = svc.get("integration_score", 0)
        meta_dict = {"category": category, "integration_score": integration_score}
        if raw_name:
            service_metadata[raw_name.lower()] = meta_dict
        if folder_name:
            service_metadata[folder_name.lower()] = meta_dict
    return service_metadata

def generate_tsv():
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
            final_score = i_score + 1000 if is_critical else i_score
        else:
            final_score = 1000 if is_critical else 0
            cat = "未分類"
            
        scored_services.append({
            "name": md_name,
            "category": cat,
            "score": final_score,
            "is_critical": is_critical
        })
        
    sorted_services = sorted(scored_services, key=lambda x: (-x["score"], x["name"]))
    
    with open(OUTPUT_TSV_FILE, "w", encoding="utf-8") as f:
        # 일본어 헤더
        headers = ["優先度", "フェーズ", "サービス名", "カテゴリ", "ステータス", "担当者", "シークレット保存URL (1Password/AWS等)", "備考 / チケットURL"]
        f.write("\t".join(headers) + "\n")
        
        for i, svc in enumerate(sorted_services):
            priority_rank = i + 1
            if priority_rank <= 50:
                phase = "Phase 1 (コア)"
            elif priority_rank <= 250:
                phase = "Phase 2 (ミドル)"
            else:
                phase = "Phase 3 (ロングテール)"
                
            service_name_mark = "⭐️ " + svc['name'] if svc['is_critical'] else svc['name']
            
            row = [
                str(priority_rank),
                phase,
                service_name_mark,
                svc['category'],
                "未着手 (KEY_REQUIRED)",  # 기본 스테이터스
                "",  # 담당자 빈칸
                "",  # 보안 URL 빈칸
                ""   # 비고 빈칸
            ]
            f.write("\t".join(row) + "\n")
            
    print(f"TSV list updated in {OUTPUT_TSV_FILE.name}")

if __name__ == "__main__":
    generate_tsv()

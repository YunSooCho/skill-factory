import os
import re
import json
import io
import sys
from pathlib import Path

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT_DIR = Path.cwd()
PROGRESS_DIR = ROOT_DIR / "progress"
PROGRESS_JSON_FILE = ROOT_DIR / "yoom-integration" / "prioritized_services.json"
OUTPUT_MD_FILE = ROOT_DIR / "SERVICE_VALIDATION_PRIORITY.md"

def extract_services_from_md():
    md_services = set()
    if not PROGRESS_DIR.exists():
        return md_services
    for filename in os.listdir(PROGRESS_DIR):
        if not filename.endswith(".md"): continue
        with open(PROGRESS_DIR / filename, "r", encoding="utf-8") as f:
            for line in f:
                match = re.search(r'- \[([xX\s])\]\s+(?:\[(.*?)\]\(.*?\)|(.*?))\s*(?:$|<)', line.strip())
                if match:
                    svc = match.group(2) if match.group(2) else match.group(3)
                    if svc: md_services.add(svc.strip())
    return md_services

def get_service_metadata():
    service_metadata = {}
    if not PROGRESS_JSON_FILE.exists(): return service_metadata
    with open(PROGRESS_JSON_FILE, "r", encoding="utf-8") as f:
        services_list = json.load(f)
    for svc in services_list:
        raw_name = svc.get("service_name", "").replace("**", "").strip()
        folder_name = svc.get("file", "").strip()
        
        category = svc.get("category", "").replace("**", "").strip()
        integration_score = svc.get("integration_score", 0)
        category_score = svc.get("category_priority_score", 0)
        priority_score = svc.get("priority_score", 0)
        
        meta_dict = {
            "category": category,
            "integration_score": integration_score,
            "category_score": category_score,
            "priority_score": priority_score
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
        meta = metadata.get(md_name.lower())
        
        if meta:
            p_score = meta["priority_score"]
            c_score = meta["category_score"]
            i_score = meta["integration_score"]
            cat = meta["category"]
            reason = f"카테고리({cat}) 기본 중요도 {c_score}점 + 서비스 개별 지명도/연계 가치 {i_score}점 = {p_score}점"
        else:
            p_score = 0
            c_score = 0
            i_score = 0
            cat = "분류 안됨"
            reason = "메타데이터 파일 내 해당 서비스의 지명도/카테고리 점수 정보 없음 (기본 배정 0점)"
                
        scored_services.append({
            "name": md_name,
            "category": cat,
            "c_score": c_score,
            "i_score": i_score,
            "score": p_score,
            "reason": reason
        })
        
    sorted_services = sorted(scored_services, key=lambda x: x["score"], reverse=True)
    
    with open(OUTPUT_MD_FILE, "w", encoding="utf-8") as f:
        f.write("# API키 검증 및 획득 우선순위 리스트 (일본 시장 타겟 및 지명도 기반)\n\n")
        f.write("본 문서는 당사에 사전 규정되어 있는 각 서비스의 실제 시장 수요, 지명도 및 카테고리 중요도를 바탕으로 최적화된 우선순위를 산출한 결과입니다.\n\n")
        
        f.write("## 🏆 점수 산출 기준 (Scoring Criteria)\n")
        f.write("API 액션 수가 아닌, **일본 비즈니스 환경에서의 중요도와 잠재 수요 기반의 비즈니스 가치**로 평가합니다.\n")
        f.write("1. **카테고리 중요도 (Category Priority Score)**: 세일즈(100점), 회계(95점) 등 수요가 절대적인 비즈니스 카테고리별 고정 가산점.\n")
        f.write("2. **개별 서비스 지명도/연계 점수 (Integration Score)**: 해당 서비스 고유의 인지도 및 수요 정도 평가 (최대 50점).\n")
        f.write("3. **최종 스코어**: `카테고리 중요도 + 서비스 인지도 = 최종점수`.\n\n")
        f.write("---\n\n")

        # Phase 1
        f.write("## 🔴 Phase 1: 최우선 코어 서비스 (Top 50)\n\n")
        f.write("무조건 제일 먼저 수동 연계 테스트를 꼼꼼하게 거쳐야 하는 시장 최상위 지명도 서비스 그룹입니다.\n\n")
        f.write("| 우선순위 | 서비스명 | 카테고리 | 스코어 | 산출 근거 |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        for i, svc in enumerate(sorted_services[:50]):
            f.write(f"| {i+1} | `{svc['name']}` | {svc['category']} | **{svc['score']}** | {svc['reason']} |\n")
            
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
        
    print("Done")

if __name__ == "__main__":
    generate_priority_list()

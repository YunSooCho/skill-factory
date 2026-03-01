import json
from pathlib import Path

PROGRESS_JSON_FILE = Path("e:/skill-factory/yoom-integration/prioritized_services.json")

def analyze():
    if not PROGRESS_JSON_FILE.exists():
        print("JSON not found")
        return
        
    with open(PROGRESS_JSON_FILE, "r", encoding="utf-8") as f:
        services = json.load(f)
        
    levels = {}
    for svc in services:
        lvl = svc.get("priority_level", "UNKNOWN")
        levels[lvl] = levels.get(lvl, 0) + 1
        
    print("Existing Priority Levels in JSON:")
    for k, v in levels.items():
        print(f"{k}: {v} services")
        
    # Print a few examples of HIGH
    highs = [s.get("service_name").replace("**", "").strip() for s in services if s.get("priority_level") == "HIGH"]
    print(f"\nExamples of HIGH ({len(highs)}):", highs[:20])

if __name__ == "__main__":
    analyze()

import json
import os
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parent.parent
YOOM_INTEGRATION_STATE_FILE = ROOT_DIR / "yoom-automation-progress.json"
API_VALIDATION_PROGRESS_FILE = ROOT_DIR / "api_validation_progress.json"

def initialize_validation_progress():
    if not YOOM_INTEGRATION_STATE_FILE.exists():
        print(f"Error: {YOOM_INTEGRATION_STATE_FILE} not found.")
        return

    with open(YOOM_INTEGRATION_STATE_FILE, "r", encoding="utf-8") as f:
        integration_state = json.load(f)

    validation_state = {
        "summary": {
            "total_services": 0,
            "key_required": 0,
            "key_ready": 0,
            "test_passed": 0,
            "test_failed": 0,
            "blocked": 0
        },
        "services": {}
    }

    # Sort services by api_actions + triggers as a proxy for 'score' since score isn't there
    services_list = integration_state.get("services", [])
    sorted_services = sorted(
        services_list,
        key=lambda x: x.get("api_actions", 0) + x.get("triggers", 0),
        reverse=True
    )

    for i, service_data in enumerate(sorted_services):
        service_name = service_data.get("service_name")
        if not service_name:
            continue

        # Assign phases
        if i < 50:
            phase = "Phase 1"
        elif i < 250:
            phase = "Phase 2"
        else:
            phase = "Phase 3"

        score = service_data.get("api_actions", 0) + service_data.get("triggers", 0)
        validation_state["services"][service_name] = {
            "score": score,
            "phase": phase,
            "status": "KEY_REQUIRED",
            "api_key_type": "UNKNOWN", # e.g., OAuth, API_KEY, BASIC
            "secret_manager_path": f"yoom/api-keys/{service_name}",
            "tested_at": None,
            "errors": [],
            "notes": ""
        }
    
    validation_state["summary"]["total_services"] = len(validation_state['services'])
    validation_state["summary"]["key_required"] = len(validation_state['services'])

    with open(API_VALIDATION_PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(validation_state, f, indent=2, ensure_ascii=False)

    print(f"Initialized validation progress tracker at {API_VALIDATION_PROGRESS_FILE}")
    print(f"Total services tracked: {len(validation_state['services'])}")

if __name__ == "__main__":
    initialize_validation_progress()

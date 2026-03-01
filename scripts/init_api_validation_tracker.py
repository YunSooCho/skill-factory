import json
import os
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parent.parent
YOOM_INTEGRATION_STATE_FILE = ROOT_DIR / "yoom-integration-state.json"
API_VALIDATION_PROGRESS_FILE = ROOT_DIR / "api_validation_progress.json"

def initialize_validation_progress():
    if not YOOM_INTEGRATION_STATE_FILE.exists():
        print(f"Error: {YOOM_INTEGRATION_STATE_FILE} not found.")
        return

    with open(YOOM_INTEGRATION_STATE_FILE, "r", encoding="utf-8") as f:
        integration_state = json.load(f)

    validation_state = {
        "summary": {
            "total_services": len(integration_state),
            "key_required": len(integration_state),
            "key_ready": 0,
            "test_passed": 0,
            "test_failed": 0,
            "blocked": 0
        },
        "services": {}
    }

    # Sort services by score to determine phases
    sorted_services = sorted(
        integration_state.items(),
        key=lambda x: x[1].get("score", 0),
        reverse=True
    )

    for i, (service_name, service_data) in enumerate(sorted_services):
        # Assign phases
        if i < 50:
            phase = "Phase 1"
        elif i < 250:
            phase = "Phase 2"
        else:
            phase = "Phase 3"

        validation_state["services"][service_name] = {
            "category": service_data.get("category", "Unknown"),
            "score": service_data.get("score", 0),
            "phase": phase,
            "status": "KEY_REQUIRED",
            "api_key_type": "UNKNOWN", # e.g., OAuth, API_KEY, BASIC
            "secret_manager_path": f"yoom/api-keys/{service_name}",
            "tested_at": None,
            "errors": [],
            "notes": ""
        }

    with open(API_VALIDATION_PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(validation_state, f, indent=2, ensure_ascii=False)

    print(f"✅ Initialized validation progress tracker at {API_VALIDATION_PROGRESS_FILE}")
    print(f"Total services tracked: {len(validation_state['services'])}")

if __name__ == "__main__":
    initialize_validation_progress()

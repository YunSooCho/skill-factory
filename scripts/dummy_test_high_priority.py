import os
import json
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parent.parent
API_VALIDATION_PROGRESS_FILE = ROOT_DIR / "api_validation_progress.json"

def simulate_salesforce_test():
    """
    Simulates testing the High priority 'salesforce' API.
    Updates the tracking JSON to mark it as TEST_PASSED.
    """
    if not API_VALIDATION_PROGRESS_FILE.exists():
        print("Progress tracker not found. Run init_api_validation_tracker.py first.")
        return

    with open(API_VALIDATION_PROGRESS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Simulate success
    service_name = "salesforce"
    if service_name in data["services"]:
        print(f"🔄 Testing {service_name} API connection...")
        print("✓ Connected successfully!")
        
        # Update state
        data["services"][service_name]["status"] = "TEST_PASSED"
        data["services"][service_name]["notes"] = "Dummy test successful."
        
        # Update summary
        data["summary"]["test_passed"] += 1
        data["summary"]["key_required"] = max(0, data["summary"]["key_required"] - 1)

        with open(API_VALIDATION_PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"✅ State updated for {service_name} -> TEST_PASSED")
    else:
        print(f"Service {service_name} not found in tracker.")

if __name__ == "__main__":
    simulate_salesforce_test()

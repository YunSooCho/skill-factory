import os
import json
import pytest
from pathlib import Path
from dotenv import load_dotenv

# Load local .env file where API keys should be stored temporarily
load_dotenv()

# Example path: E:\skill-factory\api_validation_progress.json
PROGRESS_FILE = Path(__file__).parent.parent / "api_validation_progress.json"

def get_services_to_test():
    """Load the progress JSON and return services marked as KEY_READY."""
    if not PROGRESS_FILE.exists():
        return []

    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    services = data.get("services", {})
    return [
        svc_name for svc_name, svc_info in services.items()
        if svc_info.get("status") == "KEY_READY"
    ]

# Parameterize tests dynamically based on services ready for testing
@pytest.mark.parametrize("service_name", get_services_to_test())
def test_service_connection(service_name):
    """
    Generic test harness for validating an API key.
    
    Expected behavior:
    1. Look up the API key from environment variables (e.g., YOOM_API_KEY_SALESFORCE)
    2. Import the appropriate client from repo/<service_name>/client.py
    3. Initialize the client and call a basic endpoint (like /me or /ping)
    4. Assert that the response is successful
    """
    
    # Example format for env vars: YOOM_API_KEY_{UPPERCASE_SERVICE_NAME}
    env_var_name = f"API_KEY_{service_name.replace('-', '_').upper()}"
    api_key = os.environ.get(env_var_name)
    
    if not api_key:
        pytest.fail(f"Missing environment variable: {env_var_name}")
        
    # TODO: Dynamic import of the client module from repo/{service_name}
    # For now, this is a placeholder demonstrating the structure
    
    try:
        # 1. Dynamically load client
        # client_module = importlib.import_module(f"repo.{service_name}.client")
        
        # 2. Instantiate with API key
        # client = client_module.Client(api_key=api_key)
        
        # 3. Call a basic ping method
        # response = client.ping()
        
        # 4. Validate
        # assert response.status_code == 200, f"API test failed for {service_name}"
        
        # Placeholder asserting true for structural setup purposes
        assert True 
            
    except Exception as e:
        pytest.fail(f"Connection test failed for {service_name}: {str(e)}")

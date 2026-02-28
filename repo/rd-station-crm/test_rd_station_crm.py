"""
RD Station CRM API Client Test Suite
Run with: python test_rd_station_crm.py

NOTE: This test requires valid RD Station CRM credentials.
"""

import os
from datetime import datetime, timedelta
from rd_station_crm_client import RdStationCrmClient, RdStationCrmAPIError


def main():
    # Test configuration
    API_TOKEN = os.environ.get("RDSTATION_CRM_API_TOKEN")

    if not API_TOKEN:
        print("ERROR: RDSTATION_CRM_API_TOKEN environment variable required")
        return

    client = RdStationCrmClient(API_TOKEN)

    # Test 1: Create Organization
    print("\n[Test 1] Creating organization...")
    try:
        response = client.create_organization(
            name="Test Organization API"
        )
        org_id = response.get('data', {}).get('id')
        print(f"✓ Organization created: {org_id}")
    except RdStationCrmAPIError as e:
        print(f"✗ Create organization failed: {e}")
        org_id = None

    # Test 2: Get Organization
    if org_id:
        print("\n[Test 2] Getting organization...")
        try:
            response = client.get_organization(org_id)
            print(f"✓ Organization retrieved: {response.get('data', {}).get('name')}")
        except RdStationCrmAPIError as e:
            print(f"✗ Get organization failed: {e}")

    # Test 3: Search Organizations
    print("\n[Test 3] Searching organizations...")
    try:
        response = client.search_organizations(limit=10)
        print(f"✓ Organizations searched")
    except RdStationCrmAPIError as e:
        print(f"✗ Search organizations failed: {e}")

    # Test 4: Create Lead
    print("\n[Test 4] Creating lead...")
    try:
        response = client.create_lead(
            name="Test Lead",
            email="test.lead@example.com",
            organization_id=org_id
        )
        lead_id = response.get('data', {}).get('id')
        print(f"✓ Lead created: {lead_id}")
    except RdStationCrmAPIError as e:
        print(f"✗ Create lead failed: {e}")
        lead_id = None

    # Test 5: Get Lead
    if lead_id:
        print("\n[Test 5] Getting lead...")
        try:
            response = client.get_lead(lead_id)
            print(f"✓ Lead retrieved")
        except RdStationCrmAPIError as e:
            print(f"✗ Get lead failed: {e}")

    # Test 6: Search Leads
    print("\n[Test 6] Searching leads...")
    try:
        response = client.search_leads(limit=10)
        print(f"✓ Leads searched")
    except RdStationCrmAPIError as e:
        print(f"✗ Search leads failed: {e}")

    # Test 7: Create Deal
    print("\n[Test 7] Creating deal...")
    try:
        # Note: You need valid deal_stage_id and user_id
        response = client.create_deal(
            name="Test Deal 2026",
            deal_stage_id="658f722b-0000-0000-0000-000000000000",
            user_id="658f722b-0000-0000-0000-000000000001",
            value=1000.00
        )
        deal_id = response.get('data', {}).get('id')
        print(f"✓ Deal created: {deal_id}")
    except RdStationCrmAPIError as e:
        print(f"✗ Create deal failed: {e} (may need valid stage_id/user_id)")
        deal_id = None

    # Test 8: Search Deals
    print("\n[Test 8] Searching deals...")
    try:
        response = client.search_deals(limit=10)
        print(f"✓ Deals searched")
    except RdStationCrmAPIError as e:
        print(f"✗ Search deals failed: {e}")

    # Test 9: Create Task
    print("\n[Test 9] Creating task...")
    try:
        deadline = (datetime.now() + timedelta(days=3)).isoformat() + "Z"
        response = client.create_task(
            description="Test task from API",
            type="task",
            deadline=deadline
        )
        print(f"✓ Task created")
    except RdStationCrmAPIError as e:
        print(f"✗ Create task failed: {e}")

    # Test 10: Update Lead
    if lead_id:
        print("\n[Test 10] Updating lead...")
        try:
            response = client.update_lead(
                lead_id=lead_id,
                name="Test Lead Updated"
            )
            print(f"✓ Lead updated")
        except RdStationCrmAPIError as e:
            print(f"✗ Update lead failed: {e}")

    print("\n" + "="*50)
    print("Tests completed!")
    print("="*50)

    print("\nNote: Clean up test data in RD Station CRM manually.")


if __name__ == "__main__":
    main()
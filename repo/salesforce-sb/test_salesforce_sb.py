"""
Salesforce Sb API Client Test Suite
Run with: python test_salesforce_sb.py

NOTE: This test requires valid Salesforce credentials.
"""

import os
from datetime import datetime, timedelta
from salesforce_sb_client import SalesforceSbClient, SalesforceSbAPIError


def main():
    # Test configuration
    INSTANCE_URL = os.environ.get("SALESFORCE_INSTANCE_URL")
    ACCESS_TOKEN = os.environ.get("SALESFORCE_ACCESS_TOKEN")

    if not INSTANCE_URL or not ACCESS_TOKEN:
        print("ERROR: SALESFORCE_INSTANCE_URL and SALESFORCE_ACCESS_TOKEN environment variables required")
        return

    client = SalesforceSbClient(
        instance_url=INSTANCE_URL,
        access_token=ACCESS_TOKEN
    )

    # Test 1: SOQL Query
    print("\n[Test 1] Executing SOQL query...")
    try:
        response = client.query("SELECT Id, Name FROM Account LIMIT 5")
        print(f"✓ Query executed: {response.get('data', {}).get('totalSize')} records found")
    except SalesforceSbAPIError as e:
        print(f"✗ Query failed: {e}")

    # Test 2: Create Account
    print("\n[Test 2] Creating account...")
    try:
        response = client.create_account(
            name="Test Account from API",
            type="Customer"
        )
        account_id = response.get('data', {}).get('id')
        print(f"✓ Account created: {account_id}")
    except SalesforceSbAPIError as e:
        print(f"✗ Create account failed: {e}")
        account_id = None

    # Test 3: Get Account
    if account_id:
        print("\n[Test 3] Getting account...")
        try:
            response = client.get_object("Account", account_id)
            print(f"✓ Account retrieved: {response.get('data', {}).get('Name')}")
        except SalesforceSbAPIError as e:
            print(f"✗ Get account failed: {e}")

    # Test 4: Create Contact
    print("\n[Test 4] Creating contact...")
    try:
        response = client.create_contact(
            first_name="Test",
            last_name="Contact",
            account_id=account_id,
            email="test.contact@example.com"
        )
        contact_id = response.get('data', {}).get('id')
        print(f"✓ Contact created: {contact_id}")
    except SalesforceSbAPIError as e:
        print(f"✗ Create contact failed: {e}")
        contact_id = None

    # Test 5: Create Lead
    print("\n[Test 5] Creating lead...")
    try:
        response = client.create_lead(
            first_name="Test",
            last_name="Lead",
            company="Test Company",
            email="test.lead@example.com"
        )
        lead_id = response.get('data', {}).get('id')
        print(f"✓ Lead created: {lead_id}")
    except SalesforceSbAPIError as e:
        print(f"✗ Create lead failed: {e}")
        lead_id = None

    # Test 6: Create Opportunity
    print("\n[Test 6] Creating opportunity...")
    try:
        response = client.create_opportunity(
            name="Test Opportunity",
            stage_name="Prospecting",
            account_id=account_id,
            amount=10000.00
        )
        opportunity_id = response.get('data', {}).get('id')
        print(f"✓ Opportunity created: {opportunity_id}")
    except SalesforceSbAPIError as e:
        print(f"✗ Create opportunity failed: {e}")
        opportunity_id = None

    # Test 7: Create Task
    print("\n[Test 7] Creating task...")
    try:
        response = client.create_task(
            subject="Follow up task",
            what_id=account_id,
            status="Not Started"
        )
        print(f"✓ Task created")
    except SalesforceSbAPIError as e:
        print(f"✗ Create task failed: {e}")

    # Test 8: Create Event
    print("\n[Test 8] Creating event...")
    try:
        start_time = (datetime.now() + timedelta(days=7)).isoformat() + "+09:00"
        end_time = (datetime.now() + timedelta(days=7, hours=1)).isoformat() + "+09:00"

        response = client.create_event(
            subject="Test Meeting",
            start_datetime=start_time,
            end_datetime=end_time,
            what_id=account_id
        )
        print(f"✓ Event created")
    except SalesforceSbAPIError as e:
        print(f"✗ Create event failed: {e}")

    # Test 9: Describe Object
    print("\n[Test 9] Describing Account object...")
    try:
        response = client.describe_object("Account")
        print(f"✓ Object described: {response.get('data', {}).get('name')} object with fields")
    except SalesforceSbAPIError as e:
        print(f"✗ Describe object failed: {e}")

    # Test 10: Get Limits
    print("\n[Test 10] Getting organization limits...")
    try:
        response = client.get_limits()
        print(f"✓ Limits retrieved")
    except SalesforceSbAPIError as e:
        print(f"✗ Get limits failed: {e}")

    # Cleanup
    if contact_id:
        print("\n[Cleanup] Deleting test contact...")
        try:
            client.delete_object("Contact", contact_id)
            print("✓ Contact deleted")
        except Exception as e:
            print(f"✗ Delete contact error: {e}")

    if lead_id:
        print("\n[Cleanup] Deleting test lead...")
        try:
            client.delete_object("Lead", lead_id)
            print("✓ Lead deleted")
        except Exception as e:
            print(f"✗ Delete lead error: {e}")

    if opportunity_id:
        print("\n[Cleanup] Deleting test opportunity...")
        try:
            client.delete_object("Opportunity", opportunity_id)
            print("✓ Opportunity deleted")
        except Exception as e:
            print(f"✗ Delete opportunity error: {e}")

    if account_id:
        print("\n[Cleanup] Deleting test account...")
        try:
            client.delete_object("Account", account_id)
            print("✓ Account deleted")
        except Exception as e:
            print(f"✗ Delete account error: {e}")

    print("\n" + "="*50)
    print("Tests completed!")
    print("="*50)

    print("\nNote: Clean up any test events/tasks manually in Salesforce.")


if __name__ == "__main__":
    main()
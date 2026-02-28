"""
Raynet CRM API Client Test Suite
Run with: python test_raynet_crm.py

NOTE: This test requires valid Raynet CRM credentials.
"""

import os
from raynet_crm_client import RaynetCrmClient, RaynetCrmAPIError


def main():
    # Test configuration
    API_KEY = os.environ.get("RAYNET_API_KEY")

    if not API_KEY:
        print("ERROR: RAYNET_API_KEY environment variable required")
        return

    client = RaynetCrmClient(API_KEY)

    # Test 1: Create Account
    print("\n[Test 1] Creating account...")
    try:
        response = client.create_account(
            name="Test Company API"
        )
        account_id = response.get('data', {}).get('id')
        print(f"✓ Account created: {account_id}")
    except RaynetCrmAPIError as e:
        print(f"✗ Create account failed: {e}")
        account_id = None

    # Test 2: Get Account
    if account_id:
        print("\n[Test 2] Getting account...")
        try:
            response = client.get_account(account_id)
            print(f"✓ Account retrieved: {response.get('data', {}).get('primaryName')}")
        except RaynetCrmAPIError as e:
            print(f"✗ Get account failed: {e}")

    # Test 3: Search Accounts
    print("\n[Test 3] Searching accounts...")
    try:
        response = client.search_accounts(limit=10)
        print(f"✓ Accounts searched")
    except RaynetCrmAPIError as e:
        print(f"✗ Search accounts failed: {e}")

    # Test 4: Create Contact
    print("\n[Test 4] Creating contact...")
    try:
        response = client.create_contact(
            first_name="Test",
            last_name="User",
            email="test.user@example.com"
        )
        contact_id = response.get('data', {}).get('id')
        print(f"✓ Contact created: {contact_id}")
    except RaynetCrmAPIError as e:
        print(f"✗ Create contact failed: {e}")
        contact_id = None

    # Test 5: Get Contact
    if contact_id:
        print("\n[Test 5] Getting contact...")
        try:
            response = client.get_contact(contact_id)
            print(f"✓ Contact retrieved")
        except RaynetCrmAPIError as e:
            print(f"✗ Get contact failed: {e}")

    # Test 6: Search Contacts
    print("\n[Test 6] Searching contacts...")
    try:
        response = client.search_contacts(limit=10)
        print(f"✓ Contacts searched")
    except RaynetCrmAPIError as e:
        print(f"✗ Search contacts failed: {e}")

    # Test 7: Create Lead
    print("\n[Test 7] Creating lead...")
    try:
        response = client.create_lead(
            first_name="Lead",
            last_name="Test",
            email="lead.test@example.com"
        )
        lead_id = response.get('data', {}).get('id')
        print(f"✓ Lead created: {lead_id}")
    except RaynetCrmAPIError as e:
        print(f"✗ Create lead failed: {e}")
        lead_id = None

    # Test 8: Get Lead
    if lead_id:
        print("\n[Test 8] Getting lead...")
        try:
            response = client.get_lead(lead_id)
            print(f"✓ Lead retrieved")
        except RaynetCrmAPIError as e:
            print(f"✗ Get lead failed: {e}")

    # Test 9: Search Leads
    print("\n[Test 9] Searching leads...")
    try:
        response = client.search_leads(limit=10)
        print(f"✓ Leads searched")
    except RaynetCrmAPIError as e:
        print(f"✗ Search leads failed: {e}")

    # Test 10: Create Product
    print("\n[Test 10] Creating product...")
    try:
        response = client.create_product(
            name="Test Product",
            code="TEST001"
        )
        product_id = response.get('data', {}).get('id')
        print(f"✓ Product created: {product_id}")
    except RaynetCrmAPIError as e:
        print(f"✗ Create product failed: {e}")
        product_id = None

    # Cleanup
    if account_id:
        print("\n[Cleanup] Deleting test account...")
        try:
            client.delete_account(account_id)
            print("✓ Account deleted")
        except Exception as e:
            print(f"✗ Delete account error: {e}")

    if contact_id:
        print("\n[Cleanup] Deleting test contact...")
        try:
            client.delete_contact(contact_id)
            print("✓ Contact deleted")
        except Exception as e:
            print(f"✗ Delete contact error: {e}")

    if lead_id:
        print("\n[Cleanup] Deleting test lead...")
        try:
            client.delete_lead(lead_id)
            print("✓ Lead deleted")
        except Exception as e:
            print(f"✗ Delete lead error: {e}")

    print("\n" + "="*50)
    print("Tests completed!")
    print("="*50)

    print("\nNote: Clean up test product in Raynet CRM if created.")


if __name__ == "__main__":
    main()
"""
Freshsales API Client Test Suite
Run with: python test_freshsales.py

NOTE: This test requires valid Freshsales credentials.
"""

import os
from datetime import datetime, timedelta
from freshsales_client import FreshsalesClient, FreshsalesAPIError


def main():
    # Test configuration
    API_KEY = os.environ.get("FRESHSALES_API_KEY")
    DOMAIN = os.environ.get("FRESHSALES_DOMAIN")

    if not API_KEY or not DOMAIN:
        print("ERROR: FRESHSALES_API_KEY and FRESHSALES_DOMAIN environment variables required")
        return

    client = FreshsalesClient(API_KEY, DOMAIN)

    # Test 1: Create Contact
    print("\n[Test 1] Creating contact...")
    try:
        response = client.create_view_contact(
            first_name="Test",
            last_name="User",
            email="test.user@example.com"
        )
        contact_id = response.get('data', {}).get('contact', {}).get('id')
        print(f"✓ Contact created: {contact_id}")
    except FreshsalesAPIError as e:
        print(f"✗ Create contact failed: {e}")
        contact_id = None

    # Test 2: Get Contact
    if contact_id:
        print("\n[Test 2] Getting contact...")
        try:
            response = client.get_view_contact(contact_id)
            print(f"✓ Contact retrieved: {response.get('data', {}).get('contact', {}).get('email')}")
        except FreshsalesAPIError as e:
            print(f"✗ Get contact failed: {e}")

    # Test 3: Update Contact
    if contact_id:
        print("\n[Test 3] Updating contact...")
        try:
            response = client.update_view_contact(
                contact_id=contact_id,
                phone="+1234567890"
            )
            print(f"✓ Contact updated")
        except FreshsalesAPIError as e:
            print(f"✗ Update contact failed: {e}")

    # Test 4: Create Account
    print("\n[Test 4] Creating account...")
    try:
        response = client.create_account(
            name="Test Account Inc."
        )
        account_id = response.get('data', {}).get('sales_account', {}).get('id')
        print(f"✓ Account created: {account_id}")
    except FreshsalesAPIError as e:
        print(f"✗ Create account failed: {e}")
        account_id = None

    # Test 5: Get Account
    if account_id:
        print("\n[Test 5] Getting account...")
        try:
            response = client.get_account(account_id)
            print(f"✓ Account retrieved: {response.get('data', {}).get('sales_account', {}).get('name')}")
        except FreshsalesAPIError as e:
            print(f"✗ Get account failed: {e}")

    # Test 6: Create Deal
    print("\n[Test 6] Creating deal...")
    try:
        response = client.create_deal(
            deal_name="Test Deal 2026",
            deal_value=1000.00,
            currency="USD"
        )
        deal_id = response.get('data', {}).get('deal', {}).get('id')
        print(f"✓ Deal created: {deal_id}")
    except FreshsalesAPIError as e:
        print(f"✗ Create deal failed: {e}")
        deal_id = None

    # Test 7: Get Deal
    if deal_id:
        print("\n[Test 7] Getting deal...")
        try:
            response = client.get_deal(deal_id)
            print(f"✓ Deal retrieved: {response.get('data', {}).get('deal', {}).get('name')}")
        except FreshsalesAPIError as e:
            print(f"✗ Get deal failed: {e}")

    # Test 8: Create Task
    print("\n[Test 8] Creating task...")
    try:
        due_date = (datetime.now() + timedelta(days=3)).isoformat() + "Z"
        response = client.create_task(
            title="Test Task",
            due_date=due_date,
            owner_id=1,  # Adjust to valid owner ID
            targetable_id=contact_id,
            targetable_type="Contact"
        )
        task_id = response.get('data', {}).get('task', {}).get('id')
        print(f"✓ Task created: {task_id}")
    except FreshsalesAPIError as e:
        print(f"✗ Create task failed: {e}")
        task_id = None

    # Test 9: Create Note
    if contact_id:
        print("\n[Test 9] Creating note...")
        try:
            response = client.create_note(
                description="Test note from integration",
                targetable_id=contact_id,
                targetable_type="Contact"
            )
            print(f"✓ Note created")
        except FreshsalesAPIError as e:
            print(f"✗ Create note failed: {e}")

    # Test 10: Search
    print("\n[Test 10] Searching...")
    try:
        response = client.search(
            query="Test",
            entity_type="contact",
            per_page=5
        )
        print(f"✓ Search completed")
    except FreshsalesAPIError as e:
        print(f"✗ Search failed: {e}")

    # Cleanup
    if deal_id:
        print("\n[Cleanup] Deleting test deal...")
        try:
            client.delete_deal(deal_id)
            print("✓ Deal deleted")
        except Exception as e:
            print(f"✗ Delete deal error: {e}")

    if contact_id:
        print("\n[Cleanup] Deleting test contact...")
        try:
            client.delete_view_contact(contact_id)
            print("✓ Contact deleted")
        except Exception as e:
            print(f"✗ Delete contact error: {e}")

    if task_id:
        print("\n[Cleanup] Deleting test task...")
        try:
            client.delete_task(task_id)
            print("✓ Task deleted")
        except Exception as e:
            print(f"✗ Delete task error: {e}")

    print("\n" + "="*50)
    print("Tests completed!")
    print("="*50)

    print("\nNote: Clean up test account 'Test Account Inc.' manually in Freshsales.")


if __name__ == "__main__":
    main()
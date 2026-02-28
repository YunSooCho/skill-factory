"""
Senses API Client Test Suite
Run with: python test_senses.py

NOTE: This test requires valid Senses credentials.
"""

import os
from senses_client import SensesClient, SensesAPIError


def main():
    # Test configuration
    API_KEY = os.environ.get("SENSES_API_KEY")

    if not API_KEY:
        print("ERROR: SENSES_API_KEY environment variable required")
        return

    client = SensesClient(API_KEY)

    # Test 1: Create Form
    print("\n[Test 1] Creating form...")
    try:
        fields = [
            {"type": "text", "name": "name", "label": "Name", "required": True},
            {"type": "email", "name": "email", "label": "Email", "required": True}
        ]
        response = client.create_form(
            name="Test Form",
            fields=fields
        )
        form_id = response.get('data', {}).get('id')
        print(f"✓ Form created: {form_id}")
    except SensesAPIError as e:
        print(f"✗ Create form failed: {e}")
        form_id = None

    # Test 2: Get Form
    if form_id:
        print("\n[Test 2] Getting form...")
        try:
            response = client.get_form(form_id)
            print(f"✓ Form retrieved: {response.get('data', {}).get('name')}")
        except SensesAPIError as e:
            print(f"✗ Get form failed: {e}")

    # Test 3: Update Form
    if form_id:
        print("\n[Test 3] Updating form...")
        try:
            response = client.update_form(
                form_id=form_id,
                name="Updated Test Form"
            )
            print(f"✓ Form updated")
        except SensesAPIError as e:
            print(f"✗ Update form failed: {e}")

    # Test 4: Create Campaign
    print("\n[Test 4] Creating campaign...")
    try:
        response = client.create_campaign(
            name="Test Campaign",
            type="email",
            status="draft"
        )
        campaign_id = response.get('data', {}).get('id')
        print(f"✓ Campaign created: {campaign_id}")
    except SensesAPIError as e:
        print(f"✗ Create campaign failed: {e}")
        campaign_id = None

    # Test 5: Get Campaign
    if campaign_id:
        print("\n[Test 5] Getting campaign...")
        try:
            response = client.get_campaign(campaign_id)
            print(f"✓ Campaign retrieved: {response.get('data', {}).get('name')}")
        except SensesAPIError as e:
            print(f"✗ Get campaign failed: {e}")

    # Test 6: Create User
    print("\n[Test 6] Creating user...")
    try:
        response = client.create_user(
            email="test.user@example.com",
            first_name="Test",
            last_name="User"
        )
        user_id = response.get('data', {}).get('id')
        print(f"✓ User created: {user_id}")
    except SensesAPIError as e:
        print(f"✗ Create user failed: {e}")
        user_id = None

    # Test 7: Get User
    if user_id:
        print("\n[Test 7] Getting user...")
        try:
            response = client.get_user(user_id)
            print(f"✓ User retrieved: {response.get('data', {}).get('email')}")
        except SensesAPIError as e:
            print(f"✗ Get user failed: {e}")

    # Test 8: Create Segment
    print("\n[Test 8] Creating segment...")
    try:
        criteria = {
            "field": "email",
            "operator": "contains",
            "value": "@example.com"
        }
        response = client.create_segment(
            name="Test Segment",
            criteria=criteria
        )
        segment_id = response.get('data', {}).get('id')
        print(f"✓ Segment created: {segment_id}")
    except SensesAPIError as e:
        print(f"✗ Create segment failed: {e}")
        segment_id = None

    # Test 9: Get Segment
    if segment_id:
        print("\n[Test 9] Getting segment...")
        try:
            response = client.get_segment(segment_id)
            print(f"✓ Segment retrieved: {response.get('data', {}).get('name')}")
        except SensesAPIError as e:
            print(f"✗ Get segment failed: {e}")

    # Test 10: Create Email Template
    print("\n[Test 10] Creating email template...")
    try:
        response = client.create_email_template(
            name="Test Template",
            subject="Test Subject",
            html_content="<h1>Test</h1><p>Content</p>"
        )
        print(f"✓ Email template created")
    except SensesAPIError as e:
        print(f"✗ Create email template failed: {e}")

    # Cleanup
    if form_id:
        print("\n[Cleanup] Deleting test form...")
        try:
            client.delete_form(form_id)
            print("✓ Form deleted")
        except Exception as e:
            print(f"✗ Delete form error: {e}")

    if user_id:
        print("\n[Cleanup] Deleting test user...")
        try:
            client.delete_user(user_id)
            print("✓ User deleted")
        except Exception as e:
            print(f"✗ Delete user error: {e}")

    if segment_id:
        print("\n[Cleanup] Deleting test segment...")
        try:
            client.delete_segment(segment_id)
            print("✓ Segment deleted")
        except Exception as e:
            print(f"✗ Delete segment error: {e}")

    print("\n" + "="*50)
    print("Tests completed!")
    print("="*50)

    print("\nNote: Clean up test campaign manually in Senses dashboard.")


if __name__ == "__main__":
    main()
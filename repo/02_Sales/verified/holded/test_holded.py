"""
Holded API Client Test Suite
Run with: python test_holded.py

NOTE: This test requires valid Holded credentials.
"""

import os
from holded_client import HoldedClient, HoldedAPIError


def main():
    # Test configuration
    API_KEY = os.environ.get("HOLDED_API_KEY")

    if not API_KEY:
        print("ERROR: HOLDED_API_KEY environment variable required")
        return

    client = HoldedClient(API_KEY)

    # Test 1: Create Contact
    print("\n[Test 1] Creating contact...")
    try:
        response = client.create_contact(
            name="Test Contact",
            email="test@example.com",
            phone="+1234567890"
        )
        contact_id = response.get('data', {}).get('id')
        print(f"✓ Contact created: {contact_id}")
    except HoldedAPIError as e:
        print(f"✗ Create contact failed: {e}")
        contact_id = None

    # Test 2: Get Contact
    if contact_id:
        print("\n[Test 2] Getting contact...")
        try:
            response = client.get_contact(contact_id)
            print(f"✓ Contact retrieved: {response.get('data', {}).get('name')}")
        except HoldedAPIError as e:
            print(f"✗ Get contact failed: {e}")

    # Test 3: Update Contact
    if contact_id:
        print("\n[Test 3] Updating contact...")
        try:
            response = client.update_contact(
                contact_id=contact_id,
                email="updated@example.com"
            )
            print(f"✓ Contact updated")
        except HoldedAPIError as e:
            print(f"✗ Update contact failed: {e}")

    # Test 4: Search Contacts
    print("\n[Test 4] Searching contacts...")
    try:
        response = client.search_contacts(limit=10)
        print(f"✓ Found contacts")
    except HoldedAPIError as e:
        print(f"✗ Search contacts failed: {e}")

    # Test 5: Create Product
    print("\n[Test 5] Creating product...")
    try:
        response = client.create_product(
            name="Test Product",
            description="A test product",
            sale_price=99.99,
            cost=50.00,
            sku="TEST-SKU-001"
        )
        product_id = response.get('data', {}).get('id')
        print(f"✓ Product created: {product_id}")
    except HoldedAPIError as e:
        print(f"✗ Create product failed: {e}")
        product_id = None

    # Test 6: Get Product
    if product_id:
        print("\n[Test 6] Getting product...")
        try:
            response = client.get_product(product_id)
            print(f"✓ Product retrieved: {response.get('data', {}).get('name')}")
        except HoldedAPIError as e:
            print(f"✗ Get product failed: {e}")

    # Test 7: Update Product
    if product_id:
        print("\n[Test 7] Updating product...")
        try:
            response = client.update_product(
                product_id=product_id,
                sale_price=89.99
            )
            print(f"✓ Product updated")
        except HoldedAPIError as e:
            print(f"✗ Update product failed: {e}")

    # Test 8: Search Payments
    print("\n[Test 8] Searching payments...")
    try:
        response = client.search_payments(limit=10)
        print(f"✓ Found payments")
    except HoldedAPIError as e:
        print(f"✗ Search payments failed: {e}")

    # Test 9: Get Payment (if available)
    print("\n[Test 9] Getting payments to test get_payment()...")
    try:
        response = client.search_payments(limit=1)
        payments = response.get('data', [])
        if payments:
            payment_id = payments[0].get('id')
            payment = client.get_payment(payment_id)
            print(f"✓ Payment retrieved: {payment_id}")
        else:
            print("⊘ No payments available to test")
    except HoldedAPIError as e:
        print(f"✗ Get payment failed: {e}")

    # Test 10: Delete Contact (cleanup)
    if contact_id:
        print("\n[Test 10] Deleting test contact...")
        try:
            response = client.delete_contact(contact_id)
            print(f"✓ Contact deleted")
        except HoldedAPIError as e:
            print(f"✗ Delete contact failed: {e}")

    print("\n" + "="*50)
    print("Tests completed!")
    print("="*50)

    print("\nNote: Clean up any test data created in your Holded account.")


if __name__ == "__main__":
    main()
"""
Sho Bugyo API Client Test Suite
Run with: python test_sho_bugyo.py

NOTE: This test requires valid Sho Bugyo credentials.
"""

import os
from sho_bugyo_client import ShoBugyoClient, ShoBugyoAPIError


def main():
    # Test configuration
    API_KEY = os.environ.get("SHOBUGYO_API_KEY")
    COMPANY_ID = os.environ.get("SHOBUGYO_COMPANY_ID")
    TEST_CUSTOMER_CODE = "TEST001"
    TEST_ITEM_CODE = "ITEMTEST001"

    if not API_KEY or not COMPANY_ID:
        print("ERROR: SHOBUGYO_API_KEY and SHOBUGYO_COMPANY_ID environment variables required")
        return

    client = ShoBugyoClient(API_KEY, COMPANY_ID)

    # Test 1: Create Customer
    print("\n[Test 1] Creating customer...")
    try:
        response = client.create_or_update_customer(
            customer_code=TEST_CUSTOMER_CODE,
            customer_name="テスト顧客株式会社",
            postal_code="100-0001",
            address="東京都千代田区1-1-1"
        )
        print(f"✓ Customer created: {response.get('data').get('customerCode')}")
    except ShoBugyoAPIError as e:
        print(f"✗ Create customer failed: {e}")

    # Test 2: Search Customers
    print("\n[Test 2] Searching customers...")
    try:
        response = client.search_customers(
            customer_code=TEST_CUSTOMER_CODE
        )
        data = response.get('data', {})
        print(f"✓ Found customers")
    except ShoBugyoAPIError as e:
        print(f"✗ Search customers failed: {e}")

    # Test 3: Create Product
    print("\n[Test 3] Creating product...")
    try:
        response = client.create_or_update_product(
            item_code=TEST_ITEM_CODE,
            item_name="テスト商品",
            sales_price=1000,
            purchase_price=800,
            tax_type="01",
            unit_name="個"
        )
        print(f"✓ Product created: {response.get('data').get('itemCode')}")
    except ShoBugyoAPIError as e:
        print(f"✗ Create product failed: {e}")

    # Test 4: Search Products
    print("\n[Test 4] Searching products...")
    try:
        response = client.search_products(
            item_code=TEST_ITEM_CODE
        )
        data = response.get('data', {})
        print(f"✓ Found products")
    except ShoBugyoAPIError as e:
        print(f"✗ Search products failed: {e}")

    # Test 5: Create Estimate
    print("\n[Test 5] Creating estimate...")
    try:
        items = [
            {
                "item_code": TEST_ITEM_CODE,
                "item_name": "テスト商品",
                "quantity": 10,
                "unit_price": 1000,
                "tax_type": "01"
            }
        ]

        response = client.create_estimate(
            customer_code=TEST_CUSTOMER_CODE,
            issue_date="2026-02-28",
            items=items
        )
        print(f"✓ Estimate created")
    except ShoBugyoAPIError as e:
        print(f"✗ Create estimate failed: {e}")

    # Test 6: Create Sales Order
    print("\n[Test 6] Creating sales order...")
    try:
        response = client.create_sales_order(
            customer_code=TEST_CUSTOMER_CODE,
            issue_date="2026-02-28",
            items=items,
            order_number="TEST-SO-001"
        )
        print(f"✓ Sales order created")
    except ShoBugyoAPIError as e:
        print(f"✗ Create sales order failed: {e}")

    # Test 7: Get Sales Order
    print("\n[Test 7] Getting sales order...")
    try:
        response = client.get_sales_order("TEST-SO-001")
        print(f"✓ Sales order retrieved")
    except ShoBugyoAPIError as e:
        print(f"✗ Get sales order failed: {e}")

    # Test 8: Search Sales Orders
    print("\n[Test 8] Searching sales orders...")
    try:
        response = client.search_sales_orders(
            customer_code=TEST_CUSTOMER_CODE,
            limit=10
        )
        print(f"✓ Sales orders searched")
    except ShoBugyoAPIError as e:
        print(f"✗ Search sales orders failed: {e}")

    # Test 9: Create Sales Invoice
    print("\n[Test 9] Creating sales invoice...")
    try:
        response = client.create_sales_invoice(
            customer_code=TEST_CUSTOMER_CODE,
            issue_date="2026-02-28",
            items=items,
            invoice_number="TEST-INV-001"
        )
        print(f"✓ Sales invoice created")
    except ShoBugyoAPIError as e:
        print(f"✗ Create sales invoice failed: {e}")

    # Test 10: Get Sales Invoice
    print("\n[Test 10] Getting sales invoice...")
    try:
        response = client.get_sales_invoice("TEST-INV-001")
        print(f"✓ Sales invoice retrieved")
    except ShoBugyoAPIError as e:
        print(f"✗ Get sales invoice failed: {e}")

    print("\n" + "="*50)
    print("Tests completed!")
    print("="*50)

    print("\nNote: Clean up test data (customer 'TEST001', product 'ITEMTEST001')")
    print("in your Sho Bugyo system after testing.")


if __name__ == "__main__":
    main()
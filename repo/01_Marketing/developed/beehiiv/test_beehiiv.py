"""
Test file for Beehiiv API client

Usage:
1. Replace 'your_api_key_here' and 'pub_your_publication_id_here' with actual credentials
2. Run: python test_beehiiv.py
"""

import asyncio
from beehiiv_client import (
    BeehiivAPIClient,
    SubscriptionCreateRequest,
    SubscriptionUpdateRequest
)


async def test_create_subscription():
    """Test creating a subscription"""
    print("=== Testing Create Subscription ===")

    api_key = "your_api_key_here"
    publication_id = "pub_your_publication_id_here"

    async with BeehiivAPIClient(api_key=api_key, publication_id=publication_id) as client:
        request = SubscriptionCreateRequest(
            email="test@example.com",
            send_welcome_email=False,
            utm_source="test",
            utm_medium="api",
            custom_fields=[
                {"name": "Test Field", "value": "Test Value"}
            ]
        )

        try:
            subscription = await client.create_subscription(request)
            print(f"✓ Subscription created: {subscription.id}")
            print(f"  Email: {subscription.email}")
            print(f"  Status: {subscription.status}")
            print(f"  Tier: {subscription.subscription_tier}")
            return subscription.id
        except Exception as e:
            print(f"✗ Failed: {e}")
            return None


async def test_get_subscription(sub_id: str):
    """Test getting subscription by ID"""
    print(f"\n=== Testing Get Subscription by ID ===")

    api_key = "your_api_key_here"
    publication_id = "pub_your_publication_id_here"

    async with BeehiivAPIClient(api_key=api_key, publication_id=publication_id) as client:
        try:
            sub = await client.get_subscription_by_id(sub_id)
            print(f"✓ Retrieved: {sub.email}")
            print(f"  Status: {sub.status}")
            print(f"  Created: {sub.created}")
            return True
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False


async def test_get_subscription_by_email():
    """Test getting subscription by email"""
    print(f"\n=== Testing Get Subscription by Email ===")

    api_key = "your_api_key_here"
    publication_id = "pub_your_publication_id_here"

    async with BeehiivAPIClient(api_key=api_key, publication_id=publication_id) as client:
        try:
            sub = await client.get_subscription_by_email("test@example.com")
            print(f"✓ Retrieved: {sub.email}")
            print(f"  ID: {sub.id}")
            print(f"  Status: {sub.status}")
            return True
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False


async def test_list_subscriptions():
    """Test listing subscriptions"""
    print("\n=== Testing List Subscriptions ===")

    api_key = "your_api_key_here"
    publication_id = "pub_your_publication_id_here"

    async with BeehiivAPIClient(api_key=api_key, publication_id=publication_id) as client:
        try:
            result = await client.list_subscriptions(limit=5)
            print(f"✓ Total: {result['results']} subscriptions")
            for sub in result["data"][:3]:
                print(f"  - {sub.email}: {sub.status}")
            return len(result["data"])
        except Exception as e:
            print(f"✗ Failed: {e}")
            return 0


async def test_list_subscriber_ids():
    """Test listing subscriber IDs (lightweight)"""
    print("\n=== Testing List Subscriber IDs ===")

    api_key = "your_api_key_here"
    publication_id = "pub_your_publication_id_here"

    async with BeehiivAPIClient(api_key=api_key, publication_id=publication_id) as client:
        try:
            result = await client.list_subscriber_ids(limit=5)
            print(f"✓ Total: {result['results']} IDs")
            print(f"  IDs: {result['data']}")
            return True
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False


async def test_update_subscription(sub_id: str):
    """Test updating subscription"""
    print(f"\n=== Testing Update Subscription ===")

    api_key = "your_api_key_here"
    publication_id = "pub_your_publication_id_here"

    async with BeehiivAPIClient(api_key=api_key, publication_id=publication_id) as client:
        request = SubscriptionUpdateRequest(tier="premium")
        try:
            updated = await client.update_subscription(sub_id, request)
            print(f"✓ Updated subscription tier: {updated.subscription_tier}")
            return True
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False


async def test_add_tags(sub_id: str):
    """Test adding tags to subscription"""
    print(f"\n=== Testing Add Tags ===")

    api_key = "your_api_key_here"
    publication_id = "pub_your_publication_id_here"

    async with BeehiivAPIClient(api_key=api_key, publication_id=publication_id) as client:
        try:
            result = await client.add_tags_to_subscription(sub_id, ["Test Tag", "API"])
            print(f"✓ Tags added successfully")
            return True
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False


async def test_list_posts():
    """Test listing posts"""
    print("\n=== Testing List Posts ===")

    api_key = "your_api_key_here"
    publication_id = "pub_your_publication_id_here"

    async with BeehiivAPIClient(api_key=api_key, publication_id=publication_id) as client:
        try:
            result = await client.list_posts(limit=5, status="confirmed")
            print(f"✓ Total: {result['results']} posts")
            return True
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False


async def test_search_posts():
    """Test searching posts"""
    print("\n=== Testing Search Posts ===")

    api_key = "your_api_key_here"
    publication_id = "pub_your_publication_id_here"

    async with BeehiivAPIClient(api_key=api_key, publication_id=publication_id) as client:
        try:
            result = await client.search_posts(query="newsletter", status="confirmed", limit=5)
            print(f"✓ Found: {result['results']} matching posts")
            return True
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False


async def test_list_segments():
    """Test listing segments"""
    print("\n=== Testing List Segments ===")

    api_key = "your_api_key_here"
    publication_id = "pub_your_publication_id_here"

    async with BeehiivAPIClient(api_key=api_key, publication_id=publication_id) as client:
        try:
            result = await client.list_segments()
            print(f"✓ Total: {result['results']} segments")
            for seg in result["data"][:3]:
                print(f"  - {seg.name}: {seg.count} subscribers")
            return True
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False


async def test_delete_subscription(sub_id: str):
    """Test deleting subscription"""
    print(f"\n=== Testing Delete Subscription ===")

    api_key = "your_api_key_here"
    publication_id = "pub_your_publication_id_here"

    response = input(f"Delete subscription {sub_id}? (y/N): ")
    if response.lower() != 'y':
        print("Skipped")
        return False

    async with BeehiivAPIClient(api_key=api_key, publication_id=publication_id) as client:
        try:
            success = await client.delete_subscription(sub_id)
            if success:
                print(f"✓ Deleted successfully")
            return success
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False


async def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Beehiiv API Client Test Suite")
    print("=" * 60)

    # Test 1: Create subscription
    sub_id = await test_create_subscription()

    if not sub_id:
        print("\n❌ Cannot proceed without a subscription")
        return

    # Test 2: Get by ID
    await test_get_subscription(sub_id)

    # Test 3: Get by email
    await test_get_subscription_by_email()

    # Test 4: List subscriptions
    await test_list_subscriptions()

    # Test 5: List subscriber IDs
    await test_list_subscriber_ids()

    # Test 6: Update subscription
    await test_update_subscription(sub_id)

    # Test 7: Add tags
    await test_add_tags(sub_id)

    # Test 8: List posts
    await test_list_posts()

    # Test 9: Search posts
    await test_search_posts()

    # Test 10: List segments
    await test_list_segments()

    # Test 11: Delete (optional)
    # await test_delete_subscription(sub_id)

    print("\n" + "=" * 60)
    print("Test suite completed")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
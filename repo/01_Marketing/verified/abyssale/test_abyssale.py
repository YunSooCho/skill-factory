"""
Test suite for Abyssale API client
Run with valid API key to test all endpoints
"""

import asyncio
import os
from abyssale_client import AbyssaleClient


async def test_generate_content():
    """Test content generation"""
    print("\n=== Testing Content Generation ===")

    api_key = os.getenv("ABYSSALE_API_KEY", "test_key")

    client = AbyssaleClient(api_key=api_key)

    try:
        # Step 1: List templates to get a template_id
        print("1. Listing templates...")
        templates = await client.list_templates(limit=10)
        print(f"   Found {len(templates)} templates")

        if not templates:
            print("   ⚠️  No templates found. Create one in Abyssale dashboard first.")
            print("   ⏭️  Skipping generation test")
            return

        # Show first few templates
        print("   First 3 templates:")
        for t in templates[:3]:
            print(f"     - {t.get('name', 'Unknown')} (ID: {t.get('id', 'Unknown')})")

        template_id = templates[0].get("id")

        # Step 2: Generate content
        print(f"\n2. Generating content using template {template_id}...")
        generation = await client.generate_content(
            template_id=template_id,
            format="jpg",
            elements={
                "title": "Test Generated",
                "subtitle": "Abyssale API Test"
            },
            async_mode=False
        )
        print(f"   Generation ID: {generation.generation_id}")
        print(f"   Status: {generation.status}")

        if generation.error:
            print(f"   ⚠️  Error: {generation.error}")

        assert generation.generation_id, "Generation ID should not be empty"
        print("   ✅ GENERATION CREATED")

        # Step 3: Check status if async
        if generation.status == "pending":
            print("\n3. Checking async status...")
            await asyncio.sleep(2)
            status = await client.get_generation_status(generation.generation_id)
            print(f"   Updated status: {status.status}")
            print("   ✅ STATUS CHECKED")

        return generation.generation_id

    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print("   Note: Requires valid API key and at least one template")
        return None
    finally:
        await client.session.close()


async def test_get_file():
    """Test file retrieval"""
    print("\n=== Testing File Operations ===")

    api_key = os.getenv("ABYSSALE_API_KEY", "test_key")

    client = AbyssaleClient(api_key=api_key)

    try:
        # Generate content first
        print("1. Creating test generation...")
        templates = await client.list_templates(limit=10)

        if not templates:
            print("   ⚠️  No templates available")
            return

        generation = await client.generate_content(
            template_id=templates[0].get("id"),
            format="jpg",
            async_mode=False
        )

        # Wait for completion if pending
        if generation.status == "pending":
            await asyncio.sleep(3)
            generation = await client.get_generation_status(generation.generation_id)

        # Get file info
        print("2. Getting file info...")
        file_info = await client.get_file(generation.generation_id)
        print(f"   File: {file_info.name}")
        print(f"   MIME: {file_info.mime_type}")
        print(f"   Size: {file_info.size} bytes")
        print(f"   URL: {file_info.url}")

        assert file_info.url, "File URL should not be empty"
        print("   ✅ FILE INFO RETRIEVED")

        # Download file
        print("\n3. Downloading file...")
        content = await client.download_file(generation.generation_id)
        print(f"   Downloaded {len(content)} bytes")

        assert len(content) > 0, "Content should not be empty"
        print("   ✅ FILE DOWNLOADED")

    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print("   Note: Requires successful generation first")
    finally:
        await client.session.close()


async def test_webhook_signature():
    """Test webhook signature verification"""
    print("\n=== Testing Webhook Signature ===")

    api_key = os.getenv("ABYSSALE_API_KEY", "test_key")
    webhook_secret = "test_webhook_secret"

    payload = b'{"event":"generation.completed"}'
    signature = AbyssaleClient.verify_webhook_signature(
        payload, webhook_secret, webhook_secret
    )

    print(f"1. Signature verification: {signature}")
    assert signature, "Signature verification should succeed with matching secret"
    print("   ✅ SIGNATURE VERIFIED")

    # Test invalid signature
    invalid_signature = AbyssaleClient.verify_webhook_signature(
        payload, "invalid_signature", webhook_secret
    )
    print(f"2. Invalid signature: {not invalid_signature}")
    assert not invalid_signature, "Should fail with invalid signature"
    print("   ✅ INVALID SIGNATURE REJECTED")

    # Test webhook handling
    event_data = {"event": "generation.completed", "data": {"id": "123"}}
    event = AbyssaleClient.handle_webhook_event(None, event_data)
    print(f"3. Event type: {event}")
    assert event == "generation.completed", "Should extract event type"
    print("   ✅ EVENT HANDLED")


async def test_template_operations():
    """Test template listing and details"""
    print("\n=== Testing Template Operations ===")

    api_key = os.getenv("ABYSSALE_API_KEY", "test_key")

    client = AbyssaleClient(api_key=api_key)

    try:
        # List templates
        print("1. Listing templates (limit 5)...")
        templates = await client.list_templates(limit=5)
        print(f"   Found {len(templates)} templates")

        assert isinstance(templates, list), "Templates should be a list"
        print("   ✅ TEMPLATES LISTED")

        if templates:
            # Get first template details
            template_id = templates[0].get("id")
            print(f"\n2. Getting template details for {template_id}...")
            details = await client.get_template(template_id)
            print(f"   Name: {details.get('name', 'Unknown')}")
            print(f"   Format: {details.get('format', 'Unknown')}")

            assert details, "Template details should not be empty"
            print("   ✅ TEMPLATE DETAILS RETRIEVED")
        else:
            print("   ⚠️  No templates to get details")

    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print("   Note: Requires valid API key")
    finally:
        await client.session.close()


async def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Abyssale API Test Suite")
    print("=" * 60)
    print("\nNote: Set API key as environment variable to test")
    print("Example:")
    print("  export ABYSSALE_API_KEY='your_key'")
    print("")
    print("Tip: Create at least one template in the Abyssale dashboard first")
    print("")

    await test_template_operations()
    generation_id = await test_generate_content()

    if generation_id:
        await test_get_file()

    await test_webhook_signature()

    print("\n" + "=" * 60)
    print("Test Suite Complete")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
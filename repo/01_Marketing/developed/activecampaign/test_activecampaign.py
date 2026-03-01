"""
Test suite for ActiveCampaign API client
Run with valid API credentials to test all endpoints
"""

import asyncio
import os
from activecampaign_client import ActiveCampaignClient


async def test_account_operations():
    """Test account operations"""
    print("\n=== Testing Account Operations ===")

    api_url = os.getenv("ACTIVECAMPAIGN_API_URL", "https://test.api-us1.com/api/3")
    api_key = os.getenv("ACTIVECAMPAIGN_API_KEY", "test_key")

    client = ActiveCampaignClient(api_url=api_url, api_key=api_key)

    try:
        # Test 1: Create account
        print("1. Creating account...")
        account = await client.create_account(
            name="Test Account",
            account_url="https://test.example.com"
        )
        print(f"   Account ID: {account.id}")
        print(f"   Name: {account.name}")
        assert account.id, "Account ID should not be empty"
        print("   ✅ ACCOUNT CREATED")

        # Test 2: Get account
        print("\n2. Getting account...")
        get_account = await client.get_account(account.id)
        print(f"   Got: {get_account.name}")
        assert get_account.id == account.id, "Should get same account"
        print("   ✅ ACCOUNT RETRIEVED")

        # Test 3: Update account
        print("\n3. Updating account...")
        updated = await client.update_account(
            account.id,
            name="Updated Test Account"
        )
        print(f"   New name: {updated.name}")
        assert updated.name == "Updated Test Account", "Name should be updated"
        print("   ✅ ACCOUNT UPDATED")

        # Cleanup
        await client.delete_account(account.id)
        print("\n4. Deleting account...")
        print("   ✅ ACCOUNT DELETED")

    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print("   Note: Requires valid API URL and key")
    finally:
        await client.session.close()


async def test_contact_operations():
    """Test contact operations"""
    print("\n=== Testing Contact Operations ===")

    api_url = os.getenv("ACTIVECAMPAIGN_API_URL", "https://test.api-us1.com/api/3")
    api_key = os.getenv("ACTIVECAMPAIGN_API_KEY", "test_key")

    client = ActiveCampaignClient(api_url=api_url, api_key=api_key)

    try:
        # Test 1: Create contact
        print("1. Creating contact...")
        contact = await client.create_contact(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            phone="+1234567890"
        )
        print(f"   Contact ID: {contact.id}")
        print(f"   Email: {contact.email}")
        assert contact.id, "Contact ID should not be empty"
        print("   ✅ CONTACT CREATED")

        # Test 2: Get contact
        print("\n2. Getting contact...")
        get_contact = await client.get_contact(contact.id)
        print(f"   Got: {get_contact.email}")
        assert get_contact.id == contact.id, "Should get same contact"
        print("   ✅ CONTACT RETRIEVED")

        # Test 3: Search contacts
        print("\n3. Searching contacts...")
        contacts = await client.search_contacts(email="test@example.com")
        print(f"   Found {len(contacts)} contacts")
        assert isinstance(contacts, list), "Should return list"
        print("   ✅ CONTACTS SEARCHED")

        # Test 4: Get contact score
        print("\n4. Getting contact score...")
        score = await client.get_contact_score(contact.id)
        print(f"   Score: {score}")
        assert isinstance(score, int), "Score should be integer"
        print("   ✅ CONTACT SCORE RETRIEVED")

        # Cleanup
        await client.delete_contact(contact.id)
        print("\n5. Deleting contact...")
        print("   ✅ CONTACT DELETED")

    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print("   Note: Requires valid API URL and key")
    finally:
        await client.session.close()


async def test_deal_operations():
    """Test deal operations"""
    print("\n=== Testing Deal Operations ===")

    api_url = os.getenv("ACTIVECAMPAIGN_API_URL", "https://test.api-us1.com/api/3")
    api_key = os.getenv("ACTIVECAMPAIGN_API_KEY", "test_key")

    client = ActiveCampaignClient(api_url=api_url, api_key=api_key)

    try:
        # Create contact first
        print("1. Creating contact for deal...")
        contact = await client.create_contact(email="deal@example.com")
        print(f"   Contact ID: {contact.id}")

        # Create deal
        print("\n2. Creating deal...")
        deal = await client.create_deal(
            contact_id=contact.id,
            value=1500.00,
            currency="USD",
            stage="proposal"
        )
        print(f"   Deal ID: {deal.id}")
        print(f"   Value: ${deal.value}")
        assert deal.id, "Deal ID should not be empty"
        print("   ✅ DEAL CREATED")

        # Cleanup
        await client.delete_contact(contact.id)
        print("\n3. Cleanup contact...")
        print("   ✅ CLEANUP COMPLETE")

    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print("   Note: Requires valid API URL and key")
    finally:
        await client.session.close()


async def test_contact_account_link():
    """Test contact-account linking"""
    print("\n=== Testing Contact-Account Link ===")

    api_url = os.getenv("ACTIVECAMPAIGN_API_URL", "https://test.api-us1.com/api/3")
    api_key = os.getenv("ACTIVECAMPAIGN_API_KEY", "test_key")

    client = ActiveCampaignClient(api_url=api_url, api_key=api_key)

    try:
        # Create account and contact
        print("1. Creating account and contact...")
        account = await client.create_account(name="Test Corp")
        contact = await client.create_contact(email="link@example.com")
        print(f"   Account ID: {account.id}")
        print(f"   Contact ID: {contact.id}")

        # Link them
        print("\n2. Linking contact to account...")
        linked = await client.link_contact_account(contact.id, account.id)
        print(f"   Linked: {linked}")
        assert linked, "Linking should succeed"
        print("   ✅ CONTACT LINKED TO ACCOUNT")

        # Cleanup
        await client.delete_account(account.id)
        await client.delete_contact(contact.id)
        print("\n3. Cleanup...")
        print("   ✅ CLEANUP COMPLETE")

    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print("   Note: Requires valid API URL and key")
    finally:
        await client.session.close()


async def test_notes_operations():
    """Test note operations"""
    print("\n=== Testing Note Operations ===")

    api_url = os.getenv("ACTIVECAMPAIGN_API_URL", "https://test.api-us1.com/api/3")
    api_key = os.getenv("ACTIVECAMPAIGN_API_KEY", "test_key")

    client = ActiveCampaignClient(api_url=api_url, api_key=api_key)

    try:
        # Create contact
        print("1. Creating contact...")
        contact = await client.create_contact(email="note@example.com")
        print(f"   Contact ID: {contact.id}")

        # Add note
        print("\n2. Adding note...")
        note = await client.add_note(
            contact_id=contact.id,
            note="Test note from API"
        )
        print(f"   Note ID: {note.id}")
        print(f"   Note: {note.note}")
        assert note.id, "Note ID should not be empty"
        print("   ✅ NOTE ADDED")

        # Cleanup
        await client.delete_contact(contact.id)
        print("\n3. Cleanup...")
        print("   ✅ CLEANUP COMPLETE")

    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print("   Note: Requires valid API URL and key")
    finally:
        await client.session.close()


async def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("ActiveCampaign API Test Suite")
    print("=" * 60)
    print("\nNote: Set environment variables to test")
    print("Example:")
    print("  export ACTIVECAMPAIGN_API_URL='https://your-account.api-us1.com/api/3'")
    print("  export ACTIVECAMPAIGN_API_KEY='your_key'")
    print("")

    await test_contact_operations()
    await test_account_operations()
    await test_deal_operations()
    await test_contact_account_link()
    await test_notes_operations()

    print("\n" + "=" * 60)
    print("Test Suite Complete")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
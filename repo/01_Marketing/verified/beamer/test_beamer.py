"""
Test file for Beamer API client

Usage:
1. Replace 'your_api_key_here' with your actual Beamer API key
2. Run: python test_beamer.py
"""

import asyncio
from beamer_client import BeamerAPIClient, PostCreation


async def test_connection():
    """Test API connection and authentication"""
    print("=== Testing Connection ===")

    api_key = "your_api_key_here"  # Replace with your actual API key

    async with BeamerAPIClient(api_key=api_key) as client:
        try:
            status = await client.ping()
            print(f"✓ Connected to Beamer: {status.get('name', 'Unknown')}")
            return True
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False


async def test_create_post():
    """Test creating a post"""
    print("\n=== Testing Create Post ===")

    api_key = "your_api_key_here"  # Replace with your actual API key

    async with BeamerAPIClient(api_key=api_key) as client:
        post_data = PostCreation(
            title=["Test Post from API"],
            content=["This is a test post created via the Beamer API client."],
            category="new",
            publish=True,
            language=["EN"]
        )

        try:
            post = await client.create_post(post_data)
            print(f"✓ Post created successfully")
            print(f"  ID: {post.id}")
            print(f"  Published: {post.published}")
            print(f"  Category: {post.category}")
            print(f"  Views: {post.views}")
            return post.id
        except Exception as e:
            print(f"✗ Failed to create post: {e}")
            return None


async def test_create_multilingual_post():
    """Test creating a post with multiple translations"""
    print("\n=== Testing Multilingual Post ===")

    api_key = "your_api_key_here"  # Replace with your actual API key

    async with BeamerAPIClient(api_key=api_key) as client:
        post_data = PostCreation(
            title=["Test Post (EN)", "Test Post (FR)", "Test Post (ES)"],
            content=[
                "This is a test post in English.",
                "Ceci est un message de test en français.",
                "Este es un mensaje de prueba en español."
            ],
            category="new",
            language=["EN", "FR", "ES"],
            publish=True
        )

        try:
            post = await client.create_post(post_data)
            print(f"✓ Multilingual post created successfully")
            print(f"  ID: {post.id}")
            print(f"  Translations: {len(post.translations)}")
            for t in post.translations:
                print(f"    - {t.language}: {t.title}")
            return post.id
        except Exception as e:
            print(f"✗ Failed to create multilingual post: {e}")
            print("  Note: Multiple translations require Starter plan or higher")
            return None


async def test_get_posts():
    """Test retrieving posts"""
    print("\n=== Testing Get Posts ===")

    api_key = "your_api_key_here"  # Replace with your actual API key

    async with BeamerAPIClient(api_key=api_key) as client:
        try:
            posts = await client.get_posts(published=True, max_results=5)
            print(f"✓ Retrieved {len(posts)} published posts")
            for p in posts:
                if p.translations:
                    title = p.translations[0].title if p.translations else "No title"
                    print(f"  - {p.id}: {title} (Views: {p.views})")
            return len(posts)
        except Exception as e:
            print(f"✗ Failed to get posts: {e}")
            return None


async def test_get_post_by_id(post_id: str):
    """Test retrieving a specific post"""
    print(f"\n=== Testing Get Post by ID ({post_id}) ===")

    api_key = "your_api_key_here"  # Replace with your actual API key

    async with BeamerAPIClient(api_key=api_key) as client:
        try:
            post = await client.get_post_by_id(post_id)
            print(f"✓ Retrieved post:")
            if post.translations:
                print(f"  Title: {post.translations[0].title}")
            print(f"  Published: {post.published}")
            print(f"  Category: {post.category}")
            print(f"  Views: {post.views}, Unique: {post.unique_views}")
            print(f"  Clicks: {post.clicks}, Feedback: {post.feedbacks}")
            return True
        except Exception as e:
            print(f"✗ Failed to get post: {e}")
            return False


async def test_delete_post(post_id: str):
    """Test deleting a post"""
    print(f"\n=== Testing Delete Post ({post_id}) ===")

    api_key = "your_api_key_here"  # Replace with your actual API key

    # Ask for confirmation
    response = input(f"Delete post {post_id}? (y/N): ")
    if response.lower() != 'y':
        print("Skipped deletion")
        return False

    async with BeamerAPIClient(api_key=api_key) as client:
        try:
            success = await client.delete_post(post_id)
            if success:
                print(f"✓ Post deleted successfully")
            return success
        except Exception as e:
            print(f"✗ Failed to delete post: {e}")
            return False


async def run_all_tests():
    """Run all tests sequentially"""
    print("=" * 60)
    print("Beamer API Client Test Suite")
    print("=" * 60)

    # Test 1: Connection
    connected = await test_connection()
    if not connected:
        print("\n❌ Cannot proceed without valid API connection")
        return

    # Test 2: Create post
    post_id1 = await test_create_post()

    # Test 3: Multilingual post
    post_id2 = await test_create_multilingual_post()

    # Test 4: Get posts
    await test_get_posts()

    # Test 5: Get post by ID (if any post was created)
    if post_id1:
        await test_get_post_by_id(post_id1)

    # Test 6: Delete posts (only if user confirms)
    if post_id2:
        await test_delete_post(post_id2)

    print("\n" + "=" * 60)
    print("Test suite completed")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
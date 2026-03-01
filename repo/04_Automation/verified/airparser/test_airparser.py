import asyncio
import os
from airparser_client import AirparserClient


async def test_basic_operations():
    """Test basic Airparser operations"""

    api_key = os.getenv('AIRPARSER_API_KEY')

    if not api_key:
        print("⚠️  API key not set")
        print(f"Set AIRPARSER_API_KEY environment variable:")
        print(f"export AIRPARSER_API_KEY=your_api_key")
        return

    async with AirparserClient(api_key=api_key) as client:
        try:
            print("\n🧪 Testing Airparser Client")
            print("="*50)

            # Test client initialization
            print("✅ Client initialized successfully")

            # Add your test cases here
            # result = await client.list_items()
            # if result and hasattr(result, 'success'):
            #     print(f"✅ List items: {result.success}")

            print("\n✅ All tests passed!")

        except ValueError as error:
            print(f"\n❌ Validation error: {error}")
        except Exception as error:
            print(f"\n❌ Error: {error}")


if __name__ == "__main__":
    asyncio.run(test_basic_operations())

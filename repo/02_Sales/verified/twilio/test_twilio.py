"""
Twilio API Client Test Suite
Run with: python test_twilio.py

NOTE: This test requires valid Twilio credentials and will make actual API calls.
Use a test account to avoid charges.
"""

import os
from datetime import datetime, timedelta
from twilio_client import TwilioClient, TwilioAPIError


def main():
    # Test configuration
    ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
    TEST_NUMBER = os.environ.get("TWILIO_TEST_NUMBER", "+819012345678")
    TWILIO_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER", "+818012345678")

    if not ACCOUNT_SID or not AUTH_TOKEN:
        print("ERROR: TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables required")
        return

    client = TwilioClient(ACCOUNT_SID, AUTH_TOKEN)

    # Test 1: Send SMS
    print("\n[Test 1] Sending SMS...")
    try:
        response = client.send_sms(
            to=TEST_NUMBER,
            from_=TWILIO_NUMBER,
            body="Test message from Twilio Python client"
        )
        print(f"✓ SMS sent successfully: {response['data'].get('sid')}")
    except TwilioAPIError as e:
        print(f"✗ SMS failed: {e}")

    # Test 2: List Messages
    print("\n[Test 2] Listing messages...")
    try:
        response = client.list_messages(limit=5)
        messages = response['data'].get('messages', [])
        print(f"✓ Found {len(messages)} messages")
        if messages:
            print(f"  Latest: {messages[0].get('sid')}")
    except TwilioAPIError as e:
        print(f"✗ List messages failed: {e}")

    # Test 3: Get Message Details (if available)
    print("\n[Test 3] Getting message details...")
    try:
        response = client.list_messages(limit=1)
        messages = response['data'].get('messages', [])
        if messages:
            message_sid = messages[0].get('sid')
            details = client.get_message(message_sid)
            print(f"✓ Retrieved message details: {details['data'].get('sid')}")
        else:
            print("⊘ No messages available to test")
    except TwilioAPIError as e:
        print(f"✗ Get message failed: {e}")

    # Test 4: List Calls
    print("\n[Test 4] Listing calls...")
    try:
        response = client.list_calls(limit=5)
        calls = response['data'].get('calls', [])
        print(f"✓ Found {len(calls)} calls")
        if calls:
            print(f"  Latest: {calls[0].get('sid')}")
    except TwilioAPIError as e:
        print(f"✗ List calls failed: {e}")

    # Test 5: Filter Messages by Date
    print("\n[Test 5] Filtering messages by date...")
    try:
        yesterday = datetime.now() - timedelta(days=1)
        response = client.list_messages(
            date_sent_after=yesterday,
            limit=5
        )
        messages = response['data'].get('messages', [])
        print(f"✓ Found {len(messages)} messages since yesterday")
    except TwilioAPIError as e:
        print(f"✗ Filter messages failed: {e}")

    # Test 6: Make Call (optional - will charge)
    print("\n[Test 6] Making phone call (skipped - optional)...")
    print("  To test: client.make_call(to=TEST_NUMBER, from_=TWILIO_NUMBER, url=TWIML_URL)")

    # Test 7: Get Call Details
    print("\n[Test 7] Getting call details...")
    try:
        response = client.list_calls(limit=1)
        calls = response['data'].get('calls', [])
        if calls:
            call_sid = calls[0].get('sid')
            details = client.get_call(call_sid)
            print(f"✓ Retrieved call details: {details['data'].get('sid')}")
        else:
            print("⊘ No calls available to test")
    except TwilioAPIError as e:
        print(f"✗ Get call failed: {e}")

    print("\n" + "="*50)
    print("Tests completed!")
    print("="*50)


if __name__ == "__main__":
    main()
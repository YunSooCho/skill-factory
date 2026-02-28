"""
Telegram Bot API Client

Supports:
- メッセージを送信 (Send message)
"""

import requests
from typing import Optional, Dict, Any


class TelegramClient:
    """
    Telegram Bot API client for messaging operations.

    Authentication: Bot API Token
    Base URL: https://api.telegram.org/bot{token}
    """

    def __init__(self, bot_token: str):
        """
        Initialize Telegram Bot API client.

        Args:
            bot_token: Telegram Bot API Token (from @BotFather)
        """
        self.bot_token = bot_token
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.session = requests.Session()

    def _request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make API request with error handling"""
        url = f"{self.base_url}/{method}"

        try:
            response = self.session.post(url, json=params)

            data = response.json()

            if data.get("ok"):
                return data.get("result", {})
            else:
                error = data.get("description", "Unknown error")
                raise Exception(f"Telegram API error: {error}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def send_message(
        self,
        chat_id: str,
        text: str,
        parse_mode: Optional[str] = None,
        disable_web_page_preview: bool = False,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send message to a chat.

        Args:
            chat_id: Unique identifier for target chat (username or numeric ID)
            text: Text of the message to be sent (required)
            parse_mode: Mode for parsing entities (Markdown, MarkdownV2, HTML)
            disable_web_page_preview: Disables link previews for links in this message
            disable_notification: Sends the message silently
            reply_to_message_id: If the message is a reply, ID of the original message

        Returns:
            Dict containing sent message details

        Raises:
            ValueError: If text is empty
            Exception: If API request fails
        """
        if not text or not text.strip():
            raise ValueError("Message text cannot be empty")

        params: Dict[str, Any] = {
            "chat_id": chat_id,
            "text": text
        }

        if parse_mode:
            params["parse_mode"] = parse_mode

        if disable_web_page_preview:
            params["disable_web_page_preview"] = True

        if disable_notification:
            params["disable_notification"] = True

        if reply_to_message_id:
            params["reply_to_message_id"] = reply_to_message_id

        return self._request("sendMessage", params)

    def get_me(self) -> Dict[str, Any]:
        """
        Get basic information about the bot.

        Returns:
            Dict with bot information
        """
        return self._request("getMe")

    def get_updates(
        self,
        offset: Optional[int] = None,
        limit: int = 100,
        timeout: int = 0
    ) -> Dict[str, Any]:
        """
        Get incoming updates using long polling.

        Args:
            offset: Identifier of the first update to be returned
            limit: Limits the number of updates to be retrieved
            timeout: Timeout in seconds for long polling

        Returns:
            Dict with updates
        """
        params: Dict[str, Any] = {
            "limit": limit,
            "timeout": timeout
        }

        if offset:
            params["offset"] = offset

        return self._request("getUpdates", params)

    def set_webhook(self, webhook_url: str) -> Dict[str, Any]:
        """
        Set a webhook for receiving updates.

        Args:
            webhook_url: HTTPS URL to send updates to

        Returns:
            Dict with result
        """
        params = {"url": webhook_url}
        return self._request("setWebhook", params)

    def delete_webhook(self) -> Dict[str, Any]:
        """
        Remove webhook integration.

        Returns:
            Dict with result
        """
        return self._request("deleteWebhook")

    def get_webhook_info(self) -> Dict[str, Any]:
        """
        Get current webhook status.

        Returns:
            Dict with webhook information
        """
        return self._request("getWebhookInfo")

    def close(self):
        """Close the HTTP session"""
        self.session.close()


def main():
    """Example usage"""
    bot_token = "your_telegram_bot_token"

    client = TelegramClient(bot_token=bot_token)

    try:
        # Get bot information
        bot_info = client.get_me()
        print(f"Bot info: {bot_info}")

        # Send simple text message
        result = client.send_message(
            chat_id="channel_name_or_chat_id",
            text="Hello from Telegram Bot API!"
        )
        print(f"Message sent: {result}")

        # Send message with Markdown parsing
        result = client.send_message(
            chat_id="channel_name_or_chat_id",
            text="*Bold text* and _italic text_",
            parse_mode="Markdown"
        )
        print(f"Markdown message sent: {result}")

        # Send reply message
        result = client.send_message(
            chat_id="channel_name_or_chat_id",
            text="This is a reply!",
            reply_to_message_id="123"
        )
        print(f"Reply sent: {result}")

        # Send silent message
        result = client.send_message(
            chat_id="channel_name_or_chat_id",
            text="Silent message",
            disable_notification=True
        )
        print(f"Silent message sent: {result}")

        # Get updates (long polling)
        updates = client.get_updates(timeout=30)
        print(f"Updates: {updates}")

        # Set webhook
        result = client.set_webhook("https://your-webhook-url.com")
        print(f"Webhook set: {result}")

        # Get webhook info
        webhook_info = client.get_webhook_info()
        print(f"Webhook info: {webhook_info}")

        # Delete webhook
        result = client.delete_webhook()
        print(f"Webhook deleted: {result}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        client.close()


if __name__ == "__main__":
    main()
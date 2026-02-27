"""BotStar API"""

class BotStarAPIError(Exception):
    """Base exception for BotStar API errors"""
    pass

class BotStarAuthError(BotStarAPIError):
    """Authentication error"""
    pass
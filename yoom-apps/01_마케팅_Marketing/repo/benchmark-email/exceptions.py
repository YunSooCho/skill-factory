"""Benchmark Email API"""


class BenchmarkEmailAPIError(Exception):
    """Base exception for Benchmark Email API errors"""
    pass


class BenchmarkEmailAuthError(BenchmarkEmailAPIError):
    """Authentication error"""
    pass


class BenchmarkEmailRateLimitError(BenchmarkEmailAPIError):
    """Rate limit exceeded"""
    pass
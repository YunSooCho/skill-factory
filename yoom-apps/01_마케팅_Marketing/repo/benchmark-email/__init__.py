"""
Benchmark Email API Integration
API Reference: https://www.benchmarkemail.com/API/
"""

from .client import BenchmarkEmailClient
from .exceptions import BenchmarkEmailAPIError, BenchmarkEmailAuthError

__all__ = ['BenchmarkEmailClient', 'BenchmarkEmailAPIError', 'BenchmarkEmailAuthError']
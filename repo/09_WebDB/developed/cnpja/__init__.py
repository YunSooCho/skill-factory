"""
CNPJA - Cadastro Nacional da Pessoa Jurídica (Brazilian Company Registry)

This package provides a client for accessing Brazilian company registry data.
"""

from .client import CNPJAClient

__version__ = '1.0.0'
__all__ = ['CNPJAClient']
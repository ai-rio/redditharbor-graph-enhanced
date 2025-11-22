"""
RedditHarbor Graph Integration Module

This module provides Deep-Graph-MCP integration for intelligent code analysis,
dependency mapping, and automated refactoring suggestions.
"""

from .analyzer import RedditHarborGraphAnalyzer
from .dependencies import DependencyMapper
from .refactoring import IntelligentRefactorer

__version__ = "0.1.0"
__author__ = "RedditHarbor Team"

__all__ = [
    "RedditHarborGraphAnalyzer",
    "DependencyMapper",
    "IntelligentRefactorer"
]
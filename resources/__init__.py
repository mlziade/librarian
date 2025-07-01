"""
Resources package for the Librarian MCP server.

This package contains resource definitions for various services and APIs.
"""

from .wikipedia_resources import register_wikipedia_resources, WIKIPEDIA_RESOURCES

__all__ = ['register_wikipedia_resources', 'WIKIPEDIA_RESOURCES']

"""
Logging configuration for the Librarian MCP Server.
"""

import logging


def setup_logging(level=logging.INFO):
    """
    Configure logging for the application.

    Args:
        level: Logging level (default: logging.INFO)
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        force=True  # Override any existing configuration
    )


def get_logger(name: str):
    """
    Get a logger instance for the given name.

    Args:
        name: Usually __name__ from the calling module

    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)
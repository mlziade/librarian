"""
MCP Server for Librarian

Runs the Librarian MCP server using Streamable HTTP transport (MCP spec 2026-07-28).
The MCP endpoint is available at http://0.0.0.0:8000/mcp.
"""

import logging
from librarian import mcp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting Librarian MCP Server on http://0.0.0.0:8000/mcp ...")
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
        stateless_http=True,
    )

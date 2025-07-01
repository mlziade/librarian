from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Import Wikipedia tools
from tools.wikipedia_tools import register_wikipedia_tools

# Initialize FastMCP server
mcp = FastMCP("librarian")

# Register Wikipedia tools
register_wikipedia_tools(mcp)

# Constants
NWS_API_BASE = "https://librarian.mlziade.com.br"
USER_AGENT = "librarian-app/1.0"

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
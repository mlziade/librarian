from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("librarian")

# Constants
NWS_API_BASE = "https://librarian.mlziade.com.br"
USER_AGENT = "librarian-app/1.0"
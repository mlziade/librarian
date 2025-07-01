from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Import Wikipedia tools and resources
from tools.wikipedia_tools import register_wikipedia_tools
from resources.wikipedia_resources import register_wikipedia_resources
from resources.prompt_resources import register_prompt_resources

# Initialize FastMCP server
mcp = FastMCP("librarian")

# Register Wikipedia tools and resources
register_wikipedia_tools(mcp)
register_wikipedia_resources(mcp)
register_prompt_resources(mcp)

# Constants
NWS_API_BASE = "https://librarian.mlziade.com.br"
USER_AGENT = "librarian-app/1.0"

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
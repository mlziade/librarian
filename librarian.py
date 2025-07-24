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

if __name__ == "__main__":
    print("🚀 Starting Librarian MCP Server...")
    print("📚 Wikipedia tools and resources loaded")
    print("✅ Server is ready and listening for connections")
    
    # Run the MCP server using stdio transport (standard for MCP)
    mcp.run(transport='stdio')
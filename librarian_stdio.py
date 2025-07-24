#!/usr/bin/env python3
"""
STDIO wrapper for Librarian MCP Server

This script runs the Librarian MCP server in STDIO mode,
making it compatible with Claude Desktop and other local MCP clients.
"""

import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import and run the MCP server
from librarian import mcp

if __name__ == "__main__":
    print("🚀 Starting Librarian MCP Server (STDIO)...", file=sys.stderr)
    print("📚 Wikipedia tools and resources loaded", file=sys.stderr)
    print("✅ Server is ready and listening for connections", file=sys.stderr)
    
    # Run the MCP server using stdio transport
    mcp.run(transport='stdio')
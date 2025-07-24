"""
Remote MCP Server for Librarian

This module creates a server that can host the MCP server over HTTP/WebSocket/STDIO
for remote access while maintaining MCP protocol compliance.
"""

import asyncio
import json
import logging
import sys
import os
from typing import Any, Dict, Optional
from fastapi import FastAPI, WebSocket, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import the MCP server components
from librarian import mcp
from mcp.server.session import ServerSession
from mcp.server.stdio import stdio_server
from mcp.types import (
    JSONRPCMessage,
    JSONRPCRequest,
    JSONRPCResponse,
    JSONRPCError
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Librarian MCP Server",
    description="Remote MCP server for Wikipedia fact-checking and information retrieval",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with server information."""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Librarian MCP Server</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .header { color: #2c3e50; text-align: center; }
            .info { background: #e8f6f3; padding: 20px; border-radius: 5px; margin: 20px 0; }
            .tools { margin-top: 20px; }
            .tool { background: #e3f2fd; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #2196f3; }
            .tool-name { font-weight: bold; color: #1976d2; }
            .endpoint { background: #f8f9fa; padding: 15px; border-radius: 5px; font-family: monospace; margin: 10px 0; }
            .status { color: #27ae60; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="header">📚 Librarian MCP Server</h1>
            
            <div class="info">
                <p><strong>Status:</strong> <span class="status">Running</span></p>
                <p><strong>Description:</strong> Wikipedia fact-checking and information retrieval MCP server</p>
                <p><strong>Version:</strong> 1.0.0</p>
                <p><strong>Protocol:</strong> Model Context Protocol (MCP)</p>
            </div>
            
            <h2>Available Tools</h2>
            <div class="tools">
                <div class="tool">
                    <div class="tool-name">search_wikipedia_pages</div>
                    <div>Search Wikipedia articles and get top 5 results with selection information</div>
                </div>
                <div class="tool">
                    <div class="tool-name">get_wikipedia_page_info</div>
                    <div>Get comprehensive information about a specific Wikipedia page</div>
                </div>
                <div class="tool">
                    <div class="tool-name">get_wikipedia_page_summary</div>
                    <div>Get quick summaries of Wikipedia pages with customizable length</div>
                </div>
                <div class="tool">
                    <div class="tool-name">get_wikipedia_page_sections</div>
                    <div>List all sections in a Wikipedia page for navigation</div>
                </div>
                <div class="tool">
                    <div class="tool-name">get_wikipedia_page_sections_info</div>
                    <div>Get detailed content for specific sections of a Wikipedia page</div>
                </div>
            </div>
            
            <h2>Connection Information</h2>
            <div class="endpoint">
                <strong>MCP WebSocket Endpoint:</strong><br>
                wss://librarian.mlziade.com.br/mcp
            </div>
            <div class="endpoint">
                <strong>MCP HTTP+SSE Endpoint:</strong><br>
                https://librarian.mlziade.com.br/sse
            </div>
            
            <h2>Client Configuration</h2>
            <p>For Claude Desktop (local STDIO), add this to your MCP configuration:</p>
            <div class="endpoint">
{
  "mcpServers": {
    "librarian": {
      "command": "python",
      "args": ["/path/to/librarian_stdio.py"]
    }
  }
}
            </div>
            
            <p>For remote STDIO (if server supports it), use:</p>
            <div class="endpoint">
{
  "mcpServers": {
    "librarian": {
      "command": "python",
      "args": ["/path/to/librarian_server.py", "--stdio"]
    }
  }
}
            </div>
            
            <p>For HTTP+POST testing:</p>
            <div class="endpoint">
curl -X POST https://librarian.mlziade.com.br/mcp \\
  -H "Content-Type: application/json" \\
  -d '{"method":"initialize","params":{"protocol":"mcp"}}'
            </div>
        </div>
    </body>
    </html>
    """)


class MCPWebSocketSession:
    """Handles MCP protocol over WebSocket."""
    
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.session = ServerSession(mcp)
        self.closed = False
    
    async def handle_message(self, message: str) -> None:
        """Handle incoming MCP message."""
        try:
            # Parse JSON-RPC message
            data = json.loads(message)
            logger.info(f"Received MCP message: {data}")
            
            # Process through MCP session
            if isinstance(data, dict):
                # Handle the message through the MCP server session
                response = await self.session.handle_message(data)
                if response:
                    await self.websocket.send_text(json.dumps(response))
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                }
            }
            await self.websocket.send_text(json.dumps(error_response))
        
        except Exception as e:
            logger.error(f"Error handling MCP message: {e}")
            error_response = {
                "jsonrpc": "2.0",
                "id": data.get("id") if 'data' in locals() else None,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
            await self.websocket.send_text(json.dumps(error_response))

@app.websocket("/mcp")
async def mcp_websocket(websocket: WebSocket):
    """WebSocket endpoint for MCP protocol communication."""
    await websocket.accept()
    logger.info("MCP WebSocket connection established")
    
    session = MCPWebSocketSession(websocket)
    
    try:
        while True:
            message = await websocket.receive_text()
            await session.handle_message(message)
            
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        session.closed = True
        logger.info("MCP WebSocket connection closed")


class MCPHttpSession:
    """Handles MCP protocol over HTTP+SSE."""
    
    def __init__(self):
        self.session = ServerSession(mcp)
        self.message_queue = asyncio.Queue()
        self.closed = False
    
    async def handle_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle incoming MCP message and return response."""
        try:
            logger.info(f"Received HTTP MCP message: {message}")
            
            # Process through MCP session
            response = await self.session.handle_message(message)
            logger.info(f"Sending MCP response: {response}")
            return response
            
        except Exception as e:
            logger.error(f"Error handling MCP message: {e}")
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }


@app.post("/mcp")
async def mcp_http(request: Request):
    """HTTP endpoint for MCP protocol communication."""
    try:
        data = await request.json()
        session = MCPHttpSession()
        response = await session.handle_message(data)
        return response if response else {}
        
    except Exception as e:
        logger.error(f"HTTP MCP error: {e}")
        return {
            "jsonrpc": "2.0",
            "id": None,
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        }


async def sse_generator():
    """Generate Server-Sent Events for MCP communication."""
    session = MCPHttpSession()
    
    # Send initial connection event
    yield f"data: {json.dumps({'type': 'connected', 'message': 'MCP HTTP transport ready'})}\n\n"
    
    try:
        while not session.closed:
            # Keep connection alive
            yield f"data: {json.dumps({'type': 'ping', 'timestamp': asyncio.get_event_loop().time()})}\n\n"
            await asyncio.sleep(30)  # Send ping every 30 seconds
            
    except Exception as e:
        logger.error(f"SSE error: {e}")
        yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"


@app.get("/sse")
async def mcp_sse():
    """Server-Sent Events endpoint for MCP protocol communication."""
    return StreamingResponse(
        sse_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control"
        }
    )

# For running with uvicorn or stdio
if __name__ == "__main__":
    # Check if we should run in STDIO mode (for local MCP clients like Claude Desktop)
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        print("🚀 Starting Librarian MCP Server in STDIO mode...", file=sys.stderr)
        print("📚 Wikipedia tools and resources loaded", file=sys.stderr)
        print("✅ Server is ready and listening for connections", file=sys.stderr)
        
        # Run the MCP server using stdio transport
        mcp.run(transport='stdio')
    else:
        # Run as HTTP/WebSocket server
        uvicorn.run(
            "librarian_server:app",
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
"""
WSGI/ASGI adapter for Librarian MCP Server

This module creates a web server wrapper around the MCP server to enable
remote hosting via HTTP/WebSocket connections.
"""

import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
import os
from pathlib import Path

# Import the MCP server
from librarian import mcp

# Create FastAPI app
app = FastAPI(title="Librarian MCP Server", version="1.0.0")

# Add static files if they exist
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    """Root endpoint with basic information about the MCP server."""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Librarian MCP Server</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .header { color: #2c3e50; }
            .info { background: #f8f9fa; padding: 20px; border-radius: 5px; }
            .tools { margin-top: 20px; }
            .tool { background: #e3f2fd; padding: 10px; margin: 5px 0; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1 class="header">📚 Librarian MCP Server</h1>
        <div class="info">
            <p><strong>Status:</strong> Running</p>
            <p><strong>Description:</strong> Wikipedia fact-checking and information retrieval MCP server</p>
            <p><strong>Version:</strong> 1.0.0</p>
        </div>
        
        <div class="tools">
            <h2>Available Tools:</h2>
            <div class="tool"><strong>search_wikipedia_pages</strong> - Search Wikipedia articles</div>
            <div class="tool"><strong>get_wikipedia_page_info</strong> - Get detailed page information</div>
            <div class="tool"><strong>get_wikipedia_page_summary</strong> - Get quick page summaries</div>
            <div class="tool"><strong>get_wikipedia_page_sections</strong> - List page sections</div>
            <div class="tool"><strong>get_wikipedia_page_sections_info</strong> - Get specific section content</div>
        </div>
        
        <p style="margin-top: 30px; color: #666;">
            Connect via MCP client using WebSocket endpoint: <code>ws://librarian.mlziade.com.br/mcp</code>
        </p>
    </body>
    </html>
    """)

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "librarian-mcp"}

@app.websocket("/mcp")
async def mcp_websocket(websocket: WebSocket):
    """WebSocket endpoint for MCP protocol communication."""
    await websocket.accept()
    
    try:
        while True:
            # Receive message from client
            message = await websocket.receive_text()
            
            try:
                # Parse JSON message
                request = json.loads(message)
                
                # Process MCP request through the server
                # Note: This is a simplified implementation
                # In a full implementation, you'd need to handle the MCP protocol properly
                response = await process_mcp_request(request)
                
                # Send response back
                await websocket.send_text(json.dumps(response))
                
            except json.JSONDecodeError:
                error_response = {
                    "error": {"code": -32700, "message": "Parse error"}
                }
                await websocket.send_text(json.dumps(error_response))
                
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

async def process_mcp_request(request):
    """
    Process MCP protocol request.
    
    This is a simplified implementation. For a full MCP server,
    you would need to implement the complete MCP protocol specification.
    """
    try:
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        # Handle different MCP methods
        if method == "tools/list":
            # Return list of available tools
            tools = [
                {
                    "name": "search_wikipedia_pages",
                    "description": "Search for Wikipedia pages",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "language": {"type": "string", "default": "en"}
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "get_wikipedia_page_info",
                    "description": "Get detailed information about a Wikipedia page",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "page_title": {"type": "string"},
                            "language": {"type": "string", "default": "en"}
                        },
                        "required": ["page_title"]
                    }
                }
                # Add other tools as needed
            ]
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {"tools": tools}
            }
        
        elif method == "tools/call":
            # Handle tool calls
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            
            # This would need to be implemented to actually call the MCP tools
            # For now, return a placeholder response
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Tool {tool_name} called with args: {tool_args}"
                        }
                    ]
                }
            }
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }
            
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
        }

# For gunicorn ASGI compatibility
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
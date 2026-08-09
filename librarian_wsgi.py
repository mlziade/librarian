"""
WSGI/ASGI adapter for Librarian MCP Server

Intended for production deployment behind gunicorn/uvicorn with an ASGI worker.
The MCP SDK app is mounted at root so it receives the full request path (/mcp)
without prefix stripping, avoiding the 307 redirect issue that occurs when
mounting at /mcp in FastAPI.
"""

from fastapi import FastAPI
from librarian import mcp

app = FastAPI(title="Librarian MCP Server", version="0.1.0")


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "librarian-mcp", "mcp_spec": "2026-07-28"}


# Mount at root so the sub-app receives the full path (/mcp) intact
app.mount("/", mcp.streamable_http_app(stateless_http=True))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

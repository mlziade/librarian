# librarian

Librarian is a MCP (Model Context Protocol) Server that allows any LLM with a compatible MCP client to query Wikipedia for information. It can be configured to automatically fact-check information without requiring explicit user requests.

**Note:** While this guide focuses on Claude Desktop setup, Librarian also supports remote hosting via WebSocket/HTTP for broader accessibility.


> *"The only thing that you absolutely have to know is the location of the library."*
> 
> — Albert Einstein

<div align="center">

<img src="docs/Example1.png" alt="Claude Desktop Response" width="600">

*Example of Claude Desktop using the librarian MCP server to fact-check information*

</div>

## Features

- **Automatic Fact-Checking**: Configure Claude Desktop to proactively verify factual claims using Wikipedia
- **Wikipedia Search**: Search for relevant Wikipedia articles
- **Page Information**: Get detailed information about specific Wikipedia pages
- **Page Summaries**: Quick summaries of Wikipedia pages
- **Page Sections**: Get specific sections from Wikipedia pages
- **Multi-language Support**: Query Wikipedia in different languages

## Installation

### Claude Desktop Setup

#### 1. Prerequisites

- [Claude Desktop](https://claude.ai/download) installed on your computer
- [uv](https://docs.astral.sh/uv/) package manager installed
- Python 3.13 or higher

#### 2. Clone and Set Up the Project

```bash
git clone <your-repository-url>
cd librarian
uv sync
```

#### 3. Configure Claude Desktop

Add this configuration to your Claude Desktop configuration file:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

**For Windows:**
```json
{
    "mcpServers": {
        "librarian": {
            "command": "C:\\Users\\[USERNAME]\\.local\\bin\\uv.exe",
            "args": ["--directory", "C:\\Users\\[USERNAME]\\path\\to\\librarian", "run", "python", "librarian_stdio.py"],
            "env": {
                "PYTHONPATH": "C:\\Users\\[USERNAME]\\path\\to\\librarian"
            }
        }
    }
}
```

**For macOS/Linux:**
```json
{
    "mcpServers": {
        "librarian": {
            "command": "uv",
            "args": ["--directory", "/path/to/your/librarian", "run", "python", "librarian_stdio.py"],
            "env": {
                "PYTHONPATH": "/path/to/your/librarian"
            }
        }
    }
}
```

**Important**: 
- Replace `[USERNAME]` and `/path/to/your/librarian` with your actual paths
- The `--directory` flag ensures uv uses the correct project environment
- Use the full path to `uv.exe` on Windows for reliability

#### 4. Restart Claude Desktop

After adding the configuration, restart Claude Desktop completely to load the MCP server.

#### 5. Troubleshooting

If you encounter issues:

1. **Check Claude Desktop logs**: 
   - **Windows**: `%AppData%\Claude\logs\mcp-server-librarian.log`
   - **macOS**: `~/Library/Logs/Claude/mcp-server-librarian.log`

2. **Common issues**:
   - `ModuleNotFoundError`: Ensure you're using the `--directory` flag and correct paths
   - `File not found`: Use absolute paths for both `command` and in `args`
   - `Virtual environment warnings`: These are harmless but can be avoided with proper paths

3. **Test manually**:
   ```bash
   cd /path/to/librarian
   uv run python librarian_stdio.py
   # Should start without errors
   ```


## Automatic Fact-Checking Setup

To make Claude Desktop automatically use Wikipedia for fact-checking, start your conversations with:

```
"Use your Wikipedia tools to automatically fact-check any factual claims in our conversation. Don't wait for me to ask - proactively verify information and provide corrections when needed."
```

Or use the built-in system prompt by referencing: `fact_checking_instructions`

### Behavior Examples

Once configured, Claude Desktop will automatically:

- ✅ Verify historical dates and events
- ✅ Check biographical information  
- ✅ Confirm scientific facts and discoveries
- ✅ Validate geographical information
- ✅ Correct common misconceptions
- ✅ Provide source attribution from Wikipedia

## Available Tools

1. **search_wikipedia_pages**: Search for Wikipedia articles on any topic and return the top 5 results with selection information
2. **get_wikipedia_page_info**: Get comprehensive information about a specific page including content, summary, hyperlinked words, and categories
3. **get_wikipedia_page_summary**: Get quick summaries of Wikipedia pages with customizable sentence length
4. **get_wikipedia_page_sections**: Get a list of all sections on a Wikipedia page for large pages where you need specific information
5. **get_wikipedia_page_sections_info**: Get detailed content for specific sections of a Wikipedia page by title or index

All tools support multi-language Wikipedia queries by specifying the language parameter (default: "en").

## Examples

### Available Tools in Claude Desktop
<img src="docs/Example2.png" alt="Tools Available" width="600">

*Screenshot showing the Wikipedia tools available in Claude Desktop when the MCP server is properly configured*

### MCP Servers Configuration
<img src="docs/Example3.png" alt="MCP Servers" width="600">

*Claude Desktop showing the librarian MCP server successfully connected and available*

### VS Code Integration Example
<img src="docs/Example4.png" alt="VS Code Response" width="600">

*Example of using the librarian tools within VS Code with GitHub Copilot*

## License

This project is open source. Please check the license file for details.
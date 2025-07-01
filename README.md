# librarian

Librarian is a MCP Server that allows any LLM with a compatible MCP client to query for information on Wikipedia. Tt can be configured to automatically fact-check information without requiring explicit user requests.

> *"The only thing that you absolutely have to know is the location of the library."*
> 
> — Albert Einstein

## Features

- **Automatic Fact-Checking**: Configure Claude to proactively verify factual claims using Wikipedia
- **Wikipedia Search**: Search for relevant Wikipedia articles
- **Page Information**: Get detailed information about specific Wikipedia pages
- **Page Summaries**: Quick summaries of Wikipedia pages
- **Page Existence Check**: Verify if a Wikipedia page exists before querying

## Automatic Fact-Checking Setup

To enable automatic fact-checking behavior in Claude Desktop:

### 1. Configure Claude Desktop

Add this to your Claude Desktop configuration file (`%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
    "mcpServers": {
        "librarian": {
            "command": "uv",
            "args": ["run", "python", "librarian.py"],
            "cwd": "C:\\Users\\YourUsername\\Documents\\librarian",
            "env": {
                "PYTHONPATH": "C:\\Users\\YourUsername\\Documents\\librarian"
            }
        }
    }
}
```

### 2. Enable Automatic Behavior

To make Claude automatically use Wikipedia for fact-checking, start your conversations with:

```
"Use your Wikipedia tools to automatically fact-check any factual claims in our conversation. Don't wait for me to ask - proactively verify information and provide corrections when needed."
```

Or use the built-in system prompt by referencing: `fact_checking_instructions`

### 3. Behavior Examples

Once configured, Claude will automatically:

- ✅ Verify historical dates and events
- ✅ Check biographical information  
- ✅ Confirm scientific facts and discoveries
- ✅ Validate geographical information
- ✅ Correct common misconceptions
- ✅ Provide source attribution from Wikipedia

## Available Tools

1. **search_wikipedia_pages**: Search for Wikipedia articles on any topic
2. **get_wikipedia_page_info**: Get comprehensive information about a specific page
3. **get_wikipedia_page_summary**: Get quick summaries of Wikipedia pages  
4. **check_wikipedia_page_exists**: Verify if a page exists before querying
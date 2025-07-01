"""
Wikipedia Tools for MCP Server

This module provides MCP tools for querying Wikipedia pages, including search
functionality and detailed page information retrieval.
"""

import sys
import os

# Add the parent directory to the path to import our Wikipedia API
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wiki.api import WikipediaAPI
from mcp.types import Tool


def register_wikipedia_tools(mcp_server):
    """Register Wikipedia tools with the MCP server."""
    
    @mcp_server.tool(
        name="search_wikipedia_pages",
        description="Search for Wikipedia pages on a certain word/topic and return the first 5 results with information to help choose the most relevant one"
    )
    def search_wikipedia_pages(
        query: str,
        language: str = "en"
    ) -> dict[str, object]:
        """
        Search for Wikipedia pages and return the top 5 results with selection information.
        
        Args:
            query: The search term or phrase
            language: Wikipedia language code (default: "en")
            
        Returns:
            Dict containing search results with titles, snippets, URLs, and metadata
        """
        try:
            with WikipediaAPI(language=language) as api:
                # Search for pages
                search_results = api.search(query, limit=5)
                
                if not search_results:
                    return {
                        "success": False,
                        "message": f"No results found for query: '{query}'",
                        "results": []
                    }
                
                # Format results with additional information
                formatted_results = []
                for result in search_results:
                    title = result.get('title', '')
                    snippet = result.get('snippet', '').replace('<span class="searchmatch">', '').replace('</span>', '')
                    word_count = result.get('wordcount', 0)
                    size = result.get('size', 0)
                    timestamp = result.get('timestamp', '')
                    
                    # Construct Wikipedia URL
                    safe_title = title.replace(' ', '_')
                    url = f"https://{language}.wikipedia.org/wiki/{safe_title}"
                    
                    formatted_results.append({
                        "title": title,
                        "snippet": snippet,
                        "url": url,
                        "word_count": word_count,
                        "last_modified": timestamp
                    })
                
                return {
                    "success": True,
                    "query": query,
                    "language": language,
                    "total_results": len(formatted_results),
                    "results": formatted_results
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Error searching Wikipedia for '{query}': {str(e)}"
            }
    
    @mcp_server.tool(
        name="get_wikipedia_page_info",
        description="Get detailed information about a specific Wikipedia page including content, summary, and hyperlinked words"
    )
    def get_wikipedia_page_info(
        page_title: str,
        language: str = "en",
        include_full_content: bool = False,
        include_categories: bool = False,
        include_page_info: bool = False
    ) -> dict[str, object]:
        """
        Get comprehensive information about a Wikipedia page.
        
        Args:
            page_title: The title of the Wikipedia page
            language: Wikipedia language code (default: "en")
            include_full_content: Whether to include full wikitext content (default: False)
            include_categories: Whether to include page categories (default: False)
            include_page_info: Whether to include detailed page metadata (default: False)
            
        Returns:
            Dict containing page summary, extract, links, and optionally full content, categories, and page info
        """
        try:
            with WikipediaAPI(language=language) as api:
                # Check if page exists first
                if not api.page_exists(page_title):
                    return {
                        "success": False,
                        "message": f"Page '{page_title}' does not exist on {language}.wikipedia.org",
                        "suggestions": "Try checking the spelling or using the search tool first"
                    }
                
                # Get page information
                page_info = api.get_page_info(page_title) if include_page_info else None
                summary = api.get_page_summary(page_title)
                extract = api.get_page_extract(page_title, sentences=5)
                links = api.get_page_links(page_title, limit=50)
                categories = api.get_page_categories(page_title) if include_categories else None
                
                # Construct the response
                result = {
                    "success": True,
                    "page_title": page_title,
                    "language": language,
                    "url": f"https://{language}.wikipedia.org/wiki/{page_title.replace(' ', '_')}",
                    "summary": {
                        "extract": summary.get('extract', '') if summary else '',
                        "description": summary.get('description', '') if summary else '',
                        "type": summary.get('type', '') if summary else ''
                    },
                    "content_extract": extract or "No extract available",
                    "hyperlinked_words": links or []
                }
                
                # Optionally include categories
                if include_categories:
                    result["categories"] = categories or []
                
                # Optionally include page info
                if include_page_info:
                    result["page_info"] = {
                        "length": page_info.get('length', 0) if page_info else 0,
                        "last_modified": page_info.get('touched', '') if page_info else '',
                        "page_id": page_info.get('pageid', '') if page_info else '',
                        "canonical_url": page_info.get('canonicalurl', '') if page_info else ''
                    }
                
                # Optionally include full content
                if include_full_content:
                    full_content = api.get_page_content(page_title)
                    result["full_content"] = full_content or "Full content not available"
                
                return result
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Error retrieving information for page '{page_title}': {str(e)}"
            }
    
    @mcp_server.tool(
        name="get_wikipedia_page_summary",
        description="Get a quick summary of a Wikipedia page - lighter version of get_wikipedia_page_info"
    )
    def get_wikipedia_page_summary(
        page_title: str,
        language: str = "en",
        sentences: int = 3
    ) -> dict[str, object]:
        """
        Get a quick summary of a Wikipedia page.
        
        Args:
            page_title: The title of the Wikipedia page
            language: Wikipedia language code (default: "en")
            sentences: Number of sentences to include in extract (default: 3)
            
        Returns:
            Dict containing page summary and basic information
        """
        try:
            with WikipediaAPI(language=language) as api:
                # Check if page exists
                if not api.page_exists(page_title):
                    return {
                        "success": False,
                        "message": f"Page '{page_title}' does not exist"
                    }
                
                # Get basic information
                summary = api.get_page_summary(page_title)
                extract = api.get_page_extract(page_title, sentences=sentences)
                
                return {
                    "success": True,
                    "page_title": page_title,
                    "language": language,
                    "url": f"https://{language}.wikipedia.org/wiki/{page_title.replace(' ', '_')}",
                    "summary": summary.get('extract', '') if summary else '',
                    "extract": extract or "No extract available",
                    "description": summary.get('description', '') if summary else ''
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Error getting summary for '{page_title}': {str(e)}"
            }
    
    @mcp_server.tool(
        name="check_wikipedia_page_exists",
        description="Check if a Wikipedia page exists before trying to retrieve it"
    )
    def check_wikipedia_page_exists(
        page_title: str,
        language: str = "en"
    ) -> dict[str, object]:
        """
        Check if a Wikipedia page exists.
        
        Args:
            page_title: The title of the Wikipedia page to check
            language: Wikipedia language code (default: "en")
            
        Returns:
            Dict indicating whether the page exists
        """
        try:
            with WikipediaAPI(language=language) as api:
                exists = api.page_exists(page_title)
                
                result = {
                    "success": True,
                    "page_title": page_title,
                    "language": language,
                    "exists": exists
                }
                
                if exists:
                    result["url"] = f"https://{language}.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
                    result["message"] = f"Page '{page_title}' exists"
                else:
                    result["message"] = f"Page '{page_title}' does not exist"
                
                return result
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Error checking if page '{page_title}' exists: {str(e)}"
            }


# Tool descriptions for MCP registration
WIKIPEDIA_TOOLS = [
    {
        "name": "search_wikipedia_pages",
        "description": "Search for Wikipedia pages on a certain word/topic and return the first 5 results with information to help choose the most relevant one",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search term or phrase"
                },
                "language": {
                    "type": "string",
                    "description": "Wikipedia language code (default: 'en')",
                    "default": "en"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_wikipedia_page_info",
        "description": "Get detailed information about a specific Wikipedia page including content, summary, and hyperlinked words",
        "inputSchema": {
            "type": "object",
            "properties": {
                "page_title": {
                    "type": "string",
                    "description": "The title of the Wikipedia page"
                },
                "language": {
                    "type": "string",
                    "description": "Wikipedia language code (default: 'en')",
                    "default": "en"
                },
                "include_full_content": {
                    "type": "boolean",
                    "description": "Whether to include full wikitext content (default: false). Only use if you specifically need the raw wiki markup.",
                    "default": False
                },
                "include_categories": {
                    "type": "boolean",
                    "description": "Whether to include page categories (default: false). Only use if you specifically need category information for classification or organization purposes.",
                    "default": False
                },
                "include_page_info": {
                    "type": "boolean",
                    "description": "Whether to include detailed page metadata like length, last modified date, and page ID (default: false). Only use if you specifically need technical page details.",
                    "default": False
                }
            },
            "required": ["page_title"]
        }
    },
    {
        "name": "get_wikipedia_page_summary",
        "description": "Get a quick summary of a Wikipedia page - lighter version of get_wikipedia_page_info",
        "inputSchema": {
            "type": "object",
            "properties": {
                "page_title": {
                    "type": "string",
                    "description": "The title of the Wikipedia page"
                },
                "language": {
                    "type": "string",
                    "description": "Wikipedia language code (default: 'en')",
                    "default": "en"
                },
                "sentences": {
                    "type": "integer",
                    "description": "Number of sentences to include in extract (default: 3)",
                    "default": 3
                }
            },
            "required": ["page_title"]
        }
    },
    {
        "name": "check_wikipedia_page_exists",
        "description": "Check if a Wikipedia page exists before trying to retrieve it",
        "inputSchema": {
            "type": "object",
            "properties": {
                "page_title": {
                    "type": "string",
                    "description": "The title of the Wikipedia page to check"
                },
                "language": {
                    "type": "string",
                    "description": "Wikipedia language code (default: 'en')",
                    "default": "en"
                }
            },
            "required": ["page_title"]
        }
    }
]

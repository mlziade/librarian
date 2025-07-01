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
            Dict containing:
            - success: Boolean indicating if the search was successful
            - query: The original search query
            - language: Language code used
            - total_results: Number of results returned
            - results: List of dictionaries, each containing:
                - title: Page title
                - snippet: Brief excerpt with search terms highlighted
                - url: Direct link to the Wikipedia page
                - word_count: Number of words in the page
                - last_modified: Timestamp of last modification
            Or if unsuccessful:
            - success: False
            - error: Error details
            - message: Human-readable error message
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
            Dict containing:
            - success: Boolean indicating if the request was successful
            - page_title: The requested page title
            - language: Language code used
            - url: Direct link to the Wikipedia page
            - summary: Brief summary text from page summary
            - extract: Content extract with specified number of sentences
            - description: Short page description
            Or if unsuccessful:
            - success: False
            - error: Error details
            - message: Human-readable error message
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
                
                if not summary:
                    return {
                        "success": False,
                        "message": f"Could not retrieve summary for page '{page_title}'"
                    }
                
                # Extract the content and limit to requested sentences
                extract = summary.get('extract', '')
                if extract and sentences > 0:
                    # Simple sentence splitting - split by periods and take first N sentences
                    sentences_list = [s.strip() + '.' for s in extract.split('.') if s.strip()]
                    if len(sentences_list) > sentences:
                        extract = ' '.join(sentences_list[:sentences])
                
                return {
                    "success": True,
                    "page_title": page_title,
                    "language": language,
                    "url": f"https://{language}.wikipedia.org/wiki/{page_title.replace(' ', '_')}",
                    "summary": summary.get('extract', ''),
                    "extract": extract,
                    "description": summary.get('description', '')
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Error getting summary for '{page_title}': {str(e)}"
            }
    
    @mcp_server.tool(
        name="get_wikipedia_page_sections",
        description="Get a list of the sections on a Wikipedia Page. Its useful for when a page on wikipedia is too large and the LLM can query for the available sections to it to get only necessary information"
    )
    def get_wikipedia_page_sections(
        page_title: str,
        language: str = "en"
    ) -> dict[str, object]:
        """
        Get a list of sections from a Wikipedia page.
        
        Args:
            page_title: The title of the Wikipedia page
            language: Wikipedia language code (default: "en")
            
        Returns:
            Dict containing:
            - success: Boolean indicating if the request was successful
            - page_title: The requested page title
            - language: Language code used
            - url: Direct link to the Wikipedia page
            - sections: List of dictionaries, each containing:
                - index: Section index
                - title: Section title
                - level: Section level (1, 2, 3, etc.)
                - anchor: Section anchor for direct linking
                - number: Section number
            Or if unsuccessful:
            - success: False
            - error: Error details
            - message: Human-readable error message
        """
        try:
            with WikipediaAPI(language=language) as api:
                # Check if page exists
                if not api.page_exists(page_title):
                    return {
                        "success": False,
                        "message": f"Page '{page_title}' does not exist"
                    }
                
                # Get page sections
                sections = api.get_page_sections(page_title)
                
                return {
                    "success": True,
                    "page_title": page_title,
                    "language": language,
                    "url": f"https://{language}.wikipedia.org/wiki/{page_title.replace(' ', '_')}",
                    "sections": sections
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Error getting sections for '{page_title}': {str(e)}"
            }
    
    @mcp_server.tool(
        name="get_wikipedia_page_sections_info",
        description="Get detailed sections information about a specific Wikipedia page"
    )
    def get_wikipedia_page_sections_info(
        page_title: str,
        section_titles: list[str] = None,
        section_indices: list[str] = None,
        language: str = "en"
    ) -> dict[str, object]:
        """
        Get detailed content for specific sections of a Wikipedia page.
        
        Args:
            page_title: The title of the Wikipedia page
            section_titles: List of section titles to retrieve (optional)
            section_indices: List of section indices to retrieve (optional)
            language: Wikipedia language code (default: "en")
            
        Returns:
            Dict containing:
            - success: Boolean indicating if the request was successful
            - page_title: The requested page title
            - language: Language code used
            - url: Direct link to the Wikipedia page
            - sections_content: Dictionary mapping section identifiers to their content
            Or if unsuccessful:
            - success: False
            - error: Error details
            - message: Human-readable error message
        """
        try:
            with WikipediaAPI(language=language) as api:
                # Check if page exists
                if not api.page_exists(page_title):
                    return {
                        "success": False,
                        "message": f"Page '{page_title}' does not exist"
                    }
                
                sections_content = {}
                
                # Get content by section titles if provided
                if section_titles:
                    sections_content.update(api.get_page_sections_content_by_title(page_title, section_titles))
                
                # Get content by section indices if provided
                if section_indices:
                    content_by_index = api.get_page_sections_content(page_title, section_indices)
                    sections_content.update(content_by_index)
                
                # If neither titles nor indices provided, get all sections
                if not section_titles and not section_indices:
                    all_sections = api.get_page_sections(page_title)
                    if all_sections:
                        indices = [section['index'] for section in all_sections if section.get('index')]
                        sections_content = api.get_page_sections_content(page_title, indices)
                
                return {
                    "success": True,
                    "page_title": page_title,
                    "language": language,
                    "url": f"https://{language}.wikipedia.org/wiki/{page_title.replace(' ', '_')}",
                    "sections_content": sections_content
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Error getting section content for '{page_title}': {str(e)}"
            }
    
    
    @mcp_server.tool(
        name="get_wikipedia_page_info",
        description="Get detailed information about a specific Wikipedia page including content, summary, and hyperlinked words"
    )
    def get_wikipedia_page_info(
        page_title: str,
        language: str = "en",
        include_full_content: bool = False
    ) -> dict[str, object]:
        """
        Get comprehensive information about a Wikipedia page.
        
        Args:
            page_title: The title of the Wikipedia page
            language: Wikipedia language code (default: "en")
            include_full_content: Whether to include full wikitext content (default: False)
            
        Returns:
            Dict containing:
            - success: Boolean indicating if the request was successful
            - page_title: The requested page title
            - language: Language code used
            - url: Direct link to the Wikipedia page
            - summary: Dictionary with:
                - extract: Brief summary text
                - description: Short description
                - type: Page type (e.g., "standard", "disambiguation")
            - hyperlinked_words: List of linked page titles from the page
            - categories: List of page categories
            - page_info: Dictionary with technical details:
                - length: Page length in bytes
                - last_modified: Last modification timestamp
                - page_id: Unique page identifier
                - canonical_url: Canonical URL
            - full_content: Complete wikitext content (if include_full_content=True)
            Or if unsuccessful:
            - success: False
            - error: Error details
            - message: Human-readable error message
            - suggestions: Helpful suggestions for troubleshooting
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
                page_info = api.get_page_info(page_title)
                summary = api.get_page_summary(page_title)
                links = api.get_page_links(page_title, limit=50)
                categories = api.get_page_categories(page_title)
                
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
                    "hyperlinked_words": links or [],
                    "categories": categories or [],
                    "page_info": {
                        "length": page_info.get('length', 0) if page_info else 0,
                        "last_modified": page_info.get('touched', '') if page_info else '',
                        "page_id": page_info.get('pageid', '') if page_info else '',
                        "canonical_url": page_info.get('canonicalurl', '') if page_info else ''
                    }
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
        "name": "get_wikipedia_page_sections",
        "description": "Get a list of the sections on a Wikipedia Page. Its useful for when a page on wikipedia is too large and the LLM can query for the available sections to it to get only necessary information",
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
                }
            },
            "required": ["page_title"]
        }
    },
    {
        "name": "get_wikipedia_page_sections_info",
        "description": "Get detailed sections information about a specific Wikipedia page",
        "inputSchema": {
            "type": "object",
            "properties": {
                "page_title": {
                    "type": "string",
                    "description": "The title of the Wikipedia page"
                },
                "section_titles": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "List of section titles to retrieve content for (optional)"
                },
                "section_indices": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "List of section indices to retrieve content for (optional)"
                },
                "language": {
                    "type": "string",
                    "description": "Wikipedia language code (default: 'en')",
                    "default": "en"
                }
            },
            "required": ["page_title"]
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
                }
            },
            "required": ["page_title"]
        }
    }
]

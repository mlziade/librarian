"""
Wikipedia Resources for MCP Server

This module provides MCP resources for Wikipedia content, including templates,
schemas, and static information about Wikipedia's structure and capabilities.
"""

from typing import Any, Dict, List
import json


def register_wikipedia_resources(mcp_server):
    """Register Wikipedia resources with the MCP server."""
    
    @mcp_server.resource(
        uri="wikipedia://schema/search-result",
        name="Wikipedia Search Result Schema",
        description="JSON schema for Wikipedia search results returned by search_wikipedia_pages tool"
    )
    def wikipedia_search_schema() -> str:
        """Return the JSON schema for Wikipedia search results."""
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Wikipedia Search Result",
            "description": "Schema for Wikipedia search results",
            "properties": {
                "success": {
                    "type": "boolean",
                    "description": "Whether the search was successful"
                },
                "query": {
                    "type": "string",
                    "description": "The original search query"
                },
                "language": {
                    "type": "string",
                    "description": "Wikipedia language code used"
                },
                "total_results": {
                    "type": "integer",
                    "description": "Number of results returned"
                },
                "results": {
                    "type": "array",
                    "description": "Array of search results",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Page title"
                            },
                            "snippet": {
                                "type": "string",
                                "description": "Text snippet from the page"
                            },
                            "url": {
                                "type": "string",
                                "format": "uri",
                                "description": "Direct URL to the Wikipedia page"
                            },
                            "word_count": {
                                "type": "integer",
                                "description": "Number of words in the page"
                            },
                            "last_modified": {
                                "type": "string",
                                "description": "Last modification timestamp"
                            }
                        },
                        "required": ["title", "snippet", "url"]
                    }
                }
            },
            "required": ["success"]
        }
        return json.dumps(schema, indent=2)
    
    @mcp_server.resource(
        uri="wikipedia://schema/page-info",
        name="Wikipedia Page Info Schema",
        description="JSON schema for Wikipedia page information returned by get_wikipedia_page_info tool"
    )
    def wikipedia_page_info_schema() -> str:
        """Return the JSON schema for Wikipedia page information."""
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Wikipedia Page Information",
            "description": "Schema for detailed Wikipedia page information",
            "properties": {
                "success": {
                    "type": "boolean",
                    "description": "Whether the request was successful"
                },
                "page_title": {
                    "type": "string",
                    "description": "The title of the Wikipedia page"
                },
                "language": {
                    "type": "string",
                    "description": "Wikipedia language code"
                },
                "url": {
                    "type": "string",
                    "format": "uri",
                    "description": "Direct URL to the Wikipedia page"
                },
                "summary": {
                    "type": "object",
                    "description": "Page summary information",
                    "properties": {
                        "extract": {
                            "type": "string",
                            "description": "Summary extract from the page"
                        },
                        "description": {
                            "type": "string",
                            "description": "Brief description of the page"
                        },
                        "type": {
                            "type": "string",
                            "description": "Type of the page (e.g., 'standard')"
                        }
                    }
                },
                "content_extract": {
                    "type": "string",
                    "description": "Plain text extract from the page content"
                },
                "hyperlinked_words": {
                    "type": "array",
                    "description": "List of words/phrases that are hyperlinked in the page",
                    "items": {
                        "type": "string"
                    }
                },
                "categories": {
                    "type": "array",
                    "description": "Categories the page belongs to",
                    "items": {
                        "type": "string"
                    }
                },
                "page_info": {
                    "type": "object",
                    "description": "Technical page information",
                    "properties": {
                        "length": {
                            "type": "integer",
                            "description": "Page length in characters"
                        },
                        "last_modified": {
                            "type": "string",
                            "description": "Last modification timestamp"
                        },
                        "page_id": {
                            "type": "string",
                            "description": "Internal Wikipedia page ID"
                        },
                        "canonical_url": {
                            "type": "string",
                            "format": "uri",
                            "description": "Canonical URL of the page"
                        }
                    }
                },
                "full_content": {
                    "type": "string",
                    "description": "Full wikitext content (optional, if requested)"
                }
            },
            "required": ["success", "page_title"]
        }
        return json.dumps(schema, indent=2)
    
    @mcp_server.resource(
        uri="wikipedia://languages",
        name="Wikipedia Language Codes",
        description="List of supported Wikipedia language codes and their names"
    )
    def wikipedia_languages() -> str:
        """Return a list of supported Wikipedia language codes."""
        languages = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "ja": "Japanese",
            "zh": "Chinese",
            "ko": "Korean",
            "ar": "Arabic",
            "hi": "Hindi",
            "tr": "Turkish",
            "pl": "Polish",
            "nl": "Dutch",
            "sv": "Swedish",
            "da": "Danish",
            "no": "Norwegian",
            "fi": "Finnish",
            "he": "Hebrew",
            "th": "Thai",
            "vi": "Vietnamese",
            "uk": "Ukrainian",
            "cs": "Czech",
            "hu": "Hungarian",
            "ro": "Romanian",
            "el": "Greek",
            "bg": "Bulgarian",
            "hr": "Croatian",
            "sk": "Slovak",
            "sl": "Slovenian",
            "et": "Estonian",
            "lv": "Latvian",
            "lt": "Lithuanian",
            "mt": "Maltese",
            "ga": "Irish",
            "cy": "Welsh",
            "eu": "Basque",
            "ca": "Catalan",
            "gl": "Galician",
            "is": "Icelandic",
            "fo": "Faroese",
            "sq": "Albanian",
            "mk": "Macedonian",
            "sr": "Serbian",
            "bs": "Bosnian",
            "me": "Montenegrin",
            "id": "Indonesian",
            "ms": "Malay",
            "tl": "Filipino",
            "bn": "Bengali",
            "ta": "Tamil",
            "te": "Telugu",
            "ml": "Malayalam",
            "kn": "Kannada",
            "gu": "Gujarati",
            "pa": "Punjabi",
            "ur": "Urdu",
            "fa": "Persian",
            "sw": "Swahili",
            "yo": "Yoruba",
            "ig": "Igbo",
            "ha": "Hausa",
            "am": "Amharic",
            "so": "Somali",
            "mg": "Malagasy",
            "ny": "Chichewa"
        }
        return json.dumps(languages, indent=2)
    
    @mcp_server.resource(
        uri="wikipedia://api-endpoints",
        name="Wikipedia API Endpoints",
        description="Documentation of Wikipedia API endpoints used by the tools"
    )
    def wikipedia_api_endpoints() -> str:
        """Return documentation of Wikipedia API endpoints."""
        endpoints = {
            "search_api": {
                "url": "https://{lang}.wikipedia.org/w/api.php",
                "method": "GET",
                "description": "MediaWiki API for searching articles",
                "parameters": {
                    "action": "query",
                    "format": "json",
                    "list": "search",
                    "srsearch": "Search query",
                    "srlimit": "Number of results (max 500)",
                    "srprop": "Properties to return (snippet, titlesnippet, size, wordcount, timestamp)"
                },
                "example": "https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch=python&srlimit=5"
            },
            "rest_api_summary": {
                "url": "https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title}",
                "method": "GET",
                "description": "REST API for getting page summaries",
                "parameters": {
                    "title": "Page title (URL encoded)"
                },
                "example": "https://en.wikipedia.org/api/rest_v1/page/summary/Python_(programming_language)"
            },
            "content_api": {
                "url": "https://{lang}.wikipedia.org/w/api.php",
                "method": "GET",
                "description": "MediaWiki API for getting full page content",
                "parameters": {
                    "action": "query",
                    "format": "json",
                    "titles": "Page title",
                    "prop": "revisions",
                    "rvprop": "content",
                    "rvslots": "main"
                },
                "example": "https://en.wikipedia.org/w/api.php?action=query&format=json&titles=Python&prop=revisions&rvprop=content"
            },
            "extract_api": {
                "url": "https://{lang}.wikipedia.org/w/api.php",
                "method": "GET",
                "description": "MediaWiki API for getting plain text extracts",
                "parameters": {
                    "action": "query",
                    "format": "json",
                    "titles": "Page title",
                    "prop": "extracts",
                    "exsentences": "Number of sentences",
                    "explaintext": "true",
                    "exsectionformat": "plain"
                },
                "example": "https://en.wikipedia.org/w/api.php?action=query&format=json&titles=Python&prop=extracts&exsentences=3&explaintext=true"
            }
        }
        return json.dumps(endpoints, indent=2)
    
    @mcp_server.resource(
        uri="wikipedia://usage-examples",
        name="Wikipedia Tools Usage Examples",
        description="Examples of how to use the Wikipedia tools effectively"
    )
    def wikipedia_usage_examples() -> str:
        """Return usage examples for the Wikipedia tools."""
        examples = {
            "search_examples": {
                "basic_search": {
                    "tool": "search_wikipedia_pages",
                    "input": {
                        "query": "artificial intelligence"
                    },
                    "description": "Search for pages about artificial intelligence",
                    "use_case": "When you need to find relevant Wikipedia pages on a topic"
                },
                "multilingual_search": {
                    "tool": "search_wikipedia_pages",
                    "input": {
                        "query": "inteligencia artificial",
                        "language": "es"
                    },
                    "description": "Search for AI pages in Spanish Wikipedia",
                    "use_case": "When working with non-English content"
                },
                "specific_search": {
                    "tool": "search_wikipedia_pages",
                    "input": {
                        "query": "machine learning algorithms"
                    },
                    "description": "Search for specific algorithmic topics",
                    "use_case": "When looking for technical or specialized content"
                }
            },
            "page_info_examples": {
                "basic_info": {
                    "tool": "get_wikipedia_page_info",
                    "input": {
                        "page_title": "Machine learning"
                    },
                    "description": "Get comprehensive information about machine learning",
                    "use_case": "When you need detailed information about a specific topic"
                },
                "with_content": {
                    "tool": "get_wikipedia_page_info",
                    "input": {
                        "page_title": "Python (programming language)",
                        "include_full_content": True
                    },
                    "description": "Get full page content including wikitext",
                    "use_case": "When you need the complete article content for analysis"
                },
                "multilingual_info": {
                    "tool": "get_wikipedia_page_info",
                    "input": {
                        "page_title": "Apprentissage automatique",
                        "language": "fr"
                    },
                    "description": "Get information from French Wikipedia",
                    "use_case": "When working with international sources"
                }
            },
            "workflow_examples": {
                "research_workflow": {
                    "steps": [
                        {
                            "step": 1,
                            "action": "search_wikipedia_pages",
                            "input": {"query": "quantum computing"},
                            "purpose": "Find relevant pages on the topic"
                        },
                        {
                            "step": 2,
                            "action": "get_wikipedia_page_info",
                            "input": {"page_title": "Quantum computing"},
                            "purpose": "Get detailed information about the main topic"
                        },
                        {
                            "step": 3,
                            "action": "get_wikipedia_page_info",
                            "input": {"page_title": "Quantum algorithm"},
                            "purpose": "Explore related topics from hyperlinks"
                        }
                    ],
                    "description": "Research workflow for exploring a new topic systematically"
                },
                "fact_checking": {
                    "steps": [
                        {
                            "step": 1,
                            "action": "check_wikipedia_page_exists",
                            "input": {"page_title": "Specific claim or topic"},
                            "purpose": "Verify the topic has a Wikipedia page"
                        },
                        {
                            "step": 2,
                            "action": "get_wikipedia_page_summary",
                            "input": {"page_title": "Specific claim or topic"},
                            "purpose": "Get quick verification of basic facts"
                        }
                    ],
                    "description": "Quick fact-checking workflow"
                }
            }
        }
        return json.dumps(examples, indent=2)
    
    @mcp_server.resource(
        uri="wikipedia://best-practices",
        name="Wikipedia Tools Best Practices",
        description="Guidelines and best practices for using Wikipedia tools effectively"
    )
    def wikipedia_best_practices() -> str:
        """Return best practices for using Wikipedia tools."""
        practices = {
            "search_best_practices": {
                "query_formulation": [
                    "Use specific, descriptive terms rather than single words",
                    "Include key context words (e.g., 'programming language' not just 'Python')",
                    "Try different phrasings if initial results aren't relevant",
                    "Use quotes for exact phrases when needed"
                ],
                "result_selection": [
                    "Check word count - higher counts often indicate more comprehensive articles",
                    "Read snippets carefully to assess relevance",
                    "Consider the page title for specificity",
                    "Look for disambiguation pages if multiple topics share a name"
                ],
                "language_considerations": [
                    "Start with English (en) for broadest content",
                    "Use native language codes for region-specific information",
                    "Be aware that article quality varies across languages",
                    "Some topics may be better covered in specific languages"
                ]
            },
            "page_retrieval_best_practices": {
                "title_formatting": [
                    "Use exact titles from search results when possible",
                    "Maintain proper capitalization and spacing",
                    "Include disambiguation text in parentheses if needed",
                    "Check page existence first for uncertain titles"
                ],
                "content_usage": [
                    "Use summary for quick overviews",
                    "Use extract for readable introductions",
                    "Use hyperlinked words to discover related topics",
                    "Use categories to understand topic classification"
                ],
                "performance_optimization": [
                    "Start with summaries before requesting full content",
                    "Cache frequently accessed pages",
                    "Use the existence check to avoid failed requests",
                    "Limit hyperlink retrieval to reasonable numbers"
                ]
            },
            "error_handling": [
                "Always check the 'success' field in responses",
                "Handle 'page does not exist' gracefully",
                "Implement retry logic for network failures",
                "Provide meaningful error messages to users"
            ],
            "ethical_usage": [
                "Respect Wikipedia's terms of service",
                "Don't make excessive rapid requests",
                "Attribute Wikipedia as the source when using content",
                "Be aware of Wikipedia's NPOV (Neutral Point of View) policy"
            ]
        }
        return json.dumps(practices, indent=2)


# Resource metadata for registration
WIKIPEDIA_RESOURCES = [
    {
        "uri": "wikipedia://schema/search-result",
        "name": "Wikipedia Search Result Schema",
        "description": "JSON schema for Wikipedia search results",
        "mimeType": "application/json"
    },
    {
        "uri": "wikipedia://schema/page-info",
        "name": "Wikipedia Page Info Schema", 
        "description": "JSON schema for Wikipedia page information",
        "mimeType": "application/json"
    },
    {
        "uri": "wikipedia://languages",
        "name": "Wikipedia Language Codes",
        "description": "Supported Wikipedia language codes",
        "mimeType": "application/json"
    },
    {
        "uri": "wikipedia://api-endpoints",
        "name": "Wikipedia API Endpoints",
        "description": "Documentation of Wikipedia API endpoints",
        "mimeType": "application/json"
    },
    {
        "uri": "wikipedia://usage-examples",
        "name": "Wikipedia Tools Usage Examples",
        "description": "Examples of effective tool usage",
        "mimeType": "application/json"
    },
    {
        "uri": "wikipedia://best-practices",
        "name": "Wikipedia Tools Best Practices",
        "description": "Guidelines for optimal tool usage",
        "mimeType": "application/json"
    }
]

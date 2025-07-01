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
                    "description": "Full wikitext content (optional, only included if include_full_content=true)"
                }
            },
            "required": ["success", "page_title"]
        }
        return json.dumps(schema, indent=2)
    
    @mcp_server.resource(
        uri="wikipedia://schema/page-summary",
        name="Wikipedia Page Summary Schema",
        description="JSON schema for Wikipedia page summary returned by get_wikipedia_page_summary tool"
    )
    def wikipedia_page_summary_schema() -> str:
        """Return the JSON schema for Wikipedia page summary."""
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Wikipedia Page Summary",
            "description": "Schema for Wikipedia page summary",
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
                    "type": "string",
                    "description": "Brief summary text from page summary"
                },
                "extract": {
                    "type": "string",
                    "description": "Content extract with specified number of sentences"
                },
                "description": {
                    "type": "string",
                    "description": "Short page description"
                }
            },
            "required": ["success", "page_title"]
        }
        return json.dumps(schema, indent=2)
    
    @mcp_server.resource(
        uri="wikipedia://schema/page-sections",
        name="Wikipedia Page Sections Schema",
        description="JSON schema for Wikipedia page sections returned by get_wikipedia_page_sections tool"
    )
    def wikipedia_page_sections_schema() -> str:
        """Return the JSON schema for Wikipedia page sections."""
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Wikipedia Page Sections",
            "description": "Schema for Wikipedia page sections",
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
                "sections": {
                    "type": "array",
                    "description": "List of page sections",
                    "items": {
                        "type": "object",
                        "properties": {
                            "index": {
                                "type": "string",
                                "description": "Section index"
                            },
                            "title": {
                                "type": "string",
                                "description": "Section title"
                            },
                            "level": {
                                "type": "integer",
                                "description": "Section level (1, 2, 3, etc.)"
                            },
                            "anchor": {
                                "type": "string",
                                "description": "Section anchor for direct linking"
                            },
                            "number": {
                                "type": "string",
                                "description": "Section number"
                            }
                        },
                        "required": ["index", "title", "level"]
                    }
                }
            },
            "required": ["success", "page_title"]
        }
        return json.dumps(schema, indent=2)
    
    @mcp_server.resource(
        uri="wikipedia://schema/sections-info",
        name="Wikipedia Page Sections Info Schema",
        description="JSON schema for Wikipedia page sections content returned by get_wikipedia_page_sections_info tool"
    )
    def wikipedia_page_sections_info_schema() -> str:
        """Return the JSON schema for Wikipedia page sections content."""
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Wikipedia Page Sections Content",
            "description": "Schema for Wikipedia page sections content",
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
                "sections_content": {
                    "type": "object",
                    "description": "Dictionary mapping section identifiers to their content",
                    "additionalProperties": {
                        "type": ["string", "null"],
                        "description": "Section content in wikitext format, or null if section not found"
                    }
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
                    "use_case": "When you need the complete article content for analysis (discouraged unless specifically needed)"
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
            "page_summary_examples": {
                "basic_summary": {
                    "tool": "get_wikipedia_page_summary",
                    "input": {
                        "page_title": "Artificial intelligence"
                    },
                    "description": "Get a quick 3-sentence summary of AI",
                    "use_case": "When you need a brief overview of a topic"
                },
                "longer_summary": {
                    "tool": "get_wikipedia_page_summary",
                    "input": {
                        "page_title": "Deep learning",
                        "sentences": 5
                    },
                    "description": "Get a 5-sentence summary of deep learning",
                    "use_case": "When you need more context than the default 3 sentences"
                },
                "multilingual_summary": {
                    "tool": "get_wikipedia_page_summary",
                    "input": {
                        "page_title": "Aprendizaje automático",
                        "language": "es",
                        "sentences": 2
                    },
                    "description": "Get a brief Spanish summary of machine learning",
                    "use_case": "For quick overviews in specific languages"
                }
            },
            "page_sections_examples": {
                "list_sections": {
                    "tool": "get_wikipedia_page_sections",
                    "input": {
                        "page_title": "Artificial intelligence"
                    },
                    "description": "Get all sections of the AI article",
                    "use_case": "When an article is large and you want to see the structure before requesting specific content"
                },
                "explore_large_page": {
                    "tool": "get_wikipedia_page_sections",
                    "input": {
                        "page_title": "History of science"
                    },
                    "description": "View sections of a comprehensive historical article",
                    "use_case": "For navigation of long, detailed articles"
                }
            },
            "sections_content_examples": {
                "specific_sections_by_title": {
                    "tool": "get_wikipedia_page_sections_info",
                    "input": {
                        "page_title": "Machine learning",
                        "section_titles": ["History", "Applications"]
                    },
                    "description": "Get content for History and Applications sections",
                    "use_case": "When you know the section names you're interested in"
                },
                "specific_sections_by_index": {
                    "tool": "get_wikipedia_page_sections_info",
                    "input": {
                        "page_title": "Python (programming language)",
                        "section_indices": ["1", "3", "5"]
                    },
                    "description": "Get content for sections 1, 3, and 5",
                    "use_case": "When you have section indices from get_wikipedia_page_sections"
                },
                "all_sections_content": {
                    "tool": "get_wikipedia_page_sections_info",
                    "input": {
                        "page_title": "Natural language processing"
                    },
                    "description": "Get content for all sections of the NLP article",
                    "use_case": "When you need complete structured content but want it organized by sections"
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
                            "action": "get_wikipedia_page_summary",
                            "input": {"page_title": "Quantum computing", "sentences": 5},
                            "purpose": "Get a quick overview of the main topic"
                        },
                        {
                            "step": 3,
                            "action": "get_wikipedia_page_sections",
                            "input": {"page_title": "Quantum computing"},
                            "purpose": "See the structure of the article to identify sections of interest"
                        },
                        {
                            "step": 4,
                            "action": "get_wikipedia_page_sections_info",
                            "input": {"page_title": "Quantum computing", "section_titles": ["Applications", "Quantum algorithms"]},
                            "purpose": "Get detailed content for specific sections of interest"
                        },
                        {
                            "step": 5,
                            "action": "get_wikipedia_page_info",
                            "input": {"page_title": "Quantum algorithm"},
                            "purpose": "Explore related topics from hyperlinks"
                        }
                    ],
                    "description": "Comprehensive research workflow for exploring a new topic systematically"
                },
                "fact_checking": {
                    "steps": [
                        {
                            "step": 1,
                            "action": "search_wikipedia_pages",
                            "input": {"query": "specific claim or topic"},
                            "purpose": "Find the most relevant page for the claim"
                        },
                        {
                            "step": 2,
                            "action": "get_wikipedia_page_summary",
                            "input": {"page_title": "Specific claim or topic"},
                            "purpose": "Get quick verification of basic facts"
                        }
                    ],
                    "description": "Quick fact-checking workflow"
                },
                "large_article_exploration": {
                    "steps": [
                        {
                            "step": 1,
                            "action": "get_wikipedia_page_summary",
                            "input": {"page_title": "History of science"},
                            "purpose": "Get an overview of the large article"
                        },
                        {
                            "step": 2,
                            "action": "get_wikipedia_page_sections",
                            "input": {"page_title": "History of science"},
                            "purpose": "See all available sections to choose what to read"
                        },
                        {
                            "step": 3,
                            "action": "get_wikipedia_page_sections_info",
                            "input": {"page_title": "History of science", "section_titles": ["Ancient history", "Medieval science"]},
                            "purpose": "Get content for only the sections you're interested in"
                        }
                    ],
                    "description": "Efficient workflow for exploring large Wikipedia articles without overwhelming content"
                },
                "comparative_analysis": {
                    "steps": [
                        {
                            "step": 1,
                            "action": "get_wikipedia_page_sections",
                            "input": {"page_title": "Machine learning"},
                            "purpose": "Get structure of first topic"
                        },
                        {
                            "step": 2,
                            "action": "get_wikipedia_page_sections",
                            "input": {"page_title": "Deep learning"},
                            "purpose": "Get structure of second topic"
                        },
                        {
                            "step": 3,
                            "action": "get_wikipedia_page_sections_info",
                            "input": {"page_title": "Machine learning", "section_titles": ["Applications", "Algorithms"]},
                            "purpose": "Get specific content from first topic"
                        },
                        {
                            "step": 4,
                            "action": "get_wikipedia_page_sections_info",
                            "input": {"page_title": "Deep learning", "section_titles": ["Applications", "Algorithms"]},
                            "purpose": "Get matching content from second topic for comparison"
                        }
                    ],
                    "description": "Workflow for comparing similar topics by examining equivalent sections"
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
                    "Use summary for quick overviews (get_wikipedia_page_summary)",
                    "Use page info for comprehensive information (get_wikipedia_page_info)",
                    "Use sections listing to navigate large articles (get_wikipedia_page_sections)",
                    "Use section content for targeted information (get_wikipedia_page_sections_info)",
                    "Use hyperlinked words to discover related topics",
                    "Avoid full content unless specifically needed for deep analysis"
                ],
                "tool_selection": [
                    "get_wikipedia_page_summary: Best for quick overviews and introductions",
                    "get_wikipedia_page_info: Best for comprehensive topic research",
                    "get_wikipedia_page_sections: Best for exploring article structure",
                    "get_wikipedia_page_sections_info: Best for targeted section content",
                    "search_wikipedia_pages: Best for discovering relevant articles"
                ],
                "large_article_strategy": [
                    "Start with get_wikipedia_page_summary for overview",
                    "Use get_wikipedia_page_sections to see article structure",
                    "Select specific sections with get_wikipedia_page_sections_info",
                    "This approach is more efficient than loading full content"
                ],
                "section_usage": [
                    "Use section titles when you know the exact section names",
                    "Use section indices when working with section list results",
                    "Request multiple sections in one call when possible",
                    "If no sections specified, all sections will be returned"
                ],
                "performance_optimization": [
                    "Start with summaries before requesting full content",
                    "Use section tools for large articles to reduce data transfer",
                    "Cache frequently accessed pages and sections",
                    "Limit hyperlink retrieval to reasonable numbers",
                    "Consider using section tools instead of full page content"
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
        "uri": "wikipedia://schema/page-summary",
        "name": "Wikipedia Page Summary Schema", 
        "description": "JSON schema for Wikipedia page summary",
        "mimeType": "application/json"
    },
    {
        "uri": "wikipedia://schema/page-sections",
        "name": "Wikipedia Page Sections Schema", 
        "description": "JSON schema for Wikipedia page sections",
        "mimeType": "application/json"
    },
    {
        "uri": "wikipedia://schema/sections-info",
        "name": "Wikipedia Page Sections Info Schema", 
        "description": "JSON schema for Wikipedia page sections content",
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

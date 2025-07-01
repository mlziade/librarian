"""
Wikipedia API Module

This module provides common methods for interacting with Wikipedia using the MediaWiki API.
It includes functions for searching, retrieving page content, getting summaries, and more.
"""

import httpx
from typing import List, Dict, Optional, Any
from urllib.parse import quote_plus


class WikipediaAPI:
    """A class to interact with Wikipedia's MediaWiki API."""
    
    def __init__(self, language: str = "en"):
        """
        Initialize the Wikipedia API client.
        
        Args:
            language (str): Language code for Wikipedia (e.g., 'en', 'es', 'fr')
        """
        self.language = language
        self.base_url = f"https://{language}.wikipedia.org/api/rest_v1"
        self.api_url = f"https://{language}.wikipedia.org/w/api.php"
        self.client = httpx.Client()
        self.client.headers.update({
            'User-Agent': 'Librarian/1.0 (https://github.com/user/librarian)'
        })
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close the client."""
        self.client.close()
    
    def close(self):
        """Explicitly close the HTTP client."""
        self.client.close()
    
    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for Wikipedia articles.
        
        Args:
            query (str): Search query
            limit (int): Maximum number of results to return
            
        Returns:
            List[Dict]: List of search results with title and snippet
        """
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': query,
            'srlimit': limit,
            'srprop': 'snippet|titlesnippet|size|wordcount|timestamp'
        }
        
        try:
            response = self.client.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('query', {}).get('search', [])
        except httpx.RequestError as e:
            print(f"Error searching Wikipedia: {e}")
            return []
    
    def get_page_summary(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Get a summary of a Wikipedia page.
        
        Args:
            title (str): Page title
            
        Returns:
            Optional[Dict]: Page summary including extract and basic info
        """
        encoded_title = quote_plus(title.replace(' ', '_'))
        url = f"{self.base_url}/page/summary/{encoded_title}"
        
        try:
            response = self.client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            print(f"Error getting page summary for '{title}': {e}")
            return None
    
    def get_page_content(self, title: str) -> Optional[str]:
        """
        Get the full content of a Wikipedia page.
        
        Args:
            title (str): Page title
            
        Returns:
            Optional[str]: Page content in wikitext format
        """
        params = {
            'action': 'query',
            'format': 'json',
            'titles': title,
            'prop': 'revisions',
            'rvprop': 'content',
            'rvslots': 'main'
        }
        
        try:
            response = self.client.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                if page_id != '-1':  # Page exists
                    revisions = page_data.get('revisions', [])
                    if revisions:
                        return revisions[0]['slots']['main']['*']
            return None
        except httpx.RequestError as e:
            print(f"Error getting page content for '{title}': {e}")
            return None
    
    def get_page_extract(self, title: str, sentences: int = 3) -> Optional[str]:
        """
        Get a plain text extract of a Wikipedia page.
        
        Args:
            title (str): Page title
            sentences (int): Number of sentences to extract
            
        Returns:
            Optional[str]: Plain text extract
        """
        params = {
            'action': 'query',
            'format': 'json',
            'titles': title,
            'prop': 'extracts',
            'exsentences': sentences,
            'explaintext': True,
            'exsectionformat': 'plain'
        }
        
        try:
            response = self.client.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                if page_id != '-1':  # Page exists
                    return page_data.get('extract', '')
            return None
        except httpx.RequestError as e:
            print(f"Error getting page extract for '{title}': {e}")
            return None
    
    def get_page_categories(self, title: str) -> List[str]:
        """
        Get categories for a Wikipedia page.
        
        Args:
            title (str): Page title
            
        Returns:
            List[str]: List of category names
        """
        params = {
            'action': 'query',
            'format': 'json',
            'titles': title,
            'prop': 'categories',
            'cllimit': 'max'
        }
        
        try:
            response = self.client.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                if page_id != '-1':  # Page exists
                    categories = page_data.get('categories', [])
                    return [cat['title'].replace('Category:', '') for cat in categories]
            return []
        except httpx.RequestError as e:
            print(f"Error getting categories for '{title}': {e}")
            return []
    
    def get_page_links(self, title: str, limit: int = 100) -> List[str]:
        """
        Get links from a Wikipedia page.
        
        Args:
            title (str): Page title
            limit (int): Maximum number of links to return
            
        Returns:
            List[str]: List of linked page titles
        """
        params = {
            'action': 'query',
            'format': 'json',
            'titles': title,
            'prop': 'links',
            'pllimit': limit,
            'plnamespace': 0  # Main namespace only
        }
        
        try:
            response = self.client.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                if page_id != '-1':  # Page exists
                    links = page_data.get('links', [])
                    return [link['title'] for link in links]
            return []
        except httpx.RequestError as e:
            print(f"Error getting links for '{title}': {e}")
            return []
    
    def get_page_images(self, title: str) -> List[Dict[str, str]]:
        """
        Get images from a Wikipedia page.
        
        Args:
            title (str): Page title
            
        Returns:
            List[Dict]: List of image information
        """
        params = {
            'action': 'query',
            'format': 'json',
            'titles': title,
            'prop': 'images'
        }
        
        try:
            response = self.client.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                if page_id != '-1':  # Page exists
                    images = page_data.get('images', [])
                    return [{'title': img['title']} for img in images]
            return []
        except httpx.RequestError as e:
            print(f"Error getting images for '{title}': {e}")
            return []
    
    def get_random_pages(self, count: int = 1) -> List[str]:
        """
        Get random Wikipedia page titles.
        
        Args:
            count (int): Number of random pages to retrieve
            
        Returns:
            List[str]: List of random page titles
        """
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'random',
            'rnlimit': count,
            'rnnamespace': 0  # Main namespace only
        }
        
        try:
            response = self.client.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            random_pages = data.get('query', {}).get('random', [])
            return [page['title'] for page in random_pages]
        except httpx.RequestError as e:
            print(f"Error getting random pages: {e}")
            return []
    
    def page_exists(self, title: str) -> bool:
        """
        Check if a Wikipedia page exists.
        
        Args:
            title (str): Page title
            
        Returns:
            bool: True if page exists, False otherwise
        """
        params = {
            'action': 'query',
            'format': 'json',
            'titles': title
        }
        
        try:
            response = self.client.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            pages = data.get('query', {}).get('pages', {})
            return '-1' not in pages  # -1 indicates missing page
        except httpx.RequestError as e:
            print(f"Error checking if page exists '{title}': {e}")
            return False
    
    def get_page_info(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Get basic information about a Wikipedia page.
        
        Args:
            title (str): Page title
            
        Returns:
            Optional[Dict]: Page information including length, last modified, etc.
        """
        params = {
            'action': 'query',
            'format': 'json',
            'titles': title,
            'prop': 'info',
            'inprop': 'url|displaytitle|length|touched'
        }
        
        try:
            response = self.client.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                if page_id != '-1':  # Page exists
                    return page_data
            return None
        except httpx.RequestError as e:
            print(f"Error getting page info for '{title}': {e}")
            return None


# Convenience functions for quick access
def search_wikipedia(query: str, language: str = "en", limit: int = 10) -> List[Dict[str, Any]]:
    """Quick search function."""
    api = WikipediaAPI(language)
    return api.search(query, limit)


def get_wikipedia_summary(title: str, language: str = "en") -> Optional[Dict[str, Any]]:
    """Quick summary function."""
    api = WikipediaAPI(language)
    return api.get_page_summary(title)


def get_wikipedia_extract(title: str, language: str = "en", sentences: int = 3) -> Optional[str]:
    """Quick extract function."""
    api = WikipediaAPI(language)
    return api.get_page_extract(title, sentences)


if __name__ == "__main__":
    # Example usage - Synchronous API
    print("=== Synchronous API Examples ===")
    
    # Using context manager (recommended)
    with WikipediaAPI() as api:
        # Search for articles
        results = api.search("Python programming", limit=5)
        print("Search results:")
        for result in results:
            print(f"- {result['title']}")
        
        # Get a page summary
        summary = api.get_page_summary("Python (programming language)")
        if summary:
            print(f"\nSummary: {summary.get('extract', '')[:200]}...")
        
        # Get page extract
        extract = api.get_page_extract("Python (programming language)", sentences=2)
        if extract:
            print(f"\nExtract: {extract}")
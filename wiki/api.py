"""
Wikipedia API Module

This module provides common methods for interacting with Wikipedia using the MediaWiki API.
It includes functions for searching, retrieving page content, getting summaries, and more.
"""

import httpx
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
    
    def search(self, query: str, limit: int = 10) -> list[dict[str, any]]:
        """
        Search for Wikipedia articles.
        
        Args:
            query (str): Search query
            limit (int): Maximum number of results to return
            
        Returns:
            list[dict]: List of search results with title and snippet
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
    
    def get_page_summary(self, title: str) -> dict[str, any] | None:
        """
        Get a summary of a Wikipedia page.
        
        Args:
            title (str): Page title
            
        Returns:
            dict | None: Page summary including extract and basic info
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
    
    def get_page_content(self, title: str) -> str | None:
        """
        Get the full content of a Wikipedia page.
        
        Args:
            title (str): Page title
            
        Returns:
            str | None: Page content in wikitext format
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
    
    def get_page_sections(self, title: str) -> list[dict[str, any]]:
        """
        Get the table of contents (section structure) of a Wikipedia page.
        
        Args:
            title (str): Page title
            
        Returns:
            list[dict]: List of sections with index, title, level, and anchor
        """
        params = {
            'action': 'parse',
            'format': 'json',
            'page': title,
            'prop': 'sections'
        }
        
        try:
            response = self.client.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'parse' in data and 'sections' in data['parse']:
                sections = data['parse']['sections']
                # Format sections for easier use
                formatted_sections = []
                for section in sections:
                    formatted_sections.append({
                        'index': section.get('index', ''),
                        'title': section.get('line', ''),
                        'level': int(section.get('level', 1)),
                        'anchor': section.get('anchor', ''),
                        'number': section.get('number', '')
                    })
                return formatted_sections
            return []
        except httpx.RequestError as e:
            print(f"Error getting page sections for '{title}': {e}")
            return []
    
    def get_page_sections_content(self, title: str, section_indices: list[str]) -> dict[str, str]:
        """
        Get the content of specific sections from a Wikipedia page.
        
        Args:
            title (str): Page title
            section_indices (list[str]): List of section indices to retrieve
            
        Returns:
            dict[str, str]: Dictionary mapping section indices to their content
        """
        result = {}
        
        for section_index in section_indices:
            params = {
                'action': 'parse',
                'format': 'json',
                'page': title,
                'section': section_index,
                'prop': 'wikitext'
            }
            
            try:
                response = self.client.get(self.api_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if 'parse' in data and 'wikitext' in data['parse']:
                    wikitext = data['parse']['wikitext']['*']
                    result[section_index] = wikitext
                else:
                    result[section_index] = None
            except httpx.RequestError as e:
                print(f"Error getting section {section_index} for '{title}': {e}")
                result[section_index] = None
        
        return result
    
    def get_page_sections_content_by_title(self, title: str, section_titles: list[str]) -> dict[str, str]:
        """
        Get the content of specific sections from a Wikipedia page by section titles.
        
        Args:
            title (str): Page title
            section_titles (list[str]): List of section titles to retrieve
            
        Returns:
            dict[str, str]: Dictionary mapping section titles to their content
        """
        # First get all sections to find the indices
        sections = self.get_page_sections(title)
        if not sections:
            return {}
        
        # Create a mapping of section titles to indices
        title_to_index = {}
        for section in sections:
            section_title = section['title'].strip()
            for target_title in section_titles:
                if section_title.lower() == target_title.lower():
                    title_to_index[target_title] = section['index']
        
        # Get content for found sections
        if not title_to_index:
            return {}
        
        indices = list(title_to_index.values())
        content_by_index = self.get_page_sections_content(title, indices)
        
        # Map back to section titles
        result = {}
        for section_title, section_index in title_to_index.items():
            result[section_title] = content_by_index.get(section_index)
        
        return result
    
    def get_page_categories(self, title: str) -> list[str]:
        """
        Get categories for a Wikipedia page.
        
        Args:
            title (str): Page title
            
        Returns:
            list[str]: List of category names
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
    
    def get_page_links(self, title: str, limit: int = 100) -> list[str]:
        """
        Get links from a Wikipedia page.
        
        Args:
            title (str): Page title
            limit (int): Maximum number of links to return
            
        Returns:
            list[str]: List of linked page titles
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
    
    def get_page_images(self, title: str) -> list[dict[str, str]]:
        """
        Get images from a Wikipedia page.
        
        Args:
            title (str): Page title
            
        Returns:
            list[dict]: List of image information
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
    
    def get_random_pages(self, count: int = 1) -> list[str]:
        """
        Get random Wikipedia page titles.
        
        Args:
            count (int): Number of random pages to retrieve
            
        Returns:
            list[str]: List of random page titles
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
    
    def get_page_info(self, title: str) -> dict[str, any] | None:
        """
        Get basic information about a Wikipedia page.
        
        Args:
            title (str): Page title
            
        Returns:
            dict | None: Page information including length, last modified, etc.
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


if __name__ == "__main__":
    pass
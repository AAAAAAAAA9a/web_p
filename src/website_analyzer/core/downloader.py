"""
Website downloader module.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from typing import Dict, List, Tuple, Set, Callable


class WebsiteDownloader:
    """Handles downloading of websites with configurable depth and limits."""
    
    def __init__(self, max_pages: int = 50, max_depth: int = 2, timeout: int = 10):
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def download_website(self, start_url: str, progress_callback: Callable[[str], None] = None) -> Dict[str, Dict]:
        """
        Download a website starting from the given URL.
        
        Args:
            start_url: The starting URL to download from
            progress_callback: Optional callback function for progress updates
            
        Returns:
            Dictionary mapping URLs to their page data
        """
        if progress_callback:
            progress_callback(f"Rozpoczynam pobieranie: {start_url}")
            
        visited_urls: Set[str] = set()
        to_visit: List[Tuple[str, int]] = [(start_url, 0)]  # (url, depth)
        downloaded_pages: Dict[str, Dict] = {}
        
        base_domain = urlparse(start_url).netloc
        
        while to_visit and len(downloaded_pages) < self.max_pages:
            current_url, depth = to_visit.pop(0)
            
            if current_url in visited_urls or depth > self.max_depth:
                continue
                
            visited_urls.add(current_url)
            
            try:
                if progress_callback:
                    progress_callback(f"Pobieram: {current_url}")
                    
                response = self.session.get(current_url, timeout=self.timeout)
                response.raise_for_status()
                
                downloaded_pages[current_url] = {
                    'content': response.text,
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'url': current_url,
                    'size': len(response.text)
                }
                
                # Parse HTML to find more links
                if 'text/html' in response.headers.get('content-type', ''):
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    for link in soup.find_all('a', href=True):
                        full_url = urljoin(current_url, link['href'])
                        parsed = urlparse(full_url)
                        
                        # Only follow links from the same domain
                        if parsed.netloc == base_domain and full_url not in visited_urls:
                            to_visit.append((full_url, depth + 1))
                            
            except Exception as e:
                if progress_callback:
                    progress_callback(f"Błąd pobierania {current_url}: {str(e)}")
                    
        if progress_callback:
            progress_callback(f"Pobieranie zakończone. Pobrano {len(downloaded_pages)} stron.")
            
        return downloaded_pages
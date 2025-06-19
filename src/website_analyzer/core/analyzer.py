"""
Website analysis module.
"""

from bs4 import BeautifulSoup
from collections import Counter
import re
from typing import Dict, List, Tuple


class WebsiteAnalyzer:
    """Analyzes downloaded website data."""
    
    def __init__(self):
        pass
        
    def analyze_pages(self, downloaded_pages: Dict[str, Dict]) -> Dict[str, str]:
        """
        Analyze downloaded pages and generate comprehensive report.
        
        Args:
            downloaded_pages: Dictionary of downloaded page data
            
        Returns:
            Dictionary containing analysis results for different categories
        """
        if not downloaded_pages:
            return {}
            
        # Basic statistics
        total_pages = len(downloaded_pages)
        total_size = sum(page['size'] for page in downloaded_pages.values())
        
        # Analyze all pages
        all_links = []
        all_images = []
        all_text = ""
        status_codes = []
        
        for url, page_data in downloaded_pages.items():
            content = page_data['content']
            status_codes.append(page_data['status_code'])
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract links
            for link in soup.find_all('a', href=True):
                all_links.append(link['href'])
                
            # Extract images
            for img in soup.find_all('img', src=True):
                all_images.append(img['src'])
                
            # Extract text
            all_text += soup.get_text() + " "
            
        # Generate statistics
        stats = self._generate_statistics(
            total_pages, total_size, status_codes, all_links, all_images, all_text
        )
        
        # Generate detailed analyses
        links_analysis = self._analyze_links(all_links)
        images_analysis = self._analyze_images(all_images)
        
        return {
            'stats': stats,
            'links': links_analysis,
            'images': images_analysis
        }
        
    def _generate_statistics(self, total_pages: int, total_size: int, 
                           status_codes: List[int], all_links: List[str], 
                           all_images: List[str], all_text: str) -> str:
        """Generate basic statistics report."""
        stats = f"""STATYSTYKI WITRYNY / WEBSITE STATISTICS
{'='*50}

Podstawowe informacje:
- Liczba pobranych stron: {total_pages}
- Całkowity rozmiar: {total_size:,} bajtów ({total_size/1024/1024:.2f} MB)
- Średni rozmiar strony: {total_size/total_pages:,.0f} bajtów

Kody odpowiedzi HTTP:
{Counter(status_codes)}

Linki:
- Całkowita liczba linków: {len(all_links)}
- Unikalne linki: {len(set(all_links))}

Obrazy:
- Całkowita liczba obrazów: {len(all_images)}
- Unikalne obrazy: {len(set(all_images))}

Najczęściej używane słowa:
"""
        
        # Word frequency analysis
        words = re.findall(r'\b\w+\b', all_text.lower())
        word_freq = Counter(words)
        common_words = word_freq.most_common(20)
        
        for word, count in common_words:
            if len(word) > 3:  # Skip short words
                stats += f"- {word}: {count}\n"
                
        return stats
        
    def _analyze_links(self, all_links: List[str]) -> str:
        """Analyze links found in the website."""
        links_analysis = "ANALIZA LINKÓW / LINKS ANALYSIS\n" + "="*50 + "\n\n"
        unique_links = set(all_links)
        
        # Categorize links
        internal_links = []
        external_links = []
        email_links = []
        other_links = []
        
        for link in unique_links:
            if link.startswith('mailto:'):
                email_links.append(link)
            elif link.startswith(('http://', 'https://')):
                external_links.append(link)
            elif link.startswith('/') or not link.startswith(('javascript:', '#')):
                internal_links.append(link)
            else:
                other_links.append(link)
                
        links_analysis += f"Linki wewnętrzne ({len(internal_links)}):\n"
        for link in sorted(internal_links)[:50]:  # Limit to first 50
            links_analysis += f"  {link}\n"
            
        links_analysis += f"\nLinki zewnętrzne ({len(external_links)}):\n"
        for link in sorted(external_links)[:50]:
            links_analysis += f"  {link}\n"
            
        if email_links:
            links_analysis += f"\nLinki email ({len(email_links)}):\n"
            for link in sorted(email_links):
                links_analysis += f"  {link}\n"
                
        return links_analysis
        
    def _analyze_images(self, all_images: List[str]) -> str:
        """Analyze images found in the website."""
        images_analysis = "ANALIZA OBRAZÓW / IMAGES ANALYSIS\n" + "="*50 + "\n\n"
        unique_images = set(all_images)
        
        # Categorize by extension
        extensions = {}
        for img in unique_images:
            ext = img.split('.')[-1].lower() if '.' in img else 'unknown'
            if ext not in extensions:
                extensions[ext] = []
            extensions[ext].append(img)
            
        images_analysis += f"Całkowita liczba unikalnych obrazów: {len(unique_images)}\n\n"
        
        for ext, imgs in sorted(extensions.items()):
            images_analysis += f"{ext.upper()} ({len(imgs)}):\n"
            for img in sorted(imgs)[:20]:  # Limit to first 20 per type
                images_analysis += f"  {img}\n"
            images_analysis += "\n"
            
        return images_analysis
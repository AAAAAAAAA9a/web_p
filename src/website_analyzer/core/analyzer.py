"""
Moduł analizy stron internetowych.
"""

from bs4 import BeautifulSoup
from collections import Counter
import re
from typing import Dict, List, Tuple, Callable, Optional


class WebsiteAnalyzer:
    """Analizuje pobrane dane stron internetowych."""
    
    def __init__(self):
        """Inicjalizuje analizator stron."""
        self.min_word_length = 3
        self.max_links_display = 50
        self.max_images_per_type = 20
        
    def analyze_pages(self, downloaded_pages: Dict[str, Dict], progress_callback: Optional[Callable[[str], None]] = None) -> Dict[str, str]:
        """
        Analizuje pobrane strony i generuje szczegółowy raport.
        
        Args:
            downloaded_pages: Słownik z danymi pobranych stron
            progress_callback: Opcjonalna funkcja callback do informowania o postępie
            
        Returns:
            Słownik zawierający wyniki analizy dla różnych kategorii
        """
        if not downloaded_pages:
            return {}
            
        if not downloaded_pages:
            return {'stats': 'Brak danych do analizy.', 'links': '', 'images': ''}
        
        # Podstawowe statystyki
        total_pages = len(downloaded_pages)
        total_size = sum(page['size'] for page in downloaded_pages.values())
        
        # KROK 1: Przygotuj listy do zbierania danych z wszystkich stron
        all_links = []      # wszystkie linki ze wszystkich stron
        all_images = []     # wszystkie obrazy ze wszystkich stron
        all_words = []      # wszystkie słowa ze wszystkich stron
        status_codes = []   # kody HTTP odpowiedzi (200=OK, 404=nie znaleziono, itp.)
        for i, (url, page_data) in enumerate(downloaded_pages.items()):
            if progress_callback:
                progress_callback(f"Analizuję stronę {i+1}/{total_pages}: {url[:50]}...")
                
            content = page_data['content']
            status_codes.append(page_data['status_code'])
            
            # Parse HTML only once per page
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract links
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href:
                    all_links.append(str(href))
                
            # Extract images
            for img in soup.find_all('img', src=True):
                src = img.get('src')
                if src:
                    all_images.append(str(src))
                
            # Wyciągnij słowa bezpośrednio bez przechowywania pełnego tekstu
            text = soup.get_text(separator=' ', strip=True)
            words = re.findall(r'\b[a-ząćęłńóśźż]+\b', text.lower())
            all_words.extend(word for word in words if len(word) >= self.min_word_length)
            
        if progress_callback:
            progress_callback("Generuję statystyki...")
            
        # Generate statistics
        word_freq = Counter(all_words)
        stats = self._generate_statistics(
            total_pages, total_size, status_codes, all_links, all_images, word_freq
        )
        
        # Generate detailed analyses
        if progress_callback:
            progress_callback("Analizuję linki...")
        links_analysis = self._analyze_links(all_links)
        
        if progress_callback:
            progress_callback("Analizuję obrazy...")
        images_analysis = self._analyze_images(all_images)
        
        return {
            'stats': stats,
            'links': links_analysis,
            'images': images_analysis
        }
        
    def _generate_statistics(self, total_pages: int, total_size: int, 
                           status_codes: List[int], all_links: List[str], 
                           all_images: List[str], word_freq: Counter) -> str:
        """Generuje podstawowy raport statystyk."""
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
        
        # Wyświetl najczęstsze słowa
        common_words = word_freq.most_common(20)
        
        if common_words:
            for word, count in common_words:
                stats += f"- {word}: {count}\n"
        else:
            stats += "Brak słów do analizy.\n"
                
        return stats
        
    def _analyze_links(self, all_links: List[str]) -> str:
        """Analizuje linki znalezione na stronie internetowej."""
        links_analysis = "ANALIZA LINKÓW / LINKS ANALYSIS\n" + "="*50 + "\n\n"
        unique_links = set(all_links)
        
        # Kategoryzuj linki
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
        for link in sorted(internal_links)[:self.max_links_display]:
            links_analysis += f"  {link}\n"
            
        links_analysis += f"\nLinki zewnętrzne ({len(external_links)}):\n"
        for link in sorted(external_links)[:self.max_links_display]:
            links_analysis += f"  {link}\n"
            
        if email_links:
            links_analysis += f"\nLinki email ({len(email_links)}):\n"
            for link in sorted(email_links):
                links_analysis += f"  {link}\n"
                
        return links_analysis
        
    def _analyze_images(self, all_images: List[str]) -> str:
        """Analizuje obrazy znalezione na stronie internetowej."""
        images_analysis = "ANALIZA OBRAZÓW / IMAGES ANALYSIS\n" + "="*50 + "\n\n"
        unique_images = set(all_images)
        
        # Kategoryzuj według rozszerzenia
        extensions = {}
        for img in unique_images:
            ext = img.split('.')[-1].lower() if '.' in img else 'unknown'
            if ext not in extensions:
                extensions[ext] = []
            extensions[ext].append(img)
            
        images_analysis += f"Całkowita liczba unikalnych obrazów: {len(unique_images)}\n\n"
        
        for ext, imgs in sorted(extensions.items()):
            images_analysis += f"{ext.upper()} ({len(imgs)}):\n"
            for img in sorted(imgs)[:self.max_images_per_type]:
                images_analysis += f"  {img}\n"
            images_analysis += "\n"
            
        return images_analysis
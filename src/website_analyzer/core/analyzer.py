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
        self.max_media_per_type = 15
        
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
        total_size = sum(page['size'] for page in downloaded_pages.values())          # KROK 1: Przygotuj listy do zbierania danych z wszystkich stron
        all_links = []      # wszystkie linki ze wszystkich stron
        all_images = []     # wszystkie obrazy ze wszystkich stron
        all_videos = []     # wszystkie filmy ze wszystkich stron
        all_audio = []      # wszystkie pliki audio ze wszystkich stron
        all_css = []        # wszystkie pliki CSS ze wszystkich stron
        all_js = []         # wszystkie pliki JavaScript ze wszystkich stron
        all_documents = []  # wszystkie dokumenty (PDF, DOC, itp.)
        all_words = []      # wszystkie słowa ze wszystkich stron
        status_codes = []   # kody HTTP odpowiedzi (200=OK, 404=nie znaleziono, itp.)
        for i, (url, page_data) in enumerate(downloaded_pages.items()):
            if progress_callback:
                progress_callback(f"Analizuję stronę {i+1}/{total_pages}: {url[:50]}...")
                
            content = page_data['content']
            status_codes.append(page_data['status_code'])
            
            # Parsuj HTML tylko raz na stronę
            soup = BeautifulSoup(content, 'html.parser')
            
            # Wyciągnij linki
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href:
                    all_links.append(str(href))                  # Wyciągnij obrazy
            for img in soup.find_all('img', src=True):
                src = img.get('src')
                if src:
                    all_images.append(str(src))
            
            # Wyciągnij filmy
            for video in soup.find_all('video', src=True):
                src = video.get('src')
                if src:
                    all_videos.append(str(src))
            
            # Wyciągnij źródła filmów
            for source in soup.find_all('source', src=True):
                src = source.get('src')
                if src and any(ext in src.lower() for ext in ['.mp4', '.webm', '.avi', '.mov']):
                    all_videos.append(str(src))
            
            # Wyciągnij pliki audio
            for audio in soup.find_all('audio', src=True):
                src = audio.get('src')
                if src:
                    all_audio.append(str(src))
            
            # Wyciągnij źródła plików audio
            for source in soup.find_all('source', src=True):
                src = source.get('src')
                if src and any(ext in src.lower() for ext in ['.mp3', '.wav', '.ogg', '.m4a']):
                    all_audio.append(str(src))
            
            # Wyciągnij pliki CSS
            for link in soup.find_all('link', rel='stylesheet'):
                href = link.get('href')
                if href:
                    all_css.append(str(href))
            
            # Wyciągnij pliki JavaScript
            for script in soup.find_all('script', src=True):
                src = script.get('src')
                if src:
                    all_js.append(str(src))
            
            # Wyciągnij linki do dokumentów z tagów <a>
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href and any(ext in href.lower() for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar']):
                    all_documents.append(str(href))
                
            # Wyciągnij słowa bezpośrednio bez przechowywania pełnego tekstu
            text = soup.get_text(separator=' ', strip=True)
            words = re.findall(r'\b[a-ząćęłńóśźż]+\b', text.lower())
            all_words.extend(word for word in words if len(word) >= self.min_word_length)
            
        if progress_callback:
            progress_callback("Generuję statystyki...")              # Wygeneruj statystyki
        word_freq = Counter(all_words)
        stats = self._generate_statistics(
            total_pages, total_size, status_codes, all_links, all_images, 
            all_videos, all_audio, all_css, all_js, all_documents, word_freq        )
        
        # Wygeneruj szczegółowe analizy
        if progress_callback:
            progress_callback("Analizuję linki...")
        links_analysis = self._analyze_links(all_links)
        
        if progress_callback:
            progress_callback("Analizuję obrazy...")
        images_analysis = self._analyze_images(all_images)
        
        if progress_callback:
            progress_callback("Analizuję media...")
        media_analysis = self._analyze_media_only(all_videos, all_audio)
        
        if progress_callback:
            progress_callback("Analizuję zasoby...")
        resources_analysis = self._analyze_resources(all_css, all_js)
        
        if progress_callback:
            progress_callback("Analizuję dokumenty...")
        documents_analysis = self._analyze_documents(all_documents)
        
        return {
            'stats': stats,
            'links': links_analysis,
            'images': images_analysis,
            'media': media_analysis,
            'resources': resources_analysis,
            'documents': documents_analysis
        }
    
    def _generate_statistics(self, total_pages: int, total_size: int, 
                           status_codes: List[int], all_links: List[str], 
                           all_images: List[str], all_videos: List[str], 
                           all_audio: List[str], all_css: List[str], 
                           all_js: List[str], all_documents: List[str], word_freq: Counter) -> str:
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

Media:
- Pliki video: {len(set(all_videos))}
- Pliki audio: {len(set(all_audio))}
- Pliki CSS: {len(set(all_css))}
- Pliki JavaScript: {len(set(all_js))}
- Dokumenty: {len(set(all_documents))}

Najczęstsze słowa:
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
          # Skategoryzuj linki
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
        
        # Skategoryzuj według rozszerzenia
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
    
    def _analyze_media_only(self, all_videos: List[str], all_audio: List[str]) -> str:
        """Analizuje pliki video i audio."""
        media_analysis = "ANALIZA MEDIÓW / MEDIA ANALYSIS\n" + "="*50 + "\n\n"
        
        # Analiza video
        unique_videos = set(all_videos)
        if unique_videos:
            media_analysis += f"PLIKI VIDEO ({len(unique_videos)}):\n"
            for video in sorted(unique_videos)[:self.max_media_per_type]:
                media_analysis += f"  {video}\n"
            media_analysis += "\n"
        
        # Analiza audio
        unique_audio = set(all_audio)
        if unique_audio:
            media_analysis += f"PLIKI AUDIO ({len(unique_audio)}):\n"
            for audio in sorted(unique_audio)[:self.max_media_per_type]:
                media_analysis += f"  {audio}\n"
            media_analysis += "\n"
        
        if not unique_videos and not unique_audio:
            media_analysis += "Nie znaleziono plików video ani audio.\n"
            
        return media_analysis
    
    def _analyze_resources(self, all_css: List[str], all_js: List[str]) -> str:
        """Analizuje zasoby CSS i JavaScript."""
        resources_analysis = "ANALIZA ZASOBÓW / RESOURCES ANALYSIS\n" + "="*50 + "\n\n"
        
        # Analiza CSS
        unique_css = set(all_css)
        if unique_css:
            resources_analysis += f"PLIKI CSS ({len(unique_css)}):\n"
            for css in sorted(unique_css)[:self.max_media_per_type]:
                resources_analysis += f"  {css}\n"
            resources_analysis += "\n"
          # Analiza JavaScript
        unique_js = set(all_js)
        if unique_js:
            resources_analysis += f"PLIKI JAVASCRIPT ({len(unique_js)}):\n"
            for js in sorted(unique_js)[:self.max_media_per_type]:
                resources_analysis += f"  {js}\n"
            resources_analysis += "\n"
        
        if not unique_css and not unique_js:
            resources_analysis += "Nie znaleziono plików CSS ani JavaScript.\n"
            
        return resources_analysis
    
    def _analyze_documents(self, all_documents: List[str]) -> str:
        """Analizuje dokumenty do pobrania."""
        documents_analysis = "ANALIZA DOKUMENTÓW / DOCUMENTS ANALYSIS\n" + "="*50 + "\n\n"
        
        unique_docs = set(all_documents)
        if unique_docs:            # Skategoryzuj według rozszerzenia
            extensions = {}
            for doc in unique_docs:
                ext = doc.split('.')[-1].lower() if '.' in doc else 'unknown'
                if ext not in extensions:
                    extensions[ext] = []
                extensions[ext].append(doc)
            
            documents_analysis += f"Całkowita liczba dokumentów: {len(unique_docs)}\n\n"
            
            for ext, docs in sorted(extensions.items()):
                documents_analysis += f"{ext.upper()} ({len(docs)}):\n"
                for doc in sorted(docs)[:self.max_media_per_type]:
                    documents_analysis += f"  {doc}\n"
                documents_analysis += "\n"
        else:
            documents_analysis += "Nie znaleziono dokumentów do pobrania.\n"
            
        return documents_analysis
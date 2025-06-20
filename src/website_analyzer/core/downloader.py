"""
Moduł pobierania stron internetowych.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from typing import Dict, List, Tuple, Set, Callable, Optional, Union

from .error_handler import handle_network_error, log_error


class WebsiteDownloader:
    """
    Klasa do pobierania stron internetowych.
    
    Ta klasa implementuje webcrawler - program, który automatycznie
    odwiedza strony internetowe i pobiera ich zawartość.
    Można ustawić maksymalną liczbę stron i głębokość przeszukiwania.
    
    Crawler ogranicza się do:
    - Tej samej domeny co URL startowy
    - Tej samej ścieżki bazowej co URL startowy (np. jeśli zaczynasz od 
      https://example.com/docs, crawler pozostanie w /docs i podkatalogach)
    """
    
    def __init__(self, max_pages: int = 50, max_depth: int = 2, timeout: int = 10):
        """
        Konstruktor klasy WebsiteDownloader.
        
        Argumenty:
            max_pages: maksymalna liczba stron do pobrania (domyślnie 50)
            max_depth: głębokość przeszukiwania - ile poziomów linków (domyślnie 2)
            timeout: czas oczekiwania na odpowiedź serwera w sekundach (domyślnie 10)
        """
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.timeout = timeout
        self.base_path = ""  # Ścieżka bazowa do ograniczenia crawlowania
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def download_website(self, start_url: str, progress_callback: Optional[Callable[[str], None]] = None) -> Dict[str, Dict]:
        """
        Główna metoda pobierająca witrynę internetową.
        
        Algorytm:
        1. Sprawdza czy URL jest poprawny
        2. Tworzy kolejkę stron do odwiedzenia
        3. W pętli pobiera każdą stronę
        4. Parsuje HTML i znajduje nowe linki
        5. Dodaje nowe linki do kolejki (jeśli nie przekroczono limitów)
        
        Argumenty:
            start_url: adres strony od której zaczynamy pobieranie
            progress_callback: funkcja do wyświetlania postępu (opcjonalna)
            
        Zwraca:
            Słownik gdzie klucz=URL, wartość=dane strony (zawartość, nagłówki, itp.)
        """
        # KROK 1: Sprawdź czy URL jest poprawny
        if not self._is_valid_url(start_url):
            raise ValueError(f"Nieprawidłowy URL: {start_url}")
            
        if progress_callback:
            progress_callback(f"Rozpoczynam pobieranie: {start_url}")
            
        # KROK 2: Przygotuj struktury danych do śledzenia postępu
        visited_urls: Set[str] = set()  # już odwiedzone URL
        to_visit: List[Tuple[str, int]] = [(start_url, 0)]  # kolejka: (url, głębokość)
        downloaded_pages: Dict[str, Dict] = {}  # wyniki
        
        # KROK 3: Określ domenę bazową i ścieżkę bazową
        parsed_start = urlparse(start_url)
        base_domain = parsed_start.netloc
        self.base_path = parsed_start.path.rstrip('/')
        
        # Jeśli ścieżka jest pusta lub tylko "/", nie ograniczamy ścieżki
        if self.base_path in ('', '/'):
            self.base_path = ""
        
        # KROK 4: Główna pętla pobierania
        while to_visit and len(downloaded_pages) < self.max_pages:
            # Weź następny URL z kolejki
            current_url, depth = to_visit.pop(0)
            
            # Sprawdź czy już nie odwiedziliśmy tej strony lub czy nie za głęboko
            if current_url in visited_urls or depth > self.max_depth:
                continue  # przejdź do następnego URL
                
            # Zaznacz jako odwiedzone
            visited_urls.add(current_url)
            
            # Spróbuj pobrać stronę
            if progress_callback:
                progress_callback(f"Pobieram: {current_url}")
                
            success, result = self._download_single_page(current_url)
            if success:
                downloaded_pages[current_url] = result  # type: ignore
                
                # Znajdź nowe linki jeśli to HTML
                if isinstance(result, dict):
                    new_links = self._find_new_links(result, current_url, base_domain)
                else:
                    new_links = []
                for link_url in new_links:
                    if link_url not in visited_urls and len(to_visit) < 1000:
                        # Dodatkowe zabezpieczenie - sprawdź ścieżkę przed dodaniem do kolejki
                        if self.base_path:
                            parsed_link = urlparse(link_url)
                            if not (parsed_link.path == self.base_path or parsed_link.path.startswith(self.base_path + "/")):
                                continue  # pomiń linki spoza ścieżki bazowej
                        to_visit.append((link_url, depth + 1))
            else:
                # result zawiera komunikat błędu
                if progress_callback:
                    progress_callback(result) # type: ignore
                    
        if progress_callback:
            progress_callback(f"Pobieranie zakończone. Pobrano {len(downloaded_pages)} stron.")
            
        return downloaded_pages
    
    def _download_single_page(self, url: str) -> Tuple[bool, Union[Dict, str]]:
        """Pobiera pojedynczą stronę."""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            time.sleep(0.5)  # Rate limiting
            
            return True, {
                'content': response.text,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'url': url,
                'size': len(response.text),
                'is_html': self._is_html_content(response)  # Dodaj tę informację
            }
        except requests.RequestException as e:
            return False, handle_network_error(url, e)
        except Exception as e:
            return False, f"Błąd pobierania {url}: {str(e)}"

    def _find_new_links(self, page_data: Dict, current_url: str, base_domain: str) -> List[str]:
        """Znajduje nowe linki w HTML."""
        try:
            # Sprawdź czy to HTML na podstawie nagłówków
            if not page_data.get('is_html', False):
                return []
            
            soup = BeautifulSoup(page_data['content'], 'html.parser')
            return self._extract_links(soup, current_url, base_domain)
        except Exception:
            return []
    
    def _is_valid_url(self, url: str) -> bool:
        """Sprawdza czy URL jest poprawny."""
        try:
            result = urlparse(url)
            return bool(result.scheme and result.netloc)
        except Exception:
            return False
    
    def _is_html_content(self, response) -> bool:
        """Sprawdza czy odpowiedź zawiera HTML."""
        content_type = response.headers.get('content-type', '').lower()
        return 'text/html' in content_type
    
    def _extract_links(self, soup: BeautifulSoup, current_url: str, base_domain: str) -> List[str]:
        """Wyciąga linki z HTML tylko z tej samej domeny i ścieżki bazowej."""
        links = []
        for link in soup.find_all('a', href=True):
            href_attr = link.get('href') # type: ignore
            if not href_attr:
                continue
            href = str(href_attr).strip()
            if not href or href.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                continue
                
            full_url = urljoin(current_url, href)
            parsed = urlparse(full_url)
            
            # Tylko linki z tej samej domeny
            if parsed.netloc == base_domain:
                # Sprawdź ograniczenie ścieżki bazowej
                if self.base_path:
                    # Sprawdź czy link jest w obrębie ścieżki bazowej
                    if not (parsed.path == self.base_path or parsed.path.startswith(self.base_path + "/")):
                        continue  # pomiń linki spoza ścieżki bazowej
                
                # Usuń fragment z URL
                clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                if parsed.query:
                    clean_url += f"?{parsed.query}"
                links.append(clean_url)
                
        return list(set(links))  # Usuń duplikaty
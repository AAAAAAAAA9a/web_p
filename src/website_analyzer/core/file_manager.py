"""
Narzędzia do zarządzania plikami - zapisywanie i wczytywanie danych stron internetowych.
"""

import os
import json
from typing import Dict, Optional

from .error_handler import handle_file_error, safe_execute


class FileManager:
    """Obsługuje zapisywanie i wczytywanie danych stron internetowych."""
    
    def __init__(self):
        """Inicjalizuje menedżer plików."""
        self.default_encoding = 'utf-8'
        
    def save_website_data(self, downloaded_pages: Dict[str, Dict], folder_path: str) -> bool:
        """
        Zapisuje pobrane dane strony internetowej na dysk.
        
        Args:
            downloaded_pages: Słownik z danymi stron do zapisania
            folder_path: Ścieżka do katalogu zapisu plików
            
        Returns:
            True jeśli operacja się powiodła, False w przeciwnym razie
        """
        success, _ = safe_execute(self._do_save_website_data, downloaded_pages, folder_path)
        return success
    
    def _do_save_website_data(self, downloaded_pages: Dict[str, Dict], folder_path: str):
        """Wykonuje faktyczne zapisywanie danych."""
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        # Zapisz poszczególne strony
        for i, (url, page_data) in enumerate(downloaded_pages.items()):
            filename = f"page_{i+1:03d}.html"
            filepath = os.path.join(folder_path, filename)
            
            with open(filepath, 'w', encoding=self.default_encoding) as f:
                f.write(f"<!-- URL: {url} -->\n")
                f.write(f"<!-- Status: {page_data['status_code']} -->\n")
                f.write(f"<!-- Size: {page_data['size']} bytes -->\n")
                f.write(page_data['content'])
                
        # Zapisz plik indeksu i metadane
        self._save_index_file(downloaded_pages, folder_path)
        self._save_metadata(downloaded_pages, folder_path)
            
    def _save_index_file(self, downloaded_pages: Dict[str, Dict], folder_path: str):
        """Zapisuje plik indeksu mapujący nazwy plików na URL."""
        index_path = os.path.join(folder_path, "index.txt")
        with open(index_path, 'w', encoding=self.default_encoding) as f:
            f.write("INDEKS POBRANYCH STRON / DOWNLOADED PAGES INDEX\n")
            f.write("="*60 + "\n\n")
            for i, (url, page_data) in enumerate(downloaded_pages.items(), 1):
                f.write(f"page_{i:03d}.html - {url} - {page_data['status_code']} - {page_data['size']} bytes\n")
                
    def _save_metadata(self, downloaded_pages: Dict[str, Dict], folder_path: str):
        """Zapisuje metadane jako JSON do programowego dostępu."""
        metadata = {
            'total_pages': len(downloaded_pages),
            'total_size': sum(page['size'] for page in downloaded_pages.values()),
            'pages': {}
        }
        
        for i, (url, page_data) in enumerate(downloaded_pages.items(), 1):
            filename = f"page_{i:03d}.html"
            metadata['pages'][filename] = {
                'url': url,
                'status_code': page_data['status_code'],
                'size': page_data['size'],
                'headers': page_data['headers']
            }
            
        metadata_path = os.path.join(folder_path, "metadata.json")
        with open(metadata_path, 'w', encoding=self.default_encoding) as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
            
    def save_analysis_report(self, analysis_data: Dict[str, str], filepath: str) -> bool:
        """
        Zapisuje raport analizy do pliku tekstowego.
        
        Args:
            analysis_data: Słownik zawierający wyniki analizy
            filepath: Ścieżka do zapisania raportu
            
        Returns:
            True jeśli operacja się powiodła, False w przeciwnym razie
        """
        success, _ = safe_execute(self._write_report, analysis_data, filepath)
        return success
    
    def _write_report(self, analysis_data: Dict[str, str], filepath: str):
        """Zapisuje raport do pliku."""
        with open(filepath, 'w', encoding=self.default_encoding) as f:
            f.write("RAPORT ANALIZY WITRYNY / WEBSITE ANALYSIS REPORT\n")
            f.write("="*60 + "\n\n")
            
            for section in ['stats', 'links', 'images', 'media', 'resources', 'documents']:
                if section in analysis_data:
                    if section != 'stats':
                        f.write("\n\n")
                    f.write(analysis_data[section])
            
    def load_website_data(self, folder_path: str) -> Optional[Dict[str, Dict]]:
        """
        Wczytuje wcześniej zapisane dane strony internetowej.
        
        Args:
            folder_path: Katalog zawierający zapisane dane strony
            
        Returns:
            Słownik z wczytanymi danymi stron lub None jeśli operacja się nie powiodła
        """
        success, result = safe_execute(self._do_load_website_data, folder_path)
        return result if success else None
    
    def _do_load_website_data(self, folder_path: str) -> Dict[str, Dict]:
        """Wykonuje faktyczne wczytywanie danych."""
        metadata_path = os.path.join(folder_path, "metadata.json")
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Brak pliku metadanych: {metadata_path}")
            
        with open(metadata_path, 'r', encoding=self.default_encoding) as f:
            metadata = json.load(f)
            
        downloaded_pages = {}
        
        for filename, page_info in metadata['pages'].items():
            filepath = os.path.join(folder_path, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding=self.default_encoding) as f:
                    content = f.read()
                    lines = content.split('\n')
                    content = '\n'.join(lines[3:])
                    
                downloaded_pages[page_info['url']] = {
                    'content': content,
                    'status_code': page_info['status_code'],
                    'headers': page_info['headers'],
                    'url': page_info['url'],
                    'size': page_info['size']
                }
                
        return downloaded_pages
"""
Główne okno aplikacji.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import Dict, Optional

from ..core.downloader import WebsiteDownloader
from ..core.analyzer import WebsiteAnalyzer
from ..core.file_manager import FileManager
from ..core.error_handler import set_global_logger, handle_error
from .download_tab import DownloadTab
from .analysis_tab import AnalysisTab
from .browse_tab import BrowseTab


class MainWindow:
    """Główne okno aplikacji zawierające wszystkie zakładki i funkcjonalności."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Website Analyzer - Analizator Witryn WWW")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)
        
        # Skonfiguruj obsługę błędów
        set_global_logger(self._log_message)
        
        # Skonfiguruj nowoczesny motyw
        self.setup_theme()
        
        # Główne komponenty
        self.downloader = WebsiteDownloader()
        self.analyzer = WebsiteAnalyzer()
        self.file_manager = FileManager()
        
        # Przechowywanie danych
        self.downloaded_pages: Dict[str, Dict] = {}
        self.current_analysis: Dict[str, str] = {}
        
        self.setup_ui()
        
    def setup_theme(self):
        """Konfiguruje GUI."""
        style = ttk.Style()
        
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'alt' in available_themes:
            style.theme_use('alt')
            
        style.configure('TNotebook', borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 10])

        # Konfiguracja przycisków
        style.configure('Accent.TButton',
                       foreground='white',
                       background='#0078d4',
                       borderwidth=0,
                       focuscolor='none')
        style.map('Accent.TButton',
                 background=[('active', '#106ebe')])
        
    def setup_ui(self):
        """Konfiguruje główny interfejs użytkownika."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Utwórz zakładki
        self.download_tab = DownloadTab(self.notebook, self)
        self.analysis_tab = AnalysisTab(self.notebook, self)
        self.browse_tab = BrowseTab(self.notebook, self)
          # Dodaj zakładki do notebooka
        self.notebook.add(self.download_tab.frame, text="🌐 Pobieranie")
        self.notebook.add(self.analysis_tab.frame, text="📊 Analiza")
        self.notebook.add(self.browse_tab.frame, text="📖 Przeglądanie")
        
    def start_download(self, url: str, max_depth: int, max_pages: int):
        """
        Rozpoczyna pobieranie strony internetowej w osobnym wątku.
        
        Args:
            url: URL do rozpoczęcia pobierania
            max_depth: Maksymalna głębokość przeszukiwania
            max_pages: Maksymalna liczba stron do pobrania
        """
        if not url:
            messagebox.showerror("Błąd", "Proszę podać URL witryny")
            return
            
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        # Zaktualizuj ustawienia downloadera
        self.downloader.max_pages = max_pages
        self.downloader.max_depth = max_depth
        
        # Rozpocznij pobieranie w osobnym wątku
        thread = threading.Thread(
            target=self._download_worker, 
            args=(url,)
        )
        thread.daemon = True
        thread.start()
        
    def _download_worker(self, url: str):
        """Metoda robocza do pobierania w osobnym wątku."""
        self.download_tab.set_downloading(True)
        
        try:
            self.downloaded_pages = self.downloader.download_website(
                url, self._log_message
            )
            self.root.after(0, self._download_completed)
        except Exception as e:
            error_msg = handle_error("pobierania", e)
            self.root.after(0, lambda: self.download_tab.set_downloading(False))
            
    def _download_completed(self):
        """Wywoływana gdy pobieranie zostało zakończone."""
        self.download_tab.set_downloading(False)
        self.browse_tab.update_page_list(list(self.downloaded_pages.keys()))
        
    def analyze_website(self):
        """Analizuje pobrane dane strony internetowej."""
        if not self.downloaded_pages:
            messagebox.showwarning("Brak danych", "Najpierw pobierz witrynę")
            return
            
        # Rozpocznij analizę w osobnym wątku
        thread = threading.Thread(target=self._analysis_worker)
        thread.daemon = True
        thread.start()
        
    def _analysis_worker(self):
        """Metoda robocza do analizy w osobnym wątku."""
        self.root.after(0, lambda: self.analysis_tab.set_analyzing(True))
        self._log_message("Rozpoczynam analizę witryny...")
        
        try:
            self.current_analysis = self.analyzer.analyze_pages(
                self.downloaded_pages, self._log_message
            )
            self.root.after(0, self._analysis_completed)
        except Exception as e:
            handle_error("analizy", e, show_gui=True)
            self.root.after(0, lambda: self.analysis_tab.set_analyzing(False))
            
    def _analysis_completed(self):
        """Wywoływana gdy analiza została zakończona."""
        self.analysis_tab.set_analyzing(False)
        self.analysis_tab.display_analysis(self.current_analysis)
        self.download_tab.log_message("Analiza zakończona!")
            
    def save_website(self, folder_path: str) -> bool:
        """
        Zapisuje pobrane dane strony internetowej na dysk.
        
        Args:
            folder_path: Katalog do zapisania danych
            
        Returns:
            True jeśli operacja się powiodła, False w przeciwnym razie
        """
        if not self.downloaded_pages:
            messagebox.showwarning("Brak danych", "Najpierw pobierz witrynę")
            return False
            
        return self.file_manager.save_website_data(self.downloaded_pages, folder_path)
        
    def save_analysis_report(self, filepath: str) -> bool:
        """
        Zapisuje raport analizy do pliku.
        
        Args:
            filepath: Ścieżka do zapisania raportu
            
        Returns:
            True jeśli operacja się powiodła, False w przeciwnym razie
        """
        if not self.current_analysis:
            messagebox.showwarning("Brak analizy", "Najpierw wykonaj analizę witryny")
            return False
            
        return self.file_manager.save_analysis_report(self.current_analysis, filepath)
        
    def load_website(self, folder_path: str) -> bool:
        """
        Wczytuje wcześniej zapisane dane strony internetowej.
        
        Args:
            folder_path: Katalog zawierający zapisane dane
            
        Returns:
            True jeśli operacja się powiodła, False w przeciwnym razie
        """
        loaded_data = self.file_manager.load_website_data(folder_path)
        if loaded_data:
            self.downloaded_pages = loaded_data
            self.browse_tab.update_page_list(list(self.downloaded_pages.keys()))
            self.download_tab.log_message(f"Załadowano {len(loaded_data)} stron z dysku")
            return True
        return False
        
    def get_page_content(self, url: str) -> Optional[str]:
        """
        Pobiera zawartość konkretnej strony.
        
        Args:
            url: URL strony
            
        Returns:
            Zawartość strony lub None jeśli nie znaleziono
        """
        if url in self.downloaded_pages:
            return self.downloaded_pages[url]['content']
        return None
    
    def _log_message(self, message: str):
        """Centralny punkt logowania wiadomości."""
        # Bezpiecznie wywołaj w głównym wątku
        if threading.current_thread() == threading.main_thread():
            self.download_tab.log_message(message)
        else:
            self.root.after(0, lambda: self.download_tab.log_message(message))
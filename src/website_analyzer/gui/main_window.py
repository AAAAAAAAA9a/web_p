"""
Main application window.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import Dict, Optional

from ..core.downloader import WebsiteDownloader
from ..core.analyzer import WebsiteAnalyzer
from ..core.file_manager import FileManager
from .download_tab import DownloadTab
from .analysis_tab import AnalysisTab
from .browse_tab import BrowseTab


class MainWindow:
    """Main application window containing all tabs and functionality."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Website Analyzer - Analizator Witryn WWW")
        self.root.geometry("1000x700")
        
        # Core components
        self.downloader = WebsiteDownloader()
        self.analyzer = WebsiteAnalyzer()
        self.file_manager = FileManager()
        
        # Data storage
        self.downloaded_pages: Dict[str, Dict] = {}
        self.current_analysis: Dict[str, str] = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the main user interface."""
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.download_tab = DownloadTab(self.notebook, self)
        self.analysis_tab = AnalysisTab(self.notebook, self)
        self.browse_tab = BrowseTab(self.notebook, self)
        
        # Add tabs to notebook
        self.notebook.add(self.download_tab.frame, text="Pobieranie / Download")
        self.notebook.add(self.analysis_tab.frame, text="Analiza / Analysis")
        self.notebook.add(self.browse_tab.frame, text="Przeglądanie / Browse")
        
    def start_download(self, url: str, max_depth: int, max_pages: int):
        """
        Start downloading a website in a separate thread.
        
        Args:
            url: URL to start downloading from
            max_depth: Maximum depth to crawl
            max_pages: Maximum number of pages to download
        """
        if not url:
            messagebox.showerror("Błąd", "Proszę podać URL witryny")
            return
            
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        # Update downloader settings
        self.downloader.max_pages = max_pages
        self.downloader.max_depth = max_depth
        
        # Start download in separate thread
        thread = threading.Thread(
            target=self._download_worker, 
            args=(url,)
        )
        thread.daemon = True
        thread.start()
        
    def _download_worker(self, url: str):
        """Worker method for downloading in separate thread."""
        try:
            self.download_tab.set_downloading(True)
            
            def progress_callback(message: str):
                self.download_tab.log_message(message)
                
            self.downloaded_pages = self.downloader.download_website(
                url, progress_callback
            )
            
            # Update UI on main thread
            self.root.after(0, self._download_completed)
            
        except Exception as e:
            error_msg = f"Błąd podczas pobierania: {str(e)}"
            self.root.after(0, lambda: self.download_tab.log_message(error_msg))
            self.root.after(0, lambda: self.download_tab.set_downloading(False))
            
    def _download_completed(self):
        """Called when download is completed."""
        self.download_tab.set_downloading(False)
        self.browse_tab.update_page_list(list(self.downloaded_pages.keys()))
        
    def analyze_website(self):
        """Analyze the downloaded website data."""
        if not self.downloaded_pages:
            messagebox.showwarning("Brak danych", "Najpierw pobierz witrynę")
            return
            
        try:
            self.download_tab.log_message("Rozpoczynam analizę witryny...")
            
            self.current_analysis = self.analyzer.analyze_pages(self.downloaded_pages)
            self.analysis_tab.display_analysis(self.current_analysis)
            
            self.download_tab.log_message("Analiza zakończona!")
            
        except Exception as e:
            error_msg = f"Błąd podczas analizy: {str(e)}"
            messagebox.showerror("Błąd", error_msg)
            self.download_tab.log_message(error_msg)
            
    def save_website(self, folder_path: str) -> bool:
        """
        Save downloaded website data to disk.
        
        Args:
            folder_path: Directory to save the data
            
        Returns:
            True if successful, False otherwise
        """
        if not self.downloaded_pages:
            messagebox.showwarning("Brak danych", "Najpierw pobierz witrynę")
            return False
            
        return self.file_manager.save_website_data(self.downloaded_pages, folder_path)
        
    def save_analysis_report(self, filepath: str) -> bool:
        """
        Save analysis report to file.
        
        Args:
            filepath: Path to save the report
            
        Returns:
            True if successful, False otherwise
        """
        if not self.current_analysis:
            messagebox.showwarning("Brak analizy", "Najpierw wykonaj analizę witryny")
            return False
            
        return self.file_manager.save_analysis_report(self.current_analysis, filepath)
        
    def load_website(self, folder_path: str) -> bool:
        """
        Load previously saved website data.
        
        Args:
            folder_path: Directory containing saved data
            
        Returns:
            True if successful, False otherwise
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
        Get content of a specific page.
        
        Args:
            url: URL of the page
            
        Returns:
            Page content or None if not found
        """
        if url in self.downloaded_pages:
            return self.downloaded_pages[url]['content']
        return None
"""
Browse tab GUI component.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .main_window import MainWindow


class BrowseTab:
    """GUI tab for browsing downloaded pages."""
    
    def __init__(self, parent: ttk.Notebook, main_window: 'MainWindow'):
        self.parent = parent
        self.main_window = main_window
        self.frame = ttk.Frame(parent)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the browse tab UI."""
        # Page selector
        selector_frame = ttk.Frame(self.frame)
        selector_frame.pack(fill='x', pady=5)
        
        ttk.Label(selector_frame, text="Wybierz stronę:").pack(side='left')
        self.page_combo = ttk.Combobox(selector_frame, state='readonly')
        self.page_combo.pack(side='left', fill='x', expand=True, padx=5)
        self.page_combo.bind('<<ComboboxSelected>>', self.show_page)
        
        # View options
        options_frame = ttk.Frame(self.frame)
        options_frame.pack(fill='x', pady=5)
        
        self.view_mode = tk.StringVar(value="source")
        ttk.Radiobutton(options_frame, text="Kod źródłowy", 
                       variable=self.view_mode, value="source",
                       command=self.update_view).pack(side='left')
        ttk.Radiobutton(options_frame, text="Tekst", 
                       variable=self.view_mode, value="text",
                       command=self.update_view).pack(side='left', padx=10)
        
        # Page content viewer
        viewer_frame = ttk.Frame(self.frame)
        viewer_frame.pack(fill='both', expand=True, pady=5)
        
        # Add scrollbars
        self.page_viewer = scrolledtext.ScrolledText(viewer_frame, wrap=tk.WORD)
        self.page_viewer.pack(fill='both', expand=True)
        
        # Status bar
        self.status_frame = ttk.Frame(self.frame)
        self.status_frame.pack(fill='x', pady=2)
        
        self.status_label = ttk.Label(self.status_frame, text="Brak załadowanych stron")
        self.status_label.pack(side='left')
        
    def update_page_list(self, urls: List[str]):
        """
        Update the list of available pages.
        
        Args:
            urls: List of URLs to display
        """
        self.page_combo['values'] = urls
        if urls:
            self.page_combo.current(0)
            self.show_page()
            self.status_label.config(text=f"Załadowano {len(urls)} stron")
        else:
            self.page_combo.set('')
            self.page_viewer.delete(1.0, tk.END)
            self.status_label.config(text="Brak załadowanych stron")
            
    def show_page(self, event=None):
        """Display the selected page."""
        selected_url = self.page_combo.get()
        if not selected_url:
            return
            
        content = self.main_window.get_page_content(selected_url)
        if content is None:
            self.page_viewer.delete(1.0, tk.END)
            self.page_viewer.insert(1.0, "Błąd: Nie można załadować zawartości strony")
            return
            
        self.display_content(content)
        
    def display_content(self, content: str):
        """
        Display content in the viewer based on current view mode.
        
        Args:
            content: Content to display
        """
        self.page_viewer.delete(1.0, tk.END)
        
        if self.view_mode.get() == "source":
            # Show HTML source code
            self.page_viewer.insert(1.0, content)
        else:
            # Show extracted text
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                text_content = soup.get_text(separator='\n', strip=True)
                self.page_viewer.insert(1.0, text_content)
            except ImportError:
                self.page_viewer.insert(1.0, "Błąd: Nie można wyświetlić tekstu (brak biblioteki BeautifulSoup)")
            except Exception as e:
                self.page_viewer.insert(1.0, f"Błąd podczas przetwarzania tekstu: {str(e)}")
                
    def update_view(self):
        """Update the view when view mode changes."""
        self.show_page()
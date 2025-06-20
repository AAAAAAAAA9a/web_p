"""
Komponent GUI zakładki pobierania.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .main_window import MainWindow


class DownloadTab:
    """Zakładka GUI do pobierania stron internetowych."""
    
    def __init__(self, parent: ttk.Notebook, main_window: 'MainWindow'):
        self.parent = parent
        self.main_window = main_window
        self.frame = ttk.Frame(parent)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Konfiguruje interfejs zakładki pobierania."""
        # Główny kontener z paddingiem
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill='both', expand=True, padx=20, pady=15)
          # Sekcja wprowadzania URL
        url_section = ttk.LabelFrame(main_container, text="URL Witryny", padding=15)
        url_section.pack(fill='x', pady=(0, 15))
        
        url_frame = ttk.Frame(url_section)
        url_frame.pack(fill='x')
        
        ttk.Label(url_frame, text="URL:").pack(side='left')
        self.url_entry = ttk.Entry(url_frame, width=50, font=('', 10))
        self.url_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
          # Sekcja opcji pobierania
        options_section = ttk.LabelFrame(main_container, text="Ustawienia Pobierania", padding=15)
        options_section.pack(fill='x', pady=(0, 15))
        
        options_grid = ttk.Frame(options_section)
        options_grid.pack(fill='x')
        
        # Lewa kolumna
        left_col = ttk.Frame(options_grid)
        left_col.pack(side='left', fill='x', expand=True)
        
        self.download_depth = tk.IntVar(value=2)
        ttk.Label(left_col, text="Crawl Depth:").pack(anchor='w')
        depth_frame = ttk.Frame(left_col)
        depth_frame.pack(fill='x', pady=(5, 0))
        ttk.Spinbox(depth_frame, from_=1, to=5, width=10, 
                   textvariable=self.download_depth).pack(side='left')
        ttk.Label(depth_frame, text="levels", foreground='gray').pack(side='left', padx=(5, 0))
        
        # Prawa kolumna
        right_col = ttk.Frame(options_grid)
        right_col.pack(side='left', fill='x', expand=True, padx=(30, 0))
        
        self.max_pages = tk.IntVar(value=50)
        ttk.Label(right_col, text="Max Pages:").pack(anchor='w')
        pages_frame = ttk.Frame(right_col)
        pages_frame.pack(fill='x', pady=(5, 0))
        ttk.Spinbox(pages_frame, from_=1, to=500, width=10, 
                   textvariable=self.max_pages).pack(side='left')
        ttk.Label(pages_frame, text="pages", foreground='gray').pack(side='left', padx=(5, 0))
        
        # Sekcja przycisków akcji
        actions_section = ttk.LabelFrame(main_container, text="Actions", padding=15)
        actions_section.pack(fill='x', pady=(0, 15))
        
        button_frame = ttk.Frame(actions_section)
        button_frame.pack(fill='x')
        
        self.download_btn = ttk.Button(button_frame, text="🌐 Download Website", 
                                     command=self.start_download, style='Accent.TButton')
        self.download_btn.pack(side='left', padx=(0, 10))
        
        self.save_btn = ttk.Button(button_frame, text="💾 Save to Disk", 
                                 command=self.save_website)
        self.save_btn.pack(side='left', padx=5)
        
        self.load_btn = ttk.Button(button_frame, text="📁 Load from Disk", 
                                 command=self.load_website)
        self.load_btn.pack(side='left', padx=5)
        
        # Pasek postępu
        self.progress = ttk.Progressbar(button_frame, mode='indeterminate', length=200)
        self.progress.pack(side='right')
        
        # Sekcja dziennika statusu
        log_section = ttk.LabelFrame(main_container, text="Download Log", padding=10)
        log_section.pack(fill='both', expand=True)
        
        self.status_text = scrolledtext.ScrolledText(log_section, height=12, 
                                                   font=('Consolas', 9), wrap=tk.WORD)
        self.status_text.pack(fill='both', expand=True)
        
    def start_download(self):
        """Rozpoczyna pobieranie strony internetowej."""
        url = self.url_entry.get().strip()
        depth = self.download_depth.get()
        max_pages = self.max_pages.get()
        
        self.main_window.start_download(url, depth, max_pages)
        
    def set_downloading(self, is_downloading: bool):
        """
        Aktualizuje stan UI na podstawie statusu pobierania.
        
        Args:
            is_downloading: True jeśli obecnie pobiera, False w przeciwnym razie
        """
        if is_downloading:
            self.download_btn.config(state='disabled')
            self.progress.start()
        else:
            self.download_btn.config(state='normal')
            self.progress.stop()
            
    def log_message(self, message: str):
        """
        Dodaje wiadomość do dziennika statusu.
        
        Args:
            message: Wiadomość do zapisania
        """
        timestamp = time.strftime('%H:%M:%S')
        self.status_text.insert(tk.END, f"{timestamp} - {message}\n")
        self.status_text.see(tk.END)
        self.status_text.update_idletasks()
        
    def save_website(self):
        """Zapisuje pobraną stronę na dysk."""
        folder = filedialog.askdirectory(title="Wybierz folder do zapisania")
        if not folder:
            return
            
        if self.main_window.save_website(folder):
            messagebox.showinfo("Sukces", f"Witryna zapisana w folderze: {folder}")
        else:
            messagebox.showerror("Błąd", "Błąd podczas zapisywania witryny")
            
    def load_website(self):
        """Wczytuje wcześniej zapisaną stronę z dysku."""
        folder = filedialog.askdirectory(title="Wybierz folder z zapisaną witryną")
        if not folder:
            return
            
        if self.main_window.load_website(folder):
            messagebox.showinfo("Sukces", "Witryna została wczytana z dysku")
        else:
            messagebox.showerror("Błąd", "Nie można wczytać witryny z wybranego folderu")
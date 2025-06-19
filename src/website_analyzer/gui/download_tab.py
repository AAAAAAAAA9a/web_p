"""
Download tab GUI component.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .main_window import MainWindow


class DownloadTab:
    """GUI tab for downloading websites."""
    
    def __init__(self, parent: ttk.Notebook, main_window: 'MainWindow'):
        self.parent = parent
        self.main_window = main_window
        self.frame = ttk.Frame(parent)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the download tab UI."""
        # URL input
        url_frame = ttk.Frame(self.frame)
        url_frame.pack(fill='x', pady=5)
        
        ttk.Label(url_frame, text="URL witryny:").pack(side='left')
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        # Download options
        options_frame = ttk.Frame(self.frame)
        options_frame.pack(fill='x', pady=5)
        
        self.download_depth = tk.IntVar(value=2)
        ttk.Label(options_frame, text="Głębokość pobierania:").pack(side='left')
        ttk.Spinbox(options_frame, from_=1, to=5, width=5, 
                   textvariable=self.download_depth).pack(side='left', padx=5)
        
        self.max_pages = tk.IntVar(value=50)
        ttk.Label(options_frame, text="Max stron:").pack(side='left', padx=(20,0))
        ttk.Spinbox(options_frame, from_=1, to=500, width=8, 
                   textvariable=self.max_pages).pack(side='left', padx=5)
        
        # Buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill='x', pady=10)
        
        self.download_btn = ttk.Button(button_frame, text="Pobierz witrynę", 
                                     command=self.start_download)
        self.download_btn.pack(side='left')
        
        self.save_btn = ttk.Button(button_frame, text="Zapisz na dysk", 
                                 command=self.save_website)
        self.save_btn.pack(side='left', padx=10)
        
        self.load_btn = ttk.Button(button_frame, text="Wczytaj z dysku", 
                                 command=self.load_website)
        self.load_btn.pack(side='left', padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=5)
        
        # Status text
        self.status_text = scrolledtext.ScrolledText(self.frame, height=15)
        self.status_text.pack(fill='both', expand=True, pady=5)
        
    def start_download(self):
        """Start downloading the website."""
        url = self.url_entry.get().strip()
        depth = self.download_depth.get()
        max_pages = self.max_pages.get()
        
        self.main_window.start_download(url, depth, max_pages)
        
    def set_downloading(self, is_downloading: bool):
        """
        Update UI state based on downloading status.
        
        Args:
            is_downloading: True if currently downloading, False otherwise
        """
        if is_downloading:
            self.download_btn.config(state='disabled')
            self.progress.start()
        else:
            self.download_btn.config(state='normal')
            self.progress.stop()
            
    def log_message(self, message: str):
        """
        Add a message to the status log.
        
        Args:
            message: Message to log
        """
        timestamp = time.strftime('%H:%M:%S')
        self.status_text.insert(tk.END, f"{timestamp} - {message}\n")
        self.status_text.see(tk.END)
        self.status_text.update_idletasks()
        
    def save_website(self):
        """Save downloaded website to disk."""
        folder = filedialog.askdirectory(title="Wybierz folder do zapisania")
        if not folder:
            return
            
        if self.main_window.save_website(folder):
            messagebox.showinfo("Sukces", f"Witryna zapisana w folderze: {folder}")
        else:
            messagebox.showerror("Błąd", "Błąd podczas zapisywania witryny")
            
    def load_website(self):
        """Load previously saved website from disk."""
        folder = filedialog.askdirectory(title="Wybierz folder z zapisaną witryną")
        if not folder:
            return
            
        if self.main_window.load_website(folder):
            messagebox.showinfo("Sukces", "Witryna została wczytana z dysku")
        else:
            messagebox.showerror("Błąd", "Nie można wczytać witryny z wybranego folderu")
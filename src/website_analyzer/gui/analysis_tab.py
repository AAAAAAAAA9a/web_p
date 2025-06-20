"""
Komponent GUI zakładki analizy.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .main_window import MainWindow


class AnalysisTab:
    """Zakładka GUI do analizowania stron internetowych."""
    
    def __init__(self, parent: ttk.Notebook, main_window: 'MainWindow'):
        self.parent = parent
        self.main_window = main_window
        self.frame = ttk.Frame(parent)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Konfiguruje interfejs zakładki analizy."""
        # Główny kontener z paddingiem
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Sekcja kontroli analizy
        control_section = ttk.LabelFrame(main_container, text="Analysis Controls", padding=15)
        control_section.pack(fill='x', pady=(0, 15))
        
        control_frame = ttk.Frame(control_section)
        control_frame.pack(fill='x')
        
        self.analyze_btn = ttk.Button(control_frame, text="🔍 Analyze Website", 
                                    command=self.analyze_website, style='Accent.TButton')
        self.analyze_btn.pack(side='left', padx=(0, 10))
        
        ttk.Button(control_frame, text="📊 Export Report", 
                  command=self.export_report).pack(side='left', padx=5)
        
        # Pasek postępu dla analizy
        self.analysis_progress = ttk.Progressbar(control_frame, mode='indeterminate', length=200)
        self.analysis_progress.pack(side='right')
        
        # Sekcja wyników analizy
        results_section = ttk.LabelFrame(main_container, text="Analysis Results", padding=10)
        results_section.pack(fill='both', expand=True)
        
        # Notebook wyników analizy
        self.analysis_notebook = ttk.Notebook(results_section)
        self.analysis_notebook.pack(fill='both', expand=True)
        
        # Zakładka statystyk
        stats_frame = ttk.Frame(self.analysis_notebook)
        self.analysis_notebook.add(stats_frame, text="📈 Statistics")
        stats_container = ttk.Frame(stats_frame)
        stats_container.pack(fill='both', expand=True, padx=10, pady=10)
        self.stats_text = scrolledtext.ScrolledText(stats_container, wrap=tk.WORD, 
                                                   font=('Courier', 9))
        self.stats_text.pack(fill='both', expand=True)
        
        # Zakładka linków
        links_frame = ttk.Frame(self.analysis_notebook)
        self.analysis_notebook.add(links_frame, text="🔗 Links")
        links_container = ttk.Frame(links_frame)
        links_container.pack(fill='both', expand=True, padx=10, pady=10)
        self.links_text = scrolledtext.ScrolledText(links_container, wrap=tk.WORD, 
                                                   font=('Courier', 9))
        self.links_text.pack(fill='both', expand=True)
          # Zakładka obrazów
        images_frame = ttk.Frame(self.analysis_notebook)
        self.analysis_notebook.add(images_frame, text="🖼️ Images")
        images_container = ttk.Frame(images_frame)
        images_container.pack(fill='both', expand=True, padx=10, pady=10)
        self.images_text = scrolledtext.ScrolledText(images_container, wrap=tk.WORD, 
                                                    font=('Courier', 9))
        self.images_text.pack(fill='both', expand=True)
        
        # Zakładka mediów (video/audio)
        media_frame = ttk.Frame(self.analysis_notebook)
        self.analysis_notebook.add(media_frame, text="🎬 Media")
        media_container = ttk.Frame(media_frame)
        media_container.pack(fill='both', expand=True, padx=10, pady=10)
        self.media_text = scrolledtext.ScrolledText(media_container, wrap=tk.WORD, 
                                                   font=('Courier', 9))
        self.media_text.pack(fill='both', expand=True)
        
        # Zakładka zasobów (CSS/JS)
        resources_frame = ttk.Frame(self.analysis_notebook)
        self.analysis_notebook.add(resources_frame, text="⚙️ Resources")
        resources_container = ttk.Frame(resources_frame)
        resources_container.pack(fill='both', expand=True, padx=10, pady=10)
        self.resources_text = scrolledtext.ScrolledText(resources_container, wrap=tk.WORD, 
                                                       font=('Courier', 9))
        self.resources_text.pack(fill='both', expand=True)
        
        # Zakładka dokumentów
        documents_frame = ttk.Frame(self.analysis_notebook)
        self.analysis_notebook.add(documents_frame, text="📄 Documents")
        documents_container = ttk.Frame(documents_frame)
        documents_container.pack(fill='both', expand=True, padx=10, pady=10)
        self.documents_text = scrolledtext.ScrolledText(documents_container, wrap=tk.WORD, 
                                                       font=('Courier', 9))
        self.documents_text.pack(fill='both', expand=True)
        
    def analyze_website(self):
        """Uruchamia analizę strony internetowej."""
        self.main_window.analyze_website()
        
    def display_analysis(self, analysis_data: Dict[str, str]):
        """
        Wyświetla wyniki analizy w zakładkach.
        
        Args:
            analysis_data: Słownik zawierający wyniki analizy
        """        # Wyczyść istniejącą zawartość
        self.stats_text.delete(1.0, tk.END)
        self.links_text.delete(1.0, tk.END)
        self.images_text.delete(1.0, tk.END)
        self.media_text.delete(1.0, tk.END)
        self.resources_text.delete(1.0, tk.END)
        self.documents_text.delete(1.0, tk.END)
        
        # Wyświetl nową zawartość
        if 'stats' in analysis_data:
            self.stats_text.insert(1.0, analysis_data['stats'])
            
        if 'links' in analysis_data:
            self.links_text.insert(1.0, analysis_data['links'])
            
        if 'images' in analysis_data:
            self.images_text.insert(1.0, analysis_data['images'])
            
        if 'media' in analysis_data:
            self.media_text.insert(1.0, analysis_data['media'])
            
        if 'resources' in analysis_data:
            self.resources_text.insert(1.0, analysis_data['resources'])
            
        if 'documents' in analysis_data:
            self.documents_text.insert(1.0, analysis_data['documents'])
            
    def set_analyzing(self, is_analyzing: bool):
        """
        Aktualizuje stan UI na podstawie statusu analizowania.
        
        Args:
            is_analyzing: True jeśli obecnie analizuje, False w przeciwnym razie
        """
        if is_analyzing:
            self.analyze_btn.config(state='disabled')
            self.analysis_progress.start()
        else:
            self.analyze_btn.config(state='normal')
            self.analysis_progress.stop()
            
    def export_report(self):
        """Eksportuje raport analizy do pliku."""
        filename = filedialog.asksaveasfilename(
            title="Zapisz raport",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            if self.main_window.save_analysis_report(filename):
                messagebox.showinfo("Sukces", f"Raport zapisany: {filename}")
            else:
                messagebox.showerror("Błąd", "Błąd podczas zapisywania raportu")
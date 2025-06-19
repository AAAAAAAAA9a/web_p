"""
Analysis tab GUI component.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .main_window import MainWindow


class AnalysisTab:
    """GUI tab for analyzing websites."""
    
    def __init__(self, parent: ttk.Notebook, main_window: 'MainWindow'):
        self.parent = parent
        self.main_window = main_window
        self.frame = ttk.Frame(parent)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the analysis tab UI."""
        # Analysis controls
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill='x', pady=5)
        
        ttk.Button(control_frame, text="Analizuj pobraną witrynę", 
                  command=self.analyze_website).pack(side='left')
        ttk.Button(control_frame, text="Eksportuj raport", 
                  command=self.export_report).pack(side='left', padx=10)
        
        # Analysis results notebook
        self.analysis_notebook = ttk.Notebook(self.frame)
        self.analysis_notebook.pack(fill='both', expand=True, pady=5)
        
        # Statistics tab
        stats_frame = ttk.Frame(self.analysis_notebook)
        self.analysis_notebook.add(stats_frame, text="Statystyki")
        self.stats_text = scrolledtext.ScrolledText(stats_frame, wrap=tk.WORD)
        self.stats_text.pack(fill='both', expand=True)
        
        # Links tab
        links_frame = ttk.Frame(self.analysis_notebook)
        self.analysis_notebook.add(links_frame, text="Linki")
        self.links_text = scrolledtext.ScrolledText(links_frame, wrap=tk.WORD)
        self.links_text.pack(fill='both', expand=True)
        
        # Images tab
        images_frame = ttk.Frame(self.analysis_notebook)
        self.analysis_notebook.add(images_frame, text="Obrazy")
        self.images_text = scrolledtext.ScrolledText(images_frame, wrap=tk.WORD)
        self.images_text.pack(fill='both', expand=True)
        
    def analyze_website(self):
        """Trigger website analysis."""
        self.main_window.analyze_website()
        
    def display_analysis(self, analysis_data: Dict[str, str]):
        """
        Display analysis results in the tabs.
        
        Args:
            analysis_data: Dictionary containing analysis results
        """
        # Clear existing content
        self.stats_text.delete(1.0, tk.END)
        self.links_text.delete(1.0, tk.END)
        self.images_text.delete(1.0, tk.END)
        
        # Display new content
        if 'stats' in analysis_data:
            self.stats_text.insert(1.0, analysis_data['stats'])
            
        if 'links' in analysis_data:
            self.links_text.insert(1.0, analysis_data['links'])
            
        if 'images' in analysis_data:
            self.images_text.insert(1.0, analysis_data['images'])
            
    def export_report(self):
        """Export analysis report to file."""
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
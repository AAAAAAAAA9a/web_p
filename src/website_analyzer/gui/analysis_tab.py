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
        control_section = ttk.LabelFrame(main_container, text="Kontrola Analizy", padding=15)
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
        
        # NOWA SEKCJA: Pobieranie zasobów
        download_section = ttk.LabelFrame(main_container, text="🔽 Download Resource", padding=15)
        download_section.pack(fill='x', pady=(0, 15))
        
        # Rama dla pola URL i przycisku
        download_frame = ttk.Frame(download_section)
        download_frame.pack(fill='x')
        
        # Pole do wklejenia URL
        ttk.Label(download_frame, text="Resource URL:").pack(side='left', padx=(0, 5))
        self.resource_url_var = tk.StringVar()
        self.resource_url_entry = ttk.Entry(download_frame, textvariable=self.resource_url_var, width=50)
        self.resource_url_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        # Przycisk pobierania
        self.download_btn = ttk.Button(download_frame, text="💾 Download", 
                                     command=self.download_resource)
        self.download_btn.pack(side='right')
        
        # Przycisk do kopiowania URL z analizy
        self.copy_btn = ttk.Button(download_frame, text="📋 Copy from Analysis", 
                                  command=self.copy_selected_url)
        self.copy_btn.pack(side='right', padx=(0, 5))
        
        # Informacja o statusie pobierania
        self.download_status_var = tk.StringVar(value="Ready to download")
        ttk.Label(download_section, textvariable=self.download_status_var, 
                 font=('TkDefaultFont', 8)).pack(fill='x', pady=(10, 0))
          # Sekcja wyników analizy
        results_section = ttk.LabelFrame(main_container, text="Wyniki Analizy", padding=10)
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
            title="Save report",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            if self.main_window.save_analysis_report(filename):
                messagebox.showinfo("Success", f"Raport zapisany: {filename}")
            else:                messagebox.showerror("Błąd", "Błąd podczas zapisywania raportu")
                
    def download_resource(self):
        """Pobiera zasób z podanego URL na dysk."""
        import requests
        import os
        from urllib.parse import urlparse
        
        url = self.resource_url_var.get().strip()
        if not url:
            messagebox.showwarning("Ostrzeżenie", "Proszę wprowadzić URL zasobu")
            return
              # Sprawdź czy URL jest poprawny
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                messagebox.showerror("Błąd", "Nieprawidłowy format URL")
                return
        except Exception:
            messagebox.showerror("Błąd", "Nieprawidłowy format URL")
            return
              # Wybór miejsca zapisu
        try:
            # Spróbuj odgadnąć nazwę pliku z URL
            filename = os.path.basename(parsed.path) or "downloaded_resource"
            if not filename or filename == "/":
                filename = "downloaded_resource"
            
            # Wybór pliku do zapisu
            filepath = filedialog.asksaveasfilename(
                title="Zapisz Zasób Jako",
                defaultextension=os.path.splitext(filename)[1] or ".bin",
                filetypes=[
                    ("Wszystkie pliki", "*.*"),
                    ("Obrazy", "*.jpg *.jpeg *.png *.gif *.svg *.webp"),
                    ("Dokumenty", "*.pdf *.doc *.docx *.xls *.xlsx"),
                    ("Media", "*.mp4 *.webm *.mp3 *.wav"),
                    ("Pliki webowe", "*.css *.js *.html")                ]
            )
            
            if not filepath:
                return  # Użytkownik anulował
                
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd wyboru pliku: {str(e)}")
            return
            
        # Pobierz plik
        self.download_status_var.set("Pobieranie...")
        self.download_btn.config(state='disabled')
        
        try:
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()
              # Zapisz plik
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        
            file_size = os.path.getsize(filepath)
            self.download_status_var.set(f"✅ Pobrano: {os.path.basename(filepath)} ({file_size:,} bajtów)")
            messagebox.showinfo("Sukces", f"Zasób pobrano pomyślnie!\nZapisano do: {filepath}")
            
        except requests.RequestException as e:
            self.download_status_var.set(f"❌ Pobieranie nieudane: {str(e)}")
            messagebox.showerror("Błąd Pobierania", f"Nie udało się pobrać zasobu:\n{str(e)}")
            
        except Exception as e:
            self.download_status_var.set(f"❌ Błąd: {str(e)}")
            messagebox.showerror("Błąd", f"Wystąpił błąd:\n{str(e)}")
            
        finally:
            self.download_btn.config(state='normal')
            
    def copy_selected_url(self):
        """Kopiuje wybrany URL z aktualnej zakładki analizy."""
        # Sprawdź która zakładka jest aktywna
        current_tab = self.analysis_notebook.select()
        tab_text = self.analysis_notebook.tab(current_tab, "text")
          # Określ który widget tekstu użyć
        if "Statistics" in tab_text:
            text_widget = self.stats_text
        elif "Links" in tab_text:
            text_widget = self.links_text
        elif "Images" in tab_text:
            text_widget = self.images_text
        elif "Media" in tab_text:
            text_widget = self.media_text
        elif "Resources" in tab_text:
            text_widget = self.resources_text
        elif "Documents" in tab_text:
            text_widget = self.documents_text
        else:
            messagebox.showinfo("Info", "Brak dostępnych wyników analizy")
            return
            
        # Sprawdź czy jest zaznaczony tekst
        try:
            selected_text = text_widget.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
            if selected_text:                # Spróbuj wyciągnąć URL z zaznaczonego tekstu
                import re
                url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
                urls = re.findall(url_pattern, selected_text)
                if urls:
                    self.resource_url_var.set(urls[0])
                    self.download_status_var.set(f"📋 URL skopiowany: {urls[0][:50]}...")
                else:
                    # Jeśli nie ma URL, sprawdź czy to ścieżka relatywna
                    if selected_text.startswith(('/', './')):
                        messagebox.showinfo("Info", "Wykryto ścieżkę względną. Proszę dodać domenę ręcznie.")
                        self.resource_url_var.set(selected_text)
                    else:
                        messagebox.showwarning("Ostrzeżenie", "Nie znaleziono prawidłowego URL w zaznaczonym tekście")
            else:
                messagebox.showinfo("Info", "Proszę zaznaczyć URL lub ścieżkę pliku z wyników analizy")
                
        except tk.TclError:
            messagebox.showinfo("Info", "Proszę zaznaczyć URL lub ścieżkę pliku z wyników analizy")
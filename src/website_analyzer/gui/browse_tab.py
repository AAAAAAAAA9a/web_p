"""
Komponent GUI dla zakładki przeglądania.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .main_window import MainWindow


class BrowseTab:
    """Zakładka GUI do przeglądania pobranych stron."""
    
    def __init__(self, parent: ttk.Notebook, main_window: 'MainWindow'):
        self.parent = parent
        self.main_window = main_window
        self.frame = ttk.Frame(parent)
        
        self.setup_ui()        
    def setup_ui(self):
        """Konfiguracja interfejsu użytkownika zakładki przeglądania."""
        # Selektor stron
        selector_frame = ttk.Frame(self.frame)
        selector_frame.pack(fill='x', pady=5)
        
        ttk.Label(selector_frame, text="Wybierz stronę:").pack(side='left')
        self.page_combo = ttk.Combobox(selector_frame, state='readonly')
        self.page_combo.pack(side='left', fill='x', expand=True, padx=5)
        self.page_combo.bind('<<ComboboxSelected>>', self.show_page)
        
        # Opcje widoku
        options_frame = ttk.Frame(self.frame)
        options_frame.pack(fill='x', pady=5)
        
        self.view_mode = tk.StringVar(value="source")
        ttk.Radiobutton(options_frame, text="Kod źródłowy", 
                       variable=self.view_mode, value="source",
                       command=self.update_view).pack(side='left')
        ttk.Radiobutton(options_frame, text="Tekst", 
                       variable=self.view_mode, value="text",
                       command=self.update_view).pack(side='left', padx=10)
        
        # Przycisk przeglądarki
        ttk.Button(options_frame, text="🌐 Otwórz w przeglądarce", 
                  command=self.open_in_browser).pack(side='right')
        
        # Przeglądarka treści strony
        viewer_frame = ttk.Frame(self.frame)
        viewer_frame.pack(fill='both', expand=True, pady=5)
        
        # Dodaj paski przewijania
        self.page_viewer = scrolledtext.ScrolledText(viewer_frame, wrap=tk.WORD)
        self.page_viewer.pack(fill='both', expand=True)
        
        # Pasek statusu
        self.status_frame = ttk.Frame(self.frame)
        self.status_frame.pack(fill='x', pady=2)
        
        self.status_label = ttk.Label(self.status_frame, text="Brak załadowanych stron")
        self.status_label.pack(side='left')        
    def update_page_list(self, urls: List[str]):
        """
        Aktualizuje listę dostępnych stron.
        
        Args:
            urls: Lista URL-ów do wyświetlenia
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
        """Wyświetla wybraną stronę."""
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
            # Pokaż kod źródłowy HTML
            self.page_viewer.insert(1.0, content)
        else:
            # Pokaż wyodrębniony tekst
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                text_content = soup.get_text(separator='\n', strip=True)
                self.page_viewer.insert(1.0, text_content)
            except Exception:
                # Jeśli nie można przetworzyć HTML, pokaż surową zawartość
                self.page_viewer.insert(1.0, content)                
    def update_view(self):
        """Aktualizuje widok po zmianie trybu wyświetlania."""
        self.show_page()
        
    def open_in_browser(self):
        """Otwiera aktualną stronę w przeglądarce."""
        import webbrowser
        import tempfile
        import os
        import threading
        import time
        from tkinter import messagebox
        
        selected_url = self.page_combo.get()
        if not selected_url:
            messagebox.showwarning("Uwaga", "Nie wybrano strony")
            return
            
        content = self.main_window.get_page_content(selected_url)
        if not content:
            messagebox.showerror("Błąd", "Nie można pobrać zawartości strony")
            return
            
        try:
            # Utwórz poprawny plik HTML z meta tagami
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', 
                                           delete=False, encoding='utf-8') as f:
                # Sprawdź czy to już pełny HTML
                if content.strip().startswith('<!DOCTYPE') or content.strip().startswith('<html'):
                    # To już pełny dokument HTML
                    f.write(content)
                else:
                    # Dodaj podstawową strukturę HTML
                    html_doc = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">                    <title>Analizator Witryn - {selected_url}</title>
    <base href="{selected_url}">
</head>
<body>
{content}
</body>
</html>"""
                    f.write(html_doc)
                temp_file = f.name
                
            # Otwórz w przeglądarce
            webbrowser.open(f'file://{temp_file}')
            
            # Usuń plik po 60 sekundach
            def cleanup():
                time.sleep(60)
                try:
                    os.unlink(temp_file)
                except:
                    pass
            threading.Thread(target=cleanup, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można otworzyć w przeglądarce: {str(e)}")
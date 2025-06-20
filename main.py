#!/usr/bin/env python3
"""
Analizator Stron Internetowych - Główny plik uruchomieniowy

Ten plik uruchamia aplikację GUI do analizy stron internetowych.
Aplikacja pobiera strony z internetu, analizuje ich zawartość i generuje raporty.

Autor: [Artur Lisowski, Julia Kusztal]
Przedmiot: [Aplikacje sieciowe] 
Rok: 2024/2025
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# KROK 1: Dodaj folder 'src' do ścieżki Pythona
# Dzięki temu Python znajdzie nasze moduły w folderze src/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# KROK 2: Próbuj zaimportować główne okno aplikacji
try:
    from website_analyzer.gui.main_window import MainWindow
except ImportError as e:
    print(f"Błąd importu: {e}")
    print("Upewnij się, że zainstalowałeś wszystkie wymagane biblioteki:")
    print("pip install -e .")
    sys.exit(1)


def main():
    """
    Główna funkcja uruchamiająca aplikację.
    
    Ta funkcja:
    1. Tworzy główne okno tkinter
    2. Inicjalizuje aplikację Website Analyzer
    3. Centruje okno na ekranie
    4. Uruchamia główną pętlę GUI
    """
    try:
        # KROK 3: Utwórz główne okno aplikacji (tkinter)
        root = tk.Tk()
        app = MainWindow(root)  # MainWindow to nasza główna klasa GUI
        
        # KROK 4: Wycentruj okno na ekranie (opcjonalne, ale ładnie wygląda)
        root.update_idletasks()  # odśwież okno żeby poznać jego rozmiar
        width = root.winfo_width()
        height = root.winfo_height()
        # Oblicz pozycję do wycentrowania
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")
        
        # KROK 5: Uruchom główną pętlę GUI (aplikacja czeka na interakcję użytkownika)
        root.mainloop()
        
    except Exception as e:
        error_msg = f"Błąd uruchamiania aplikacji: {str(e)}"
        print(error_msg)
        # Spróbuj pokazać GUI error, ale jeśli się nie uda - trudno
        try:
            messagebox.showerror("Błąd", error_msg)
        except:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()
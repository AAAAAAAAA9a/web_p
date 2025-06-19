#!/usr/bin/env python3
"""
Website Analyzer - Main entry point
Analizator Witryn WWW - Główny punkt uruchomienia
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from website_analyzer.gui.main_window import MainWindow
except ImportError as e:
    print(f"Błąd importu: {e}")
    print("Upewnij się, że zainstalowałeś wszystkie wymagane biblioteki:")
    print("pip install -r requirements.txt")
    sys.exit(1)


def main():
    """Main application entry point."""
    try:
        root = tk.Tk()
        app = MainWindow(root)
        
        # Center window on screen
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Start the application
        root.mainloop()
        
    except Exception as e:
        error_msg = f"Błąd uruchamiania aplikacji: {str(e)}"
        print(error_msg)
        try:
            messagebox.showerror("Błąd", error_msg)
        except:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()
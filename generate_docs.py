#!/usr/bin/env python3
"""
Skrypt do generowania dokumentacji dla projektu Website Analyzer.

Automatycznie generuje HTML dokumentację z docstrings używając pdoc.
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path


def install_pdoc():
    """Instaluje pdoc jeśli nie jest zainstalowane."""
    try:
        import pdoc
        print("pdoc już zainstalowane")
        return True
    except ImportError:
        print("Instaluję pdoc...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pdoc"])
            print("pdoc zainstalowane pomyślnie")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Błąd instalacji pdoc: {e}")
            return False


def generate_docs():
    """Generuje dokumentację HTML."""
    docs_dir = Path("docs")
    
    docs_dir.mkdir(exist_ok=True)
    
    print("📖 Generuję dokumentację...")
    
    try:
        # Komenda pdoc do generowania dokumentacji
        cmd = [
            sys.executable, "-m", "pdoc",
            "--output-directory", str(docs_dir),
            "src/website_analyzer"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Dokumentacja wygenerowana pomyślnie!")
            
            html_file = docs_dir / "website_analyzer" / "index.html"
            if html_file.exists():
                print(f"Dokumentacja zapisana w: {html_file.absolute()}")
                return str(html_file.absolute())
            else:
                html_files = list(docs_dir.glob("**/*.html"))
                if html_files:
                    return str(html_files[0].absolute())
        else:
            print(f"Błąd generowania dokumentacji:")
            print(result.stderr)
            return None
            
    except Exception as e:
        print(f"Błąd: {e}")
        return None


def open_docs(html_path):
    """Otwiera dokumentację w przeglądarce."""
    if html_path and os.path.exists(html_path):
        print(f"Otwieram dokumentację w przeglądarce...")
        file_url = f"file://{html_path}"
        webbrowser.open(file_url)
        return True
    return False


def main():
    """Główna funkcja skryptu."""
    print("Generator dokumentacji Website Analyzer")
    print("=" * 50)
    
    if not Path("src/website_analyzer").exists():
        print("Błąd: Nie znaleziono katalogu src/website_analyzer")
        print("Uruchom skrypt z głównego katalogu projektu")
        sys.exit(1)
    
    if not install_pdoc():
        sys.exit(1)
    
    html_path = generate_docs()
    if not html_path:
        sys.exit(1)
    
    if open_docs(html_path):
        print("Gotowe")
    else:
        print(f"Dokumentacja dostępna w: {html_path}")
    
    print("\n💡 Aby ponownie wygenerować dokumentację: python generate_docs.py")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Skrypt do tworzenia pliku .exe dla aplikacji Website Analyzer.

Automatycznie tworzy standalone executable używając PyInstaller.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def install_pyinstaller():
    """Instaluje PyInstaller jeśli nie jest zainstalowane."""
    try:
        import PyInstaller
        print("PyInstaller już zainstalowane")
        return True
    except ImportError:
        print("Instaluję PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "pyinstaller"])
            print("PyInstaller zainstalowane pomyślnie")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Błąd instalacji PyInstaller: {e}")
            return False


def create_spec_file():
    """Tworzy plik .spec dla PyInstaller z customową konfiguracją."""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.scrolledtext',
        'requests',
        'bs4',
        'lxml',
        'urllib.parse',
        'urllib3',
        're',
        'json',
        'threading',
        'time',
        'collections',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WebsiteAnalyzer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Ukryj okno konsoli
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Tutaj można dodać ścieżkę do ikony .ico
)
'''
    
    with open('website_analyzer.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("Plik konfiguracyjny .spec utworzony")


def build_executable():
    """Buduje plik wykonywalny."""
    print("Tworzę plik wykonywalny, może potrwać kilka minut")
    
    try:
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "website_analyzer.spec"]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Plik wykonywalny utworzony pomyślnie!")
            
            exe_path = Path("dist/WebsiteAnalyzer.exe")
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"Plik: {exe_path.absolute()}")
                print(f"Rozmiar: {size_mb:.1f} MB")
                return str(exe_path.absolute())
            else:
                print("Nie znaleziono utworzonego pliku .exe")
                return None
        else:
            print("Błąd podczas tworzenia pliku wykonywalnego:")
            print(result.stderr)
            return None
            
    except Exception as e:
        print(f"Błąd: {e}")
        return None


def cleanup_build_files():
    """Usuwa tymczasowe pliki po buildzie."""
    print("Sprzątam pliki tymczasowe...")
    
    cleanup_paths = ['build', '__pycache__', 'website_analyzer.spec']
    
    for path in cleanup_paths:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    
    print("Pliki tymczasowe usunięte")


def create_distribution_folder():
    """Tworzy folder z aplikacją gotową do dystrybucji."""
    dist_folder = Path("release")
    
    if dist_folder.exists():
        shutil.rmtree(dist_folder)
    
    dist_folder.mkdir()
    
    exe_source = Path("dist/WebsiteAnalyzer.exe")
    if exe_source.exists():
        shutil.copy2(exe_source, dist_folder / "WebsiteAnalyzer.exe")
    
    readme_content = """# Website Analyzer - Analizator Stron Internetowych

## Jak uruchomić:
1. Kliknij dwukrotnie na plik WebsiteAnalyzer.exe
2. Aplikacja uruchomi się automatycznie

## Użycie:
1. Wprowadź URL witryny do analizy
2. Ustaw parametry pobierania (głębokość, liczba stron)
3. Kliknij "Pobierz witrynę"
4. Po pobraniu przejdź do zakładki "Analiza" 
5. Kliknij "Analizuj witrynę"
6. Przeglądaj wyniki w różnych zakładkach
7. Możesz pobierać zasoby wklejając URL do odpowiedniego pola
8. Możesz otworzyć wybraną stronę w przeglądarce klikając przycisk "Otwórz w przeglądarce"

Autor: [Artur Lisowski, Julia Kusztal]
Projekt studencki - {rok}
"""
    
    with open(dist_folder / "README.txt", 'w', encoding='utf-8') as f:
        f.write(readme_content.format(rok="2024/2025"))
    
    print(f"Pakiet dystrybucyjny utworzony w folderze: {dist_folder.absolute()}")
    return dist_folder


def main():
    """Główna funkcja skryptu."""
    print("Builder pliku wykonywalnego Website Analyzer")
    print("=" * 55)
    
    if not Path("main.py").exists():
        print("Błąd: Nie znaleziono pliku main.py")
        print("Uruchom skrypt z głównego katalogu projektu")
        sys.exit(1)
    
    if not install_pyinstaller():
        sys.exit(1)
    
    create_spec_file()
    
    exe_path = build_executable()
    if not exe_path:
        sys.exit(1)
    
    dist_folder = create_distribution_folder()
    
    cleanup_build_files()
    
    print(f"Pakiet dystrybucyjny: {dist_folder.absolute()}")
    print("\nInstrukcje:")
    print("   - Skopiuj folder 'release' na docelowy komputer")
    print("   - Uruchom WebsiteAnalyzer.exe")


if __name__ == "__main__":
    main()
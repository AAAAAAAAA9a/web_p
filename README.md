# Analizator Stron Internetowych

**Autor**: [Artur Lisowski, Julia Kusztal]  
**Przedmiot**: [Aplikacje Sieciowe]  
**Rok akademicki**: 2024/2025

## Opis projektu

Aplikacja GUI w języku Python do pobierania i analizowania stron internetowych.

## Funkcjonalności

1. **Pobieranie stron** - rekursywne pobieranie witryn z kontrolą głębokości
2. **Analiza zawartości** - statystyki, linki, obrazy, media, zasoby, dokumenty, częstotliwość słów
3. **Pobieranie zasobów** - możliwość pobierania pojedynczych plików z witryny
4. **Przeglądanie** - wyświetlanie pobranych stron z kodem źródłowym
5. **Zarządzanie danymi** - zapisywanie i wczytywanie projektów
6. **Eksport raportów** - generowanie szczegółowych raportów analizy

## Technologie

- **Python 3.7+** - język programowania
- **tkinter** - interfejs graficzny (GUI)
- **requests** - pobieranie stron HTTP
- **BeautifulSoup** - parsowanie HTML
- **lxml** - parser XML/HTML

## Struktura projektu

```text
src/website_analyzer/
├── core/                    # Logika biznesowa
│   ├── downloader.py       # Klasa do pobierania stron
│   ├── analyzer.py         # Klasa do analizy danych
│   ├── file_manager.py     # Zarządzanie plikami
│   └── error_handler.py    # Obsługa błędów
├── gui/                     # Interfejs użytkownika
│   ├── main_window.py      # Główne okno
│   ├── download_tab.py     # Zakładka pobierania
│   ├── analysis_tab.py     # Zakładka analizy
│   └── browse_tab.py       # Zakładka przeglądania
└── __init__.py
main.py                      # Uruchomienie aplikacji
tests/                       # Testy jednostkowe
pyproject.toml              # Konfiguracja projektu
```

## Instalacja i uruchomienie

### Krok 1: Przygotowanie środowiska

```bash
# Klonuj projekt
git clone [adres-repo]
cd src\website_analyzer

# Utwórz środowisko wirtualne
python -m venv venv
source venv/bin/activat  # Linux/Mac
# lub
venv\Scripts\activate     # Windows
```

### Krok 2: Instalacja zależności

```bash
pip install -e .
```

### Krok 3: Uruchomienie

```bash
python main.py
```

## Instrukcja użycia

### 1. Pobieranie strony

- Wprowadź URL w polu "URL"
- Ustaw głębokość pobierania (1-5 poziomów)
- Ustaw maksymalną liczbę stron
- Kliknij "🌐 Pobierz Witrynę"

### 2. Analiza danych

- Przejdź do zakładki "📊 Analiza"
- Kliknij "🔍 Analizuj Witrynę"
- Przeglądaj wyniki w sześciu kategoriach:
  - **Statystyki** - podstawowe dane liczbowe i częstotliwość słów
  - **Linki** - analiza odnośników (wewnętrzne, zewnętrzne, email)
  - **Obrazy** - analiza grafik według formatów
  - **Media** - pliki video i audio
  - **Zasoby** - pliki CSS i JavaScript
  - **Dokumenty** - pliki PDF, DOC, XLS i inne

### 2a. Pobieranie zasobów

- W zakładce "📊 Analiza" znajdziesz sekcję "🔽 Download Resource"
- Wklej URL zasobu lub skopiuj go z wyników analizy
- Kliknij "💾 Download" aby pobrać plik na dysk
- Dostępne formaty: obrazy, dokumenty, media, pliki webowe

### 3. Przeglądanie

- Zakładka "📖 Przeglądanie" pozwala:
  - Przeglądać listę pobranych stron
  - Wyświetlać kod źródłowy HTML
  - Wyświetlać czysty tekst

### 4. Zarządzanie projektami

- **Zapisz na dysk** - eksport danych do folderu
- **Wczytaj z dysku** - import wcześniej zapisanych danych
- **Eksportuj raport** - generowanie raportu tekstowego

## Wzorce projektowe użyte w kodzie

1. **Separacja warstw** - podział na logikę biznesową (core) i interfejs (gui)
2. **Observer/Callback** - informowanie o postępie operacji
3. **Dependency Injection** - przekazywanie zależności między klasami
4. **Facade** - uproszczony interfejs do skomplikowanych operacji

## Testowanie

```bash
# Uruchom wszystkie testy
python -m pytest tests/

# Test konkretnego modułu
python -m pytest tests/test_downloader.py

# Test z pokryciem kodu
python -m pytest --cov=src/website_analyzer tests/
```

## Dokumentacja

Automatyczne generowanie dokumentacji HTML z docstrings:

```bash
# Wygeneruj dokumentację (automatycznie otwiera w przeglądarce)
python generate_docs.py

# Dokumentacja zostanie zapisana w folderze docs/
```

## Tworzenie pliku wykonywalnego (.exe)

Dla użytkowników Windows - tworzenie standalone aplikacji:

```bash
# Automatyczne tworzenie pliku .exe (Windows)
python build_exe.py

# Plik zostanie utworzony w folderze release/
```

### Instrukcja manualna

```bash
# 1. Zainstaluj PyInstaller
pip install pyinstaller

# 2. Utwórz plik wykonywalny
pyinstaller --onefile --windowed --name="WebsiteAnalyzer" main.py

# 3. Plik .exe będzie w folderze dist/
```

## Przykład użycia w kodzie

```python
from src.website_analyzer.core.downloader import WebsiteDownloader
from src.website_analyzer.core.analyzer import WebsiteAnalyzer

# Pobieranie strony
downloader = WebsiteDownloader(max_pages=10, max_depth=2)
pages = downloader.download_website("https://example.com")

# Analiza danych
analyzer = WebsiteAnalyzer()
results = analyzer.analyze_pages(pages)
print(results['stats'])
```

## Problemy znane i ograniczenia

- Aplikacja może działać wolno dla dużych witryn
- Brak obsługi JavaScript (tylko statyczny HTML)
- Rate limiting może spowalniać pobieranie
- GUI zoptimalizowane dla rozdzielczości 1200x800+

## TODO / Przyszłe ulepszenia

- [ ] Dodanie obsługi robots.txt
- [ ] Implementacja wielowątkowości dla pobierania
- [ ] Eksport do formatów CSV/JSON
- [ ] Zaawansowane filtry analizy
- [ ] Obsługa cookies i sesji

## Licencja

Projekt edukacyjny - MIT License

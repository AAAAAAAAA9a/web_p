# Website Analyzer - Analizator Witryn WWW

Profesjonalna aplikacja GUI do pobierania, przeglądania i analizy witryn internetowych z modularną strukturą projektu.

## Funkcje

- **Pobieranie witryn WWW**: Rekursywne pobieranie z konfigurowalnną głębokością (1-5 poziomów)
- **Analiza zawartości**: Szczegółowa analiza linków, obrazów, statystyk i częstotliwości słów
- **Przeglądanie stron**: Wbudowana przeglądarka z trybem kodu źródłowego i tekstu
- **Zarządzanie danymi**: Zapisywanie/wczytywanie projektów z metadanymi
- **Eksport raportów**: Generowanie szczegółowych raportów analitycznych

## Struktura Projektu

```
website_analyzer/
├── src/
│   └── website_analyzer/
│       ├── core/                 # Logika biznesowa
│       │   ├── downloader.py     # Pobieranie witryn
│       │   ├── analyzer.py       # Analiza zawartości
│       │   └── file_manager.py   # Zarządzanie plikami
│       └── gui/                  # Interfejs użytkownika
│           ├── main_window.py    # Główne okno aplikacji
│           ├── download_tab.py   # Zakładka pobierania
│           ├── analysis_tab.py   # Zakładka analizy
│           └── browse_tab.py     # Zakładka przeglądania
├── tests/                        # Testy jednostkowe
├── docs/                         # Dokumentacja
├── assets/                       # Zasoby (ikony, obrazy)
├── main.py                       # Punkt wejścia aplikacji
├── setup.py                      # Instalator
├── pyproject.toml               # Konfiguracja projektu
└── requirements.txt             # Zależności
```

## Instalacja

### Standardowa instalacja
```bash
# Klonuj repozytorium
git clone https://github.com/yourusername/website-analyzer.git
cd website-analyzer

# Zainstaluj zależności
pip install -r requirements.txt

# Uruchom aplikację
python main.py
```

### Instalacja deweloperska
```bash
# Zainstaluj w trybie development
pip install -e .

# Uruchom aplikację
website-analyzer
```

## Użycie

### 1. Zakładka "Pobieranie / Download"
- **URL witryny**: Wprowadź adres do pobrania (http/https)
- **Głębokość pobierania**: Ustaw poziomy rekursji (1-5)
- **Maksymalna liczba stron**: Ogranicz liczbę pobranych stron
- **Opcje zapisu**: Zapisz na dysk lub wczytaj wcześniej pobrany projekt

### 2. Zakładka "Analiza / Analysis"
- **Statystyki**: Podstawowe metryki witryny, kody HTTP, analiza słów
- **Linki**: Kategoryzacja linków (wewnętrzne, zewnętrzne, email)
- **Obrazy**: Analiza obrazów według typów i rozszerzeń
- **Eksport**: Generowanie raportów w formacie tekstowym

### 3. Zakładka "Przeglądanie / Browse"
- **Wybór strony**: Lista wszystkich pobranych stron
- **Tryb wyświetlania**: Kod źródłowy HTML lub czysty tekst
- **Nawigacja**: Szybkie przełączanie między stronami

## Rozwój i Testowanie

```bash
# Uruchom testy
python -m pytest tests/

# Uruchom konkretny test
python -m pytest tests/test_downloader.py

# Analiza pokrycia kodu
pip install pytest-cov
python -m pytest --cov=src/website_analyzer tests/
```

## Wymagania Techniczne

- **Python**: 3.7+ 
- **GUI**: tkinter (standardowa biblioteka)
- **HTTP**: requests >= 2.28.0
- **Parsing**: beautifulsoup4 >= 4.11.0, lxml >= 4.9.0
- **System**: Windows, Linux, MacOS

## Architektura

Aplikacja wykorzystuje wzorzec **separacji warstw**:
- **Core**: Logika biznesowa niezależna od GUI
- **GUI**: Komponenty interfejsu użytkownika
- **Main**: Punkt wejścia i konfiguracja aplikacji

Komunikacja między warstwami odbywa się przez wzorzec **callback** dla operacji asynchronicznych i **dependency injection** dla współdzielenia stanu.
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python GUI application called "Website Analyzer" that downloads and analyzes websites. The project uses a modular architecture with separation between core business logic and GUI components.

## Development Commands

### Running the Application
```bash
# Main entry point
python main.py

# Or after installation
website-analyzer
```

### Testing
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_downloader.py

# Run with coverage
python -m pytest --cov=src/website_analyzer tests/
```

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Development installation
pip install -e .
```

### Linting and Formatting
```bash
# Note: No linting tools configured yet
# Consider adding: black, flake8, mypy
```

## Project Architecture

### Directory Structure
- `src/website_analyzer/` - Main application package
  - `core/` - Business logic modules (downloader, analyzer, file_manager)
  - `gui/` - GUI components (main_window, tabs)
- `tests/` - Unit tests
- `main.py` - Application entry point
- `setup.py` & `pyproject.toml` - Package configuration

### Key Components

1. **WebsiteDownloader** (`src/website_analyzer/core/downloader.py`):
   - Handles recursive website downloading
   - Configurable depth and page limits
   - Progress callback support

2. **WebsiteAnalyzer** (`src/website_analyzer/core/analyzer.py`):
   - Analyzes downloaded content
   - Generates statistics, link analysis, image analysis
   - Word frequency analysis

3. **FileManager** (`src/website_analyzer/core/file_manager.py`):
   - Saves/loads website data with metadata
   - Exports analysis reports
   - JSON metadata handling

4. **GUI Components** (`src/website_analyzer/gui/`):
   - `MainWindow` - Main application window and coordination
   - `DownloadTab` - Website downloading interface
   - `AnalysisTab` - Analysis results display
   - `BrowseTab` - Downloaded page browser

### Design Patterns
- **Separation of Concerns**: Core logic separated from GUI
- **Observer Pattern**: Progress callbacks for async operations
- **Dependency Injection**: MainWindow coordinates between components
- **Modular Architecture**: Each component has single responsibility

## Dependencies

- `requests` - HTTP client for downloading
- `beautifulsoup4` - HTML parsing
- `lxml` - XML/HTML parser
- `tkinter` - GUI framework (standard library)

## Development Notes

- The application uses threading for non-blocking downloads
- All file operations include proper error handling
- GUI components use TYPE_CHECKING to avoid circular imports
- Progress updates are handled via callbacks to keep UI responsive

## Common Tasks

When modifying this codebase:
1. **Adding new analysis features**: Extend `WebsiteAnalyzer` class
2. **Modifying GUI**: Update relevant tab component in `gui/` directory
3. **Adding new core functionality**: Create new module in `core/` directory
4. **Adding tests**: Create test files in `tests/` directory following naming convention

## Configuration

- `.claude/settings.local.json` - Claude Code permissions
- `requirements.txt` - Python dependencies
- `setup.py` & `pyproject.toml` - Package configuration
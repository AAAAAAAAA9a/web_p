"""
Moduł do prostej obsługi błędów i logowania.

Centralizuje obsługę błędów w całej aplikacji.
"""

import traceback
from typing import Optional, Callable
from tkinter import messagebox


class SimpleErrorHandler:
    """
    Prosta klasa do obsługi błędów w aplikacji.
    
    Standaryzuje sposób raportowania błędów i upraszcza kod.
    """
    
    def __init__(self, logger_callback: Optional[Callable[[str], None]] = None):
        """
        Konstruktor handlera błędów.
        
        Argumenty:
            logger_callback: funkcja do logowania wiadomości (opcjonalna)
        """
        self.logger_callback = logger_callback or print
    
    def log(self, message: str):
        """Loguje wiadomość przez callback."""
        if self.logger_callback:
            self.logger_callback(message)
    
    def handle_network_error(self, url: str, error: Exception) -> str:
        """Obsługuje błędy sieciowe."""
        msg = f"Błąd sieci dla {url}: {str(error)}"
        self.log(msg)
        return msg
    
    def handle_file_error(self, filepath: str, error: Exception) -> str:
        """Obsługuje błędy plików."""
        msg = f"Błąd pliku {filepath}: {str(error)}"
        self.log(msg)
        return msg
    
    def handle_general_error(self, operation: str, error: Exception, show_gui: bool = False) -> str:
        """
        Obsługuje ogólne błędy.
        
        Argumenty:
            operation: nazwa operacji która się nie powiodła
            error: obiekt błędu
            show_gui: czy pokazać okno dialogowe błędu
        """
        msg = f"Błąd {operation}: {str(error)}"
        self.log(msg)
        
        if show_gui:
            try:
                messagebox.showerror("Błąd", msg)
            except:
                pass  # jeśli GUI nie działa, zignoruj
        
        return msg
    
    def safe_execute(self, func, *args, **kwargs):
        """
        Bezpiecznie wykonuje funkcję łapiąc błędy.
        
        Zwraca:
            (success: bool, result_or_error_message)
        """
        try:
            result = func(*args, **kwargs)
            return True, result
        except Exception as e:
            error_msg = self.handle_general_error(func.__name__, e)
            return False, error_msg


# Globalny handler błędów - jeden dla całej aplikacji
_global_handler = SimpleErrorHandler()


def set_global_logger(logger_callback: Callable[[str], None]):
    """Ustawia globalny callback do logowania."""
    global _global_handler
    _global_handler = SimpleErrorHandler(logger_callback)


def get_handler() -> SimpleErrorHandler:
    """Zwraca globalny handler błędów."""
    return _global_handler


# Funkcje pomocnicze do szybkiego użycia
def log_error(message: str):
    """Szybkie logowanie błędu."""
    get_handler().log(message)


def handle_network_error(url: str, error: Exception) -> str:
    """Szybka obsługa błędu sieciowego."""
    return get_handler().handle_network_error(url, error)


def handle_file_error(filepath: str, error: Exception) -> str:
    """Szybka obsługa błędu pliku."""
    return get_handler().handle_file_error(filepath, error)


def handle_error(operation: str, error: Exception, show_gui: bool = False) -> str:
    """Szybka obsługa ogólnego błędu."""
    return get_handler().handle_general_error(operation, error, show_gui)


def safe_execute(func, *args, **kwargs):
    """Bezpiecznie wykonuje funkcję."""
    return get_handler().safe_execute(func, *args, **kwargs)
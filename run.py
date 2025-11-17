#!/usr/bin/env python3
"""
Cross-platform launcher for Website Analyzer.
Works on Windows, Linux, and macOS without any modifications.

Usage:
    python run.py
"""

import sys
import subprocess
import os
from pathlib import Path


def check_dependencies():
    """Check if required packages are installed."""
    required = ['requests', 'bs4', 'lxml']
    missing = []

    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    return missing


def install_dependencies():
    """Install missing dependencies."""
    print("Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "requests>=2.28.0",
            "beautifulsoup4>=4.11.0",
            "lxml>=4.9.0"
        ])
        return True
    except subprocess.CalledProcessError:
        return False


def main():
    """Main launcher function."""
    print("=" * 50)
    print("  Website Analyzer")
    print("  Starting application...")
    print("=" * 50)
    print()

    # Check for missing dependencies
    missing = check_dependencies()

    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        response = input("Install now? (y/n): ").strip().lower()

        if response == 'y':
            if not install_dependencies():
                print("ERROR: Failed to install dependencies")
                print("Please run manually: pip install requests beautifulsoup4 lxml")
                return 1
            print("Dependencies installed successfully!")
            print()
        else:
            print("Cannot start without dependencies.")
            print("Install with: pip install requests beautifulsoup4 lxml")
            return 1

    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    # Run main.py
    print("Launching Website Analyzer...")
    print()

    try:
        # Import and run main
        sys.path.insert(0, str(script_dir / 'src'))
        from website_analyzer.gui.main_window import MainWindow
        import tkinter as tk

        root = tk.Tk()
        app = MainWindow(root)

        # Center window
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")

        root.mainloop()
        return 0

    except ImportError as e:
        print(f"ERROR: Import failed - {e}")
        print("Make sure you're in the project directory.")
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

"""
File management utilities for saving and loading website data.
"""

import os
import json
from typing import Dict, Optional


class FileManager:
    """Handles saving and loading of website data."""
    
    def __init__(self):
        pass
        
    def save_website_data(self, downloaded_pages: Dict[str, Dict], folder_path: str) -> bool:
        """
        Save downloaded website data to disk.
        
        Args:
            downloaded_pages: Dictionary of page data to save
            folder_path: Directory path to save files
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                
            # Save individual pages
            for i, (url, page_data) in enumerate(downloaded_pages.items()):
                filename = f"page_{i+1:03d}.html"
                filepath = os.path.join(folder_path, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"<!-- URL: {url} -->\n")
                    f.write(f"<!-- Status: {page_data['status_code']} -->\n")
                    f.write(f"<!-- Size: {page_data['size']} bytes -->\n")
                    f.write(page_data['content'])
                    
            # Save index file
            self._save_index_file(downloaded_pages, folder_path)
            
            # Save metadata
            self._save_metadata(downloaded_pages, folder_path)
            
            return True
            
        except Exception as e:
            print(f"Error saving website data: {e}")
            return False
            
    def _save_index_file(self, downloaded_pages: Dict[str, Dict], folder_path: str):
        """Save index file mapping filenames to URLs."""
        index_path = os.path.join(folder_path, "index.txt")
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write("INDEKS POBRANYCH STRON / DOWNLOADED PAGES INDEX\n")
            f.write("="*60 + "\n\n")
            for i, (url, page_data) in enumerate(downloaded_pages.items(), 1):
                f.write(f"page_{i:03d}.html - {url} - {page_data['status_code']} - {page_data['size']} bytes\n")
                
    def _save_metadata(self, downloaded_pages: Dict[str, Dict], folder_path: str):
        """Save metadata as JSON for programmatic access."""
        metadata = {
            'total_pages': len(downloaded_pages),
            'total_size': sum(page['size'] for page in downloaded_pages.values()),
            'pages': {}
        }
        
        for i, (url, page_data) in enumerate(downloaded_pages.items(), 1):
            filename = f"page_{i:03d}.html"
            metadata['pages'][filename] = {
                'url': url,
                'status_code': page_data['status_code'],
                'size': page_data['size'],
                'headers': page_data['headers']
            }
            
        metadata_path = os.path.join(folder_path, "metadata.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
            
    def save_analysis_report(self, analysis_data: Dict[str, str], filepath: str) -> bool:
        """
        Save analysis report to a text file.
        
        Args:
            analysis_data: Dictionary containing analysis results
            filepath: Path to save the report
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("RAPORT ANALIZY WITRYNY / WEBSITE ANALYSIS REPORT\n")
                f.write("="*60 + "\n\n")
                
                if 'stats' in analysis_data:
                    f.write(analysis_data['stats'])
                    
                if 'links' in analysis_data:
                    f.write("\n\n" + analysis_data['links'])
                    
                if 'images' in analysis_data:
                    f.write("\n\n" + analysis_data['images'])
                    
            return True
            
        except Exception as e:
            print(f"Error saving analysis report: {e}")
            return False
            
    def load_website_data(self, folder_path: str) -> Optional[Dict[str, Dict]]:
        """
        Load previously saved website data.
        
        Args:
            folder_path: Directory containing saved website data
            
        Returns:
            Dictionary of loaded page data or None if failed
        """
        try:
            metadata_path = os.path.join(folder_path, "metadata.json")
            if not os.path.exists(metadata_path):
                return None
                
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                
            downloaded_pages = {}
            
            for filename, page_info in metadata['pages'].items():
                filepath = os.path.join(folder_path, filename)
                if os.path.exists(filepath):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Remove HTML comments we added
                        lines = content.split('\n')
                        content = '\n'.join(lines[3:])  # Skip first 3 comment lines
                        
                    downloaded_pages[page_info['url']] = {
                        'content': content,
                        'status_code': page_info['status_code'],
                        'headers': page_info['headers'],
                        'url': page_info['url'],
                        'size': page_info['size']
                    }
                    
            return downloaded_pages
            
        except Exception as e:
            print(f"Error loading website data: {e}")
            return None
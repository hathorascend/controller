"""Data persistence layer with modular storage management."""

import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

from models import AppData, StorageError


class DataManager:
    """Manages application data persistence and retrieval."""
    
    def __init__(self, data_file: Path, log_file: Path) -> None:
        """Initialize data manager.
        
        Args:
            data_file: Path to JSON data file
            log_file: Path to operation log file
        """
        self.data_file = data_file
        self.log_file = log_file
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
    
    def load_data(self, template: Any = None) -> AppData:
        """Load data from file or create default.
        
        Args:
            template: Default template if file doesn't exist
            
        Returns:
            Application data
            
        Raises:
            StorageError: If loading fails
        """
        if self.data_file.exists():
            try:
                content = self.data_file.read_text(encoding="utf-8")
                return json.loads(content)
            except (json.JSONDecodeError, IOError) as e:
                raise StorageError(f"Failed to load data: {e}")
        return template or {}
    
    def save_data(self, data: AppData) -> None:
        """Save data to file.
        
        Args:
            data: Application data to save
            
        Raises:
            StorageError: If saving fails
        """
        try:
            content = json.dumps(data, ensure_ascii=False, indent=2)
            self.data_file.write_text(content, encoding="utf-8")
            self.log_operation("SAVE", f"Data saved successfully")
        except (IOError, json.JSONEncodeError) as e:
            raise StorageError(f"Failed to save data: {e}")
    
    def log_operation(self, action: str, detail: str) -> None:
        """Log an operation.
        
        Args:
            action: Action type
            detail: Action details
        """
        try:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            line = f"[{ts}] {action}: {detail}\n"
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            with self.log_file.open("a", encoding="utf-8") as f:
                f.write(line)
        except IOError as e:
            print(f"Warning: Could not log operation: {e}")
    
    def export_month_txt(self, year: int, month: int, items: list) -> Path:
        """Export monthly data to TXT.
        
        Args:
            year: Year
            month: Month
            items: Monthly items
            
        Returns:
            Path to exported file
        """
        out_file = self.data_file.parent / f"pendientes_{year:04d}-{month:02d}.txt"
        pending = [i for i in items if not i.get("paid", False)]
        
        lines = [f"Pendientes {year:04d}-{month:02d}", "=" * 60]
        for item in sorted(pending, key=lambda x: x.get("due", "")):
            lines.append(f"{item.get('due')} | {item.get('amount', 0):.2f}€ | {item.get('name')}")
        
        lines.extend(["=" * 60, f"TOTAL: {sum(i.get('amount', 0) for i in pending):.2f}€"])
        
        try:
            out_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
            self.log_operation("EXPORT", f"Exported {out_file.name}")
            return out_file
        except IOError as e:
            raise StorageError(f"Failed to export file: {e}")

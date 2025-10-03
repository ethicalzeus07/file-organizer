"""Main file organizer module."""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class FileOrganizer:
    """A class for organizing files in directories based on various criteria."""

    def __init__(self, source_directory: str | Path):
        """Initialize the FileOrganizer.
        
        Args:
            source_directory: The directory to organize files from.
        """
        self.source_directory = Path(source_directory)
        if not self.source_directory.exists():
            raise ValueError(f"Directory {source_directory} does not exist")
        
        # File type mappings
        self.file_type_mappings: Dict[str, List[str]] = {
            "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg"],
            "documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
            "videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
            "audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
            "archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
            "code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h"],
            "spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
            "presentations": [".ppt", ".pptx", ".odp"],
        }

    def get_file_type(self, file_path: Path) -> str:
        """Determine the file type based on extension.
        
        Args:
            file_path: Path to the file.
            
        Returns:
            The file type category or 'other' if not recognized.
        """
        extension = file_path.suffix.lower()
        
        for file_type, extensions in self.file_type_mappings.items():
            if extension in extensions:
                return file_type
        
        return "other"

    def scan_directory(self) -> Dict[str, List[Path]]:
        """Scan the source directory and categorize files.
        
        Returns:
            Dictionary mapping file types to lists of file paths.
        """
        files_by_type: Dict[str, List[Path]] = {}
        
        for file_path in self.source_directory.iterdir():
            if file_path.is_file():
                file_type = self.get_file_type(file_path)
                if file_type not in files_by_type:
                    files_by_type[file_type] = []
                files_by_type[file_type].append(file_path)
        
        return files_by_type

    def organize_by_type(self, dry_run: bool = False) -> Dict[str, List[str]]:
        """Organize files by type into subdirectories.
        
        Args:
            dry_run: If True, only preview what would be moved without actually moving files.
            
        Returns:
            Dictionary mapping destination directories to lists of filenames that were/would be moved.
        """
        files_by_type = self.scan_directory()
        moved_files: Dict[str, List[str]] = {}
        
        for file_type, files in files_by_type.items():
            if not files:  # Skip empty categories
                continue
                
            type_directory = self.source_directory / file_type
            type_directory.mkdir(parents=True, exist_ok=True)
            
            moved_files[f"{file_type}/"] = []
            
            for file_path in files:
                destination = type_directory / file_path.name
                
                # Skip if file already exists in destination
                if destination.exists():
                    continue
                
                if dry_run:
                    print(f"[DRY RUN] Would move {file_path.name} to {type_directory}")
                    moved_files[f"{file_type}/"].append(file_path.name)
                else:
                    try:
                        shutil.move(str(file_path), str(destination))
                        print(f"Moved {file_path.name} to {type_directory}")
                        moved_files[f"{file_type}/"].append(file_path.name)
                    except Exception as e:
                        print(f"Error moving {file_path.name}: {e}")
        
        return moved_files

    def organize_by_date(self, dry_run: bool = False) -> Dict[str, List[str]]:
        """Organize files by modification date into YYYY/MM subdirectories.
        
        Args:
            dry_run: If True, only preview what would be moved without actually moving files.
            
        Returns:
            Dictionary mapping destination directories to lists of filenames that were/would be moved.
        """
        moved_files: Dict[str, List[str]] = {}
        
        for file_path in self.source_directory.iterdir():
            if not file_path.is_file():
                continue
            
            # Get modification time
            mtime = os.path.getmtime(file_path)
            mod_date = datetime.fromtimestamp(mtime)
            
            # Create YYYY/MM directory structure
            year = mod_date.strftime("%Y")
            month = mod_date.strftime("%m")
            date_directory = self.source_directory / year / month
            date_directory.mkdir(parents=True, exist_ok=True)
            
            destination = date_directory / file_path.name
            dir_key = f"{year}/{month}/"
            
            # Initialize directory key if not exists
            if dir_key not in moved_files:
                moved_files[dir_key] = []
            
            # Skip if file already exists in destination
            if destination.exists():
                continue
            
            if dry_run:
                print(f"[DRY RUN] Would move {file_path.name} to {date_directory}")
                moved_files[dir_key].append(file_path.name)
            else:
                try:
                    shutil.move(str(file_path), str(destination))
                    print(f"Moved {file_path.name} to {date_directory}")
                    moved_files[dir_key].append(file_path.name)
                except Exception as e:
                    print(f"Error moving {file_path.name}: {e}")
        
        return moved_files

    def preview_organization(self) -> Dict[str, List[str]]:
        """Preview what files would be moved where.
        
        Returns:
            Dictionary mapping destination directories to lists of filenames.
        """
        return self.organize_by_type(dry_run=True)

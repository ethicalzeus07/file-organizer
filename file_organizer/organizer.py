"""Main file organizer module."""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Set


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

    def organize_by_type(self, target_directory: Optional[str | Path] = None) -> None:
        """Organize files by type into subdirectories.
        
        Args:
            target_directory: Directory to organize files into. 
                             If None, uses source_directory.
        """
        if target_directory is None:
            target_directory = self.source_directory
        else:
            target_directory = Path(target_directory)
            target_directory.mkdir(parents=True, exist_ok=True)
        
        files_by_type = self.scan_directory()
        
        for file_type, files in files_by_type.items():
            type_directory = target_directory / file_type
            type_directory.mkdir(exist_ok=True)
            
            for file_path in files:
                destination = type_directory / file_path.name
                if not destination.exists():
                    shutil.move(str(file_path), str(destination))
                    print(f"Moved {file_path.name} to {type_directory}")

    def preview_organization(self) -> Dict[str, List[str]]:
        """Preview what files would be moved where.
        
        Returns:
            Dictionary mapping destination directories to lists of filenames.
        """
        files_by_type = self.scan_directory()
        preview: Dict[str, List[str]] = {}
        
        for file_type, files in files_by_type.items():
            preview[f"{file_type}/"] = [file.name for file in files]
        
        return preview

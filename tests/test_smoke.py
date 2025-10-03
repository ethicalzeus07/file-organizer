"""Smoke tests for the file organizer package."""

import os
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from file_organizer import FileOrganizer


class TestFileOrganizerSmoke:
    """Basic smoke tests to ensure the package works."""

    def test_import(self):
        """Test that the package can be imported."""
        from file_organizer import FileOrganizer
        assert FileOrganizer is not None

    def test_initialization(self):
        """Test that FileOrganizer can be initialized with a valid directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            organizer = FileOrganizer(temp_dir)
            assert organizer.source_directory == Path(temp_dir)

    def test_initialization_with_nonexistent_directory(self):
        """Test that FileOrganizer raises an error for nonexistent directories."""
        with pytest.raises(ValueError):
            FileOrganizer("/nonexistent/directory")

    def test_get_file_type(self):
        """Test file type detection."""
        with tempfile.TemporaryDirectory() as temp_dir:
            organizer = FileOrganizer(temp_dir)
            
            # Test image file
            assert organizer.get_file_type(Path("test.jpg")) == "images"
            
            # Test document file
            assert organizer.get_file_type(Path("test.pdf")) == "documents"
            
            # Test unknown file type
            assert organizer.get_file_type(Path("test.xyz")) == "other"

    def test_scan_empty_directory(self):
        """Test scanning an empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            organizer = FileOrganizer(temp_dir)
            result = organizer.scan_directory()
            assert result == {}

    def test_preview_organization(self):
        """Test preview functionality."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create some test files
            (Path(temp_dir) / "test.jpg").touch()
            (Path(temp_dir) / "test.pdf").touch()
            (Path(temp_dir) / "test.xyz").touch()
            
            organizer = FileOrganizer(temp_dir)
            preview = organizer.preview_organization()
            
            assert "images/" in preview
            assert "documents/" in preview
            assert "other/" in preview
            assert "test.jpg" in preview["images/"]
            assert "test.pdf" in preview["documents/"]
            assert "test.xyz" in preview["other/"]

    def test_file_type_mappings(self):
        """Test that file type mappings are properly defined."""
        with tempfile.TemporaryDirectory() as temp_dir:
            organizer = FileOrganizer(temp_dir)
            
            # Test that all expected file types are present
            expected_types = {
                "images", "documents", "videos", "audio", 
                "archives", "code", "spreadsheets", "presentations"
            }
            assert set(organizer.file_type_mappings.keys()) == expected_types
            
            # Test that extensions are lowercase
            for extensions in organizer.file_type_mappings.values():
                for ext in extensions:
                    assert ext.startswith(".")
                    assert ext.islower()

    def test_organize_by_type_dry_run(self):
        """Test dry-run functionality for organize_by_type."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create sample files
            (temp_path / "test.jpg").touch()
            (temp_path / "document.pdf").touch()
            (temp_path / "script.py").touch()
            (temp_path / "unknown.xyz").touch()
            
            organizer = FileOrganizer(temp_dir)
            result = organizer.organize_by_type(dry_run=True)
            
            # Check that files are categorized correctly
            assert "images/" in result
            assert "documents/" in result
            assert "code/" in result
            assert "other/" in result
            
            assert "test.jpg" in result["images/"]
            assert "document.pdf" in result["documents/"]
            assert "script.py" in result["code/"]
            assert "unknown.xyz" in result["other/"]
            
            # Verify no directories were actually created
            assert not (temp_path / "images").exists()
            assert not (temp_path / "documents").exists()
            assert not (temp_path / "code").exists()
            assert not (temp_path / "other").exists()

    def test_organize_by_type_real_run(self):
        """Test actual file organization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create sample files
            (temp_path / "test.jpg").touch()
            (temp_path / "document.pdf").touch()
            (temp_path / "script.py").touch()
            
            organizer = FileOrganizer(temp_dir)
            result = organizer.organize_by_type(dry_run=False)
            
            # Check that files were moved correctly
            assert "images/" in result
            assert "documents/" in result
            assert "code/" in result
            
            assert "test.jpg" in result["images/"]
            assert "document.pdf" in result["documents/"]
            assert "script.py" in result["code/"]
            
            # Verify directories were created and files moved
            assert (temp_path / "images" / "test.jpg").exists()
            assert (temp_path / "documents" / "document.pdf").exists()
            assert (temp_path / "code" / "script.py").exists()
            
            # Verify original files are gone
            assert not (temp_path / "test.jpg").exists()
            assert not (temp_path / "document.pdf").exists()
            assert not (temp_path / "script.py").exists()

    def test_organize_skip_existing_files(self):
        """Test that existing files in destination are skipped."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create a file and its destination directory
            (temp_path / "test.jpg").touch()
            (temp_path / "images").mkdir()
            (temp_path / "images" / "test.jpg").touch()
            
            organizer = FileOrganizer(temp_dir)
            result = organizer.organize_by_type(dry_run=False)
            
            # Should not move the file since it already exists in destination
            assert "images/" in result
            assert result["images/"] == []  # No files moved

    def test_organize_empty_directory(self):
        """Test organizing an empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            organizer = FileOrganizer(temp_dir)
            result = organizer.organize_by_type(dry_run=False)
            assert result == {}

    def test_preview_organization_uses_dry_run(self):
        """Test that preview_organization uses dry-run internally."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create sample files
            (temp_path / "test.jpg").touch()
            (temp_path / "document.pdf").touch()
            
            organizer = FileOrganizer(temp_dir)
            preview = organizer.preview_organization()
            
            # Check that files are in preview
            assert "images/" in preview
            assert "documents/" in preview
            assert "test.jpg" in preview["images/"]
            assert "document.pdf" in preview["documents/"]
            
            # Verify no directories were created (dry-run behavior)
            assert not (temp_path / "images").exists()
            assert not (temp_path / "documents").exists()

    def test_organize_by_date_dry_run(self):
        """Test dry-run functionality for organize_by_date."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create files with specific modification times
            file1 = temp_path / "test1.jpg"
            file2 = temp_path / "test2.pdf"
            file1.touch()
            file2.touch()
            
            # Set fixed modification times
            # File 1: January 15, 2023
            mtime1 = datetime(2023, 1, 15, 10, 30, 0).timestamp()
            os.utime(file1, (mtime1, mtime1))
            
            # File 2: March 22, 2024
            mtime2 = datetime(2024, 3, 22, 14, 45, 0).timestamp()
            os.utime(file2, (mtime2, mtime2))
            
            organizer = FileOrganizer(temp_dir)
            result = organizer.organize_by_date(dry_run=True)
            
            # Check that files are categorized by date
            assert "2023/01/" in result
            assert "2024/03/" in result
            
            assert "test1.jpg" in result["2023/01/"]
            assert "test2.pdf" in result["2024/03/"]
            
            # Verify no directories were actually created
            assert not (temp_path / "2023").exists()
            assert not (temp_path / "2024").exists()

    def test_organize_by_date_real_run(self):
        """Test actual file organization by date."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create files with specific modification times
            file1 = temp_path / "test1.jpg"
            file2 = temp_path / "test2.pdf"
            file1.touch()
            file2.touch()
            
            # Set fixed modification times
            # File 1: January 15, 2023
            mtime1 = datetime(2023, 1, 15, 10, 30, 0).timestamp()
            os.utime(file1, (mtime1, mtime1))
            
            # File 2: March 22, 2024
            mtime2 = datetime(2024, 3, 22, 14, 45, 0).timestamp()
            os.utime(file2, (mtime2, mtime2))
            
            organizer = FileOrganizer(temp_dir)
            result = organizer.organize_by_date(dry_run=False)
            
            # Check that files were moved correctly
            assert "2023/01/" in result
            assert "2024/03/" in result
            
            assert "test1.jpg" in result["2023/01/"]
            assert "test2.pdf" in result["2024/03/"]
            
            # Verify directories were created and files moved
            assert (temp_path / "2023" / "01" / "test1.jpg").exists()
            assert (temp_path / "2024" / "03" / "test2.pdf").exists()
            
            # Verify original files are gone
            assert not (temp_path / "test1.jpg").exists()
            assert not (temp_path / "test2.pdf").exists()

    def test_organize_by_date_idempotent(self):
        """Test that date organization is idempotent (can be run multiple times safely)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create a file with specific modification time
            file1 = temp_path / "test1.jpg"
            file1.touch()
            
            # Set fixed modification time: January 15, 2023
            mtime1 = datetime(2023, 1, 15, 10, 30, 0).timestamp()
            os.utime(file1, (mtime1, mtime1))
            
            organizer = FileOrganizer(temp_dir)
            
            # First run
            result1 = organizer.organize_by_date(dry_run=False)
            assert "2023/01/" in result1
            assert "test1.jpg" in result1["2023/01/"]
            
            # Second run - should not move anything since file is already in destination
            result2 = organizer.organize_by_date(dry_run=False)
            assert result2 == {}  # No files moved in second run
            
            # Verify file is still in the correct location
            assert (temp_path / "2023" / "01" / "test1.jpg").exists()

    def test_organize_by_date_same_month(self):
        """Test organizing multiple files from the same month."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create multiple files
            files = ["file1.jpg", "file2.pdf", "file3.py"]
            for filename in files:
                file_path = temp_path / filename
                file_path.touch()
                
                # Set all files to the same month (March 2024)
                mtime = datetime(2024, 3, 15, 12, 0, 0).timestamp()
                os.utime(file_path, (mtime, mtime))
            
            organizer = FileOrganizer(temp_dir)
            result = organizer.organize_by_date(dry_run=False)
            
            # All files should be in the same directory
            assert "2024/03/" in result
            assert len(result["2024/03/"]) == 3
            
            for filename in files:
                assert filename in result["2024/03/"]
                assert (temp_path / "2024" / "03" / filename).exists()
                assert not (temp_path / filename).exists()

"""Smoke tests for the file organizer package."""

import tempfile
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

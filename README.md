# File Organizer

A Python tool for automatically organizing files in your directories based on file types or modification dates.

## Features

- **Type-based organization**: Organize files by extension (images, documents, videos, etc.)
- **Date-based organization**: Sort files by modification date in YYYY/MM structure
- **Dry-run mode**: Preview changes before applying them
- **Safe operations**: Skip existing files, idempotent runs
- **Command-line interface**: Easy to use CLI with argparse

## Installation

```bash
# Clone the repository
git clone https://github.com/ethicalzeus07/file-organizer.git
cd file-organizer

# Install in development mode
pip install -e .
```

## Usage

### Basic Commands

```bash
# Organize files by type (default mode)
python3 -m file_organizer.cli --path /path/to/directory

# Organize files by modification date
python3 -m file_organizer.cli --path /path/to/directory --mode date

# Preview what would be organized (dry-run)
python3 -m file_organizer.cli --path /path/to/directory --dry-run

# Preview date-based organization
python3 -m file_organizer.cli --path /path/to/directory --mode date --dry-run
```

### Organization Modes

#### Type-based Organization (`--mode type`)

Files are organized into subdirectories based on their extensions:

- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`, `.svg` → `images/`
- **Documents**: `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt` → `documents/`
- **Videos**: `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`, `.flv`, `.webm` → `videos/`
- **Audio**: `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.m4a` → `audio/`
- **Archives**: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2` → `archives/`
- **Code**: `.py`, `.js`, `.html`, `.css`, `.java`, `.cpp`, `.c`, `.h` → `code/`
- **Spreadsheets**: `.xls`, `.xlsx`, `.csv`, `.ods` → `spreadsheets/`
- **Presentations**: `.ppt`, `.pptx`, `.odp` → `presentations/`
- **Other**: Unknown extensions → `other/`

#### Date-based Organization (`--mode date`)

Files are organized by their modification date in YYYY/MM directory structure:

```
/path/to/directory/
├── 2023/
│   ├── 01/
│   │   ├── file1.jpg
│   │   └── document.pdf
│   └── 12/
│       └── video.mp4
└── 2024/
    └── 03/
        ├── script.py
        └── archive.zip
```

### Examples

```bash
# Example 1: Organize Downloads folder by file type
python3 -m file_organizer.cli --path ~/Downloads

# Example 2: Organize Photos folder by date
python3 -m file_organizer.cli --path ~/Pictures --mode date

# Example 3: Preview type-based organization
python3 -m file_organizer.cli --path /tmp/messy_folder --mode type --dry-run

# Example 4: Preview date-based organization
python3 -m file_organizer.cli --path /tmp/messy_folder --mode date --dry-run
```

### Safety Features

- **Dry-run mode**: Always preview changes before applying them
- **Skip existing files**: Won't overwrite files that already exist in destination
- **Idempotent runs**: Safe to run multiple times on the same directory
- **Error handling**: Graceful handling of file operation failures

## Development

### Running Tests

```bash
# Install development dependencies
pip install pytest

# Run tests
python3 -m pytest tests/ -v
```

### Project Structure

```
file-organizer/
├── file_organizer/
│   ├── __init__.py
│   ├── organizer.py      # Core organization logic
│   └── cli.py           # Command-line interface
├── tests/
│   └── test_smoke.py    # Test suite
├── pyproject.toml       # Project configuration
└── README.md
```

## License

MIT License - see LICENSE file for details.

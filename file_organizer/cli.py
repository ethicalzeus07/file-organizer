"""Command-line interface for the file organizer."""

import argparse
import sys
from pathlib import Path

from .organizer import FileOrganizer


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.
    
    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        description="Organize files in a directory by type",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
  %(prog)s --path /path/to/directory --dry-run
  %(prog)s --path /path/to/directory --mode type
  %(prog)s --path /path/to/directory --mode date --dry-run
        """,
    )
    
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="Path to the directory containing files to organize",
    )
    
    parser.add_argument(
        "--mode",
        choices=["type", "date"],
        default="type",
        help="Organization mode: 'type' for file extension, 'date' for modification date (default: type)",
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be moved without actually moving files",
    )
    
    return parser


def main() -> None:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Validate path
    path = Path(args.path)
    if not path.exists():
        print(f"Error: Path '{args.path}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    if not path.is_dir():
        print(f"Error: Path '{args.path}' is not a directory", file=sys.stderr)
        sys.exit(1)
    
    try:
        organizer = FileOrganizer(path)
        
        # Choose organization method based on mode
        if args.mode == "type":
            mode_description = "by type"
            organize_func = organizer.organize_by_type
        elif args.mode == "date":
            mode_description = "by date (YYYY/MM)"
            organize_func = organizer.organize_by_date
        else:
            raise ValueError(f"Unknown mode: {args.mode}")
        
        if args.dry_run:
            print(f"Dry run mode: Previewing organization of files in '{path}' {mode_description}")
            print("-" * 50)
            moved_files = organize_func(dry_run=True)
            
            if not moved_files:
                print("No files to organize.")
            else:
                total_files = sum(len(files) for files in moved_files.values())
                print(f"\nSummary: {total_files} files would be organized into {len(moved_files)} categories")
        else:
            print(f"Organizing files in '{path}' {mode_description}...")
            print("-" * 50)
            moved_files = organize_func(dry_run=False)
            
            if not moved_files:
                print("No files to organize.")
            else:
                total_files = sum(len(files) for files in moved_files.values())
                print(f"\nSummary: {total_files} files organized into {len(moved_files)} categories")
                
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

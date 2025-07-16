"""
Main application module for get-lines
"""

import sys
import os
import argparse
from pathlib import Path
from typing import List, Tuple, Optional

from .scanner import FileScanner
from .counter import LineCounter
from .formatter import ReportFormatter


def parse_args() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Analyze code files and count lines in your project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  get-lines                    # Scan current directory
  get-lines --min 50           # Show only files with 50+ lines
  get-lines --min 100 /path    # Scan specific path, show 100+ line files
        """
    )
    
    parser.add_argument(
        "path",
        nargs="?",
        default=os.getcwd(),
        help="Path to scan (default: current directory)"
    )
    
    parser.add_argument(
        "--min",
        type=int,
        default=0,
        help="Minimum number of lines required to show a file in the report"
    )
    
    return parser.parse_args()


def main():
    """Main entry point for the get-lines application"""
    try:
        # Parse command line arguments
        args = parse_args()
        current_dir = Path(args.path).resolve()
        min_lines = args.min
        
        # Validate directory
        if not current_dir.exists():
            print(f"Error: Path '{current_dir}' does not exist", file=sys.stderr)
            sys.exit(1)
        
        if not current_dir.is_dir():
            print(f"Error: Path '{current_dir}' is not a directory", file=sys.stderr)
            sys.exit(1)
        
        # Initialize components
        scanner = FileScanner(current_dir)
        counter = LineCounter()
        formatter = ReportFormatter()
        
        # Show scanning info
        if min_lines > 0:
            formatter.show_info(f"Scanning directory: {current_dir} (showing files with {min_lines}+ lines)")
        else:
            formatter.show_info(f"Scanning directory: {current_dir}")
        
        # Scan for code files
        code_files = scanner.scan_files()
        
        if not code_files:
            formatter.format_report([])
            return
        
        # Count lines in each file and filter by min_lines
        file_data: List[Tuple[str, int]] = []
        processed_files = 0
        
        for file_path in code_files:
            line_count = counter.count_lines(file_path)
            if line_count is not None and line_count >= min_lines:
                relative_path = scanner.get_relative_path(file_path)
                file_data.append((relative_path, line_count))
                processed_files += 1
        
        # Show processing info
        total_filtered = len(code_files)
        if min_lines > 0:
            filtered_out = len(code_files) - processed_files
            if filtered_out > 0:
                formatter.show_info(f"Found {total_filtered} files, {processed_files} have {min_lines}+ lines, {filtered_out} filtered by minimum lines requirement")
        else:
            formatter.show_info(f"Processed {processed_files} files")
        
        # Format and display report
        formatter.format_report(file_data)
        
    except KeyboardInterrupt:
        formatter.show_error("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        formatter.show_error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
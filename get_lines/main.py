"""
Main application module for get-lines
"""

import sys
import os
from pathlib import Path
from typing import List, Tuple

from .scanner import FileScanner
from .counter import LineCounter
from .formatter import ReportFormatter


def main():
    """Main entry point for the get-lines application"""
    try:
        # Get current working directory
        current_dir = os.getcwd()
        
        # Initialize components
        scanner = FileScanner(current_dir)
        counter = LineCounter()
        formatter = ReportFormatter()
        
        # Show scanning info
        formatter.show_info(f"Scanning directory: {current_dir}")
        
        # Scan for code files
        code_files = scanner.scan_files()
        
        if not code_files:
            formatter.format_report([])
            return
        
        # Count lines in each file
        file_data: List[Tuple[str, int]] = []
        processed_files = 0
        
        for file_path in code_files:
            line_count = counter.count_lines(file_path)
            if line_count is not None:
                relative_path = scanner.get_relative_path(file_path)
                file_data.append((relative_path, line_count))
                processed_files += 1
        
        # Show processing info
        if processed_files != len(code_files):
            skipped = len(code_files) - processed_files
            formatter.show_info(f"Processed {processed_files} files, skipped {skipped} files (access denied or read errors)")
        
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
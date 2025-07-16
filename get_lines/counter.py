"""
Line counter module for counting lines in code files
"""

from pathlib import Path
from typing import Optional
import chardet


class LineCounter:
    
    def count_lines(self, file_path: Path) -> Optional[int]:
        """Count lines in a file with proper encoding detection"""
        try:
            # Try to detect encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read(8192)  # Read first 8KB for encoding detection
                if not raw_data:
                    return 0
                
                detected = chardet.detect(raw_data)
                encoding = detected.get('encoding', 'utf-8')
            
            # If detection failed, try common encodings
            if not encoding:
                encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
                for enc in encodings_to_try:
                    try:
                        with open(file_path, 'r', encoding=enc) as f:
                            return sum(1 for _ in f)
                    except (UnicodeDecodeError, UnicodeError):
                        continue
                return None
            
            # Count lines with detected encoding
            with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                return sum(1 for _ in f)
                
        except (OSError, IOError, PermissionError):
            return None
        except Exception:
            # Fallback: try to count as binary
            try:
                with open(file_path, 'rb') as f:
                    return sum(1 for _ in f)
            except Exception:
                return None
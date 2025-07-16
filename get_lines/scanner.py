"""
File scanner module for finding code files in directory structure
"""

import os
from pathlib import Path
from typing import List, Set, Optional
import pathspec


class FileScanner:
    
    CODE_EXTENSIONS = {
        '.py', '.pyx', '.pyi',  # Python
        '.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs',  # JavaScript/TypeScript
        '.java',  # Java
        '.c', '.cpp', '.cc', '.cxx', '.c++', '.h', '.hpp', '.hxx', '.h++',  # C/C++
        '.cs',  # C#
        '.go',  # Go
        '.rs',  # Rust
        '.php', '.php3', '.php4', '.php5', '.phtml',  # PHP
        '.rb', '.rbw',  # Ruby
        '.swift',  # Swift
        '.kt', '.kts',  # Kotlin
        '.scala', '.sc',  # Scala
        '.r', '.R',  # R
        '.m', '.mm',  # Objective-C
        '.sh', '.bash', '.zsh', '.fish',  # Shell scripts
        '.pl', '.pm',  # Perl
        '.lua',  # Lua
        '.dart',  # Dart
        '.elm',  # Elm
        '.ex', '.exs',  # Elixir
        '.erl', '.hrl',  # Erlang
        '.fs', '.fsx', '.fsi',  # F#
        '.hs', '.lhs',  # Haskell
        '.jl',  # Julia
        '.clj', '.cljs', '.cljc',  # Clojure
        '.ml', '.mli',  # OCaml
        '.pas', '.pp',  # Pascal
        '.asm', '.s',  # Assembly
        '.vb', '.vbs',  # Visual Basic
        '.groovy', '.gradle',  # Groovy
        '.vue',  # Vue.js
        '.svelte',  # Svelte
        '.sql',  # SQL
        '.xml', '.xsl', '.xslt',  # XML
        '.html', '.htm', '.xhtml',  # HTML
        '.css', '.scss', '.sass', '.less',  # CSS
        '.json', '.jsonc',  # JSON
        '.yaml', '.yml',  # YAML
        '.toml',  # TOML
        '.ini', '.cfg', '.conf',  # Configuration files
        '.dockerfile', '.containerfile',  # Docker
        '.vim',  # Vim script
        '.ps1', '.psm1',  # PowerShell
        '.bat', '.cmd',  # Windows batch
        '.makefile', '.mk',  # Makefile
        '.cmake',  # CMake
        '.proto',  # Protocol Buffers
        '.graphql', '.gql',  # GraphQL
        '.md', '.markdown',  # Markdown
        '.tex',  # LaTeX
        '.nim',  # Nim
        '.cr',  # Crystal
        '.d',  # D
        '.v',  # V
        '.zig',  # Zig
    }
    
    def __init__(self, root_path: str = '.'):
        self.root_path = Path(root_path).resolve()
        self.gitignore_spec = self._load_gitignore_patterns()
    
    def scan_files(self) -> List[Path]:
        """Scan directory tree for code files"""
        code_files = []
        
        try:
            for item in self.root_path.rglob('*'):
                if self._is_code_file(item) and not self._is_ignored(item):
                    code_files.append(item)
        except PermissionError:
            pass
        
        return code_files
    
    def _is_code_file(self, path: Path) -> bool:
        """Check if file is a code file based on extension"""
        if not path.is_file():
            return False
            
        # Check by extension
        if path.suffix.lower() in self.CODE_EXTENSIONS:
            return True
            
        # Check for files without extension that might be code
        if not path.suffix:
            filename = path.name.lower()
            # Common files without extensions
            no_ext_files = {
                'makefile', 'dockerfile', 'containerfile', 'rakefile',
                'gemfile', 'vagrantfile', 'berksfile', 'guardfile',
                'podfile', 'fastfile', 'appfile', 'deliverfile',
                'snapfile', 'scanfile', 'matchfile', 'gymfile'
            }
            if filename in no_ext_files:
                return True
        
        return False
    
    def get_relative_path(self, file_path: Path) -> str:
        """Get relative path from root directory"""
        try:
            return str(file_path.relative_to(self.root_path))
        except ValueError:
            return str(file_path)
    
    def _load_gitignore_patterns(self) -> Optional[pathspec.PathSpec]:
        """Load and parse .gitignore files"""
        patterns = []
        
        # Find all .gitignore files from root up to current directory
        current_path = self.root_path
        while True:
            gitignore_file = current_path / '.gitignore'
            if gitignore_file.exists():
                try:
                    with open(gitignore_file, 'r', encoding='utf-8', errors='ignore') as f:
                        gitignore_lines = f.read().splitlines()
                        # Add patterns with relative path context
                        for line in gitignore_lines:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                patterns.append(line)
                except (OSError, IOError, PermissionError):
                    pass
            
            # Move up to parent directory
            parent = current_path.parent
            if parent == current_path:  # Reached filesystem root
                break
            current_path = parent
        
        # Also check for global .gitignore
        if patterns:
            try:
                return pathspec.PathSpec.from_lines('gitwildmatch', patterns)
            except Exception:
                return None
        
        return None
    
    def _is_ignored(self, file_path: Path) -> bool:
        """Check if file should be ignored based on .gitignore patterns"""
        if self.gitignore_spec is None:
            return False
        
        try:
            # Get relative path for pattern matching
            relative_path = str(file_path.relative_to(self.root_path))
            # Normalize path separators for cross-platform compatibility
            relative_path = relative_path.replace('\\', '/')
            
            # Check if file matches any ignore pattern
            return self.gitignore_spec.match_file(relative_path)
        except (ValueError, Exception):
            return False
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Commands

### Development & Testing
- `python -m pip install -e .` - Install in development mode
- `python -m get_lines.main` - Run directly from source
- `get-lines` - Run installed CLI command
- `python -m pytest tests/` - Run tests (if they exist)
- `python -c "import get_lines; get_lines.counter.LineCounter().count_lines(get_lines/__init__.py)"` - Test line counting

### Build & Distribution
- `python setup.py bdist_wheel` - Build wheel
- `python -m build` - Modern build system
- `twine upload dist/*` - Publish to PyPI

## Architecture Overview

**get-lines** is a Python CLI tool that analyzes codebases by counting lines in support files. The architecture follows a clean separation of concerns with distinct modules:

### Module Structure
- `main.py:main()` - Entry point orchestrator
- `scanner.py:FileScanner` - File discovery with 80+ extension support and .gitignore integration
- `counter.py:LineCounter` - Line counting with intelligent encoding detection
- `formatter.py:ReportFormatter` - Rich terminal formatting and analysis display

### Key Design Decisions
- **Rich Console**: Terminal formatting using the `rich` library for beautiful tables
- **Git Integration**: Respects .gitignore patterns from any directory level
- **Cross-platform**: Works on Windows/Linux with proper path handling
- **Encoding Resilience**: Uses `chardet` for character encoding detection with fallback encoding strategies
- **Extension-based filtering**: 69 supported extensions plus special files (Dockerfile, Makefile, etc.)

### Dependencies
- `rich>=10.0.0` - Terminal formatting and tables
- `chardet>=4.0.0` - Character encoding detection
- `pathspec>=0.9.0` - .gitignore pattern matching
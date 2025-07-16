# get-lines

A powerful Python tool to analyze code files and count lines in your project. Instantly identify large files that may be candidates for refactoring.

## Features

- 🔍 **Comprehensive File Support**: Supports all major programming languages and file types
- 📊 **Beautiful Terminal Output**: Rich, colored tables with clear formatting
- 🚀 **Zero Configuration**: Just run and get results immediately
- 🔄 **Cross-Platform**: Works on Windows (PowerShell) and Linux (Bash)
- 📈 **Smart Analysis**: Identifies refactoring candidates and provides summary statistics
- 🎯 **Performance Optimized**: Fast scanning even for large codebases

## Installation

Install via pip:

```bash
pip install get-lines
```

## Usage

Navigate to your project directory and run:

```bash
get-lines
```

That's it! The tool will:
1. Scan the current directory and all subdirectories
2. Find all code files
3. Count lines in each file
4. Display a beautiful report sorted by line count (largest first)
5. Show refactoring candidates and summary statistics

## Supported File Types

The tool supports over 80 file extensions including:

- **Python**: `.py`, `.pyx`, `.pyi`
- **JavaScript/TypeScript**: `.js`, `.jsx`, `.ts`, `.tsx`, `.mjs`, `.cjs`
- **Java**: `.java`
- **C/C++**: `.c`, `.cpp`, `.cc`, `.cxx`, `.h`, `.hpp`
- **C#**: `.cs`
- **Go**: `.go`
- **Rust**: `.rs`
- **PHP**: `.php`, `.php3`, `.php4`, `.php5`, `.phtml`
- **Ruby**: `.rb`, `.rbw`
- **Swift**: `.swift`
- **Kotlin**: `.kt`, `.kts`
- **Scala**: `.scala`, `.sc`
- **R**: `.r`, `.R`
- **Shell**: `.sh`, `.bash`, `.zsh`, `.fish`
- **Web**: `.html`, `.css`, `.scss`, `.sass`, `.vue`, `.svelte`
- **Config**: `.json`, `.yaml`, `.yml`, `.toml`, `.xml`
- **And many more...**

## Example Output

```
                           Code Lines Analysis Report                           
┌─────────────────────────────────────┬────────┬─────────────────┐
│ File Path                           │  Lines │ Size Indicator  │
├─────────────────────────────────────┼────────┼─────────────────┤
│ src/main/java/Application.java      │  1,547 │ 🔥 Large        │
│ frontend/src/components/Dashboard.js│    892 │ ⚠️  Medium       │
│ backend/models/user.py              │    456 │ 📄 Small        │
│ utils/helpers.js                    │    123 │ 📝 Tiny         │
└─────────────────────────────────────┴────────┴─────────────────┘

                                    Summary                                     
Total Files:                   47
Total Lines:                   12,456
Average Lines per File:        264
Largest File:                  src/main/java/Application.java (1,547 lines)

🔧 Refactoring Candidates (>500 lines):
  • src/main/java/Application.java (1,547 lines)
  • frontend/src/components/Dashboard.js (892 lines)
```

## Requirements

- Python 3.7+
- Rich library (automatically installed with pip)

## License

MIT License
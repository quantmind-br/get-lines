"""
Terminal formatter module for beautiful output display
"""

from typing import List, Tuple
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box


class ReportFormatter:
    
    def __init__(self):
        self.console = Console(force_terminal=True, legacy_windows=False)
    
    def format_report(self, file_data: List[Tuple[str, int]]) -> None:
        """Format and display the report with beautiful terminal output"""
        if not file_data:
            self.console.print("[yellow]No code files found in the current directory.[/yellow]")
            return
        
        # Sort by line count (descending)
        sorted_data = sorted(file_data, key=lambda x: x[1], reverse=True)
        
        # Create table
        table = Table(
            title="[bold blue]Code Lines Analysis Report[/bold blue]",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )
        
        table.add_column("File Path", style="cyan", no_wrap=False, min_width=30)
        table.add_column("Lines", style="green", justify="right", min_width=10)
        table.add_column("Size Indicator", style="yellow", justify="center", min_width=15)
        
        total_lines = 0
        total_files = len(sorted_data)
        
        for file_path, line_count in sorted_data:
            total_lines += line_count
            
            # Add size indicator
            if line_count > 1000:
                size_indicator = "[red]Large[/red]"
            elif line_count > 500:
                size_indicator = "[yellow]Medium[/yellow]"
            elif line_count > 100:
                size_indicator = "[blue]Small[/blue]"
            else:
                size_indicator = "[dim]Tiny[/dim]"
            
            # Format line count with separators
            formatted_lines = f"{line_count:,}"
            
            table.add_row(
                file_path,
                formatted_lines,
                size_indicator
            )
        
        # Display the table
        self.console.print()
        self.console.print(table)
        
        # Display summary
        self.console.print()
        summary_table = Table(
            title="[bold green]Summary[/bold green]",
            box=box.SIMPLE,
            show_header=False
        )
        summary_table.add_column("", style="bold")
        summary_table.add_column("", style="cyan")
        
        summary_table.add_row("Total Files:", f"{total_files:,}")
        summary_table.add_row("Total Lines:", f"{total_lines:,}")
        
        if total_files > 0:
            avg_lines = total_lines // total_files
            summary_table.add_row("Average Lines per File:", f"{avg_lines:,}")
        
        # Show largest files (top 3)
        if len(sorted_data) > 0:
            largest_file = sorted_data[0]
            summary_table.add_row("Largest File:", f"{largest_file[0]} ({largest_file[1]:,} lines)")
        
        self.console.print(summary_table)
        self.console.print()
        
        # Show refactoring candidates
        refactor_candidates = [item for item in sorted_data if item[1] > 500]
        if refactor_candidates:
            self.console.print("[bold red]Refactoring Candidates (>500 lines):[/bold red]")
            for file_path, line_count in refactor_candidates[:5]:  # Show top 5
                self.console.print(f"  - [cyan]{file_path}[/cyan] ([red]{line_count:,} lines[/red])")
            if len(refactor_candidates) > 5:
                self.console.print(f"  ... and {len(refactor_candidates) - 5} more files")
            self.console.print()
    
    def show_error(self, message: str) -> None:
        """Display error message"""
        self.console.print(f"[bold red]Error:[/bold red] {message}")
    
    def show_info(self, message: str) -> None:
        """Display info message"""
        self.console.print(f"[blue]Info:[/blue] {message}")
import random
import copy
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()

class mines:
    def __init__(self, mines=2, level='basic'):
        self.mines = mines
        self.level = level
        self.started_at = time.time()
        self.end = None
        self.moves_made = 0
        self.invalid_moves = 0
        self.size = 4 if self.level == "basic" else 9
        
        # Create a blank player-facing grid
        self.grid = [["." for _ in range(self.size)] for _ in range(self.size)]
        
        # Hide mine locations in a separate set for instant lookups
        self.mine_positions = self._place_mines()
        
    def _place_mines(self):
        positions = set()
        # Ensure we don't accidentally create an infinite loop if mines exceed grid capacity
        max_mines = (self.size * self.size) - 1
        actual_mines = min(self.mines, max_mines)
        
        while len(positions) < actual_mines:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            positions.add((row, col))
        return positions

    def show(self):
        console.clear()
        title = Text("🧩 MINES CHOOSE CORRECT STEP 🧩", style="bold yellow")
        status = f"Level: {self.level.upper()} | Mines: {self.mines} | Moves: {self.moves_made}"
        console.print(Panel(title, subtitle=status))
        self.render_grid()

    def render_grid(self):
        table = Table(show_header=True, show_lines=True)
        
        # Add index header column for tracking columns easily
        table.add_column("", justify="center", width=3)
        for i in range(self.size):
            table.add_column(f"[bold cyan]{i}[/bold cyan]", justify="center", width=3)
            
        for r_idx, row in enumerate(self.grid):
            # Row index label
            cells = [f"[bold cyan]{r_idx}[/bold cyan]"]
            for value in row:
                if value == ".":
                    cells.append("[dim].[/dim]")
                elif value == "💣":
                    cells.append("[bold red]💣[/bold red]")
                elif value == "0":
                    cells.append("[dim green]0[/dim green]")
                else:
                    cells.append(f"[bold green]{value}[/bold green]")
            table.add_row(*cells)
        console.print(table)

    def _count_adjacent_mines(self, row, col):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < self.size and 0 <= c < self.size:
                    if (r, c) in self.mine_positions:
                        count += 1
        return count

    def _check_win(self):
        # Win if all non-mine cells are revealed
        revealed_cells = sum(1 for row in self.grid for val in row if val != ".")
        target_cells = (self.size * self.size) - len(self.mine_positions)
        return revealed_cells == target_cells

    def _reveal_all_mines(self):
        for (r, c) in self.mine_positions:
            self.grid[r][c] = "💣"

    def play(self):
        while True:
            self.show()
            
            # Get user input
            try:
                user_input = console.input("[bold white]Enter row and column numbers split by space (e.g., 0 2) or 'q' to quit: [/bold white]").strip()
                if user_input.lower() == 'q':
                    console.print("[yellow]Game exited by player.[/yellow]")
                    break
                
                parts = user_input.split()
                if len(parts) != 2:
                    raise ValueError
                
                row, col = int(parts[0]), int(parts[1])
                
                if not (0 <= row < self.size and 0 <= col < self.size):
                    console.print("[red]Coordinates are out of bounds![/red]")
                    self.invalid_moves += 1
                    time.sleep(1.5)
                    continue
                    
            except ValueError:
                console.print("[red]Invalid entry format. Provide two numbers separated by a space.[/red]")
                self.invalid_moves += 1
                time.sleep(1.5)
                continue

            # Skip if cell is already opened
            if self.grid[row][col] != ".":
                console.print("[yellow]Tile already selected. Choose a hidden tile.[/yellow]")
                time.sleep(1.2)
                continue

            self.moves_made += 1

            # Hit a mine condition
            if (row, col) in self.mine_positions:
                self._reveal_all_mines()
                self.show()
                duration = round(time.time() - self.started_at, 1)
                console.print(Panel("[bold red]💥 BOOM! You stepped on a mine. GAME OVER! 💥[/bold red]", 
                                    subtitle=f"Time survived: {duration}s"))
                break

            # Safe move execution
            adjacent_count = self._count_adjacent_mines(row, col)
            self.grid[row][col] = str(adjacent_count)

            # Win check condition
            if self._check_win():
                self.show()
                duration = round(time.time() - self.started_at, 1)
                console.print(Panel("[bold gold1]🎉 CONGRATULATIONS! You cleared the field and won! 🎉[/bold gold1]", 
                                    subtitle=f"Completed in {duration}s with {self.moves_made} moves!"))
                break

# Run advanced layout
mines(mines=3, level='basic').play()

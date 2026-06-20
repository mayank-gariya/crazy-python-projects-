
import random
import copy
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
import time

console = Console()


class Sudoku:
    def __init__(self, level="basic"):
        self.level = level
        self.grid = self._generate_grid()
        self.original_grid = copy.deepcopy(self.grid)
        
        self.start_time = time.time()
        self.end_time = None

        self.hints_used = 0
        self.moves_made = 0
        self.invalid_moves = 0

    def _generate_grid(self):
        if self.level == "basic":
            puzzles = [
                [
                    [1, 0, 0, 4],
                    [0, 4, 1, 0],
                    [2, 0, 4, 3],
                    [0, 3, 0, 1],
                ],
                [
                    [0, 2, 0, 4],
                    [4, 0, 2, 0],
                    [0, 4, 0, 2],
                    [2, 0, 3, 0],
                ],
            ]
        else:
            puzzles = [[
                [5,3,0,0,7,0,0,0,0],
                [6,0,0,1,9,5,0,0,0],
                [0,9,8,0,0,0,0,6,0],
                [8,0,0,0,6,0,0,0,3],
                [4,0,0,8,0,3,0,0,1],
                [7,0,0,0,2,0,0,0,6],
                [0,6,0,0,0,0,2,8,0],
                [0,0,0,4,1,9,0,0,5],
                [0,0,0,0,8,0,0,7,9],
            ]]
        return copy.deepcopy(random.choice(puzzles))

    def render_grid(self):
        size = 4 if self.level == "basic" else 9

        table = Table(show_header=False, show_lines=True)

        for _ in range(size):
            table.add_column(justify="center")

        for row in self.grid:
            cells = []
            for value in row:
                cells.append(f"[bold green]{value}[/bold green]" if value else "[dim].[/dim]")
            table.add_row(*cells)

        console.print(table)
            
    def show(self):
        title = Text("🧩 SUDOKU CHAMPION 🧩", style="bold yellow")
        console.print(Panel(title, subtitle=f"Level: {self.level.upper()}"))
        self.render_grid()
    

    def is_valid_move(self, row, col, num):
        size = 4 if self.level == "basic" else 9
        box = 2 if self.level == "basic" else 3

        for c in range(size):
            if self.grid[row][c] == num and c != col:
                return False

        for r in range(size):
            if self.grid[r][col] == num and r != row:
                return False

        sr = (row // box) * box
        sc = (col // box) * box

        for r in range(sr, sr + box):
            for c in range(sc, sc + box):
                if self.grid[r][c] == num and (r, c) != (row, col):
                    return False

        return True
    
    def show_summary(self):

        self.end_time = time.time()

        total_seconds = int(self.end_time - self.start_time)

        minutes = total_seconds // 60
        seconds = total_seconds % 60

        total_attempts = self.moves_made + self.invalid_moves

        accuracy = (
            (self.moves_made / total_attempts) * 100
            if total_attempts > 0
            else 100
        )

        score = max(
            1000
            - (self.hints_used * 50)
            - (self.invalid_moves * 20),
            0
        )

        stars = "⭐"

        if score >= 500:
            stars = "⭐⭐"

        if score >= 800:
            stars = "⭐⭐⭐"

        if score >= 900:
            rank = "👑 Grandmaster"

        elif score >= 750:
            rank = "🥇 Sudoku Master"

        elif score >= 600:
            rank = "🥈 Sudoku Expert"

        elif score >= 400:
            rank = "🥉 Sudoku Player"

        else:
            rank = "🎯 Beginner"

        summary = Table(
            show_header=True,
            header_style="bold cyan"
        )

        summary.add_column("Metric", style="bold yellow")
        summary.add_column("Value", justify="center")

        summary.add_row("🎮 Difficulty", self.level.upper())
        summary.add_row("⏱ Time Taken", f"{minutes}m {seconds}s")
        summary.add_row("✅ Moves Made", str(self.moves_made))
        summary.add_row("💡 Hints Used", str(self.hints_used))
        summary.add_row("❌ Invalid Moves", str(self.invalid_moves))
        summary.add_row("🎯 Accuracy", f"{accuracy:.1f}%")
        summary.add_row("⭐ Rating", stars)
        summary.add_row("🏆 Final Score", str(score))

        console.print()

        console.print(
            Panel.fit(
                summary,
                title="🎉 VICTORY SUMMARY 🎉",
                border_style="green"
            )
        )

        console.print()

        console.print(
            Panel.fit(
                f"[bold green]{rank}[/bold green]",
                title="🏅 Achievement Unlocked",
                border_style="yellow"
            )
        )

        console.print()

        if score >= 900:
            console.print(
                "[bold bright_green]Perfect performance! You dominated this puzzle! 🚀[/bold bright_green]"
            )

        elif score >= 750:
            console.print(
                "[bold cyan]Excellent work! Very few mistakes. 🔥[/bold cyan]"
            )

        elif score >= 600:
            console.print(
                "[bold yellow]Good job! Keep practicing to reach Master level. 💪[/bold yellow]"
            )

        else:
            console.print(
                "[bold magenta]Every solved puzzle makes you better. Keep going! 🎯[/bold magenta]"
            )


    def place_number(self, row, col, num):
        size = 4 if self.level == "basic" else 9

        if not (1 <= num <= size):
            console.print(
                f"[red]Number must be between 1 and {size}![/red]"
            )
            self.invalid_moves += 1
            return False

        if self.original_grid[row][col] != 0:
            console.print("[red]Cannot modify original cell![/red]")
            self.invalid_moves += 1
            return False

        if self.is_valid_move(row, col, num):

            self.grid[row][col] = num
            self.moves_made += 1
            return True

        self.invalid_moves += 1
        console.print("[red]Invalid move![/red]")
        return False

    def find_empty(self):
        size = 4 if self.level == "basic" else 9
        for r in range(size):
            for c in range(size):
                if self.grid[r][c] == 0:
                    return r, c
        return None

    def solve(self):
        empty = self.find_empty()
        if not empty:
            return True

        row, col = empty
        size = 4 if self.level == "basic" else 9

        for num in range(1, size + 1):
            if self.is_valid_move(row, col, num):
                self.grid[row][col] = num

                if self.solve():
                    return True

                self.grid[row][col] = 0
        

        return False

    def hint(self):

        self.hints_used += 1

        temp = copy.deepcopy(self.grid)

        if self.solve():

            for r in range(len(temp)):
                for c in range(len(temp[r])):

                    if temp[r][c] == 0:

                        console.print(
                            f"[cyan]💡 Hint:[/cyan] Row {r+1}, Col {c+1} = {self.grid[r][c]}"
                        )

                        self.grid = temp
                        return

        self.grid = temp

    def is_completed(self):
        size = 4 if self.level == "basic" else 9

        for r in range(size):
            for c in range(size):
                value = self.grid[r][c]
                if value == 0:
                    return False

                self.grid[r][c] = 0
                valid = self.is_valid_move(r, c, value)
                self.grid[r][c] = value

                if not valid:
                    return False
        return True

    def play(self):
        while True:
            console.clear()
            self.show()
            
            if self.is_completed():

                console.print(
                    "\n[bold green]🎉 Congratulations! You solved the Sudoku![/bold green]"
                )

                self.show_summary()

                break

            console.print("\n[yellow]Commands:[/yellow]")
            console.print("row col value  -> place number")
            console.print("hint           -> get a hint")
            console.print("solve          -> auto solve")
            console.print("q              -> quit")

            cmd = input("\n> ").strip().lower()

            if cmd == "q":
                break

            if cmd == "hint":
                self.hint()
                input("Press Enter...")
                continue

            if cmd == "solve":
                self.solve()
                continue

            try:
                row, col, value = map(int, cmd.split())
                self.place_number(row - 1, col - 1, value)
            except Exception:
                console.print("[red]Invalid input![/red]")
                input("Press Enter...")


if __name__ == "__main__":
    level = input("Choose difficulty (basic/advanced): ").strip().lower()
    if level not in ["basic", "advanced"]:
        level = "basic"

    Sudoku(level).play()
    
    
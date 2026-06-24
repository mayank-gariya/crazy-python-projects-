import random
import copy
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import time

console = Console()


class Shift_block:
    def __init__(self):
        self.target = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]

        self.board = copy.deepcopy(self.target)

        # Make some random moves to shuffle
        for _ in range(30):
            self.random_move()

        self.moves = 0
        self.start = time.time()

    def display(self):
        table = Table(title="Sliding Puzzle")

        for _ in range(3):
            table.add_column(justify="center")

        for row in self.board:
            display_row = []
            for num in row:
                if num == 0:
                    display_row.append(" ")
                else:
                    display_row.append(str(num))

            table.add_row(*display_row)

        console.print(table)

    def find_zero(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j

    def move(self, direction):
        x, y = self.find_zero()

        if direction == "w" and x > 0:
            self.board[x][y], self.board[x - 1][y] = (
                self.board[x - 1][y],
                self.board[x][y],
            )
            return True

        elif direction == "s" and x < 2:
            self.board[x][y], self.board[x + 1][y] = (
                self.board[x + 1][y],
                self.board[x][y],
            )
            return True

        elif direction == "a" and y > 0:
            self.board[x][y], self.board[x][y - 1] = (
                self.board[x][y - 1],
                self.board[x][y],
            )
            return True

        elif direction == "d" and y < 2:
            self.board[x][y], self.board[x][y + 1] = (
                self.board[x][y + 1],
                self.board[x][y],
            )
            return True

        return False

    def random_move(self):
        directions = ["w", "a", "s", "d"]
        self.move(random.choice(directions))

    def is_solved(self):
        return self.board == self.target

    def start_game(self):
        console.print(
            Panel.fit(
                "Use [bold green]W A S D[/bold green] keys to move the tiles.\n"
                "Arrange the numbers in order.\n"
                "Press [bold red]q[/bold red] to quit."
            )
        )

        while True:
            self.display()

            if self.is_solved():
                end = time.time()
                console.print(
                    f"\n🎉 Congratulations! Puzzle solved in "
                    f"{self.moves} moves and "
                    f"{round(end-self.start,2)} seconds."
                )
                break

            move = input("Move (w/a/s/d): ").lower()

            if move == "q":
                console.print("Game exited.")
                break

            if move not in ["w", "a", "s", "d"]:
                console.print("[red]Invalid input![/red]")
                continue

            if self.move(move):
                self.moves += 1
            else:
                console.print("[yellow]Cannot move in that direction![/yellow]")


game = Shift_block()
game.start_game()
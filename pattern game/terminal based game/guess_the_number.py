import random
import time
import numpy as np
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()

class guss_the_number:
    def __init__(self, upper_range=100):
        self.upper_range = upper_range
        self.started_at = time.time()
        self.end_time = None

    def start_game(self):
        # show the headings for the game
        self.show()
        # first get the number
        number = random.randint(0, self.upper_range)
        count = 1
        difference = []

        while True:
            try:
                user_guess = int(input('Guess your number: '))
            except ValueError:
                console.print("[bold red]Invalid input! Please enter a valid integer.[/bold red]")
                continue

            distance = self._get_distances(user_number=user_guess, number=number)
            difference.append(distance)
            
            if self._validation(user_guess, number) is True:
                break
            count += 1

        # summary - result
        self._show_summary(number=number, count=count, differences=difference)

    def show(self):
        title = Text(' 🧐 Guess the number, I bet you cannot guess the number 😎')
        console.print(Panel(title, border_style='red', style='bold yellow'))

    def _show_summary(self, number, count, differences):
        self.end_time = time.time()
        total_seconds = int(self.end_time - self.started_at)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        
        trials = count
        Mae = np.mean(differences)
        Std_error = np.std(differences)
        
        summary = Table(show_header=True, header_style="bold cyan")
        summary.add_column("Metric", style="bold yellow")
        summary.add_column("Value", justify="center")
        
        summary.add_row('🎮 Trials', str(trials))        
        summary.add_row("⏱ Time Taken", f"{minutes}m {seconds}s")
        summary.add_row("🎯 Mean error", f"{Mae:.1f}")
        summary.add_row("⭐ Standard deviation error", f'{Std_error:.1f}')
        summary.add_row("🏆 Number was", str(number))
        
        console.print()
        console.print(
            Panel.fit(
                summary,
                title="🎉 VICTORY SUMMARY 🎉",
                border_style="green"
            )
        )

    def _get_distances(self, user_number, number):
        return abs(user_number - number)

    def _validation(self, user_num, number):
        if user_num > number:
            console.print(f'[bold magenta]Your guess {user_num} is [bold yellow]higher[/bold yellow] than actual number[/bold magenta]')
            return False
        elif user_num < number:
            console.print(f'[bold magenta]Your guess {user_num} is [bold yellow]lower[/bold yellow] than actual number[/bold magenta]')
            return False
        else:
            console.print(f'[bold blue]You guessed the number correctly! Original number was {number} [bold yellow]Hurray! You won the game 🤗😝[/bold yellow][/bold blue]')
            return True

if __name__ == "__main__":
    guss_the_number().start_game()

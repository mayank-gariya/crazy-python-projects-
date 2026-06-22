import random
import time 
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.live import Live
from rich.table import Table

console = Console()

class RememberNumber:
    def __init__(self, upper=100, display_time=2):
        self.upper = upper
        self.number = None
        self.time = display_time
        
    def show_header(self):
        """Displays a stylish game header with instructions."""

        table = Table.grid(padding=1)
        table.add_column(style="cyan", justify="right")
        table.add_column(style="white")
        
        table.add_row("🎯 Goal:", "Memorise the number before it vanishes!")
        table.add_row("⏳ Time:", f"You only have [bold yellow]{self.time} seconds[/bold yellow].")
        table.add_row("🔢 Range:", f"Numbers range from [bold yellow]0 to {self.upper}[/bold yellow].")
        
        # Wrap everything in a main title panel
        header_panel = Panel(
            table,
            title="✨ [bold magenta]NUM-FLASH MEMORY GAME[/bold magenta] ✨",
            subtitle="[italic dim]Test your brain speed[/italic dim]",
            border_style="magenta",
            expand=False
        )
        console.print(header_panel)
        console.print("\n" + "─" * 45 + "\n") # Decorative separator line
    
    def startgame(self):
        # 1. Print the game header first
        self.show_header()
        
        self.number = random.randint(0, self.upper)
        
        # 2. Countdown and flash sequence
        with Live(auto_refresh=False) as live:
            live.update(Panel("[bold yellow]Ready...[/bold yellow]", expand=False), refresh=True)
            time.sleep(1.5)
            
            live.update(Panel("[bold orange3]Steady...[/bold orange3]", expand=False), refresh=True)
            time.sleep(1.5)
            
            # Flash the Number
            number_panel = Panel(f"[bold magenta size=20]  {self.number}  [/bold magenta size=20]", title="👉 REMEMBER THIS 👈", border_style="cyan", expand=False)
            live.update(number_panel, refresh=True)
            time.sleep(self.time)
            
            # Force disappear
            live.update("", refresh=True)

        # 3. Prompt for answer
        user_input = Prompt.ask("[bold green]Enter the number you saw[/bold green]")
        
        try:
            user_num = int(user_input)
        except ValueError:
            console.print("[bold red]❌ Invalid input! You lose.[/bold red]")
            return
        
        # 4. Results
        if user_num == self.number:
            console.print(Panel(f"[bold green]🎉 Perfect! It was {self.number}. You win![/bold green]", border_style="green"))
        else:
            console.print(Panel(f"[bold red]❌ Wrong! You entered {user_num}, but it was {self.number}.[/bold red]", border_style="red"))

RememberNumber().startgame()

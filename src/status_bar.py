from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from datetime import datetime
import psutil
import asyncio

console = Console()

class StatusBar:
    def __init__(self):
        self.cpu_percent = 0
        self.memory_percent = 0
        self.active_contracts = 0
        self.wallet_balance = "0.00"
        self.network_status = "CONNECTED"
        self.last_update = datetime.now()

    def create_status_panel(self) -> Panel:
        """Create a status panel with system information"""
        status_content = f"""[cyan]System Status[/cyan]
• CPU: [yellow]{self.cpu_percent}%[/yellow]
• Memory: [yellow]{self.memory_percent}%[/yellow]
• Network: [green]{self.network_status}[/green]
• Active Contracts: [cyan]{self.active_contracts}[/cyan]
• Wallet Balance: [green]{self.wallet_balance} SOL[/green]
• Last Update: [dim]{self.last_update.strftime('%H:%M:%S')}[/dim]"""
        
        return Panel(status_content, title="[bold cyan]ICA Terminal Status[/bold cyan]", border_style="cyan")

    async def update_status(self):
        """Update system status information"""
        while True:
            self.cpu_percent = psutil.cpu_percent()
            self.memory_percent = psutil.virtual_memory().percent
            self.last_update = datetime.now()
            await asyncio.sleep(1)

    def get_layout(self) -> Layout:
        """Create a layout with the status panel"""
        layout = Layout()
        layout.update(self.create_status_panel())
        return layout

async def create_status_bar():
    """Create and return a new status bar instance"""
    status_bar = StatusBar()
    # Start the update task in the background
    asyncio.create_task(status_bar.update_status())
    return status_bar

if __name__ == "__main__":
    # Test the status bar
    async def main():
        status_bar = await create_status_bar()
        with Live(status_bar.get_layout(), refresh_per_second=1):
            await asyncio.sleep(10)

    asyncio.run(main())
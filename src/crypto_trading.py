from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from datetime import datetime
import questionary
from typing import Dict, List, Any
import asyncio
import random
import logging

console = Console()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CryptoTradingContract:
    def __init__(self):
        self.active_trades = 0
        self.profit_loss = 0.0
        self.active_bots = 0
        self.market_status = "ONLINE"

    def create_status_display(self) -> Panel:
        """Create a rich panel with current trading status"""
        status_content = f"""[cyan]Trading Status[/cyan]
• Active Trades: [yellow]{self.active_trades}[/yellow]
• P/L: [{'green' if self.profit_loss >= 0 else 'red'}]{self.profit_loss:+.2f}%[/{'green' if self.profit_loss >= 0 else 'red'}]
• Active Bots: [yellow]{self.active_bots}[/yellow]
• Market Status: [{'green' if self.market_status == "ONLINE" else 'red'}]{self.market_status}[/{'green' if self.market_status == "ONLINE" else 'red'}]
• Last Update: [cyan]{datetime.now().strftime('%H:%M:%S')}[/cyan]"""
        
        return Panel(status_content, title="[bold cyan]Crypto Trading Dashboard[/bold cyan]", border_style="cyan")

    def create_market_table(self) -> Table:
        """Create a rich table with market information"""
        table = Table(title="Market Overview")
        table.add_column("Pair", style="cyan")
        table.add_column("Price", justify="right")
        table.add_column("24h Change", justify="right")
        table.add_column("Signal", justify="center")
        
        # Sample data - would be replaced with real API data
        table.add_row("BTC/USDT", "$45,123.45", "+2.34%", "🟢 BUY")
        table.add_row("ETH/USDT", "$2,845.67", "-1.23%", "🔴 SELL")
        table.add_row("SOL/USDT", "$98.76", "+5.67%", "🟢 BUY")
        
        return table

    async def update_dashboard(self, live: Live):
        """Update the dashboard with simulated data periodically"""
        while True:
            self.active_trades = random.randint(0, 10)
            self.profit_loss = random.uniform(-5, 5)
            self.active_bots = random.randint(0, 5)
            self.market_status = random.choice(["ONLINE", "OFFLINE", "MAINTENANCE"])
            
            layout = Layout()
            layout.split_column(
                Layout(name="upper"),
                Layout(name="lower")
            )
            layout["upper"].update(self.create_status_display())
            layout["lower"].update(self.create_market_table())
            live.update(layout)
            await asyncio.sleep(5)  # Update every 5 seconds

    async def display_trading_dashboard(self, live: Live):
        """Display live trading dashboard"""
        console.clear()
        layout = Layout()
        layout.split_column(
            Layout(name="upper"),
            Layout(name="lower")
        )
        layout["upper"].update(self.create_status_display())
        layout["lower"].update(self.create_market_table())
        live.update(layout)

    async def configure_bot_parameters(self) -> Dict[str, Any]:
        """Configure trading bot parameters"""
        questions = [
            {
                'type': 'list',
                'name': 'strategy',
                'message': 'Select Trading Strategy:',
                'choices': [
                    'Grid Trading',
                    'DCA (Dollar Cost Averaging)',
                    'Momentum Trading',
                    'Arbitrage Trading',
                    'Back'
                ]
            },
            {
                'type': 'input',
                'name': 'investment',
                'message': 'Maximum Investment (USDT):',
                'validate': lambda x: float(x) > 0,
                'when': lambda answers: answers['strategy'] != 'Back'
            },
            {
                'type': 'list',
                'name': 'risk_level',
                'message': 'Risk Level:',
                'choices': ['Low', 'Medium', 'High'],
                'when': lambda answers: answers['strategy'] != 'Back'
            },
            {
                'type': 'checkbox',
                'name': 'trading_pairs',
                'message': 'Select Trading Pairs:',
                'choices': ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'ADA/USDT'],
                'when': lambda answers: answers['strategy'] != 'Back'
            }
        ]
        
        answers = await questionary.prompt(questions)
        if answers['strategy'] != 'Back':
            console.print(Panel(f"""
[cyan]Bot Configuration Summary[/cyan]
• Strategy: [yellow]{answers['strategy']}[/yellow]
• Investment: [green]{answers['investment']} USDT[/green]
• Risk Level: [yellow]{answers['risk_level']}[/yellow]
• Trading Pairs: [cyan]{', '.join(answers['trading_pairs'])}[/cyan]
            """, title="Bot Configuration"))
            
            await self.confirm_and_deploy_bot(answers)
        
        return answers

    async def confirm_and_deploy_bot(self, config: Dict[str, Any]):
        """Confirm and deploy trading bot"""
        confirm = await questionary.prompt([
            {
                'type': 'confirm',
                'name': 'deploy',
                'message': 'Deploy trading bot with these parameters?',
                'default': False
            }
        ])
        
        if confirm['deploy']:
            with console.status("[bold green]Deploying trading bot..."):
                # Simulated deployment delay
                await asyncio.sleep(2)
                self.active_bots += 1
                console.print("[green]Trading bot successfully deployed![/green]")
        else:
            console.print("[yellow]Deployment canceled.[/yellow]")

    async def view_trading_history(self):
        """Display trading history"""
        table = Table(title="Recent Trading History")
        table.add_column("Time", style="cyan")
        table.add_column("Pair")
        table.add_column("Type", justify="center")
        table.add_column("Price", justify="right")
        table.add_column("Amount", justify="right")
        table.add_column("P/L", justify="right")
        
        # Sample data - would be replaced with actual trading history
        table.add_row(
            "10:15:23", "BTC/USDT", "BUY", "$45,123.45", "0.1 BTC", "+2.3%"
        )
        table.add_row(
            "10:14:15", "ETH/USDT", "SELL", "$2,845.67", "1.5 ETH", "-1.2%"
        )
        
        console.print(table)

    async def main_menu(self, live: Live):
        """Main crypto trading interface"""
        while True:
            await self.display_trading_dashboard(live)
            
            questions = [
                {
                    'type': 'list',
                    'name': 'action',
                    'message': 'Crypto Trading Options:',
                    'choices': [
                        'Configure Trading Bot',
                        'View Active Bots',
                        'View Trading History',
                        'Market Analysis',
                        'Risk Management',
                        'Back to Main Menu'
                    ]
                }
            ]
            
            answers = await questionary.prompt(questions)
            
            if answers['action'] == 'Back to Main Menu':
                break
            elif answers['action'] == 'Configure Trading Bot':
                await self.configure_bot_parameters()
            elif answers['action'] == 'View Trading History':
                await self.view_trading_history()
            
            input("\nPress Enter to continue...")

    async def run(self):
        """Run the main application loop"""
        with Live(refresh_per_second=4) as live:
            await asyncio.gather(self.update_dashboard(live), self.main_menu(live))

if __name__ == "__main__":
    trader = CryptoTradingContract()
    asyncio.run(trader.run())
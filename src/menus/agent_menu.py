import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import logging
import asyncio
from src.banner import clear_terminal_preserve_banner

console = Console()

class AgentMenuManager:
    def __init__(self):
        self.active_agents = 0
        self.wallet_balance = "0.00"

    def display_status(self):
        clear_terminal_preserve_banner()
        console.print(Panel(f"""
[cyan]Agents' Status[/cyan]
• Active Agents: [yellow]{self.active_agents}[/yellow]
• Available Balance: [green]{self.wallet_balance} SOL[/green]
""", title="Agent Status"))

    async def web_designer_options(self):
        while True:
            self.display_status()
            result = await questionary.select(
                "Web Designer Options:",
                choices=[
                    'Create New Project',
                    'Generate Component Templates',
                    'Setup Build System',
                    'Configure Development Environment',
                    'Back'
                ]
            ).ask_async()
            
            if result == 'Back':
                break
                
            console.print("[yellow]Feature not implemented yet[/yellow]")
            await asyncio.sleep(1)

    async def crypto_trading_options(self):
        while True:
            self.display_status()
            result = await questionary.select(
                "Crypto Trading Options:",
                choices=[
                    'View Market Analysis',
                    'Set Trading Parameters',
                    'Start Trading Bot',
                    'View Trading History',
                    'Back'
                ]
            ).ask_async()
            
            if result == 'Back':
                break
                
            console.print("[yellow]Feature not implemented yet[/yellow]")
            await asyncio.sleep(1)

    async def robinhood_options(self):
        while True:
            self.display_status()
            result = await questionary.select(
                "Robinhood Trading Options:",
                choices=[
                    'Connect Account',
                    'View Positions',
                    'Place Order',
                    'Trading History',
                    'Back'
                ]
            ).ask_async()
            
            if result == 'Back':
                break
                
            console.print("[yellow]Feature not implemented yet[/yellow]")
            await asyncio.sleep(1)

    async def web_crawler_options(self):
        while True:
            self.display_status()
            result = await questionary.select(
                "Web Crawler Options:",
                choices=[
                    'Set Target URLs',
                    'Configure Crawler',
                    'Start Crawling',
                    'View Results',
                    'Back'
                ]
            ).ask_async()
            
            if result == 'Back':
                break
                
            console.print("[yellow]Feature not implemented yet[/yellow]")
            await asyncio.sleep(1)

    async def dark_web_options(self):
        while True:
            self.display_status()
            result = await questionary.select(
                "Dark Web Crawler Options:",
                choices=[
                    'Configure TOR',
                    'Set Search Parameters',
                    'Start Crawling',
                    'View Results',
                    'Back'
                ]
            ).ask_async()
            
            if result == 'Back':
                break
                
            console.print("[yellow]Feature not implemented yet[/yellow]")
            await asyncio.sleep(1)

    async def network_scanner_options(self):
        while True:
            self.display_status()
            result = await questionary.select(
                "Network Scanner Options:",
                choices=[
                    'Set Target Network',
                    'Configure Scan Type',
                    'Start Scanning',
                    'View Results',
                    'Back'
                ]
            ).ask_async()
            
            if result == 'Back':
                break
                
            console.print("[yellow]Feature not implemented yet[/yellow]")
            await asyncio.sleep(1)

    async def marketplace_menu(self):
        while True:
            self.display_status()
            result = await questionary.select(
                "Agent Marketplace:",
                choices=[
                    'View Available Agents',
                    'Deploy New Agent',
                    'My Active Bids',
                    'Agent History',
                    'Back'
                ]
            ).ask_async()
            
            if result == 'Back':
                break
                
            console.print("[yellow]Feature not implemented yet[/yellow]")
            await asyncio.sleep(1)

    async def run(self):
        try:
            while True:
                self.display_status()
                result = await questionary.select(
                    "Select Agent Type:",
                    choices=[
                        'Web Designer Agent',
                        'Crypto Trading Agent',
                        'Robinhood Trading Agent',
                        'Web Crawler Agent',
                        'Dark Web Crawler Agent',
                        'Network Scanner Agent',
                        'Agent Marketplace',
                        'Back to Main Menu'
                    ]
                ).ask_async()
                
                if result == 'Back to Main Menu':
                    break
                    
                agent_options = {
                    'Web Designer Agent': self.web_designer_options,
                    'Crypto Trading Agent': self.crypto_trading_options,
                    'Robinhood Trading Agent': self.robinhood_options,
                    'Web Crawler Agent': self.web_crawler_options,
                    'Dark Web Crawler Agent': self.dark_web_options,
                    'Network Scanner Agent': self.network_scanner_options,
                    'Agent Marketplace': self.marketplace_menu
                }
                
                if result in agent_options:
                    await agent_options[result]()
                
        except Exception as e:
            logging.error(f"Agent menu error: {str(e)}")
            console.print(f"[red]Error in agent menu: {str(e)}[/red]")
            await asyncio.sleep(2)

if __name__ == "__main__":
    async def main():
        menu = AgentMenu()
        await menu.run()
    
    asyncio.run(main())
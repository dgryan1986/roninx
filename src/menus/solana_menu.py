# src/menus/solana_menu.py

import questionary
from rich.console import Console
from rich.panel import Panel
import logging
import asyncio
from src.solana_manager import SolanaManager
from src.banner import clear_terminal_preserve_banner

console = Console()

class SolanaMenu:
    def __init__(self, solana_manager: SolanaManager):
        """
        Initialize the SolanaMenu with a SolanaManager instance.

        :param solana_manager: An instance of SolanaManager to handle Solana operations.
        """
        self.solana_manager = solana_manager
        self.wallet_balance = "0.00"

    def display_status(self):
        """Display the current status of the Solana wallet."""
        clear_terminal_preserve_banner()
        console.print(Panel(f"""
[cyan]Solana Wallet Status[/cyan]
• Network: [yellow]{self.solana_manager.network.upper()}[/yellow]
• Balance: [green]{self.wallet_balance} SOL[/green]
• Wallet: [cyan]{self.solana_manager.keypair.pubkey() if self.solana_manager.keypair else 'Not Loaded'}[/cyan]
""", title="Solana Status"))

    async def handle_wallet_creation(self):
        """Handle the workflow for creating a new Solana wallet."""
        try:
            wallet_info = await self.solana_manager.create_wallet()
            self.wallet_balance = str(await self.solana_manager.get_balance())
            return wallet_info
        except Exception as e:
            logging.error(f"Error creating wallet: {str(e)}")
            console.print(f"[red]Error creating wallet: {str(e)}[/red]")

    async def handle_wallet_loading(self):
        """Handle the workflow for loading an existing Solana wallet."""
        try:
            private_key = await questionary.text(
                "Enter private key:",
                password=True
            ).ask_async()
            await self.solana_manager.load_wallet(private_key)
            self.wallet_balance = str(await self.solana_manager.get_balance())
        except Exception as e:
            logging.error(f"Error loading wallet: {str(e)}")
            console.print(f"[red]Error loading wallet: {str(e)}[/red]")

    async def handle_balance_check(self):
        """Handle the workflow for checking the balance of a Solana address."""
        try:
            check_type = await questionary.select(
                "Check balance for:",
                choices=['My Wallet', 'Other Address']
            ).ask_async()
            
            if check_type == 'Other Address':
                address = await questionary.text("Enter Solana address:").ask_async()
                balance = await self.solana_manager.get_balance(address)
                console.print(f"[green]Balance: {balance} SOL[/green]")
            else:
                self.wallet_balance = str(await self.solana_manager.get_balance())
                console.print(f"[green]Your balance: {self.wallet_balance} SOL[/green]")
        except Exception as e:
            logging.error(f"Error checking balance: {str(e)}")
            console.print(f"[red]Error checking balance: {str(e)}[/red]")

    async def handle_transfer(self):
        """Handle the workflow for transferring SOL from the current wallet."""
        try:
            to_address = await questionary.text("Enter recipient's Solana address:").ask_async()
            amount = await questionary.float("Enter amount of SOL to transfer:").ask_async()
            
            confirm = await questionary.confirm(f"Send {amount} SOL to {to_address}?").ask_async()
            if confirm:
                await self.solana_manager.transfer_sol(to_address, amount)
                self.wallet_balance = str(await self.solana_manager.get_balance())
                console.print(f"[green]Transfer successful. New balance: {self.wallet_balance} SOL[/green]")
        except Exception as e:
            logging.error(f"Error transferring SOL: {str(e)}")
            console.print(f"[red]Error transferring SOL: {str(e)}[/red]")

    async def handle_token_deployment(self):
        """Handle the workflow for deploying a new Solana token."""
        try:
            token_info = await questionary.form(
                questions=[
                    {'type': 'text', 'name': 'name', 'message': 'Token Name:'},
                    {'type': 'text', 'name': 'symbol', 'message': 'Token Symbol:'},
                    {'type': 'number', 'name': 'decimals', 'message': 'Decimals (usually 9):', 'default': 9}
                ]
            ).ask_async()
            
            await self.solana_manager.create_token(
                token_info['name'],
                token_info['symbol'],
                int(token_info['decimals'])
            )
            console.print(f"[green]Token '{token_info['name']}' deployed successfully.[/green]")
        except Exception as e:
            logging.error(f"Error deploying token: {str(e)}")
            console.print(f"[red]Error deploying token: {str(e)}[/red]")

    async def handle_wallet_actions(self):
        """Handle wallet-related actions like creation or loading."""
        try:
            wallet_action = await questionary.select(
                "Wallet Options:",
                choices=['Create New Wallet', 'Load Existing Wallet']
            ).ask_async()
            
            if wallet_action == 'Create New Wallet':
                await self.handle_wallet_creation()
            else:
                await self.handle_wallet_loading()
        except Exception as e:
            logging.error(f"Error handling wallet actions: {str(e)}")
            console.print(f"[red]Error handling wallet actions: {str(e)}[/red]")

    async def handle_airdrop(self):
        """Handle the workflow for requesting an airdrop on Devnet."""
        try:
            amount = await questionary.float(
                "Enter amount of SOL to request (max 2):",
                validate=lambda x: 0 < float(x) <= 2
            ).ask_async()
            
            success = await self.solana_manager.airdrop(amount)
            if success:
                self.wallet_balance = str(await self.solana_manager.get_balance())
                console.print(f"[green]Airdrop successful! New balance: {self.wallet_balance} SOL[/green]")
            else:
                console.print("[red]Airdrop failed.[/red]")
        except Exception as e:
            logging.error(f"Error requesting airdrop: {str(e)}")
            console.print(f"[red]Error requesting airdrop: {str(e)}[/red]")

    async def handle_wallet_save(self):
        """Handle the workflow for saving the current wallet to a file."""
        try:
            filename = await questionary.text(
                "Enter filename to save wallet:",
                default="wallet.json"
            ).ask_async()
            
            await self.solana_manager.save_wallet(filename)
            console.print(f"[green]Wallet saved successfully to {filename}[/green]")
        except Exception as e:
            logging.error(f"Error saving wallet: {str(e)}")
            console.print(f"[red]Error saving wallet: {str(e)}[/red]")

    async def run(self):
        """Main Solana menu loop"""
        try:
            while True:
                self.display_status()
                result = await questionary.select(
                    "Solana Token Operations:",
                    choices=[
                        'Load/Create Wallet',
                        'Check Balance',
                        'Transfer SOL',
                        'Request Airdrop (Devnet)',
                        'Deploy New Token',
                        'Save Wallet',
                        'Back to Main Menu'
                    ]
                ).ask_async()
                
                if result == 'Back to Main Menu':
                    break
                    
                actions = {
                    'Load/Create Wallet': self.handle_wallet_actions,
                    'Check Balance': self.handle_balance_check,
                    'Transfer SOL': self.handle_transfer,
                    'Request Airdrop (Devnet)': self.handle_airdrop,
                    'Deploy New Token': self.handle_token_deployment,
                    'Save Wallet': self.handle_wallet_save
                }
                
                if result in actions:
                    await actions[result]()
                    await asyncio.sleep(2)  # Give time to read output
                    
        except Exception as e:
            logging.error(f"Solana menu error: {str(e)}")
            console.print(f"[red]Error in Solana menu: {str(e)}[/red]")
            await asyncio.sleep(2)
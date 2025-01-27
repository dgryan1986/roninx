import os
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import logging
import asyncio
from datetime import datetime
from src.banner import clear_terminal_preserve_banner
from src.irc.irc_core import IRCInterface, IRCClient
from src.menus.settings_menu import IdentityManager  # Fixed import path

console = Console()

import os
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import logging
import asyncio
from datetime import datetime
from src.banner import clear_terminal_preserve_banner
from src.irc.irc_core import IRCInterface
from src.menus.settings_menu import IdentityManager

console = Console()

class IRCMenu:
    def __init__(self):
        self.irc_interface = None
        self.solana_manager = None
        self.tor_manager = None
        self.identity_manager = IdentityManager()

    def get_current_nickname(self) -> str:
        """Get the current nickname based on identity settings"""
        if self.identity_manager.identity.use_wallet_address:
            if (self.solana_manager and hasattr(self.solana_manager, 'keypair') and 
                self.solana_manager.keypair is not None):
                return f"Agent_{str(self.solana_manager.keypair.pubkey())[:8]}"
            return f"Agent_{os.urandom(4).hex()}"
        
        # Use IRC username if set, otherwise fallback to random
        return (self.identity_manager.identity.irc_username or 
                f"Agent_{os.urandom(4).hex()}")

    def update_nickname(self):
        """Update IRC nickname based on current identity settings"""
        if not self.irc_interface or not self.irc_interface.client:
            return

        new_nick = self.get_current_nickname()
        if self.irc_interface.client.nickname != new_nick:
            self.irc_interface.client.nickname = new_nick
            if self.irc_interface.client.connected:
                asyncio.create_task(
                    self.irc_interface.client.send_raw(f"NICK {new_nick}")
                )

    def display_status(self):
        """Display current IRC status"""
        clear_terminal_preserve_banner()
        tor_status = "ENABLED" if self.tor_manager and self.tor_manager.onion_mode else "DISABLED"
        identity_mode = ("Wallet Address" if self.identity_manager.identity.use_wallet_address 
                        else "IRC Username")
        
        current_nickname = self.get_current_nickname()
        
        if self.irc_interface and self.irc_interface.client:
            console.print(Panel(f"""
[cyan]IRC Status[/cyan]
• Connection: [{'green' if self.irc_interface.client.connected else 'red'}]{'CONNECTED' if self.irc_interface.client.connected else 'DISCONNECTED'}[/{'green' if self.irc_interface.client.connected else 'red'}]
• Active Channels: [yellow]{len(self.irc_interface.client.channels)}[/yellow]
• Nickname: [cyan]{current_nickname}[/cyan]
• Identity Mode: [magenta]{identity_mode}[/magenta]
• Onion Routing: [cyan]{tor_status}[/cyan]
""", title="IRC Status"))

    async def run(self, solana_manager=None, tor_manager=None):
        """Initialize and run IRC menu with optional Solana and Tor managers"""
        try:
            self.solana_manager = solana_manager
            self.tor_manager = tor_manager
            
            while True:
                self.display_status()
                result = await questionary.select(
                    "IRC Communication:",
                    choices=[
                        'Launch IRC Client',
                        'Quick Connect',
                        'View Status',
                        'Identity Settings',
                        'Back to Main Menu'
                    ]
                ).ask_async()
                
                if result == 'Back to Main Menu':
                    break
                    
                if result == 'Launch IRC Client':
                    await self.launch_irc_client()
                elif result == 'Quick Connect':
                    await self.quick_connect()
                elif result == 'View Status':
                    await self.view_status()
                elif result == 'Identity Settings':
                    await self.manage_identity()
                
                await asyncio.sleep(1)
                
        except Exception as e:
            logging.error(f"IRC menu error: {str(e)}")
            console.print(f"[red]Error: {str(e)}[/red]")
            await asyncio.sleep(2)

    async def manage_identity(self):
        """Quick access to identity settings"""
        current_mode = "Wallet Address" if self.identity_manager.identity.use_wallet_address else "IRC Username"
        current_username = self.identity_manager.identity.irc_username or "[Not Set]"
        
        console.print(Panel(f"""
Current Settings:
• Identity Mode: [cyan]{current_mode}[/cyan]
• IRC Username: [cyan]{current_username}[/cyan]
"""))
        
        result = await questionary.select(
            "Identity Settings:",
            choices=[
                'Change Identity Mode',
                'Set IRC Username',
                'Back'
            ]
        ).ask_async()
        
        if result == 'Change Identity Mode':
            use_wallet = await questionary.confirm(
                "Use wallet address as identity?",
                default=self.identity_manager.identity.use_wallet_address
            ).ask_async()
            
            self.identity_manager.identity.use_wallet_address = use_wallet
            self.identity_manager.save_identity()
            self.update_nickname()
            
        elif result == 'Set IRC Username':
            username = await questionary.text(
                "Enter IRC username (3-16 alphanumeric characters):",
                validate=lambda x: len(x) >= 3 and len(x) <= 16 and x.isalnum()
            ).ask_async()
            
            if await questionary.confirm(f"Set IRC username to '{username}'?").ask_async():
                self.identity_manager.identity.irc_username = username
                self.identity_manager.save_identity()
                if not self.identity_manager.identity.use_wallet_address:
                    self.update_nickname()

    async def launch_irc_client(self):
        """Launch the full-screen IRC client interface"""
        try:
            # Initialize the interface if not already done
            if not self.irc_interface:
                self.irc_interface = IRCInterface()
                self.update_nickname()  # Set initial nickname based on identity settings
                
                # Configure Tor if enabled
                if self.tor_manager and self.tor_manager.onion_mode:
                    self.irc_interface.client.use_tor = True
                    self.irc_interface.client.tor_manager = self.tor_manager
            
            # Launch the full-screen interface
            await self.irc_interface.run()
            
        except Exception as e:
            logging.error(f"Failed to launch IRC client: {str(e)}")
            console.print(f"[red]Error launching IRC client: {str(e)}[/red]")

    async def quick_connect(self):
        """Quick connect to a server without full interface"""
        if not self.irc_interface:
            self.irc_interface = IRCInterface()
            self.update_nickname()  # Set nickname before connecting
        
        server = await questionary.text("Enter IRC server address:").ask_async()
        if not server:
            return
            
        channel = await questionary.text("Enter channel to join (optional):").ask_async()
        
        try:
            if await self.irc_interface.client.connect(server):
                console.print("[green]Successfully connected to server![/green]")
                
                if channel:
                    if not channel.startswith('#'):
                        channel = f"#{channel}"
                    await self.irc_interface.client.send_raw(f"JOIN {channel}")
                    console.print(f"[green]Joined channel {channel}[/green]")
            
        except Exception as e:
            console.print(f"[red]Connection failed: {str(e)}[/red]")

    # In IRCMenu class

    def display_status(self):
        clear_terminal_preserve_banner()
        is_tor = self.tor_manager and self.tor_manager.onion_mode
        
        status_text = f"""
    [{"purple" if is_tor else "cyan"}]IRC Status[/{"purple" if is_tor else "cyan"}]
    - Connection: [{'green' if self.irc_interface and self.irc_interface.client.connected else 'red'}]{'CONNECTED' if self.irc_interface and self.irc_interface.client.connected else 'DISCONNECTED'}[/{'green' if self.irc_interface and self.irc_interface.client.connected else 'red'}]
    - Active Channels: [yellow]{len(self.irc_interface.client.channels) if self.irc_interface and self.irc_interface.client else 0}[/yellow]
    - Nickname: [cyan]{self.get_current_nickname()}[/cyan]
    - Network Mode: [{'purple' if is_tor else 'cyan'}]{('Tor' if is_tor else 'Standard')}[/{'purple' if is_tor else 'cyan'}]
    """
        title = "[purple]IRC Status[/purple] [Tor Running]" if is_tor else "IRC Status"
        console.print(Panel(status_text, title=title))

    async def view_status(self):
        """Display detailed IRC status"""
        if not self.irc_interface or not self.irc_interface.client:
            console.print("[yellow]IRC client not initialized[/yellow]")
            return
            
        # Create status table
        table = Table(title="IRC Status")
        table.add_column("Setting")
        table.add_column("Value")
        
        client = self.irc_interface.client
        table.add_row("Connection Status", 
                     "[green]Connected[/green]" if client.connected else "[red]Disconnected[/red]")
        table.add_row("Nickname", client.nickname)
        table.add_row("Active Channels", str(len(client.channels)))
        table.add_row("Identity Mode", 
                     "Wallet Address" if self.identity_manager.identity.use_wallet_address 
                     else "IRC Username")
        table.add_row("IRC Username", 
                     self.identity_manager.identity.irc_username or "[Not Set]")
        table.add_row("Tor Mode", 
                     "[green]Enabled[/green]" if self.tor_manager and self.tor_manager.onion_mode 
                     else "[red]Disabled[/red]")
        
        console.print(table)
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    async def main():
        menu = IRCMenu()
        await menu.run()
    
    asyncio.run(main())
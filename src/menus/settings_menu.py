import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import logging
import asyncio
import json
import os
from dataclasses import dataclass
from src.banner import clear_terminal_preserve_banner

console = Console()

@dataclass
class AgentIdentity:
    use_wallet_address: bool = True
    irc_username: str = ""
    
    def to_dict(self):
        return {
            "use_wallet_address": self.use_wallet_address,
            "irc_username": self.irc_username
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            use_wallet_address=data.get("use_wallet_address", True),
            irc_username=data.get("irc_username", "")
        )

class IdentityManager:
    def __init__(self, config_path="config/identity.json", solana_manager=None):
        self.config_path = config_path
        self.solana_manager = solana_manager
        self.identity = self.load_identity()
    
    def load_identity(self) -> AgentIdentity:
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return AgentIdentity.from_dict(json.load(f))
        except Exception as e:
            logging.error(f"Error loading identity: {e}")
        return AgentIdentity()
    
    def save_identity(self):
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.identity.to_dict(), f, indent=2)
        except Exception as e:
            logging.error(f"Error saving identity: {e}")
            raise

    def get_active_identity(self) -> str:
        if self.identity.use_wallet_address:
            if self.solana_manager and hasattr(self.solana_manager, 'keypair') and self.solana_manager.keypair:
                return str(self.solana_manager.keypair.pubkey())
            return "<wallet_address>"
        return self.identity.irc_username or f"Agent_{os.urandom(4).hex()}"

class SettingsMenu:
    def __init__(self, solana_manager=None):
        self.solana_manager = solana_manager
        self.identity_manager = IdentityManager(solana_manager=solana_manager)
        self.irc_client = None
        self.wallet_balance = "0.00"
        self.active_agents = 0
        self.tor_manager = None

    def display_status(self):
        clear_terminal_preserve_banner()
        tor_status = "[purple]Tor Enabled[/purple]" if self.tor_manager and self.tor_manager.onion_mode else "Standard"
        
        status_text = f"""
[cyan]System Status[/cyan]
• Identity: [cyan]{self.identity_manager.get_active_identity()}[/cyan]
• Wallet Balance: [green]{self.wallet_balance} {"SOL" if not (self.tor_manager and self.tor_manager.onion_mode) else "BTC/XMR"}[/green]
• Active Agents: [yellow]{self.active_agents}[/yellow]
• Network Mode: {tor_status}
• Network: [green]{'CONNECTED' if self.irc_client and self.irc_client.connected else 'DISCONNECTED'}[/green]
"""
        console.print(Panel(status_text, title="Settings Status"))

    async def manage_identity(self):
        try:
            while True:
                self.display_status()
                result = await questionary.select(
                    "Identity Settings:",
                    choices=[
                        'Change Identity Mode',
                        'Set IRC Username',
                        'View Current Settings',
                        'Back'
                    ]
                ).ask_async()
                
                if result == 'Back':
                    break
                    
                if result == 'Change Identity Mode':
                    use_wallet = await questionary.confirm(
                        "Use wallet address as identity?",
                        default=self.identity_manager.identity.use_wallet_address
                    ).ask_async()
                    
                    self.identity_manager.identity.use_wallet_address = use_wallet
                    self.identity_manager.save_identity()
                    
                    if self.irc_client and self.irc_client.connected:
                        new_nick = self.identity_manager.get_active_identity()
                        self.irc_client.socket.send(f"NICK {new_nick}\r\n".encode())
                        self.irc_client.nickname = new_nick
                
                elif result == 'Set IRC Username':
                    username = await questionary.text(
                        "Enter IRC username (3-16 alphanumeric characters):",
                        validate=lambda x: len(x) >= 3 and len(x) <= 16 and x.isalnum()
                    ).ask_async()
                    
                    if await questionary.confirm(f"Set IRC username to '{username}'?").ask_async():
                        self.identity_manager.identity.irc_username = username
                        self.identity_manager.save_identity()
                        
                        if (self.irc_client and self.irc_client.connected and 
                            not self.identity_manager.identity.use_wallet_address):
                            self.irc_client.socket.send(f"NICK {username}\r\n".encode())
                            self.irc_client.nickname = username
                
                elif result == 'View Current Settings':
                    console.print(Panel(f"""[cyan]Current Identity Settings[/cyan]
• Identity Mode: {'Wallet Address' if self.identity_manager.identity.use_wallet_address else 'IRC Username'}
• IRC Username: {self.identity_manager.identity.irc_username or '[dim]Not Set[/dim]'}
• Active Display: {self.identity_manager.get_active_identity()}
""", title="Identity Configuration"))
                    input("\nPress Enter to continue...")
                
        except Exception as e:
            logging.error(f"Identity management error: {str(e)}")
            console.print(f"[red]Error managing identity: {str(e)}[/red]")

    async def manage_security(self):
        try:
            while True:
                self.display_status()
                result = await questionary.select(
                    "Security Settings:",
                    choices=[
                        'Change Password',
                        'Enable 2FA',
                        'View Security Log',
                        'Back'
                    ]
                ).ask_async()
                
                if result == 'Back':
                    break
                
                console.print("[yellow]Feature not implemented yet[/yellow]")
                await asyncio.sleep(1)
                
        except Exception as e:
            logging.error(f"Security settings error: {str(e)}")
            console.print(f"[red]Error in security settings: {str(e)}[/red]")

    async def manage_api(self):
        try:
            while True:
                self.display_status()
                result = await questionary.select(
                    "API Settings:",
                    choices=[
                        'Add API Key',
                        'Remove API Key',
                        'View API Keys',
                        'Back'
                    ]
                ).ask_async()
                
                if result == 'Back':
                    break
                
                console.print("[yellow]Feature not implemented yet[/yellow]")
                await asyncio.sleep(1)
                
        except Exception as e:
            logging.error(f"API settings error: {str(e)}")
            console.print(f"[red]Error in API settings: {str(e)}[/red]")

    async def run(self):
        try:
            while True:
                self.display_status()
                result = await questionary.select(
                    "Agent Settings:",
                    choices=[
                        'Identity Management',
                        'Security Settings',
                        'API Integration',
                        'General Configuration',
                        'Back to Main Menu'
                    ]
                ).ask_async()
                
                if result == 'Back to Main Menu':
                    break
                    
                actions = {
                    'Identity Management': self.manage_identity,
                    'Security Settings': self.manage_security,
                    'API Integration': self.manage_api,
                    'General Configuration': self.manage_general
                }
                
                if result in actions:
                    await actions[result]()
                
        except Exception as e:
            logging.error(f"Settings menu error: {str(e)}")
            console.print(f"[red]Error in settings menu: {str(e)}[/red]")

    async def manage_general(self):
        try:
            while True:
                self.display_status()
                result = await questionary.select(
                    "General Configuration:",
                    choices=[
                        'Change Theme',
                        'Toggle Notifications',
                        'Set Default Network',
                        'Back'
                    ]
                ).ask_async()
                
                if result == 'Back':
                    break
                
                console.print("[yellow]Feature not implemented yet[/yellow]")
                await asyncio.sleep(1)
                
        except Exception as e:
            logging.error(f"General settings error: {str(e)}")
            console.print(f"[red]Error in general settings: {str(e)}[/red]")

if __name__ == "__main__":
    async def main():
        menu = SettingsMenu()
        await menu.run()
    
    asyncio.run(main())
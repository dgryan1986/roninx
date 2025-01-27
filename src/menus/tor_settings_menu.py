from dataclasses import dataclass
from rich.console import Console
from rich.panel import Panel
import questionary
from questionary import Style
import logging
import asyncio
import json
import os
from typing import Optional

console = Console()

# Tor-specific style
tor_style = Style([
    ('question', 'fg:purple bold'),
    ('pointer', 'fg:purple bold'),
    ('highlighted', 'fg:purple bold'),
    ('selected', 'fg:purple bold'),
])

@dataclass
class TorIdentity:
    use_onion_address: bool = True
    irc_username: str = ""
    onion_services: list = None
    
    def __post_init__(self):
        if self.onion_services is None:
            self.onion_services = []
    
    def to_dict(self):
        return {
            "use_onion_address": self.use_onion_address,
            "irc_username": self.irc_username,
            "onion_services": self.onion_services
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            use_onion_address=data.get("use_onion_address", True),
            irc_username=data.get("irc_username", ""),
            onion_services=data.get("onion_services", [])
        )

class TorIdentityManager:
    def __init__(self, config_path="config/tor_identity.json"):
        self.config_path = config_path
        self.identity = self.load_identity()
    
    def load_identity(self) -> TorIdentity:
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return TorIdentity.from_dict(json.load(f))
        except Exception as e:
            logging.error(f"Error loading Tor identity: {e}")
        return TorIdentity()
    
    def save_identity(self):
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.identity.to_dict(), f, indent=2)
        except Exception as e:
            logging.error(f"Error saving Tor identity: {e}")
            raise

class TorSettingsMenu:
    def __init__(self):
        self.identity_manager = TorIdentityManager()
        self.irc_client = None
        self.crypto_balance = {"BTC": "0.00", "XMR": "0.00"}
        self.active_agents = 0

    def display_status(self):
        console.print(Panel(f"""
[purple]Tor System Status[/purple]
• Identity: [purple]{self.identity_manager.identity.irc_username or '<onion-address>'}[/purple]
• BTC Balance: [green]{self.crypto_balance['BTC']} BTC[/green]
• XMR Balance: [green]{self.crypto_balance['XMR']} XMR[/green]
• Active Agents: [yellow]{self.active_agents}[/yellow]
• Network: [purple]TOR ENABLED[/purple]
""", title="[purple]Tor Settings Status[/purple]"))

    async def manage_tor_identity(self):
        """Manage Tor-specific identity settings"""
        try:
            while True:
                self.display_status()
                result = await questionary.select(
                    "Tor Identity Settings:",
                    choices=[
                        'Change Identity Mode',
                        'Set IRC Username',
                        'Manage Onion Services',
                        'View Current Settings',
                        'Back'
                    ],
                    style=tor_style
                ).ask_async()
                
                if result == 'Back':
                    break
                    
                if result == 'Change Identity Mode':
                    use_onion = await questionary.confirm(
                        "Use .onion address as identity?",
                        default=self.identity_manager.identity.use_onion_address,
                        style=tor_style
                    ).ask_async()
                    
                    self.identity_manager.identity.use_onion_address = use_onion
                    self.identity_manager.save_identity()
                
                elif result == 'Set IRC Username':
                    username = await questionary.text(
                        "Enter IRC username (3-16 alphanumeric characters):",
                        validate=lambda x: len(x) >= 3 and len(x) <= 16 and x.isalnum(),
                        style=tor_style
                    ).ask_async()
                    
                    if await questionary.confirm(
                        f"Set IRC username to '{username}'?",
                        style=tor_style
                    ).ask_async():
                        self.identity_manager.identity.irc_username = username
                        self.identity_manager.save_identity()
                
                elif result == 'Manage Onion Services':
                    await self.manage_onion_services()
                
                elif result == 'View Current Settings':
                    console.print(Panel(f"""[purple]Current Tor Identity Settings[/purple]
• Identity Mode: {'Onion Address' if self.identity_manager.identity.use_onion_address else 'IRC Username'}
• IRC Username: {self.identity_manager.identity.irc_username or '[dim]Not Set[/dim]'}
• Active Onion Services: {len(self.identity_manager.identity.onion_services)}
""", title="[purple]Tor Identity Configuration[/purple]"))
                    input("\nPress Enter to continue...")

        except Exception as e:
            logging.error(f"Tor identity management error: {str(e)}")
            console.print(f"[red]Error managing Tor identity: {str(e)}[/red]")

    async def manage_onion_services(self):
        """Manage Tor hidden services"""
        try:
            while True:
                result = await questionary.select(
                    "Onion Services:",
                    choices=[
                        'View Active Services',
                        'Create New Service',
                        'Remove Service',
                        'Back'
                    ],
                    style=tor_style
                ).ask_async()
                
                if result == 'Back':
                    break
                
                elif result == 'View Active Services':
                    services = self.identity_manager.identity.onion_services
                    if not services:
                        console.print("[yellow]No active onion services[/yellow]")
                    else:
                        for service in services:
                            console.print(f"[purple]• {service}[/purple]")
                    await asyncio.sleep(2)

        except Exception as e:
            logging.error(f"Onion services error: {str(e)}")
            console.print(f"[red]Error managing onion services: {str(e)}[/red]")

    async def run(self):
        """Run the Tor settings menu"""
        try:
            while True:
                self.display_status()
                result = await questionary.select(
                    "Tor Agent Settings:",
                    choices=[
                        'Identity Management',
                        'Privacy Settings',
                        'Onion Services',
                        'Network Configuration',
                        'Back to Main Menu'
                    ],
                    style=tor_style
                ).ask_async()
                
                if result == 'Back to Main Menu':
                    break
                    
                actions = {
                    'Identity Management': self.manage_tor_identity,
                    'Privacy Settings': self.manage_privacy_settings,
                    'Onion Services': self.manage_onion_services,
                    'Network Configuration': self.manage_network_config
                }
                
                if result in actions:
                    await actions[result]()
                
        except Exception as e:
            logging.error(f"Tor settings menu error: {str(e)}")
            console.print(f"[red]Error in Tor settings menu: {str(e)}[/red]")

    async def manage_privacy_settings(self):
        """Manage privacy-specific settings"""
        try:
            while True:
                result = await questionary.select(
                    "Privacy Settings:",
                    choices=[
                        'Configure Privacy Level',
                        'Manage Cryptocurrency Settings',
                        'Back'
                    ],
                    style=tor_style
                ).ask_async()
                
                if result == 'Back':
                    break
                
                console.print("[yellow]Feature in development[/yellow]")
                await asyncio.sleep(1)
                
        except Exception as e:
            logging.error(f"Privacy settings error: {str(e)}")
            console.print(f"[red]Error in privacy settings: {str(e)}[/red]")

    async def manage_network_config(self):
        """Manage Tor network configuration"""
        try:
            while True:
                result = await questionary.select(
                    "Network Configuration:",
                    choices=[
                        'Bridge Configuration',
                        'Circuit Settings',
                        'Exit Node Preferences',
                        'Back'
                    ],
                    style=tor_style
                ).ask_async()
                
                if result == 'Back':
                    break
                
                console.print("[yellow]Feature in development[/yellow]")
                await asyncio.sleep(1)
                
        except Exception as e:
            logging.error(f"Network config error: {str(e)}")
            console.print(f"[red]Error in network configuration: {str(e)}[/red]")
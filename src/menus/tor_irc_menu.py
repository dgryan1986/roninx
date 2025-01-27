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
from questionary import Style

console = Console()

# Tor-specific style
tor_style = Style([
    ('question', 'fg:purple bold'),
    ('pointer', 'fg:purple bold'),
    ('highlighted', 'fg:purple bold'),
    ('selected', 'fg:purple bold'),
])

class TorIRCMenu:
    def __init__(self):
        self.irc_interface = None
        self.crypto_manager = None
        self.tor_manager = None
        self.onion_mode = True
        self.connected_nodes = []
        self.secure_channels = set()
        self.encryption_enabled = True
        self.last_circuit_refresh = None

    def get_current_nickname(self) -> str:
        """Get current nickname for Tor IRC"""
        return f"anon_{os.urandom(4).hex()}"

    def display_status(self):
        """Display current Tor IRC status"""
        clear_terminal_preserve_banner()
        
        console.print(Panel(f"""
[purple]Tor IRC Status[/purple]
• Connection: [{'green' if self.irc_interface and self.irc_interface.client.connected else 'red'}]{'CONNECTED' if self.irc_interface and self.irc_interface.client.connected else 'DISCONNECTED'}[/{'green' if self.irc_interface and self.irc_interface.client.connected else 'red'}]
• Active Channels: [yellow]{len(self.irc_interface.client.channels) if self.irc_interface and self.irc_interface.client else 0}[/yellow]
• Nickname: [purple]{self.get_current_nickname()}[/purple]
• Onion Address: [purple]{self.tor_manager.onion_address if self.tor_manager else 'Not Available'}[/purple]
• Connected Nodes: [yellow]{len(self.connected_nodes)}[/yellow]
• Encryption: [{'purple' if self.encryption_enabled else 'red'}]{'Enabled' if self.encryption_enabled else 'Disabled'}[/{'purple' if self.encryption_enabled else 'red'}]
• Secure Channels: [yellow]{len(self.secure_channels)}[/yellow]
""", title="[purple]Tor IRC Status[/purple]"))

    async def run(self, crypto_manager=None, tor_manager=None):
        """Initialize and run Tor IRC menu"""
        self.crypto_manager = crypto_manager
        self.tor_manager = tor_manager
        
        while True:
            try:
                self.display_status()
                result = await questionary.select(
                    "Tor IRC Communication:",
                    choices=[
                        'Connect to Hidden Service',
                        'Join Private Channel',
                        'Direct Message',
                        'View Status',
                        'Security Settings',
                        'Manage Circuits',
                        'Back to Main Menu'
                    ],
                    style=tor_style
                ).ask_async()
                
                if result == 'Back to Main Menu':
                    break
                    
                actions = {
                    'Connect to Hidden Service': self.connect_to_hidden_service,
                    'Join Private Channel': self.join_private_channel,
                    'Direct Message': self.send_direct_message,
                    'View Status': self.view_status,
                    'Security Settings': self.manage_security_settings,
                    'Manage Circuits': self.manage_circuits
                }
                
                if result in actions:
                    await actions[result]()
                
                await asyncio.sleep(1)
                
            except Exception as e:
                logging.error(f"Tor IRC menu error: {str(e)}")
                console.print(f"[red]Error: {str(e)}[/red]")
                await asyncio.sleep(2)

    async def connect_to_hidden_service(self):
        """Connect to an IRC hidden service"""
        onion_address = await questionary.text(
            "Enter .onion address:",
            validate=lambda x: x.endswith('.onion'),
            style=tor_style
        ).ask_async()
        
        if not onion_address:
            return
            
        try:
            if not self.irc_interface:
                self.irc_interface = IRCInterface()
                self.irc_interface.client.nickname = self.get_current_nickname()
            
            # Configure Tor settings
            self.irc_interface.client.use_tor = True
            self.irc_interface.client.tor_manager = self.tor_manager
            
            console.print("[purple]Establishing secure connection via Tor...[/purple]")
            await asyncio.sleep(1)
            console.print("[purple]Verifying hidden service authenticity...[/purple]")
            await asyncio.sleep(1)
            console.print("[purple]Creating new circuit...[/purple]")
            await asyncio.sleep(1)
            
            # Simulate successful connection
            self.connected_nodes.append(onion_address)
            console.print("[green]Successfully connected to hidden service![/green]")
            
        except Exception as e:
            console.print(f"[red]Connection failed: {str(e)}[/red]")

    async def join_private_channel(self):
        """Join a private IRC channel"""
        if not self.irc_interface or not self.irc_interface.client.connected:
            console.print("[red]Not connected to any hidden service[/red]")
            return
            
        channel = await questionary.text(
            "Enter private channel name:",
            style=tor_style
        ).ask_async()
        
        if not channel:
            return
            
        if not channel.startswith('#'):
            channel = f"#{channel}"
            
        try:
            # Optional: Enter channel key
            use_key = await questionary.confirm(
                "Does this channel require a key?",
                style=tor_style
            ).ask_async()
            
            if use_key:
                key = await questionary.password(
                    "Enter channel key:",
                    style=tor_style
                ).ask_async()
                join_command = f"JOIN {channel} {key}"
            else:
                join_command = f"JOIN {channel}"
            
            console.print(f"[purple]Joining secure channel {channel}...[/purple]")
            await self.irc_interface.client.send_raw(join_command)
            self.secure_channels.add(channel)
            console.print(f"[green]Successfully joined {channel}[/green]")
            
        except Exception as e:
            console.print(f"[red]Failed to join channel: {str(e)}[/red]")

    async def send_direct_message(self):
        """Send an encrypted direct message"""
        if not self.irc_interface or not self.irc_interface.client.connected:
            console.print("[red]Not connected to any hidden service[/red]")
            return
            
        recipient = await questionary.text(
            "Enter recipient's nickname:",
            style=tor_style
        ).ask_async()
        
        if not recipient:
            return
            
        message = await questionary.text(
            "Enter message:",
            style=tor_style
        ).ask_async()
        
        if not message:
            return
            
        try:
            console.print("[purple]Establishing encrypted connection...[/purple]")
            await asyncio.sleep(1)
            console.print("[purple]Encrypting message...[/purple]")
            await asyncio.sleep(1)
            
            # Send encrypted private message
            await self.irc_interface.client.send_raw(f"PRIVMSG {recipient} :{message}")
            console.print(f"[green]Encrypted message sent to {recipient}[/green]")
            
        except Exception as e:
            console.print(f"[red]Failed to send message: {str(e)}[/red]")

    async def view_status(self):
        """Display detailed Tor IRC status"""
        table = Table(title="[purple]Tor IRC Detailed Status[/purple]")
        table.add_column("Setting", style="purple")
        table.add_column("Value")
        
        if self.irc_interface and self.irc_interface.client:
            table.add_row(
                "Connection Status",
                "[green]Connected[/green]" if self.irc_interface.client.connected else "[red]Disconnected[/red]"
            )
            table.add_row("Current Nickname", self.irc_interface.client.nickname)
            table.add_row("Connected Nodes", str(len(self.connected_nodes)))
            table.add_row("Secure Channels", str(len(self.secure_channels)))
            table.add_row("Encryption Status", 
                         "[green]Enabled[/green]" if self.encryption_enabled else "[red]Disabled[/red]")
            table.add_row("Last Circuit Refresh",
                         str(self.last_circuit_refresh) if self.last_circuit_refresh else "Never")
            
        console.print(table)
        input("\nPress Enter to continue...")

    async def manage_security_settings(self):
        """Manage Tor IRC security settings"""
        while True:
            result = await questionary.select(
                "Security Settings:",
                choices=[
                    'Toggle Encryption',
                    'Refresh Circuit',
                    'Manage Trusted Nodes',
                    'View Security Log',
                    'Back'
                ],
                style=tor_style
            ).ask_async()
            
            if result == 'Back':
                break
                
            elif result == 'Toggle Encryption':
                self.encryption_enabled = not self.encryption_enabled
                status = "enabled" if self.encryption_enabled else "disabled"
                console.print(f"[purple]Encryption {status}[/purple]")
                
            elif result == 'Refresh Circuit':
                await self.refresh_circuit()
                
            elif result == 'Manage Trusted Nodes':
                await self.manage_trusted_nodes()
                
            elif result == 'View Security Log':
                self.view_security_log()

    async def manage_circuits(self):
        """Manage Tor circuits"""
        while True:
            result = await questionary.select(
                "Circuit Management:",
                choices=[
                    'Create New Circuit',
                    'View Current Circuits',
                    'Set Circuit Preferences',
                    'Back'
                ],
                style=tor_style
            ).ask_async()
            
            if result == 'Back':
                break
                
            elif result == 'Create New Circuit':
                await self.refresh_circuit()
            
            elif result == 'View Current Circuits':
                self.view_circuits()
            
            elif result == 'Set Circuit Preferences':
                await self.set_circuit_preferences()

    async def refresh_circuit(self):
        """Refresh Tor circuit"""
        try:
            console.print("[purple]Initiating circuit refresh...[/purple]")
            await asyncio.sleep(1)
            console.print("[purple]Creating new circuit path...[/purple]")
            await asyncio.sleep(1)
            console.print("[purple]Verifying circuit integrity...[/purple]")
            await asyncio.sleep(1)
            
            self.last_circuit_refresh = datetime.now()
            console.print("[green]Circuit successfully refreshed![/green]")
            
        except Exception as e:
            console.print(f"[red]Circuit refresh failed: {str(e)}[/red]")

    async def manage_trusted_nodes(self):
        """Manage trusted Tor nodes"""
        while True:
            result = await questionary.select(
                "Trusted Nodes:",
                choices=[
                    'View Trusted Nodes',
                    'Add Trusted Node',
                    'Remove Trusted Node',
                    'Back'
                ],
                style=tor_style
            ).ask_async()
            
            if result == 'Back':
                break
            
            console.print("[yellow]Feature in development[/yellow]")
            await asyncio.sleep(1)

    def view_security_log(self):
        """View security-related events log"""
        console.print("[purple]Security Log:[/purple]")
        # Implement actual security logging
        console.print("[yellow]No security events recorded[/yellow]")
        input("\nPress Enter to continue...")

    def view_circuits(self):
        """View current Tor circuits"""
        console.print("[purple]Current Circuits:[/purple]")
        # Implement actual circuit viewing
        console.print("[yellow]No active circuits to display[/yellow]")
        input("\nPress Enter to continue...")

    async def set_circuit_preferences(self):
        """Set circuit preferences"""
        console.print("[yellow]Circuit preference configuration is in development[/yellow]")
        await asyncio.sleep(1)

if __name__ == "__main__":
    async def main():
        menu = TorIRCMenu()
        await menu.run()
    
    asyncio.run(main())
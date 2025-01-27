from stem.control import Controller
from stem import CircStatus
from stem.util import term
from rich.console import Console
from rich.panel import Panel
import os
from enum import Enum
from typing import Optional, List

console = Console()

class NetworkMode(Enum):
    STANDARD = "standard"
    ONION = "onion"

class CryptoMode(Enum):
    SOLANA = "solana"
    PRIVACY = "privacy"  # BTC/XMR

class TorManager:
    def __init__(self, control_port=9051, password=None):
        self.control_port = control_port
        self.password = password
        self.onion_mode = False
        self.controller = None
        self.onion_address = None
        self.network_mode = NetworkMode.STANDARD
        self.crypto_mode = CryptoMode.SOLANA
        self.available_currencies: List[str] = ["SOL"]
        self.hidden_services = {}

    def connect_to_tor(self) -> bool:
        """Connect to Tor control port"""
        try:
            self.controller = Controller.from_port(port=self.control_port)
            if self.password:
                self.controller.authenticate(password=self.password)
            else:
                self.controller.authenticate()
            return True
        except Exception as e:
            console.print(f"[red]Failed to connect to Tor: {str(e)}[/red]")
            return False

    def create_hidden_service(self, port: int, target_port: int) -> Optional[str]:
        """Create a new hidden service for onion routing"""
        if not self.controller:
            if not self.connect_to_tor():
                return None
        
        hs_dir = os.path.join(os.getcwd(), 'hidden_service')
        if not os.path.exists(hs_dir):
            os.makedirs(hs_dir)
        try:
            # Create the hidden service with proper port mapping
            self.controller.create_ephemeral_hidden_service(
                {port: str(target_port)},
                await_publication=True
            )
            service = self.controller.get_hidden_service_conf(hs_dir)
            self.onion_address = service.hostname if service else None
            self.hidden_services[port] = service
            return self.onion_address
        except Exception as e:
            console.print(f"[red]Error creating hidden service: {str(e)}[/red]")
            return None

    def toggle_onion_mode(self, is_onion: bool) -> bool:
        """Toggle between Onion Mode and Standard Mode"""
        try:
            if is_onion:
                if not self.is_tor_running():
                    console.print("[red]Cannot enable Onion Mode - Tor is not running[/red]")
                    return False
                
                self.network_mode = NetworkMode.ONION
                self.crypto_mode = CryptoMode.PRIVACY
                self.available_currencies = ["BTC", "XMR"]
                self.onion_mode = True
                console.print("[cyan]Switching to Onion Mode - Privacy coins enabled[/cyan]")
                
                # Display network status after switch
                self.display_network_status()
                return True
            else:
                self.network_mode = NetworkMode.STANDARD
                self.crypto_mode = CryptoMode.SOLANA
                self.available_currencies = ["SOL"]
                self.onion_mode = False
                
                # Clean up any existing hidden services
                self._cleanup_hidden_services()
                
                console.print("[cyan]Switching to Standard Mode - Solana enabled[/cyan]")
                self.display_network_status()
                return True
                
        except Exception as e:
            console.print(f"[red]Error toggling network mode: {str(e)}[/red]")
            return False

    def _cleanup_hidden_services(self):
        """Clean up all hidden services when switching to standard mode"""
        if self.controller:
            try:
                for service in self.controller.list_ephemeral_hidden_services():
                    self.controller.remove_ephemeral_hidden_service(service)
                self.hidden_services.clear()
                self.onion_address = None
            except Exception as e:
                console.print(f"[yellow]Warning: Could not remove hidden services: {str(e)}[/yellow]")

    def is_tor_running(self) -> bool:
        """Check if Tor is running by attempting to connect"""
        return self.connect_to_tor()

    def display_network_status(self):
        """Display current network and cryptocurrency status"""
        console.print(Panel(f"""
[cyan]Network Status[/cyan]
- Mode: [yellow]{self.network_mode.value.upper()}[/yellow]
- Crypto Mode: [green]{self.crypto_mode.value.upper()}[/green]
- Available Currencies: [magenta]{', '.join(self.available_currencies)}[/magenta]
- Onion Address: [cyan]{self.onion_address or 'Not Available'}[/cyan]
- Tor Connection: [{'green' if self.is_tor_running() else 'red'}]{'CONNECTED' if self.is_tor_running() else 'DISCONNECTED'}[/{'green' if self.is_tor_running() else 'red'}]
""", title="Network Status"))

    def get_available_features(self) -> dict:
        """Get available features based on current network mode"""
        if self.network_mode == NetworkMode.ONION:
            return {
                "marketplace": "Privacy Marketplace (BTC/XMR)",
                "agents": ["Privacy Agents", "Anonymous Trading"],
                "currencies": self.available_currencies,
                "services": ["Hidden Services", "Anonymous Communication"]
            }
        else:
            return {
                "marketplace": "Standard Marketplace (SOL)",
                "agents": ["Public Agents", "Solana Trading"],
                "currencies": self.available_currencies,
                "services": ["Public Services", "Standard Communication"]
            }

    def __del__(self):
        """Cleanup on deletion"""
        try:
            if self.controller:
                self._cleanup_hidden_services()
                self.controller.close()
        except:
            pass
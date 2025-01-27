# src/menus/privacy_menus.py
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import asyncio
from questionary import Style

console = Console()

# Custom style for Tor mode
tor_style = Style([
    ('question', 'fg:purple bold'),
    ('pointer', 'fg:purple bold'),
    ('highlighted', 'fg:purple bold'),
    ('selected', 'fg:purple bold'),
])

async def privacy_token_menu(tor_manager):
    """Handle privacy token operations (BTC/XMR)"""
    while True:
        console.print(Panel(f"""
Privacy Token Operations
- Available Coins: [cyan]BTC, XMR[/cyan]
- Network Status: [green]Tor Enabled[/green]
- Onion Address: [yellow]{tor_manager.onion_address or 'Not Available'}[/yellow]
""", style="purple"))

        choices = [
            'BTC Operations [Tor Running]',
            'XMR Operations [Tor Running]',
            'View Balances [Tor Running]',
            'Back [Tor Running]'
        ]

        result = await questionary.select(
            "Select Privacy Token Operation:",
            choices=choices,
            style=tor_style
        ).ask_async()

        if result == 'Back [Tor Running]':
            break

async def privacy_agent_menu(tor_manager):
    """Handle privacy agents in Tor mode"""
    while True:
        console.print(Panel(f"""
Privacy Agents
- Network: [green]Tor Enabled[/green]
- Payment Methods: [cyan]BTC, XMR[/cyan]
""", style="purple"))

        choices = [
            'View Available Agents [Tor Running]',
            'Deploy New Agent [Tor Running]',
            'Manage Active Agents [Tor Running]',
            'Back [Tor Running]'
        ]

        result = await questionary.select(
            "Select Privacy Agent Operation:",
            choices=choices,
            style=tor_style
        ).ask_async()

        if result == 'Back [Tor Running]':
            break

async def onion_marketplace_menu(tor_manager):
    """Handle onion marketplace operations"""
    while True:
        console.print(Panel(f"""
Onion Marketplace
- Network: [green]Tor Enabled[/green]
- Payment Methods: [cyan]BTC, XMR[/cyan]
- Marketplace Status: [green]Active[/green]
""", style="purple"))

        choices = [
            'Browse Listings [Tor Running]',
            'Create Listing [Tor Running]',
            'View Orders [Tor Running]',
            'Back [Tor Running]'
        ]

        result = await questionary.select(
            "Select Marketplace Operation:",
            choices=choices,
            style=tor_style
        ).ask_async()

        if result == 'Back [Tor Running]':
            break
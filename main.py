import asyncio
from src.banner import display_startup_sequence
from src.menus.irc_menu import IRCMenu
from src.menus.settings_menu import SettingsMenu
from src.menus.solana_menu import SolanaMenu
from src.menus.agent_menu import AgentMenuManager
from src.menus.privacy_menus import (
    privacy_token_menu, 
    privacy_agent_menu, 
    onion_marketplace_menu
)
from src.menus.tor_settings_menu import TorSettingsMenu
from src.menus.tor_irc_menu import TorIRCMenu
from src.solana_manager import SolanaManager
from src.tor_manager import TorManager
import questionary
from questionary import Style
from rich.console import Console

console = Console()

tor_style = Style([
    ('question', 'purple bold'),
    ('pointer', 'purple bold'),
    ('highlighted', 'purple bold'),
    ('answer', 'purple bold'),
])

STANDARD_MODE_CHOICES = [
    'Available Agents',
    'Solana Token Operations',
    'Agent Marketplace',
    'Agent Settings',
    'IRC Communication',
    'Switch to Tor Mode',
    'Exit Terminal'
]

TOR_MODE_CHOICES = [
    'Privacy Agents',
    'Privacy Token Operations (BTC/XMR)',
    'Onion Marketplace',
    'Agent Settings',
    'IRC Communication',
    'Switch to Standard Mode',
    'Exit Terminal'
]

async def run_terminal(solana_manager, tor_manager):
    irc_menu = IRCMenu()
    settings_menu = SettingsMenu()
    solana_menu = SolanaMenu(solana_manager)
    agent_menu = AgentMenuManager()

    tor_irc_menu = TorIRCMenu()
    tor_settings_menu = TorSettingsMenu()

    while True:
        is_tor_mode = tor_manager.onion_mode
        
        if is_tor_mode:
            choices = [f"{choice} [Tor Running]" for choice in TOR_MODE_CHOICES]
            current_style = tor_style
        else:
            choices = STANDARD_MODE_CHOICES
            current_style = None

        result = await questionary.select(
            "Select Operation:",
            choices=choices,
            style=current_style
        ).ask_async()

        clean_result = result.replace(' [Tor Running]', '')
        
        if clean_result == 'Exit Terminal':
            console.print("[red]Terminating ICA Terminal session...[/red]")
            break

        if clean_result in ['Switch to Tor Mode', 'Switch to Standard Mode']:
            new_mode = clean_result == 'Switch to Tor Mode'
            if new_mode != tor_manager.onion_mode:
                if new_mode and not tor_manager.is_tor_running():
                    console.print("[red]Tor is not running. Please start Tor before enabling Tor Mode.[/red]")
                    continue
                
                if tor_manager.toggle_onion_mode(new_mode):
                    if new_mode:
                        onion_address = tor_manager.create_hidden_service(80, 8080)
                        if onion_address:
                            console.print(f"Your .onion address: [yellow]{onion_address}[/yellow]")
                            if solana_manager.keypair:
                                solana_manager.onion_address = solana_manager.wallet_to_onion(
                                    str(solana_manager.keypair.pubkey())
                                )
                                console.print(f"Wallet Onion Address Updated: [yellow]{solana_manager.onion_address}[/yellow]")
                    tor_manager.display_network_status()
                continue

        if is_tor_mode:
            try:
                if clean_result == 'Privacy Token Operations (BTC/XMR)':
                    await privacy_token_menu(tor_manager)
                elif clean_result == 'Privacy Agents':
                    await privacy_agent_menu(tor_manager)
                elif clean_result == 'Onion Marketplace':
                    await onion_marketplace_menu(tor_manager)
                elif clean_result == 'Agent Settings':
                    await tor_settings_menu.run()
                elif clean_result == 'IRC Communication':
                    await tor_irc_menu.run(solana_manager, tor_manager)
            except Exception as e:
                console.print(f"[red]Error in Tor mode operation: {str(e)}[/red]")

        else:
            try:
                menu_routes = {
                    'Available Agents': agent_menu.run,
                    'Solana Token Operations': solana_menu.run,
                    'Agent Marketplace': agent_menu.run,
                    'Agent Settings': settings_menu.run,
                    'IRC Communication': irc_menu.run,
                }
                
                if clean_result in menu_routes:
                    if clean_result in ['Agent Settings', 'Available Agents', 'Agent Marketplace']:
                        await menu_routes[clean_result]()
                    elif clean_result == 'Solana Token Operations':
                        await menu_routes[clean_result]()
                    else:
                        await menu_routes[clean_result](solana_manager, tor_manager)
            except Exception as e:
                console.print(f"[red]Error in standard mode operation: {str(e)}[/red]")

async def main():
    try:
        solana_manager = SolanaManager()
        tor_manager = TorManager()
        await solana_manager.initialize()
        await display_startup_sequence()
        await run_terminal(solana_manager, tor_manager)
    finally:
        await solana_manager.cleanup()
        if tor_manager.controller:
            tor_manager.controller.close()

if __name__ == "__main__":
    asyncio.run(main())
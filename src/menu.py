import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import logging
import asyncio
from typing import Dict, Optional, List
from dataclasses import dataclass

console = Console()

@dataclass
class Agent:
    id: str
    name: str
    type: str
    status: str
    reward: float
    description: str
    requirements: List[str]

class AgentMenuManager:
    def __init__(self, terminal):
        self.terminal = terminal
        self.active_agents: Dict[str, Agent] = {}
        self.available_agents: Dict[str, Agent] = self._initialize_agents()

    def _initialize_agents(self) -> Dict[str, Agent]:
        """Initialize available agents"""
        return {
            "web1": Agent(
                id="web1",
                name="Web Designer Agent",
                type="Web Designer",
                status="Available",
                reward=2.5,
                description="Complete redesign of corporate website with modern UI/UX",
                requirements=["React", "Tailwind CSS", "Responsive Design"]
            ),
            "crypto1": Agent(
                id="crypto1",
                name="Trading Bot Agent",
                type="Crypto Trading",
                status="Available",
                reward=3.0,
                description="Develop automated trading bot for major cryptocurrencies",
                requirements=["Python", "API Integration", "Risk Management"]
            ),
        }

    async def display_agent_details(self, agent: Agent):
        """Display detailed information about an agent"""
        console.print(Panel(f"""
[cyan]Agent Details[/cyan]
• ID: [yellow]{agent.id}[/yellow]
• Name: [green]{agent.name}[/green]
• Type: [blue]{agent.type}[/blue]
• Status: [magenta]{agent.status}[/magenta]
• Reward: [green]{agent.reward} SOL[/green]

[cyan]Description[/cyan]
{agent.description}

[cyan]Requirements[/cyan]
{"".join(f"• {req}\n" for req in agent.requirements)}
""", title=f"Agent: {agent.name}"))

    async def handle_agent_options(self, options: Dict[str, List[str]]):
        """Handle agent-specific options"""
        while True:
            self.terminal.display_status()
            result = await questionary.select(
                f"{options['title']} Options:",
                choices=options['choices']
            ).ask_async()

            if result == 'Back':
                break

            console.print(f"[yellow]Selected: {result} - Feature in development[/yellow]")
            await asyncio.sleep(1)

    async def web_designer_options(self):
        """Handle Web Designer agent options"""
        await self.handle_agent_options({
            'title': "Web Designer",
            'choices': [
                'Create New Project',
                'Generate Component Templates',
                'Setup Build System',
                'Configure Development Environment',
                'Back'
            ]
        })

    async def crypto_trading_options(self):
        """Handle Crypto Trading agent options"""
        await self.handle_agent_options({
            'title': "Crypto Trading",
            'choices': [
                'View Market Analysis',
                'Set Trading Parameters',
                'Start Trading Bot',
                'View Trading History',
                'Back'
            ]
        })

    async def view_agents(self, agents: Dict[str, Agent]):
        """Display agents in table format"""
        table = Table(title="Agents")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Type")
        table.add_column("Status")
        table.add_column("Reward")

        for agent in agents.values():
            table.add_row(
                agent.id,
                agent.name,
                agent.type,
                agent.status,
                f"{agent.reward} SOL"
            )
        console.print(table)
        
        if agents:
            agent_id = await questionary.select(
                "Select an agent for details:",
                choices=[*agents.keys(), 'Back']
            ).ask_async()
            
            if agent_id != 'Back':
                await self.display_agent_details(agents[agent_id])

    async def agents_menu(self):
        """Handle the agents submenu"""
        try:
            while True:
                self.terminal.display_status()
                result = await questionary.select(
                    "Select Agent Type:",
                    choices=[
                        'View Available Agents',
                        'Web Designer Agent',
                        'Crypto Trading Agent',
                        'Active Agents',
                        'Agent History',
                        'Back to Main Menu'
                    ]
                ).ask_async()

                if result == 'Back to Main Menu':
                    break

                elif result == 'View Available Agents':
                    await self.view_agents(self.available_agents)

                elif result == 'Web Designer Agent':
                    await self.web_designer_options()
                elif result == 'Crypto Trading Agent':
                    await self.crypto_trading_options()
                elif result == 'Active Agents':
                    if not self.active_agents:
                        console.print("[yellow]No active agents[/yellow]")
                    else:
                        await self.view_agents(self.active_agents)

                await asyncio.sleep(1)

        except Exception as e:
            logging.error(f"Agents menu error: {str(e)}")
            console.print(f"[red]Error in agents menu: {str(e)}[/red]")

    async def handle_marketplace_options(self, options: Dict[str, List[str]]):
        """Handle marketplace options"""
        while True:
            self.terminal.display_status()
            result = await questionary.select(
                f"{options['title']} Marketplace:",
                choices=options['choices']
            ).ask_async()

            if result == 'Back to Main Menu':
                break

            if result in options['choices']:
                console.print(f"[yellow]{result} - Feature in development[/yellow]")
            await asyncio.sleep(1)

    async def marketplace_menu(self):
        """Handle marketplace operations"""
        try:
            await self.handle_marketplace_options({
                'title': "Agent",
                'choices': [
                    'Browse Agents',
                    'Deploy New Agent',
                    'My Active Deployments',
                    'Agent History',
                    'Back to Main Menu'
                ]
            })
        except Exception as e:
            logging.error(f"Marketplace menu error: {str(e)}")
            console.print(f"[red]Error in marketplace: {str(e)}[/red]")
            await asyncio.sleep(2)
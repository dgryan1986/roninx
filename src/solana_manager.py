from solders.keypair import Keypair
from solders.pubkey import Pubkey as PublicKey
from solders.system_program import TransferParams, transfer
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
from spl.token.async_client import AsyncToken
from spl.token.constants import TOKEN_PROGRAM_ID
from rich.console import Console
from rich.panel import Panel
from typing import Optional, Dict
from src.client import SolanaClient
import base58
import json
import os
import asyncio
import hashlib
import base64

console = Console()

class SolanaManager:
    def __init__(self, network: str = "devnet"):
        self.network = network
        self.client = AsyncClient(self._get_network_url())
        self.keypair: Optional[Keypair] = None
        self.api_client = SolanaClient()
        self.onion_mode = False
        self.onion_address = None
        
    def _get_network_url(self) -> str:
        networks = {
            "devnet": "https://api.devnet.solana.com",
            "testnet": "https://api.testnet.solana.com",
            "mainnet": "https://api.mainnet-beta.solana.com"
        }
        return networks.get(self.network, networks["devnet"])
    
    async def initialize(self):
        """Initialize API client connection"""
        await self.api_client.connect()

    async def cleanup(self):
        """Cleanup API client connection"""
        await self.api_client.close()
    
    async def create_wallet(self) -> Dict:
        try:
            self.keypair = Keypair()
            wallet_info = {
                "public_key": str(self.keypair.pubkey()),
                "private_key": base58.b58encode(bytes(self.keypair.secret())).decode("ascii"),
                "network": self.network
            }
            console.print(Panel(f"""
[green]Wallet Created Successfully![/green]
- Network: [cyan]{self.network}[/cyan]
- Public Key: [yellow]{wallet_info['public_key']}[/yellow]
            """))
            return wallet_info
        except Exception as e:
            console.print(f"[red]Error creating wallet: {str(e)}[/red]")
            raise

    async def load_wallet(self, private_key: str) -> str:
        try:
            secret_key = base58.b58decode(private_key)
            self.keypair = Keypair.from_bytes(list(secret_key))
            public_key = str(self.keypair.pubkey())
            self.onion_address = self.wallet_to_onion(public_key)
            console.print(f"[green]Wallet loaded successfully: {public_key}[/green]")
            console.print(f"[cyan]Corresponding Onion Address: {self.onion_address}[/cyan]")
            return public_key
        except Exception as e:
            console.print(f"[red]Error loading wallet: {str(e)}[/red]")
            raise

    async def save_wallet(self, filepath: str = "wallet.json"):
        try:
            if not self.keypair:
                raise ValueError("No wallet to save")
                
            wallet_data = {
                "network": self.network,
                "public_key": str(self.keypair.pubkey()),
                "private_key": base58.b58encode(bytes(self.keypair.secret())).decode("ascii"),
                "onion_address": self.onion_address
            }
            
            os.makedirs("wallets", exist_ok=True)
            full_path = os.path.join("wallets", filepath)
            
            with open(full_path, "w") as f:
                json.dump(wallet_data, f, indent=2)
                
            console.print(f"[green]Wallet saved to {full_path}[/green]")
            
        except Exception as e:
            console.print(f"[red]Error saving wallet: {str(e)}[/red]")
            raise
    
    async def get_balance(self, public_key: Optional[str] = None) -> float:
        try:
            pubkey = PublicKey.from_string(public_key or str(self.keypair.pubkey()) if self.keypair else "")
            response = await self.client.get_balance(pubkey, commitment=Confirmed)
            return response.value / 1e9
        except ValueError as ve:
            if "No public key provided" in str(ve):
                console.print("[red]No public key provided and no wallet loaded.[/red]")
            else:
                console.print(f"[red]Error getting balance: {str(ve)}[/red]")
            raise
        except Exception as e:
            console.print(f"[red]Error getting balance: {str(e)}[/red]")
            raise
    
    async def transfer_sol(self, to_pubkey: str, amount: float, phone_number: Optional[str] = None) -> str:
        try:
            if not self.keypair:
                raise ValueError("Wallet not loaded")
            
            lamports = int(amount * 1e9)
            transfer_params = TransferParams(
                from_pubkey=self.keypair.pubkey(),
                to_pubkey=PublicKey(to_pubkey),
                lamports=lamports
            )
            transfer_ix = transfer(transfer_params)
            
            recent_blockhash = (await self.client.get_recent_blockhash(Confirmed))["result"]["value"]["blockhash"]
            
            transaction = Transaction()
            transaction.recent_blockhash = recent_blockhash
            transaction.add(transfer_ix)
            transaction.sign(self.keypair)
            
            opts = TxOpts(skip_preflight=False)
            result = await self.client.send_transaction(
                transaction,
                self.keypair,
                opts=opts
            )
            
            signature = result["result"]
            
            await self.api_client.send_transaction(
                str(self.keypair.pubkey()),
                amount,
                to_pubkey,
                phone_number
            )
            
            console.print(f"[green]Transaction sent! Signature: {signature}[/green]")
            if self.onion_mode:
                console.print(f"[cyan]Transaction routed through Onion Network: {self.onion_address}[/cyan]")
            return signature
            
        except Exception as e:
            console.print(f"[red]Error transferring SOL: {str(e)}[/red]")
            raise

    async def airdrop(self, amount: float = 1.0) -> bool:
        try:
            if not self.keypair:
                raise ValueError("Wallet not loaded")
            
            if self.network != "devnet":
                raise ValueError("Airdrops only available on devnet")
            
            lamports = int(amount * 1e9)
            result = await self.client.request_airdrop(
                self.keypair.pubkey(),
                lamports,
                Confirmed
            )
            
            if "result" in result:
                console.print(f"[green]Airdrop successful! Signature: {result['result']}[/green]")
                if self.onion_mode:
                    console.print(f"[cyan]Airdrop routed through Onion Network: {self.onion_address}[/cyan]")
                return True
            return False
            
        except Exception as e:
            console.print(f"[red]Error requesting airdrop: {str(e)}[/red]")
            return False
    
    async def create_token(self, name: str, symbol: str, decimals: int = 9) -> Dict:
        try:
            if not self.keypair:
                raise ValueError("Wallet not loaded")
                
            # Create token
            token = await AsyncToken.create_mint(
                self.client,
                self.keypair,
                self.keypair.pubkey(),
                decimals,
                TOKEN_PROGRAM_ID
            )
            
            token_data = {
                "name": name,
                "symbol": symbol,
                "decimals": decimals,
                "mint": str(token.pubkey),
                "authority": str(self.keypair.pubkey())
            }
            
            # Notify server about token creation
            await self.api_client.send_transaction(
                str(self.keypair.pubkey()),
                0,
                str(self.keypair.pubkey()),
                None,
                transaction_type="token_creation",
                metadata=token_data
            )
            
            console.print(Panel(f"""
    [green]Token Created Successfully![/green]
    • Name: [cyan]{name}[/cyan]
    • Symbol: [cyan]{symbol}[/cyan]
    • Decimals: [cyan]{decimals}[/cyan]
    • Mint Address: [yellow]{token_data['mint']}[/yellow]
            """))
            
            return token_data
        except Exception as e:
            console.print(f"[red]Error creating token: {str(e)}[/red]")
            raise

        # In solana_manager.py
    async def cleanup(self):
        """Cleanup API client connection"""
        await self.api_client.close()
        await self.client.close()  # Close the AsyncClient if it's open

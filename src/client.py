import aiohttp
import logging
from typing import Optional, Dict, Any

class SolanaClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def connect(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
            
    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None
            
    async def send_transaction(
        self,
        wallet_address: str,
        amount: float,
        recipient: str,
        phone_number: Optional[str] = None,
        transaction_type: str = "transfer",
        metadata: Optional[Dict[str, Any]] = None
    ):
        await self.connect()
        
        data = {
            "wallet_address": wallet_address,
            "amount": amount,
            "recipient": recipient,
            "phone_number": phone_number,
            "type": transaction_type
        }
        
        if metadata:
            data["metadata"] = metadata
            
        try:
            async with self.session.post(
                f"{self.base_url}/transaction",
                json=data
            ) as response:
                if response.status != 200:
                    logging.error(f"Transaction notification failed: {await response.text()}")
                return await response.json()
                
        except Exception as e:
            logging.error(f"Failed to notify server: {str(e)}")
            raise
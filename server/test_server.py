import asyncio
import websockets
import json
import aiohttp

async def test_rest_endpoint():
    async with aiohttp.ClientSession() as session:
        data = {
            "wallet_address": "test_wallet",
            "amount": 1.0,
            "recipient": "recipient_wallet",
            "phone_number": "+1234567890"
        }
        
        async with session.post("http://localhost:8000/transaction", json=data) as response:
            print(f"REST Response: {await response.json()}")

async def test_websocket():
    async with websockets.connect("ws://localhost:8000/ws/test_client") as ws:
        data = {
            "type": "transaction",
            "wallet": "test_wallet",
            "amount": 1.0,
            "recipient": "recipient_wallet"
        }
        await ws.send(json.dumps(data))
        response = await ws.recv()
        print(f"WebSocket Response: {response}")

async def main():
    await test_rest_endpoint()
    await test_websocket()

if __name__ == "__main__":
    asyncio.run(main())
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from twilio.rest import Client
from typing import Dict, Optional
import json
import asyncio
import logging
import os

# Initialize FastAPI
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Solana dApp location
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Twilio setup
twilio_client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

# Store active connections
connections: Dict[str, WebSocket] = {}

class TransactionRequest(BaseModel):
    wallet_address: str
    amount: float
    recipient: str
    phone_number: Optional[str]

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    connections[client_id] = websocket
    try:
        while True:
            data = await websocket.receive_json()
            # Handle different message types
            if data["type"] == "transaction":
                # Process transaction from Python CLI
                await handle_transaction(data, websocket)
            elif data["type"] == "notification":
                # Handle notifications
                await send_notification(data)
    except Exception as e:
        logging.error(f"WebSocket error: {e}")
    finally:
        connections.pop(client_id, None)

@app.post("/transaction")
async def create_transaction(request: TransactionRequest):
    try:
        # Validate transaction request
        if request.amount <= 0:
            raise HTTPException(status_code=400, detail="Invalid amount")

        # Notify connected dApp clients
        for ws in connections.values():
            await ws.send_json({
                "type": "new_transaction",
                "data": {
                    "wallet": request.wallet_address,
                    "amount": request.amount,
                    "recipient": request.recipient
                }
            })

        # Send SMS notification if phone number provided
        if request.phone_number:
            await send_sms(
                request.phone_number,
                f"New transaction: {request.amount} SOL to {request.recipient}"
            )

        return {"status": "success", "message": "Transaction processed"}

    except Exception as e:
        logging.error(f"Transaction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def handle_transaction(data: dict, websocket: WebSocket):
    try:
        # Process transaction logic
        # Add your Solana transaction code here
        response = {
            "type": "transaction_response",
            "status": "success",
            "data": data
        }
        await websocket.send_json(response)
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })

async def send_notification(data: dict):
    try:
        if data.get("phone_number"):
            await send_sms(
                data["phone_number"],
                data["message"]
            )
    except Exception as e:
        logging.error(f"Notification error: {e}")

async def send_sms(to_number: str, message: str):
    try:
        twilio_client.messages.create(
            body=message,
            from_=os.getenv("TWILIO_PHONE_NUMBER"),
            to=to_number
        )
    except Exception as e:
        logging.error(f"SMS error: {e}")
        raise

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect
import asyncio, random, json
from datetime import datetime

app = FastAPI()
clients = []
stocks = {
    "AAPL": 150,
    "MSFT": 300,
    "GOOGL": 2800,
    "TSLA": 700
}

# Serve HTML
@app.get("/")
async def get():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            # Update stock prices
            for stock in stocks:
                stocks[stock] += random.uniform(-5, 5)

            data = {
                "time": datetime.now().strftime("%H:%M:%S"),
                "stocks": stocks
            }

            # Broadcast to all clients
            for client in clients.copy():
                try:
                    await client.send_text(json.dumps(data))
                except WebSocketDisconnect:
                    clients.remove(client)

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        if websocket in clients:
            clients.remove(websocket)

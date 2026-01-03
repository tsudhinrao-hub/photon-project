from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio, random, json
from contextlib import asynccontextmanager

clients = []
stocks = {
    "AAPL": 150,
    "MSFT": 300,
    "GOOGL": 2800,
    "TSLA": 700
}

async def stream():
    while True:
        # Update stock prices
        for s in stocks:
            stocks[s] += random.uniform(-5, 5)

        # Send updates to all clients
        for c in clients.copy():
            try:
                await c.send_text(json.dumps(stocks))
            except WebSocketDisconnect:
                clients.remove(c)
            except Exception:
                clients.remove(c)

        await asyncio.sleep(1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(stream())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        await asyncio.Future()  # Keep connection alive
    except WebSocketDisconnect:
        if websocket in clients:
            clients.remove(websocket)

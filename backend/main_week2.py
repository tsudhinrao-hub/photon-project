from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
import asyncio, random, json
from contextlib import asynccontextmanager

app = FastAPI()
clients = []

async def stock_stream():
    price = 150
    while True:
        price += random.uniform(-2, 2)
        data = {"stock": "AAPL", "price": round(price, 2)}

        for client in clients.copy():
            try:
                await client.send_text(json.dumps(data))
            except WebSocketDisconnect:
                clients.remove(client)

        await asyncio.sleep(1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(stock_stream())
    yield

app = FastAPI(lifespan=lifespan)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        if websocket in clients:
            clients.remove(websocket)

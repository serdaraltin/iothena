from fastapi import FastAPI, WebSocket, Depends
from starlette.websockets import WebSocketDisconnect

from app.api.v1.base import BaseApi

class ConnectionManager:
    def __init__(self):
        BaseApi.__init__(self)
        self.active_connection: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connection.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connection.remove(websocket)

    @staticmethod
    async def send_message(message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connection:
            await connection.send_text(message)

connection_manager = ConnectionManager()

class WebsocketApi(BaseApi):
    def __init__(self):
        BaseApi.__init__(self)

    @staticmethod
    async def websocket_endpoint(websocket: WebSocket, client_id: int):
        await connection_manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                await connection_manager.send_message(f"You said: {data}", websocket)
                await connection_manager.broadcast(f"Client {client_id} said: {data}")
        except WebSocketDisconnect:
            connection_manager.disconnect(websocket)
            await connection_manager.broadcast(f"Client {client_id} disconnected")

    @staticmethod
    async def data(websocket: WebSocket):
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
            await websocket.close()


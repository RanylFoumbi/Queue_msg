
from typing import List, Optional
from starlette.websockets import WebSocket, WebSocketDisconnect

class SocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    def is_connected(self, websocket: WebSocket):
        return websocket in self.active_connections

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, socket: WebSocket):
        try:
            await socket.send_text(message)
        except WebSocketDisconnect:
            self.active_connections.remove(socket)
            
           
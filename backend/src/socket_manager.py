
import json
from typing import Dict
from .data_model import Message
from starlette.websockets import WebSocket, WebSocketDisconnect

class SocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    def is_connected(self, user_name: str):
        return user_name in self.active_connections.keys()

    async def connect(self,user_name: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_name] = websocket

    async def disconnect(self,user_name: str):
        print(f"Disconnecting {user_name}")
        self.active_connections.pop(user_name)

    async def send_message(self, body: str, socket: WebSocket, queue: str):
        message = Message.from_dict(json.loads(body))
        await socket.send_text(body)
        if message.content == "DISCONNECTION_MESSAGE" and message.user_name == queue:
            raise WebSocketDisconnect
           
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List
import pika

app = FastAPI()
EXCHANGE = 'chat'
EXCHANGE_TYPE = 'fanout'
RABBIT_MQ_HOST = 'rabbitmq'

class Message(BaseModel):
    content: str

class SocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = SocketManager()

@app.post("/send/")
async def send_message(message: Message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_MQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(
        exchange=EXCHANGE, 
        exchange_type=EXCHANGE_TYPE
    )
    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key='',
        body=message.content,
    )
    connection.close()
    return {"status": "message sent"}

@app.websocket("/receive/{user_name}")
async def receive_message(user_name: str, websocket: WebSocket):
    await manager.connect(websocket)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)
    result = channel.queue_declare(queue=user_name)
    queue_name = result.method.queue

    channel.queue_bind(exchange=EXCHANGE, queue=queue_name)

    while True:
        method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)
        try:
            await websocket.send_text(body.decode())
        except WebSocketDisconnect:
            manager.disconnect(websocket)

import asyncio
import pika
import json

from src.data_model import Message
from src.socket_manager import SocketManager
from src.constants import RABBIT_MQ_HOST, EXCHANGE, EXCHANGE_TYPE
from fastapi import FastAPI
from starlette.concurrency import run_in_threadpool
from starlette.websockets import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        body=json.dumps(message.to_dict()),
        properties=pika.BasicProperties( delivery_mode = pika.DeliveryMode.Persistent)
    )
    connection.close()
    return {"status": "message sent"}

@app.websocket("/receive/{user_name}")
async def receive_message(user_name: str, websocket: WebSocket):
    await manager.connect(user_name, websocket)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)
    channel.queue_declare(queue=user_name, durable=True)
    channel.queue_bind(exchange=EXCHANGE, queue=user_name)

    def callback(ch, method, properties, body):
        try:
            if manager.is_connected(user_name):
                asyncio.run(manager.send_message(body.decode('utf-8'), websocket, queue=user_name))
                ch.basic_ack(delivery_tag=method.delivery_tag)
        except WebSocketDisconnect:
            print(f"[x] Error {user_name}")
            asyncio.run(manager.disconnect(user_name))
                

    def consume():
        channel.basic_consume(queue=user_name, on_message_callback=callback, auto_ack=False)
        channel.start_consuming()
    await run_in_threadpool(consume)

@app.get("/users/")
async def get_users():
    return {"users": list(manager.active_connections.keys())}
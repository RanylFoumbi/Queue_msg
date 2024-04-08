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


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True, # Allows cookies
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
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
    await manager.connect(websocket)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)
    channel.queue_declare(queue=user_name, durable=True)
    channel.queue_bind(exchange=EXCHANGE, queue=user_name)

    def callback(ch, method, properties, body):
        try:
            if manager.is_connected(websocket):
                asyncio.run(manager.send_message(body.decode('utf-8'), websocket))
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except WebSocketDisconnect as e:
            print(f"[x] Error: {e}")
            manager.disconnect(websocket)
            connection.close()

    def consume():
        channel.basic_consume(queue=user_name, on_message_callback=callback, auto_ack=False)
        channel.start_consuming()
    await run_in_threadpool(consume)
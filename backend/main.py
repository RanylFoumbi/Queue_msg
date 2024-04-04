from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pika

app = FastAPI()
EXCHANGE = 'chat'
EXCHANGE_TYPE = 'fanout'
RABBIT_MQ_HOST = 'rabbitmq'

class Message(BaseModel):
    content: str

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

@app.get("/receive/")
async def receive_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE)
    result = channel.queue_declare(queue='')
    queue_name = result.method.queue

    channel.queue_bind(exchange=EXCHANGE, queue=queue_name)

    method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)
    if method_frame:
        print(f" [x] Received {body}")
        return {"message": body.decode()}
    else:
        return {"message": "No messages in queue"}
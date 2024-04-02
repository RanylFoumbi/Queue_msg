from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pika

app = FastAPI()

class Message(BaseModel):
    content: str

@app.post("/send/")
async def send_message(message: Message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='chat')
    channel.basic_publish(exchange='', routing_key='chat', body=message.content)
    connection.close()
    return {"status": "message sent"}

@app.get("/receive/")
async def receive_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='chat')
    method_frame, header_frame, body = channel.basic_get('chat')
    if method_frame:
        channel.basic_ack(method_frame.delivery_tag)
        return {"message": body.decode()}
    else:
        return {"message": "No messages in queue"}
import os
import pika
import json
import time

password= os.getenv("password")
hostname= os.getenv("hostname")

credentials= pika.PlainCredentials('user', password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='sample')

def callback(ch, method, properties, body):
    #ch.stop_consuming()
    user = json.loads(body)
    print('Received:', user)
    time.sleep(user['wait-duration'])

channel.basic_consume(queue='sample', auto_ack=True, on_message_callback=callback)

print('Start MQ Consuming')
channel.start_consuming()
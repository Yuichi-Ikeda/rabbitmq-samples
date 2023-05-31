import os
import pika
import json

password= os.getenv("password")
hostname= os.getenv("hostname")

credentials= pika.PlainCredentials('user', password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='sample')

# Set number of messages to send
for num in range(1000000):
    user = {
        'id': num,
        'name': 'sample1',
        'email': 'sample1@sample.com',
        'wait-duration': 300
    }
    channel.basic_publish(exchange='', routing_key='sample', body=json.dumps(user))

connection.close()
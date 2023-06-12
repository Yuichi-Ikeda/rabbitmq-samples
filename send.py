import os
import pika
import json
import uuid

password= os.getenv("password")
hostname= os.getenv("hostname")

credentials= pika.PlainCredentials('user', password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='sample', durable=True)

# JOB GUID for tracking
jobGUID = str(uuid.uuid4())
print('job-id: ' + jobGUID, flush=True)

# Set number of messages to send
for num in range(20):
    task = {
        'job-id': jobGUID,
        'task-id': num,
        'task': 'task for something',
        'wait-seconds': 30
    }
    channel.basic_publish(exchange='', 
                        routing_key='sample',
                        properties=pika.BasicProperties(delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE),
                        body=json.dumps(task))

connection.close()
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

# JOB ID for tracking
jobID = str(uuid.uuid4())
print('job-id: ' + jobID, flush=True)

# Set number of messages to send
for num in range(4000):
    task = {
        'job-id': jobID,
        'task-id': num,
        'task': 'task for something',
        'wait-seconds': 10
    }
    channel.basic_publish(exchange='', 
                        routing_key='sample',
                        properties=pika.BasicProperties(delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE),
                        body=json.dumps(task))

connection.close()
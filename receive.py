import os
import pika
import json
import time

password= os.getenv("password")
hostname= os.getenv("hostname")

credentials= pika.PlainCredentials('user', password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='sample', durable=True)
channel.basic_qos(prefetch_count=1)

def callback(ch, method, properties, body):
    task = json.loads(body)
    print('TASK_START:', task, flush=True)
    
    # Manual ack
    ch.basic_ack(delivery_tag = method.delivery_tag)
    
    # Wait for seconds for task simulation
    time.sleep(task['wait-seconds'])

    print('TASK_END:', task, flush=True)


channel.basic_consume(queue='sample', auto_ack=False, on_message_callback=callback)

print('Start MQ Consuming', flush=True)
channel.start_consuming()